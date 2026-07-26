"""Unit contract for canonical, catalog-free semantic serialization."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import json
import subprocess
import sys

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


def _program() -> tuple[ca.SimpleProgram, loci.FiniteConfiguration]:
    source = loci.history_configuration((True, False, False))
    alphabet = alphabets.boolean()
    return (
        ca.SimpleProgram(
            seeds.exact(source),
            alphabet,
            frontiers.everywhere(
                configuration_contract=source.contract,
                value_profile=alphabet.value_profile,
            ),
            neighborhoods.dyadlags_0d(
                configuration_contract=source.contract,
            ),
            rules.dyadlags_0d(rule=150),
        ),
        source,
    )


def _certificate(
    kind: rules.CertificateKind,
    label: str,
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _anchored_fixture(
    *,
    mass: Fraction | None = None,
    conflict_policy: rules.ProposalConflictPolicy = (
        rules.ProposalConflictPolicy.REQUIRE_EQUAL
    ),
) -> tuple[
    ca.SimpleProgram,
    loci.FiniteConfiguration,
    neighborhoods.ReadableView,
]:
    """Build one complete value-anchored five-field codec fixture."""

    source = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        axes=("x",),
    )
    alphabet = alphabets.boolean()
    anchor = alphabets.ValueAnchor(
        alphabets.value_equals(True),
        alphabets.AnchorCardinality.EXACTLY_ONE,
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
    replacement = rules.DerivationClauseResult(
        (
            rules.ExistingDispositionPlan(
                rules.capability_group_item(0, 0),
                rules.DispositionAction.REPLACE,
                rules.literal_expr(False),
            ),
        ),
        (),
        rules.Progress.ADVANCED,
        rules.Continue(),
        rules.literal_expr("anchored-codec-derivation"),
        ("codec:anchored",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "anchored-codec-derivation",
        ),
    )
    zero_result = rules.DerivationClauseResult(
        (),
        (),
        rules.Progress.QUIESCENT,
        rules.Continue(),
        rules.literal_expr("anchored-codec-zero"),
        ("codec:anchored-zero",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "anchored-codec-zero",
        ),
    )
    contract = rules.RuleContract(
        source.contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
        entropy_interface=(
            seeds.EntropyInterface.REPLAY_KEY
            if mass is not None
            else seeds.EntropyInterface.NONE
        ),
    )
    rule = rules.anchored_clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(True),
                replacement,
                mass,
            ),
        ),
        group_channel=0,
        zero_result=zero_result,
        contract=contract,
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "anchored-codec-complete",
        ),
        conflict_policy=conflict_policy,
        selection=(
            rules.ClauseSelection.ALL
            if mass is not None
            else rules.ClauseSelection.FIRST
        ),
    )
    simple_program = ca.SimpleProgram(
        seed=seeds.exact(source),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )
    resolved = readable.resolve(source)
    assert type(resolved) is neighborhoods.ReadableView
    return simple_program, source, resolved


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _redigest(envelope: dict[str, object]) -> bytes:
    core = {
        "tag": envelope["tag"],
        "version": envelope["version"],
        "payload": envelope["payload"],
    }
    envelope["digest"] = "sha256:" + sha256(_canonical_json(core)).hexdigest()
    return _canonical_json(envelope)


def _nested_wire_value(value: object) -> dict[str, object]:
    """Encode one value as a nested canonical node without a root digest."""

    envelope = json.loads(serialization.dumps(value))
    del envelope["digest"]
    return envelope


def _assert_rejected(blob: object, reason: str | None = None) -> None:
    result = serialization.loads(blob)  # type: ignore[arg-type]
    assert isinstance(result, serialization.DecodeRejected)
    assert isinstance(result.fault, serialization.DecodeFault)
    if reason is not None:
        assert result.fault.reason == reason


def test_decode_result_is_decoded_or_typed_rejection() -> None:
    """Decoding is total and never returns a partial semantic object."""

    encoded = serialization.dumps(Fraction(-7, 13))
    result = serialization.loads(encoded)

    assert result == serialization.Decoded(Fraction(-7, 13))
    for invalid in (
        b"",
        b"\xff",
        b"null",
        b"{}",
        b'{"tag":',
        bytearray(encoded),
        "not bytes",
    ):
        _assert_rejected(invalid)


def test_canonical_program_envelope_uses_tag_v1_and_exactly_five_keys() -> None:
    """The first program schema expands only the five semantic fields."""

    simple_program, _ = _program()
    encoded = serialization.dumps(simple_program)
    envelope = json.loads(encoded)

    assert tuple(envelope) == ("digest", "payload", "tag", "version")
    assert envelope["tag"] == "ca.simple-program"
    assert envelope["version"] == 1
    assert set(envelope["payload"]) == {
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    }
    assert len(envelope["digest"]) == len("sha256:") + 64
    decoded = serialization.loads(encoded)
    assert decoded == serialization.Decoded(simple_program)
    assert serialization.dumps(decoded.value) == encoded


def test_every_registered_shape_and_exact_scalar_round_trips_canonically() -> None:
    """The closed registry and exact scalar algebra share one codec boundary."""

    schemas = serialization._schema_rows()
    assert len(schemas) == 187
    assert sum(
        len(row.enum_values) if row.enum_values else 1 for row in schemas
    ) == 441
    assert len({row.tag for row in schemas}) == 187
    assert len({row.value_type for row in schemas}) == 187

    samples: list[object] = [
        None,
        False,
        True,
        0,
        -1,
        10**10_000,
        "",
        "λ\n\u0000",
        "\ud800",
        Fraction(-355, 113),
        (None, False, 7, Fraction(2, 3), ("nested",)),
        loci.coordinate("x", 2, scope="sample"),
        alphabets.AlgebraicNumber(
            (1, 0, -2),
            (Fraction(1), Fraction(2)),
        ),
    ]
    for row in schemas:
        if row.enum_values:
            samples.extend(row.value_type(value) for value in row.enum_values)

    simple_program, source = _program()
    samples.extend(
        (
            simple_program,
            ca.apply(simple_program, source),
            ca.rollout(simple_program, steps=1, initial=source),
        )
    )
    for sample in samples:
        encoded = serialization.dumps(sample)
        decoded = serialization.loads(encoded)
        assert decoded == serialization.Decoded(sample)
        assert serialization.dumps(decoded.value) == encoded


def test_registry_fails_closed_when_an_owner_gains_an_unregistered_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Owner-surface reflection detects drift but never selects a wire path."""

    @dataclass(frozen=True)
    class FutureSealed:
        marker: int

    FutureSealed.__module__ = loci.__name__
    monkeypatch.setattr(loci, "FutureSealed", FutureSealed, raising=False)

    with pytest.raises(RuntimeError, match="missing=.*FutureSealed"):
        serialization._validate_registry()


def test_explicit_wire_tag_survives_python_type_and_module_rename() -> None:
    """A deliberate code move updates membership metadata, never wire v1."""

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            """
from dataclasses import replace
import json
from types import MappingProxyType

from ca import loci, program, serialization

value = loci.coordinate("x", 7, scope="stable-wire")
original = serialization._SCHEMA_BY_TYPE[loci.Locus]
assert original.tag == "ca.loci.locus"
renamed = replace(
    original,
    owner=program.__name__,
    type_name="SpatialLocus",
)
serialization._SCHEMAS = tuple(
    renamed if row.value_type is loci.Locus else row
    for row in serialization._schema_rows()
)
by_type = dict(serialization._SCHEMA_BY_TYPE)
by_type[loci.Locus] = renamed
serialization._SCHEMA_BY_TYPE = MappingProxyType(by_type)
by_tag = dict(serialization._SCHEMA_BY_TAG)
by_tag[renamed.tag] = renamed
serialization._SCHEMA_BY_TAG = MappingProxyType(by_tag)
loci.Locus.__module__ = program.__name__
loci.Locus.__name__ = "SpatialLocus"
loci.Locus.__qualname__ = "SpatialLocus"
program.SpatialLocus = loci.Locus

serialization._validate_registry()
encoded = serialization.dumps(value)
assert renamed.owner == "ca.program"
assert renamed.type_name == "SpatialLocus"
assert json.loads(encoded)["tag"] == "ca.loci.locus"
assert serialization.loads(encoded) == serialization.Decoded(value)
""",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def _new_rule_expression_samples() -> tuple[rules.RuleExpr, ...]:
    """Return one structurally valid expression for each reopened G7-02 node."""

    source = rules.literal_expr("source")
    sequence = rules.literal_expr(
        alphabets.word_value(("a", "b"), tag="symbols")
    )
    index = rules.literal_expr(0)
    default = rules.literal_expr("default")
    value = rules.literal_expr("value")
    table = rules.literal_expr("table")
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_sequence((alphabets.pattern_bind("item"),)),
        alphabets.template_sequence(
            (alphabets.template_binding("item"),)
        ),
    )
    rewrite_rules = rules.literal_expr(
        alphabets.rewrite_rules_value((rewrite_rule,))
    )
    source_field = alphabets.grid_field_value(
        ("x",),
        (1,),
        ("A",),
        tag="codec-source",
    )
    tile = alphabets.grid_field_value(
        ("x",),
        (1,),
        ("a",),
        tag="codec-tile",
    )
    productions = alphabets.map_value(
        (alphabets.map_entry_value("A", tile),),
        tag="mosaic-productions",
    )
    return (
        rules.bound_value(1),
        rules.bound_index(1),
        rules.record_field(source, "field"),
        rules.record_update(source, "field", value),
        rules.length(source),
        rules.item_at(source, index, default),
        rules.slice_items(source, index, rules.literal_expr(1)),
        rules.concatenate(source, value),
        rules.reverse(source),
        rules.replace_at(source, index, value),
        rules.map_lookup(source, index, default),
        rules.map_update(source, index, value),
        rules.index_of(source, value, rules.literal_expr(-1)),
        rules.index_of_tag(source, "head", rules.literal_expr(-1)),
        rules.floor_divide(rules.literal_expr(7), rules.literal_expr(3)),
        rules.absolute(rules.literal_expr(-7)),
        rules.fractional_part(rules.literal_expr(Fraction(7, 3))),
        rules.integer_digits(rules.literal_expr(7), 2, width=3),
        rules.from_digits(source, 2),
        rules.maximal_runs(source),
        rules.product_value("product", value),
        rules.word_value("word", value),
        rules.flat_map_lookup(source, table),
        rules.map_items(sequence, rules.bound_value(), "mapped"),
        rules.filter_items(
            sequence,
            rules.equal(rules.bound_index(), rules.literal_expr(0)),
        ),
        rules.flat_map_items(
            sequence,
            rules.word_value("symbols", rules.bound_value()),
            "symbols",
        ),
        rules.sliding_windows(
            sequence,
            1,
            1,
            rules.SequenceBoundary.FIXED,
            exterior=rules.literal_expr("outside"),
        ),
        rules.pattern_rewrite(
            sequence,
            rewrite_rules,
            scan=rules.RewriteScan.LOCATION_PRIORITY_NONOVERLAPPING,
        ),
        rules.mosaic_substitute(
            rules.literal_expr(source_field),
            rules.literal_expr(productions),
        ),
    )


def _reopened_mode_expression_samples() -> tuple[rules.RuleExpr, ...]:
    """Exercise every new boundary/scan mode in an inhabitable AST."""

    sequence = rules.literal_expr(
        alphabets.word_value(("a", "b"), tag="symbols")
    )
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_sequence((alphabets.pattern_bind("item"),)),
        alphabets.template_sequence(
            (alphabets.template_binding("item"),)
        ),
    )
    rewrite_rules = rules.literal_expr(
        alphabets.rewrite_rules_value((rewrite_rule,))
    )
    source_field = alphabets.grid_field_value(
        ("x",),
        (1,),
        ("A",),
        tag="codec-source",
    )
    tile = alphabets.grid_field_value(
        ("x",),
        (1,),
        ("a",),
        tag="codec-tile",
    )
    independent_productions = alphabets.map_value(
        (alphabets.map_entry_value("A", tile),),
        tag="mosaic-productions",
    )
    context = alphabets.word_value(("A",), tag="mosaic-context")
    contextual_productions = alphabets.map_value(
        (alphabets.map_entry_value(context, tile),),
        tag="mosaic-productions",
    )
    source_expression = rules.literal_expr(source_field)
    contextual_expression = rules.literal_expr(contextual_productions)

    return (
        rules.sliding_windows(
            sequence,
            1,
            1,
            rules.SequenceBoundary.FIXED,
            exterior=rules.literal_expr("outside"),
        ),
        rules.sliding_windows(
            sequence,
            1,
            1,
            rules.SequenceBoundary.PERIODIC,
        ),
        rules.sliding_windows(
            sequence,
            1,
            1,
            rules.SequenceBoundary.REFLECTIVE,
        ),
        *(
            rules.pattern_rewrite(
                sequence,
                rewrite_rules,
                scan=scan,
            )
            for scan in rules.RewriteScan
        ),
        rules.mosaic_substitute(
            source_expression,
            rules.literal_expr(independent_productions),
        ),
        rules.mosaic_substitute(
            source_expression,
            contextual_expression,
            offsets=((0,),),
            boundary=rules.SequenceBoundary.FIXED,
            exterior=rules.literal_expr("outside"),
        ),
        rules.mosaic_substitute(
            source_expression,
            contextual_expression,
            offsets=((0,),),
            boundary=rules.SequenceBoundary.PERIODIC,
        ),
        rules.mosaic_substitute(
            source_expression,
            contextual_expression,
            offsets=((0,),),
            boundary=rules.SequenceBoundary.REFLECTIVE,
        ),
    )


def _rank_four_program() -> tuple[
    ca.SimpleProgram,
    loci.FiniteConfiguration,
]:
    source = loci.grid_configuration(
        (1, 1, 1, 2),
        (False, True),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        axes=("batch", "time", "row", "column"),
    )
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
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
        witness=rules.literal_expr("rank-four-codec"),
        provenance=("codec:rank-four",),
    )
    return (
        ca.SimpleProgram(
            seeds.exact(source),
            alphabet,
            writable,
            readable,
            rule,
        ),
        source,
    )


def test_new_rule_expression_primitives_round_trip_in_exact_enum_order() -> None:
    """Every reopened mechanics node uses the existing closed RuleExpr codec."""

    samples = _new_rule_expression_samples()
    new_primitives = (
        rules.ExpressionPrimitive.BOUND_VALUE,
        rules.ExpressionPrimitive.BOUND_INDEX,
        rules.ExpressionPrimitive.RECORD_FIELD,
        rules.ExpressionPrimitive.RECORD_UPDATE,
        rules.ExpressionPrimitive.LENGTH,
        rules.ExpressionPrimitive.ITEM_AT,
        rules.ExpressionPrimitive.SLICE,
        rules.ExpressionPrimitive.CONCATENATE,
        rules.ExpressionPrimitive.REVERSE,
        rules.ExpressionPrimitive.REPLACE_AT,
        rules.ExpressionPrimitive.MAP_LOOKUP,
        rules.ExpressionPrimitive.MAP_UPDATE,
        rules.ExpressionPrimitive.INDEX_OF,
        rules.ExpressionPrimitive.INDEX_OF_TAG,
        rules.ExpressionPrimitive.FLOOR_DIVIDE,
        rules.ExpressionPrimitive.ABSOLUTE,
        rules.ExpressionPrimitive.FRACTIONAL_PART,
        rules.ExpressionPrimitive.INTEGER_DIGITS,
        rules.ExpressionPrimitive.FROM_DIGITS,
        rules.ExpressionPrimitive.MAXIMAL_RUNS,
        rules.ExpressionPrimitive.PRODUCT_VALUE,
        rules.ExpressionPrimitive.WORD_VALUE,
        rules.ExpressionPrimitive.FLAT_MAP_LOOKUP,
        rules.ExpressionPrimitive.MAP_ITEMS,
        rules.ExpressionPrimitive.FILTER_ITEMS,
        rules.ExpressionPrimitive.FLAT_MAP_ITEMS,
        rules.ExpressionPrimitive.SLIDING_WINDOWS,
        rules.ExpressionPrimitive.PATTERN_REWRITE,
        rules.ExpressionPrimitive.MOSAIC_SUBSTITUTE,
    )

    assert len(samples) == 29
    assert tuple(expression.primitive for expression in samples) == new_primitives
    for expression in samples:
        encoded = serialization.dumps(expression)
        assert serialization.loads(encoded) == serialization.Decoded(expression)
        assert serialization.dumps(expression) == encoded


@pytest.mark.parametrize("expression", _new_rule_expression_samples())
def test_new_rule_expression_primitives_reject_malformed_wire_shape(
    expression: rules.RuleExpr,
) -> None:
    """A valid digest cannot bypass each new primitive's shape validation."""

    envelope = json.loads(serialization.dumps(expression))
    arguments = envelope["payload"]["arguments"]
    assert arguments["tag"] == "ca.tuple"
    arguments["payload"]["items"] = []

    result = serialization.loads(_redigest(envelope))
    assert isinstance(result, serialization.DecodeRejected)
    assert result.fault.reason == "invalid-descriptor"


def test_reopened_expression_modes_round_trip_without_collapsing() -> None:
    """Boundary, scan, and contextual forms retain their exact operands."""

    expressions = _reopened_mode_expression_samples()

    assert len(expressions) == 10
    encoded = tuple(serialization.dumps(expression) for expression in expressions)
    assert len(set(encoded)) == len(encoded)
    for expression, blob in zip(expressions, encoded, strict=True):
        assert serialization.loads(blob) == serialization.Decoded(expression)
        assert serialization.dumps(expression) == blob


def test_reopened_structural_components_and_results_round_trip() -> None:
    """The reopened schema is exercised by real non-default inhabitants."""

    equal = alphabets.value_equals(
        True,
        path=alphabets.ValuePath(("state", "armed")),
    )
    tagged = alphabets.value_tagged(
        "head",
        path=alphabets.ValuePath(("state", "role", 0)),
    )
    conjunction = alphabets.value_and((equal, tagged))
    negation = alphabets.value_not(equal)
    disjunction = alphabets.value_or((conjunction, negation))
    anchors = tuple(
        alphabets.ValueAnchor(disjunction, cardinality)
        for cardinality in alphabets.AnchorCardinality
    )
    semantic_map = alphabets.map_value(
        (
            alphabets.map_entry_value(False, "boolean"),
            alphabets.map_entry_value(0, "integer"),
        ),
        tag="semantic-keys",
    )
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "pair",
            (
                alphabets.pattern_bind("left"),
                alphabets.pattern_bind("right"),
            ),
        ),
        alphabets.template_node(
            "swapped",
            (
                alphabets.template_binding("right"),
                alphabets.template_binding("left"),
            ),
        ),
    )
    rewrite_bundle = alphabets.rewrite_rules_value((rewrite_rule,))
    grid_field = alphabets.grid_field_value(
        ("batch", "time", "row", "column"),
        (1, 1, 2, 2),
        (0, 1, 2, 3),
        tag="rank-four-field",
    )
    anchored_programs = tuple(
        _anchored_fixture(conflict_policy=policy)
        for policy in rules.ProposalConflictPolicy
    )
    simple_program, source, resolved = anchored_programs[0]
    application = ca.apply(simple_program, source)
    assert type(application) is program.ApplicationComplete
    dependency = resolved.dependencies[0]
    selector = rules.capability_group_item(0, 0)
    denotation = simple_program.rule.descriptor.denotation
    assert type(denotation) is rules.AnchoredClauseKernelDenotation
    rank_four_program, rank_four_source = _rank_four_program()

    values: tuple[object, ...] = (
        equal.path,
        equal,
        tagged,
        conjunction,
        negation,
        disjunction,
        *anchors,
        alphabets.rational_interval(
            Fraction(-2, 3),
            Fraction(5, 7),
            lower_closed=False,
        ),
        alphabets.symbolic_expression(),
        alphabets.symbolic_value(
            "plus",
            items=(1, alphabets.symbolic_value("x")),
        ),
        semantic_map,
        rewrite_bundle,
        grid_field,
        simple_program.frontier,
        simple_program.neighborhood,
        dependency,
        resolved,
        selector,
        denotation,
        simple_program.rule.descriptor,
        simple_program.rule,
        simple_program,
        application,
        rank_four_source,
        rank_four_program,
        *(
            fixture[0].rule.descriptor.denotation
            for fixture in anchored_programs
        ),
    )
    for value in values:
        blob = serialization.dumps(value)
        decoded = serialization.loads(blob)
        assert decoded == serialization.Decoded(value)
        assert serialization.dumps(decoded.value) == blob


def test_mutated_enum_singleton_cannot_encode_as_another_member() -> None:
    """Enum value forgery is rejected without polluting this interpreter."""

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            """
from ca import loci, serialization

member = loci.LocusKind.COORDINATE
object.__setattr__(member, "_value_", "named")
try:
    serialization.dumps(member)
except TypeError:
    pass
else:
    raise AssertionError("forged enum member encoded canonically")
""",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


@pytest.mark.parametrize(
    "member",
    (
        alphabets.AlphabetKind.RATIONAL_INTERVAL,
        alphabets.ValuePredicateKind.EQUAL,
        alphabets.AnchorCardinality.EXACTLY_ONE,
        rules.RulePrimitive.ANCHORED_CLAUSE_KERNEL,
        rules.ExpressionPrimitive.BOUND_VALUE,
        rules.SequenceBoundary.FIXED,
        rules.RewriteScan.RULE_PRIORITY_FIRST,
        rules.CapabilitySelectorKind.GROUP_ITEM,
        rules.ProposalConflictPolicy.REQUIRE_EQUAL,
    ),
)
def test_each_reopened_enum_schema_rejects_an_unknown_value(
    member: Enum,
) -> None:
    envelope = json.loads(serialization.dumps(member))
    envelope["payload"]["value"] = "future-reopened-member"
    _assert_rejected(_redigest(envelope), "unknown-enum-value")


def test_unknown_lossy_noncanonical_or_forged_payloads_fail_closed() -> None:
    """Hostile schema and integrity mutations cannot default or migrate."""

    simple_program, _ = _program()
    original = serialization.dumps(simple_program)
    envelope = json.loads(original)

    mutation = dict(envelope)
    mutation["tag"] = "ca.catalog.eca"
    _assert_rejected(_redigest(mutation), "unknown-tag")

    mutation = dict(envelope)
    mutation["version"] = 0
    _assert_rejected(_redigest(mutation), "unknown-version")

    mutation = dict(envelope)
    mutation["payload"] = dict(envelope["payload"])
    del mutation["payload"]["rule"]
    _assert_rejected(_redigest(mutation), "missing-field")

    mutation = dict(envelope)
    mutation["payload"] = dict(envelope["payload"])
    mutation["payload"]["observer"] = mutation["payload"]["seed"]
    _assert_rejected(_redigest(mutation), "extra-field")

    mutation = dict(envelope)
    mutation["digest"] = "sha256:" + "0" * 64
    _assert_rejected(_canonical_json(mutation), "forged-digest")

    enum_envelope = json.loads(
        serialization.dumps(loci.LocusKind.COORDINATE)
    )
    enum_envelope["payload"]["value"] = "future-locus"
    _assert_rejected(_redigest(enum_envelope), "unknown-enum-value")

    integer_envelope = json.loads(serialization.dumps(7))
    integer_envelope["payload"]["value"] = "007"
    _assert_rejected(_redigest(integer_envelope), "noncanonical-integer")

    rational_envelope = json.loads(serialization.dumps(Fraction(1, 2)))
    rational_envelope["payload"]["numerator"] = "2"
    rational_envelope["payload"]["denominator"] = "4"
    _assert_rejected(_redigest(rational_envelope), "noncanonical-rational")

    invalid_locus = json.loads(
        serialization.dumps(loci.coordinate("x", 1))
    )
    invalid_locus["payload"]["scope"]["payload"]["value"] = ""
    _assert_rejected(_redigest(invalid_locus), "invalid-descriptor")

    float_envelope = {
        "tag": "ca.scalar.float",
        "version": 1,
        "payload": {"value": "1.25"},
    }
    float_envelope["digest"] = (
        "sha256:"
        + sha256(
            _canonical_json(
                {
                    "tag": float_envelope["tag"],
                    "version": 1,
                    "payload": float_envelope["payload"],
                }
            )
        ).hexdigest()
    )
    _assert_rejected(_canonical_json(float_envelope), "unknown-primitive")

    noncanonical = original + b"\n"
    _assert_rejected(noncanonical, "noncanonical-encoding")

    duplicate = original.replace(
        b'"tag":"ca.simple-program"',
        b'"tag":"ca.simple-program","tag":"ca.simple-program"',
        1,
    )
    _assert_rejected(duplicate, "duplicate-field")


def test_reopened_expression_nested_wire_mutations_fail_closed() -> None:
    """Nested scan, boundary, exterior, and offset structure is validated."""

    expressions = _reopened_mode_expression_samples()

    sliding = json.loads(serialization.dumps(expressions[0]))
    sliding_arguments = sliding["payload"]["arguments"]["payload"]["items"]
    sliding_arguments[3]["payload"]["value"] = "future-boundary"
    _assert_rejected(_redigest(sliding), "invalid-descriptor")

    pattern = json.loads(serialization.dumps(expressions[3]))
    pattern_arguments = pattern["payload"]["arguments"]["payload"]["items"]
    pattern_arguments[2]["payload"]["value"] = "future-scan"
    _assert_rejected(_redigest(pattern), "invalid-descriptor")

    mosaic = json.loads(serialization.dumps(expressions[7]))
    mosaic_arguments = mosaic["payload"]["arguments"]["payload"]["items"]
    mosaic_arguments[2]["payload"]["tag"]["payload"]["value"] = (
        "forged-offsets"
    )
    _assert_rejected(_redigest(mosaic), "invalid-descriptor")

    missing_exterior = json.loads(serialization.dumps(expressions[7]))
    missing_arguments = (
        missing_exterior["payload"]["arguments"]["payload"]["items"]
    )
    missing_arguments.pop()
    _assert_rejected(_redigest(missing_exterior), "invalid-descriptor")


def test_expanded_v1_records_reject_pre_delta_missing_fields() -> None:
    """Reopened v1 shapes cannot silently fill their newly required fields."""

    simple_program, _, resolved = _anchored_fixture()
    selector = rules.capability_group_item(0, 0)
    expanded = (
        (simple_program.frontier, "value_anchor"),
        (simple_program.neighborhood, "value_anchor"),
        (resolved.dependencies[0], "value_anchor"),
        (selector, "channel"),
        (selector, "item"),
    )

    for value, field in expanded:
        envelope = json.loads(serialization.dumps(value))
        del envelope["payload"][field]
        _assert_rejected(_redigest(envelope), "missing-field")


def test_expanded_record_invariants_reject_hostile_wire_values() -> None:
    """Non-default anchor/selector fields remain locally fail-closed."""

    simple_program, _, resolved = _anchored_fixture()

    negative_channel = json.loads(
        serialization.dumps(rules.capability_group_item(0, 0))
    )
    negative_channel["payload"]["channel"] = _nested_wire_value(-1)
    _assert_rejected(_redigest(negative_channel), "invalid-descriptor")

    boolean_item = json.loads(
        serialization.dumps(rules.capability_group_item(0, 0))
    )
    boolean_item["payload"]["item"] = _nested_wire_value(True)
    _assert_rejected(_redigest(boolean_item), "invalid-descriptor")

    forbidden_index = json.loads(
        serialization.dumps(rules.capability_group_item(0, 0))
    )
    forbidden_index["payload"]["index"] = _nested_wire_value(0)
    _assert_rejected(_redigest(forbidden_index), "invalid-descriptor")

    hidden_selector = json.loads(
        serialization.dumps(simple_program.neighborhood)
    )
    hidden_selector["payload"]["selector"] = _nested_wire_value(
        loci.selector_tagged("forbidden")
    )
    _assert_rejected(_redigest(hidden_selector), "invalid-descriptor")

    dependency_selector = json.loads(
        serialization.dumps(resolved.dependencies[0])
    )
    dependency_selector["payload"]["selector"] = _nested_wire_value(
        loci.selector_tagged("forbidden")
    )
    _assert_rejected(_redigest(dependency_selector), "invalid-descriptor")

    wrong_writable_descriptor = json.loads(
        serialization.dumps(simple_program.frontier)
    )
    wrong_writable_descriptor["payload"]["descriptor"] = _nested_wire_value(
        loci.all_support()
    )
    _assert_rejected(
        _redigest(wrong_writable_descriptor),
        "invalid-descriptor",
    )


def test_reopened_predicate_and_interval_wire_mutations_fail_closed() -> None:
    """New selector and exact-interval records reject forged inhabitants."""

    path = alphabets.ValuePath(("state", 0))
    invalid_path = json.loads(serialization.dumps(path))
    path_items = invalid_path["payload"]["segments"]["payload"]["items"]
    path_items[1] = _nested_wire_value(True)
    _assert_rejected(_redigest(invalid_path), "invalid-descriptor")

    equal = alphabets.value_equals(True)
    conjunction = alphabets.value_and(
        (equal, alphabets.value_not(equal))
    )
    invalid_conjunction = json.loads(serialization.dumps(conjunction))
    children = invalid_conjunction["payload"]["children"]["payload"]["items"]
    children.pop()
    _assert_rejected(_redigest(invalid_conjunction), "invalid-descriptor")

    invalid_equal = json.loads(serialization.dumps(equal))
    invalid_equal["payload"]["expected"] = _nested_wire_value(None)
    _assert_rejected(_redigest(invalid_equal), "invalid-descriptor")

    invalid_anchor = json.loads(
        serialization.dumps(alphabets.ValueAnchor(equal))
    )
    invalid_anchor["payload"]["cardinality"]["payload"]["value"] = (
        "future-cardinality"
    )
    _assert_rejected(_redigest(invalid_anchor), "unknown-enum-value")

    interval = alphabets.rational_interval(
        Fraction(-1, 2),
        Fraction(3, 2),
    ).descriptor

    def scalar_items(
        envelope: dict[str, object],
    ) -> tuple[list[object], dict[str, list[object]]]:
        items = envelope["payload"]["scalars"]["payload"]["items"]
        by_name = {
            pair["payload"]["items"][0]["payload"]["value"]: (
                pair["payload"]["items"]
            )
            for pair in items
        }
        return items, by_name

    reordered = json.loads(serialization.dumps(interval))
    items, _ = scalar_items(reordered)
    items.reverse()
    _assert_rejected(_redigest(reordered), "invalid-descriptor")

    missing = json.loads(serialization.dumps(interval))
    items, _ = scalar_items(missing)
    items.pop()
    _assert_rejected(_redigest(missing), "invalid-descriptor")

    integer_bound = json.loads(serialization.dumps(interval))
    _, parameters = scalar_items(integer_bound)
    parameters["lower"][1] = _nested_wire_value(0)
    _assert_rejected(_redigest(integer_bound), "invalid-descriptor")

    reversed_bounds = json.loads(serialization.dumps(interval))
    _, parameters = scalar_items(reversed_bounds)
    parameters["lower"][1] = _nested_wire_value(Fraction(2))
    parameters["upper"][1] = _nested_wire_value(Fraction(1))
    _assert_rejected(_redigest(reversed_bounds), "invalid-descriptor")

    empty_interval = json.loads(serialization.dumps(interval))
    _, parameters = scalar_items(empty_interval)
    parameters["lower"][1] = _nested_wire_value(Fraction(1))
    parameters["upper"][1] = _nested_wire_value(Fraction(1))
    parameters["lower_closed"][1] = _nested_wire_value(False)
    _assert_rejected(_redigest(empty_interval), "invalid-descriptor")


def test_composite_value_wire_order_and_semantic_keys_are_canonical() -> None:
    """Maps and named structural fields cannot admit a second byte spelling."""

    semantic_map = alphabets.map_value(
        (
            alphabets.map_entry_value(False, "boolean"),
            alphabets.map_entry_value(0, "integer"),
        ),
        tag="semantic-keys",
    )
    reversed_map = json.loads(serialization.dumps(semantic_map))
    map_items = reversed_map["payload"]["items"]["payload"]["items"]
    map_items.reverse()
    _assert_rejected(_redigest(reversed_map), "noncanonical-encoding")

    duplicate_key = json.loads(serialization.dumps(semantic_map))
    map_items = duplicate_key["payload"]["items"]["payload"]["items"]
    first_key = map_items[0]["payload"]["items"]["payload"]["items"][0]
    second_items = map_items[1]["payload"]["items"]["payload"]["items"]
    second_items[0] = deepcopy(first_key)
    _assert_rejected(_redigest(duplicate_key), "invalid-descriptor")

    field = alphabets.grid_field_value(
        ("x", "y"),
        (1, 2),
        (0, 1),
        tag="canonical-field",
    )
    reversed_fields = json.loads(serialization.dumps(field))
    fields = reversed_fields["payload"]["fields"]["payload"]["items"]
    fields.reverse()
    _assert_rejected(
        _redigest(reversed_fields),
        "noncanonical-encoding",
    )


def test_hostile_anchored_rule_graphs_fail_closed() -> None:
    """Decoded anchored Rules must satisfy builder-level graph contracts."""

    weighted_program, _, _ = _anchored_fixture(mass=Fraction(1))
    anchored_rule = weighted_program.rule

    wrong_entropy = json.loads(serialization.dumps(anchored_rule))
    contract = wrong_entropy["payload"]["contract"]["payload"]
    contract["entropy_interface"] = _nested_wire_value(
        seeds.EntropyInterface.NONE
    )
    _assert_rejected(_redigest(wrong_entropy), "invalid-descriptor")

    missing_effect = json.loads(serialization.dumps(anchored_rule))
    contract = missing_effect["payload"]["contract"]["payload"]
    effect_profile = contract["required_effect_profile"]["payload"]
    effect_profile["existing"] = _nested_wire_value(())
    _assert_rejected(_redigest(missing_effect), "invalid-descriptor")

    def denotation_payload(envelope: dict[str, object]) -> dict[str, object]:
        return envelope["payload"]["descriptor"]["payload"]["denotation"][
            "payload"
        ]

    wrong_channel = json.loads(serialization.dumps(anchored_rule))
    denotation_payload(wrong_channel)["group_channel"] = _nested_wire_value(
        True
    )
    _assert_rejected(_redigest(wrong_channel), "invalid-descriptor")

    wrong_selector = json.loads(serialization.dumps(anchored_rule))
    denotation = denotation_payload(wrong_selector)
    clause = denotation["clauses"]["payload"]["items"][0]["payload"]
    clause_result = clause["result"]
    plan = clause_result["payload"]["existing_plans"]["payload"]["items"][0]
    plan["payload"]["selector"] = _nested_wire_value(
        rules.capability_index(0)
    )
    _assert_rejected(_redigest(wrong_selector), "invalid-descriptor")

    proposed_zero = json.loads(serialization.dumps(anchored_rule))
    denotation = denotation_payload(proposed_zero)
    clause = denotation["clauses"]["payload"]["items"][0]["payload"]
    denotation["zero_result"] = deepcopy(clause["result"])
    _assert_rejected(_redigest(proposed_zero), "invalid-descriptor")

    standard_result = rules.DerivationClauseResult(
        (
            rules.ExistingDispositionPlan(
                rules.capability_index(0),
                rules.DispositionAction.REPLACE,
                rules.literal_expr(False),
            ),
        ),
        (
            rules.FreshDispositionPlan(
                rules.capability_index(0),
                rules.DispositionAction.CREATE,
                rules.literal_expr(True),
            ),
        ),
        rules.Progress.ADVANCED,
        rules.Continue(),
        rules.literal_expr("standard-clause-codec"),
        ("codec:standard-clause",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "standard-clause-codec",
        ),
    )
    standard_contract = rules.RuleContract(
        anchored_rule.contract.configuration_contract,
        anchored_rule.contract.value_profile,
        anchored_rule.contract.required_read_shape,
        anchored_rule.contract.required_join_shape,
        frontiers.EffectProfile(
            existing=(frontiers.Effect.REPLACE,),
            fresh=(frontiers.Effect.CREATE,),
        ),
    )
    standard_rule = rules.clause_kernel(
        (
            rules.RuleClause(
                rules.literal_expr(True),
                standard_result,
            ),
        ),
        contract=standard_contract,
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "standard-clause-complete",
        ),
    )
    for effect_side in ("existing", "fresh"):
        missing_standard_effect = json.loads(
            serialization.dumps(standard_rule)
        )
        contract = missing_standard_effect["payload"]["contract"]["payload"]
        effect_profile = contract["required_effect_profile"]["payload"]
        effect_profile[effect_side] = _nested_wire_value(())
        _assert_rejected(
            _redigest(missing_standard_effect),
            "invalid-descriptor",
        )


def test_hostile_rule_variant_refinements_fail_closed() -> None:
    """Signed wire data cannot bypass public Rule-constructor refinements."""

    base_rule = _program()[0].rule
    terminal = rules.NoSuccessor(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.literal_expr("codec-terminal"),
        rules.Witness(
            "codec-terminal",
            rules.literal_expr("codec-terminal"),
        ),
        ("codec:terminal",),
        _certificate(
            rules.CertificateKind.TERMINALITY,
            "codec-terminal",
        ),
    )
    literal_rule = rules.finite_rule(
        (terminal,),
        contract=base_rule.contract,
    )
    empty_literal = json.loads(serialization.dumps(literal_rule))
    literal_denotation = empty_literal["payload"]["descriptor"]["payload"][
        "denotation"
    ]["payload"]
    literal_denotation["outcomes"]["payload"]["support"] = (
        _nested_wire_value(rules.finite_support(()))
    )
    _assert_rejected(_redigest(empty_literal), "invalid-descriptor")

    complete = rules.RuleComplete(
        rules.OutcomeSpace(rules.finite_support((terminal,)))
    )
    empty_complete = json.loads(serialization.dumps(complete))
    empty_complete["payload"]["outcome_space"]["payload"]["support"] = (
        _nested_wire_value(rules.finite_support(()))
    )
    _assert_rejected(_redigest(empty_complete), "invalid-descriptor")

    parallel_rule = rules.parallel((base_rule, base_rule))
    standalone_parallel = json.loads(
        serialization.dumps(
            rules.ParallelDenotation((base_rule, base_rule))
        )
    )
    standalone_parts = standalone_parallel["payload"]["parts"]["payload"][
        "items"
    ]
    standalone_contract = standalone_parts[0]["payload"]["contract"]["payload"]
    standalone_contract["required_effect_profile"]["payload"]["existing"] = (
        _nested_wire_value(())
    )
    _assert_rejected(
        _redigest(standalone_parallel),
        "invalid-descriptor",
    )

    wrong_outer_contract = json.loads(
        serialization.dumps(parallel_rule)
    )
    outer_contract = wrong_outer_contract["payload"]["contract"]["payload"]
    outer_contract["required_effect_profile"]["payload"]["existing"] = (
        _nested_wire_value(())
    )
    _assert_rejected(
        _redigest(wrong_outer_contract),
        "invalid-descriptor",
    )

    unequal_part_contracts = json.loads(
        serialization.dumps(parallel_rule)
    )
    parallel_denotation = unequal_part_contracts["payload"]["descriptor"][
        "payload"
    ]["denotation"]["payload"]
    first_part = parallel_denotation["parts"]["payload"]["items"][0]["payload"]
    first_contract = first_part["contract"]["payload"]
    first_contract["required_effect_profile"]["payload"]["existing"] = (
        _nested_wire_value(())
    )
    _assert_rejected(
        _redigest(unequal_part_contracts),
        "invalid-descriptor",
    )

    cardinality = rules.ExactlyOne(
        _certificate(
            rules.CertificateKind.CARDINALITY,
            "codec-intensional-one",
        )
    )
    complete = _certificate(
        rules.CertificateKind.COMPLETENESS,
        "codec-intensional-complete",
    )
    sound = _certificate(
        rules.CertificateKind.SOUNDNESS,
        "codec-intensional-sound",
    )
    relation_rule = rules.relation(
        rules.literal_expr("codec-relation"),
        cardinality,
        contract=base_rule.contract,
        completeness_evidence=complete,
        soundness_evidence=sound,
    )
    missing_distribution_law = json.loads(
        serialization.dumps(relation_rule)
    )
    relation_descriptor = missing_distribution_law["payload"]["descriptor"][
        "payload"
    ]
    relation_descriptor["primitive"] = _nested_wire_value(
        rules.RulePrimitive.DISTRIBUTION
    )
    _assert_rejected(
        _redigest(missing_distribution_law),
        "invalid-descriptor",
    )

    law = rules.ProbabilityLaw(
        rules.ProbabilityPresentation.INTENSIONAL,
        (),
        rules.literal_expr("codec-measure"),
        _certificate(
            rules.CertificateKind.NORMALIZATION,
            "codec-measure-normalized",
        ),
        _certificate(
            rules.CertificateKind.MEASURABILITY,
            "codec-measure-measurable",
        ),
    )
    replay_contract = rules.RuleContract(
        base_rule.contract.configuration_contract,
        base_rule.contract.value_profile,
        base_rule.contract.required_read_shape,
        base_rule.contract.required_join_shape,
        base_rule.contract.required_effect_profile,
        exactness_profile=base_rule.contract.exactness_profile,
        entropy_interface=seeds.EntropyInterface.REPLAY_KEY,
    )
    distribution_rule = rules.distribution(
        rules.literal_expr("codec-distribution"),
        cardinality,
        law,
        contract=replay_contract,
        completeness_evidence=complete,
        soundness_evidence=sound,
    )
    for primitive in (
        rules.RulePrimitive.RELATION,
        rules.RulePrimitive.DIFFERENTIAL,
    ):
        law_on_non_distribution = json.loads(
            serialization.dumps(distribution_rule)
        )
        descriptor = law_on_non_distribution["payload"]["descriptor"][
            "payload"
        ]
        descriptor["primitive"] = _nested_wire_value(primitive)
        _assert_rejected(
            _redigest(law_on_non_distribution),
            "invalid-descriptor",
        )

    finite_law = rules.ProbabilityLaw(
        rules.ProbabilityPresentation.FINITE,
        (rules.AtomMass("codec-atom", Fraction(1)),),
        None,
        _certificate(
            rules.CertificateKind.NORMALIZATION,
            "codec-finite-normalized",
        ),
        _certificate(
            rules.CertificateKind.MEASURABILITY,
            "codec-finite-measurable",
        ),
    )
    finite_distribution_law = json.loads(
        serialization.dumps(distribution_rule)
    )
    distribution_denotation = finite_distribution_law["payload"][
        "descriptor"
    ]["payload"]["denotation"]["payload"]
    distribution_denotation["probability_law"] = _nested_wire_value(
        finite_law
    )
    _assert_rejected(
        _redigest(finite_distribution_law),
        "invalid-descriptor",
    )


def test_hostile_value_anchored_readable_views_fail_closed() -> None:
    source = loci.grid_configuration(
        (3,),
        (False, False, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        axes=("x",),
    )
    anchor = alphabets.ValueAnchor(
        alphabets.value_equals(True),
        alphabets.AnchorCardinality.ZERO_OR_MORE,
    )
    view = neighborhoods.value_relative(
        anchor,
        ((0,),),
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    ).resolve(source)

    wrong_region = json.loads(serialization.dumps(view))
    dependency = wrong_region["payload"]["dependencies"]["payload"]["items"][0]
    dependency["payload"]["region"] = _nested_wire_value(loci.all_support())
    _assert_rejected(_redigest(wrong_region), "invalid-descriptor")

    wrong_join = json.loads(serialization.dumps(view))
    wrong_join["payload"]["join_shape"] = _nested_wire_value(
        neighborhoods.JoinShape(
            neighborhoods.JoinMode.GLOBAL,
            ("value-relative",),
        )
    )
    _assert_rejected(_redigest(wrong_join), "invalid-descriptor")

    realized_source = loci.grid_configuration(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
        axes=("x",),
    )
    realized = neighborhoods.value_relative(
        alphabets.ValueAnchor(alphabets.value_equals(True)),
        ((0,),),
        configuration_contract=realized_source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    ).resolve(realized_source)
    missing_source_anchor = json.loads(serialization.dumps(realized))
    no_anchor = _nested_wire_value(None)
    for observation in (
        missing_source_anchor["payload"]["observations"]["payload"]["items"]
    ):
        observation["payload"]["anchor"] = deepcopy(no_anchor)
    for group in missing_source_anchor["payload"]["groups"]["payload"]["items"]:
        group["payload"]["anchor"] = deepcopy(no_anchor)
        group["payload"]["key"]["payload"]["anchor"] = deepcopy(no_anchor)
    _assert_rejected(
        _redigest(missing_source_anchor),
        "invalid-descriptor",
    )

    multiple_source = loci.grid_configuration(
        (3,),
        (True, False, True),
        boundary=loci.Boundary(loci.BoundaryPolicy.PERIODIC),
        axes=("x",),
    )
    multiple = neighborhoods.value_relative(
        alphabets.ValueAnchor(
            alphabets.value_equals(True),
            alphabets.AnchorCardinality.ONE_OR_MORE,
        ),
        ((0,),),
        configuration_contract=multiple_source.contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    ).resolve(multiple_source)
    false_singleton = json.loads(serialization.dumps(multiple))
    dependency = false_singleton["payload"]["dependencies"]["payload"][
        "items"
    ][0]
    dependency["payload"]["value_anchor"]["payload"]["cardinality"] = (
        _nested_wire_value(alphabets.AnchorCardinality.EXACTLY_ONE)
    )
    _assert_rejected(_redigest(false_singleton), "invalid-descriptor")

    relation = loci.selector_tagged("codec-intensional")
    intensional_contract = loci.CarrierContract(
        loci.CarrierKind.INTENSIONAL
    )
    intensional_source = loci.IntensionalConfiguration(
        intensional_contract,
        relation,
        "codec-intensional-source",
    )
    intensional = neighborhoods.intensional(
        "x",
        relation,
        configuration_contract=intensional_contract,
        value_profile=alphabets.ValueProfile.SYMBOLIC,
        exactness_profile=seeds.ExactnessProfile.SYMBOLIC,
    ).resolve(intensional_source)
    assert type(intensional) is neighborhoods.IntensionalReadableView
    finite_anchor = json.loads(serialization.dumps(intensional))
    finite_anchor["payload"]["dependencies"]["payload"]["items"][0] = (
        _nested_wire_value(multiple.dependencies[0])
    )
    _assert_rejected(_redigest(finite_anchor), "invalid-descriptor")


def test_hostile_readable_group_identity_mutations_fail_closed() -> None:
    source = loci.record_configuration((("a", 1), ("b", 2)))
    first, second = tuple(target for target, _ in source.entries)
    dependency = neighborhoods.ReadDependency(
        "record",
        loci.all_support(),
        None,
        seeds.ExactnessProfile.EXACT,
    )
    observations = (
        neighborhoods.Observation(
            first,
            neighborhoods.Present(1),
            anchor=first,
        ),
        neighborhoods.Observation(
            second,
            neighborhoods.Present(2),
            anchor=first,
        ),
    )
    view = neighborhoods.ReadableView(
        source.identity,
        observations,
        (
            neighborhoods.ObservationGroup(
                neighborhoods.GroupKey(first, 0),
                (0,),
                anchor=first,
            ),
            neighborhoods.ObservationGroup(
                neighborhoods.GroupKey(first, 1),
                (1,),
                anchor=first,
            ),
        ),
        neighborhoods.JoinShape(
            neighborhoods.JoinMode.ANCHOR_IDENTITY,
            ("target", "channel"),
        ),
        (dependency,),
    )

    duplicate_key = json.loads(serialization.dumps(view))
    groups = duplicate_key["payload"]["groups"]["payload"]["items"]
    groups[1]["payload"]["key"] = deepcopy(groups[0]["payload"]["key"])
    _assert_rejected(_redigest(duplicate_key), "invalid-descriptor")

    global_view = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.INTEGER,
    ).resolve(source)
    mismatched_none_anchor = json.loads(serialization.dumps(global_view))
    observations_wire = (
        mismatched_none_anchor["payload"]["observations"]["payload"]["items"]
    )
    observations_wire[1]["payload"]["anchor"] = _nested_wire_value(first)
    _assert_rejected(
        _redigest(mismatched_none_anchor),
        "invalid-descriptor",
    )


def test_catalog_invocation_legacy_dynamics_and_observers_are_not_canonical() -> None:
    """Aliases, observer records, and 0.1 manifests have no codec authority."""

    @dataclass(frozen=True)
    class Observer:
        label: str

    class ForeignEnum(Enum):
        VALUE = "value"

    for value in (
        Observer("view"),
        ForeignEnum.VALUE,
        {"type": "Dynamics", "version": 1, "rule": 30},
        ["eca", 30],
        1.0,
        b"opaque",
    ):
        with pytest.raises(TypeError):
            serialization.dumps(value)

    legacy = {
        "tag": "ca.dynamics",
        "version": 1,
        "payload": {"constructor": "eca", "arguments": {"rule": "30"}},
    }
    legacy["digest"] = (
        "sha256:"
        + sha256(
            _canonical_json(
                {
                    "tag": legacy["tag"],
                    "version": legacy["version"],
                    "payload": legacy["payload"],
                }
            )
        ).hexdigest()
    )
    _assert_rejected(_canonical_json(legacy), "unknown-tag")

    assert ca.serialization is serialization
    assert "serialization" in ca.__all__
    assert not hasattr(ca, "Decoded")
    assert not hasattr(ca, "dumps")

    forged_locus = loci.coordinate("x", 1)
    object.__setattr__(forged_locus, "scope", "")
    with pytest.raises(TypeError):
        serialization.dumps(forged_locus)

    source = loci.record_configuration((("nested", True),))
    nested_locus = source.entries[0][0]
    object.__setattr__(nested_locus, "scope", "")
    with pytest.raises(TypeError):
        serialization.dumps(source)

    forged_descriptor = alphabets.enum((0, False)).descriptor
    object.__setattr__(forged_descriptor, "values", (0, False))
    with pytest.raises(TypeError):
        serialization.dumps(forged_descriptor)

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            """
import importlib.abc
import sys

class BlockCatalog(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "ca.catalog" or fullname.startswith("ca.catalog."):
            raise ImportError("catalog blocked")
        return None

sys.meta_path.insert(0, BlockCatalog())
import ca
value = ca.loci.coordinate("x", 3)
blob = ca.serialization.dumps(value)
decoded = ca.serialization.loads(blob)
assert decoded == ca.serialization.Decoded(value)
assert "ca.catalog" not in sys.modules
""",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
