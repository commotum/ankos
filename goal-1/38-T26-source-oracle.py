#!/usr/bin/env python3
"""Frozen primary-source audit for T26 two-dimensional substitution systems.

This is an evidence oracle, not a substitution-system implementation.  It
closes the Book's direct names, square-grid construction, inherited parallel
substitution mechanics, executable Notes form, backgrounds, dimensional and
shape variants, named examples, observer/encoding relations, sibling
boundaries, actual Index, split documents, Atlas, catalog, and false-positive
controls.

The evidence supports a two-dimensional ordered patch-emission form of the
existing SimpleProgram substitution construction.  It does not by itself
justify a T26 executor or top-level state class.  The strict square-grid source
uses uniformly aligned patches; orientation-sensitive off-grid geometry,
neighbor-dependent choice, adaptive subdivision, rasters, and coordinate
formulas are retained as variants, relations, controls, or observers rather
than silently promoted into the strict rule.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T26 source oracle requires assertions; do not use -O")


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "ref/A-New-Kind-of-Science"
DEFAULT_BOOK = SOURCE_ROOT / "A-New-Kind-of-Science.md"
ATLAS = SOURCE_ROOT / "ANKoS-Atlas.md"
CATALOG = ROOT / "ref/notes/CA-Types.csv"
TAXONOMY = ROOT / "ref/notes/CA-Types.md"

INDEX_FIRST_LINE = 20826
EXPECTED_BOOK_LINES = 22498
EXPECTED_BOOK_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
EXPECTED_ATLAS_SHA256 = "5ffab93f0007bbeb5da60af7cc08570f9a358c9f9f94e37c5e00f9fc0997bc8a"
EXPECTED_CATALOG_SHA256 = "26cef05af1155f80bc301900d2df95469a90de027ba860730519d25d096c2b73"
EXPECTED_TAXONOMY_SHA256 = "4c30fe079b2fb8f69e4c8c0dde3d59065227d4224cbe4b7693a17c0126cc3f1a"


# The protocol deliberately mixes exact names with independent mechanics,
# aliases, named examples, page routes, relations, sibling controls, headings,
# actual-Index routes, and absent modern spellings.  Broad terms are always
# paired with construction-specific context so this audit does not pretend
# that every occurrence of "substitution system" concerns T26.
QUERIES = {
    "Q00": r"\btwo-dimensional substitution systems?\b|\b2D substitution systems?\b",
    "Q01": (
        r"\btwo dimensional substitution systems?\b|"
        r"\b2-dimensional substitution systems?\b|"
        r"\b2-D substitution systems?\b|"
        r"\bsubstitution systems? in two dimensions\b"
    ),
    "Q02": (
        r"\bconstruct two-dimensional substitution systems? that work in essentially the same way\b|"
        r"\beach square is replaced by four smaller squares at every step\b|"
        r"\breplace each black square with several smaller black squares\b|"
        r"\bnew black squares is then in turn replaced in exactly the\b|"
        r"\bidentical copy of the whole pattern\b"
    ),
    "Q03": r"\bSS2DEvolve\b|\bFlatten2D\b",
    "Q04": (
        r"1 \\to \\{\\{1, 0\\}, \\{1, 1\\}\\}|"
        r"\bpatterns? \(a\) through \(f\) on page 188\b|"
        r"\bexcluded pairs of digits are in exact correspondence\b"
    ),
    "Q05": (
        r"\bcolor of a cell at position \{i, j\} in a 2D substitution system\b|"
        r"\bcolor of any square in a nested pattern can be found from its coordinates\b|"
        r"\bone more digit in their coordinates\b|"
        r"\btake the rules for the substitution system that generates a particular nested pattern\b|"
        r"\bfeeding the digit sequences of its y and x coordinates\b"
    ),
    "Q06": (
        r"\b2D substitution system from a initial condition such as\b|"
        r"\bNon-white backgrounds\b|"
        r"\bwhite squares are replaced by blocks which contain black squares\b"
    ),
    "Q07": (
        r"\bHigher-dimensional generalizations\b|"
        r"\bddimensional substitution system\b|"
        r"\bnested list of depth d\b|"
        r"\bSSEvolve\b|\bFlattenArray\b|"
        r"\banalog in 3D of the 2D rule on page 187\b|"
        r"\bin d dimensions, each black cell must be replaced by at least d\+1\b"
    ),
    "Q08": (
        r"\bOther shapes\b|"
        r"\bbased on subdividing squares into smaller squares\b|"
        r"\bbased on subdividing other geometrical figures\b|"
        r"\blabelling each shape and orientation with a different color\b|"
        r"\breproduced with equal-sized squares using the rule\b"
    ),
    "Q09": (
        r"\bPage 187 . Sierpi.ski pattern\b|"
        r"\bexample on page 187 by Wac.aw Sierpi.ski\b|"
        r"\bexamples \(a\) and \(c\) on page 188 by Karl Menger\b|"
        r"\bSierpi.ski[^.]{0,120}\b2D substitution system\b|"
        r"\b2D substitution system[^.]{0,120}\bSierpi.ski\b"
    ),
    "Q10": (
        r"\btwo-dimensional recursive subdivision\b|"
        r"\bgeneralization of a two-dimensional substitution system\b|"
        r"\bquadtree representation\b|"
        r"\bRecursive subdivision[^.]{0,100}\bsubstitution systems?, 187\b|"
        r"\bSubdivision systems \(substitution systems\), 82 2D, 187\b"
    ),
    "Q11": (
        r"\bas in a two-dimensional substitution system each black cell should repeatedly be replaced\b|"
        r"\bgenerated from the two-dimensional substitution systems shown\b|"
        r"\bExamples of nested patterns created by following the two-dimensional substitution rules shown\b|"
        r"\btwo-dimensional pointer-based encoding scheme[^.]{0,120}\bnested structure\b"
    ),
    "Q12": (
        r"\b4 billion or so possible such systems with 2.2 blocks and up to four colors\b|"
        r"\bOne starts from the substitution system with rules\b|"
        r"\b51 of the 65,536 possible 2.2 blocks of cells with 16 colors\b"
    ),
    "Q13": (
        r"\bevolution of a 2D substitution system, or equivalently from a Kronecker product\b|"
        r"Nest\[Flatten2D\[Map\[# \{\{1, 1\}, \{1, -1\}\}"
    ),
    "Q14": r"\bpattern can be generated by a 2D substitution system with rule\b",
    "Q15": (
        r"\bnothing about this basic process that depends on the squares being arranged\b|"
        r"\bsimple geometrical rule to replace each black square by two smaller black squares\b|"
        r"\bmust take account of the orientation of that square\b|"
        r"\bgeometrical rule that is used to replace each black square\b|"
        r"\breplacing one black square by two or more smaller black squares\b"
    ),
    "Q16": (
        r"\breplacement for a particular element at a given step can depend\b|"
        r"\bsets up elements on a grid it is straightforward to allow the replacements\b|"
        r"\bNeighbor-dependent substitution systems\b|"
        r"\bFlatten2D\[Partition\[list, \{2, 2\}, 1, -1\] /\. rule\]\b|"
        r"\barbitrarily large set of different possible neighborhood configurations\b"
    ),
    "Q17": (
        r"\bhow can this be generalized to higher dimensions\b|"
        r"\bno immediate way to generalize sequential substitution systems to two or more dimensions\b|"
        r"\belements are scanned in order.but whatever order is used\b"
    ),
    "Q18": r"^#### \*\*Substitution Systems and Fractals\*\*$",
    "Q19": (
        r"\bat each step each one of these elements is replaced by a new block of elements\b|"
        r"\beach element of a particular color should be replaced by a fixed block\b|"
        r"\bat every step each kind of element is replaced by a fixed block\b|"
        r"\bsubdividing each element into several that are drawn smaller\b"
    ),
    "Q20": (
        r"\b2D geometrical substitution systems?\b|"
        r"\bgeometrical substitution systems?\b|"
        r"\bAffine transformations\b|"
        r"\bPenrose tilings\b"
    ),
    "Q21": (
        r"\bpage 187\b|\bpage 188\b|\bpages 187 and 188\b|"
        r"\b187[–-]192\b|\b187[–-]189\b"
    ),
    "Q22": (
        r"\bD0L systems\b|\b0L systems\b|\bL systems, 82.87 2D, 187.189\b|"
        r"\bSubdivision systems \(substitution systems\)\b"
    ),
    "Q23": (
        r"\bAffine transformations and 2D substitution systems, 933\b|"
        r"\bC curve from 1D substitution system, 892 from 2D substitution system, 190\b|"
        r"\bDeterminism in 2D substitution systems, 188\b|"
        r"\bDigit sequences[^.]{0,100}\band 2D substitution systems, 931\b|"
        r"\bFractals[^.]{0,100}\band 2D substitution systems, 187\b|"
        r"\bGoldenRatio[^.]{0,100}\band 2D substitution systems, 932\b|"
        r"\bMatrices and 2D substitution systems, 933\b"
    ),
    "Q24": (
        r"\bin 2D substitution systems, 187\b|"
        r"\bSierpi.ski[^.]{0,160}\band 2D substitution system, 188\b|"
        r"\bSierpi.ski pattern[^.]{0,160}\band 2D substitution system, 187\b|"
        r"\bTop[^.]{0,120}\bin 2D substitution systems, 188\b"
    ),
    "Q25": (
        r"\bSubstitution systems, 82.87 2D. 187.192\b|"
        r"\bd.-dimensional, 932, 1091\b|"
        r"\bgeometrical, 189.192\b|"
        r"\bneighbor-dependent 2D, 192, 935\b|"
        r"\bneighbor-independent 2D, 187\b"
    ),
    "Q26": (
        r"\bTwo-dimensional cellular automata[^.]{0,180}\bsubstitution systems, 187.192\b|"
        r"\bL systems, 82.87 2D, 187.189\b|"
        r"\bRecursive subdivision and data compression, 568[^.]{0,160}\band substitution systems, 187\b"
    ),
    "Q27": (
        r"\bpatterns shown here ultimately have a simple nested structure\b|"
        r"\ball the patterns shown here ultimately have a simple nested structure\b|"
        r"\bpurely nested patterns\b"
    ),
    "Q28": (
        r"\btile substitution systems?\b|\bblock substitution systems?\b|"
        r"\barray substitution systems?\b|\bpicture grammars?\b|"
        r"\borientation policy\b|\bscale factor\b"
    ),
    "Q29": (
        r"\b2D representations\b|"
        r"\bsequences from 1D substitution systems can be displayed in 2D\b|"
        r"\barranged in two dimensions\b"
    ),
}


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 38-T26-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
    )
    print("source", "OK" if source_ok else "MISMATCH")
    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {n for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)}
        hits[name] = found
        print(
            name,
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
            ",".join(map(str, sorted(found))),
        )
    union = set().union(*hits.values())
    pre = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre
    print("union", len(union), digest(union), ",".join(map(str, sorted(union))))
    print("pre", len(pre), digest(pre), ",".join(map(str, sorted(pre))))
    print("index", len(index), digest(index), ",".join(map(str, sorted(index))))
    return 0 if source_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
