"""Export explicit downstream dataset views to viewer bundle version 1.

The Goal 7 target layer in this module accepts only ``DatasetEpisode`` and
``DatasetBatch`` tensor projections prepared by ``datasets.py``. It preserves
the existing ``ankos.viz.bundle`` wire contract and presentation metadata. It
does not infer a tensor layout from arbitrary semantic results, define the
canonical program codec, or participate in application.

The target signature is documented but not falsely overloaded while the live
0.1 exporter still consumes ``RawEpisode`` and ``RawBatch``. That implementation
remains intact below the explicit legacy divider until the atomic G7-01
downstream migration.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

from ..specs import RawBatch, RawEpisode
from .format import FORMAT_NAME, FORMAT_VERSION, align_offset, encode_bundle


if TYPE_CHECKING:
    from ..datasets import DatasetBatch, DatasetEpisode

    DatasetViewSource = DatasetEpisode | DatasetBatch


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.1: Explicit Dataset-View Input
# ---------------------------------------------------------------------------

# Target spelling:
#
#     save_viewer_bundle(
#         source: DatasetEpisode | DatasetBatch,
#         path: str | Path,
#         ...,
#     ) -> VizBundleInfo
#
# No runtime overload is declared until that source union is actually accepted.


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.2: Bundle Preparation
# ---------------------------------------------------------------------------

# Dataset payload, coordinate, palette, and presentation metadata preparation
# stays downstream of the explicit projection boundary.


# ---------------------------------------------------------------------------
# Goal 7 Phase 2: Viewer-Presentation Aliases
# ---------------------------------------------------------------------------

# Legacy wire labels such as ``RawEpisode``/``RawBatch``, ``domain``, and
# ``rule_id`` remain presentation metadata under bundle version 1.


# ===========================================================================
# Legacy 0.1 implementation retained until atomic G7-01 cutover
# ===========================================================================


_STATE_DTYPES = {
    "uint8": np.dtype("<u1"),
    "uint16": np.dtype("<u2"),
}
_COORD_DTYPE = np.dtype("<i4")
_MAX_CODES = 65_536


@dataclass(frozen=True)
class VizBundleInfo:
    """Summary of a written visualization bundle."""

    path: str
    kind: str
    domain: str
    state_shape: tuple[int, ...]
    state_storage_dtype: str
    storage_mode: str
    bytes_written: int


@dataclass(frozen=True)
class _PreparedSource:
    kind: str
    domain: str
    shape: tuple[int, ...]
    rule_id: int
    steps: int
    states: np.ndarray
    coords: np.ndarray | None
    metadata: Mapping[str, Any] | None


@dataclass(frozen=True)
class _PreparedStates:
    array: np.ndarray
    storage_dtype: str
    storage_mode: str
    value_map: dict[str, Any] | None
    unique_values: np.ndarray


def save_viewer_bundle(
    source: RawEpisode | RawBatch,
    path: str | Path,
    *,
    palette: str | Sequence[Sequence[int]] = "auto",
    row: int | None = None,
    include_coords: bool = False,
    storage_dtype: str = "auto",
    title: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> VizBundleInfo:
    """Write a `.ankos` static-viewer bundle for a raw episode or batch row."""

    prepared_source = _prepare_source(source, row=row)
    prepared_states = _prepare_states(prepared_source.states, storage_dtype=storage_dtype)
    state_payload = _payload_bytes(prepared_states.array)
    state_entry = {
        "layout": _episode_layout(prepared_source.domain),
        "shape": list(prepared_states.array.shape),
        "source_dtype": str(prepared_source.states.dtype),
        "storage_dtype": prepared_states.storage_dtype,
        "storage_mode": prepared_states.storage_mode,
        "byte_offset": 0,
        "byte_length": len(state_payload),
        "byte_order": "little",
    }

    payload = bytearray(state_payload)
    coords_entry = None
    if include_coords:
        if prepared_source.coords is None:
            raise ValueError("include_coords=True requires source.coords to be present")
        coords_array = _prepare_coords(prepared_source.coords)
        coords_offset = align_offset(len(payload))
        payload.extend(b"\0" * (coords_offset - len(payload)))
        coords_payload = _payload_bytes(coords_array)
        payload.extend(coords_payload)
        coords_entry = {
            "layout": "N4",
            "shape": list(coords_array.shape),
            "source_dtype": str(np.asarray(prepared_source.coords).dtype),
            "storage_dtype": "int32",
            "byte_offset": coords_offset,
            "byte_length": len(coords_payload),
            "byte_order": "little",
        }

    merged_metadata = _merge_metadata(prepared_source, source, row=row, metadata=metadata)
    header = {
        "format": FORMAT_NAME,
        "version": FORMAT_VERSION,
        "kind": prepared_source.kind,
        "domain": prepared_source.domain,
        "shape": list(prepared_source.shape),
        "steps": prepared_source.steps,
        "title": title,
        "rule_id": prepared_source.rule_id,
        "states": state_entry,
        "coords": coords_entry,
        "value_map": prepared_states.value_map,
        "palette": _palette_spec(palette, prepared_states.unique_values),
        "metadata": merged_metadata,
    }

    bundle = encode_bundle(_json_safe(header), bytes(payload))
    out_path = Path(path)
    if out_path.parent != Path("."):
        out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(bundle)

    return VizBundleInfo(
        path=str(out_path),
        kind=prepared_source.kind,
        domain=prepared_source.domain,
        state_shape=tuple(int(size) for size in prepared_states.array.shape),
        state_storage_dtype=prepared_states.storage_dtype,
        storage_mode=prepared_states.storage_mode,
        bytes_written=out_path.stat().st_size,
    )


def _prepare_source(source: RawEpisode | RawBatch, row: int | None) -> _PreparedSource:
    if isinstance(source, RawEpisode):
        if row is not None:
            raise ValueError("row is only valid when exporting RawBatch")
        return _PreparedSource(
            kind="RawEpisode",
            domain=source.domain,
            shape=tuple(source.shape),
            rule_id=int(source.rule_id),
            steps=int(source.steps),
            states=np.asarray(source.states),
            coords=source.coords,
            metadata=source.metadata,
        )

    if isinstance(source, RawBatch):
        if row is None:
            raise ValueError("RawBatch export requires row=int in the MVP")
        if isinstance(row, bool):
            raise TypeError("row must be an integer, not bool")
        row_index = int(row)
        states = np.asarray(source.states)
        if row_index < 0 or row_index >= states.shape[0]:
            raise IndexError(f"row {row_index} is outside batch range 0..{states.shape[0] - 1}")
        return _PreparedSource(
            kind="RawEpisode",
            domain=source.domain,
            shape=tuple(source.shape),
            rule_id=int(np.asarray(source.rule_ids).reshape(-1)[row_index]),
            steps=int(source.steps),
            states=np.asarray(states[row_index]),
            coords=source.coords,
            metadata=source.metadata,
        )

    raise TypeError("source must be ca.RawEpisode or ca.RawBatch")


def _prepare_states(states: np.ndarray, storage_dtype: str) -> _PreparedStates:
    states = np.asarray(states)
    if states.dtype == np.dtype("O"):
        raise TypeError("object state arrays cannot be exported")
    if np.issubdtype(states.dtype, np.floating):
        raise TypeError("float state arrays are deferred for a future numeric viewer mode")
    if not (np.issubdtype(states.dtype, np.integer) or np.issubdtype(states.dtype, np.bool_)):
        raise TypeError(f"state arrays must be integer-like for the MVP, got {states.dtype}")

    storage_dtype = str(storage_dtype).lower()
    if storage_dtype not in {"auto", *_STATE_DTYPES}:
        raise ValueError("storage_dtype must be 'auto', 'uint8', or 'uint16'")

    states_i = np.ascontiguousarray(states)
    unique = np.unique(states_i)
    if unique.size == 0:
        raise ValueError("state array cannot be empty")
    if unique.size > _MAX_CODES:
        raise ValueError(f"state arrays with more than {_MAX_CODES} distinct values are not supported")

    if storage_dtype != "auto":
        dtype = _STATE_DTYPES[storage_dtype]
        info = np.iinfo(dtype)
        min_value = int(unique[0])
        max_value = int(unique[-1])
        if min_value < 0 or max_value > int(info.max):
            raise ValueError(f"states cannot be represented as raw {storage_dtype}")
        return _PreparedStates(
            array=np.ascontiguousarray(states_i.astype(dtype, copy=False)),
            storage_dtype=storage_dtype,
            storage_mode="raw",
            value_map=None,
            unique_values=unique.astype(np.int64, copy=False),
        )

    if _is_dense_unsigned_codes(unique, 256):
        return _PreparedStates(
            array=np.ascontiguousarray(states_i.astype(_STATE_DTYPES["uint8"], copy=False)),
            storage_dtype="uint8",
            storage_mode="raw",
            value_map=None,
            unique_values=unique.astype(np.int64, copy=False),
        )

    if _is_dense_unsigned_codes(unique, 65_536):
        return _PreparedStates(
            array=np.ascontiguousarray(states_i.astype(_STATE_DTYPES["uint16"], copy=False)),
            storage_dtype="uint16",
            storage_mode="raw",
            value_map=None,
            unique_values=unique.astype(np.int64, copy=False),
        )

    code_dtype_name = "uint8" if unique.size <= 256 else "uint16"
    code_dtype = _STATE_DTYPES[code_dtype_name]
    codes = np.searchsorted(unique, states_i).astype(code_dtype, copy=False)
    unique_i64 = unique.astype(np.int64, copy=False)
    return _PreparedStates(
        array=np.ascontiguousarray(codes),
        storage_dtype=code_dtype_name,
        storage_mode="indexed",
        value_map={
            "code_dtype": code_dtype_name,
            "raw_dtype": str(states_i.dtype),
            "values": unique_i64.tolist(),
        },
        unique_values=unique_i64,
    )


def _is_dense_unsigned_codes(unique: np.ndarray, limit: int) -> bool:
    if unique.size == 0:
        return False
    if int(unique[0]) != 0:
        return False
    if int(unique[-1]) >= int(limit):
        return False
    return bool(np.array_equal(unique, np.arange(unique.size, dtype=unique.dtype)))


def _prepare_coords(coords: np.ndarray) -> np.ndarray:
    coords_array = np.asarray(coords)
    if coords_array.ndim != 2 or coords_array.shape[1] != 4:
        raise ValueError(f"coords must have shape (N, 4), got {tuple(coords_array.shape)}")
    if not np.issubdtype(coords_array.dtype, np.integer):
        raise TypeError("coords must be integer arrays")
    info = np.iinfo(_COORD_DTYPE)
    if np.any(coords_array < info.min) or np.any(coords_array > info.max):
        raise ValueError("coords exceed int32 storage range")
    return np.ascontiguousarray(coords_array.astype(_COORD_DTYPE, copy=False))


def _episode_layout(domain: str) -> str:
    layouts = {
        "t+0d": "T",
        "t+1d": "TX",
        "t+2d": "TXY",
        "t+3d": "TXYZ",
    }
    try:
        return layouts[str(domain).lower()]
    except KeyError as exc:
        raise ValueError(f"unsupported domain {domain!r}") from exc


def _payload_bytes(array: np.ndarray) -> bytes:
    return np.ascontiguousarray(array).tobytes(order="C")


def _palette_spec(
    palette: str | Sequence[Sequence[int]],
    raw_values: np.ndarray,
) -> dict[str, Any]:
    values = np.asarray(raw_values)
    color_count = int(values.size)
    if color_count <= 0:
        raise ValueError("palette requires at least one value")

    if isinstance(palette, str):
        name = palette.lower()
        if name == "auto":
            if color_count == 2 and set(int(value) for value in values.tolist()) == {0, 1}:
                name = "binary"
            elif color_count <= 32:
                name = "categorical"
            else:
                name = "categorical"
        if name == "binary":
            if color_count > 2:
                raise ValueError("binary palette can only be used with at most two values")
            colors = _binary_colors(color_count)
        elif name == "categorical":
            colors = [_categorical_color(index) for index in range(color_count)]
        elif name == "heat":
            colors = [_heat_color(index, max(color_count - 1, 1)) for index in range(color_count)]
        elif name == "gray":
            colors = [_gray_color(index, max(color_count - 1, 1)) for index in range(color_count)]
        else:
            raise ValueError(f"unknown palette {palette!r}")
        return {
            "name": name,
            "colors": colors,
        }

    colors = [_validate_rgba(row) for row in palette]
    if len(colors) < color_count:
        raise ValueError(f"explicit palette needs at least {color_count} colors")
    return {
        "name": "custom",
        "colors": colors,
    }


def _binary_colors(count: int) -> list[list[int]]:
    colors = [[255, 255, 255, 255], [0, 0, 0, 255]]
    return colors[:count]


def _categorical_color(index: int) -> list[int]:
    if index == 0:
        return [245, 245, 245, 255]
    # Integer hash constants keep colors deterministic without importing colorsys.
    red = (37 + index * 97) % 256
    green = (91 + index * 57) % 256
    blue = (149 + index * 131) % 256
    return [int(red), int(green), int(blue), 255]


def _heat_color(index: int, high: int) -> list[int]:
    ratio = index / high
    red = int(round(255 * ratio))
    green = int(round(220 * max(0.0, 1.0 - abs(ratio - 0.5) * 2.0)))
    blue = int(round(255 * (1.0 - ratio)))
    return [red, green, blue, 255]


def _gray_color(index: int, high: int) -> list[int]:
    value = int(round(255 * (index / high)))
    return [value, value, value, 255]


def _validate_rgba(row: Sequence[int]) -> list[int]:
    values = [int(value) for value in row]
    if len(values) != 4:
        raise ValueError("palette colors must be RGBA sequences")
    for value in values:
        if value < 0 or value > 255:
            raise ValueError("palette color channels must be in 0..255")
    return values


def _merge_metadata(
    prepared_source: _PreparedSource,
    original_source: RawEpisode | RawBatch,
    *,
    row: int | None,
    metadata: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged = dict(prepared_source.metadata or {})
    if isinstance(original_source, RawBatch):
        merged.setdefault("source_kind", "RawBatch")
        merged.setdefault("batch_row", int(row) if row is not None else None)
        merged.setdefault("batch_size", int(np.asarray(original_source.states).shape[0]))
    if metadata is not None:
        merged.update(dict(metadata))
    return _json_safe(merged)


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, np.generic):
        return _json_safe(value.item())
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    raise TypeError(f"value of type {type(value).__name__} is not JSON-safe")


__all__ = [
    "VizBundleInfo",
    "save_viewer_bundle",
]
