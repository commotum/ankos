"""Canonical, fail-closed serialization for expanded semantic values.

This module owns versioned codecs and typed decode results for the closed
values defined by the semantic owner modules. It consumes expanded programs,
components, results, evidence, and traces without owning catalog lookup,
constructor invocation history, execution dispatch, compatibility fallback,
or a sixth program field.

The declarations below are an inert Goal 7 scaffold. They establish the
canonical program envelope and public decode boundary, while every encoding,
decoding, validation, digest, and lossless migration operation remains
uniformly unimplemented.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, NoReturn, TypeAlias, TypeVar

from . import alphabets, frontiers, neighborhoods, program, rules, seeds


T = TypeVar("T")
C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")

_PROGRAM_SCHEMA_TAG = "ca.simple-program"
_PROGRAM_SCHEMA_VERSION = 1


def _not_implemented() -> NoReturn:
    """Raise the standard error for unfinished Goal 7 codec behavior."""

    raise NotImplementedError("Goal 7 serialization scaffold is not implemented")


# ---------------------------------------------------------------------------
# Phase 1: Canonical Envelope and Decode Result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ProgramPayload(Generic[C, V, W, R]):
    """Expanded canonical payload with exactly the five program fields."""

    seed: seeds.Seed[C]
    alphabet: alphabets.Alphabet[V]
    frontier: frontiers.WritableRegion[C, W]
    neighborhood: neighborhoods.ReadableRegion[C, R]
    rule: rules.Rule[R, W, C]


@dataclass(frozen=True)
class DecodeFault:
    """Closed reason that canonical decoding could not produce a value."""

    phase: str
    reason: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class DecodeRejected:
    """Fail-closed decode result with no partially restored value."""

    fault: DecodeFault


@dataclass(frozen=True)
class Decoded(Generic[T]):
    """Successfully decoded and validated semantic value."""

    value: T


DecodeResult: TypeAlias = Decoded[T] | DecodeRejected


# ---------------------------------------------------------------------------
# Phase 2: Canonical Codec Surface
# ---------------------------------------------------------------------------


def dumps(value: T) -> bytes:
    """Encode one validated public semantic value canonically."""

    _not_implemented()


def loads(data: bytes) -> DecodeResult[T]:
    """Decode one canonical value or return a typed rejection."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Phase 3: Versioned Nodes and Lossless Migrations
# ---------------------------------------------------------------------------

# Owner-specific codecs, canonical ordering, exact number handling, derived
# digests, forged-envelope rejection, and total validated lossless migrations
# land here in G7-03. No catalog or 0.1 Dynamics fallback belongs here.


__all__ = [
    "DecodeFault",
    "DecodeRejected",
    "DecodeResult",
    "Decoded",
    "dumps",
    "loads",
]
