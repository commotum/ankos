"""Unit contract for canonical, catalog-free semantic serialization."""

from __future__ import annotations

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
    assert len(schemas) == 178
    assert sum(
        len(row.enum_values) if row.enum_values else 1 for row in schemas
    ) == 387
    assert len({row.tag for row in schemas}) == 178
    assert len({row.value_type for row in schemas}) == 178

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
