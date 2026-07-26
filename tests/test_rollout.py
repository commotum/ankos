"""Focused tests for program-owned semantic traversal."""

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds


def _program(seed=None):
    source = loci.history_configuration((True, False, False))
    alphabet = alphabets.boolean()
    if seed is None:
        seed = seeds.exact(source)
    return (
        ca.SimpleProgram(
            seed,
            alphabet,
            frontiers.everywhere(
                configuration_contract=source.contract,
                value_profile=alphabet.value_profile,
            ),
            neighborhoods.dyadlags_0d(
                configuration_contract=source.contract
            ),
            rules.dyadlags_0d(rule=150),
        ),
        source,
    )


def test_zero_step_rollout_retains_root_and_reports_depth_bound() -> None:
    simple_program, source = _program()

    result = ca.rollout(simple_program, steps=0, initial=source)

    assert isinstance(result, program.RolloutTruncated)
    assert result.cause is program.TruncationCause.DEPTH_BOUND
    assert result.raw_trace.roots.support.atoms == (source,)
    assert not result.raw_trace.applications.atoms
    assert result.continuing_leaves.atoms[0].configuration == source


def test_deterministic_rollout_retains_each_application_and_lineage_edge() -> None:
    simple_program, source = _program()

    result = ca.rollout(simple_program, steps=3, initial=source)

    assert isinstance(result, program.RolloutTruncated)
    assert len(result.raw_trace.applications.atoms) == 3
    assert len(result.raw_trace.derivation_edges.atoms) == 3
    assert len(result.raw_trace.lineage_graph) == 3
    lineage = result.continuing_leaves.atoms[0].trace_lineage
    assert len(lineage.path) == 3


def test_invalid_bounds_and_initial_values_return_typed_rejections() -> None:
    simple_program, _ = _program()

    negative = ca.rollout(simple_program, steps=-1)
    boolean = ca.rollout(simple_program, steps=True)  # type: ignore[arg-type]
    invalid_initial = ca.rollout(
        simple_program,
        steps=1,
        initial=loci.history_configuration((0, 1, 0)),
    )

    assert isinstance(negative, program.RolloutRejected)
    assert isinstance(boolean, program.RolloutRejected)
    assert isinstance(invalid_initial, program.RolloutRejected)


def test_seed_law_is_retained_and_replay_draw_is_deterministic() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    seed = seeds.uniform_bits(length=3, configuration_contract=contract)
    simple_program, _ = _program(seed)

    left = ca.rollout(simple_program, steps=0, replay_key="key")
    right = ca.rollout(simple_program, steps=0, replay_key="key")

    assert isinstance(left, program.RolloutTruncated)
    assert isinstance(right, program.RolloutTruncated)
    assert len(left.raw_trace.roots.support.atoms) == 8
    assert left.raw_trace.roots.probability_law is not None
    assert len(left.continuing_leaves.atoms) == 1
    assert left.continuing_leaves == right.continuing_leaves
    assert left.raw_trace.seed_evidence == right.raw_trace.seed_evidence


def test_constructive_seed_realizes_at_zero_steps_but_partiality_does_not() -> None:
    source = loci.history_configuration((True, False, False))
    fill_seed = seeds.constructive(
        seeds.Construction(seeds.ConstructionOp.FILL, (True,)),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    filled_program, _ = _program(fill_seed)

    filled = ca.rollout(filled_program, steps=0)

    assert isinstance(filled, program.RolloutTruncated)
    assert filled.cause is program.TruncationCause.DEPTH_BOUND
    realized = filled.continuing_leaves.atoms[0].configuration
    assert isinstance(realized, loci.FiniteConfiguration)
    assert tuple(value for _, value in realized.entries) == (True, True, True)

    obligation = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    partial_seed = seeds.partial(
        source,
        unresolved=(source.entries[0][0],),
        obligations=(obligation,),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    partial_program, _ = _program(partial_seed)

    partial = ca.rollout(partial_program, steps=0)

    assert isinstance(partial, program.RolloutTruncated)
    assert partial.cause is program.TruncationCause.INTENSIONAL_SUPPORT
    assert (
        partial.raw_trace.roots.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    denotation = partial.raw_trace.seed_evidence.denotation
    assert denotation is not None
    assert isinstance(denotation.source, seeds.PartialSource)
    assert denotation.source.obligations == (obligation,)


def test_rollout_accepts_only_settled_keywords() -> None:
    simple_program, source = _program()

    with pytest.raises(TypeError):
        ca.rollout(
            simple_program,
            steps=1,
            initial=source,
            observer=object(),  # type: ignore[call-arg]
        )
