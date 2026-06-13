"""Tests for built-in compact dataset streams."""

import numpy as np

import ca
from ca import datasets


def test_registry_specs_match_pe_recipes() -> None:
    assert datasets.DATASET_IDS == (
        "0d-dyadlags",
        "1d-dyadrads",
        "2d-dyadaxes",
        "3d-dyadaxes",
    )

    assert datasets.get_spec("0d-dyadlags").shape == ()
    assert datasets.get_spec("0d-dyadlags").seed_families == ("uniform_bits",)
    assert datasets.get_spec("1d-dyadrads").shape == (123,)
    assert datasets.get_spec("2d-dyadaxes").shape == (11, 11)
    assert datasets.get_spec("3d-dyadaxes").shape == (5, 5, 5)
    assert datasets.get_spec("2d-dyadaxes").boundary == {"policy": "fixed", "value": 0}


def test_rule_pools_use_pe_split() -> None:
    pools = datasets.rule_pools("2d-dyadaxes")

    assert pools["train"][0] == 0
    assert pools["train"][-1] == 203
    assert len(pools["train"]) == 204
    assert pools["held_out_rule"][0] == 204
    assert pools["held_out_rule"][-1] == 255
    assert len(pools["held_out_rule"]) == 52


def test_plan_episode_matches_pe_rule_and_rng_derivation() -> None:
    plan = datasets.plan_episode("2d-dyadaxes", kind="held-out-seed", episode_index=7)
    expected_rng = ca.rng.derive_episode_rng(
        {
            "policy": "splitmix64",
            "base_rng": datasets.stable_hash64("2d-dyadaxes", "eval", "held-out-seed"),
        },
        7,
    )
    expected_seed_family = datasets.get_spec("2d-dyadaxes").seed_families[expected_rng % 2]

    assert plan.rule_id == 7
    assert plan.episode_rng == expected_rng
    assert plan.seed_stream_family == "held-out-seed"
    assert plan.seed_family == expected_seed_family


def test_train_kind_uses_train_split_for_rng_derivation() -> None:
    plan = datasets.plan_episode("1d-dyadrads", kind="train", episode_index=3)
    expected_rng = ca.rng.derive_episode_rng(
        {
            "policy": "splitmix64",
            "base_rng": datasets.stable_hash64("1d-dyadrads", "train", "train"),
        },
        3,
    )

    assert plan.split == "train"
    assert plan.seed_stream_family == "train"
    assert plan.episode_rng == expected_rng


def test_compact_defaults_are_small_and_limited() -> None:
    plans = [
        datasets.plan_episode("2d-dyadaxes", kind="held-out-seed", episode_index=index)
        for index in range(10)
    ]
    held_out = [
        datasets.plan_episode("2d-dyadaxes", kind="held-out-rule", episode_index=index)
        for index in range(10)
    ]

    assert plans[0].steps == 17
    assert [plan.rule_id for plan in plans[:8]] == list(range(8))
    assert plans[8].rule_id == 0
    assert [plan.rule_id for plan in held_out[:8]] == list(range(204, 212))
    assert held_out[8].rule_id == 204
    assert sum(1 for _ in datasets.stream("2d-dyadaxes")) == 8


def test_pe_profile_uses_pe_token_window_sizing() -> None:
    t0d = datasets.plan_episode("0d-dyadlags", profile="pe")
    t1d = datasets.plan_episode("1d-dyadrads", profile="pe")
    t1d_ood = datasets.plan_episode("1d-dyadrads", kind="ood-horizon", profile="pe")

    assert t0d.steps == 2047
    assert t1d.steps == 17
    assert t1d_ood.steps == 34
    assert sum(1 for _ in datasets.stream("1d-dyadrads", profile="pe", steps=3)) == 64


def test_each_dataset_yields_valid_raw_episode() -> None:
    expected_shapes = {
        "0d-dyadlags": (128,),
        "1d-dyadrads": (17, 123),
        "2d-dyadaxes": (17, 11, 11),
        "3d-dyadaxes": (17, 5, 5, 5),
    }

    for dataset_id, expected_shape in expected_shapes.items():
        episode = next(datasets.stream(dataset_id, count=1))

        assert isinstance(episode, ca.RawEpisode)
        assert episode.states.shape == expected_shape
        assert episode.coords is not None
        assert episode.metadata is not None
        assert episode.metadata["dataset_id"] == dataset_id
        assert episode.metadata["profile"] == "compact"


def test_stream_batch_yields_raw_batch() -> None:
    batch = next(datasets.stream_batch("2d-dyadaxes", count=3, batch_size=3))

    assert isinstance(batch, ca.RawBatch)
    assert batch.states.shape == (3, 17, 11, 11)
    np.testing.assert_array_equal(batch.rule_ids, np.array([0, 1, 2], dtype=np.int64))
    assert batch.metadata is not None
    assert len(batch.metadata["episodes"]) == 3


def test_ood_variants_are_available_without_large_defaults() -> None:
    scale = datasets.plan_episode("2d-dyadaxes", kind="ood-scale")
    boundary_0 = datasets.plan_episode("2d-dyadaxes", kind="ood-boundary", episode_index=0)
    boundary_1 = datasets.plan_episode("2d-dyadaxes", kind="ood-boundary", episode_index=1)
    invariant = datasets.plan_episode("2d-dyadaxes", kind="invariance", episode_index=0)

    assert scale.shape == (15, 15)
    assert scale.steps == 17
    assert boundary_0.boundary == {"policy": "periodic"}
    assert boundary_1.boundary == {"policy": "reflective"}
    assert invariant.transform is not None
    assert invariant.transform["id"] == "rot-xy-90"
