from __future__ import annotations

import pytest

from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
)


def _state(tag: str, payload: int = 0) -> alphabets.ValueNode:
    return alphabets.tag_value(tag, payload)


def _anchor(
    cardinality: alphabets.AnchorCardinality = (
        alphabets.AnchorCardinality.EXACTLY_ONE
    ),
) -> alphabets.ValueAnchor:
    return alphabets.ValueAnchor(
        alphabets.value_tagged("head"),
        cardinality,
    )


def _grid(
    values: tuple[alphabets.SemanticValue, ...],
    policy: loci.BoundaryPolicy = loci.BoundaryPolicy.NONE,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    boundary = (
        loci.Boundary(policy, _state("outside"))
        if policy is loci.BoundaryPolicy.FIXED
        else loci.Boundary(policy)
    )
    return loci.grid_configuration(
        (len(values),),
        values,
        boundary=boundary,
        axes=("x",),
    )


def test_single_value_anchor_binds_shared_snapshot_and_ordered_group() -> None:
    source = _grid(
        (
            _state("cell"),
            _state("cell"),
            _state("head", 1),
            _state("cell"),
            _state("cell"),
        )
    )
    anchor = _anchor()
    writable = frontiers.value_relative(anchor, ((0,), (1,))).resolve(source)
    readable = neighborhoods.value_relative(
        anchor,
        ((-1,), (0,), (1,)),
    ).resolve(source)

    center = loci.cell((0,), axes=("x",))
    assert writable.snapshot_identity == source.identity
    assert readable.snapshot_identity == source.identity
    assert readable.snapshot_identity == writable.snapshot_identity
    assert writable.targets == (
        center,
        loci.cell((1,), axes=("x",)),
    )
    assert tuple(observation.target for observation in readable.observations) == (
        loci.cell((-1,), axes=("x",)),
        center,
        loci.cell((1,), axes=("x",)),
    )
    assert tuple(observation.anchor for observation in readable.observations) == (
        center,
        center,
        center,
    )
    assert len(readable.groups) == 1
    assert readable.groups[0].indices == (0, 1, 2)
    assert readable.groups[0].anchor == center
    assert readable.groups[0].key.anchor == center
    assert readable.dependencies[0].value_anchor == anchor

    changed = _grid(
        (
            _state("cell", 9),
            _state("cell"),
            _state("head", 1),
            _state("cell"),
            _state("cell"),
        )
    )
    assert (
        neighborhoods.value_relative(
            anchor,
            ((0,),),
        ).resolve(changed).snapshot_identity
        != readable.snapshot_identity
    )


def test_multiple_anchors_deduplicate_writes_but_preserve_read_groups() -> None:
    source = _grid(
        (
            _state("cell"),
            _state("head", 1),
            _state("head", 2),
            _state("cell"),
            _state("cell"),
        )
    )
    anchor = _anchor(alphabets.AnchorCardinality.ONE_OR_MORE)

    writable = frontiers.value_relative(anchor, ((0,), (1,))).resolve(source)
    readable = neighborhoods.value_relative(anchor, ((0,), (1,))).resolve(
        source
    )

    left = loci.cell((-1,), axes=("x",))
    center = loci.cell((0,), axes=("x",))
    right = loci.cell((1,), axes=("x",))
    assert writable.targets == (left, center, right)
    assert tuple(observation.target for observation in readable.observations) == (
        left,
        center,
        center,
        right,
    )
    assert tuple(group.indices for group in readable.groups) == (
        (0, 1),
        (2, 3),
    )
    assert tuple(group.anchor for group in readable.groups) == (left, center)
    assert tuple(
        observation.anchor for observation in readable.observations
    ) == (left, left, center, center)


def test_zero_or_more_anchor_produces_explicit_empty_envelopes() -> None:
    source = _grid((_state("cell"), _state("cell"), _state("cell")))
    anchor = _anchor(alphabets.AnchorCardinality.ZERO_OR_MORE)

    writable = frontiers.value_relative(anchor, ((0,),)).resolve(source)
    readable = neighborhoods.value_relative(anchor, ((0,),)).resolve(source)

    assert writable.targets == ()
    assert writable.reconstruction.lenses == ()
    assert readable.observations == ()
    assert readable.groups == ()
    assert readable.dependencies[0].value_anchor == anchor
    assert readable.snapshot_identity == writable.snapshot_identity


def test_zero_or_more_no_anchor_is_a_valid_quiescent_public_apply() -> None:
    source = loci.grid_configuration(
        (3,),
        (False, False, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        axes=("x",),
    )
    alphabet = alphabets.boolean()
    anchor = alphabets.ValueAnchor(
        alphabets.value_equals(True),
        alphabets.AnchorCardinality.ZERO_OR_MORE,
    )
    writable = frontiers.value_relative(
        anchor,
        ((0,),),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.value_relative(
        anchor,
        ((0,),),
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(rules.ExistingPlanKind.PRESERVE, ()),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("zero-anchor-quiescence"),
        provenance=("test:value-anchor",),
        progress=rules.Progress.QUIESCENT,
    )
    simple = program.SimpleProgram(
        seeds.exact(source),
        alphabet,
        writable,
        readable,
        rule,
    )

    result = program.apply(simple, source)

    assert isinstance(result, program.ApplicationComplete)
    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    assert loci.configuration_equal(groups[0].successor, source)


@pytest.mark.parametrize(
    ("values", "cardinality"),
    (
        (
            (_state("cell"), _state("cell"), _state("cell")),
            alphabets.AnchorCardinality.EXACTLY_ONE,
        ),
        (
            (_state("head"), _state("head"), _state("cell")),
            alphabets.AnchorCardinality.EXACTLY_ONE,
        ),
        (
            (_state("cell"), _state("cell"), _state("cell")),
            alphabets.AnchorCardinality.ONE_OR_MORE,
        ),
    ),
)
def test_value_anchor_cardinality_failures_are_shared(
    values: tuple[alphabets.SemanticValue, ...],
    cardinality: alphabets.AnchorCardinality,
) -> None:
    source = _grid(values)
    anchor = _anchor(cardinality)

    with pytest.raises(frontiers.WritableResolutionError):
        frontiers.value_relative(anchor, ((0,),)).resolve(source)
    with pytest.raises(neighborhoods.ReadableResolutionError):
        neighborhoods.value_relative(anchor, ((0,),)).resolve(source)


def test_history_groups_retain_each_selected_occurrence_identity() -> None:
    source = loci.history_configuration(
        (_state("head", 1), _state("cell"), _state("head", 2))
    )
    anchor = _anchor(alphabets.AnchorCardinality.ONE_OR_MORE)

    writable = frontiers.value_relative(anchor, ((0,),)).resolve(source)
    readable = neighborhoods.value_relative(anchor, ((0,),)).resolve(source)

    first = loci.occurrence("history", 0)
    last = loci.occurrence("history", 2)
    assert writable.targets == (first, last)
    assert tuple(group.anchor for group in readable.groups) == (first, last)
    assert tuple(observation.target for observation in readable.observations) == (
        first,
        last,
    )
    assert tuple(
        observation.anchor for observation in readable.observations
    ) == (first, last)


@pytest.mark.parametrize(
    ("policy", "expected"),
    (
        (loci.BoundaryPolicy.PERIODIC, -1),
        (loci.BoundaryPolicy.REFLECTIVE, 0),
    ),
)
def test_aliased_boundaries_resolve_actual_existing_identity(
    policy: loci.BoundaryPolicy,
    expected: int,
) -> None:
    source = _grid(
        (_state("cell"), _state("cell"), _state("head")),
        policy,
    )
    anchor = _anchor()
    expected_target = loci.cell((expected,), axes=("x",))

    writable = frontiers.value_relative(anchor, ((1,),)).resolve(source)
    readable = neighborhoods.value_relative(anchor, ((1,),)).resolve(source)

    assert writable.targets == (expected_target,)
    assert readable.observations[0].target == expected_target
    assert isinstance(readable.observations[0].state, neighborhoods.Present)


def test_periodic_aliases_are_deduplicated_only_in_write_envelope() -> None:
    source = _grid(
        (_state("cell"), _state("cell"), _state("head")),
        loci.BoundaryPolicy.PERIODIC,
    )
    anchor = _anchor()
    head = loci.cell((1,), axes=("x",))

    writable = frontiers.value_relative(anchor, ((0,), (3,))).resolve(source)
    readable = neighborhoods.value_relative(anchor, ((0,), (3,))).resolve(
        source
    )

    assert writable.targets == (head,)
    assert tuple(observation.target for observation in readable.observations) == (
        head,
        head,
    )
    assert readable.groups[0].indices == (0, 1)


def test_fixed_and_absent_boundary_laws_fail_closed_for_writes() -> None:
    anchor = _anchor()
    for policy in (loci.BoundaryPolicy.FIXED, loci.BoundaryPolicy.NONE):
        source = _grid(
            (_state("cell"), _state("cell"), _state("head")),
            policy,
        )
        with pytest.raises(frontiers.WritableResolutionError):
            frontiers.value_relative(anchor, ((1,),)).resolve(source)

    fixed = _grid(
        (_state("cell"), _state("cell"), _state("head")),
        loci.BoundaryPolicy.FIXED,
    )
    fixed_view = neighborhoods.value_relative(anchor, ((1,),)).resolve(fixed)
    assert isinstance(
        fixed_view.observations[0].state,
        neighborhoods.BoundaryDefault,
    )

    absent = _grid(
        (_state("cell"), _state("cell"), _state("head")),
        loci.BoundaryPolicy.NONE,
    )
    with pytest.raises(neighborhoods.ReadableResolutionError):
        neighborhoods.value_relative(anchor, ((1,),)).resolve(absent)


def test_value_paths_exact_predicates_and_boolean_composition() -> None:
    selected = alphabets.record_value(
        (
            ("armed", True),
            ("role", alphabets.tag_value("head", 7)),
        ),
        tag="machine-state",
    )
    other = alphabets.record_value(
        (
            ("armed", False),
            ("role", alphabets.tag_value("head", 8)),
        ),
        tag="machine-state",
    )
    predicate = alphabets.value_and(
        (
            alphabets.value_tagged(
                "head",
                path=alphabets.ValuePath(("role",)),
            ),
            alphabets.value_equals(
                True,
                path=alphabets.ValuePath(("armed",)),
            ),
            alphabets.value_not(
                alphabets.value_equals(
                    8,
                    path=alphabets.ValuePath(("role", 0)),
                )
            ),
        )
    )

    assert alphabets.value_matches(predicate, selected)
    assert not alphabets.value_matches(predicate, other)
    assert alphabets.value_matches(
        alphabets.value_or(
            (
                alphabets.value_equals(other),
                alphabets.value_equals(selected),
            )
        ),
        selected,
    )


def test_malformed_paths_carriers_ranks_and_boundaries_fail_closed() -> None:
    with pytest.raises(TypeError):
        alphabets.ValuePath((True,))
    with pytest.raises(alphabets.ValueSelectionError):
        alphabets.ValuePath((-1,))
    with pytest.raises(alphabets.ValueSelectionError):
        alphabets.resolve_value_path(1, alphabets.ValuePath((0,)))

    anchor = _anchor()
    record = loci.record_configuration((("state", _state("head")),))
    with pytest.raises(frontiers.WritableResolutionError):
        frontiers.value_relative(anchor, ((0,),)).resolve(record)
    with pytest.raises(neighborhoods.ReadableResolutionError):
        neighborhoods.value_relative(anchor, ((0,),)).resolve(record)

    grid = _grid((_state("cell"), _state("head"), _state("cell")))
    with pytest.raises(frontiers.WritableResolutionError):
        frontiers.value_relative(anchor, ((0, 0),)).resolve(grid)
    with pytest.raises(neighborhoods.ReadableResolutionError):
        neighborhoods.value_relative(anchor, ((0, 0),)).resolve(grid)
