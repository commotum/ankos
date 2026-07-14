#!/usr/bin/env python3
"""Frozen primary-source audit for T28 contextual two-dimensional substitution.

This is an evidence oracle, not a substitution-system implementation.  It
freezes a deliberately redundant vocabulary over the canonical monolithic
Book, dispositions every candidate returned by that vocabulary, follows
governed continuations and source-linked images, checks actual-Index routes,
and reverse-joins the split corpus.

The source supports a grid-aligned, snapshot-parallel contextual patch
replacement: a 2 x 2 neighborhood selects a replacement patch and the patches
are assembled with ``Flatten2D``.  The displayed native preset exists only as
a raster; the Notes give an example row and the step expression, but no
machine-readable complete rule table or seed.  This oracle therefore freezes
the construction while refusing to invent an executable preset from pixels.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T28 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"
NATIVE_RASTER = (
    SOURCE_ROOT
    / "CHAPTERS/5-Two-Dimensions-and-Beyond/Images/_page_207_Figure_1.jpeg"
)

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"
EXPECTED_NATIVE_RASTER_SHA256 = "e7f0112ebc4a6b4276bffeaccc043855335527d38e638c2ed37c428451d57b1c"


# Each lane has a distinct purpose.  Direct names and mechanics find the
# construction; aliases and absent modern spellings guard vocabulary drift;
# executable symbols and Notes phrases bind the only textual rule schema;
# sibling lanes preserve the T14/T26/T27/T29/T31 boundaries; page and Index
# lanes follow the Book's own routes.  Broad words occur only with local
# construction context, so this is a closed audit of this frozen vocabulary,
# not a claim to have searched every imaginable paraphrase.
QUERIES = {
    "Q00": r"\bneighbor(?:[\s-]*)dependent(?:[\s-]+)substitution systems?\b",
    "Q01": (
        r"\btwo[- ]dimensional neighbor[- ]dependent substitution systems?\b|"
        r"\bneighbor[- ]dependent two[- ]dimensional substitution systems?\b|"
        r"\b2D neighbor[- ]dependent substitution systems?\b|"
        r"\bneighbor[- ]dependent 2D\b"
    ),
    "Q02": (
        r"\binteraction between different elements\b|"
        r"\breplacement for a particular element[^.]{0,220}\bneighboring elements\b|"
        r"\bsets up elements on a grid[^.]{0,220}\breplacements?[^.]{0,120}\bdepend on its neighbors\b|"
        r"\breplacements? for a given element[^.]{0,160}\bdepend on its neighbors\b"
    ),
    "Q03": (
        r"Flatten2D\[Partition\[list, \{2, 2\}, 1, -1\] /\. rule\]|"
        r"\\\{\\\{-, 1\\\}, \\\{0, 1\\\}\\\} \\rightarrow \\\{\\\{1, 0\\\}, \\\{1, 1\\\}\\\}|"
        r"\barbitrarily large set of different possible neighborhood configurations\b"
    ),
    "Q04": (
        r"\bwrap around in both (?:of )?its dimensions\b|"
        r"\bneighbor[- ]dependent substitution systems?[^.]{0,180}\b(?:wrap|cyclic boundary)\b|"
        r"\b(?:wrap|cyclic boundary)[^.]{0,180}\bneighbor[- ]dependent substitution systems?\b"
    ),
    "Q05": r"\bPage 192\b|\bpage 935\b|\b187[–-]192\b",
    "Q06": (
        r"\bimmediately to its right\b|"
        r"\brightmost element is always dropped\b|"
        r"\bSS2EvolveList\b|"
        r"Partition\[#, 2, 1\] /\. rule"
    ),
    "Q07": (
        r"\btwo-dimensional substitution systems?\b|"
        r"\b2D substitution systems?\b|"
        r"\bsubstitution systems? in two dimensions\b"
    ),
    "Q08": (
        r"\bgeometrical replacement rules?\b|"
        r"\bdifficult to define an obvious notion of neighbors\b|"
        r"\bsquares produced to overlap\b"
    ),
    "Q09": (
        r"\bnetwork systems?[^.]{0,200}\b(?:local structure|underlying grid)\b|"
        r"\b(?:local structure|underlying grid)[^.]{0,200}\bnetwork systems?\b"
    ),
    "Q10": (
        r"^#### \*\*Systems Based on Constraints\*\*$|"
        r"\bform is defined by the constraint that every cell should have at least one neighbor\b|"
        r"\btwo-dimensional systems based on constraints\b"
    ),
    "Q11": (
        r"\bgeneralizes? to neighbor[- ]dependent substitution systems?[^.]{0,160}\bemulate cellular automata\b|"
        r"\bneighbor[- ]dependent substitution systems? that emulate cellular automata\b|"
        r"\bhighly uniform rules always yielding just one cell\b"
    ),
    "Q12": (
        r"\bcontext(?:ual|[- ](?:dependent|sensitive)) two[- ]dimensional substitution systems?\b|"
        r"\btwo[- ]dimensional context(?:ual|[- ](?:dependent|sensitive)) substitution systems?\b|"
        r"\b(?:tile|block|array) substitution systems?\b|"
        r"\bpicture grammars?\b"
    ),
    "Q13": (
        r"\bcontext[^.]{0,120}\bsubstitution systems?\b|"
        r"\bsubstitution systems?[^.]{0,120}\bcontext\b"
    ),
    "Q14": (
        r"\bno immediate way to generalize sequential substitution systems to two or more dimensions\b|"
        r"\bon a two-dimensional grid[^.]{0,220}\bscan all the elements\b"
    ),
    "Q15": (
        r"\bSubstitution systems, 82[–-]87 2D[.,] 187[–-]192\b|"
        r"\bTwo-dimensional cellular automata[^.]{0,180}\bsubstitution systems, 187[–-]192\b|"
        r"\bneighbor-dependent 2D, 192, 935\b"
    ),
    "Q16": r"_page_20[67]_(?:Picture_1|Figure_1)\.jpeg",
    "Q17": r"\bPage 192 · Neighbor-dependent substitution systems\b",
    "Q18": r"\b1L systems, 85[–-]88\b|\bD1L systems, 85[–-]87\b",
    "Q19": (
        r"\b(?:padding|padded with (?:a )?blank|special boundary symbol)\b[^.]{0,180}\bsubstitution systems?\b|"
        r"\bsubstitution systems?\b[^.]{0,180}\b(?:padding|padded with (?:a )?blank|special boundary symbol)\b"
    ),
    "Q20": (
        r"\bfixed underlying geometrical structure which remains unchanged\b|"
        r"\bnetwork system is fundamentally just a collection of nodes\b|"
        r"\brules that specify how these connections should change from one step to the next\b"
    ),
    "Q21": (
        r"\bexplicit rules that specify how the system evolves from step to step\b|"
        r"\binstead of having explicit rules for evolution[^.]{0,180}\bconstraints to satisfy\b|"
        r"\bknowing only this constraint gives no explicit procedure\b"
    ),
    "Q22": (
        r"\bwhat about two dimensions\? The proof for one dimension breaks down\b|"
        r"\bas a first example of a two-dimensional system, consider an array\b|"
        r"\ba system consisting of a grid of black and white cells defined by the constraint\b"
    ),
    "Q23": (
        r"\bA two-dimensional neighbor-dependent substitution system\b|"
        r"\bgrid of cells is assumed to wrap around in both its dimensions\b|"
        r"\bPatterns generated by 8 steps of evolution in various two-dimensional neighbor-dependent substitution systems\b"
    ),
    "Q24": (
        r"\bPage 187 · Two-dimensional substitution systems\b|"
        r"\bPage 192 · Space-filling curves\b|"
        r"\bSubstitution Systems and Fractals\b"
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 39-T28-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
        and sha256(NATIVE_RASTER) == EXPECTED_NATIVE_RASTER_SHA256
    )
    print("source", "OK" if source_ok else "MISMATCH")
    for name, pattern in QUERIES.items():
        found = {
            line_no
            for line_no, line in enumerate(lines, 1)
            if re.search(pattern, line, re.IGNORECASE)
        }
        print(
            name,
            len(found),
            sum(line_no < INDEX_FIRST_LINE for line_no in found),
            sum(line_no >= INDEX_FIRST_LINE for line_no in found),
            digest(found),
            ",".join(map(str, sorted(found))),
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
