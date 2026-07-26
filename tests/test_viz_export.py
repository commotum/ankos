"""Tests for lightweight visualization bundle export."""

from __future__ import annotations

import struct

import numpy as np
import pytest

from ca import program
from ca.datasets import DatasetBatch, DatasetEpisode
from ca.viz import VizBundleInfo, save_viewer_bundle
from ca.viz.format import FORMAT_NAME, FORMAT_VERSION, HEADER_PREFIX_LENGTH, MAGIC, decode_header


def _bundle(path):
    data = path.read_bytes()
    header, payload_base = decode_header(data)
    return data, header, payload_base


def _coordinate_table(shape: tuple[int, ...], steps: int) -> np.ndarray:
    axes = tuple(
        tuple(range(-(size // 2), -(size // 2) + size))
        for size in shape
    )
    spatial = tuple(np.ndindex(shape)) if shape else ((),)
    rows = []
    for time in range(steps):
        for native in spatial:
            point = tuple(axes[axis][index] for axis, index in enumerate(native))
            padded = (*point, *(0 for _ in range(3 - len(point))))
            rows.append((time, padded[0], padded[1], padded[2]))
    return np.asarray(rows, dtype=np.int64)


def _episode_for_domain(domain: str) -> DatasetEpisode:
    recipes = {
        "t+0d": ((), 4, 0),
        "t+1d": ((3,), 3, 37),
        "t+2d": ((3, 3), 3, 91),
        "t+3d": ((3, 3, 3), 2, 173),
    }
    shape, steps, rule_id = recipes[domain]
    states = np.arange(steps * (int(np.prod(shape)) if shape else 1))
    states = (states % 2).reshape((steps, *shape))
    if not shape:
        states = states.reshape(steps)
    return DatasetEpisode(
        states=states.astype(np.int64),
        coords=_coordinate_table(shape, steps),
        domain=domain,
        shape=shape,
        rule_id=rule_id,
        steps=steps,
    )


@pytest.mark.parametrize(
    ("domain", "layout"),
    [
        ("t+0d", "T"),
        ("t+1d", "TX"),
        ("t+2d", "TXY"),
        ("t+3d", "TXYZ"),
    ],
)
def test_raw_episode_export_for_supported_domains(tmp_path, domain: str, layout: str) -> None:
    episode = _episode_for_domain(domain)
    path = tmp_path / f"{domain}.ankos"

    info = save_viewer_bundle(episode, path)
    data, header, payload_base = _bundle(path)

    assert isinstance(info, VizBundleInfo)
    assert info.path == str(path)
    assert info.kind == "RawEpisode"
    assert info.domain == domain
    assert info.bytes_written == len(data)
    assert data[: len(MAGIC)] == MAGIC
    assert struct.unpack("<I", data[len(MAGIC) : HEADER_PREFIX_LENGTH])[0] == payload_base - HEADER_PREFIX_LENGTH
    assert payload_base % 8 == 0
    assert header["format"] == FORMAT_NAME
    assert header["version"] == FORMAT_VERSION
    assert header["kind"] == "RawEpisode"
    assert header["domain"] == domain
    assert header["shape"] == list(episode.shape)
    assert header["steps"] == episode.steps
    assert header["states"]["layout"] == layout
    assert header["states"]["shape"] == list(info.state_shape)
    assert header["states"]["byte_offset"] == 0
    assert header["states"]["byte_length"] == np.prod(info.state_shape) * np.dtype(info.state_storage_dtype).itemsize
    assert header["coords"] is None


def test_raw_batch_row_export_uses_episode_layout_and_selected_rule(tmp_path) -> None:
    batch = DatasetBatch(
        states=np.array(
            [
                [[1, 0, 1], [0, 1, 0], [1, 1, 0]],
                [[0, 1, 0], [1, 0, 1], [0, 0, 1]],
            ],
            dtype=np.int64,
        ),
        coords=_coordinate_table((3,), 3),
        rule_ids=np.array([0, 37], dtype=np.int64),
        domain="t+1d",
        shape=(3,),
        steps=3,
    )

    save_viewer_bundle(batch, tmp_path / "row.ankos", row=1)
    _, header, _ = _bundle(tmp_path / "row.ankos")

    assert header["kind"] == "RawEpisode"
    assert header["states"]["layout"] == "TX"
    assert header["states"]["shape"] == [3, 3]
    assert header["rule_id"] == 37
    assert header["metadata"]["source_kind"] == "RawBatch"
    assert header["metadata"]["batch_row"] == 1
    assert header["metadata"]["batch_size"] == 2


def test_raw_batch_requires_row_in_mvp(tmp_path) -> None:
    batch = DatasetBatch(
        states=np.array([[0, 1]], dtype=np.int64),
        coords=None,
        rule_ids=np.array([0], dtype=np.int64),
        domain="t+0d",
        shape=(),
        steps=2,
    )

    with pytest.raises(ValueError, match="requires row"):
        save_viewer_bundle(batch, tmp_path / "batch.ankos")


def test_export_rejects_semantic_rollout_results(tmp_path) -> None:
    semantic_result = program.RolloutRejected(
        program.RolloutFault("fixture rejection")
    )
    with pytest.raises(TypeError, match="DatasetEpisode or ca.datasets.DatasetBatch"):
        save_viewer_bundle(  # type: ignore[arg-type]
            semantic_result,
            tmp_path / "semantic-result.ankos",
        )


def test_export_includes_aligned_coords_when_requested(tmp_path) -> None:
    episode = _episode_for_domain("t+2d")
    save_viewer_bundle(episode, tmp_path / "coords.ankos", include_coords=True)
    data, header, payload_base = _bundle(tmp_path / "coords.ankos")

    coords = header["coords"]
    assert coords["layout"] == "N4"
    assert coords["shape"] == list(episode.coords.shape)
    assert coords["storage_dtype"] == "int32"
    assert (payload_base + coords["byte_offset"]) % np.dtype("int32").itemsize == 0
    assert coords["byte_length"] == episode.coords.size * np.dtype("int32").itemsize
    coords_view = np.frombuffer(
        data,
        dtype="<i4",
        count=episode.coords.size,
        offset=payload_base + coords["byte_offset"],
    ).reshape(episode.coords.shape)
    np.testing.assert_array_equal(coords_view, episode.coords.astype(np.int32))


def test_include_coords_requires_present_coords(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([0, 1], dtype=np.int64),
        coords=None,
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=2,
    )

    with pytest.raises(ValueError, match="coords"):
        save_viewer_bundle(episode, tmp_path / "missing-coords.ankos", include_coords=True)


def test_sparse_integer_values_use_indexed_value_map(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([[10, 20, 10]], dtype=np.int64),
        coords=None,
        domain="t+1d",
        shape=(3,),
        rule_id=0,
        steps=1,
    )

    save_viewer_bundle(episode, tmp_path / "indexed.ankos")
    data, header, payload_base = _bundle(tmp_path / "indexed.ankos")

    assert header["states"]["storage_mode"] == "indexed"
    assert header["states"]["storage_dtype"] == "uint8"
    assert header["value_map"] == {
        "code_dtype": "uint8",
        "raw_dtype": "int64",
        "values": [10, 20],
    }
    state_view = np.frombuffer(
        data,
        dtype=np.uint8,
        count=3,
        offset=payload_base + header["states"]["byte_offset"],
    )
    np.testing.assert_array_equal(state_view, np.array([0, 1, 0], dtype=np.uint8))


def test_explicit_storage_dtype_validates_range(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([[300]], dtype=np.int64),
        coords=None,
        domain="t+1d",
        shape=(1,),
        rule_id=0,
        steps=1,
    )

    with pytest.raises(ValueError, match="uint8"):
        save_viewer_bundle(episode, tmp_path / "bad.ankos", storage_dtype="uint8")

    info = save_viewer_bundle(episode, tmp_path / "ok.ankos", storage_dtype="uint16")
    _, header, _ = _bundle(tmp_path / "ok.ankos")

    assert info.state_storage_dtype == "uint16"
    assert header["states"]["storage_dtype"] == "uint16"
    assert header["states"]["storage_mode"] == "raw"


def test_invalid_storage_dtype_is_rejected(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([0], dtype=np.int64),
        coords=None,
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
    )

    with pytest.raises(ValueError, match="storage_dtype"):
        save_viewer_bundle(episode, tmp_path / "bad.ankos", storage_dtype="int32")


def test_coord_int32_range_is_validated(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([0], dtype=np.int64),
        coords=np.array(
            [[0, 0, 0, np.iinfo(np.int32).max + 1]], dtype=np.int64
        ),
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
    )

    with pytest.raises(ValueError, match="int32"):
        save_viewer_bundle(episode, tmp_path / "coords.ankos", include_coords=True)


@pytest.mark.parametrize(
    "states",
    [
        np.array([object()], dtype=object),
        np.array([0.0], dtype=np.float64),
        np.array(["a"], dtype="<U1"),
    ],
)
def test_non_integer_state_modes_are_rejected(tmp_path, states: np.ndarray) -> None:
    episode = DatasetEpisode(
        states=states,
        coords=None,
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
    )

    with pytest.raises(TypeError):
        save_viewer_bundle(episode, tmp_path / "bad.ankos")


def test_custom_palette_validation(tmp_path) -> None:
    episode = DatasetEpisode(
        states=np.array([[0, 1]], dtype=np.int64),
        coords=None,
        domain="t+1d",
        shape=(2,),
        rule_id=0,
        steps=1,
    )

    save_viewer_bundle(
        episode,
        tmp_path / "palette.ankos",
        palette=[[1, 2, 3, 255], [4, 5, 6, 255]],
    )
    _, header, _ = _bundle(tmp_path / "palette.ankos")

    assert header["palette"]["name"] == "custom"
    assert header["palette"]["colors"] == [[1, 2, 3, 255], [4, 5, 6, 255]]
