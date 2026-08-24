"""Ordinary Alphabet values and their shared operations."""

from __future__ import annotations


def accepts(alphabet: object, value: object) -> bool:
    """Return whether a membership container or predicate admits one value."""

    if callable(alphabet):
        return bool(alphabet(value))
    try:
        return value in alphabet  # type: ignore[operator]
    except TypeError as error:
        raise TypeError("Alphabet must be a membership container or callable") from error


__all__ = ["accepts"]
