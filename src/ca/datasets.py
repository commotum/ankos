"""Deterministic downstream datasets built from ordinary simple programs.

This module owns experiment planning and explicit NumPy views.  A dataset ID
selects one of four program constructors; it never selects an executor, Rule
interpreter, semantic family, or catalog entry.  Every episode is traversed by
``ca.program.rollout`` and batching is only a loop-and-stack convenience.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, replace
from functools import lru_cache
from math import ceil, prod
from types import MappingProxyType
from typing import Literal, TypeAlias

import numpy as np

from . import alphabets, frontiers, loci, neighborhoods, program, rng, rules, seeds


DatasetId = Literal[
    "0d-dyadlags",
    "1d-dyadrads",
    "2d-dyadaxes",
    "3d-dyadaxes",
]
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
BoundaryPolicy = Literal["none", "fixed", "periodic", "reflective"]
DatasetMetadataValue: TypeAlias = str | int | float | bool | None

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
OOD_SCALE_FACTORS_BY_RANK = MappingProxyType({1: 2.0, 2: 1.35, 3: 1.4})
RULE_IDS = tuple(range(256))


@dataclass(frozen=True)
class BoundarySpec:
    """One closed dataset-level finite boundary choice."""

    policy: BoundaryPolicy
    value: bool | int | None = None

    def __post_init__(self) -> None:
        if self.policy == "fixed" and self.value is None:
            raise ValueError("a fixed boundary requires a value")
        if self.policy != "fixed" and self.value is not None:
            raise ValueError("only a fixed boundary carries a value")
        if self.policy == "fixed" and self.value not in (False, True, 0, 1):
            raise ValueError("binary dataset boundaries must be 0 or 1")


@dataclass(frozen=True)
class AffineTransform:
    """Presentation-only coordinate-transform identity."""

    id: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("transform id cannot be empty")


@dataclass(frozen=True)
class DatasetSpec:
    """One immutable downstream experiment recipe."""

    id: DatasetId
    domain: str
    shape: tuple[int, ...]
    seed_families: tuple[str, ...]
    boundary: BoundarySpec


@dataclass(frozen=True)
class EpisodePlan:
    """One deterministic construction decision before semantic rollout."""

    id: str
    dataset_id: DatasetId
    split: str
    kind: StreamKind
    profile: StreamProfile
    episode_index: int
    rule_id: int
    episode_rng: int
    seed_stream_family: str
    seed_family: str
    seed_index: int | None
    shape: tuple[int, ...]
    steps: int
    boundary: BoundarySpec
    transform: AffineTransform | None = None


@dataclass(frozen=True)
class DatasetEpisode:
    """One explicit dense tensor projection of a linear finite rollout."""

    states: np.ndarray
    coords: np.ndarray | None
    domain: str
    shape: tuple[int, ...]
    rule_id: int
    steps: int
    metadata: Mapping[str, DatasetMetadataValue] | None = None


@dataclass(frozen=True)
class DatasetBatch:
    """A downstream stack of compatible explicit episode projections."""

    states: np.ndarray
    coords: np.ndarray | None
    rule_ids: np.ndarray
    domain: str
    shape: tuple[int, ...]
    steps: int
    metadata: Mapping[str, DatasetMetadataValue] | None = None


_SPECS = (
    DatasetSpec(
        "0d-dyadlags",
        "t+0d",
        (),
        ("uniform_bits",),
        BoundarySpec("none"),
    ),
    DatasetSpec(
        "1d-dyadrads",
        "t+1d",
        (123,),
        ("bernoulli", "structured"),
        BoundarySpec("fixed", 0),
    ),
    DatasetSpec(
        "2d-dyadaxes",
        "t+2d",
        (11, 11),
        ("bernoulli", "structured"),
        BoundarySpec("fixed", 0),
    ),
    DatasetSpec(
        "3d-dyadaxes",
        "t+3d",
        (5, 5, 5),
        ("bernoulli", "structured"),
        BoundarySpec("fixed", 0),
    ),
)
DATASET_SPECS: Mapping[str, DatasetSpec] = MappingProxyType(
    {item.id: item for item in _SPECS}
)
DATASET_IDS = tuple(item.id for item in _SPECS)


def get_spec(dataset_id: str) -> DatasetSpec:
    """Return one of the four closed dataset recipes."""

    try:
        return DATASET_SPECS[str(dataset_id)]
    except KeyError as error:
        raise KeyError(
            f"unknown dataset {dataset_id!r}; expected one of {DATASET_IDS}"
        ) from error


def rule_pools(
    dataset_id: str,
    *,
    split: float = DEFAULT_SPLIT,
) -> dict[str, tuple[int, ...]]:
    """Return explicit train and held-out subsets of the finite 0..255 domain."""

    get_spec(dataset_id)
    if not 0.0 < float(split) < 1.0:
        raise ValueError("split must lie strictly between zero and one")
    train_count = max(1, min(255, int(256 * float(split))))
    train = RULE_IDS[:train_count]
    held_out = RULE_IDS[train_count:]
    return {
        "all": RULE_IDS,
        "train": train,
        "held_out_rule": held_out,
        "eval": held_out,
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
    boundary: BoundarySpec | Mapping[str, str | int | bool] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
) -> EpisodePlan:
    """Plan one episode without constructing or applying its program."""

    spec = get_spec(dataset_id)
    resolved_profile = _validate_profile(profile)
    resolved_kind = _normalize_kind(kind)
    index = int(episode_index)
    if index < 0:
        raise ValueError(f"episode_index must be non-negative, got {index}")

    resolved_split = "train" if resolved_kind == "train" else str(split)
    resolved_shape = _resolve_shape(spec, resolved_kind, shape)
    resolved_boundary = _resolve_boundary(
        spec, resolved_kind, index, boundary
    )
    resolved_steps = _resolve_steps(
        spec,
        resolved_kind,
        resolved_profile,
        resolved_shape,
        steps,
        max_tokens,
    )
    pool_name = "held_out_rule" if resolved_kind == "held-out-rule" else "train"
    selected_rules = _selected_rule_ids(
        spec.id,
        pool_name=pool_name,
        profile=resolved_profile,
        split=split_fraction,
        rule_limit=rule_limit,
    )
    rule_id = selected_rules[index % len(selected_rules)]
    seed_stream_family = (
        "train"
        if resolved_split == "train" or resolved_kind == "train"
        else resolved_kind
    )
    episode_rng = rng.derive_episode_rng(
        stable_hash64(spec.id, resolved_split, seed_stream_family),
        index,
    )
    seed_family = spec.seed_families[episode_rng % len(spec.seed_families)]
    seed_index = _structured_seed_index(
        seed_family, resolved_shape, episode_rng
    )
    transform = _transform_for_kind(spec, resolved_kind, index)

    return EpisodePlan(
        id=f"{spec.id}/{resolved_split}/{resolved_kind}/{index:012d}",
        dataset_id=spec.id,
        split=resolved_split,
        kind=resolved_kind,
        profile=resolved_profile,
        episode_index=index,
        rule_id=rule_id,
        episode_rng=episode_rng,
        seed_stream_family=seed_stream_family,
        seed_family=seed_family,
        seed_index=seed_index,
        shape=resolved_shape,
        steps=resolved_steps,
        boundary=resolved_boundary,
        transform=transform,
    )


def realize_episode(
    plan: EpisodePlan,
    *,
    return_coords: bool = True,
) -> DatasetEpisode:
    """Construct one ordinary program, traverse it, and project a dense view."""

    if plan.steps <= 0:
        raise ValueError("dataset episodes require at least one projected state")
    initial_seed = _seed_for_plan(plan)
    simple_program = _build_program(
        plan.dataset_id,
        rule=plan.rule_id,
        seed=initial_seed,
        shape=plan.shape,
        boundary=plan.boundary,
    )
    # Dataset ``steps`` counts projected states.  Semantic rollout counts
    # applications, so a root plus ``steps - 1`` successors has that length.
    result = program.rollout(simple_program, steps=plan.steps - 1)
    episode = _project_dataset_episode(
        result,
        domain=get_spec(plan.dataset_id).domain,
        shape=plan.shape,
        rule_id=plan.rule_id,
        steps=plan.steps,
    )
    metadata = MappingProxyType(_plan_metadata(plan))
    return replace(
        episode,
        coords=episode.coords if return_coords else None,
        metadata=metadata,
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
    boundary: BoundarySpec | Mapping[str, str | int | bool] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
    start: int = 0,
    return_coords: bool = True,
) -> Iterator[DatasetEpisode]:
    """Yield deterministic explicit views, one generic rollout at a time."""

    total = _resolve_count(count, profile)
    for offset in range(total):
        yield realize_episode(
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
            ),
            return_coords=return_coords,
        )


def stream_batch(
    dataset_id: str,
    *,
    split: str = "eval",
    kind: StreamKind = "held-out-seed",
    count: int | None = None,
    profile: StreamProfile = "compact",
    steps: int | None = None,
    shape: Sequence[int] | None = None,
    boundary: BoundarySpec | Mapping[str, str | int | bool] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    split_fraction: float = DEFAULT_SPLIT,
    rule_limit: int | None = None,
    batch_size: int | None = None,
    start: int = 0,
    return_coords: bool = True,
) -> Iterator[DatasetBatch]:
    """Yield loop-and-stack batches without a semantic batch executor."""

    total = _resolve_count(count, profile)
    rows = total if batch_size is None else int(batch_size)
    if rows <= 0:
        raise ValueError("batch_size must be positive")
    planned = tuple(
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
    )
    for chunk_start in range(0, len(planned), rows):
        episodes = tuple(
            realize_episode(plan, return_coords=return_coords)
            for plan in planned[chunk_start : chunk_start + rows]
        )
        yield _project_dataset_batch(episodes)


# ---------------------------------------------------------------------------
# Explicit ordinary program construction
# ---------------------------------------------------------------------------


def _build_program(
    dataset_id: DatasetId,
    *,
    rule: int,
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
    boundary: BoundarySpec,
) -> program.SimpleProgram[
    loci.FiniteConfiguration[bool],
    bool,
    frontiers.WritableCapabilities,
    neighborhoods.ReadableView[bool],
]:
    if dataset_id == "0d-dyadlags":
        return _build_0d_dyadlags_program(
            rule=rule, seed=seed, shape=shape, boundary=boundary
        )
    if dataset_id == "1d-dyadrads":
        return _build_1d_dyadrads_program(
            rule=rule, seed=seed, shape=shape, boundary=boundary
        )
    if dataset_id == "2d-dyadaxes":
        return _build_2d_dyadaxes_program(
            rule=rule, seed=seed, shape=shape, boundary=boundary
        )
    if dataset_id == "3d-dyadaxes":
        return _build_3d_dyadaxes_program(
            rule=rule, seed=seed, shape=shape, boundary=boundary
        )
    raise AssertionError(f"unreachable dataset id {dataset_id!r}")


def _build_0d_dyadlags_program(
    *,
    rule: int,
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
    boundary: BoundarySpec,
) -> program.SimpleProgram:
    """Build the five-field temporal binary lookup experiment."""

    if shape or boundary.policy != "none":
        raise ValueError("0d-dyadlags requires shape () and boundary none")
    _require_seed_boundary(seed, boundary)
    contract = seed.configuration_contract
    return program.SimpleProgram(
        seed=seed,
        alphabet=alphabets.boolean(),
        frontier=frontiers.everywhere(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        neighborhood=neighborhoods.dyadlags_0d(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        rule=rules.dyadlags_0d(rule=rule),
    )


def _build_1d_dyadrads_program(
    *,
    rule: int,
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
    boundary: BoundarySpec,
) -> program.SimpleProgram:
    """Build the five-field radius-one binary line experiment."""

    _require_grid_rank(shape, 1)
    _require_seed_boundary(seed, boundary)
    _require_seed_grid_shape(seed, shape)
    contract = seed.configuration_contract
    return program.SimpleProgram(
        seed=seed,
        alphabet=alphabets.boolean(),
        frontier=frontiers.everywhere(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        neighborhood=neighborhoods.dyadrads_1d(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        rule=rules.dyadrads_1d(rule=rule),
    )


def _build_2d_dyadaxes_program(
    *,
    rule: int,
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
    boundary: BoundarySpec,
) -> program.SimpleProgram:
    """Build the five-field binary square-grid experiment."""

    _require_grid_rank(shape, 2)
    _require_seed_boundary(seed, boundary)
    _require_seed_grid_shape(seed, shape)
    contract = seed.configuration_contract
    return program.SimpleProgram(
        seed=seed,
        alphabet=alphabets.boolean(),
        frontier=frontiers.everywhere(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        neighborhood=neighborhoods.dyadaxes_2d(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        rule=rules.dyadaxes_2d(rule=rule),
    )


def _build_3d_dyadaxes_program(
    *,
    rule: int,
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
    boundary: BoundarySpec,
) -> program.SimpleProgram:
    """Build the five-field binary cubic-grid experiment."""

    _require_grid_rank(shape, 3)
    _require_seed_boundary(seed, boundary)
    _require_seed_grid_shape(seed, shape)
    contract = seed.configuration_contract
    return program.SimpleProgram(
        seed=seed,
        alphabet=alphabets.boolean(),
        frontier=frontiers.everywhere(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        neighborhood=neighborhoods.dyadaxes_3d(
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        rule=rules.dyadaxes_3d(rule=rule),
    )


def _require_grid_rank(shape: tuple[int, ...], rank: int) -> None:
    if len(shape) != rank or any(size <= 0 for size in shape):
        raise ValueError(f"expected a positive rank-{rank} grid shape, got {shape}")


def _require_seed_boundary(
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    boundary: BoundarySpec,
) -> None:
    configuration = seed.denote().exact_configuration
    if not isinstance(configuration, loci.FiniteConfiguration):
        raise TypeError("dataset recipes require an exact finite Seed")
    if configuration.carrier.boundary != _loci_boundary(boundary):
        raise ValueError("dataset boundary and exact Seed boundary disagree")


def _require_seed_grid_shape(
    seed: seeds.Seed[loci.FiniteConfiguration[bool]],
    shape: tuple[int, ...],
) -> None:
    contract = seed.configuration_contract
    if contract.kind is not loci.CarrierKind.GRID or contract.shape != shape:
        raise ValueError("dataset shape and exact Seed grid shape disagree")


# ---------------------------------------------------------------------------
# Exact source preparation
# ---------------------------------------------------------------------------


def _seed_for_plan(
    plan: EpisodePlan,
) -> seeds.Seed[loci.FiniteConfiguration[bool]]:
    generator = rng.numpy_rng(plan.episode_rng)
    if plan.seed_family == "uniform_bits":
        values = tuple(bool(value) for value in generator.integers(2, size=3))
        configuration = loci.history_configuration(values)
        return seeds.exact(
            configuration, value_profile=alphabets.ValueProfile.BOOLEAN
        )
    if plan.seed_family == "bernoulli":
        probability = float(generator.random())
        values = tuple(
            bool(value)
            for value in (generator.random(int(prod(plan.shape))) < probability)
        )
        configuration = loci.grid_configuration(
            plan.shape,
            values,
            boundary=_loci_boundary(plan.boundary),
        )
        return seeds.exact(
            configuration, value_profile=alphabets.ValueProfile.BOOLEAN
        )
    if plan.seed_family == "structured":
        recipes = _structured_seed_recipes(plan.shape)
        index = 0 if plan.seed_index is None else plan.seed_index
        chosen = recipes[index % len(recipes)]
        source = chosen.denote().exact_configuration
        targets = loci.grid_loci(plan.shape)
        configuration = loci.grid_configuration(
            plan.shape,
            tuple(bool(source.value_at(target)) for target in targets),
            boundary=_loci_boundary(plan.boundary),
        )
        return seeds.exact(
            configuration, value_profile=alphabets.ValueProfile.BOOLEAN
        )
    raise ValueError(f"unknown seed family {plan.seed_family!r}")


@lru_cache(maxsize=None)
def _structured_seed_recipes(
    shape: tuple[int, ...],
) -> tuple[seeds.Seed[loci.FiniteConfiguration[bool]], ...]:
    """Enumerate a compact, dimension-polymorphic exact pattern catalog."""

    _require_grid_rank(shape, len(shape))
    coordinates = tuple(
        loci.grid_coordinates(target) for target in loci.grid_loci(shape)
    )
    predicates = [
        lambda point: all(value == 0 for value in point),
        lambda point: sum(abs(value) for value in point) <= 1,
        lambda point: max(abs(value) for value in point) <= 1,
        lambda point: sum(point) % 2 == 0,
        lambda point: point[0] >= 0,
    ]
    predicates.extend(
        (lambda point, axis=axis: point[axis] == 0)
        for axis in range(len(shape))
    )
    if len(shape) >= 2:
        predicates.append(lambda point: point[0] == point[1])
        predicates.append(lambda point: point[0] == -point[1])

    boundary = loci.Boundary(loci.BoundaryPolicy.FIXED, False)
    candidates: list[seeds.Seed[loci.FiniteConfiguration[bool]]] = []
    for predicate in predicates:
        values = tuple(bool(predicate(point)) for point in coordinates)
        for pattern in (values, tuple(not value for value in values)):
            configuration = loci.grid_configuration(
                shape, pattern, boundary=boundary
            )
            candidates.append(
                seeds.exact(
                    configuration,
                    value_profile=alphabets.ValueProfile.BOOLEAN,
                )
            )
    return _dedupe_seed_recipes(tuple(candidates), shape)


def _dedupe_seed_recipes(
    recipes: tuple[seeds.Seed[loci.FiniteConfiguration[bool]], ...],
    shape: tuple[int, ...],
) -> tuple[seeds.Seed[loci.FiniteConfiguration[bool]], ...]:
    """Deduplicate exact patterns by canonical ordered Boolean values."""

    expected = int(prod(shape))
    kept: list[seeds.Seed[loci.FiniteConfiguration[bool]]] = []
    seen: set[tuple[bool, ...]] = set()
    targets = loci.grid_loci(shape)
    for recipe in recipes:
        configuration = recipe.denote().exact_configuration
        values = tuple(
            bool(configuration.value_at(target)) for target in targets
        )
        if len(values) != expected:
            raise ValueError("structured recipe has the wrong grid size")
        if values in seen:
            continue
        seen.add(values)
        kept.append(recipe)
    if not kept:
        raise ValueError(f"structured seed catalog is empty for shape {shape}")
    return tuple(kept)


def _structured_seed_index(
    seed_family: str,
    shape: tuple[int, ...],
    episode_rng: int,
) -> int | None:
    if seed_family != "structured":
        return None
    return episode_rng % len(_structured_seed_recipes(shape))


def _loci_boundary(spec: BoundarySpec) -> loci.Boundary[bool]:
    policies = {
        "none": loci.BoundaryPolicy.NONE,
        "fixed": loci.BoundaryPolicy.FIXED,
        "periodic": loci.BoundaryPolicy.PERIODIC,
        "reflective": loci.BoundaryPolicy.REFLECTIVE,
    }
    exterior = bool(spec.value) if spec.policy == "fixed" else None
    return loci.Boundary(policies[spec.policy], exterior)


# ---------------------------------------------------------------------------
# Tensor projection
# ---------------------------------------------------------------------------


def _project_dataset_episode(
    result: program.RolloutResult,
    *,
    domain: str,
    shape: tuple[int, ...],
    rule_id: int,
    steps: int,
) -> DatasetEpisode:
    """Project one finite, nonbranching rollout; reject every lossy case."""

    configurations = _linear_configurations(result)
    if len(configurations) != steps:
        raise ValueError(
            f"rollout contains {len(configurations)} states, expected {steps}"
        )
    states = np.stack(
        tuple(_configuration_tensor(item, shape) for item in configurations),
        axis=0,
    )
    if not shape:
        states = states.reshape(steps)
    return DatasetEpisode(
        states=states,
        coords=_canonical_coordinate_table(shape, steps),
        domain=domain,
        shape=shape,
        rule_id=rule_id,
        steps=steps,
    )


def _linear_configurations(
    result: program.RolloutResult,
) -> tuple[loci.FiniteConfiguration[bool], ...]:
    """Extract the root and unique successor chain from a semantic trace."""

    if isinstance(result, program.RolloutRejected):
        raise ValueError(f"cannot project rejected rollout: {result.fault.reason}")
    roots = _finite_support(result.raw_trace.roots.support)
    if len(roots) != 1 or not isinstance(roots[0], loci.FiniteConfiguration):
        raise ValueError("dataset projection requires one finite root")

    root = roots[0]
    out: list[loci.FiniteConfiguration[bool]] = [root]
    current: loci.FiniteConfiguration[bool] = root
    for application in _finite_support(result.raw_trace.applications):
        if (
            application.evidence.input_configuration_identity
            != current.identity
        ):
            raise ValueError(
                "dataset projection rejects disconnected trace applications"
            )
        applied = _finite_support(application.applied_atoms)
        if len(applied) != 1 or not isinstance(
            applied[0], program.AppliedDerivation
        ):
            raise ValueError(
                "dataset projection requires one replacement derivation"
            )
        groups = _finite_support(
            application.successor_quotient_with_derivation_fibers
        )
        if len(groups) != 1 or len(groups[0].derivations) != 1:
            raise ValueError("dataset projection rejects branching rollouts")
        successor = groups[0].successor
        if not isinstance(successor, loci.FiniteConfiguration):
            raise ValueError("dataset projection rejects intensional successors")
        out.append(successor)
        current = successor
    return tuple(out)


def _finite_support(space: rules.SupportSpace) -> tuple[object, ...]:
    if space.presentation is not rules.SupportPresentation.FINITE:
        raise ValueError("dataset projection requires explicitly finite support")
    return space.atoms


def _configuration_tensor(
    configuration: loci.FiniteConfiguration[bool],
    shape: tuple[int, ...],
) -> np.ndarray:
    if not shape:
        if configuration.contract.kind is not loci.CarrierKind.HISTORY:
            raise ValueError("0d dataset projection requires history configurations")
        history_size = configuration.contract.shape
        if history_size is None or len(history_size) != 1:
            raise ValueError("history configuration has no finite length")
        target = loci.occurrence("history", history_size[0] - 1)
        return np.asarray(int(configuration.value_at(target)), dtype=np.int64)

    expected = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=len(shape),
        shape=shape,
        axes=("x", "y", "z")[: len(shape)],
    )
    if not expected.accepts(configuration.contract):
        raise ValueError("grid configuration does not match the dataset shape")
    expected_targets = set(loci.grid_loci(shape))
    actual_targets = {target for target, _ in configuration.entries}
    if actual_targets != expected_targets:
        raise ValueError("grid configuration is not a complete exact grid")
    output = np.empty(shape, dtype=np.int64)
    axis_values = tuple(loci.centered_axis_values(size) for size in shape)
    axis_index = tuple(
        {coordinate: index for index, coordinate in enumerate(values)}
        for values in axis_values
    )
    for target, value in configuration.entries:
        coordinates = loci.grid_coordinates(target)
        native = tuple(
            axis_index[axis][coordinate]
            for axis, coordinate in enumerate(coordinates)
        )
        output[native] = int(value)
    return output


def _project_dataset_batch(
    episodes: tuple[DatasetEpisode, ...],
) -> DatasetBatch:
    """Stack compatible views without defining a second transition path."""

    if not episodes:
        raise ValueError("cannot project an empty dataset batch")
    first = episodes[0]
    for episode in episodes[1:]:
        if (
            episode.domain != first.domain
            or episode.shape != first.shape
            or episode.steps != first.steps
        ):
            raise ValueError("dataset batch episodes are incompatible")
        if (episode.coords is None) != (first.coords is None):
            raise ValueError("dataset batch coordinate choices disagree")
        if (
            first.coords is not None
            and episode.coords is not None
            and not np.array_equal(episode.coords, first.coords)
        ):
            raise ValueError("dataset batch coordinate tables disagree")
    return DatasetBatch(
        states=np.stack(tuple(episode.states for episode in episodes), axis=0),
        coords=None if first.coords is None else first.coords.copy(),
        rule_ids=np.asarray(
            tuple(episode.rule_id for episode in episodes), dtype=np.int64
        ),
        domain=first.domain,
        shape=first.shape,
        steps=first.steps,
        metadata=MappingProxyType({"batch_size": len(episodes)}),
    )


def _canonical_coordinate_table(
    shape: tuple[int, ...],
    steps: int,
) -> np.ndarray:
    """Return flattened time-major ``[t, x, y, z]`` coordinates."""

    if steps <= 0:
        raise ValueError("steps must be positive")
    spatial = tuple(
        itertools.product(
            *(loci.centered_axis_values(size) for size in shape)
        )
    )
    if not shape:
        spatial = ((),)
    rows: list[tuple[int, int, int, int]] = []
    for time in range(steps):
        for point in spatial:
            padded = (*point, *(0 for _ in range(3 - len(point))))
            rows.append((time, padded[0], padded[1], padded[2]))
    return np.asarray(rows, dtype=np.int64)


# ---------------------------------------------------------------------------
# Planning helpers and presentation-only OOD metadata
# ---------------------------------------------------------------------------


def _validate_profile(profile: str) -> StreamProfile:
    if profile not in ("compact", "pe"):
        raise ValueError("profile must be 'compact' or 'pe'")
    return profile


def _normalize_kind(kind: str) -> StreamKind:
    aliases = {
        "eval": "held-out-seed",
        "held_out_rule": "held-out-rule",
        "held_out_seed": "held-out-seed",
        "ood_horizon": "ood-horizon",
        "ood_scale": "ood-scale",
        "ood_boundary": "ood-boundary",
    }
    resolved = aliases.get(str(kind), str(kind))
    valid = (
        "train",
        "held-out-rule",
        "held-out-seed",
        "ood-horizon",
        "ood-scale",
        "ood-boundary",
        "invariance",
    )
    if resolved not in valid:
        raise ValueError(f"unknown stream kind {kind!r}")
    return resolved  # type: ignore[return-value]


def _resolve_count(count: int | None, profile: str) -> int:
    resolved = (
        DEFAULT_COMPACT_COUNT
        if count is None and profile == "compact"
        else DEFAULT_PE_COUNT if count is None else int(count)
    )
    if resolved <= 0:
        raise ValueError(f"count must be positive, got {resolved}")
    return resolved


def _resolve_shape(
    spec: DatasetSpec,
    kind: StreamKind,
    override: Sequence[int] | None,
) -> tuple[int, ...]:
    if override is not None:
        resolved = tuple(int(size) for size in override)
        if len(resolved) != len(spec.shape) or any(size <= 0 for size in resolved):
            raise ValueError(
                f"{spec.id} requires a positive rank-{len(spec.shape)} shape"
            )
        return resolved
    if kind == "ood-scale" and spec.shape:
        return ood_scale_shape(spec.shape)
    return spec.shape


def _resolve_boundary(
    spec: DatasetSpec,
    kind: StreamKind,
    episode_index: int,
    override: BoundarySpec | Mapping[str, str | int | bool] | None,
) -> BoundarySpec:
    if override is not None:
        return _normalize_boundary(override)
    if kind == "ood-boundary" and spec.shape:
        variants = ood_boundary_variants(spec)
        return variants[episode_index % len(variants)]
    return spec.boundary


def _resolve_steps(
    spec: DatasetSpec,
    kind: StreamKind,
    profile: StreamProfile,
    shape: tuple[int, ...],
    override: int | None,
    max_tokens: int,
) -> int:
    if override is not None:
        resolved = int(override)
    elif profile == "pe":
        tokens = int(max_tokens)
        if kind == "ood-horizon":
            tokens *= OOD_HORIZON_TOKEN_MULTIPLIER
        elif kind == "ood-scale" and shape:
            tokens *= OOD_SCALE_TOKEN_MULTIPLIER
        resolved = token_window_steps(shape, tokens)
    else:
        resolved = (
            DEFAULT_COMPACT_0D_STEPS
            if not spec.shape
            else DEFAULT_COMPACT_SPATIAL_STEPS
        )
        if kind == "ood-horizon":
            resolved *= OOD_HORIZON_TOKEN_MULTIPLIER
    if resolved <= 0:
        raise ValueError(f"steps must be positive, got {resolved}")
    return resolved


def token_window_steps(
    shape: Sequence[int],
    max_tokens: int = DEFAULT_MAX_TOKENS,
    special_tokens_per_episode: int = SPECIAL_TOKENS_PER_EPISODE,
) -> int:
    """Return the number of raw states fitting one serialized token window."""

    shape_tuple = tuple(int(size) for size in shape)
    shape_size = int(prod(shape_tuple)) if shape_tuple else 1
    available = int(max_tokens) - int(special_tokens_per_episode)
    if available <= 0:
        raise ValueError("max_tokens must exceed special_tokens_per_episode")
    source_states = available // shape_size
    if source_states <= 0:
        raise ValueError(
            f"max_tokens={max_tokens} cannot fit one state for shape {shape_tuple}"
        )
    return source_states + 1


def _selected_rule_ids(
    dataset_id: str,
    *,
    pool_name: str,
    profile: StreamProfile,
    split: float,
    rule_limit: int | None,
) -> tuple[int, ...]:
    pool = rule_pools(dataset_id, split=split)[pool_name]
    limit = (
        DEFAULT_COMPACT_RULE_LIMIT
        if rule_limit is None and profile == "compact"
        else rule_limit
    )
    if limit is not None:
        resolved_limit = int(limit)
        if resolved_limit <= 0:
            raise ValueError("rule_limit must be positive")
        pool = pool[:resolved_limit]
    if not pool:
        raise ValueError(f"rule pool {pool_name!r} is empty")
    return pool


def stable_hash64(*parts: object) -> int:
    """Return a deterministic unsigned 64-bit hash for planning values."""

    payload = json.dumps(
        _json_ready(parts), sort_keys=True, separators=(",", ":")
    )
    digest = hashlib.blake2b(payload.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little")


def _json_ready(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {
            str(key): _json_ready(item)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return [_json_ready(item) for item in value]
    raise TypeError(f"cannot convert {type(value).__name__} to JSON")


def ood_scale_shape(shape: Sequence[int]) -> tuple[int, ...]:
    """Return the larger PE-style spatial shape for an OOD-scale stream."""

    shape_tuple = tuple(int(size) for size in shape)
    if not shape_tuple:
        return ()
    factor = OOD_SCALE_FACTORS_BY_RANK.get(len(shape_tuple))
    if factor is None:
        raise ValueError(f"cannot scale rank-{len(shape_tuple)} shape")
    return tuple(
        _odd_ceil(max(size + 1, size * factor)) for size in shape_tuple
    )


def ood_boundary_variants(
    spec: DatasetSpec | str,
) -> tuple[BoundarySpec, ...]:
    """Return the non-baseline periodic and reflective boundary choices."""

    resolved = get_spec(spec) if isinstance(spec, str) else spec
    if not resolved.shape:
        return ()
    return (BoundarySpec("periodic"), BoundarySpec("reflective"))


def invariance_transforms(
    spec: DatasetSpec | str,
) -> tuple[AffineTransform, ...]:
    """Return compact presentation-only transform identities."""

    resolved = get_spec(spec) if isinstance(spec, str) else spec
    rank = len(resolved.shape)
    if rank == 0:
        return (AffineTransform("time-shift-pos-17"),)
    if rank == 1:
        return (
            AffineTransform("reflect-x"),
            AffineTransform("shift-x-half-pos"),
            AffineTransform("shift-x-full-pos"),
        )
    if rank == 2:
        return tuple(
            AffineTransform(name)
            for name in (
                "rot-xy-90",
                "rot-xy-180",
                "rot-xy-270",
                "shift-x-full-pos",
                "shift-y-full-pos",
                "shift-xy-full-pos-pos",
            )
        )
    return tuple(
        AffineTransform(name)
        for name in (
            "rot-x-90",
            "rot-y-90",
            "rot-z-90",
            "shift-x-full-pos",
            "shift-y-full-pos",
            "shift-z-full-pos",
            "shift-xyz-full-pos-pos-pos",
        )
    )


def affine_transform(
    transform_id: str,
    *,
    matrix: Sequence[Sequence[int]] | None = None,
    offset: Sequence[int] = (0, 0, 0, 0),
) -> AffineTransform:
    """Retain the planning helper while treating matrices as view metadata."""

    if matrix is not None and (
        len(matrix) != 4 or any(len(row) != 4 for row in matrix)
    ):
        raise ValueError("transform matrix must be 4 by 4")
    if len(offset) != 4:
        raise ValueError("transform offset must have four entries")
    return AffineTransform(str(transform_id))


def _transform_for_kind(
    spec: DatasetSpec,
    kind: StreamKind,
    episode_index: int,
) -> AffineTransform | None:
    if kind != "invariance":
        return None
    transforms = invariance_transforms(spec)
    return transforms[episode_index % len(transforms)]


def _normalize_boundary(
    boundary: BoundarySpec | Mapping[str, str | int | bool],
) -> BoundarySpec:
    if isinstance(boundary, BoundarySpec):
        return boundary
    policy = str(boundary.get("policy", "none")).lower()
    if policy not in ("none", "fixed", "periodic", "reflective"):
        raise ValueError(f"unknown boundary policy {policy!r}")
    value = boundary.get("value") if policy == "fixed" else None
    if value is not None and not isinstance(value, (bool, int)):
        raise TypeError("fixed boundary value must be Boolean or integer")
    return BoundarySpec(policy, value)  # type: ignore[arg-type]


def _plan_metadata(plan: EpisodePlan) -> dict[str, DatasetMetadataValue]:
    metadata: dict[str, DatasetMetadataValue] = {
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
        "boundary_policy": plan.boundary.policy,
    }
    if plan.boundary.value is not None:
        metadata["boundary_value"] = int(plan.boundary.value)
    if plan.transform is not None:
        metadata["transform_id"] = plan.transform.id
    return metadata


def _odd_ceil(value: float) -> int:
    resolved = int(ceil(float(value)))
    return resolved + 1 if resolved % 2 == 0 else resolved


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
    "AffineTransform",
    "BoundarySpec",
    "DatasetBatch",
    "DatasetEpisode",
    "DatasetId",
    "DatasetSpec",
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
    "rule_pools",
    "stable_hash64",
    "stream",
    "stream_batch",
    "token_window_steps",
]
