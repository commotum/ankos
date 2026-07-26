"""Unit tests for closed Rule denotations and results."""

from dataclasses import dataclass
from fractions import Fraction

import pytest

from ca import alphabets, frontiers, loci, neighborhoods, rules, seeds


def _certificate(kind: rules.CertificateKind) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(kind.value))


@dataclass(frozen=True, eq=False)
class _EqualityMaskingAtom:
    identity: str

    @property
    def canonical_identity(self) -> str:
        return self.identity

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _EqualityMaskingAtom)


def _bindings():
    source = loci.history_configuration((True, False, False))
    writable_region = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    readable_region = neighborhoods.dyadlags_0d(
        configuration_contract=source.contract
    )
    return (
        source,
        readable_region.resolve(source),
        writable_region.resolve(source),
    )


def _kernel_contract(
    source,
    readable,
    writable,
    *,
    value_profile: alphabets.ValueProfile,
    entropy: seeds.EntropyInterface = seeds.EntropyInterface.NONE,
) -> rules.RuleContract:
    return rules.RuleContract(
        source.contract,
        value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
        entropy_interface=entropy,
    )


def _derivation_clause_result(
    *,
    existing: tuple[rules.ExistingDispositionPlan, ...] = (),
    fresh: tuple[rules.FreshDispositionPlan, ...] = (),
    witness: rules.RuleExpr | None = None,
    certificate_template: rules.EvidenceTerm | None = None,
    provenance_templates: tuple[rules.ProvenanceTemplate, ...] = (),
) -> rules.DerivationClauseResult:
    return rules.DerivationClauseResult(
        existing_plans=existing,
        fresh_plans=fresh,
        progress=rules.Progress.ADVANCED,
        continuation=rules.Continue(),
        witness=witness or rules.literal_expr("clause"),
        provenance=("test:clause-kernel",),
        certificate=_certificate(rules.CertificateKind.DERIVATION),
        certificate_template=certificate_template,
        provenance_templates=provenance_templates,
    )


def test_rule_expression_ast_is_closed_versioned_and_exact() -> None:
    expression = rules.lookup(
        (False, True),
        rules.modulo(
            rules.add(rules.observation(0), rules.literal_expr(1)),
            2,
        ),
    )

    assert expression.version == 1
    assert expression.primitive is rules.ExpressionPrimitive.LOOKUP
    assert expression.canonical_identity == expression.canonical_identity
    with pytest.raises(TypeError):
        rules.RuleExpr(
            rules.ExpressionPrimitive.LITERAL,
            (lambda: None,),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("primitive", "arguments"),
    (
        (rules.ExpressionPrimitive.LITERAL, ()),
        (
            rules.ExpressionPrimitive.LITERAL,
            (rules.literal_expr(1),),
        ),
        (rules.ExpressionPrimitive.OBSERVATION, (True,)),
        (rules.ExpressionPrimitive.GROUP, (-1,)),
        (
            rules.ExpressionPrimitive.TARGET_REFERENCE,
            (rules.literal_expr(1),),
        ),
        (rules.ExpressionPrimitive.PROJECT, (rules.literal_expr(1),)),
        (
            rules.ExpressionPrimitive.PROJECT,
            (1, 0),
        ),
        (rules.ExpressionPrimitive.TUPLE, (1,)),
        (rules.ExpressionPrimitive.ADD, ()),
        (rules.ExpressionPrimitive.ADD, (1,)),
        (rules.ExpressionPrimitive.MULTIPLY, ()),
        (rules.ExpressionPrimitive.MULTIPLY, (1,)),
        (
            rules.ExpressionPrimitive.MODULO,
            (rules.literal_expr(1), 0),
        ),
        (
            rules.ExpressionPrimitive.COUNT,
            (rules.literal_expr(1), rules.literal_expr(2)),
        ),
        (
            rules.ExpressionPrimitive.GATE,
            (rules.literal_expr(1), "unknown", 0),
        ),
        (
            rules.ExpressionPrimitive.GATE,
            (rules.literal_expr(1), rules.GateKind.ANY.value, True),
        ),
        (
            rules.ExpressionPrimitive.LOOKUP,
            (rules.literal_expr(1),),
        ),
        (
            rules.ExpressionPrimitive.EQUAL,
            (rules.literal_expr(1), 1),
        ),
        (
            rules.ExpressionPrimitive.SUBTRACT,
            (rules.literal_expr(1),),
        ),
        (
            rules.ExpressionPrimitive.DIVIDE,
            (rules.literal_expr(1), 2),
        ),
        (
            rules.ExpressionPrimitive.LESS,
            (rules.literal_expr(1),),
        ),
        (
            rules.ExpressionPrimitive.LESS_EQUAL,
            (1, rules.literal_expr(2)),
        ),
        (
            rules.ExpressionPrimitive.CONDITIONAL,
            (rules.literal_expr(1), rules.literal_expr(2)),
        ),
        (rules.ExpressionPrimitive.ALL, (1,)),
        (rules.ExpressionPrimitive.ANY, ()),
    ),
)
def test_rule_expression_primitives_reject_wrong_arity_or_types(
    primitive: rules.ExpressionPrimitive,
    arguments: tuple[object, ...],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        rules.RuleExpr(primitive, arguments)  # type: ignore[arg-type]


def test_rule_expression_and_evidence_collections_require_exact_tuples() -> None:
    with pytest.raises(TypeError, match="immutable tuple"):
        rules.RuleExpr(
            rules.ExpressionPrimitive.LITERAL,
            [1],  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError, match="immutable tuple"):
        rules.EvidenceTerm("proof", [1])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="immutable tuple"):
        rules.ProvenanceTemplate("{}", [rules.literal_expr(1)])  # type: ignore[arg-type]


def test_cardinality_variants_require_exact_cardinality_certificates() -> None:
    wrong = _certificate(rules.CertificateKind.SOUNDNESS)

    for constructor in (
        lambda: rules.ExactlyZero(wrong),
        lambda: rules.ExactlyOne(wrong),
        lambda: rules.Many(2, None, wrong),
        lambda: rules.Undetermined(rules.literal_expr("unknown"), wrong),
    ):
        with pytest.raises(ValueError, match="cardinality evidence"):
            constructor()

    with pytest.raises(TypeError, match="infinite cardinality"):
        rules.Many(
            None,
            "uncountable",  # type: ignore[arg-type]
            _certificate(rules.CertificateKind.CARDINALITY),
        )


def test_support_and_probability_canonicalize_by_identity_sequence() -> None:
    support = rules.finite_support(
        (_EqualityMaskingAtom("z"), _EqualityMaskingAtom("a"))
    )

    assert tuple(atom.canonical_identity for atom in support.atoms) == ("a", "z")

    law = rules.ProbabilityLaw(
        rules.ProbabilityPresentation.FINITE,
        (
            rules.AtomMass("z", Fraction(1, 2)),
            rules.AtomMass("a", Fraction(1, 2)),
        ),
        None,
        _certificate(rules.CertificateKind.NORMALIZATION),
        _certificate(rules.CertificateKind.MEASURABILITY),
    )
    assert tuple(item.atom_identity for item in law.masses) == ("a", "z")


def test_rule_fault_and_result_wrappers_are_closed_exact_variants() -> None:
    conformance = _certificate(rules.CertificateKind.CONFORMANCE)
    with pytest.raises(TypeError, match="Certificate tuple"):
        rules.RuleFault(
            rules.RuleFaultPhase.DENOTATION,
            rules.RuleFaultReason.INVALID_DESCRIPTOR,
            [conformance],  # type: ignore[arg-type]
            "invalid",
        )
    with pytest.raises(TypeError, match="fault variant"):
        rules.RuleRejected(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="outcome space"):
        rules.RuleComplete(object())  # type: ignore[arg-type]

    unknown_support = rules.finite_support((_EqualityMaskingAtom("unknown"),))
    with pytest.raises(TypeError, match="unknown atom variant"):
        rules.RuleComplete(rules.OutcomeSpace(unknown_support))  # type: ignore[arg-type]


def test_public_evidence_and_evaluation_ast_types_are_exported_and_closed() -> None:
    expected = {
        "EvaluationProof",
        "EvaluationScope",
        "EvaluationStep",
        "EvidenceExpression",
        "EvidenceTerm",
        "FormattedEvidence",
        "ProvenanceTemplate",
    }
    assert expected.issubset(set(rules.__all__))

    step = rules.EvaluationStep(
        rules.literal_expr(1),
        None,
        1,
        ("read",),
    )
    proof = rules.EvaluationProof((step,))
    assert proof.steps == (step,)

    with pytest.raises(TypeError, match="EvaluationStep tuple"):
        rules.EvaluationProof([step])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="read evidence"):
        rules.EvaluationStep(
            rules.literal_expr(1),
            None,
            1,
            ["read"],  # type: ignore[arg-type]
        )


def test_clause_kernel_records_and_helpers_are_public() -> None:
    expected = {
        "CapabilitySelector",
        "CapabilitySelectorKind",
        "ClauseKernelDenotation",
        "ClauseResult",
        "ClauseSelection",
        "DerivationClauseResult",
        "ExistingDispositionPlan",
        "FreshDispositionPlan",
        "NoSuccessorClauseResult",
        "RuleClause",
        "capability_index",
        "capability_target",
        "clause_kernel",
        "conditional",
        "divide",
        "equal",
        "every_capability",
        "less_equal",
        "less_than",
        "subtract",
        "target_reference",
    }

    assert expected.issubset(set(rules.__all__))


def test_native_rule_denotes_one_total_derivation() -> None:
    source, readable, writable = _bindings()
    rule = rules.dyadlags_0d(rule=150)

    result = rule.denote(readable, writable)

    assert isinstance(result, rules.RuleComplete)
    support = result.outcome_space.support
    assert support.presentation is rules.SupportPresentation.FINITE
    assert rules.cardinality_size(support.cardinality) == 1
    atom = support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert tuple(item.target for item in atom.replacement.existing) == tuple(
        target for target, _ in source.entries
    )
    assert not atom.replacement.fresh
    assert atom.progress is rules.Progress.ADVANCED
    assert isinstance(atom.continuation, rules.Continue)


def test_cardinality_and_probability_records_remain_independent() -> None:
    source, readable, writable = _bindings()
    base = rules.dyadlags_0d(rule=150).denote(readable, writable)
    assert isinstance(base, rules.RuleComplete)
    atom = base.outcome_space.support.atoms[0]
    second = rules.Derivation(
        atom.replacement,
        atom.progress,
        atom.continuation,
        rules.Witness("second", rules.literal_expr("second")),
        ("test:second",),
        atom.certificate,
    )
    support = rules.finite_support((atom, second))
    law = rules.finite_probability_law(
        ((atom, Fraction(1, 4)), (second, Fraction(3, 4)))
    )
    outcomes = rules.OutcomeSpace(support, law)

    assert rules.cardinality_size(outcomes.support.cardinality) == 2
    assert sorted(item.mass for item in outcomes.probability_law.masses) == [
        Fraction(1, 4),
        Fraction(3, 4),
    ]
    assert not hasattr(outcomes.probability_law, "draw")


def test_no_successor_atoms_are_typed_not_empty_support() -> None:
    atom = rules.NoSuccessor(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.literal_expr("done"),
        rules.Witness("terminal", rules.literal_expr("terminal")),
        ("test:terminal",),
        rules.Certificate(
            rules.CertificateKind.TERMINALITY,
            rules.literal_expr("proved-terminal"),
        ),
    )

    support = rules.finite_support((atom,))

    assert rules.cardinality_size(support.cardinality) == 1
    assert support.atoms == (atom,)
    assert rules.cardinality_size(rules.finite_support(()).cardinality) == 0


def test_intensional_relation_retains_cardinality_obligation_without_solver() -> None:
    source, _, _ = _bindings()
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    certificate = rules.Certificate(
        rules.CertificateKind.CARDINALITY,
        rules.literal_expr("obligation"),
    )
    unknown = rules.Undetermined(
        rules.literal_expr("not-enumerated"),
        certificate,
    )
    contract = rules.RuleContract(
        source.contract,
        alphabets.ValueProfile.BOOLEAN,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
    )
    rule = rules.relation(
        rules.literal_expr("x satisfies relation"),
        unknown,
        contract=contract,
        completeness_evidence=rules.Certificate(
            rules.CertificateKind.COMPLETENESS,
            rules.literal_expr("complete"),
        ),
        soundness_evidence=rules.Certificate(
            rules.CertificateKind.SOUNDNESS,
            rules.literal_expr("sound"),
        ),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    assert result.outcome_space.support.presentation is rules.SupportPresentation.INTENSIONAL
    assert isinstance(result.outcome_space.support.cardinality, rules.Undetermined)


def test_clause_kernel_all_branches_with_exact_normalized_probability() -> None:
    source = loci.record_configuration((("mode", 1), ("value", 3)))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    value_target = source.entries[1][0]
    shared = {
        "certificate_template": rules.EvidenceTerm(
            "evaluated-result",
            (rules.EvidenceExpression(rules.observation(1)),),
        ),
        "provenance_templates": (
            rules.ProvenanceTemplate("mode={0}", (rules.observation(0),)),
        ),
    }
    clauses = (
        rules.RuleClause(
            rules.equal(rules.observation(0), rules.literal_expr(1)),
            _derivation_clause_result(
                existing=(
                    rules.ExistingDispositionPlan(
                        rules.capability_target(value_target),
                        rules.DispositionAction.REPLACE,
                        rules.add(rules.observation(1), rules.literal_expr(1)),
                    ),
                ),
                witness=rules.add(
                    rules.observation(1),
                    rules.literal_expr(10),
                ),
                **shared,
            ),
            Fraction(1, 4),
        ),
        rules.RuleClause(
            rules.less_equal(rules.observation(1), rules.literal_expr(3)),
            _derivation_clause_result(
                existing=(
                    rules.ExistingDispositionPlan(
                        rules.capability_index(1),
                        rules.DispositionAction.REPLACE,
                        rules.multiply(
                            rules.observation(1),
                            rules.literal_expr(2),
                        ),
                    ),
                ),
                witness=rules.add(
                    rules.observation(1),
                    rules.literal_expr(10),
                ),
                **shared,
            ),
            Fraction(3, 4),
        ),
    )
    rule = rules.clause_kernel(
        clauses,
        contract=_kernel_contract(
            source,
            readable,
            writable,
            value_profile=alphabets.ValueProfile.INTEGER,
            entropy=seeds.EntropyInterface.REPLAY_KEY,
        ),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    atoms = result.outcome_space.support.atoms
    assert len(atoms) == 2
    assert all(isinstance(atom, rules.Derivation) for atom in atoms)
    assert {
        atom.replacement.existing[1].payload.value
        for atom in atoms
        if isinstance(
            atom.replacement.existing[1].payload,
            rules.ValuePayload,
        )
    } == {4, 6}
    assert all(
        atom.replacement.existing[0].action
        is rules.DispositionAction.PRESERVE
        for atom in atoms
    )
    assert all("mode=1" in atom.provenance for atom in atoms)
    assert all(
        atom.certificate.statement.primitive
        is rules.ExpressionPrimitive.TUPLE
        for atom in atoms
    )
    assert all(
        atom.witness.descriptor.arguments[3].arguments == (13,)
        for atom in atoms
    )
    law = result.outcome_space.probability_law
    assert law is not None
    assert sorted(item.mass for item in law.masses) == [
        Fraction(1, 4),
        Fraction(3, 4),
    ]


def test_clause_kernel_first_uses_explicit_typed_fallback() -> None:
    source = loci.record_configuration((("mode", 0),))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    terminal = rules.NoSuccessorClauseResult(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.conditional(
            rules.equal(rules.observation(0), rules.literal_expr(0)),
            rules.literal_expr("inactive"),
            rules.literal_expr("unexpected"),
        ),
        rules.observation(0),
        ("test:explicit-fallback",),
        _certificate(rules.CertificateKind.TERMINALITY),
        provenance_templates=(
            rules.ProvenanceTemplate("mode={0}", (rules.observation(0),)),
        ),
    )
    rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.equal(rules.observation(0), rules.literal_expr(1)),
                _derivation_clause_result(
                    existing=(
                        rules.ExistingDispositionPlan(
                            rules.every_capability(),
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(1),
                        ),
                    ),
                ),
            ),
            rules.RuleClause(rules.literal_expr(1), terminal),
        ),
        contract=_kernel_contract(
            source,
            readable,
            writable,
            value_profile=alphabets.ValueProfile.INTEGER,
        ),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
        selection=rules.ClauseSelection.FIRST,
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    assert len(result.outcome_space.support.atoms) == 1
    atom = result.outcome_space.support.atoms[0]
    assert isinstance(atom, rules.NoSuccessor)
    assert atom.outcome is rules.NoSuccessorOutcome.TERMINAL
    assert atom.reason.arguments == ("inactive",)
    assert "mode=0" in atom.provenance
    assert atom.witness.descriptor.arguments[4].arguments == (0,)


def test_clause_kernel_materializes_delete_create_and_total_defaults() -> None:
    source = loci.record_configuration((("keep", True), ("parent", False)))
    parent = source.entries[1][0]
    reference = loci.fresh_reference(
        "children",
        "child",
        parent=parent,
    )
    existing = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
        effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
    )
    fresh = frontiers.fresh(
        loci.literal(fresh=(reference,)),
        namespace=frontiers.FreshNamespace("children", parent),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    writable = frontiers.union((existing, fresh))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(1),
                _derivation_clause_result(
                    existing=(
                        rules.ExistingDispositionPlan(
                            rules.capability_target(parent),
                            rules.DispositionAction.DELETE,
                        ),
                    ),
                    fresh=(
                        rules.FreshDispositionPlan(
                            rules.capability_target(reference),
                            rules.DispositionAction.CREATE,
                            rules.literal_expr(True),
                        ),
                    ),
                ),
            ),
        ),
        contract=_kernel_contract(
            source,
            readable,
            writable,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    atom = result.outcome_space.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    assert tuple(
        disposition.action for disposition in atom.replacement.existing
    ) == (
        rules.DispositionAction.PRESERVE,
        rules.DispositionAction.DELETE,
    )
    assert atom.replacement.fresh[0].action is rules.DispositionAction.CREATE
    assert isinstance(atom.replacement.fresh[0].payload, rules.ValuePayload)
    assert atom.replacement.fresh[0].payload.value is True


def test_clause_kernel_exact_fraction_arithmetic_and_lazy_conditional() -> None:
    source = loci.record_configuration((("value", Fraction(1, 2)),))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.RATIONAL,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.RATIONAL,
    )
    expression = rules.conditional(
        rules.less_than(
            rules.subtract(
                rules.observation(0),
                rules.literal_expr(Fraction(1, 4)),
            ),
            rules.literal_expr(Fraction(1, 2)),
        ),
        rules.divide(
            rules.add(
                rules.observation(0),
                rules.literal_expr(Fraction(1, 4)),
            ),
            rules.literal_expr(1),
        ),
        rules.divide(rules.literal_expr(1), rules.literal_expr(0)),
    )
    rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(1),
                _derivation_clause_result(
                    existing=(
                        rules.ExistingDispositionPlan(
                            rules.capability_index(0),
                            rules.DispositionAction.REPLACE,
                            expression,
                        ),
                    ),
                ),
            ),
        ),
        contract=_kernel_contract(
            source,
            readable,
            writable,
            value_profile=alphabets.ValueProfile.RATIONAL,
        ),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    atom = result.outcome_space.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    payload = atom.replacement.existing[0].payload
    assert isinstance(payload, rules.ValuePayload)
    assert payload.value == Fraction(3, 4)


def test_clause_kernel_can_emit_the_current_target_as_structural_data() -> None:
    source = loci.record_configuration(
        (
            (
                "value",
                alphabets.ValueNode(
                    alphabets.ValueKind.SYMBOLIC,
                    "placeholder",
                ),
            ),
        )
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    existing = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    existing_target = source.entries[0][0]
    fresh_target = loci.fresh_reference(
        "nodes",
        "new",
        parent=existing_target,
    )
    fresh = frontiers.fresh(
        loci.literal(fresh=(fresh_target,)),
        namespace=frontiers.FreshNamespace("nodes", existing_target),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    )
    writable = frontiers.union((existing, fresh))
    rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(1),
                _derivation_clause_result(
                    existing=(
                        rules.ExistingDispositionPlan(
                            rules.capability_index(0),
                            rules.DispositionAction.REPLACE,
                            rules.target_reference(),
                        ),
                    ),
                    fresh=(
                        rules.FreshDispositionPlan(
                            rules.capability_target(fresh_target),
                            rules.DispositionAction.CREATE,
                            rules.target_reference(),
                        ),
                    ),
                ),
            ),
        ),
        contract=_kernel_contract(
            source,
            readable,
            writable,
            value_profile=alphabets.ValueProfile.STRUCTURAL,
        ),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    result = rule.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(result, rules.RuleComplete)
    atom = result.outcome_space.support.atoms[0]
    assert isinstance(atom, rules.Derivation)
    payload = atom.replacement.existing[0].payload
    assert isinstance(payload, rules.ValuePayload)
    assert payload.value == alphabets.StructuralReference(existing_target)
    fresh_payload = atom.replacement.fresh[0].payload
    assert isinstance(fresh_payload, rules.ValuePayload)
    assert fresh_payload.value == alphabets.StructuralReference(fresh_target)


def test_clause_kernel_fails_closed_for_no_match_and_bad_probability_mass() -> None:
    source = loci.record_configuration((("value", 0),))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    contract = _kernel_contract(
        source,
        readable,
        writable,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    no_match = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(0),
                _derivation_clause_result(),
            ),
        ),
        contract=contract,
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    absent = no_match.denote(readable.resolve(source), writable.resolve(source))

    assert isinstance(absent, rules.RuleRejected)
    assert absent.fault.reason is rules.RuleFaultReason.NO_MATCHING_CLAUSE

    weighted_contract = rules.RuleContract(
        source.contract,
        alphabets.ValueProfile.INTEGER,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
        entropy_interface=seeds.EntropyInterface.REPLAY_KEY,
    )
    bad_mass = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(1),
                _derivation_clause_result(
                    witness=rules.literal_expr("one")
                ),
                Fraction(1, 3),
            ),
            rules.RuleClause(
                rules.literal_expr(1),
                _derivation_clause_result(
                    witness=rules.literal_expr("two")
                ),
                Fraction(1, 3),
            ),
        ),
        contract=weighted_contract,
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
    )

    invalid = bad_mass.denote(
        readable.resolve(source),
        writable.resolve(source),
    )

    assert isinstance(invalid, rules.RuleRejected)
    assert (
        invalid.fault.reason
        is rules.RuleFaultReason.INVALID_PROBABILITY_LAW
    )


def test_clause_kernel_records_and_contracts_reject_ambiguous_shapes() -> None:
    index = rules.capability_index(0)
    with pytest.raises(ValueError, match="non-negative"):
        rules.capability_index(-1)
    with pytest.raises(TypeError, match="Locus or FreshReference"):
        rules.capability_target("cell")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="cannot carry"):
        rules.ExistingDispositionPlan(
            index,
            rules.DispositionAction.PRESERVE,
            rules.literal_expr(1),
        )
    with pytest.raises(ValueError, match="fresh-only"):
        rules.ExistingDispositionPlan(
            index,
            rules.DispositionAction.CREATE,
            rules.literal_expr(1),
        )
    with pytest.raises(ValueError, match="existing-only"):
        rules.FreshDispositionPlan(
            index,
            rules.DispositionAction.DELETE,
        )
    with pytest.raises(ValueError, match="duplicate"):
        _derivation_clause_result(
            existing=(
                rules.ExistingDispositionPlan(
                    index,
                    rules.DispositionAction.PRESERVE,
                ),
                rules.ExistingDispositionPlan(
                    index,
                    rules.DispositionAction.DELETE,
                ),
            ),
        )
    with pytest.raises(ValueError, match="every selector"):
        _derivation_clause_result(
            existing=(
                rules.ExistingDispositionPlan(
                    rules.every_capability(),
                    rules.DispositionAction.PRESERVE,
                ),
                rules.ExistingDispositionPlan(
                    rules.capability_index(0),
                    rules.DispositionAction.PRESERVE,
                ),
            ),
        )
    with pytest.raises(ValueError, match="at least one clause"):
        rules.ClauseKernelDenotation(
            (),
            rules.ClauseSelection.ALL,
            _certificate(rules.CertificateKind.COMPLETENESS),
        )
    with pytest.raises(ValueError, match="masses"):
        rules.ClauseKernelDenotation(
            (
                rules.RuleClause(
                    rules.literal_expr(1),
                    _derivation_clause_result(),
                    Fraction(1, 2),
                ),
                rules.RuleClause(
                    rules.literal_expr(1),
                    _derivation_clause_result(),
                ),
            ),
            rules.ClauseSelection.ALL,
            _certificate(rules.CertificateKind.COMPLETENESS),
        )


def test_clause_kernel_constructor_rejects_undeclared_effects_and_entropy() -> None:
    source = loci.record_configuration((("value", 0),))
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    )
    replacing_clause = rules.RuleClause(
        rules.literal_expr(1),
        _derivation_clause_result(
            existing=(
                rules.ExistingDispositionPlan(
                    rules.capability_index(0),
                    rules.DispositionAction.REPLACE,
                    rules.literal_expr(1),
                ),
            ),
        ),
    )
    no_effect_contract = rules.RuleContract(
        source.contract,
        alphabets.ValueProfile.INTEGER,
        readable.result_shape,
        readable.join_shape,
        frontiers.EffectProfile(existing=()),
    )

    with pytest.raises(ValueError, match="omits required existing effects"):
        rules.clause_kernel(
            (replacing_clause,),
            contract=no_effect_contract,
            completeness_evidence=_certificate(
                rules.CertificateKind.COMPLETENESS
            ),
        )

    deterministic_contract = rules.RuleContract(
        source.contract,
        alphabets.ValueProfile.INTEGER,
        readable.result_shape,
        readable.join_shape,
        frontiers.EffectProfile(),
    )
    with pytest.raises(ValueError, match="replay-key entropy"):
        rules.clause_kernel(
            (
                rules.RuleClause(
                    replacing_clause.condition,
                    replacing_clause.result,
                    Fraction(1),
                ),
            ),
            contract=deterministic_contract,
            completeness_evidence=_certificate(
                rules.CertificateKind.COMPLETENESS
            ),
        )


def test_intensional_projection_cardinalities_are_explicit_and_evidenced() -> None:
    claims = rules.ProjectionCardinalities(
        rules.finite_cardinality(1),
        rules.finite_cardinality(0),
        rules.finite_cardinality(1),
        _certificate(rules.CertificateKind.COMPOSITION),
    )
    support = rules.intensional_support(
        rules.literal_expr("closed-relation"),
        rules.finite_cardinality(1),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
        soundness_evidence=_certificate(rules.CertificateKind.SOUNDNESS),
    )
    outcome = rules.OutcomeSpace(
        support,
        projection_cardinalities=claims,
    )

    assert outcome.projection_cardinalities is claims
    with pytest.raises(ValueError, match="composition"):
        rules.ProjectionCardinalities(
            rules.finite_cardinality(1),
            rules.finite_cardinality(0),
            rules.finite_cardinality(1),
            _certificate(rules.CertificateKind.CARDINALITY),
        )
    with pytest.raises(ValueError, match="finite supports"):
        rules.OutcomeSpace(
            rules.finite_support((rules.literal_expr("atom"),)),
            projection_cardinalities=claims,
        )


def test_intensional_projection_cardinalities_obey_partition_and_quotient_laws() -> None:
    source = rules.intensional_support(
        rules.literal_expr("one-source-atom"),
        rules.finite_cardinality(1),
        completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
        soundness_evidence=_certificate(rules.CertificateKind.SOUNDNESS),
    )
    composition = _certificate(rules.CertificateKind.COMPOSITION)

    with pytest.raises(ValueError, match="do not partition"):
        rules.OutcomeSpace(
            source,
            projection_cardinalities=rules.ProjectionCardinalities(
                rules.finite_cardinality(1),
                rules.finite_cardinality(1),
                rules.finite_cardinality(1),
                composition,
            ),
        )
    with pytest.raises(ValueError, match="successor cardinality"):
        rules.OutcomeSpace(
            source,
            projection_cardinalities=rules.ProjectionCardinalities(
                rules.finite_cardinality(1),
                rules.finite_cardinality(0),
                rules.finite_cardinality(2),
                composition,
            ),
        )
    with pytest.raises(ValueError, match="zero distinct successors"):
        rules.OutcomeSpace(
            source,
            projection_cardinalities=rules.ProjectionCardinalities(
                rules.finite_cardinality(0),
                rules.finite_cardinality(1),
                rules.finite_cardinality(1),
                composition,
            ),
        )
    undetermined = rules.Undetermined(
        rules.literal_expr("unproved"),
        _certificate(rules.CertificateKind.CARDINALITY),
    )
    unknown_projection = rules.ProjectionCardinalities(
        undetermined,
        rules.finite_cardinality(0),
        undetermined,
        composition,
    )
    outcome = rules.OutcomeSpace(
        source,
        projection_cardinalities=unknown_projection,
    )
    assert outcome.projection_cardinalities is unknown_projection


def test_intensional_projection_cardinalities_reject_impossible_infinite_claims() -> None:
    cardinality = _certificate(rules.CertificateKind.CARDINALITY)
    composition = _certificate(rules.CertificateKind.COMPOSITION)
    zero = rules.finite_cardinality(0)
    one = rules.finite_cardinality(1)
    countable = rules.Many(
        None,
        rules.InfiniteCardinality.COUNTABLY_INFINITE,
        cardinality,
    )
    uncountable = rules.Many(
        None,
        rules.InfiniteCardinality.UNCOUNTABLE,
        cardinality,
    )

    def outcome(
        source_cardinality: rules.Cardinality,
        derivations: rules.Cardinality,
        no_successors: rules.Cardinality,
        successors: rules.Cardinality,
    ) -> rules.OutcomeSpace:
        source = rules.intensional_support(
            rules.literal_expr("infinite-source"),
            source_cardinality,
            completeness_evidence=_certificate(rules.CertificateKind.COMPLETENESS),
            soundness_evidence=_certificate(rules.CertificateKind.SOUNDNESS),
        )
        return rules.OutcomeSpace(
            source,
            projection_cardinalities=rules.ProjectionCardinalities(
                derivations,
                no_successors,
                successors,
                composition,
            ),
        )

    with pytest.raises(ValueError, match="do not partition"):
        outcome(countable, uncountable, zero, uncountable)
    with pytest.raises(ValueError, match="cannot exceed countably"):
        outcome(countable, countable, zero, uncountable)
    with pytest.raises(ValueError, match="do not partition"):
        outcome(uncountable, countable, zero, countable)
    with pytest.raises(ValueError, match="do not partition"):
        outcome(uncountable, one, countable, one)

    assert outcome(countable, countable, zero, one).projection_cardinalities
    assert outcome(uncountable, uncountable, zero, countable).projection_cardinalities


@pytest.mark.parametrize(
    "factory",
    (
        lambda: rules.ar2_modular_0d(rule=17),
        lambda: rules.dyadlags_0d(rule=150),
        lambda: rules.lagcounts_0d(rule=91),
        lambda: rules.dyadrads_1d(rule=30),
        lambda: rules.dyadaxes_2d(rule=128),
        lambda: rules.dyadaxes_3d(rule=128),
    ),
)
def test_retained_native_rules_store_concrete_construction_data(factory) -> None:
    rule = factory()

    assert isinstance(rule, rules.Rule)
    assert rule.descriptor.primitive is rules.RulePrimitive.EXPRESSION
    assert not hasattr(rule, "family")
    assert not hasattr(rule, "params")


def test_elementary_constructor_is_an_ordinary_closed_rule() -> None:
    rule = rules.elementary(30)

    assert isinstance(rule, rules.Rule)
    assert rule.descriptor.primitive is rules.RulePrimitive.EXPRESSION
    assert rule.contract.required_read_shape == neighborhoods.eca().result_shape
    with pytest.raises(ValueError):
        rules.elementary(256)
