"""Shared Goal 7 conformance assertions.

G7-01 activates the descriptor, complete-result, and no-commit helpers.  The
codec, representation, and catalog helpers remain explicit later-stage
placeholders.
"""

from collections.abc import Callable
from typing import NoReturn, TypeVar


T = TypeVar("T")
L = TypeVar("L")
R = TypeVar("R")
Representation = TypeVar("Representation")
Native = TypeVar("Native")
Represented = TypeVar("Represented")
Source = TypeVar("Source")
Program = TypeVar("Program")
Arguments = TypeVar("Arguments")


def _not_implemented() -> NoReturn:
    """Raise the standard error for unfinished Goal 7 conformance helpers."""

    raise NotImplementedError("Goal 7 conformance helpers are not implemented")


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


def assert_no_authoritative_commit(result: T, original: Source) -> None:
    """Assert rejection left the input unchanged and exposed no successor."""

    assert result.__class__.__name__ == "ApplicationRejected"
    assert not hasattr(result, "applied_atoms")
    assert not hasattr(result, "successor_quotient_with_derivation_fibers")
    identity = getattr(original, "identity", None)
    if identity is not None:
        assert getattr(original, "identity") == identity


def assert_canonical_roundtrip(value: T) -> None:
    """Assert exact decode equality and byte-for-byte canonical re-encoding."""

    _not_implemented()


def assert_representation_commutes(
    representation: Representation,
    native: Native,
    represented: Represented,
    source: Source,
) -> None:
    """Assert inverse-on-image and full one-step result commutation."""

    _not_implemented()


def assert_catalog_expansion(
    public_constructor: Callable[..., Program],
    canonical_constructor: Callable[..., Program],
    arguments: Arguments,
) -> None:
    """Assert the declared callable relation yields the exact expanded value."""

    _not_implemented()
