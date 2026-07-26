"""CT09: exhaustive, canonical, fail-closed semantic serialization."""

from __future__ import annotations

from dataclasses import fields, is_dataclass, replace
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import json
from typing import Callable

import pytest

from ca import alphabets, loci, program, rules, serialization

from g7_codec_samples import public_sealed_types, representative_values


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _resign(envelope: dict[str, object]) -> bytes:
    core = {
        "tag": envelope["tag"],
        "version": envelope["version"],
        "payload": envelope["payload"],
    }
    changed = dict(envelope)
    changed["digest"] = "sha256:" + sha256(_canonical_json(core)).hexdigest()
    return _canonical_json(changed)


def _envelope(
    tag: str,
    payload: dict[str, object],
    *,
    version: object = 1,
) -> bytes:
    return _resign(
        {
            "tag": tag,
            "version": version,
            "payload": payload,
            "digest": "",
        }
    )


def _parsed(value: object) -> dict[str, object]:
    parsed = json.loads(serialization.dumps(value))
    assert type(parsed) is dict
    return parsed


def _rejected(blob: object) -> serialization.DecodeRejected:
    result = serialization.loads(blob)  # type: ignore[arg-type]
    assert isinstance(result, serialization.DecodeRejected)
    assert type(result) is serialization.DecodeRejected
    assert type(result.fault) is serialization.DecodeFault
    assert not hasattr(result, "value")
    assert result.fault.phase
    assert result.fault.reason
    assert type(result.fault.evidence) is tuple
    return result


def _decoded(value: object) -> object:
    blob = serialization.dumps(value)
    result = serialization.loads(blob)
    assert isinstance(result, serialization.Decoded)
    assert type(result) is serialization.Decoded
    assert type(result.value) is type(value)
    assert serialization.dumps(result.value) == blob
    return result.value


def _assert_semantically_equal(left: object, right: object) -> None:
    assert type(left) is type(right)
    if isinstance(
        left,
        (loci.FiniteConfiguration, loci.IntensionalConfiguration),
    ):
        assert loci.configuration_equal(left, right)
    elif isinstance(
        left,
        (
            alphabets.AlgebraicNumber,
            alphabets.ExactComplex,
            alphabets.StructuralReference,
            alphabets.ValueNode,
            alphabets.RepresentedNumber,
        ),
    ):
        assert alphabets.semantic_equal(left, right)
    elif isinstance(left, (loci.Locus, loci.FreshReference)):
        assert loci.canonical_identity(left) == loci.canonical_identity(right)
    else:
        assert left == right


def _mutate(
    value: object,
    mutation: Callable[[dict[str, object]], None],
    *,
    resign: bool = True,
) -> bytes:
    envelope = _parsed(value)
    mutation(envelope)
    return _resign(envelope) if resign else _canonical_json(envelope)


def _payload(envelope: dict[str, object]) -> dict[str, object]:
    payload = envelope["payload"]
    assert type(payload) is dict
    return payload


def _node_payload(node: object) -> dict[str, object]:
    assert type(node) is dict
    payload = node["payload"]
    assert type(payload) is dict
    return payload


def test_every_public_semantic_value_round_trips_and_reencodes_identically() -> None:
    """One record per owner type and every enum member cross the real boundary."""

    values = representative_values()
    sealed_types = public_sealed_types()

    assert len(values) == 441
    assert len(sealed_types) == 187
    assert {type(value) for value in values} == set(sealed_types)
    assert sum(isinstance(value, Enum) for value in values) == 300
    assert sum(not isinstance(value, Enum) for value in values) == 141

    for value in values:
        decoded = _decoded(value)
        _assert_semantically_equal(value, decoded)


def test_every_semantic_record_version_is_exact_integer_one() -> None:
    """Boolean and rational lookalikes cannot masquerade as schema version 1."""

    versioned = tuple(
        value
        for value in representative_values()
        if is_dataclass(value)
        and any(field.name == "version" for field in fields(value))
    )
    assert len(versioned) == 64

    for value in versioned:
        canonical = serialization.dumps(value)
        for invalid in (True, Fraction(1, 1)):
            with pytest.raises((TypeError, ValueError)):
                replace(value, version=invalid)
            object.__setattr__(value, "version", invalid)
            with pytest.raises(TypeError):
                serialization.dumps(value)
            object.__setattr__(value, "version", 1)
        assert serialization.dumps(value) == canonical


def test_program_payload_has_exactly_five_expanded_field_keys() -> None:
    """Program identity contains expanded components and no catalog receipt."""

    simple_program = next(
        value
        for value in representative_values()
        if type(value) is program.SimpleProgram
    )
    blob = serialization.dumps(simple_program)
    envelope = json.loads(blob)

    assert tuple(sorted(envelope)) == (
        "digest",
        "payload",
        "tag",
        "version",
    )
    assert envelope["tag"] == "ca.simple-program"
    assert envelope["version"] == 1
    assert set(envelope["payload"]) == {
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    }
    assert tuple(field.name for field in fields(simple_program)) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert all(
        set(node) == {"tag", "version", "payload"}
        for node in envelope["payload"].values()
    )
    def object_keys(value: object) -> set[str]:
        if type(value) is dict:
            return set(value).union(
                *(object_keys(item) for item in value.values())
            )
        if type(value) is list:
            return set().union(*(object_keys(item) for item in value))
        return set()

    # ``arguments`` is intentionally a semantic field of several closed ASTs;
    # reject receipt metadata by its structural keys, not by substrings in
    # legitimate evidence text.
    assert object_keys(envelope).isdisjoint(
        {
            "catalog",
            "catalog_id",
            "constructor",
            "constructor_name",
            "invocation",
            "alias",
            "recipe",
            "spf",
            "family_id",
            "source_citation",
            "update_policy",
            "callback",
            "python_module",
            "python_class",
        }
    )
    _assert_semantically_equal(simple_program, _decoded(simple_program))


def test_round_trip_preserves_every_exact_semantic_distinction() -> None:
    """Exact scalars and semantically distinct closed variants never collapse."""

    sqrt_two = alphabets.AlgebraicNumber(
        (1, 0, -2),
        (Fraction(1), Fraction(2)),
    )
    exact_values = (
        None,
        False,
        True,
        0,
        1,
        -1,
        10**5000 + 7,
        -(10**5000 + 7),
        "",
        "é/λ/𐐷",
        "\ud800",
        Fraction(0),
        Fraction(-17, 19),
        (False, 0, Fraction(1, 2), "0"),
        sqrt_two,
        alphabets.ExactComplex(sqrt_two, Fraction(-1, 3)),
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.DECIMAL,
            "0.5",
        ),
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.FIXED_POINT,
            Fraction(1, 2),
        ),
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.IEEE754_BINARY32,
            0x3F000000,
        ),
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.IEEE754_BINARY64,
            0x3FE0000000000000,
        ),
        alphabets.RepresentedNumber(
            alphabets.RepresentedNumberProfile.INTERVAL,
            (Fraction(1, 3), Fraction(2, 3)),
        ),
        alphabets.StructuralReference(loci.named("same-spelling")),
        alphabets.StructuralReference(
            loci.fresh_reference("same-spelling", "same-spelling")
        ),
        rules.NoPayload(),
        rules.ValuePayload(False),
    )

    encoded = tuple(serialization.dumps(value) for value in exact_values)
    assert len(encoded) == len(set(encoded))
    for value, blob in zip(exact_values, encoded, strict=True):
        result = serialization.loads(blob)
        assert isinstance(result, serialization.Decoded)
        _assert_semantically_equal(value, result.value)
        assert serialization.dumps(result.value) == blob

    # Decimal text is representation, not an implicit float or rational.
    represented = next(
        value
        for value in exact_values
        if isinstance(value, alphabets.RepresentedNumber)
        and value.profile is alphabets.RepresentedNumberProfile.DECIMAL
    )
    decoded_represented = _decoded(represented)
    assert isinstance(decoded_represented, alphabets.RepresentedNumber)
    assert decoded_represented.profile is (
        alphabets.RepresentedNumberProfile.DECIMAL
    )
    assert decoded_represented.representation == "0.5"

    # Cardinality variants retain evidence and do not collapse to bare sizes.
    certificate = rules.Certificate(
        rules.CertificateKind.CARDINALITY,
        rules.literal_expr("codec-cardinality"),
    )
    cardinalities = (
        rules.ExactlyZero(certificate),
        rules.ExactlyOne(certificate),
        rules.Many(2, None, certificate),
        rules.Many(
            None,
            rules.InfiniteCardinality.COUNTABLY_INFINITE,
            certificate,
        ),
        rules.Many(
            None,
            rules.InfiniteCardinality.UNCOUNTABLE,
            certificate,
        ),
        rules.Undetermined(
            rules.literal_expr("unknown"),
            certificate,
        ),
    )
    assert len(
        {serialization.dumps(value) for value in cardinalities}
    ) == len(cardinalities)
    for value in cardinalities:
        assert _decoded(value) == value


def test_hostile_envelopes_and_nodes_reject_without_partial_values() -> None:
    locus = loci.named("codec-hostile")
    valid = _parsed(locus)

    missing_root = dict(valid)
    missing_root.pop("payload")
    extra_root = dict(valid)
    extra_root["catalog"] = "eca"
    invalid_digest = dict(valid)
    invalid_digest["digest"] = "sha256:XYZ"
    forged = dict(valid)
    _payload(forged)["scope"] = {
        "tag": "ca.scalar.string",
        "version": 1,
        "payload": {"value": "forged"},
    }

    noncanonical = json.dumps(
        valid,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=False,
    ).encode("utf-8")
    duplicate_root = serialization.dumps(locus).decode("utf-8").replace(
        '{"digest":',
        '{"digest":"sha256:' + ("0" * 64) + '","digest":',
        1,
    ).encode("utf-8")

    scope = _payload(valid)["scope"]
    assert type(scope) is dict
    payload_items = dict(_payload(valid))
    nested = _canonical_json(scope).decode("utf-8")
    payload_text = _canonical_json(payload_items).decode("utf-8")
    duplicate_payload = (
        '{"scope":'
        + nested
        + ","
        + payload_text[1:]
    )
    duplicate_nested = (
        '{"digest":'
        + json.dumps(valid["digest"])
        + ',"payload":'
        + duplicate_payload
        + ',"tag":'
        + json.dumps(valid["tag"])
        + ',"version":1}'
    ).encode("utf-8")

    hostile = (
        b"\xff\xfe\x80",
        b"",
        b"{",
        b"[]",
        b"\xef\xbb\xbf{}",
        bytearray(serialization.dumps(locus)),
        missing_root,
        extra_root,
        invalid_digest,
        forged,
        noncanonical,
        duplicate_root,
        duplicate_nested,
    )
    for item in hostile:
        blob: object
        if type(item) is dict:
            blob = _canonical_json(item)
        else:
            blob = item
        _rejected(blob)


@pytest.mark.parametrize(
    ("blob", "reason"),
    (
        (
            _envelope("ca.unknown.owner", {}),
            "unknown-tag",
        ),
        (
            _envelope("ca.scalar.float", {"value": "1.0"}),
            "unknown-primitive",
        ),
        (
            _envelope("ca.scalar.none", {"value": None}),
            "extra-field",
        ),
        (
            _envelope("ca.scalar.boolean", {"value": 1}),
            "invalid-boolean",
        ),
        (
            _envelope("ca.scalar.integer", {"value": "01"}),
            "noncanonical-integer",
        ),
        (
            _envelope("ca.scalar.integer", {"value": "-0"}),
            "noncanonical-integer",
        ),
        (
            _envelope(
                "ca.scalar.rational",
                {"numerator": "2", "denominator": "4"},
            ),
            "noncanonical-rational",
        ),
        (
            _envelope(
                "ca.scalar.rational",
                {"numerator": "1", "denominator": "0"},
            ),
            "noncanonical-rational",
        ),
        (
            _envelope("ca.scalar.string", {"value": False}),
            "invalid-string",
        ),
        (
            _envelope("ca.tuple", {"items": {}}),
            "invalid-tuple",
        ),
        (
            _envelope(
                "ca.loci.locus-kind",
                {"value": "future-locus-kind"},
            ),
            "unknown-enum-value",
        ),
        (
            _envelope(
                "ca.loci.locus-kind",
                {"value": "named"},
                version=0,
            ),
            "unknown-version",
        ),
        (
            _envelope(
                "ca.loci.locus-kind",
                {"value": "named"},
                version=2,
            ),
            "unknown-version",
        ),
        (
            _envelope(
                "ca.loci.locus-kind",
                {"value": "named"},
                version="1",
            ),
            "invalid-version",
        ),
    ),
)
def test_unknown_versions_primitives_enums_and_noncanonical_scalars_reject(
    blob: bytes,
    reason: str,
) -> None:
    assert _rejected(blob).fault.reason == reason


def test_missing_extra_nested_version_and_invalid_descriptors_reject() -> None:
    locus = loci.named("codec-nested")

    def missing_scope(envelope: dict[str, object]) -> None:
        _payload(envelope).pop("scope")

    def extra_scope(envelope: dict[str, object]) -> None:
        _payload(envelope)["constructor"] = _parsed("named")

    def nested_version(envelope: dict[str, object]) -> None:
        scope = _payload(envelope)["scope"]
        assert type(scope) is dict
        scope["version"] = 2

    def invalid_scope(envelope: dict[str, object]) -> None:
        scope = _payload(envelope)["scope"]
        _node_payload(scope)["value"] = ""

    cases = (
        (_mutate(locus, missing_scope), "missing-field"),
        (_mutate(locus, extra_scope), "extra-field"),
        (_mutate(locus, nested_version), "unknown-version"),
        (_mutate(locus, invalid_scope), "invalid-descriptor"),
    )
    for blob, reason in cases:
        assert _rejected(blob).fault.reason == reason


def test_forged_digest_and_noncanonical_bytes_reject() -> None:
    value = (10**1000, Fraction(-5, 7), "canonical")
    canonical = serialization.dumps(value)
    envelope = json.loads(canonical)

    forged = dict(envelope)
    forged["digest"] = "sha256:" + ("0" * 64)
    assert _rejected(_canonical_json(forged)).fault.reason == "forged-digest"

    pretty = json.dumps(
        envelope,
        ensure_ascii=False,
        allow_nan=False,
        indent=1,
        sort_keys=True,
    ).encode("utf-8")
    assert _rejected(pretty).fault.reason == "noncanonical-encoding"

    reordered = (
        b'{"tag":'
        + _canonical_json(envelope["tag"])
        + b',"version":1,"payload":'
        + _canonical_json(envelope["payload"])
        + b',"digest":'
        + _canonical_json(envelope["digest"])
        + b"}"
    )
    assert _rejected(reordered).fault.reason == "noncanonical-encoding"


@pytest.mark.parametrize(
    "value",
    (
        0.0,
        [],
        {},
        object(),
        lambda: None,
    ),
)
def test_unsupported_encode_values_have_no_lossy_fallback(value: object) -> None:
    with pytest.raises(TypeError):
        serialization.dumps(value)


def test_program_mutations_do_not_default_or_admit_a_sixth_field() -> None:
    simple_program = next(
        value
        for value in representative_values()
        if type(value) is program.SimpleProgram
    )
    five = ("seed", "alphabet", "frontier", "neighborhood", "rule")

    for field in five:
        def remove(
            envelope: dict[str, object],
            field: str = field,
        ) -> None:
            _payload(envelope).pop(field)

        assert _rejected(
            _mutate(simple_program, remove)
        ).fault.reason == "missing-field"

    for field in (
        "update_policy",
        "catalog",
        "constructor",
        "arguments",
        "alias",
        "observer",
    ):
        def add(
            envelope: dict[str, object],
            field: str = field,
        ) -> None:
            _payload(envelope)[field] = _parsed(None)

        assert _rejected(
            _mutate(simple_program, add)
        ).fault.reason == "extra-field"


def test_context_validated_records_cannot_cross_the_codec_alone_invalid() -> None:
    """Registered sum/evidence records retain their owner-level invariants."""

    compatibility = next(
        value
        for value in representative_values()
        if type(value) is program.CompatibilityEvidence
    )
    with pytest.raises(TypeError, match="semantic alphabet value"):
        rules.ValuePayload(rules.NoPayload())
    with pytest.raises(ValueError, match="canonical proof"):
        program.CompatibilityEvidence(
            compatibility.configuration_contract,
            compatibility.value_profile,
            (1,),  # type: ignore[arg-type]
        )

    no_payload = _parsed(rules.NoPayload())
    no_payload.pop("digest")

    def invalid_value_payload(envelope: dict[str, object]) -> None:
        _payload(envelope)["value"] = no_payload

    bad_value_payload = _mutate(
        rules.ValuePayload(False),
        invalid_value_payload,
    )
    assert _rejected(bad_value_payload).fault.reason == "invalid-descriptor"

    integer = _parsed(1)
    integer.pop("digest")

    def invalid_compatibility(envelope: dict[str, object]) -> None:
        clauses = _payload(envelope)["clauses"]
        _node_payload(clauses)["items"] = [integer]

    bad_compatibility = _mutate(
        compatibility,
        invalid_compatibility,
    )
    assert _rejected(bad_compatibility).fault.reason == "invalid-descriptor"


def test_legacy_dynamics_manifest_is_not_a_canonical_program() -> None:
    """There is no version-zero, alias, recipe, or compatibility fallback."""

    legacy_and_recipes = (
        b'{"version":"0.1","class":"Dynamics","rule":30}',
        _envelope(
            "ca.dynamics",
            {
                "initial_condition": _parsed(None),
                "update_function": _parsed("eca-30"),
            },
        ),
        _envelope(
            "ca.catalog.eca",
            {
                "constructor": _parsed("eca"),
                "arguments": _parsed((("rule", 30),)),
            },
        ),
        _envelope(
            "ca.simple-program",
            {
                "constructor": _parsed("eca"),
                "arguments": _parsed((("rule", 30),)),
            },
        ),
        _envelope(
            "ca.simple-program",
            {
                "alias": _parsed("elementary-cellular-automaton"),
                "rule": _parsed(30),
            },
        ),
    )
    for blob in legacy_and_recipes:
        _rejected(blob)
