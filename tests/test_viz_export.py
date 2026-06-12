"""Tests for lightweight visualization bundle export."""

from __future__ import annotations

import struct

import numpy as np
import pytest

import ca
from ca.viz import VizBundleInfo, save_viewer_bundle
from ca.viz.format import FORMAT_NAME, FORMAT_VERSION, HEADER_PREFIX_LENGTH, MAGIC, decode_header


def _bundle(path):
    data = path.read_bytes()
    header, payload_base = decode_header(data)
    return data, header, payload_base


def _episode_for_domain(domain: str) -> ca.RawEpisode:
    if domain == "t+0d":
        dynamics = ca.Dynamics(
            domain="t+0d",
            shape=(),
            rule=ca.ar2_modular_0d(modulus=97),
            neighborhoods=(),
            frontier=ca.time_slice(()),
        )
        return ca.rollout(dynamics, rule_id=0, seed_state=np.array([1, 2]), steps=4)

    if domain == "t+1d":
        dynamics = ca.Dynamics(
            domain="t+1d",
            shape=(3,),
            rule=ca.dyadrads_1d_rule(),
            neighborhoods=(ca.dyadrads_1d_neighborhood(),),
            frontier=ca.time_slice((3,)),
            boundary={"policy": "fixed", "value": 0},
        )
        return ca.rollout(dynamics, rule_id=37, seed_state=np.array([1, 0, 1]), steps=3)

    if domain == "t+2d":
        dynamics = ca.Dynamics(
            domain="t+2d",
            shape=(3, 3),
            rule=ca.dyadaxes_2d_rule(),
            neighborhoods=(ca.dyadaxes_2d_neighborhood(),),
            frontier=ca.time_slice((3, 3)),
            boundary={"policy": "fixed", "value": 0},
        )
        seed = np.zeros((3, 3), dtype=np.int64)
        seed[1, :] = 1
        return ca.rollout(dynamics, rule_id=91, seed_state=seed, steps=3)

    if domain == "t+3d":
        dynamics = ca.Dynamics(
            domain="t+3d",
            shape=(3, 3, 3),
            rule=ca.dyadaxes_3d_rule(),
            neighborhoods=(ca.dyadaxes_3d_neighborhood(),),
            frontier=ca.time_slice((3, 3, 3)),
            boundary={"policy": "fixed", "value": 0},
        )
        seed = np.zeros((3, 3, 3), dtype=np.int64)
        seed[1, 1, 1] = 1
        return ca.rollout(dynamics, rule_id=173, seed_state=seed, steps=2)

    raise AssertionError(domain)


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
    dynamics = ca.Dynamics(
        domain="t+1d",
        shape=(3,),
        rule=ca.dyadrads_1d_rule(),
        neighborhoods=(ca.dyadrads_1d_neighborhood(),),
        frontier=ca.time_slice((3,)),
        boundary={"policy": "fixed", "value": 0},
    )
    batch = ca.rollout_batch(
        dynamics=dynamics,
        rule_ids=np.array([0, 37], dtype=np.int64),
        seed_states=np.array([[1, 0, 1], [0, 1, 0]], dtype=np.int64),
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
    batch = ca.RawBatch(
        domain="t+0d",
        shape=(),
        rule_ids=np.array([0], dtype=np.int64),
        steps=2,
        states=np.array([[0, 1]], dtype=np.int64),
    )

    with pytest.raises(ValueError, match="requires row"):
        save_viewer_bundle(batch, tmp_path / "batch.ankos")


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
    episode = ca.RawEpisode(
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=2,
        states=np.array([0, 1], dtype=np.int64),
        coords=None,
    )

    with pytest.raises(ValueError, match="coords"):
        save_viewer_bundle(episode, tmp_path / "missing-coords.ankos", include_coords=True)


def test_sparse_integer_values_use_indexed_value_map(tmp_path) -> None:
    episode = ca.RawEpisode(
        domain="t+1d",
        shape=(3,),
        rule_id=0,
        steps=1,
        states=np.array([[10, 20, 10]], dtype=np.int64),
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
    episode = ca.RawEpisode(
        domain="t+1d",
        shape=(1,),
        rule_id=0,
        steps=1,
        states=np.array([[300]], dtype=np.int64),
    )

    with pytest.raises(ValueError, match="uint8"):
        save_viewer_bundle(episode, tmp_path / "bad.ankos", storage_dtype="uint8")

    info = save_viewer_bundle(episode, tmp_path / "ok.ankos", storage_dtype="uint16")
    _, header, _ = _bundle(tmp_path / "ok.ankos")

    assert info.state_storage_dtype == "uint16"
    assert header["states"]["storage_dtype"] == "uint16"
    assert header["states"]["storage_mode"] == "raw"


def test_invalid_storage_dtype_is_rejected(tmp_path) -> None:
    episode = ca.RawEpisode(
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
        states=np.array([0], dtype=np.int64),
    )

    with pytest.raises(ValueError, match="storage_dtype"):
        save_viewer_bundle(episode, tmp_path / "bad.ankos", storage_dtype="int32")


def test_coord_int32_range_is_validated(tmp_path) -> None:
    episode = ca.RawEpisode(
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
        states=np.array([0], dtype=np.int64),
        coords=np.array([[0, 0, 0, np.iinfo(np.int32).max + 1]], dtype=np.int64),
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
    episode = ca.RawEpisode(
        domain="t+0d",
        shape=(),
        rule_id=0,
        steps=1,
        states=states,
    )

    with pytest.raises(TypeError):
        save_viewer_bundle(episode, tmp_path / "bad.ankos")


def test_custom_palette_validation(tmp_path) -> None:
    episode = ca.RawEpisode(
        domain="t+1d",
        shape=(2,),
        rule_id=0,
        steps=1,
        states=np.array([[0, 1]], dtype=np.int64),
    )

    save_viewer_bundle(
        episode,
        tmp_path / "palette.ankos",
        palette=[[1, 2, 3, 255], [4, 5, 6, 255]],
    )
    _, header, _ = _bundle(tmp_path / "palette.ankos")

    assert header["palette"]["name"] == "custom"
    assert header["palette"]["colors"] == [[1, 2, 3, 255], [4, 5, 6, 255]]
