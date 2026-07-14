#!/usr/bin/env python3
"""Frozen primary-source audit for T25 two-dimensional Turing machines.

This is an evidence oracle, not a Turing-machine implementation.  It closes
the Book's direct name, captions, Notes implementation, aliases, turning-rule
variant, historical routes, actual Index, split documents, Atlas, catalog, and
false-positive controls.  It preserves the Book's distinction between the
generic square-grid rule (head state need not be heading), restricted systems
whose state records heading, and the separate 2D-mobile-automaton construction.

The architectural conclusion is deliberately no stronger than the evidence:
T25 reuses the T12 finite-state/symbol head event while parameterizing its
fixed support and displacement set to two dimensions.  A transparent tagged
cell representation is lossless, but arbitrary CA rules, hidden interpreters,
random transition choice, path-only state, or a T25 executor are not inferred.
"""

from __future__ import annotations

import hashlib
import itertools
import re
import sys
import unicodedata
from pathlib import Path


if not __debug__:
    raise RuntimeError("T25 source oracle requires assertions; do not use -O")


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


# Q00--Q04 close direct names, dimensional generalization, captions, the
# executable Notes form, and fixed-versus-relative movement. Q05--Q09 close
# every named alias, person route, Langton-ant formula, worm/hex variant, and
# visualization/path vocabulary. Q10 guards the adjacent but distinct 2D
# mobile-automaton construction. Q11--Q15 independently recover inherited
# Turing semantics: unique stateful head, self-only read, complete atomic
# transition, blank/default support, rule cardinality, and lossless tagged-cell
# representation. Q16--Q20 deliberately broaden worm, turtle, turning, hex-grid,
# and two-dimensional-grid vocabulary to expose false positives. Q21--Q24
# close dense actual-Index entry routes, aliases, Logo/robotics history, and the
# TMs redirect. Q25 closes all Turing section headings; Q26 closes experiment
# randomness and repeated-position language without treating either as a
# stochastic rule. Q27 independently closes the fixed-grid fact inherited from
# the Chapter 3 construction.
QUERIES = {
    "Q00": r"\btwo-dimensional Turing machines?\b|\b2D Turing machines?\b",
    "Q01": (
        r"\bgeneralize Turing machines to two dimensions\b|"
        r"\bgeneralizes Turing machines to move in two dimensions\b|"
        r"\bhead of the Turing machine to move around on a two-dimensional grid\b|"
        r"\bbackwards and forwards on a one-dimensional tape\b"
    ),
    "Q02": (
        r"\bfour possible directions the head should move\b|"
        r"\borientation of the arrow representing the state of the head has no direct relationship\b|"
        r"\bhead often visits the same position on the grid\b"
    ),
    "Q03": (
        r"\bTM2DStep\b|"
        r"\{dx, dy\}|"
        r"r : \{x\_, y\_\}|"
        r"tape\[\[x, y\]\]"
    ),
    "Q04": (
        r"\bRules based on turning\b|"
        r"\bfixed directions in the underlying grid\b|"
        r"\bturns to make at each step in the motion of the head\b|"
        r"\bturtles in the Logo computer language are set up\b"
    ),
    "Q05": (
        r"\bprehistoric worm\b|\bpossible worms\b|\bPaterson worms?\b|"
        r"\bvants?\b|\bturmites?\b|\bturning machines?\b|"
        r"\bLangton's ant\b|\bmobile turtles?\b"
    ),
    "Q06": (
        r"\bMichael Paterson (?:and John Conway|considers a class of simple 2D Turing machines)\b|"
        r"\bMichael Beeler[^.]{0,100}\b1296 possible worms\b|"
        r"\bChristopher Langton[^.]{0,100}\bvants\b|"
        r"\bRudy Rucker[^.]{0,100}\bturmites\b|"
        r"\bAllen Brady[^.]{0,100}\bturning machines\b"
    ),
    "Q07": (
        r"sp = s \(2c - 1\)i|"
        r"\{sp, 1 - c, \{Re\[sp\], Im\[sp\]\}\}|"
        r"\bspecific 4-state rule\b"
    ),
    "Q08": (
        r"\b1296 possible worms\b|"
        r"\bstate of the head records the direction of the motion taken at each step\b|"
        r"\bworms with rules of the simplest type on a hexagonal grid\b"
    ),
    "Q09": (
        r"\b2D position of the head at 500 successive steps\b|"
        r"\bpath traced out by the head of the two-dimensional Turing machine\b|"
        r"\bseemingly random fluctuations in this path\b"
    ),
    "Q10": (
        r"\b2D mobile automata\b|"
        r"\bMobile automata can be generalized just like Turing machines\b|"
        r"\$\(4k\)\^k\$ possible rules"
    ),
    "Q11": (
        r"\bline of cells, known as the \"tape\"\b|"
        r"\bsingle active cell, known as the \"head\"\b|"
        r"\brule for a Turing machine can depend on the state of the head\b|"
        r"\bnot on the colors of any neighboring cells\b"
    ),
    "Q12": (
        r"\bstate of a Turing machine at a particular step can be represented by the triple\b|"
        r"\bleft-hand side in each case gives the state of the head\b|"
        r"\bnew state of the head, the new value of the cell under the head and the displacement\b|"
        r"\bTMStep\b|\bTMEvolveList\b"
    ),
    "Q13": (
        r"\bresult of \*t\* steps of evolution from a blank tape\b|"
        r"s = 1; a\[_\] = 0; n = 0|"
        r"\bactive cell must start at a definite location\b|"
        r"\ball cells are initially white\b"
    ),
    "Q14": (
        r"\blighter colors in the cellular automaton represent ordinary cells in the Turing machine\b|"
        r"\bdarker colors represent the cell under the head\b|"
        r"\bcellular automaton which emulates it can be constructed\b|"
        r"\bcellular automaton has k\(s\+1\) colors\b"
    ),
    "Q15": (
        r"\bWith k possible colors for each cell and s possible states\b|"
        r"\$\(2sk\)\^\{sk\}\$|"
        r"\btotal of 4096 rules of this kind\b"
    ),
    "Q16": r"\bworms?\b",
    "Q17": r"\bturtles?\b",
    "Q18": r"\bturning\b",
    "Q19": r"\bhexagonal grid\b",
    "Q20": r"\btwo-dimensional grid\b",
    "Q21": (
        r"\bBeeler, Michael.*?and 2D Turing machines, 930\b|"
        r"\bBrady, Allen.*?and 2D Turing machines, 930\b|"
        r"\bConway, John.*?and 2D Turing machines, 930\b|"
        r"\bLangton, Christopher.*?and 2D Turing machines, 930\b|"
        r"\bPaterson, Michael.*?and 2D Turing machines, 880, 930\b|"
        r"\bRucker, Rudy.*?and 2D Turing machines, 930\b"
    ),
    "Q22": (
        r"\bTuring machines, 78-81 2D 184-186\b|"
        r"\bhistory of 2D, 930\b|\bimplementation of 2D, 930\b|"
        r"\bpaths in 3D from 2D, 931\b|"
        r"\bTurmites \(2D Turing machines\), 930\b|"
        r"\bTurning machines \(2D Turing machines\), 930\b|"
        r"\bTurtles \(artificial\) and 2D Turing machines, 930\b|"
        r"\bVants \(2D Turing machines\), 930\b|"
        r"\bTwo-dimensional cellular automata[^.]{0,240}\bTuring machines, 184.186\b"
    ),
    "Q23": (
        r"\bLogo \(computer language\) and 2D TMs, 930, 931\b|"
        r"\bRobotics[^.]{0,100}\bmobile turtles 930\b|"
        r"\bMIT[^.]{0,140}\bPaterson worms, 930\b|"
        r"\bWorm[^.]{0,100}\bPaterson's, 930\b"
    ),
    "Q24": r"\bTMs, see Turing machines\b",
    "Q25": r"^#### \*\*Turing Machines\*\*$",
    "Q26": (
        r"\bmillion randomly chosen rules\b|"
        r"\belements of randomness at some steps\b|"
        r"\bhead often visits the same position on the grid many times\b"
    ),
    "Q27": (
        r"\bcellular automata, mobile automata and Turing machines all have in common\b|"
        r"\bunderlying number and organization of cells always stays the same\b"
    ),
}


def line_set(spec: str) -> frozenset[int]:
    """Parse comma-separated line numbers and inclusive ranges."""
    result: set[int] = set()
    for item in filter(None, map(str.strip, spec.split(","))):
        if "-" in item:
            start, end = map(int, item.split("-", 1))
            result.update(range(start, end + 1))
        else:
            result.add(int(item))
    return frozenset(result)


# Filled after the deterministic query protocol is fixed.  Each tuple is
# (all physical lines, pre-Index lines, actual-Index lines, line-set digest).
EXPECTED_QUERY: dict[str, tuple[int, int, int, str]] = {}


# Every broad-query collision stays visible.  No line is silently discarded.
EXCLUDED_CLASS = {
    "unrelated_worms": line_set("4966,20480"),
    "unrelated_turning": line_set("5036,15324,17045"),
    "other_hexagonal_grid_systems": line_set("4422,4430,4440,15708,15865"),
    "other_two_dimensional_grid_systems": line_set("2364,5634"),
    "other_emulation_construction": line_set("18352"),
}
EXCLUDED = frozenset().union(*EXCLUDED_CLASS.values())


# Native evidence is the construction itself or an inherited Turing primitive:
# one stateful head, self-only table input, typed write/state/displacement
# result, fixed support, blank/default realization, and the explicit square-
# grid/turning/hex variants.  Images are included only when they are direct
# construction/rule/evolution evidence for the dependent asset audit.
NATIVE_EVIDENCE = line_set(
    "940,942,948,982,"
    "12014,12016,12018,12020,12023,12026,12034,12037,12039,12042,"
    "14275,"
    "2266,2268,2270,2280,2284,2286,2290,2292,2294,"
    "13662,13664,13666,13668,13670,13678"
)

# Relations are historical routes, observers, behavior summaries, generic
# dimensional context, equivalent transparent representations, and path views.
RELATION_EVIDENCE = line_set(
    "936,956,2152,2156,2264,2272,2274,2276,2306,"
    "2298,2302,"
    "7938,11566,12012,12028,12031,"
    "13660,13672,13674,"
    "18363,18366-18369,18372"
)

# Controls prevent nearby language from becoming invented semantics: random
# rule sampling and observed randomness are not stochastic UPDATE; a missing
# printed 3-state formula is not reconstructed; 2D mobile automata are a
# different read rule; and CA emulation is not the native compact program.
CONTROL_EVIDENCE = line_set(
    "2278,13676,13679,16400"
)

RETAINED = NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE


IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)$")
NATIVE_IMAGE_LINES = line_set("2268,2280,2284,2286,2290,2292")
RELATION_IMAGE_LINES = line_set("2298,2302,13674")
CONTROL_IMAGE_LINES = line_set("")
GOVERNED_IMAGE_LINES = (
    NATIVE_IMAGE_LINES | RELATION_IMAGE_LINES | CONTROL_IMAGE_LINES
)


# Actual Index supplies routes, never construction mechanics. Dense physical
# rows are classified by the exact T25 entry guarded below.
INDEX_CLASS = {
    "named_people_routes": line_set("20910,20940,21050,21432,21761,21990"),
    "logo_robotics_worm_routes": line_set("21475,21521,21970,22434"),
    "turing_entry_and_alias_routes": line_set("22346,22362,22378,22380,22394"),
    "broad_turning_collision_routes": line_set("20946,22352"),
}
INDEX_ROUTED = frozenset().union(*INDEX_CLASS.values())

INDEX_ENTRY_GUARDS = {
    "named_people_routes": {
        20910: ("beeler, michael", "and 2d turing machines, 930"),
        20940: ("brady, allen", "and 2d turing machines, 930"),
        21050: ("conway, john", "and 2d turing machines, 930"),
        21432: ("langton, christopher", "langton's ant (2d turing machine), 931"),
        21761: ("paterson, michael", "and 2d turing machines, 880, 930"),
        21990: ("rucker, rudy", "and 2d turing machines, 930"),
    },
    "logo_robotics_worm_routes": {
        21475: ("logo (computer language) and 2d tms, 930, 931",),
        21521: ("mit", "and paterson worms, 930"),
        21970: ("robotics", "and mobile turtles 930"),
        22434: ("worm", "paterson's, 930"),
    },
    "turing_entry_and_alias_routes": {
        22346: ("tms, see turing machines",),
        22362: ("turing machines, 78-81 2d 184-186",),
        22378: (
            "history of 2d, 930", "implementation of 2d, 930",
            "paths in 3d from 2d, 931", "turmites (2d turing machines), 930",
            "turning machines (2d turing machines), 930",
            "turtles (artificial) and 2d turing machines, 930",
        ),
        22380: ("two-dimensional cellular automata", "turing machines, 184–186"),
        22394: ("vants (2d turing machines), 930",),
    },
    "broad_turning_collision_routes": {
        20946: ("turning tracks of",),
        22352: ("tracks made by turning vehicles",),
    },
}


# Frozen values are populated below after the source protocol is exercised.
EXPECTED_SET: dict[str, tuple[int, str]] = {}
EXPECTED_EXCLUDED_CLASS: dict[str, tuple[int, str]] = {}
EXPECTED_INDEX_CLASS: dict[str, tuple[int, str]] = {}
EXPECTED_INDEX_ENTRY_GUARDS: tuple[int, str] = (0, "")
EXPECTED_IMAGE_PARTITION: dict[str, tuple[int, str]] = {}

EXPECTED_SPLIT_FILE_COUNT = 17
EXPECTED_SPLIT_PATHS_DIGEST = "409ee97767cd31136d0d647ac9f1d4555fa6154e20a3cd620baaa915d1bf6692"
EXPECTED_SPLIT_MANIFEST_DIGEST = "55a03f55f7c609afc197dc37f38bc25081b90502e720ed7210335deee15a9a84"
EXPECTED_SPLIT_QUERY: tuple[int, str] = (0, "")
EXPECTED_SPLIT_QUERY_EXACT: tuple[int, str] = (0, "")
EXPECTED_SPLIT_QUERY_NONEXACT: tuple[int, str] = (0, "")
EXPECTED_SPLIT_QUERY_MAPPING_DIGEST = ""
EXPECTED_SPLIT_RETAINED_EXACT: tuple[int, str] = (0, "")
EXPECTED_SPLIT_RETAINED_NONEXACT: tuple[int, str] = (0, "")
EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST = ""
EXPECTED_MONOLITH_ONLY: tuple[int, str] = (0, "")
EXPECTED_ATLAS_HITS: tuple[int, str] = (0, "")


def digest(values: set[int] | frozenset[int]) -> str:
    return hashlib.sha256(",".join(map(str, sorted(values))).encode("ascii")).hexdigest()


def digest_records(records: set[str] | list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(records)).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_line(line: str) -> str:
    text = unicodedata.normalize("NFKD", line).lower().replace("\\", "")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def best_witness(canonical: str, candidates: list[tuple[str, str]]) -> tuple[str, float]:
    canonical_tokens = set(normalized_line(canonical).split())
    scored: list[tuple[float, str]] = []
    for record, normalized in candidates:
        candidate_tokens = set(normalized.split())
        denominator = min(len(canonical_tokens), len(candidate_tokens))
        score = len(canonical_tokens & candidate_tokens) / denominator if denominator else 0.0
        scored.append((score, record))
    score, record = max(scored, key=lambda item: (item[0], item[1]))
    return record, score


def cardinal_moves() -> tuple[tuple[int, int], ...]:
    return ((-1, 0), (0, -1), (0, 1), (1, 0))


def tagged_step(
    cells: dict[tuple[int, int], tuple[str, int, int] | tuple[str, int]],
    table: dict[tuple[int, int], tuple[int, int, tuple[int, int]]],
    blank: int = 0,
) -> dict[tuple[int, int], tuple[str, int, int] | tuple[str, int]]:
    """Derived transparent two-write lowering of one deterministic TM event."""
    heads = [
        (position, value) for position, value in cells.items()
        if value[0] == "head"
    ]
    assert len(heads) == 1
    source, (_, state, symbol) = heads[0]
    next_state, write, move = table[(state, symbol)]
    assert move in cardinal_moves()
    destination = (source[0] + move[0], source[1] + move[1])
    destination_old = cells.get(destination, ("plain", blank))
    assert destination_old[0] == "plain"
    result = dict(cells)
    result[source] = ("plain", write)
    result[destination] = ("head", next_state, destination_old[1])
    return result


def langton_transition(state: complex, color: int) -> tuple[complex, int, tuple[int, int]]:
    """Exact Notes formula, evaluated over the four unit complex headings."""
    assert state in (1, 1j, -1, -1j) and color in (0, 1)
    next_state = state * (2 * color - 1) * 1j
    move = (int(next_state.real), int(next_state.imag))
    return next_state, 1 - color, move


def main() -> int:
    if len(sys.argv) > 2:
        raise SystemExit("usage: 37-T25-source-oracle.py [BOOK]")
    book = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_BOOK
    raw = book.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    at = lambda line_no: lines[line_no - 1]

    source_ok = (
        len(lines) == EXPECTED_BOOK_LINES
        and hashlib.sha256(raw).hexdigest() == EXPECTED_BOOK_SHA256
        and sha256(ATLAS) == EXPECTED_ATLAS_SHA256
        and sha256(CATALOG) == EXPECTED_CATALOG_SHA256
        and sha256(TAXONOMY) == EXPECTED_TAXONOMY_SHA256
    )
    ok = source_ok
    print("source", "OK" if source_ok else "MISMATCH")

    hits: dict[str, set[int]] = {}
    for name, pattern in QUERIES.items():
        found = {n for n, line in enumerate(lines, 1) if re.search(pattern, line, re.I)}
        hits[name] = found
        actual = (
            len(found),
            sum(n < INDEX_FIRST_LINE for n in found),
            sum(n >= INDEX_FIRST_LINE for n in found),
            digest(found),
        )
        good = actual == EXPECTED_QUERY.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    union = set().union(*hits.values())
    pre_index_union = {n for n in union if n < INDEX_FIRST_LINE}
    index = union - pre_index_union
    matched_retained = pre_index_union - set(EXCLUDED)
    governed = set(RETAINED) - union
    sets = {
        "union": union,
        "pre_index_union": pre_index_union,
        "index": index,
        "matched_retained": matched_retained,
        "governed_continuations": governed,
        "retained": set(RETAINED),
        "excluded": set(EXCLUDED),
        "native": set(NATIVE_EVIDENCE),
        "relation": set(RELATION_EVIDENCE),
        "control": set(CONTROL_EVIDENCE),
        "governed_images": set(GOVERNED_IMAGE_LINES),
    }
    for name, values in sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_SET.get(name)
        ok &= good
        print(name, "OK" if good else "MISMATCH", *actual)

    excluded_ok = (
        set().union(*EXCLUDED_CLASS.values()) == set(EXCLUDED)
        and sum(map(len, EXCLUDED_CLASS.values())) == len(EXCLUDED)
    )
    for name, values in EXCLUDED_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_EXCLUDED_CLASS.get(name)
        excluded_ok &= good
        print(f"excluded_{name}", "OK" if good else "MISMATCH", *actual)
    unexpected_pre_index = pre_index_union - set(RETAINED) - set(EXCLUDED)
    missing_query_classification = matched_retained - set(RETAINED)
    excluded_ok &= not unexpected_pre_index and not missing_query_classification
    ok &= excluded_ok
    print(
        "unresolved_pre_index", "OK" if excluded_ok else "MISMATCH",
        len(unexpected_pre_index) + len(missing_query_classification),
        *sorted(unexpected_pre_index | missing_query_classification),
    )

    index_ok = (
        set().union(*INDEX_CLASS.values()) == index
        and sum(map(len, INDEX_CLASS.values())) == len(index)
    )
    for name, values in INDEX_CLASS.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_INDEX_CLASS.get(name)
        index_ok &= good
        print(f"index_{name}", "OK" if good else "MISMATCH", *actual)
    guard_records = {
        f"{class_name}:{line_no}:{'|'.join(needles)}"
        for class_name, entries in INDEX_ENTRY_GUARDS.items()
        for line_no, needles in entries.items()
    }
    index_entry_guards_ok = (
        set(INDEX_ENTRY_GUARDS) == set(INDEX_CLASS)
        and all(
            set(INDEX_ENTRY_GUARDS[class_name]) == set(INDEX_CLASS[class_name])
            for class_name in INDEX_CLASS
        )
        and all(
            all(needle in at(line_no).lower() for needle in needles)
            for entries in INDEX_ENTRY_GUARDS.values()
            for line_no, needles in entries.items()
        )
        and (len(guard_records), digest_records(guard_records))
        == EXPECTED_INDEX_ENTRY_GUARDS
    )
    index_ok &= index_entry_guards_ok
    print(
        "index_entry_occurrence_guards",
        "OK" if index_entry_guards_ok else "MISMATCH",
        len(guard_records), digest_records(guard_records),
    )
    ok &= index_ok
    print("unresolved_index", "OK" if index_ok else "MISMATCH", len(index ^ set(INDEX_ROUTED)))

    derived_images = {n for n in RETAINED if IMAGE_RE.fullmatch(at(n))}
    image_sets = {
        "native": NATIVE_IMAGE_LINES,
        "relation": RELATION_IMAGE_LINES,
        "control": CONTROL_IMAGE_LINES,
    }
    images_ok = (
        derived_images == set(GOVERNED_IMAGE_LINES)
        and sum(map(len, image_sets.values())) == len(GOVERNED_IMAGE_LINES)
        and NATIVE_IMAGE_LINES <= NATIVE_EVIDENCE
        and RELATION_IMAGE_LINES <= RELATION_EVIDENCE
        and CONTROL_IMAGE_LINES <= CONTROL_EVIDENCE
        and all(IMAGE_RE.fullmatch(at(n)) for n in GOVERNED_IMAGE_LINES)
    )
    for name, values in image_sets.items():
        actual = (len(values), digest(values))
        good = actual == EXPECTED_IMAGE_PARTITION.get(name)
        images_ok &= good
        print(f"images_{name}", "OK" if good else "MISMATCH", *actual)
    ok &= images_ok
    print(
        "governed_image_interface", "OK" if images_ok else "MISMATCH",
        len(derived_images), digest(derived_images),
    )

    # Exact source wording and executable shape. No textbook-default boundary,
    # direction/state coupling, random rule choice, or missing formula is added.
    source_facts_ok = (
        "line of cells, known as the \"tape\"" in at(940)
        and "single active cell, known as the \"head\"" in at(940)
        and "state of the head" in at(942)
        and "color of the cell at the position of the head" in at(942)
        and "not on the colors of any neighboring cells" in at(942)
        and "fixed array of cells" in at(982)
        and "underlying number and organization of cells always stays the same" in at(982)
        and "generalize Turing machines to two dimensions" in at(2266)
        and "move around on a two-dimensional grid" in at(2266)
        and "four possible directions" in at(2270)
        and "no direct relationship to directions on the grid" in at(2270)
        and "all cells are initially white" in at(2294)
        and "head often visits the same position" in at(2294)
        and "\\{s, a\\} \\rightarrow \\{sp, ap, \\{dx, dy\\}\\}" in at(13662)
        and "TM2DStep" in at(13664)
        and "ReplacePart[tape, #2, {r}]" in at(13664)
        and "{s, tape[[x, y]]}/. rule" in at(13664)
    )
    ok &= source_facts_ok
    print("source_core_t25_mechanics", "OK" if source_facts_ok else "MISMATCH")

    inherited_turing_ok = (
        "state of a Turing machine at a particular step" in at(12014)
        and "state of the head" in at(12018)
        and "value of the cell under the head" in at(12018)
        and "new state of the head" in at(12018)
        and "new value of the cell under the head" in at(12018)
        and "displacement of the head" in at(12018)
        and "TMStep" in at(12023)
        and "ReplacePart" in at(12023)
        and "TMEvolveList" in at(12026)
        and "blank tape" in at(12034)
        and "a[_] = 0" in at(12037)
        and "n += d" in at(12039)
        and "$(2sk)^{sk}$" in at(12042)
        and "active cell must start at a definite location" in at(14275)
    )
    ok &= inherited_turing_ok
    print("source_inherited_t12_state_read_write_move", "OK" if inherited_turing_ok else "MISMATCH")

    tagged_representation_ok = (
        "lighter colors" in at(7938)
        and "ordinary cells in the Turing machine" in at(7938)
        and "darker colors represent the cell under the head" in at(7938)
        and "specific darker color corresponding to each possible state of the head" in at(7938)
        and "cellular automaton which emulates it" in at(18363)
        and "k(s+1) colors" in at(18372)
        and "single cell of color k" in at(18372)
        and "blank tape" in at(18372)
    )
    ok &= tagged_representation_ok
    print("source_lossless_tagged_cell_route", "OK" if tagged_representation_ok else "MISMATCH")

    variants_ok = (
        "state of the head records the direction" in at(13666)
        and "1296 possible worms" in at(13666)
        and "hexagonal grid" in at(13666)
        and "vants" in at(13666)
        and "turmites" in at(13666)
        and "turning machines" in at(13666)
        and "sp = s (2c - 1)i" in at(13668)
        and "sp, 1 - c" in at(13668)
        and "Re[sp], Im[sp]" in at(13668)
        and "Langton's ant" in at(13670)
        and "fixed directions in the underlying grid" in at(13678)
        and "turns to make at each step" in at(13678)
    )
    ok &= variants_ok
    print("source_alias_turning_hex_variants", "OK" if variants_ok else "MISMATCH")

    experiment_controls_ok = (
        "million randomly chosen rules" in at(2278)
        and "one of the rules" in at(2294)
        and "elements of randomness at some steps" in at(13676)
        and at(13677) == ""
        and at(13678).startswith("- Rules based on turning.")
        and "2D mobile automata" in at(13679)
        and "$(4k)^k$" in at(13679)
    )
    ok &= experiment_controls_ok
    print(
        "random_ensemble_missing_formula_mobile_control",
        "OK" if experiment_controls_ok else "MISMATCH",
    )

    # Conditional rule-space count: inherited Q x Sigma input and typed output
    # gain exactly the four printed square-grid displacements. This is derived,
    # not attributed as a printed Book formula.
    square_rule_count_ok = all(
        (4 * states * colors) ** (states * colors) > 0
        and len(cardinal_moves()) == 4
        for states in range(1, 6)
        for colors in range(1, 5)
    )
    square_4_state_binary_count = (4 * 4 * 2) ** (4 * 2)
    square_rule_count_ok &= square_4_state_binary_count == 32**8
    ok &= square_rule_count_ok
    print(
        "derived_square_grid_total_table_count",
        "OK" if square_rule_count_ok else "MISMATCH",
        square_4_state_binary_count,
    )

    langton_rows = {
        (state, color): langton_transition(state, color)
        for state, color in itertools.product((1, 1j, -1, -1j), (0, 1))
    }
    langton_ok = (
        len(langton_rows) == 8
        and all(row[0] in (1, 1j, -1, -1j) for row in langton_rows.values())
        and all(row[1] == 1 - color for (_, color), row in langton_rows.items())
        and {row[2] for row in langton_rows.values()} == set(cardinal_moves())
        and all(
            row[2] == (int(row[0].real), int(row[0].imag))
            for row in langton_rows.values()
        )
    )
    ok &= langton_ok
    print("derived_langton_closed_absolute_table", "OK" if langton_ok else "MISMATCH", len(langton_rows))

    sample_table = {
        (0, 0): (1, 1, (1, 0)),
        (0, 1): (0, 0, (0, 1)),
        (1, 0): (0, 1, (-1, 0)),
        (1, 1): (1, 0, (0, -1)),
    }
    initial = {
        (0, 0): ("head", 0, 0),
        (1, 0): ("plain", 1),
    }
    next_cells = tagged_step(initial, sample_table)
    atomic_lowering_ok = (
        next_cells[(0, 0)] == ("plain", 1)
        and next_cells[(1, 0)] == ("head", 1, 1)
        and sum(value[0] == "head" for value in next_cells.values()) == 1
    )
    ok &= atomic_lowering_ok
    print("derived_transparent_atomic_head_move", "OK" if atomic_lowering_ok else "MISMATCH")

    structural = (
        not NATIVE_EVIDENCE & RELATION_EVIDENCE
        and not NATIVE_EVIDENCE & CONTROL_EVIDENCE
        and not RELATION_EVIDENCE & CONTROL_EVIDENCE
        and NATIVE_EVIDENCE | RELATION_EVIDENCE | CONTROL_EVIDENCE == RETAINED
        and not RETAINED & index
        and matched_retained == set(RETAINED) & pre_index_union
        and governed == set(RETAINED) - union
    )
    ok &= structural
    print("structural", "OK" if structural else "MISMATCH")

    # Close all split Markdown copies with immutable manifests, complete query
    # enumeration, and deterministic reverse joins to the canonical monolith.
    split_paths = sorted(
        path for path in SOURCE_ROOT.rglob("*.md")
        if path.resolve() not in {DEFAULT_BOOK.resolve(), ATLAS.resolve()}
    )
    relative_paths = [path.relative_to(SOURCE_ROOT).as_posix() for path in split_paths]
    manifest = [
        f"{relative}\0{len(path.read_bytes())}\0{sha256(path)}"
        for path, relative in zip(split_paths, relative_paths, strict=True)
    ]
    split_manifest_ok = (
        len(split_paths) == EXPECTED_SPLIT_FILE_COUNT
        and digest_records(relative_paths) == EXPECTED_SPLIT_PATHS_DIGEST
        and digest_records(manifest) == EXPECTED_SPLIT_MANIFEST_DIGEST
    )
    ok &= split_manifest_ok
    print(
        "split_manifest", "OK" if split_manifest_ok else "MISMATCH",
        len(split_paths), digest_records(relative_paths), digest_records(manifest),
    )

    compiled = [re.compile(pattern, re.I) for pattern in QUERIES.values()]
    monolith_query_text = {at(n) for n in union}
    split_records: set[str] = set()
    split_exact: set[str] = set()
    split_nonexact: set[str] = set()
    split_lines: list[tuple[str, str]] = []
    split_texts: set[str] = set()
    split_record_text: dict[str, str] = {}
    for path, relative in zip(split_paths, relative_paths, strict=True):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            record = f"{relative}:{line_no}"
            split_lines.append((record, normalized_line(line)))
            split_texts.add(line)
            split_record_text[record] = line
            if not any(rx.search(line) for rx in compiled):
                continue
            split_records.add(record)
            (split_exact if line in monolith_query_text else split_nonexact).add(record)

    query_mapping: set[str] = set()
    query_mapping_ok = True
    monolith_witnesses = [
        (str(line_no), normalized_line(at(line_no))) for line_no in sorted(union)
    ]
    for record in sorted(split_nonexact):
        witness, score = best_witness(split_record_text[record], monolith_witnesses)
        query_mapping.add(f"{record}->{witness}:{score:.6f}")
        query_mapping_ok &= score >= 0.50 and int(witness) in union
    split_query_ok = (
        (len(split_records), digest_records(split_records)) == EXPECTED_SPLIT_QUERY
        and (len(split_exact), digest_records(split_exact)) == EXPECTED_SPLIT_QUERY_EXACT
        and (len(split_nonexact), digest_records(split_nonexact)) == EXPECTED_SPLIT_QUERY_NONEXACT
        and digest_records(query_mapping) == EXPECTED_SPLIT_QUERY_MAPPING_DIGEST
        and query_mapping_ok
    )
    ok &= split_query_ok
    print(
        "split_query_reverse_join", "OK" if split_query_ok else "MISMATCH",
        len(split_records), digest_records(split_records),
        len(split_exact), digest_records(split_exact),
        len(split_nonexact), digest_records(split_nonexact),
        digest_records(query_mapping),
    )

    exact_retained = {n for n in RETAINED if at(n) in split_texts}
    nonexact_retained = set(RETAINED) - exact_retained
    retained_mapping: set[str] = set()
    monolith_only: set[int] = set()
    for line_no in sorted(nonexact_retained):
        witness, score = best_witness(at(line_no), split_lines)
        if score >= 0.50:
            retained_mapping.add(f"{line_no}->{witness}:{score:.6f}")
        else:
            monolith_only.add(line_no)
    split_retained_ok = (
        (len(exact_retained), digest(exact_retained)) == EXPECTED_SPLIT_RETAINED_EXACT
        and (len(nonexact_retained), digest(nonexact_retained)) == EXPECTED_SPLIT_RETAINED_NONEXACT
        and digest_records(retained_mapping) == EXPECTED_SPLIT_RETAINED_MAPPING_DIGEST
        and (len(monolith_only), digest(monolith_only)) == EXPECTED_MONOLITH_ONLY
        and len(retained_mapping) + len(monolith_only) == len(nonexact_retained)
    )
    ok &= split_retained_ok
    print(
        "split_retained_reverse_join", "OK" if split_retained_ok else "MISMATCH",
        len(exact_retained), digest(exact_retained),
        len(nonexact_retained), digest(nonexact_retained),
        len(retained_mapping), digest_records(retained_mapping),
        len(monolith_only), digest(monolith_only),
    )

    atlas_lines = ATLAS.read_text(encoding="utf-8").splitlines()
    atlas_hits = {
        n for n, line in enumerate(atlas_lines, 1)
        if any(rx.search(line) for rx in compiled)
    }
    atlas_ok = (
        len(atlas_lines) == 542
        and (len(atlas_hits), digest(atlas_hits)) == EXPECTED_ATLAS_HITS
        and "Turing Machines" in atlas_lines[176]
        and "move in two dimensions" in atlas_lines[178]
    )
    ok &= atlas_ok
    print("atlas_summary_only", "OK" if atlas_ok else "MISMATCH", len(atlas_hits), digest(atlas_hits))

    catalog_lines = CATALOG.read_text(encoding="utf-8").splitlines()
    taxonomy_text = TAXONOMY.read_text(encoding="utf-8")
    catalog_ok = (
        len(catalog_lines) == 46
        and catalog_lines[25] == "Two-Dimensional Turing Machines,"
        and len(set(catalog_lines[1:])) == 45
        and "## 25. Two-Dimensional Turing Machines" in taxonomy_text
        and "Two-dimensional grid of tape cells." in taxonomy_text
        and "single active head occupies one grid location" in taxonomy_text
        and "four possible movement directions on the square grid" in taxonomy_text
        and "`movement_set`" in taxonomy_text
    )
    ok &= catalog_ok
    print("catalog_taxonomy_vocabulary_only", "OK" if catalog_ok else "MISMATCH")

    architecture_inference_ok = (
        source_facts_ok
        and inherited_turing_ok
        and tagged_representation_ok
        and variants_ok
        and experiment_controls_ok
        and square_rule_count_ok
        and langton_ok
        and atomic_lowering_ok
    )
    ok &= architecture_inference_ok
    print(
        "architecture_inference_parameterizes_t12_event_over_2d_support_and_moves",
        "OK" if architecture_inference_ok else "MISMATCH",
    )

    unresolved_total = (
        len(unexpected_pre_index)
        + len(missing_query_classification)
        + len(index - set(INDEX_ROUTED))
        + len(set(INDEX_ROUTED) - index)
        + len(monolith_only)
    )
    unresolved_ok = unresolved_total == 0
    ok &= unresolved_ok
    print("unresolved_total", "OK" if unresolved_ok else "MISMATCH", unresolved_total)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
