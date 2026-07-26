"""Adversarial regressions for application integrity and Seed execution edges."""

from __future__ import annotations

from builtins import range as builtin_range
from dataclasses import replace as dataclass_replace

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import certificate, derivation, finite_record_program, no_successor


def _unknown_cardinality(label: str) -> rules.Undetermined:
    return rules.Undetermined(
        rules.literal_expr(f"{label}:cardinality"),
        certificate(rules.CertificateKind.CARDINALITY, f"{label}:obligation"),
    )


def _relation_program(
    seed: seeds.Seed,
    alphabet: alphabets.Alphabet,
    *,
    relation_label: str = "adversarial-unused-relation",
) -> ca.SimpleProgram:
    """Build a contract-compatible Rule whose denotation need never enumerate."""

    writable = frontiers.everywhere(
        configuration_contract=seed.configuration_contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=seed.configuration_contract,
        value_profile=alphabet.value_profile,
    )
    contract = rules.RuleContract(
        seed.configuration_contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
    )
    relation = rules.relation(
        rules.literal_expr(relation_label),
        _unknown_cardinality(relation_label),
        contract=contract,
        completeness_evidence=certificate(
            rules.CertificateKind.COMPLETENESS,
            f"{relation_label}:complete",
        ),
        soundness_evidence=certificate(
            rules.CertificateKind.SOUNDNESS,
            f"{relation_label}:sound",
        ),
    )
    return ca.SimpleProgram(seed, alphabet, writable, readable, relation)


def _literal_strings(expression: rules.RuleExpr) -> tuple[str, ...]:
    values: list[str] = []

    def walk(node: rules.RuleExpr) -> None:
        if node.primitive is rules.ExpressionPrimitive.LITERAL:
            value = node.arguments[0]
            if isinstance(value, str):
                values.append(value)
            return
        for argument in node.arguments:
            if type(argument) is rules.RuleExpr:
                walk(argument)

    walk(expression)
    return tuple(values)


def test_intensional_application_relations_bind_context_and_filter_projections() -> None:
    source = loci.record_configuration((("cell", False),))
    alternate = loci.record_configuration((("cell", True),))
    simple_program = _relation_program(
        seeds.exact(source),
        alphabets.boolean(),
        relation_label="input-independent-rule-relation",
    )
    left_lineage = program.TraceLineage("left-input-root")
    right_lineage = program.TraceLineage("right-input-root")
    alternate_lineage = program.TraceLineage("alternate-input-root")

    left = ca.apply(
        simple_program,
        program.ApplicationInput(source, left_lineage),
    )
    right = ca.apply(
        simple_program,
        program.ApplicationInput(source, right_lineage),
    )
    changed = ca.apply(
        simple_program,
        program.ApplicationInput(alternate, alternate_lineage),
    )

    assert isinstance(left, program.ApplicationComplete)
    assert isinstance(right, program.ApplicationComplete)
    assert isinstance(changed, program.ApplicationComplete)
    assert (
        left.source_outcomes.support.relation
        == right.source_outcomes.support.relation
        == changed.source_outcomes.support.relation
    )
    assert left.evidence.application_identity == right.evidence.application_identity
    assert (
        left.evidence.input_trace_lineage_identity
        == left_lineage.canonical_identity
    )
    assert (
        right.evidence.input_trace_lineage_identity
        == right_lineage.canonical_identity
    )

    projections = (
        (
            "applied_atoms",
            "application-projection:applied-atoms:v1",
            "filter:all-rule-atoms",
        ),
        (
            "no_successor_partition",
            "application-projection:no-successor-partition:v1",
            "filter:no-successor",
        ),
        (
            "successor_quotient_with_derivation_fibers",
            "application-projection:successor-quotient:v1",
            "filter:derivation",
        ),
    )
    for field_name, projection_label, filter_label in projections:
        left_relation = getattr(left, field_name).relation
        right_relation = getattr(right, field_name).relation
        changed_relation = getattr(changed, field_name).relation
        assert type(left_relation) is rules.RuleExpr
        assert type(right_relation) is rules.RuleExpr
        assert type(changed_relation) is rules.RuleExpr
        assert left_relation != right_relation
        assert left_relation != changed_relation
        left_literals = set(_literal_strings(left_relation))
        assert projection_label in left_literals
        assert filter_label in left_literals
        assert {
            left.evidence.program_identity,
            left.evidence.canonical_rule_identity,
            left.evidence.input_configuration_identity,
            left.evidence.readable_binding_identity,
            left.evidence.writable_binding_identity,
            left.evidence.input_trace_lineage_identity,
        }.issubset(left_literals)


def test_application_complete_rejects_cross_space_and_identity_contradictions() -> None:
    def atoms(targets: tuple[loci.Locus, ...]):
        return (
            derivation(
                "one-valid-derivation",
                existing=tuple(rules.preserve(target) for target in targets),
            ),
            no_successor("one-valid-no-successor"),
        )

    simple_program, source = finite_record_program(
        (("cell", False),),
        atoms,
    )
    valid = ca.apply(simple_program, source)
    assert isinstance(valid, program.ApplicationComplete)

    with pytest.raises(ValueError):
        dataclass_replace(
            valid,
            applied_atoms=rules.finite_support(
                valid.applied_atoms.atoms[:1],
                label="contradictory-applied-subset",
            ),
        )
    with pytest.raises(ValueError):
        dataclass_replace(
            valid,
            no_successor_partition=rules.finite_support(
                (),
                label="contradictory-no-successor-partition",
            ),
        )
    with pytest.raises(ValueError):
        dataclass_replace(
            valid,
            successor_cardinality=rules.finite_cardinality(0),
            successor_quotient_with_derivation_fibers=rules.finite_support(
                (),
                label="contradictory-successor-quotient",
            ),
        )

    alternate = loci.record_configuration((("cell", True),))
    other = ca.apply(simple_program, alternate)
    assert isinstance(other, program.ApplicationComplete)
    with pytest.raises(ValueError):
        dataclass_replace(valid, evidence=other.evidence)

    first = valid.applied_atoms.atoms[0]
    mismatched_atom = dataclass_replace(
        first,
        evidence=dataclass_replace(
            first.evidence,
            application_identity="foreign-application",
        ),
    )
    mismatched_atoms = (mismatched_atom, *valid.applied_atoms.atoms[1:])
    with pytest.raises(ValueError):
        dataclass_replace(
            valid,
            applied_atoms=rules.finite_support(
                mismatched_atoms,
                label="identity-mismatched-applied-space",
            ),
        )


def test_accepted_constructive_and_uniform_tuple_seeds_survive_zero_steps() -> None:
    history_contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(2,),
        axes=("history",),
    )
    record_contract = loci.CarrierContract(
        loci.CarrierKind.RECORD,
        rank=0,
        shape=(),
        axes=(),
    )
    grid_contract = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        shape=(2,),
        axes=("x",),
    )
    seed_cases = (
        (
            "grid",
            seeds.constructive(
                seeds.Construction(
                    seeds.ConstructionOp.GRID,
                    (
                        (2,),
                        (False, True),
                        (("policy", "fixed"), ("exterior", False)),
                    ),
                ),
                configuration_contract=grid_contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
            alphabets.boolean(),
        ),
        (
            "fill",
            seeds.constructive(
                seeds.Construction(
                    seeds.ConstructionOp.FILL,
                    (True,),
                ),
                configuration_contract=history_contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
            alphabets.boolean(),
        ),
        (
            "point",
            seeds.constructive(
                seeds.Construction(
                    seeds.ConstructionOp.POINT,
                    (loci.named("chosen", scope="record"), True),
                ),
                configuration_contract=record_contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
            alphabets.boolean(),
        ),
        (
            "empty",
            seeds.constructive(
                seeds.Construction(seeds.ConstructionOp.EMPTY),
                configuration_contract=record_contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
            alphabets.boolean(),
        ),
        (
            "uniform-tuple",
            seeds.law(
                seeds.UniformTupleLaw(length=2, value_count=3),
                configuration_contract=history_contract,
                value_profile=alphabets.ValueProfile.INTEGER,
                construction=seeds.Construction(
                    seeds.ConstructionOp.SEQUENCE
                ),
            ),
            alphabets.naturals(),
        ),
    )

    for case_id, seed, alphabet in seed_cases:
        result = ca.rollout(
            _relation_program(seed, alphabet, relation_label=f"{case_id}:unused"),
            steps=0,
        )
        assert not isinstance(result, program.RolloutRejected), (
            case_id,
            result,
        )
        assert isinstance(result, program.RolloutTruncated)
        assert result.cause is program.TruncationCause.DEPTH_BOUND
        assert (
            result.raw_trace.roots.support.presentation
            is rules.SupportPresentation.FINITE
        )


def test_constructive_grid_boundary_must_conform_before_execution() -> None:
    grid_contract = loci.CarrierContract(
        loci.CarrierKind.GRID,
        rank=1,
        shape=(2,),
        axes=("x",),
    )
    invalid_boundary_seed = seeds.constructive(
        seeds.Construction(
            seeds.ConstructionOp.GRID,
            (
                (2,),
                (False, True),
                (("policy", "fixed"), ("exterior", 7)),
            ),
        ),
        configuration_contract=grid_contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )

    with pytest.raises(
        program.ProgramCompatibilityError,
        match="does not conform to Alphabet",
    ):
        _relation_program(invalid_boundary_seed, alphabets.boolean())


def test_partial_seed_obligations_never_become_executable_complete_roots() -> None:
    configuration = loci.history_configuration((False, True))
    unresolved = (configuration.entries[0][0],)
    obligations = (
        loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP),
    )
    partial_seed = seeds.partial(
        configuration,
        unresolved=unresolved,
        obligations=obligations,
        configuration_contract=configuration.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )

    result = ca.rollout(
        _relation_program(partial_seed, alphabets.boolean()),
        steps=0,
    )

    assert isinstance(result, program.RolloutTruncated)
    assert result.cause is program.TruncationCause.INTENSIONAL_SUPPORT
    assert (
        result.raw_trace.roots.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert not result.raw_trace.roots.support.atoms
    assert (
        result.continuing_leaves.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    denotation = result.raw_trace.seed_evidence.denotation
    assert denotation is not None
    assert type(denotation.source) is seeds.PartialSource
    assert denotation.source.unresolved == unresolved
    assert denotation.source.obligations == obligations


def test_huge_uniform_tuple_uses_bounded_direct_sampling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Guard against both tuple(range(N)) and N-wide weight construction."""

    value_count = 1_000_000_000
    history_contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(2,),
        axes=("history",),
    )
    huge_seed = seeds.law(
        seeds.UniformTupleLaw(length=2, value_count=value_count),
        configuration_contract=history_contract,
        value_profile=alphabets.ValueProfile.INTEGER,
        construction=seeds.Construction(seeds.ConstructionOp.SEQUENCE),
    )

    observed_ranges: list[int] = []

    def guarded_range(*arguments: int):
        candidate = builtin_range(*arguments)
        size = len(candidate)
        observed_ranges.append(size)
        if size > 4_096:
            raise AssertionError(
                f"attempted to construct or traverse an oversized range: {size}"
            )
        return candidate

    observed_weighted_widths: list[tuple[int, int]] = []
    owned_select_weighted = program._select_weighted

    def guarded_select_weighted(values, weights, **kwargs):
        widths = (len(values), len(weights))
        observed_weighted_widths.append(widths)
        if max(widths) > 4_096:
            raise AssertionError(
                f"attempted an oversized weighted materialization: {widths}"
            )
        return owned_select_weighted(values, weights, **kwargs)

    monkeypatch.setattr(program, "range", guarded_range, raising=False)
    monkeypatch.setattr(program, "_select_weighted", guarded_select_weighted)

    simple_program = _relation_program(
        huge_seed,
        alphabets.naturals(),
        relation_label="huge-uniform-tuple:unused",
    )
    result = ca.rollout(
        simple_program,
        steps=0,
        replay_key="bounded-direct-uniform-sampling",
    )

    assert isinstance(result, program.RolloutTruncated)
    assert result.cause is program.TruncationCause.DEPTH_BOUND
    assert (
        result.raw_trace.roots.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert len(result.continuing_leaves.atoms) == 1
    selected = result.continuing_leaves.atoms[0].configuration
    assert isinstance(selected, loci.FiniteConfiguration)
    assert len(selected.entries) == 2
    assert all(
        isinstance(value, int) and 0 <= value < value_count
        for _, value in selected.entries
    )
    assert all(size <= 4_096 for size in observed_ranges)
    assert all(
        max(widths) <= 4_096 for widths in observed_weighted_widths
    )
