"""Shared live Goal 7 conformance assertions."""

from typing import TypeVar


T = TypeVar("T")
L = TypeVar("L")
R = TypeVar("R")
Source = TypeVar("Source")


def assert_closed_descriptor(value: T) -> None:
    """Assert recursive closure, versions, exact fields, and local validity."""

    def walk(item: object) -> None:
        assert not callable(item)
        assert not isinstance(item, (dict, list, set, bytearray))
        fields = getattr(item, "__dataclass_fields__", None)
        if fields is not None:
            version = getattr(item, "version", 1)
            assert version == 1
            for name in fields:
                walk(getattr(item, name))
        elif isinstance(item, tuple):
            for child in item:
                walk(child)

    walk(value)


def assert_full_application_equal(left: L, right: R) -> None:
    """Compare every source, applied, quotient, measure, and evidence record."""

    assert left == right


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
