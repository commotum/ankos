#!/usr/bin/env python3
"""Fail-closed primary-source audit for T40 mathematical-constant expansions.

T40's native identity is an immutable exact-number/representation denotation
plus typed coefficient queries.  It is not a fabricated mutable constant or a
mandatory append-prefix transition.  The Book also gives explicit algorithms
(long division, a square-root digit machine, continued-fraction iteration)
whose visible work states may be represented by ordinary SimplePrograms; those
are realizations of the denotation, not hidden executor state or T40's identity.

The Book does not use the catalog label.  Eighteen bounded, redundant query
lanes therefore freeze the strict section, Notes, relations, actual flattened
Index, boundary controls, image interface, and false positives.  The chapter
split is intentionally treated as an abridged summary: two linked plates and
most mechanics are explicit omissions rather than silently invented matches.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("T40 source oracle requires assertions; do not use -O")


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BOOK = SCRIPT_ROOT / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


def line_set(spec: str) -> frozenset[int]:
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Exactly eighteen bounded lanes from the first-principles audit.  Q00 proves
# that the catalog label is external vocabulary; Q15/Q16 close all 24 images.
QUERIES = {
    "Q00": r"Mathematical-Constant Digit Systems?",
    "Q01": r"Mathematical Constants",
    "Q02": (
        r"first 4000 digits|first 20,000 digits|two hundred billion digits|"
        r"circumference.{0,100}diameter"
    ),
    "Q03": (
        r"digit sequences for various rational|number of the form p/q|"
        r"standard long division|remainder at each of the steps"
    ),
    "Q04": (
        r"procedure for generating.{0,80}square roots|two numbers r and s|"
        r"s\^2 \+ 4r"
    ),
    "Q05": (
        r"cube roots.{0,80}fourth roots|logarithms and exponentials|"
        r"only kinds of numbers that have repetitive"
    ),
    "Q06": (
        r"representation for a number|procedures for building up|"
        r"continued fraction representations?"
    ),
    "Q07": (
        r"Computing.{0,40}digits directly|PowerMod\[2|Simon Plouffe|"
        r"values of \*?PolyLog\*?"
    ),
    "Q08": (
        r"Digit sequence properties|normal in a particular base|"
        r"statistical tests of randomness|Stoneham"
    ),
    "Q09": (
        r"Nested digit sequences|Concatenation sequences|Runs of digits|"
        r"Leading digits"
    ),
    "Q10": (
        r"Page 143.{0,20}Continued fractions|Khinchin|Hurwitz numbers|"
        r"Jeffrey Shallit"
    ),
    "Q11": (
        r"Floor\[NestList\[1/Mod|FromContinuedFraction|Euclid.s algorithm|"
        r"Egyptian fractions|Nested radicals|Digital slope representation"
    ),
    "Q12": (
        r"continued fraction map|Iterated division|compare page 153|"
        r"continued fraction.{0,120}substitution"
    ),
    "Q13": (
        r"noncomputable.{0,80}digit|Chaitin.{0,120}digit|"
        r"digits of.{0,40}sqrt.{0,120}cellular automata|"
        r"digit sequence.{0,100}data compression"
    ),
    "Q14": (
        r"Mathematical constants, 136-144|Continued fractions, 143, 914|"
        r"Digit sequences, 116-127, 136-142|Number representations, 142|"
        r"Normal numbers, 912|Rational numbers approximation by|"
        r"Plouffe, Simon|Khinchin \(Khinchin.s constant\)"
    ),
    "Q15": r"_page_(?:151_Figure_7|154_Figure_2|156_Figure_1)\.jpeg",
    "Q16": (
        r"_page_(?:927_Figure_14|928_Figure_(?:9|11|13|22)|"
        r"929_Picture_1[1-6]|930_(?:Picture_(?:4|12|14)|Figure_10)|"
        r"931_Figure_(?:9|10|11|12|13|17))\.jpeg"
    ),
    "Q17": (
        r"^#### (?:\*\*)?(?:The Sequence of Primes|Mathematical Functions)"
        r"(?:\*\*)?$"
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(
        ",".join(map(str, sorted(values))).encode("ascii")
    ).hexdigest()


def digest_records(records: set[str] | list[str] | tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_book(argument: str | None) -> tuple[Path, Path, Path]:
    if argument is not None:
        book = Path(argument).resolve()
    elif DEFAULT_BOOK.is_file():
        book = DEFAULT_BOOK.resolve()
    else:
        candidate = (
            Path.cwd() / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
        ).resolve()
        if not candidate.is_file():
            raise FileNotFoundError("cannot locate default A New Kind of Science source")
        book = candidate
    return book, book.parent, book.parents[2]


if __name__ == "__main__":
    raise SystemExit("T40 source oracle construction incomplete")
