"""CT10: inverse-on-image and complete one-step representation commutation."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction

import pytest

import ca
from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
    serialization,
)

from g7_fixtures import (
    certificate,
    derivation,
    finite_record_program,
    no_successor,
    rule_contract,
)
from g7_mechanics import (
    MECHANICS_ROWS,
    assert_mechanics_run,
    materialized_px10_source,
    materialized_px10_target,
    run_mechanics_fixture,
    run_px10_representation_case,
)


PX10_ROWS = tuple(row for row in MECHANICS_ROWS if row.primary == "PX10")


def _oracle_word(
    tag: str,
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.WORD, tag, items=items)


def _oracle_record(
    tag: str,
    **values: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(
        alphabets.ValueKind.RECORD,
        tag,
        fields=tuple(values.items()),
    )


def _oracle_product(
    tag: str,
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.ValueNode(alphabets.ValueKind.PRODUCT, tag, items=items)


PX10_ORACLE_PAIRS = {
    "SPF012": (
        (
            _oracle_word("source-word", "A", "A", "A", "B", "B"),
            _oracle_record("run-records", run0="A:3", run1="B:2"),
        ),
        (
            _oracle_word("source-word", "B"),
            _oracle_record("run-records", run0="B:1"),
        ),
    ),
    "SPF054": (
        (
            _oracle_word("prefix-block", "A"),
            _oracle_word("prefix-bits", 0),
        ),
        (
            _oracle_word("prefix-block", "B"),
            _oracle_word("prefix-bits", 1, 0),
        ),
    ),
    "SPF055": (
        (
            _oracle_word("message", "A", "B"),
            _oracle_record(
                "nested-interval",
                low=Fraction(1, 4),
                high=Fraction(1, 2),
            ),
        ),
        (
            _oracle_word("message", "A", "A"),
            _oracle_record(
                "nested-interval",
                low=Fraction(0),
                high=Fraction(1, 4),
            ),
        ),
    ),
    "SPF056": (
        (
            _oracle_word("history-input", "A", "B", "A", "B"),
            _oracle_word(
                "history-records",
                "literal:A",
                "literal:B",
                "ref:offset=2,length=2",
            ),
        ),
        (
            _oracle_word("history-input", "A", "B", "C"),
            _oracle_word(
                "history-records",
                "literal:A",
                "literal:B",
                "literal:C",
            ),
        ),
    ),
    "SPF057": (
        (
            _oracle_product("uniform-grid", 1, 1, 1, 1),
            _oracle_record("region-leaf", bounds="2x2", value=1),
        ),
        (
            _oracle_product("nonuniform-grid", 1, 0, 0, 1),
            _oracle_record("region-branch", children=4, bounds="2x2"),
        ),
    ),
    "SPF058": (
        (
            _oracle_word("vector", 1, 1),
            _oracle_word("walsh-coefficients", 1, 0),
        ),
        (
            _oracle_word("vector", 1, -1),
            _oracle_word("walsh-coefficients", 0, 1),
        ),
    ),
    "SPF059": (
        (
            _oracle_word("samples", 1, 2, 3),
            _oracle_word("residuals", 1, 1, 1),
        ),
        (
            _oracle_word("samples", 2, 4, 6),
            _oracle_word("residuals", 2, 2, 2),
        ),
    ),
    "SPF060": (
        (
            _oracle_product(
                "xor-operands",
                _oracle_word("data", 1, 0, 1),
                _oracle_word("generator", 0, 1, 1),
            ),
            _oracle_word("xor-output", 1, 1, 0),
        ),
        (
            _oracle_product(
                "xor-operands",
                _oracle_word("data", 1, 1, 0),
                _oracle_word("generator", 0, 1, 1),
            ),
            _oracle_word("xor-output", 1, 0, 1),
        ),
    ),
}


def _assert_exact_relation_matches_oracle(
    relation: alphabets.RepresentationRelation,
    oracle_pairs: tuple[
        tuple[alphabets.SemanticValue, alphabets.SemanticValue],
        tuple[alphabets.SemanticValue, alphabets.SemanticValue],
    ],
) -> None:
    """Require the complete declared graph, image, and inverse literally."""

    assert relation.profile is alphabets.RepresentationProfile.EXACT
    assert relation.source_schema == alphabets.enum(
        tuple(source for source, _ in oracle_pairs)
    ).descriptor
    assert relation.target_schema == alphabets.enum(
        tuple(target for _, target in oracle_pairs)
    ).descriptor
    assert len(relation.relation) == len(oracle_pairs) == 2
    assert len(relation.inverse_evidence) == len(oracle_pairs)
    assert len(relation.image_evidence) == len(oracle_pairs)
    for source, target in oracle_pairs:
        assert alphabets.semantic_equal(relation.forward(source), target)
        assert alphabets.semantic_equal(relation.inverse(target), source)
        assert any(
            alphabets.semantic_equal(pair.source, source)
            and alphabets.semantic_equal(pair.target, target)
            for pair in relation.relation
        )
        assert any(
            alphabets.semantic_equal(pair.source, target)
            and alphabets.semantic_equal(pair.target, source)
            for pair in relation.inverse_evidence
        )
        assert any(
            alphabets.semantic_equal(image_value, target)
            for image_value in relation.image_evidence
        )


def _exact_relation(row) -> alphabets.RepresentationRelation:
    execution = run_mechanics_fixture(row)
    assert_mechanics_run(execution)
    relation = execution.representation

    assert relation is not None
    _assert_exact_relation_matches_oracle(
        relation,
        PX10_ORACLE_PAIRS[row.spf],
    )
    return relation


def _transition_system(
    relation_pairs: tuple[
        tuple[alphabets.SemanticValue, alphabets.SemanticValue],
        tuple[alphabets.SemanticValue, alphabets.SemanticValue],
    ],
    *,
    identity: str,
) -> tuple[
    ca.SimpleProgram,
    tuple[loci.FiniteConfiguration, loci.FiniteConfiguration],
    ca.SimpleProgram,
    tuple[loci.FiniteConfiguration, loci.FiniteConfiguration],
]:
    """Build one fixed conjugate program per side from a literal oracle.

    The PX10 family fixture itself is a transducer that establishes the
    relation; it is not one side of a native/represented state pair.  This
    separate pair of two-clause programs tests the representation claim as a
    state conjugacy without pretending the transducer and represented
    dynamics are the same role, deriving expectations from the relation under
    test, or rebuilding either program for a different domain point.
    """

    stopped = rules.Stop(
        rules.literal_expr(f"{identity}:complete"),
        certificate(
            rules.CertificateKind.TERMINALITY,
            f"{identity}:complete",
        ),
    )

    def build(
        values: tuple[alphabets.SemanticValue, ...],
    ) -> tuple[
        ca.SimpleProgram,
        tuple[loci.FiniteConfiguration, loci.FiniteConfiguration],
    ]:
        sources = tuple(
            loci.record_configuration((("value", value),))
            for value in values
        )
        first_source = sources[0]
        target = first_source.entries[0][0]
        assert all(source.entries[0][0] == target for source in sources)
        alphabet = alphabets.enum(values)
        writable = frontiers.everywhere(
            configuration_contract=first_source.contract,
            value_profile=alphabet.value_profile,
            effects=(frontiers.Effect.REPLACE,),
        )
        readable = neighborhoods.global_view(
            configuration_contract=first_source.contract,
            value_profile=alphabet.value_profile,
        )
        clauses = tuple(
            rules.RuleClause(
                rules.equal(
                    rules.observation(0),
                    rules.literal_expr(current),
                ),
                rules.DerivationClauseResult(
                    (
                        rules.ExistingDispositionPlan(
                            rules.capability_target(target),
                            rules.DispositionAction.REPLACE,
                            rules.literal_expr(values[1 - index]),
                        ),
                    ),
                    (),
                    rules.Progress.ADVANCED,
                    stopped,
                    rules.literal_expr(f"{identity}:case-{index}"),
                    (f"test:{identity}:case-{index}",),
                    certificate(
                        rules.CertificateKind.DERIVATION,
                        f"{identity}:case-{index}:derived",
                    ),
                ),
            )
            for index, current in enumerate(values)
        )
        rule = rules.clause_kernel(
            clauses,
            contract=rule_contract(
                first_source,
                alphabet,
                writable,
                readable,
            ),
            completeness_evidence=certificate(
                rules.CertificateKind.COMPLETENESS,
                f"{identity}:complete-domain",
            ),
            selection=rules.ClauseSelection.FIRST,
        )
        return (
            ca.SimpleProgram(
                seeds.exact(
                    first_source,
                    value_profile=alphabet.value_profile,
                ),
                alphabet,
                writable,
                readable,
                rule,
            ),
            sources,
        )

    native_program, native_sources = build(
        tuple(pair[0] for pair in relation_pairs)
    )
    represented_program, represented_sources = build(
        tuple(pair[1] for pair in relation_pairs)
    )
    return (
        native_program,
        native_sources,
        represented_program,
        represented_sources,
    )


def _stochastic_pair() -> tuple[
    alphabets.RepresentationRelation,
    program.ApplicationComplete,
    program.ApplicationComplete,
]:
    """Exercise laws, no-successors, submeasures, and a two-witness fiber."""

    encoded_false = alphabets.ValueNode(
        alphabets.ValueKind.TAG,
        "encoded-bit",
        items=(0,),
    )
    encoded_true = alphabets.ValueNode(
        alphabets.ValueKind.TAG,
        "encoded-bit",
        items=(1,),
    )
    source_schema = alphabets.enum((False, True)).descriptor
    target_schema = alphabets.enum((encoded_false, encoded_true)).descriptor
    relation = alphabets.RepresentationRelation(
        source_schema,
        target_schema,
        alphabets.RepresentationProfile.EXACT,
        (
            alphabets.RepresentationPair(False, encoded_false),
            alphabets.RepresentationPair(True, encoded_true),
        ),
        (encoded_false, encoded_true),
        inverse_evidence=(
            alphabets.RepresentationPair(encoded_false, False),
            alphabets.RepresentationPair(encoded_true, True),
        ),
    )

    def build(
        initial: alphabets.SemanticValue,
        following: alphabets.SemanticValue,
        alphabet: alphabets.Alphabet,
    ) -> tuple[ca.SimpleProgram, loci.FiniteConfiguration]:
        def atoms(targets: tuple[loci.Locus, ...]):
            replacement = (rules.replace(targets[0], following),)
            return (
                derivation("left-witness", existing=replacement),
                derivation("right-witness", existing=replacement),
                no_successor(
                    "rejected-witness",
                    rules.NoSuccessorOutcome.UNDEFINED,
                ),
            )

        return finite_record_program(
            (("value", initial),),
            atoms,
            alphabet=alphabet,
            effects=(ca.frontiers.Effect.REPLACE,),
            probability=(
                Fraction(1, 4),
                Fraction(1, 4),
                Fraction(1, 2),
            ),
        )

    native_program, native_source = build(
        False,
        True,
        alphabets.enum((False, True)),
    )
    represented_program, represented_source = build(
        encoded_false,
        encoded_true,
        alphabets.enum((encoded_false, encoded_true)),
    )
    native = ca.apply(native_program, native_source)
    represented = ca.apply(represented_program, represented_source)
    assert isinstance(native, program.ApplicationComplete)
    assert isinstance(represented, program.ApplicationComplete)
    return relation, native, represented


def _clause_read_evidence_identities(
    witness: rules.Witness,
) -> tuple[str, ...]:
    """Extract only runtime read IDs from a clause-kernel witness proof."""

    descriptor = witness.descriptor
    if (
        descriptor.primitive is not rules.ExpressionPrimitive.TUPLE
        or len(descriptor.arguments) < 5
        or type(descriptor.arguments[0]) is not rules.RuleExpr
        or descriptor.arguments[0].primitive
        is not rules.ExpressionPrimitive.LITERAL
        or descriptor.arguments[0].arguments
        != ("clause-kernel-witness-v1",)
        or type(descriptor.arguments[4]) is not rules.RuleExpr
    ):
        return ()

    evidence: list[str] = []

    def visit(expression: rules.RuleExpr) -> None:
        if (
            expression.primitive is rules.ExpressionPrimitive.TUPLE
            and expression.arguments
            and type(expression.arguments[0]) is rules.RuleExpr
            and expression.arguments[0].primitive
            is rules.ExpressionPrimitive.LITERAL
            and expression.arguments[0].arguments == ("read-evidence",)
        ):
            for item in expression.arguments[1:]:
                assert type(item) is rules.RuleExpr
                assert (
                    item.primitive
                    is rules.ExpressionPrimitive.LITERAL
                )
                assert (
                    len(item.arguments) == 1
                    and type(item.arguments[0]) is str
                )
                evidence.append(item.arguments[0])
            return
        for item in expression.arguments:
            if type(item) is rules.RuleExpr:
                visit(item)

    visit(descriptor.arguments[4])
    return tuple(evidence)


def _identity_aliases(
    result: program.ApplicationComplete,
) -> dict[str, str]:
    aliases = {
        result.evidence.program_identity: "@program",
        result.evidence.input_configuration_identity: "@input",
        result.evidence.readable_binding_identity: "@readable",
        result.evidence.writable_binding_identity: "@writable",
        result.evidence.application_identity: "@application",
        result.evidence.canonical_rule_identity: "@rule",
        result.evidence.input_trace_lineage_identity: "@input-lineage",
    }
    for atom in result.source_outcomes.support.atoms:
        source_label = ":".join(
            (type(atom).__name__, *atom.provenance)
        )
        aliases[atom.canonical_identity] = f"@source:{source_label}"
        for index, identity in enumerate(
            dict.fromkeys(_clause_read_evidence_identities(atom.witness))
        ):
            aliases[identity] = (
                f"@read-evidence:{source_label}:{index}"
            )
    for atom in result.applied_atoms.atoms:
        source_alias = aliases[atom.source.canonical_identity]
        aliases[atom.canonical_identity] = f"@applied:{source_alias}"
        aliases[atom.evidence.application_identity] = "@application"
        aliases[atom.evidence.disposition_identity] = (
            f"@disposition:{source_alias}"
        )
        if isinstance(atom, program.AppliedDerivation):
            for index, binding in enumerate(atom.fresh_bindings):
                aliases[loci.canonical_identity(binding.identity)] = (
                    f"@fresh:{source_alias}:{index}"
                )
        if isinstance(atom, program.AppliedDerivation):
            aliases[loci.configuration_identity(atom.successor)] = "@successor"
    return aliases


_IDENTITY_FIELDS = frozenset(
    {
        (rules.AtomMass, "atom_identity"),
        (rules.Witness, "identity"),
        (rules.Witness, "descriptor"),
        (program.FreshBinding, "identity"),
        (program.AppliedEvidence, "application_identity"),
        (program.AppliedEvidence, "disposition_identity"),
        (program.MeasureMass, "point_identity"),
        (program.ApplicationEvidence, "program_identity"),
        (program.ApplicationEvidence, "input_configuration_identity"),
        (program.ApplicationEvidence, "readable_binding_identity"),
        (program.ApplicationEvidence, "writable_binding_identity"),
        (program.ApplicationEvidence, "application_identity"),
        (program.ApplicationEvidence, "canonical_rule_identity"),
        (program.ApplicationEvidence, "input_trace_lineage_identity"),
    }
)


def _normalize_complete_result(
    result: program.ApplicationComplete,
    *,
    decode_relation: alphabets.RepresentationRelation | None = None,
) -> tuple[object, ...]:
    """Normalize every stored field, changing only declared values and IDs."""

    aliases = _identity_aliases(result)
    output_lineages = {
        (
            atom.output_trace_lineage.root_identity,
            atom.output_trace_lineage.path,
        ): (
            atom.input_trace_lineage.path,
            aliases[atom.source.canonical_identity],
        )
        for atom in result.applied_atoms.atoms
    }
    default_lineage_root = loci.canonical_identity(
        (
            "direct-application-root",
            result.evidence.input_configuration_identity,
        )
    )

    def normalize(
        value: object,
        *,
        identity_bearing: bool = False,
    ) -> object:
        if (
            decode_relation is not None
            and isinstance(value, alphabets.ValueNode)
        ):
            for pair in decode_relation.relation:
                if alphabets.semantic_equal(value, pair.target):
                    return normalize(pair.source)
        if type(value) is loci.Locus and value.kind is loci.LocusKind.FRESH:
            identity = loci.canonical_identity(value)
            if identity in aliases:
                return ("bound-fresh-locus", aliases[identity])
        if type(value) is program.TraceLineage:
            root = value.root_identity
            if root == default_lineage_root:
                root = "@default-lineage-root"
            path: tuple[str, ...] = value.path
            output = output_lineages.get(
                (value.root_identity, value.path)
            )
            if output is not None:
                input_path, witness = output
                assert path[:-1] == input_path
                path = (*input_path, f"@output-edge:{witness}")
            return (
                "record",
                value.__class__.__module__,
                value.__class__.__name__,
                (
                    ("root_identity", root),
                    ("path", path),
                    ("version", value.version),
                ),
            )
        if value is None or type(value) in (bool, int):
            return value
        if type(value) is Fraction:
            return ("fraction", value.numerator, value.denominator)
        if type(value) is str:
            if identity_bearing and value in aliases:
                return aliases[value]
            return value
        if isinstance(value, Enum):
            return (
                "enum",
                value.__class__.__module__,
                value.__class__.__name__,
                value.value,
            )
        if type(value) is tuple:
            return tuple(
                normalize(item, identity_bearing=identity_bearing)
                for item in value
            )
        if not is_dataclass(value):
            raise AssertionError(
                f"unhandled complete-result value {type(value).__name__}"
            )
        normalized_fields: list[tuple[str, object]] = []
        for field in fields(value):
            field_value = normalize(
                getattr(value, field.name),
                identity_bearing=identity_bearing
                or (type(value), field.name) in _IDENTITY_FIELDS,
            )
            if (
                type(value) is rules.SupportSpace
                and field.name == "atoms"
            ) or (
                type(value) is rules.ProbabilityLaw
                and field.name == "masses"
            ) or (
                type(value) is program.ProgramMeasure
                and field.name == "masses"
            ) or (
                type(value) is program.SuccessorGroup
                and field.name == "derivations"
            ):
                assert type(field_value) is tuple
                field_value = tuple(sorted(field_value, key=repr))
            normalized_fields.append((field.name, field_value))
        return (
            "record",
            value.__class__.__module__,
            value.__class__.__name__,
            tuple(normalized_fields),
        )

    normalized = normalize(result)
    assert type(normalized) is tuple
    return normalized


def test_exact_representation_is_inverse_on_its_declared_image() -> None:
    """Every exact PX10 relation agrees with an independent literal oracle."""

    assert len(PX10_ROWS) == 8
    for row in PX10_ROWS:
        relation = _exact_relation(row)
        for source, target in PX10_ORACLE_PAIRS[row.spf]:
            assert relation.forward(source) == target
            assert relation.inverse(target) == source
        with pytest.raises(ValueError, match="outside"):
            relation.inverse(
                alphabets.ValueNode(
                    alphabets.ValueKind.SYMBOLIC,
                    "outside-image",
                )
            )


@pytest.mark.parametrize(
    "mutated_target",
    (
        _oracle_word("wrong-xor-tag", 1, 1, 0),
        _oracle_word("xor-output", 0, 1, 1),
    ),
    ids=("wrong-tag", "wrong-order"),
)
def test_spf060_oracle_rejects_payload_only_relation_mutations(
    mutated_target: alphabets.ValueNode,
) -> None:
    """Equal-looking bits cannot hide a wrong structural tag or bit order."""

    oracle_pairs = PX10_ORACLE_PAIRS["SPF060"]
    corrupted_pairs = (
        (oracle_pairs[0][0], mutated_target),
        oracle_pairs[1],
    )
    corrupted = alphabets.RepresentationRelation(
        alphabets.enum(
            tuple(source for source, _ in corrupted_pairs)
        ).descriptor,
        alphabets.enum(
            tuple(target for _, target in corrupted_pairs)
        ).descriptor,
        alphabets.RepresentationProfile.EXACT,
        tuple(
            alphabets.RepresentationPair(source, target)
            for source, target in corrupted_pairs
        ),
        tuple(target for _, target in corrupted_pairs),
        inverse_evidence=tuple(
            alphabets.RepresentationPair(target, source)
            for source, target in corrupted_pairs
        ),
    )

    with pytest.raises(AssertionError):
        _assert_exact_relation_matches_oracle(corrupted, oracle_pairs)


def _terminal_px10_result(
    execution,
) -> program.ApplicationComplete:
    """Select the terminal application without assuming the first step stops."""

    if execution.trajectory:
        _, terminal_result = execution.trajectory[-1]
    else:
        terminal_result = execution.result
    assert isinstance(terminal_result, program.ApplicationComplete)
    return terminal_result


@pytest.mark.parametrize("row", PX10_ROWS, ids=lambda row: row.spf)
def test_represented_and_native_one_step_results_commute_completely(
    row,
) -> None:
    """Both domain points use one transducer and one fixed conjugate pair."""

    executions = tuple(
        run_px10_representation_case(row, case_index)
        for case_index in (0, 1)
    )
    primary, alternate = executions
    assert (
        primary.simple_program.canonical_identity
        == alternate.simple_program.canonical_identity
    )
    assert primary.simple_program == alternate.simple_program
    assert primary.representation == alternate.representation

    relation = primary.representation
    assert relation is not None
    oracle_pairs = PX10_ORACLE_PAIRS[row.spf]
    _assert_exact_relation_matches_oracle(relation, oracle_pairs)

    (
        native_program,
        native_sources,
        represented_program,
        represented_sources,
    ) = _transition_system(
        oracle_pairs,
        identity=row.fixture,
    )
    native_identity = native_program.canonical_identity
    represented_identity = represented_program.canonical_identity
    for fixed_program in (native_program, represented_program):
        denotation = fixed_program.rule.descriptor.denotation
        assert type(denotation) is rules.ClauseKernelDenotation
        assert len(denotation.clauses) == 2
        assert all(
            clause.condition.primitive is rules.ExpressionPrimitive.EQUAL
            for clause in denotation.clauses
        )
    assert not loci.configuration_equal(native_sources[0], native_sources[1])
    assert not loci.configuration_equal(
        represented_sources[0],
        represented_sources[1],
    )

    for case_index, execution in enumerate(executions):
        assert_mechanics_run(execution)
        assert execution.representation == relation
        assert execution.representation_source is not None
        assert execution.representation_target is not None
        oracle_source, oracle_target = oracle_pairs[case_index]
        assert alphabets.semantic_equal(
            execution.representation_source,
            oracle_source,
        )
        assert alphabets.semantic_equal(
            execution.representation_target,
            oracle_target,
        )
        actual_source = materialized_px10_source(execution)
        assert alphabets.semantic_equal(actual_source, oracle_source)
        assert alphabets.semantic_equal(
            relation.forward(oracle_source),
            oracle_target,
        )
        actual_target = materialized_px10_target(execution)
        assert alphabets.semantic_equal(actual_target, oracle_target)
        if row.spf == "SPF060":
            assert type(actual_target) is alphabets.ValueNode
            assert type(oracle_target) is alphabets.ValueNode
            assert actual_target.kind is alphabets.ValueKind.WORD
            assert actual_target.tag == oracle_target.tag == "xor-output"
            assert actual_target.items == oracle_target.items

        terminal_result = _terminal_px10_result(execution)
        terminal_derivations = tuple(
            atom
            for atom in terminal_result.applied_atoms.atoms
            if isinstance(atom, program.AppliedDerivation)
        )
        assert len(terminal_derivations) == 1
        assert isinstance(
            terminal_derivations[0].source.continuation,
            rules.Stop,
        )

        assert native_program.canonical_identity == native_identity
        assert represented_program.canonical_identity == represented_identity
        native = ca.apply(native_program, native_sources[case_index])
        represented = ca.apply(
            represented_program,
            represented_sources[case_index],
        )
        assert isinstance(native, program.ApplicationComplete)
        assert isinstance(represented, program.ApplicationComplete)
        for result in (native, represented):
            atom = result.applied_atoms.atoms[0]
            assert isinstance(atom, program.AppliedDerivation)
            assert isinstance(atom.source.continuation, rules.Stop)
        assert native_program.canonical_identity == native_identity
        assert represented_program.canonical_identity == represented_identity

        assert _normalize_complete_result(
            represented,
            decode_relation=relation,
        ) == _normalize_complete_result(native)


def test_commutation_compares_all_outcomes_evidence_measures_and_fibers() -> None:
    """The mapper covers nontrivial laws, no-successors, fibers, and evidence."""

    relation, native, represented = _stochastic_pair()
    assert len(native.source_outcomes.support.atoms) == 3
    assert len(native.no_successor_partition.atoms) == 1
    assert len(
        native.successor_quotient_with_derivation_fibers.atoms[0].derivations
    ) == 2
    assert isinstance(native.applied_atom_measure, program.MeasureAvailable)
    assert isinstance(native.successor_submeasure, program.MeasureAvailable)
    assert isinstance(native.no_successor_submeasure, program.MeasureAvailable)

    assert _normalize_complete_result(
        represented,
        decode_relation=relation,
    ) == _normalize_complete_result(native)
    for result in (native, represented):
        blob = serialization.dumps(result)
        assert serialization.loads(blob) == serialization.Decoded(result)
        assert serialization.dumps(serialization.loads(blob).value) == blob


def test_commutation_never_erases_hex_shaped_semantic_strings() -> None:
    """Only explicitly identified derived IDs may be normalized."""

    def result(
        initial: str,
        following: str,
    ) -> program.ApplicationComplete:
        def atoms(targets: tuple[loci.Locus, ...]):
            return (
                derivation(
                    "hex-shaped-semantic-value",
                    existing=(rules.replace(targets[0], following),),
                ),
            )

        simple_program, source = finite_record_program(
            (("value", initial),),
            atoms,
            alphabet=alphabets.enum((initial, following)),
            effects=(ca.frontiers.Effect.REPLACE,),
        )
        application = ca.apply(simple_program, source)
        assert isinstance(application, program.ApplicationComplete)
        return application

    left = result("a" * 64, "b" * 64)
    right = result("c" * 64, "d" * 64)

    assert _normalize_complete_result(left) != _normalize_complete_result(right)


def test_commutation_normalizes_ids_only_in_identity_bearing_fields() -> None:
    """A lineage ID equal to a cell value cannot erase that semantic value."""

    def result(value: str) -> program.ApplicationComplete:
        def atoms(targets: tuple[loci.Locus, ...]):
            return (
                derivation(
                    "identity-shaped-semantic-value",
                    existing=(rules.replace(targets[0], value),),
                ),
            )

        simple_program, source = finite_record_program(
            (("value", value),),
            atoms,
            alphabet=alphabets.enum((value,)),
            effects=(ca.frontiers.Effect.REPLACE,),
        )
        application = ca.apply(
            simple_program,
            program.ApplicationInput(
                source,
                program.TraceLineage(value),
            ),
        )
        assert isinstance(application, program.ApplicationComplete)
        return application

    left = result("semantic-left")
    right = result("semantic-right")

    assert _normalize_complete_result(left) != _normalize_complete_result(right)


def test_commutation_retains_caller_supplied_lineage_prefixes() -> None:
    """Only the newly derived lineage edge is representation-relative."""

    def atoms(targets: tuple[loci.Locus, ...]):
        return (
            derivation(
                "retained-lineage",
                existing=(rules.replace(targets[0], True),),
            ),
        )

    simple_program, source = finite_record_program(
        (("value", False),),
        atoms,
    )
    left = ca.apply(
        simple_program,
        program.ApplicationInput(
            source,
            program.TraceLineage("root-left", ("retained-left",)),
        ),
    )
    right = ca.apply(
        simple_program,
        program.ApplicationInput(
            source,
            program.TraceLineage("root-right", ("retained-right",)),
        ),
    )
    assert isinstance(left, program.ApplicationComplete)
    assert isinstance(right, program.ApplicationComplete)
    assert left != right

    assert _normalize_complete_result(left) != _normalize_complete_result(right)


def test_commutation_maps_fresh_bindings_and_bound_structural_loci() -> None:
    """Related fresh writes commute without erasing raw binding evidence."""

    encoded_false = alphabets.ValueNode(
        alphabets.ValueKind.TAG,
        "encoded-fresh-bit",
        items=(0,),
    )
    encoded_true = alphabets.ValueNode(
        alphabets.ValueKind.TAG,
        "encoded-fresh-bit",
        items=(1,),
    )
    relation = alphabets.RepresentationRelation(
        alphabets.boolean().descriptor,
        alphabets.enum((encoded_false, encoded_true)).descriptor,
        alphabets.RepresentationProfile.EXACT,
        (
            alphabets.RepresentationPair(False, encoded_false),
            alphabets.RepresentationPair(True, encoded_true),
        ),
        (encoded_false, encoded_true),
        inverse_evidence=(
            alphabets.RepresentationPair(encoded_false, False),
            alphabets.RepresentationPair(encoded_true, True),
        ),
    )

    def result(
        initial: alphabets.SemanticValue,
        following: alphabets.SemanticValue,
        alphabet: alphabets.Alphabet,
    ) -> program.ApplicationComplete:
        source = loci.record_configuration((("parent", initial),))
        parent = source.entries[0][0]
        reference = loci.fresh_reference(
            "representation-children",
            "child",
            parent=parent,
        )
        writable = ca.frontiers.fresh(
            loci.literal(fresh=(reference,)),
            namespace=ca.frontiers.FreshNamespace(
                "representation-children",
                parent,
            ),
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        readable = ca.neighborhoods.global_view(
            configuration_contract=source.contract,
            value_profile=alphabet.value_profile,
        )
        atom = derivation(
            "fresh-representation",
            existing=(),
            fresh=(rules.create(reference, following),),
        )
        simple_program = ca.SimpleProgram(
            ca.seeds.exact(
                source,
                value_profile=alphabet.value_profile,
            ),
            alphabet,
            writable,
            readable,
            rules.finite_rule(
                (atom,),
                contract=rule_contract(
                    source,
                    alphabet,
                    writable,
                    readable,
                ),
            ),
        )
        application = ca.apply(simple_program, source)
        assert isinstance(application, program.ApplicationComplete)
        return application

    native = result(False, True, alphabets.boolean())
    represented = result(
        encoded_false,
        encoded_true,
        alphabets.enum((encoded_false, encoded_true)),
    )
    native_atom = native.applied_atoms.atoms[0]
    represented_atom = represented.applied_atoms.atoms[0]
    assert isinstance(native_atom, program.AppliedDerivation)
    assert isinstance(represented_atom, program.AppliedDerivation)
    assert len(native_atom.fresh_bindings) == 1
    assert len(represented_atom.fresh_bindings) == 1
    assert (
        native_atom.fresh_bindings[0].identity
        != represented_atom.fresh_bindings[0].identity
    )

    assert _normalize_complete_result(
        represented,
        decode_relation=relation,
    ) == _normalize_complete_result(native)


def test_lossy_approximate_or_out_of_image_translation_remains_explicit() -> None:
    """Qualified realizations never masquerade as exact aliases."""

    source = alphabets.enum((0, 1)).descriptor
    target = alphabets.enum((0,)).descriptor
    pairs = (
        alphabets.RepresentationPair(0, 0),
        alphabets.RepresentationPair(1, 0),
    )
    lossy = alphabets.RepresentationRelation(
        source,
        target,
        alphabets.RepresentationProfile.LOSSY,
        pairs,
        (0,),
        qualification=(("discarded-bits", 1),),
    )
    approximate = alphabets.RepresentationRelation(
        source,
        target,
        alphabets.RepresentationProfile.APPROXIMATE,
        pairs,
        (0,),
        qualification=(("error-bound", Fraction(1, 2)),),
    )

    assert lossy.forward(0) == lossy.forward(1) == 0
    assert approximate.qualification == (("error-bound", Fraction(1, 2)),)
    for relation in (lossy, approximate):
        blob = serialization.dumps(relation)
        assert serialization.loads(blob) == serialization.Decoded(relation)
        assert serialization.dumps(serialization.loads(blob).value) == blob
        with pytest.raises(ValueError, match="only exact"):
            relation.inverse(0)
        with pytest.raises(ValueError, match="outside"):
            relation.forward(2)
