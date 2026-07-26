"""Tests for downstream program recipes and explicit dataset views."""

from __future__ import annotations

from dataclasses import fields, replace

import numpy as np

from ca import program
from ca import datasets, rng, rules


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
    assert datasets.get_spec("2d-dyadaxes").boundary == datasets.BoundarySpec(
        "fixed", 0
    )


def test_rule_pools_are_the_explicit_finite_0_to_255_domain() -> None:
    pools = datasets.rule_pools("2d-dyadaxes")
    assert pools["all"] == tuple(range(256))
    assert pools["train"] == tuple(range(204))
    assert pools["held_out_rule"] == tuple(range(204, 256))
    assert pools["eval"] == pools["held_out_rule"]


def test_plan_episode_matches_pe_rule_and_rng_derivation() -> None:
    plan = datasets.plan_episode(
        "2d-dyadaxes", kind="held-out-seed", episode_index=7
    )
    expected_rng = rng.derive_episode_rng(
        datasets.stable_hash64(
            "2d-dyadaxes", "eval", "held-out-seed"
        ),
        7,
    )
    expected_seed_family = datasets.get_spec(
        "2d-dyadaxes"
    ).seed_families[expected_rng % 2]
    assert plan.rule_id == 7
    assert plan.episode_rng == expected_rng
    assert plan.seed_stream_family == "held-out-seed"
    assert plan.seed_family == expected_seed_family


def test_train_kind_uses_train_split_for_rng_derivation() -> None:
    plan = datasets.plan_episode(
        "1d-dyadrads", kind="train", episode_index=3
    )
    expected_rng = rng.derive_episode_rng(
        datasets.stable_hash64("1d-dyadrads", "train", "train"),
        3,
    )
    assert plan.split == "train"
    assert plan.seed_stream_family == "train"
    assert plan.episode_rng == expected_rng


def test_compact_defaults_are_small_and_rule_limited() -> None:
    plans = tuple(
        datasets.plan_episode(
            "2d-dyadaxes",
            kind="held-out-seed",
            episode_index=index,
        )
        for index in range(10)
    )
    held_out = tuple(
        datasets.plan_episode(
            "2d-dyadaxes",
            kind="held-out-rule",
            episode_index=index,
        )
        for index in range(10)
    )
    assert plans[0].steps == 17
    assert tuple(plan.rule_id for plan in plans[:8]) == tuple(range(8))
    assert plans[8].rule_id == 0
    assert tuple(plan.rule_id for plan in held_out[:8]) == tuple(
        range(204, 212)
    )
    assert held_out[8].rule_id == 204


def test_pe_profile_uses_pe_token_window_sizing() -> None:
    t0d = datasets.plan_episode("0d-dyadlags", profile="pe")
    t1d = datasets.plan_episode("1d-dyadrads", profile="pe")
    t1d_ood = datasets.plan_episode(
        "1d-dyadrads", kind="ood-horizon", profile="pe"
    )
    assert t0d.steps == 2047
    assert t1d.steps == 17
    assert t1d_ood.steps == 34


def test_each_recipe_constructs_an_ordinary_program_and_dense_view() -> None:
    cases = (
        ("0d-dyadlags", (), (2,)),
        ("1d-dyadrads", (5,), (2, 5)),
        ("2d-dyadaxes", (3, 3), (2, 3, 3)),
        ("3d-dyadaxes", (3, 3, 3), (2, 3, 3, 3)),
    )
    for dataset_id, shape, expected_states_shape in cases:
        plan = datasets.plan_episode(
            dataset_id,
            shape=shape,
            steps=2,
            episode_index=1,
        )
        exact_seed = datasets._seed_for_plan(plan)
        simple_program = datasets._build_program(
            plan.dataset_id,
            rule=plan.rule_id,
            seed=exact_seed,
            shape=plan.shape,
            boundary=plan.boundary,
        )
        assert isinstance(simple_program, program.SimpleProgram)
        assert tuple(item.name for item in fields(simple_program)) == (
            "seed",
            "alphabet",
            "frontier",
            "neighborhood",
            "rule",
        )

        episode = datasets.realize_episode(plan)
        assert isinstance(episode, datasets.DatasetEpisode)
        assert episode.states.shape == expected_states_shape
        assert episode.coords is not None
        assert episode.metadata is not None
        assert episode.metadata["dataset_id"] == dataset_id


def test_stream_and_batch_only_loop_and_stack_explicit_views() -> None:
    episodes = tuple(
        datasets.stream(
            "2d-dyadaxes",
            count=2,
            shape=(3, 3),
            steps=2,
        )
    )
    assert len(episodes) == 2
    assert all(isinstance(item, datasets.DatasetEpisode) for item in episodes)

    batch = next(
        datasets.stream_batch(
            "2d-dyadaxes",
            count=3,
            batch_size=3,
            shape=(3, 3),
            steps=2,
        )
    )
    assert isinstance(batch, datasets.DatasetBatch)
    assert batch.states.shape == (3, 2, 3, 3)
    np.testing.assert_array_equal(
        batch.rule_ids, np.array([0, 1, 2], dtype=np.int64)
    )
    assert batch.metadata == {"batch_size": 3}


def test_projection_follows_lineage_not_support_tuple_order() -> None:
    plan = datasets.plan_episode(
        "1d-dyadrads",
        shape=(5,),
        steps=3,
        episode_index=2,
    )
    exact_seed = datasets._seed_for_plan(plan)
    simple_program = datasets._build_program(
        plan.dataset_id,
        rule=plan.rule_id,
        seed=exact_seed,
        shape=plan.shape,
        boundary=plan.boundary,
    )
    result = program.rollout(simple_program, steps=2)
    assert not isinstance(result, program.RolloutRejected)
    expected = datasets._project_dataset_episode(
        result,
        domain="t+1d",
        shape=(5,),
        rule_id=plan.rule_id,
        steps=3,
    )

    raw_trace = result.raw_trace
    reordered_applications = rules.finite_support(
        tuple(reversed(raw_trace.applications.atoms)),
        label="reordered-for-view-test",
    )
    reordered = replace(
        result,
        raw_trace=replace(
            raw_trace,
            applications=reordered_applications,
        ),
    )
    projected = datasets._project_dataset_episode(
        reordered,
        domain="t+1d",
        shape=(5,),
        rule_id=plan.rule_id,
        steps=3,
    )
    np.testing.assert_array_equal(projected.states, expected.states)


def test_ood_variants_remain_downstream_planning_data() -> None:
    scale = datasets.plan_episode("2d-dyadaxes", kind="ood-scale")
    boundary_0 = datasets.plan_episode(
        "2d-dyadaxes", kind="ood-boundary", episode_index=0
    )
    boundary_1 = datasets.plan_episode(
        "2d-dyadaxes", kind="ood-boundary", episode_index=1
    )
    invariant = datasets.plan_episode(
        "2d-dyadaxes", kind="invariance", episode_index=0
    )
    assert scale.shape == (15, 15)
    assert scale.steps == 17
    assert boundary_0.boundary == datasets.BoundarySpec("periodic")
    assert boundary_1.boundary == datasets.BoundarySpec("reflective")
    assert invariant.transform is not None
    assert invariant.transform.id == "rot-xy-90"
