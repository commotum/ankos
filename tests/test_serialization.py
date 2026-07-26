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
    index = rules.literal_expr(0)
    default = rules.literal_expr("default")
    value = rules.literal_expr("value")
    table = rules.literal_expr("table")
    return (
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
    )


def test_new_rule_expression_primitives_round_trip_in_exact_enum_order() -> None:
    """Every reopened mechanics node uses the existing closed RuleExpr codec."""

    samples = _new_rule_expression_samples()
    new_primitives = (
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
    )

    assert len(samples) == 21
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
