"""Shared runtime conformance assertions."""

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
from typing import TypeVar

import ca


T = TypeVar("T")
Source = TypeVar("Source")


def assert_closed_descriptor(value: T) -> None:
    """Assert recursive closure and the complete five-field descriptor contract."""

    def walk(item: object) -> None:
        assert not callable(item)
        assert not isinstance(item, (dict, list, set, bytearray))
        if isinstance(item, Enum):
            assert item in type(item)
        elif is_dataclass(item) and not isinstance(item, type):
            declared = tuple(field.name for field in fields(item))
            assert declared == tuple(item.__dataclass_fields__)
            stored = getattr(item, "__dict__", None)
            if stored is not None:
                assert set(stored) == set(declared)
            if "version" in declared:
                assert type(getattr(item, "version")) is int
                assert getattr(item, "version") == 1
            for name in declared:
                walk(getattr(item, name))
        elif isinstance(item, tuple):
            for child in item:
                walk(child)
        else:
            assert type(item) in (
                type(None),
                bool,
                int,
                Fraction,
                str,
                bytes,
            )

    walk(value)
    if type(value) is ca.program.SimpleProgram:
        assert tuple(field.name for field in fields(value)) == (
            "seed",
            "alphabet",
            "frontier",
            "neighborhood",
            "rule",
        )
        assert value.seed.version == 1
        assert value.alphabet.descriptor.version == 1
        assert value.frontier.version == 1
        assert value.neighborhood.version == 1
        assert value.rule.descriptor.version == 1
        assert value.rule.contract.version == 1
        assert (
            value.seed.exactness_profile
            is value.frontier.exactness_profile
            is value.neighborhood.exactness_profile
            is value.rule.contract.exactness_profile
        )
        assert isinstance(
            value.seed.entropy_interface,
            ca.seeds.EntropyInterface,
        )
        assert isinstance(
            value.rule.contract.entropy_interface,
            ca.seeds.EntropyInterface,
        )
        assert not hasattr(value.seed, "rng")
        blob = ca.serialization.dumps(value)
        decoded = ca.serialization.loads(blob)
        assert decoded == ca.serialization.Decoded(value)
        assert ca.serialization.dumps(decoded.value) == blob


def assert_no_authoritative_commit(
    result: T,
    original: Source,
    expected_identity: str,
) -> None:
    """Assert rejection left the input unchanged and exposed no successor."""

    assert result.__class__.__name__ == "ApplicationRejected"
    assert not hasattr(result, "applied_atoms")
    assert not hasattr(result, "successor_quotient_with_derivation_fibers")
    assert getattr(original, "identity") == expected_identity
