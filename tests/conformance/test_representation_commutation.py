"""CT10: inverse-on-image and complete one-step representation commutation."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction

import pytest

import ca
from ca import alphabets, loci, program, rules, serialization

from g7_fixtures import (
    derivation,
    finite_record_program,
    no_successor,
    rule_contract,
)
from g7_mechanics import (
    MECHANICS_ROWS,
    assert_mechanics_run,
    run_mechanics_fixture,
)


PX10_ROWS = tuple(row for row in MECHANICS_ROWS if row.primary == "PX10")
def _exact_relation(row) -> alphabets.RepresentationRelation:
    execution = run_mechanics_fixture(row)
    assert_mechanics_run(execution)
    relation = execution.representation

    assert relation is not None
    assert relation.profile is alphabets.RepresentationProfile.EXACT
    return relation


def _transition_pair(
    relation: alphabets.RepresentationRelation,
) -> tuple[program.ApplicationComplete, program.ApplicationComplete]:
    """Build independently expanded native/represented conjugate steps."""

    assert len(relation.relation) >= 2
    first, second = relation.relation[:2]

    def build(
        initial: alphabets.SemanticValue,
        following: alphabets.SemanticValue,
        values: tuple[alphabets.SemanticValue, ...],
    ) -> tuple[ca.SimpleProgram, loci.FiniteConfiguration]:
        def atoms(targets: tuple[loci.Locus, ...]):
            return (
                derivation(
                    "representation-step",
                    existing=(rules.replace(targets[0], following),),
                ),
            )

        return finite_record_program(
            (("value", initial),),
            atoms,
            alphabet=alphabets.enum(values),
            effects=(ca.frontiers.Effect.REPLACE,),
        )

    native_program, native_source = build(
        first.source,
        second.source,
        tuple(pair.source for pair in relation.relation),
    )
    represented_program, represented_source = build(
        first.target,
        second.target,
        tuple(pair.target for pair in relation.relation),
    )
    native = ca.apply(native_program, native_source)
    represented = ca.apply(represented_program, represented_source)
    assert isinstance(native, program.ApplicationComplete)
    assert isinstance(represented, program.ApplicationComplete)
    return native, represented


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
        aliases[atom.canonical_identity] = f"@source:{atom.witness.identity}"
    for atom in result.applied_atoms.atoms:
        witness = atom.source.witness.identity
        aliases[atom.canonical_identity] = f"@applied:{witness}"
        aliases[atom.evidence.application_identity] = "@application"
        aliases[atom.evidence.disposition_identity] = f"@disposition:{witness}"
        aliases[atom.input_trace_lineage.root_identity] = "@lineage-root"
        aliases[atom.output_trace_lineage.root_identity] = "@lineage-root"
        if isinstance(atom, program.AppliedDerivation):
            for index, binding in enumerate(atom.fresh_bindings):
                aliases[loci.canonical_identity(binding.identity)] = (
                    f"@fresh:{witness}:{index}"
                )
        for index, identity in enumerate(atom.input_trace_lineage.path):
            aliases.setdefault(identity, f"@input-path:{index}")
        for index, identity in enumerate(atom.output_trace_lineage.path):
            aliases.setdefault(identity, f"@output-path:{index}")
        if isinstance(atom, program.AppliedDerivation):
            aliases[loci.configuration_identity(atom.successor)] = "@successor"
    return aliases


_IDENTITY_FIELDS = frozenset(
    {
        (rules.AtomMass, "atom_identity"),
        (program.TraceLineage, "root_identity"),
        (program.TraceLineage, "path"),
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
                identity_bearing=(type(value), field.name)
                in _IDENTITY_FIELDS,
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
    """Every exact PX10 relation decodes its full declared image."""

    assert len(PX10_ROWS) == 8
    for row in PX10_ROWS:
        relation = _exact_relation(row)
        for pair in relation.relation:
            assert relation.inverse(relation.forward(pair.source)) == pair.source
        with pytest.raises(ValueError, match="outside"):
            relation.inverse(
                alphabets.ValueNode(
                    alphabets.ValueKind.SYMBOLIC,
                    "outside-image",
                )
            )


@pytest.mark.parametrize("row", PX10_ROWS, ids=lambda row: row.spf)
def test_represented_and_native_one_step_results_commute_completely(row) -> None:
    """Mapped represented application equals native application in every field."""

    relation = _exact_relation(row)
    native, represented = _transition_pair(relation)

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
        with pytest.raises(ValueError, match="only exact"):
            relation.inverse(0)
        with pytest.raises(ValueError, match="outside"):
            relation.forward(2)
