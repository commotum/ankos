"""Unit tests for closed Rule denotations and results."""

from dataclasses import dataclass
from fractions import Fraction

import pytest

from ca import alphabets, frontiers, loci, neighborhoods, rules


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
