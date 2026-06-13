"""Small PE-compatible dataset streams for raw CA episode exploration.

This module mirrors the dataset recipes used by the PE experiments without
copying their training-budget machinery. The default stream profile is compact
and visualization-friendly; callers can opt into PE-style rule pools and token
window sizing with ``profile="pe"``.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from math import ceil, prod
from typing import Any, Literal

import numpy as np

from . import frontiers, rng, rules, seeds
from .neighborhoods import dyadlags_0d, dyadrads_1d, dyadaxes_2d, dyadaxes_3d
from .rollout import rollout, rollout_batch
from .specs import Dynamics, RawBatch, RawEpisode


DatasetId = Literal["0d-dyadlags", "1d-dyadrads", "2d-dyadaxes", "3d-dyadaxes"]
StreamKind = Literal[
    "train",
    "held-out-rule",
    "held-out-seed",
    "ood-horizon",
    "ood-scale",
    "ood-boundary",
    "invariance",
]
StreamProfile = Literal["compact", "pe"]

DEFAULT_SPLIT = 0.8
DEFAULT_MAX_TOKENS = 2048
DEFAULT_COMPACT_COUNT = 8
DEFAULT_PE_COUNT = 64
DEFAULT_COMPACT_SPATIAL_STEPS = 17
DEFAULT_COMPACT_0D_STEPS = 128
DEFAULT_COMPACT_RULE_LIMIT = 8
SPECIAL_TOKENS_PER_EPISODE = 2
OOD_HORIZON_TOKEN_MULTIPLIER = 2
OOD_SCALE_TOKEN_MULTIPLIER = 2
OOD_SCALE_FACTORS_BY_RANK = {
    1: 2.0,
    2: 1.35,
    3: 1.4,
}


@dataclass(frozen=True)
class DatasetSpec:
    """PE-compatible raw CA dataset recipe."""

    id: str
    domain: str
    shape: tuple[int, ...]
    rule_family: str
    neighborhood_family: str
    seed_families: tuple[str, ...]
    boundary: Mapping[str, Any]


@dataclass(frozen=True)
class EpisodePlan:
    """One deterministic raw episode decision before seed rendering."""

    id: str
    dataset_id: str
    split: str
    kind: str
    profile: str
    episode_index: int
    rule_id: int
    episode_rng: int
    seed_stream_family: str
    seed_family: str
    seed_index: int | None
    shape: tuple[int, ...]
    steps: int
    boundary: Mapping[str, Any]
    transform: Mapping[str, Any] | None = None


DATASET_SPECS: dict[str, DatasetSpec] = {
    "0d-dyadlags": DatasetSpec(
        id="0d-dyadlags",
        domain="t+0d",
        shape=(),
        rule_family="dyadlags_0d",
        neighborhood_family="dyadlags_0d",
        seed_families=("uniform_bits",),
        boundary={"policy": "none"},
    ),
    "1d-dyadrads": DatasetSpec(
        id="1d-dyadrads",
        domain="t+1d",
        shape=(123,),
        rule_family="dyadrads_1d",
        neighborhood_family="dyadrads_1d",
        seed_families=("bernoulli", "structured"),
        boundary={"policy": "fixed", "value": 0},
    ),
    "2d-dyadaxes": DatasetSpec(
        id="2d-dyadaxes",
        domain="t+2d",
        shape=(11, 11),
        rule_family="dyadaxes_2d",
        neighborhood_family="dyadaxes_2d",
        seed_families=("bernoulli", "structured"),
        boundary={"policy": "fixed", "value": 0},
    ),
    "3d-dyadaxes": DatasetSpec(
        id="3d-dyadaxes",
        domain="t+3d",
        shape=(5, 5, 5),
        rule_family="dyadaxes_3d",
        neighborhood_family="dyadaxes_3d",
        seed_families=("bernoulli", "structured"),
        boundary={"policy": "fixed", "value": 0},
    ),
}
DATASET_IDS = tuple(DATASET_SPECS)


def get_spec(dataset_id: str) -> DatasetSpec:
    """Return one PE-compatible raw CA dataset spec."""

    try:
        return DATASET_SPECS[str(dataset_id)]
    except KeyError as exc:
        raise KeyError(f"unknown dataset {dataset_id!r}; expected one of {DATASET_IDS}") from exc


def rule_pools(dataset_id: str, *, split: float = DEFAULT_SPLIT) -> dict[str, tuple[int, ...]]:
    """Return PE-style train and held-out rule-id pools."""

    spec = get_spec(dataset_id)
    rule_count = rules.rule_count(_rule(spec))
    train_count = max(1, min(rule_count - 1, int(rule_count * float(split))))
    train = tuple(range(train_count))
    held_out_rule = tuple(range(train_count, rule_count)) or train[-1:]
    return {
        "all": tuple(range(rule_count)),
        "train": train,
        "held_out_rule": held_out_rule,
        "eval": held_out_rule,
    }


def plan_episode(
    dataset_id: str,
    *,
    episode_index: int = 0,
    split: str = "eval",
    kind: StreamKind = "held-out-seed",
    profile: StreamProfile = "compact",
    steps: int | None = None,
    shape: Sequence[int] | None = None,
    boundary: Mapping[str, Any] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
) -> EpisodePlan:
    """Plan one deterministic episode without rendering its seed or rollout."""

    spec = get_spec(dataset_id)
    profile = _validate_profile(profile)
    kind = _normalize_kind(kind)
    episode_index = int(episode_index)
    if episode_index < 0:
        raise ValueError(f"episode_index must be non-negative, got {episode_index}")

    split = "train" if kind == "train" else str(split)
    stream_shape = _resolve_shape(spec, kind, shape)
    stream_boundary = _resolve_boundary(spec, kind, episode_index, boundary)
    stream_steps = _resolve_steps(spec, kind, profile, stream_shape, steps, max_tokens)
    pool_name = _rule_pool_for_kind(kind)
    selected_rules = _selected_rule_ids(
        spec.id,
        pool_name=pool_name,
        profile=profile,
        split=split_fraction,
        rule_limit=rule_limit,
    )
    rule_id = selected_rules[episode_index % len(selected_rules)]
    seed_stream_family = _seed_stream_family(kind, split)
    episode_rng = rng.derive_episode_rng(
        {
            "policy": "splitmix64",
            "base_rng": stable_hash64(spec.id, split, seed_stream_family),
        },
        episode_index,
    )
    seed_family = _seed_family_for_episode(spec, episode_rng)
    seed_index = _structured_seed_index(seed_family, stream_shape, episode_rng)
    transform = _transform_for_kind(spec, kind, episode_index)

    return EpisodePlan(
        id=f"{spec.id}/{split}/{kind}/{episode_index:012d}",
        dataset_id=spec.id,
        split=split,
        kind=kind,
        profile=profile,
        episode_index=episode_index,
        rule_id=int(rule_id),
        episode_rng=int(episode_rng),
        seed_stream_family=seed_stream_family,
        seed_family=seed_family,
        seed_index=seed_index,
        shape=tuple(stream_shape),
        steps=int(stream_steps),
        boundary=dict(stream_boundary),
        transform=transform,
    )


def realize_episode(plan: EpisodePlan, *, return_coords: bool = True) -> RawEpisode:
    """Realize one planned episode as a ``RawEpisode``."""

    spec = get_spec(plan.dataset_id)
    seed_state = render_seed_state(plan)
    result = rollout(
        dynamics=_dynamics(spec, plan.shape, plan.boundary),
        rule_id=plan.rule_id,
        seed_state=seed_state,
        steps=plan.steps,
        return_coords=return_coords,
    )
    return RawEpisode(
        domain=result.domain,
        shape=result.shape,
        rule_id=result.rule_id,
        steps=result.steps,
        states=result.states,
        coords=result.coords,
        metadata={**_plan_metadata(plan), **dict(result.metadata or {})},
    )


def stream(
    dataset_id: str,
    *,
    split: str = "eval",
    kind: StreamKind = "held-out-seed",
    count: int | None = None,
    profile: StreamProfile = "compact",
    steps: int | None = None,
    shape: Sequence[int] | None = None,
    boundary: Mapping[str, Any] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
    start: int = 0,
    return_coords: bool = True,
) -> Iterator[RawEpisode]:
    """Yield deterministic raw episodes from a compact or PE-style stream."""

    total = _resolve_count(count, profile)
    for offset in range(total):
        plan = plan_episode(
            dataset_id,
            episode_index=int(start) + offset,
            split=split,
            kind=kind,
            profile=profile,
            steps=steps,
            shape=shape,
            boundary=boundary,
            max_tokens=max_tokens,
            split_fraction=split_fraction,
            rule_limit=rule_limit,
        )
        yield realize_episode(plan, return_coords=return_coords)


def stream_batch(
    dataset_id: str,
    *,
    split: str = "eval",
    kind: StreamKind = "held-out-seed",
    count: int | None = None,
    profile: StreamProfile = "compact",
    steps: int | None = None,
    shape: Sequence[int] | None = None,
    boundary: Mapping[str, Any] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
    batch_size: int | None = None,
    start: int = 0,
    return_coords: bool = True,
) -> Iterator[RawBatch]:
    """Yield deterministic raw episode batches where dynamics are shared."""

    spec = get_spec(dataset_id)
    total = _resolve_count(count, profile)
    rows = total if batch_size is None else max(1, int(batch_size))
    plans = [
        plan_episode(
            dataset_id,
            episode_index=int(start) + offset,
            split=split,
            kind=kind,
            profile=profile,
            steps=steps,
            shape=shape,
            boundary=boundary,
            max_tokens=max_tokens,
            split_fraction=split_fraction,
            rule_limit=rule_limit,
        )
        for offset in range(total)
    ]
    for chunk_start in range(0, len(plans), rows):
        chunk = plans[chunk_start : chunk_start + rows]
        for group in _contiguous_plan_groups(chunk):
            seed_states = np.stack([render_seed_state(plan) for plan in group], axis=0)
            result = rollout_batch(
                dynamics=_dynamics(spec, group[0].shape, group[0].boundary),
                rule_ids=np.asarray([plan.rule_id for plan in group], dtype=np.int64),
                seed_states=seed_states,
                steps=group[0].steps,
                return_coords=return_coords,
            )
            yield RawBatch(
                domain=result.domain,
                shape=result.shape,
                rule_ids=result.rule_ids,
                steps=result.steps,
                states=result.states,
                coords=result.coords,
                metadata={
                    "episodes": [_plan_metadata(plan) for plan in group],
                    **dict(result.metadata or {}),
                },
            )


def render_seed_state(plan: EpisodePlan) -> np.ndarray:
    """Render the initial seed state for one planned episode."""

    seed = _seed_for_plan(plan)
    return np.asarray(seeds.render(seed, plan.shape, rng=rng.numpy_rng(plan.episode_rng)), dtype=np.int64)


def stable_hash64(*parts: Any) -> int:
    """Return PE-compatible deterministic unsigned 64-bit hash."""

    payload = json.dumps(_json_ready(parts), sort_keys=True, separators=(",", ":"))
    digest = hashlib.blake2b(payload.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little")


def _validate_profile(profile: str) -> StreamProfile:
    if profile not in {"compact", "pe"}:
        raise ValueError("profile must be 'compact' or 'pe'")
    return profile  # type: ignore[return-value]


def _normalize_kind(kind: str) -> StreamKind:
    aliases = {
        "eval": "held-out-seed",
        "held_out_rule": "held-out-rule",
        "held_out_seed": "held-out-seed",
        "ood_horizon": "ood-horizon",
        "ood_scale": "ood-scale",
        "ood_boundary": "ood-boundary",
    }
    kind = aliases.get(str(kind), str(kind))
    valid = {
        "train",
        "held-out-rule",
        "held-out-seed",
        "ood-horizon",
        "ood-scale",
        "ood-boundary",
        "invariance",
    }
    if kind not in valid:
        raise ValueError(f"unknown stream kind {kind!r}")
    return kind  # type: ignore[return-value]


def _resolve_count(count: int | None, profile: str) -> int:
    resolved = DEFAULT_COMPACT_COUNT if count is None and profile == "compact" else count
    resolved = DEFAULT_PE_COUNT if resolved is None else resolved
    resolved = int(resolved)
    if resolved <= 0:
        raise ValueError(f"count must be positive, got {resolved}")
    return resolved


def _resolve_shape(
    spec: DatasetSpec,
    kind: str,
    override: Sequence[int] | None,
) -> tuple[int, ...]:
    if override is not None:
        return tuple(int(size) for size in override)
    if kind == "ood-scale" and spec.shape:
        return ood_scale_shape(spec.shape)
    return spec.shape


def _resolve_boundary(
    spec: DatasetSpec,
    kind: str,
    episode_index: int,
    override: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    if override is not None:
        return _normalize_boundary(override)
    if kind == "ood-boundary" and spec.shape:
        variants = ood_boundary_variants(spec)
        if variants:
            return variants[int(episode_index) % len(variants)]["boundary"]
    return dict(spec.boundary)


def _resolve_steps(
    spec: DatasetSpec,
    kind: str,
    profile: str,
    shape: Sequence[int],
    override: int | None,
    max_tokens: int,
) -> int:
    if override is not None:
        steps = int(override)
    elif profile == "pe":
        tokens = int(max_tokens)
        if kind == "ood-horizon":
            tokens *= OOD_HORIZON_TOKEN_MULTIPLIER
        elif kind == "ood-scale" and shape:
            tokens *= OOD_SCALE_TOKEN_MULTIPLIER
        steps = token_window_steps(shape, tokens)
    else:
        steps = DEFAULT_COMPACT_0D_STEPS if not spec.shape else DEFAULT_COMPACT_SPATIAL_STEPS
        if kind == "ood-horizon":
            steps *= OOD_HORIZON_TOKEN_MULTIPLIER
    if steps <= 0:
        raise ValueError(f"steps must be positive, got {steps}")
    return steps


def token_window_steps(
    shape: Sequence[int],
    max_tokens: int = DEFAULT_MAX_TOKENS,
    special_tokens_per_episode: int = SPECIAL_TOKENS_PER_EPISODE,
) -> int:
    """Return PE raw-state count for one serialized episode window."""

    shape_tuple = tuple(int(size) for size in shape)
    shape_size = int(prod(shape_tuple)) if shape_tuple else 1
    available = int(max_tokens) - int(special_tokens_per_episode)
    if available <= 0:
        raise ValueError("max_tokens must exceed special_tokens_per_episode")
    source_states = available // shape_size
    if source_states <= 0:
        raise ValueError(f"max_tokens={max_tokens} cannot fit one state for shape {shape_tuple}")
    return int(source_states + 1)


def _rule_pool_for_kind(kind: str) -> str:
    return "held_out_rule" if kind == "held-out-rule" else "train"


def _selected_rule_ids(
    dataset_id: str,
    *,
    pool_name: str,
    profile: str,
    split: float,
    rule_limit: int | None,
) -> tuple[int, ...]:
    pool = rule_pools(dataset_id, split=split)[pool_name]
    limit = rule_limit
    if limit is None and profile == "compact":
        limit = DEFAULT_COMPACT_RULE_LIMIT
    if limit is not None:
        limit = int(limit)
        if limit <= 0:
            raise ValueError(f"rule_limit must be positive, got {limit}")
        pool = pool[:limit]
    if not pool:
        raise ValueError(f"rule pool {pool_name!r} is empty")
    return pool


def _seed_stream_family(kind: str, split: str) -> str:
    if str(split) == "train" or kind == "train":
        return "train"
    return kind


def _seed_family_for_episode(spec: DatasetSpec, episode_rng: int) -> str:
    families = spec.seed_families
    return families[int(episode_rng) % len(families)]


def _structured_seed_index(seed_family: str, shape: Sequence[int], episode_rng: int) -> int | None:
    if seed_family != "structured":
        return None
    catalog = _structured_catalog(tuple(int(size) for size in shape))
    if not catalog:
        raise ValueError(f"structured seed catalog is empty for shape {tuple(shape)}")
    return int(episode_rng) % len(catalog)


def _seed_for_plan(plan: EpisodePlan) -> seeds.Seed:
    if plan.seed_family == "uniform_bits":
        return seeds.uniform_bits(length=3)
    if plan.seed_family == "bernoulli":
        return seeds.bernoulli(p_low=0.0, p_high=1.0)
    if plan.seed_family == "structured":
        catalog = _structured_catalog(plan.shape)
        seed_index = 0 if plan.seed_index is None else int(plan.seed_index)
        return catalog[seed_index % len(catalog)]
    raise ValueError(f"unknown seed family {plan.seed_family!r}")


@lru_cache(maxsize=None)
def _structured_catalog(shape: tuple[int, ...]) -> tuple[seeds.Seed, ...]:
    return tuple(seeds.structured(shape))


def _dynamics(spec: DatasetSpec, shape: Sequence[int], boundary: Mapping[str, Any]) -> Dynamics:
    return Dynamics(
        domain=spec.domain,
        shape=tuple(int(size) for size in shape),
        rule=_rule(spec),
        neighborhoods=(_neighborhood(spec),),
        frontier=frontiers.time_slice(shape),
        boundary=boundary,
        metadata={"dataset_id": spec.id},
    )


def _rule(spec: DatasetSpec) -> rules.Rule:
    if spec.rule_family == "dyadlags_0d":
        return rules.dyadlags_0d()
    if spec.rule_family == "dyadrads_1d":
        return rules.dyadrads_1d()
    if spec.rule_family == "dyadaxes_2d":
        return rules.dyadaxes_2d()
    if spec.rule_family == "dyadaxes_3d":
        return rules.dyadaxes_3d()
    raise ValueError(f"unsupported rule family {spec.rule_family!r}")


def _neighborhood(spec: DatasetSpec) -> Any:
    if spec.neighborhood_family == "dyadlags_0d":
        return dyadlags_0d()
    if spec.neighborhood_family == "dyadrads_1d":
        return dyadrads_1d()
    if spec.neighborhood_family == "dyadaxes_2d":
        return dyadaxes_2d()
    if spec.neighborhood_family == "dyadaxes_3d":
        return dyadaxes_3d()
    raise ValueError(f"unsupported neighborhood family {spec.neighborhood_family!r}")


def _contiguous_plan_groups(plans: Sequence[EpisodePlan]) -> Iterator[list[EpisodePlan]]:
    group: list[EpisodePlan] = []
    group_key: tuple[Any, ...] | None = None
    for plan in plans:
        key = _plan_dynamics_key(plan)
        if group and key != group_key:
            yield group
            group = []
        group.append(plan)
        group_key = key
    if group:
        yield group


def _plan_dynamics_key(plan: EpisodePlan) -> tuple[Any, ...]:
    boundary_key = tuple(sorted(dict(plan.boundary).items()))
    return plan.dataset_id, plan.shape, plan.steps, boundary_key


def _plan_metadata(plan: EpisodePlan) -> dict[str, Any]:
    metadata = {
        "dataset_id": plan.dataset_id,
        "episode_id": plan.id,
        "split": plan.split,
        "kind": plan.kind,
        "profile": plan.profile,
        "episode_index": plan.episode_index,
        "episode_rng": plan.episode_rng,
        "seed_stream_family": plan.seed_stream_family,
        "seed_family": plan.seed_family,
        "seed_index": plan.seed_index,
        "boundary": dict(plan.boundary),
    }
    if plan.transform is not None:
        metadata["transform"] = dict(plan.transform)
    return metadata


def ood_scale_shape(shape: Sequence[int]) -> tuple[int, ...]:
    """Return PE-style larger spatial shape for OOD-scale streams."""

    shape_tuple = tuple(int(size) for size in shape)
    if not shape_tuple:
        return shape_tuple
    factor = OOD_SCALE_FACTORS_BY_RANK.get(len(shape_tuple))
    if factor is None:
        raise ValueError(f"cannot build OOD-scale shape for rank {len(shape_tuple)}")
    return tuple(_odd_ceil(max(size + 1, size * factor)) for size in shape_tuple)


def ood_boundary_variants(spec: DatasetSpec | str) -> tuple[dict[str, Any], ...]:
    """Return PE-style OOD boundary variants for one spatial dataset."""

    if isinstance(spec, str):
        spec = get_spec(spec)
    if not spec.shape:
        return ()
    base = _normalize_boundary(spec.boundary)
    variants = []
    for boundary in ({"policy": "periodic"}, {"policy": "reflective"}):
        normalized = _normalize_boundary(boundary)
        if normalized != base:
            variants.append({"id": f"boundary-{normalized['policy']}", "boundary": normalized})
    return tuple(variants)


def invariance_transforms(spec: DatasetSpec | str) -> tuple[dict[str, Any], ...]:
    """Return PE-style coordinate transform metadata for invariance streams."""

    if isinstance(spec, str):
        spec = get_spec(spec)
    shape = spec.shape
    axes = ("x", "y", "z")[: len(shape)]
    if not axes:
        return (affine_transform("time-shift-pos-17", offset=(17, 0, 0, 0)),)

    transforms: list[dict[str, Any]] = []
    if len(axes) == 1:
        transforms.append(affine_transform("reflect-x", matrix=reflection_matrix(("x",))))
    elif len(axes) == 2:
        transforms.extend(
            affine_transform(f"rot-xy-{quarter_turns * 90}", matrix=rotation_matrix("xy", quarter_turns))
            for quarter_turns in (1, 2, 3)
        )
    else:
        for plane, axis in (("yz", "x"), ("xz", "y"), ("xy", "z")):
            transforms.extend(
                affine_transform(f"rot-{axis}-{quarter_turns * 90}", matrix=rotation_matrix(plane, quarter_turns))
                for quarter_turns in (1, 2, 3)
            )
    transforms.extend(axis_shift_transforms(shape))
    transforms.extend(diagonal_shift_transforms(shape))
    return tuple(_dedupe_affine_transforms(transforms))


def _transform_for_kind(spec: DatasetSpec, kind: str, episode_index: int) -> Mapping[str, Any] | None:
    if kind != "invariance":
        return None
    transforms = invariance_transforms(spec)
    if not transforms:
        return None
    return transforms[int(episode_index) % len(transforms)]


AXIS_COLUMNS = {"t": 0, "x": 1, "y": 2, "z": 3}


def affine_transform(
    transform_id: str,
    *,
    matrix: Sequence[Sequence[int]] | None = None,
    offset: Sequence[int] = (0, 0, 0, 0),
) -> dict[str, Any]:
    matrix = identity_matrix() if matrix is None else matrix
    return {
        "id": str(transform_id),
        "family": "affine",
        "matrix": [[int(value) for value in row] for row in matrix],
        "offset": [int(value) for value in offset],
    }


def identity_matrix() -> list[list[int]]:
    return [[1 if row == column else 0 for column in range(4)] for row in range(4)]


def reflection_matrix(axes: Sequence[str]) -> list[list[int]]:
    matrix = identity_matrix()
    for axis in axes:
        matrix[AXIS_COLUMNS[str(axis)]][AXIS_COLUMNS[str(axis)]] = -1
    return matrix


def rotation_matrix(plane: str, quarter_turns: int) -> list[list[int]]:
    first = AXIS_COLUMNS[plane[0]]
    second = AXIS_COLUMNS[plane[1]]
    step = identity_matrix()
    step[first][first] = 0
    step[first][second] = -1
    step[second][first] = 1
    step[second][second] = 0
    matrix = identity_matrix()
    for _ in range(int(quarter_turns) % 4):
        matrix = multiply_matrices(step, matrix)
    return matrix


def multiply_matrices(left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]) -> list[list[int]]:
    return [
        [
            sum(int(left[row][inner]) * int(right[inner][column]) for inner in range(4))
            for column in range(4)
        ]
        for row in range(4)
    ]


def axis_shift_transforms(shape: Sequence[int]) -> tuple[dict[str, Any], ...]:
    transforms = []
    for axis, size in zip(("x", "y", "z")[: len(shape)], shape, strict=True):
        half = ceil(int(size) / 2)
        for distance_name, amount in (("half", half), ("full", int(size))):
            for sign_name, sign in (("pos", 1), ("neg", -1)):
                transforms.append(
                    affine_transform(
                        f"shift-{axis}-{distance_name}-{sign_name}",
                        offset=axis_offset({axis: sign * amount}),
                    )
                )
    return tuple(transforms)


def diagonal_shift_transforms(shape: Sequence[int]) -> tuple[dict[str, Any], ...]:
    shape_by_axis = {
        axis: int(size)
        for axis, size in zip(("x", "y", "z")[: len(shape)], shape, strict=True)
    }
    transforms = []
    axes = tuple(shape_by_axis)
    for combo_size in range(2, len(axes) + 1):
        for axis_combo in itertools.combinations(axes, combo_size):
            for signs in itertools.product((-1, 1), repeat=combo_size):
                sign_label = "-".join("pos" if sign > 0 else "neg" for sign in signs)
                offsets = {
                    axis: int(sign) * shape_by_axis[axis]
                    for axis, sign in zip(axis_combo, signs, strict=True)
                }
                transforms.append(
                    affine_transform(
                        f"shift-{''.join(axis_combo)}-full-{sign_label}",
                        offset=axis_offset(offsets),
                    )
                )
    return tuple(transforms)


def axis_offset(offsets: Mapping[str, int]) -> tuple[int, int, int, int]:
    out = [0, 0, 0, 0]
    for axis, amount in offsets.items():
        out[AXIS_COLUMNS[str(axis)]] = int(amount)
    return tuple(out)


def _dedupe_affine_transforms(transforms: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for transform in transforms:
        matrix = tuple(tuple(int(value) for value in row) for row in transform["matrix"])
        offset = tuple(int(value) for value in transform["offset"])
        key = (matrix, offset)
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(transform))
    return out


def _normalize_boundary(boundary: Mapping[str, Any] | None) -> dict[str, Any]:
    if not boundary:
        return {"policy": "none"}
    policy = str(boundary.get("policy", "none")).lower()
    if policy not in {"none", "fixed", "periodic", "reflective"}:
        raise ValueError(f"unknown boundary policy {policy!r}")
    out: dict[str, Any] = {"policy": policy}
    if policy == "fixed":
        out["value"] = int(boundary.get("value", 0))
    return out


def _odd_ceil(value: float) -> int:
    out = int(ceil(float(value)))
    return out + 1 if out % 2 == 0 else out


def _json_ready(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [_json_ready(item) for item in value]
    raise TypeError(f"cannot convert {type(value).__name__} to JSON")


__all__ = [
    "DATASET_IDS",
    "DATASET_SPECS",
    "DEFAULT_COMPACT_COUNT",
    "DEFAULT_COMPACT_RULE_LIMIT",
    "DEFAULT_COMPACT_SPATIAL_STEPS",
    "DEFAULT_COMPACT_0D_STEPS",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_PE_COUNT",
    "DEFAULT_SPLIT",
    "DatasetSpec",
    "DatasetId",
    "EpisodePlan",
    "StreamKind",
    "StreamProfile",
    "affine_transform",
    "get_spec",
    "invariance_transforms",
    "ood_boundary_variants",
    "ood_scale_shape",
    "plan_episode",
    "realize_episode",
    "render_seed_state",
    "rule_pools",
    "stable_hash64",
    "stream",
    "stream_batch",
    "token_window_steps",
]
