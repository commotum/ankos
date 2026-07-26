from __future__ import annotations

from fractions import Fraction

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


BLANK = alphabets.tag_value("blank", 0)
HEAD = alphabets.tag_value("head", 0)


def _certificate(
    kind: rules.CertificateKind,
    label: str,
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _derivation_result(
    outputs: tuple[alphabets.SemanticValue, ...],
    *,
    channel: int = 0,
    label: str = "move",
    progress: rules.Progress = rules.Progress.ADVANCED,
    certificate_template: rules.EvidenceTerm | None = None,
) -> rules.DerivationClauseResult:
    return rules.DerivationClauseResult(
        tuple(
            rules.ExistingDispositionPlan(
                rules.capability_group_item(channel, index),
                rules.DispositionAction.REPLACE,
                rules.literal_expr(value),
            )
            for index, value in enumerate(outputs)
        ),
        (),
        progress,
        rules.Continue(),
        rules.group(channel),
        (f"test:{label}",),
        _certificate(rules.CertificateKind.DERIVATION, f"{label}:derived"),
        certificate_template=certificate_template,
    )


def _zero_result() -> rules.DerivationClauseResult:
    return rules.DerivationClauseResult(
        (),
        (),
        rules.Progress.QUIESCENT,
        rules.Continue(),
        rules.literal_expr("zero-anchors"),
        ("test:zero-anchors",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "zero-anchors:derived",
        ),
    )


def _head_condition(channel: int = 0) -> rules.RuleExpr:
    return rules.equal(
        rules.project(rules.group(channel), 0),
        rules.literal_expr(HEAD),
    )


def _source(
    values: tuple[alphabets.SemanticValue, ...],
    *,
    boundary: loci.BoundaryPolicy = loci.BoundaryPolicy.NONE,
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    return loci.grid_configuration(
        (len(values),),
        values,
        boundary=loci.Boundary(boundary),
        axes=("x",),
    )


def _anchored_components(
    source: loci.FiniteConfiguration[alphabets.SemanticValue],
    *,
    cardinality: alphabets.AnchorCardinality,
    offsets: tuple[tuple[int, ...], ...] = ((0,), (1,)),
) -> tuple[
    alphabets.Alphabet[alphabets.SemanticValue],
    frontiers.WritableRegion[object, object],
    neighborhoods.ReadableRegion[object, object],
]:
    alphabet = alphabets.enum((BLANK, HEAD))
    anchor = alphabets.ValueAnchor(
        alphabets.value_tagged("head"),
        cardinality,
    )
    writable = frontiers.value_relative(
        anchor,
        offsets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.value_relative(
        anchor,
        offsets,
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    return alphabet, writable, readable


def _contract(
    source: loci.FiniteConfiguration[alphabets.SemanticValue],
    alphabet: alphabets.Alphabet[alphabets.SemanticValue],
    writable: frontiers.WritableRegion[object, object],
    readable: neighborhoods.ReadableRegion[object, object],
    *,
    entropy: seeds.EntropyInterface = seeds.EntropyInterface.NONE,
) -> rules.RuleContract:
    return rules.RuleContract(
        source.contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
        entropy_interface=entropy,
    )


def _simple_program(
    source: loci.FiniteConfiguration[alphabets.SemanticValue],
    *,
    cardinality: alphabets.AnchorCardinality,
    outputs: tuple[alphabets.SemanticValue, ...],
    conflict: rules.ProposalConflictPolicy = (
        rules.ProposalConflictPolicy.REQUIRE_EQUAL
    ),
    offsets: tuple[tuple[int, ...], ...] = ((0,), (1,)),
    certificate_template: rules.EvidenceTerm | None = None,
) -> program.SimpleProgram[object, object, object, object]:
    alphabet, writable, readable = _anchored_components(
        source,
        cardinality=cardinality,
        offsets=offsets,
    )
    clause = rules.RuleClause(
        _head_condition(),
        _derivation_result(
            outputs,
            certificate_template=certificate_template,
        ),
    )
    rule = rules.anchored_clause_kernel(
        (clause,),
        group_channel=0,
        conflict_policy=conflict,
        zero_result=_zero_result(),
        contract=_contract(
            source,
            alphabet,
            writable,
            readable,
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "anchored:complete",
        ),
    )
    return program.SimpleProgram(
        seeds.exact(
            source,
            value_profile=alphabet.value_profile,
        ),
        alphabet,
        writable,
        readable,
        rule,
    )


def _only_successor(
    result: program.ApplicationResult[
        loci.FiniteConfiguration[alphabets.SemanticValue]
    ],
) -> loci.FiniteConfiguration[alphabets.SemanticValue]:
    assert isinstance(result, program.ApplicationComplete)
    groups = result.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    return groups[0].successor


def _values(
    configuration: loci.FiniteConfiguration[alphabets.SemanticValue],
) -> tuple[alphabets.SemanticValue, ...]:
    return tuple(value for _, value in configuration.entries)


def test_exactly_one_tagged_source_writes_source_and_destination_atomically() -> None:
    source = _source((BLANK, BLANK, HEAD, BLANK, BLANK))
    assert source.entries[2][0] == loci.cell((0,), axes=("x",))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
        outputs=(BLANK, HEAD),
    )

    result = program.apply(simple, source)

    assert _values(_only_successor(result)) == (
        BLANK,
        BLANK,
        BLANK,
        HEAD,
        BLANK,
    )
    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert tuple(item.action for item in atom.replacement.existing) == (
        rules.DispositionAction.REPLACE,
        rules.DispositionAction.REPLACE,
    )
    assert tuple(item.target for item in atom.replacement.existing) == (
        loci.cell((0,), axes=("x",)),
        loci.cell((1,), axes=("x",)),
    )


def test_anchor_evidence_scalar_fallback_is_materialized_once() -> None:
    source = _source((BLANK, BLANK, HEAD, BLANK, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
        outputs=(BLANK, HEAD),
        certificate_template=rules.EvidenceTerm(
            "anchor-evidence",
            (7,),
        ),
    )

    result = program.apply(simple, source)

    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert atom.certificate.statement.arguments[2] == rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (
            rules.literal_expr("anchor-evidence"),
            rules.literal_expr(7),
        ),
    )


def test_multiple_active_sources_compose_one_total_disposition() -> None:
    source = _source((BLANK, HEAD, BLANK, HEAD, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.ONE_OR_MORE,
        outputs=(BLANK, HEAD),
    )

    result = program.apply(simple, source)

    assert _values(_only_successor(result)) == (
        BLANK,
        BLANK,
        HEAD,
        BLANK,
        HEAD,
    )
    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert len(atom.replacement.existing) == 4
    assert atom.replacement.totality_evidence.kind is rules.CertificateKind.TOTALITY


def test_require_equal_accepts_semantically_equal_overlap() -> None:
    source = _source((BLANK, HEAD, HEAD, BLANK, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.ONE_OR_MORE,
        outputs=(HEAD, HEAD),
    )

    result = program.apply(simple, source)

    assert _values(_only_successor(result)) == (
        BLANK,
        HEAD,
        HEAD,
        HEAD,
        BLANK,
    )


def test_require_equal_rejects_conflicting_overlap() -> None:
    source = _source((BLANK, HEAD, HEAD, BLANK, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.ONE_OR_MORE,
        outputs=(BLANK, HEAD),
    )

    result = program.apply(simple, source)

    assert isinstance(result, program.ApplicationRejected)
    assert "REQUIRE_EQUAL" in result.fault.reason


@pytest.mark.parametrize(
    ("policy", "overlap_value"),
    (
        (rules.ProposalConflictPolicy.FIRST, HEAD),
        (rules.ProposalConflictPolicy.LAST, BLANK),
    ),
)
def test_ordered_conflict_policies_are_explicit(
    policy: rules.ProposalConflictPolicy,
    overlap_value: alphabets.SemanticValue,
) -> None:
    source = _source((BLANK, HEAD, HEAD, BLANK, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.ONE_OR_MORE,
        outputs=(BLANK, HEAD),
        conflict=policy,
    )

    successor = _only_successor(program.apply(simple, source))

    assert successor.value_at(loci.cell((0,), axes=("x",))) == overlap_value


def test_zero_anchors_use_the_explicit_closed_zero_result() -> None:
    source = _source((BLANK, BLANK, BLANK))
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.ZERO_OR_MORE,
        outputs=(BLANK, HEAD),
    )

    result = program.apply(simple, source)

    successor = _only_successor(result)
    assert loci.configuration_equal(successor, source)
    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert atom.progress is rules.Progress.QUIESCENT
    assert atom.provenance == ("test:zero-anchors",)


def test_periodic_alias_selector_resolves_the_existing_writable_identity() -> None:
    source = _source(
        (BLANK, BLANK, HEAD),
        boundary=loci.BoundaryPolicy.PERIODIC,
    )
    simple = _simple_program(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
        outputs=(BLANK, HEAD),
        conflict=rules.ProposalConflictPolicy.LAST,
        offsets=((0,), (3,)),
    )

    result = program.apply(simple, source)

    assert loci.configuration_equal(_only_successor(result), source)
    assert isinstance(result, program.ApplicationComplete)
    atom = result.source_outcomes.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert len(atom.replacement.existing) == 1
    assert atom.replacement.existing[0].target == loci.cell((1,), axes=("x",))


def test_unweighted_all_forms_the_finite_cartesian_alternative_space() -> None:
    source = _source((BLANK, HEAD, BLANK))
    alphabet, writable, readable = _anchored_components(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
    )
    clauses = (
        rules.RuleClause(
            _head_condition(),
            _derivation_result((BLANK, HEAD), label="right"),
        ),
        rules.RuleClause(
            _head_condition(),
            _derivation_result((HEAD, BLANK), label="left"),
        ),
    )
    rule = rules.anchored_clause_kernel(
        clauses,
        group_channel=0,
        selection=rules.ClauseSelection.ALL,
        zero_result=_zero_result(),
        contract=_contract(source, alphabet, writable, readable),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "anchored-all:complete",
        ),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    assert len(result.outcome_space.support.atoms) == 2
    assert result.outcome_space.probability_law is None
    assert len(
        {
            atom.witness.canonical_identity
            for atom in result.outcome_space.support.atoms
            if isinstance(atom, rules.Derivation)
        }
    ) == 2


def test_weighted_all_multiplies_exact_anchor_local_masses() -> None:
    source = _source((HEAD, BLANK, HEAD, BLANK, BLANK))
    alphabet, writable, readable = _anchored_components(
        source,
        cardinality=alphabets.AnchorCardinality.ONE_OR_MORE,
    )
    clauses = (
        rules.RuleClause(
            _head_condition(),
            _derivation_result((BLANK, HEAD), label="advance"),
            Fraction(1, 3),
        ),
        rules.RuleClause(
            _head_condition(),
            _derivation_result((HEAD, BLANK), label="stay"),
            Fraction(2, 3),
        ),
    )
    rule = rules.anchored_clause_kernel(
        clauses,
        group_channel=0,
        selection=rules.ClauseSelection.ALL,
        conflict_policy=rules.ProposalConflictPolicy.FIRST,
        zero_result=_zero_result(),
        contract=_contract(
            source,
            alphabet,
            writable,
            readable,
            entropy=seeds.EntropyInterface.REPLAY_KEY,
        ),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "anchored-weighted:complete",
        ),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    assert len(result.outcome_space.support.atoms) == 4
    law = result.outcome_space.probability_law
    assert law is not None
    assert sorted(item.mass for item in law.masses) == [
        Fraction(1, 9),
        Fraction(2, 9),
        Fraction(2, 9),
        Fraction(4, 9),
    ]


def test_malformed_anchored_constructions_fail_closed() -> None:
    with pytest.raises(ValueError):
        rules.capability_group_item(-1, 0)
    with pytest.raises(ValueError):
        rules.capability_group_item(0, -1)

    source = _source((BLANK, HEAD, BLANK))
    alphabet, writable, readable = _anchored_components(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
    )
    contract = _contract(source, alphabet, writable, readable)
    completeness = _certificate(
        rules.CertificateKind.COMPLETENESS,
        "malformed:complete",
    )
    terminal = rules.NoSuccessorClauseResult(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.literal_expr("local-stop"),
        rules.literal_expr("local-stop"),
        ("test:local-stop",),
        _certificate(rules.CertificateKind.TERMINALITY, "local-stop"),
    )
    with pytest.raises(ValueError, match="NoSuccessor"):
        rules.anchored_clause_kernel(
            (rules.RuleClause(rules.literal_expr(True), terminal),),
            group_channel=0,
            zero_result=_zero_result(),
            contract=contract,
            completeness_evidence=completeness,
        )

    global_selector = rules.DerivationClauseResult(
        (
            rules.ExistingDispositionPlan(
                rules.capability_index(0),
                rules.DispositionAction.REPLACE,
                rules.literal_expr(HEAD),
            ),
        ),
        (),
        rules.Progress.ADVANCED,
        rules.Continue(),
        rules.literal_expr("global-selector"),
        ("test:global-selector",),
        _certificate(rules.CertificateKind.DERIVATION, "global-selector"),
    )
    with pytest.raises(ValueError, match="group-item"):
        rules.anchored_clause_kernel(
            (
                rules.RuleClause(
                    rules.literal_expr(True),
                    global_selector,
                ),
            ),
            group_channel=0,
            zero_result=_zero_result(),
            contract=contract,
            completeness_evidence=completeness,
        )

    with pytest.raises(ValueError, match="weighted"):
        rules.anchored_clause_kernel(
            (
                rules.RuleClause(
                    rules.literal_expr(True),
                    _derivation_result((BLANK, HEAD)),
                    Fraction(1),
                ),
            ),
            group_channel=0,
            selection=rules.ClauseSelection.FIRST,
            zero_result=_zero_result(),
            contract=rules.RuleContract(
                source.contract,
                alphabet.value_profile,
                readable.result_shape,
                readable.join_shape,
                writable.effect_profile,
                entropy_interface=seeds.EntropyInterface.REPLAY_KEY,
            ),
            completeness_evidence=completeness,
        )


def test_unresolvable_group_item_is_a_typed_rule_rejection() -> None:
    source = _source((BLANK, HEAD, BLANK))
    alphabet, writable, readable = _anchored_components(
        source,
        cardinality=alphabets.AnchorCardinality.EXACTLY_ONE,
    )
    invalid_result = _derivation_result((BLANK, HEAD, HEAD))
    rule = rules.anchored_clause_kernel(
        (
            rules.RuleClause(
                _head_condition(),
                invalid_result,
            ),
        ),
        group_channel=0,
        zero_result=_zero_result(),
        contract=_contract(source, alphabet, writable, readable),
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "invalid-item:complete",
        ),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleRejected)
    assert result.fault.reason is rules.RuleFaultReason.EVALUATION_FAILURE
    assert "outside channel" in result.fault.detail
