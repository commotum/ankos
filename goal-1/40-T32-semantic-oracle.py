#!/usr/bin/env python3
"""Independent semantic oracle for T32, Template Constraint Systems.

T32 is a declarative model-set construction, not a transition construction.
Its strict Book profile is a binary field on ``Z^2`` whose oriented
word in the raw sorted ``(row, column)`` offset order
``((-1,0),(0,-1),(0,0),(0,1),(1,0))`` belongs to a fixed allowed set.  Only
after the explicit adapter ``(row,column) -> (x=column,y=-row)`` may these
slots be called ``(North, West, Self, East, South)``.  The five slots are the
non-corner entries of the displayed 3 by 3 cross.  Adjacent occurrences
overlap because all words are views of one pointwise field; they are not
independently placeable tiles.

The source boundary is local and explicit:

* BOOK:2614 says every local arrangement must match a fixed set of templates;
* BOOK:2618 says the templates apply at every cell and neighboring templates
  overlap;
* BOOK:2620 and BOOK:14048 establish 32 binary five-slot templates and 2^32
  possible allowed sets for the strict profile;
* BOOK:13513-13520 fixes raw sorted row/column offsets and the descending
  binary configuration catalog; compass names are adapter-derived, not source;
* BOOK:2634 begins T33 by additionally requiring a particular allowed
  template to occur somewhere;
* BOOK:2646 says a constraint supplies no direct pattern-production procedure;
* BOOK:14055-14061 gives a pure ``SatisfiedQ`` check over overlapping views;
* BOOK:14082-14083 separates unbounded existence and finite-region search;
* BOOK:14113 describes cellular-automaton fixed points as a relation, not the
  native T32 execution semantics.

Accordingly, the smallest reusable base is T31's declarative relation/model
set, exact periodic/open/window presentations, pure verifier, and scoped query
envelopes.  T32 adds one closed relation node: an ordered footprint plus an
unordered finite set of exact allowed words.  The strict Book cross is a
preset.  There is no seed, time, active locus, write, successor, or commit.

This file proves the composition without implementing runtime code.  It uses
independent native-cross and generic-offset verifiers; exhaustive bounded
commutation; a reversible cross-matrix codec; exact overlap checks; wrapped
alias-occurrence tests; orientation-versus-histogram counterexamples; explicit
scope and pointwise-model identity checks; verifier/solver separation; and
hostile validation.  It additionally exhausts the complete 1,024-member
binary cardinal T31 relation space, proves a checked compact-histogram / exact-
template round trip and direct-verifier commutation, and proves simultaneous
C4 rotation of support, templates, models, and violation reports.  Rotation is
an explicit observer/transform: it is neither implicit template matching nor
pointwise model equality.  The oracle is dependency-free, deterministic,
portable outside the repository root, silent on import, and fails closed under
``python -O``.

BOOK:13513-13520 textually fixes the sorted five-neighbor slot order and its
descending binary catalog, so BOOK:14050's 32-bit numeric constraint codec is
reconstructed and guarded below without reading pixels.  BOOK:13513's first
offset nevertheless uses the malformed delimiter ``(-1,0)`` where the rest use
list braces; the exact one-token delimiter repair is pinned and never presented
as pristine executable Mathematica.  Determinant-negative reflection, binary
label exchange, and representation-only slot permutation are separately
commuted below.  Deliberately open source matters remain rather than being
guessed: the complete displayed rows for the numbered main-text examples and
the 171-pattern raster catalog are not reconstructed by this semantic oracle.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256
from itertools import product
from math import lcm
from pathlib import Path


if not __debug__:
    raise RuntimeError("T32 semantic verification requires assertions; do not run with -O")


Coord2 = tuple[int, int]
Offset2 = tuple[int, int]
Template = tuple[int, ...]
Histogram = tuple[int, ...]
Tile = tuple[tuple[int, ...], ...]
ValueTable = tuple[tuple[Coord2, int], ...]

BOOK_CROSS_OFFSETS: tuple[Offset2, ...] = (
    (-1, 0),  # previous row, same column
    (0, -1),  # same row, previous column
    (0, 0),   # anchor row and column
    (0, 1),   # same row, next column
    (1, 0),   # next row, same column
)
BOOK_CROSS_SLOT_NAMES = (
    "row-1,column",
    "row,column-1",
    "row,column",
    "row,column+1",
    "row+1,column",
)
ENU_CROSS_OFFSETS: tuple[Offset2, ...] = (
    (0, 1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (0, -1),
)
ADAPTER_DERIVED_DIRECTION_NAMES = ("North", "West", "Self", "East", "South")
RAW_BOOK_OFFSET_FRAGMENT = (
    r"$\{(-1, 0), \{0, -1\}, \{0, 0\}, \{0, 1\}, \{1, 0\}\}$"
)
REPAIRED_BOOK_OFFSET_FRAGMENT = (
    r"$\{\{-1, 0\}, \{0, -1\}, \{0, 0\}, \{0, 1\}, \{1, 0\}\}$"
)
SOURCE_REPAIRS: tuple[str, ...] = (
    "BOOK:13513 first raw offset delimiter (-1,0) -> {-1,0}; guarded by exact full-fragment equality and prose/context, not executed as pristine Mathematica",
)
GENERIC_SLOT_PERMUTATION: tuple[int, ...] = (2, 4, 0, 3, 1)
SOURCE_BINARY_CATALOG: tuple[Template, ...] = tuple(
    tuple((value >> shift) & 1 for shift in range(4, -1, -1))
    for value in range(31, -1, -1)
)
BINARY_TEMPLATES: tuple[Template, ...] = SOURCE_BINARY_CATALOG

SOURCE_CLAIMS: tuple[tuple[int, str], ...] = (
    (2614, "local arrangement of colors around every cell to match a fixed set of possible templates"),
    (2618, "templates apply to every cell, with templates of neighboring cells overlapping"),
    (2620, "There are a total of 4,294,967,296 possible sets of such templates"),
    (2634, "a particular template from this set must appear at least somewhere"),
    (2646, "there is no such direct procedure"),
    (2654, "no pattern that satisfies the constraint in a limited region"),
    (13513, r"for 2D 5-neighbor rules it is  $\{(-1, 0), \{0, -1\}, \{0, 0\}, \{0, 1\}, \{1, 0\}\}$"),
    (13513, "offset lists are always taken to be in the order given by *Sort*"),
    (13516, "Reverse[Table[IntegerDigits[i - 1,"),
    (13517, "k, Length[os]], {i, k^Length[os]}]]"),
    (13520, "page 941 for 5-neighbor rules"),
    (14048, "total of 32 possible"),
    (14050, "Position[IntegerDigits[n, 2, 32], 1]"),
    (14055, "A set of allowed templates can be specified"),
    (14058, "SatisfiedQ[list_, allowed_]"),
    (14060, "Partition[list, {3, 3}, {1, 1}]"),
    (14082, "formally undecidable"),
    (14083, "finite region is NPcomplete"),
    (14097, "increase the size of the templates, or increase the number of possible colors"),
    (14109, "only 2×2 arrangements of colors that can occur"),
    (14113, "configurations that remain unchanged in the evolution of a 2D cellular automaton"),
)

OPEN_SOURCE_MATTERS: tuple[str, ...] = (
    "BOOK:2616/2626/2628 contain raster-only displayed example rows and the 171-pattern tiles; those pixels are not promoted to exact program or witness data here.",
    "The Book does not specify a canonical complete solver, proof-certificate AST, or finite search schedule for T32.",
)

ARCHITECTURE_CLASSIFICATION: tuple[str, ...] = (
    "1: direct reuse of T31 model-set, scope, verifier, query-result, and certificate boundaries",
    "2: parameterize the closed local relation by an ordered footprint and exact allowed words; the binary cross is a preset",
    "3: lossless native cross-matrix and generic ordered-offset representations",
    "4: inherit the established D058/T31 declarative model-set nonfit to SimpleProgram rollout; no canonical successor can be supplied faithfully, while the incremental T32 delta is classes 1-3 only and adds no class-4 category or execution algebra",
)

GOAL2_DELTA = (
    "Add AllowedLocalPatterns(offsets, allowed_words) as one closed node in "
    "T31's declarative constraint algebra, plus orientation-preserving local "
    "violations and the binary-cross preset; reuse scope/model/verifier/query/"
    "certificate infrastructure and add no rollout, frontier, rule-result, or "
    "update branch.  AllowedOrientedTemplates in this oracle is a proof model, "
    "not a prescribed Goal 2 API name.  Include the guarded source-derived "
    "32-bit numeric codec only for the strict binary raw Book row/column cross "
    "preset, with compass names available solely through the checked Book/ENU adapter."
)


def exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def exact_tuple(value: object, name: str) -> tuple[object, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{name} must be an exact tuple")
    return value


def checked_coord(value: object, name: str) -> Coord2:
    raw = exact_tuple(value, name)
    if len(raw) != 2:
        raise ValueError(f"{name} must be a row/column pair")
    return (exact_int(raw[0], f"{name}.row"), exact_int(raw[1], f"{name}.column"))


def book_row_column_to_enu(value: object) -> Coord2:
    """Explicit semantic adapter: raw Book (row,column) to (east,north)."""

    row, column = checked_coord(value, "Book row/column offset")
    return (column, -row)


def enu_to_book_row_column(value: object) -> Coord2:
    """Inverse adapter from (east,north) back to raw Book (row,column)."""

    raw = exact_tuple(value, "ENU offset")
    if len(raw) != 2:
        raise ValueError("ENU offset must be an east/north pair")
    east = exact_int(raw[0], "ENU east offset")
    north = exact_int(raw[1], "ENU north offset")
    return (-north, east)


def guarded_book_offset_repair(raw_fragment: object) -> tuple[tuple[Offset2, ...], str]:
    """Accept exactly the malformed source fragment and repair one delimiter."""

    if type(raw_fragment) is not str:
        raise TypeError("raw source fragment must be an exact string")
    if raw_fragment != RAW_BOOK_OFFSET_FRAGMENT:
        raise ValueError("raw source fragment differs from the pinned BOOK:13513 text")
    repaired = raw_fragment.replace("(-1, 0)", r"\{-1, 0\}", 1)
    if repaired != REPAIRED_BOOK_OFFSET_FRAGMENT:
        raise RuntimeError("guarded source repair produced unexpected text")
    return BOOK_CROSS_OFFSETS, repaired


def checked_alphabet_size(value: object) -> int:
    size = exact_int(value, "alphabet size")
    if size <= 0:
        raise ValueError("alphabet must be finite and nonempty")
    return size


def checked_label(value: object, alphabet_size: int, name: str) -> int:
    size = checked_alphabet_size(alphabet_size)
    label = exact_int(value, name)
    if label < 0 or label >= size:
        raise ValueError(f"{name} is outside the declared alphabet")
    return label


def checked_offsets(value: object) -> tuple[Offset2, ...]:
    raw = exact_tuple(value, "offset footprint")
    if not raw:
        raise ValueError("offset footprint must be nonempty")
    offsets = tuple(checked_coord(item, "offset") for item in raw)
    if len(set(offsets)) != len(offsets):
        raise ValueError("offset occurrences must have distinct lattice addresses")
    if (0, 0) not in offsets:
        raise ValueError("T32 local templates must include the anchor cell")
    return offsets


def checked_template(
    value: object,
    alphabet_size: int,
    arity: int,
    *,
    name: str = "template",
) -> Template:
    raw = exact_tuple(value, name)
    if len(raw) != arity:
        raise ValueError(f"{name} must contain exactly {arity} oriented slots")
    return tuple(
        checked_label(item, alphabet_size, f"{name}[{index}]")
        for index, item in enumerate(raw)
    )


@dataclass(frozen=True)
class AllowedOrientedTemplates:
    """Closed local relation data; an empty allowed set is valid and inconsistent."""

    alphabet_size: int
    offsets: tuple[Offset2, ...]
    allowed: tuple[Template, ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        offsets = checked_offsets(self.offsets)
        raw_allowed = exact_tuple(self.allowed, "allowed template set")
        checked = tuple(
            checked_template(item, size, len(offsets), name="allowed template")
            for item in raw_allowed
        )
        if len(set(checked)) != len(checked):
            raise ValueError("allowed template set contains a duplicate")
        object.__setattr__(self, "offsets", offsets)
        object.__setattr__(self, "allowed", tuple(sorted(checked)))

    def contains(self, observed: Template) -> bool:
        checked = checked_template(
            observed,
            self.alphabet_size,
            len(self.offsets),
            name="observed template",
        )
        return checked in self.allowed


def checked_neighbor_offsets(value: object) -> tuple[Offset2, ...]:
    raw = exact_tuple(value, "neighbor footprint")
    if not raw:
        raise ValueError("neighbor footprint must be nonempty")
    offsets = tuple(checked_coord(item, "neighbor offset") for item in raw)
    if (0, 0) in offsets:
        raise ValueError("center is conditioned separately and cannot be a neighbor offset")
    if len(set(offsets)) != len(offsets):
        raise ValueError("neighbor footprint contains a duplicate offset")
    return offsets


def checked_histogram(
    value: object,
    alphabet_size: int,
    degree: int,
    *,
    name: str = "histogram",
) -> Histogram:
    raw = exact_tuple(value, name)
    if len(raw) != alphabet_size:
        raise ValueError(f"{name} must contain one count per alphabet value")
    counts = tuple(exact_int(item, f"{name} count") for item in raw)
    if any(count < 0 for count in counts):
        raise ValueError(f"{name} counts must be nonnegative")
    if sum(counts) != degree:
        raise ValueError(f"{name} counts must sum to neighbor degree {degree}")
    return counts


def all_histograms(alphabet_size: int, degree: int) -> tuple[Histogram, ...]:
    size = checked_alphabet_size(alphabet_size)
    checked_degree = exact_int(degree, "neighbor degree")
    if checked_degree <= 0:
        raise ValueError("neighbor degree must be positive")
    return tuple(
        counts
        for counts in product(range(checked_degree + 1), repeat=size)
        if sum(counts) == checked_degree
    )


@dataclass(frozen=True)
class CenterConditionedHistogram:
    """Closed T31 relation: center label selects allowed neighbor histograms."""

    alphabet_size: int
    neighbor_offsets: tuple[Offset2, ...]
    allowed_by_center: tuple[tuple[Histogram, ...], ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        offsets = checked_neighbor_offsets(self.neighbor_offsets)
        raw_rows = exact_tuple(self.allowed_by_center, "center-conditioned rows")
        if len(raw_rows) != size:
            raise ValueError("there must be exactly one allowed row per center label")
        rows: list[tuple[Histogram, ...]] = []
        for center, raw_row in enumerate(raw_rows):
            row = exact_tuple(raw_row, f"allowed row for center {center}")
            checked = tuple(
                checked_histogram(
                    item,
                    size,
                    len(offsets),
                    name=f"allowed histogram for center {center}",
                )
                for item in row
            )
            if len(set(checked)) != len(checked):
                raise ValueError("center-conditioned row contains a duplicate histogram")
            rows.append(tuple(sorted(checked)))
        object.__setattr__(self, "neighbor_offsets", offsets)
        object.__setattr__(self, "allowed_by_center", tuple(rows))

    def contains(self, center: object, histogram: object) -> bool:
        checked_center = checked_label(center, self.alphabet_size, "center label")
        checked = checked_histogram(
            histogram,
            self.alphabet_size,
            len(self.neighbor_offsets),
            name="observed histogram",
        )
        return checked in self.allowed_by_center[checked_center]


def histogram_of(values: object, alphabet_size: int) -> Histogram:
    raw = exact_tuple(values, "neighbor values")
    size = checked_alphabet_size(alphabet_size)
    labels = tuple(
        checked_label(item, size, f"neighbor value {index}")
        for index, item in enumerate(raw)
    )
    return tuple(labels.count(label) for label in range(size))


def compile_histogram_relation(
    compact: CenterConditionedHistogram,
) -> AllowedOrientedTemplates:
    """Exhaustively lower T31 data; center is the final compiled slot."""

    if type(compact) is not CenterConditionedHistogram:
        raise TypeError("histogram compiler requires CenterConditionedHistogram")
    offsets = compact.neighbor_offsets + ((0, 0),)
    allowed: list[Template] = []
    for word in all_words(compact.alphabet_size, len(offsets)):
        neighbor_values = word[:-1]
        center = word[-1]
        if compact.contains(center, histogram_of(neighbor_values, compact.alphabet_size)):
            allowed.append(word)
    return AllowedOrientedTemplates(compact.alphabet_size, offsets, tuple(allowed))


def recover_histogram_relation(
    compiled: AllowedOrientedTemplates,
) -> CenterConditionedHistogram:
    """Checked inverse on the histogram-invariant image of the compiler."""

    if type(compiled) is not AllowedOrientedTemplates:
        raise TypeError("histogram recovery requires AllowedOrientedTemplates")
    if compiled.offsets[-1] != (0, 0) or (0, 0) in compiled.offsets[:-1]:
        raise ValueError("compiled histogram form requires one final center slot")
    neighbor_offsets = compiled.offsets[:-1]
    rows: list[tuple[Histogram, ...]] = []
    words = all_words(compiled.alphabet_size, len(compiled.offsets))
    allowed = set(compiled.allowed)
    for center in range(compiled.alphabet_size):
        accepted_histograms: list[Histogram] = []
        for histogram in all_histograms(compiled.alphabet_size, len(neighbor_offsets)):
            group = tuple(
                word
                for word in words
                if word[-1] == center
                and histogram_of(word[:-1], compiled.alphabet_size) == histogram
            )
            membership = {word in allowed for word in group}
            if len(membership) != 1:
                raise ValueError(
                    "oriented membership is not invariant under neighbor permutations"
                )
            if True in membership:
                accepted_histograms.append(histogram)
        rows.append(tuple(accepted_histograms))
    return CenterConditionedHistogram(
        compiled.alphabet_size,
        neighbor_offsets,
        tuple(rows),
    )


def book_cross_relation(allowed: object) -> AllowedOrientedTemplates:
    return AllowedOrientedTemplates(2, BOOK_CROSS_OFFSETS, exact_tuple(allowed, "allowed"))


def fixed_binary_digits(value: object, width: object) -> tuple[int, ...]:
    number = exact_int(value, "binary number")
    checked_width = exact_int(width, "binary width")
    if checked_width <= 0:
        raise ValueError("binary width must be positive")
    if number < 0 or number >= 2**checked_width:
        raise ValueError("binary number does not fit the declared width")
    return tuple(
        (number >> shift) & 1 for shift in range(checked_width - 1, -1, -1)
    )


def selected_catalog_templates(constraint_number: object) -> tuple[Template, ...]:
    """BOOK:14050: select 1-indexed catalog positions whose fixed digit is one."""

    digits = fixed_binary_digits(constraint_number, len(SOURCE_BINARY_CATALOG))
    return tuple(
        template
        for template, digit in zip(SOURCE_BINARY_CATALOG, digits)
        if digit == 1
    )


def decode_constraint_number(constraint_number: object) -> AllowedOrientedTemplates:
    return book_cross_relation(selected_catalog_templates(constraint_number))


def encode_constraint_number(relation: AllowedOrientedTemplates) -> int:
    """Checked inverse for the strict binary cross relation only."""

    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("constraint-number encoding requires AllowedOrientedTemplates")
    if relation.alphabet_size != 2 or relation.offsets != BOOK_CROSS_OFFSETS:
        raise ValueError("constraint-number encoding is defined only for the strict binary cross")
    allowed = set(relation.allowed)
    digits = tuple(
        1 if template in allowed else 0 for template in SOURCE_BINARY_CATALOG
    )
    number = 0
    for digit in digits:
        number = 2 * number + digit
    return number


def all_words(alphabet_size: int, arity: int) -> tuple[Template, ...]:
    size = checked_alphabet_size(alphabet_size)
    checked_arity = exact_int(arity, "template arity")
    if checked_arity <= 0:
        raise ValueError("template arity must be positive")
    return tuple(product(range(size), repeat=checked_arity))


def checked_tile(value: object, alphabet_size: int, *, name: str = "tile") -> Tile:
    raw_rows = exact_tuple(value, name)
    if not raw_rows:
        raise ValueError(f"{name} must have positive height")
    width: int | None = None
    rows: list[tuple[int, ...]] = []
    for row_index, raw_row in enumerate(raw_rows):
        row = exact_tuple(raw_row, f"{name} row")
        if not row:
            raise ValueError(f"{name} must have positive width")
        labels = tuple(
            checked_label(item, alphabet_size, f"{name}[{row_index},{column_index}]")
            for column_index, item in enumerate(row)
        )
        if width is None:
            width = len(labels)
        elif len(labels) != width:
            raise ValueError(f"{name} rows must be rectangular")
        rows.append(labels)
    return tuple(rows)


@dataclass(frozen=True)
class NativeBinaryTorus:
    """Native strict-profile representation used only by the direct verifier."""

    rows: Tile

    def __post_init__(self) -> None:
        object.__setattr__(self, "rows", checked_tile(self.rows, 2, name="native torus"))

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.rows), len(self.rows[0]))


@dataclass(frozen=True)
class PeriodicPresentation:
    """Exact total field on Z^2, represented by one rectangular fundamental tile."""

    alphabet_size: int
    tile: Tile

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        object.__setattr__(self, "tile", checked_tile(self.tile, size, name="periodic tile"))

    @property
    def periods(self) -> tuple[int, int]:
        return (len(self.tile), len(self.tile[0]))

    def value_at(self, coordinate: object) -> int:
        row, column = checked_coord(coordinate, "lattice coordinate")
        height, width = self.periods
        return self.tile[row % height][column % width]


def encode_native(native: NativeBinaryTorus) -> PeriodicPresentation:
    if type(native) is not NativeBinaryTorus:
        raise TypeError("native value must be an exact NativeBinaryTorus")
    return PeriodicPresentation(2, native.rows)


def decode_native(presentation: PeriodicPresentation) -> NativeBinaryTorus:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("presentation must be an exact PeriodicPresentation")
    if presentation.alphabet_size != 2:
        raise ValueError("native T32 cross codec requires the binary alphabet")
    return NativeBinaryTorus(presentation.tile)


@dataclass(frozen=True)
class DirectViolation:
    anchor: Coord2
    observed: Template


@dataclass(frozen=True)
class DirectReport:
    checked_anchors: int
    violations: tuple[DirectViolation, ...]

    @property
    def satisfied(self) -> bool:
        return not self.violations


def direct_cross_at(native: NativeBinaryTorus, anchor: object) -> Template:
    """Literal Book-cross read, independent of the generic offset reader."""

    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct verifier requires NativeBinaryTorus")
    row, column = checked_coord(anchor, "anchor")
    height, width = native.shape
    rows = native.rows
    return (
        rows[(row - 1) % height][column % width],
        rows[row % height][(column - 1) % width],
        rows[row % height][column % width],
        rows[row % height][(column + 1) % width],
        rows[(row + 1) % height][column % width],
    )


def direct_verify_periodic(native: NativeBinaryTorus, allowed: frozenset[Template]) -> DirectReport:
    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct verifier requires NativeBinaryTorus")
    if type(allowed) is not frozenset:
        raise TypeError("direct allowed set must be an exact frozenset")
    for item in allowed:
        checked_template(item, 2, 5, name="direct allowed template")
    height, width = native.shape
    violations: list[DirectViolation] = []
    for row in range(height):
        for column in range(width):
            observed = direct_cross_at(native, (row, column))
            if observed not in allowed:
                violations.append(DirectViolation((row, column), observed))
    return DirectReport(height * width, tuple(violations))


def direct_count_word_at(native: NativeBinaryTorus, anchor: object) -> Template:
    """Independent T31 read in raw Book cardinal-offset order, then center.

    The direction aliases here are justified only by ``book_row_column_to_enu``.
    """

    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct count verifier requires NativeBinaryTorus")
    row, column = checked_coord(anchor, "count anchor")
    height, width = native.shape
    rows = native.rows
    return (
        rows[(row - 1) % height][column % width],
        rows[row % height][(column - 1) % width],
        rows[row % height][(column + 1) % width],
        rows[(row + 1) % height][column % width],
        rows[row % height][column % width],
    )


def direct_verify_count_periodic(
    native: NativeBinaryTorus,
    compact: CenterConditionedHistogram,
) -> DirectReport:
    """Direct count semantics; it never calls the template compiler/verifier."""

    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct count verifier requires NativeBinaryTorus")
    if type(compact) is not CenterConditionedHistogram:
        raise TypeError("direct count verifier requires CenterConditionedHistogram")
    if compact.alphabet_size != 2:
        raise ValueError("native binary direct count verifier requires alphabet size two")
    if compact.neighbor_offsets != (
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    ):
        raise ValueError("native direct count verifier requires the four cardinal slots")
    height, width = native.shape
    violations: list[DirectViolation] = []
    for row in range(height):
        for column in range(width):
            observed = direct_count_word_at(native, (row, column))
            histogram = (
                observed[:-1].count(0),
                observed[:-1].count(1),
            )
            if not compact.contains(observed[-1], histogram):
                violations.append(DirectViolation((row, column), observed))
    return DirectReport(height * width, tuple(violations))


@dataclass(frozen=True)
class LocalViolation:
    anchor: Coord2
    observed: Template


@dataclass(frozen=True)
class Verification:
    scope: str
    checked_anchors: int
    violations: tuple[LocalViolation, ...]
    proves_global_model: bool

    @property
    def satisfied(self) -> bool:
        return not self.violations


def generic_read_periodic(
    presentation: PeriodicPresentation,
    relation: AllowedOrientedTemplates,
    anchor: object,
) -> Template:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("generic reader requires PeriodicPresentation")
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("generic reader requires AllowedOrientedTemplates")
    if presentation.alphabet_size != relation.alphabet_size:
        raise ValueError("presentation and relation alphabets differ")
    row, column = checked_coord(anchor, "anchor")
    return tuple(
        presentation.value_at((row + delta_row, column + delta_column))
        for delta_row, delta_column in relation.offsets
    )


def generic_verify_periodic(
    presentation: PeriodicPresentation,
    relation: AllowedOrientedTemplates,
) -> Verification:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("generic verifier requires PeriodicPresentation")
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("generic verifier requires AllowedOrientedTemplates")
    if presentation.alphabet_size != relation.alphabet_size:
        raise ValueError("presentation and relation alphabets differ")
    height, width = presentation.periods
    violations: list[LocalViolation] = []
    for row in range(height):
        for column in range(width):
            observed = generic_read_periodic(presentation, relation, (row, column))
            if not relation.contains(observed):
                violations.append(LocalViolation((row, column), observed))
    return Verification(
        "periodic-global-proof",
        height * width,
        tuple(violations),
        not violations,
    )


def normalized_direct(report: DirectReport) -> tuple[int, tuple[tuple[Coord2, Template], ...]]:
    return (
        report.checked_anchors,
        tuple((violation.anchor, violation.observed) for violation in report.violations),
    )


def normalized_generic(report: Verification) -> tuple[int, tuple[tuple[Coord2, Template], ...]]:
    return (
        report.checked_anchors,
        tuple((violation.anchor, violation.observed) for violation in report.violations),
    )


def checked_value_table(value: object, alphabet_size: int, *, name: str) -> ValueTable:
    raw = exact_tuple(value, name)
    entries: list[tuple[Coord2, int]] = []
    seen: set[Coord2] = set()
    for index, item in enumerate(raw):
        pair = exact_tuple(item, f"{name}[{index}]")
        if len(pair) != 2:
            raise ValueError(f"{name} entry must be a coordinate/label pair")
        coordinate = checked_coord(pair[0], f"{name} coordinate")
        label = checked_label(pair[1], alphabet_size, f"{name} label")
        if coordinate in seen:
            raise ValueError(f"{name} contains a duplicate coordinate")
        seen.add(coordinate)
        entries.append((coordinate, label))
    return tuple(sorted(entries))


@dataclass(frozen=True)
class OpenPatch:
    alphabet_size: int
    values: ValueTable

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        object.__setattr__(
            self,
            "values",
            checked_value_table(self.values, size, name="open patch values"),
        )


@dataclass(frozen=True)
class FiniteWindow:
    alphabet_size: int
    anchors: tuple[Coord2, ...]
    values: ValueTable

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw_anchors = exact_tuple(self.anchors, "window anchors")
        anchors = tuple(checked_coord(item, "window anchor") for item in raw_anchors)
        if len(set(anchors)) != len(anchors):
            raise ValueError("window anchors contain a duplicate")
        object.__setattr__(self, "anchors", tuple(sorted(anchors)))
        object.__setattr__(
            self,
            "values",
            checked_value_table(self.values, size, name="window values"),
        )


def read_table_at(
    table: dict[Coord2, int],
    relation: AllowedOrientedTemplates,
    anchor: Coord2,
) -> Template | None:
    values: list[int] = []
    for delta_row, delta_column in relation.offsets:
        coordinate = (anchor[0] + delta_row, anchor[1] + delta_column)
        if coordinate not in table:
            return None
        values.append(table[coordinate])
    return tuple(values)


def verify_open(patch: OpenPatch, relation: AllowedOrientedTemplates) -> Verification:
    if type(patch) is not OpenPatch:
        raise TypeError("open verifier requires OpenPatch")
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("open verifier requires AllowedOrientedTemplates")
    if patch.alphabet_size != relation.alphabet_size:
        raise ValueError("patch and relation alphabets differ")
    table = dict(patch.values)
    violations: list[LocalViolation] = []
    checked = 0
    for anchor in sorted(table):
        observed = read_table_at(table, relation, anchor)
        if observed is None:
            continue
        checked += 1
        if not relation.contains(observed):
            violations.append(LocalViolation(anchor, observed))
    return Verification("open-local-check", checked, tuple(violations), False)


def verify_window(window: FiniteWindow, relation: AllowedOrientedTemplates) -> Verification:
    if type(window) is not FiniteWindow:
        raise TypeError("window verifier requires FiniteWindow")
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("window verifier requires AllowedOrientedTemplates")
    if window.alphabet_size != relation.alphabet_size:
        raise ValueError("window and relation alphabets differ")
    table = dict(window.values)
    violations: list[LocalViolation] = []
    for anchor in window.anchors:
        observed = read_table_at(table, relation, anchor)
        if observed is None:
            raise ValueError("finite window is missing a declared anchor's footprint halo")
        if not relation.contains(observed):
            violations.append(LocalViolation(anchor, observed))
    return Verification("finite-window", len(window.anchors), tuple(violations), False)


def periodic_equal(left: PeriodicPresentation, right: PeriodicPresentation) -> bool:
    """Exact pointwise identity over the componentwise LCM fundamental box."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("periodic equality requires exact periodic presentations")
    if left.alphabet_size != right.alphabet_size:
        return False
    height = lcm(left.periods[0], right.periods[0])
    width = lcm(left.periods[1], right.periods[1])
    return all(
        left.value_at((row, column)) == right.value_at((row, column))
        for row in range(height)
        for column in range(width)
    )


def checked_quarter_turns(value: object) -> int:
    turns = exact_int(value, "quarter turns")
    if turns < 0 or turns > 3:
        raise ValueError("quarter turns must be one of 0, 1, 2, 3")
    return turns


def rotate_coordinate(value: object, quarter_turns: object) -> Coord2:
    """Apply an orientation-preserving determinant-+1 square rotation."""

    row, column = checked_coord(value, "rotation coordinate")
    turns = checked_quarter_turns(quarter_turns)
    for _ in range(turns):
        row, column = -column, row
    return (row, column)


def rotate_cross_template(template: object, quarter_turns: object) -> Template:
    checked = checked_template(template, 2, 5, name="cross template")
    turns = checked_quarter_turns(quarter_turns)
    values_by_rotated_offset = {
        rotate_coordinate(offset, turns): label
        for offset, label in zip(BOOK_CROSS_OFFSETS, checked)
    }
    assert set(values_by_rotated_offset) == set(BOOK_CROSS_OFFSETS)
    return tuple(values_by_rotated_offset[offset] for offset in BOOK_CROSS_OFFSETS)


def rotate_cross_relation(
    relation: AllowedOrientedTemplates,
    quarter_turns: object,
) -> AllowedOrientedTemplates:
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("relation rotation requires AllowedOrientedTemplates")
    if relation.alphabet_size != 2 or relation.offsets != BOOK_CROSS_OFFSETS:
        raise ValueError("strict cross rotation requires the binary Book cross profile")
    turns = checked_quarter_turns(quarter_turns)
    return book_cross_relation(
        tuple(rotate_cross_template(template, turns) for template in relation.allowed)
    )


def rotate_periodic(
    presentation: PeriodicPresentation,
    quarter_turns: object,
) -> PeriodicPresentation:
    """Rotate the exact total field: Y[q] = X[R^-1 q]."""

    if type(presentation) is not PeriodicPresentation:
        raise TypeError("model rotation requires PeriodicPresentation")
    turns = checked_quarter_turns(quarter_turns)
    source_height, source_width = presentation.periods
    target_height, target_width = (
        (source_height, source_width)
        if turns % 2 == 0
        else (source_width, source_height)
    )
    inverse_turns = (-turns) % 4
    tile = tuple(
        tuple(
            presentation.value_at(
                rotate_coordinate((row, column), inverse_turns)
            )
            for column in range(target_width)
        )
        for row in range(target_height)
    )
    return PeriodicPresentation(presentation.alphabet_size, tile)


def rotated_report_signature(
    report: Verification,
    quarter_turns: object,
    target_periods: object,
) -> tuple[tuple[Coord2, Template], ...]:
    if type(report) is not Verification:
        raise TypeError("report rotation requires Verification")
    turns = checked_quarter_turns(quarter_turns)
    raw_periods = exact_tuple(target_periods, "target periods")
    if len(raw_periods) != 2:
        raise ValueError("target periods must contain height and width")
    height = exact_int(raw_periods[0], "target period height")
    width = exact_int(raw_periods[1], "target period width")
    if height <= 0 or width <= 0:
        raise ValueError("target periods must be positive")
    entries = []
    for violation in report.violations:
        row, column = rotate_coordinate(violation.anchor, turns)
        entries.append(
            (
                (row % height, column % width),
                rotate_cross_template(violation.observed, turns),
            )
        )
    return tuple(sorted(entries))


def report_signature(report: Verification) -> tuple[tuple[Coord2, Template], ...]:
    if type(report) is not Verification:
        raise TypeError("report signature requires Verification")
    return tuple(sorted((item.anchor, item.observed) for item in report.violations))


def same_rotation_orbit(
    left: PeriodicPresentation,
    right: PeriodicPresentation,
) -> bool:
    """Explicit observer; this does not alter pointwise model equality."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("rotation-orbit comparison requires periodic presentations")
    return any(periodic_equal(rotate_periodic(left, turns), right) for turns in range(4))


def reflect_coordinate(value: object) -> Coord2:
    """Determinant-negative reflection of raw (row,column) across column zero."""

    row, column = checked_coord(value, "reflection coordinate")
    return (row, -column)


def reflect_cross_template(template: object) -> Template:
    checked = checked_template(template, 2, 5, name="cross template")
    values_by_reflected_offset = {
        reflect_coordinate(offset): label
        for offset, label in zip(BOOK_CROSS_OFFSETS, checked)
    }
    assert set(values_by_reflected_offset) == set(BOOK_CROSS_OFFSETS)
    return tuple(values_by_reflected_offset[offset] for offset in BOOK_CROSS_OFFSETS)


def reflect_cross_relation(
    relation: AllowedOrientedTemplates,
) -> AllowedOrientedTemplates:
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("relation reflection requires AllowedOrientedTemplates")
    if relation.alphabet_size != 2 or relation.offsets != BOOK_CROSS_OFFSETS:
        raise ValueError("strict cross reflection requires the binary Book cross profile")
    return book_cross_relation(
        tuple(reflect_cross_template(template) for template in relation.allowed)
    )


def reflect_periodic(presentation: PeriodicPresentation) -> PeriodicPresentation:
    """Reflect the exact total field: Y[q] = X[F q], with F = F^-1."""

    if type(presentation) is not PeriodicPresentation:
        raise TypeError("model reflection requires PeriodicPresentation")
    height, width = presentation.periods
    tile = tuple(
        tuple(
            presentation.value_at(reflect_coordinate((row, column)))
            for column in range(width)
        )
        for row in range(height)
    )
    return PeriodicPresentation(presentation.alphabet_size, tile)


def reflected_report_signature(
    report: Verification,
    target_periods: object,
) -> tuple[tuple[Coord2, Template], ...]:
    if type(report) is not Verification:
        raise TypeError("report reflection requires Verification")
    raw_periods = exact_tuple(target_periods, "target periods")
    if len(raw_periods) != 2:
        raise ValueError("target periods must contain height and width")
    height = exact_int(raw_periods[0], "target period height")
    width = exact_int(raw_periods[1], "target period width")
    if height <= 0 or width <= 0:
        raise ValueError("target periods must be positive")
    entries = []
    for violation in report.violations:
        row, column = reflect_coordinate(violation.anchor)
        entries.append(
            (
                (row % height, column % width),
                reflect_cross_template(violation.observed),
            )
        )
    return tuple(sorted(entries))


def same_reflection_orbit(
    left: PeriodicPresentation,
    right: PeriodicPresentation,
) -> bool:
    """Explicit two-element observer orbit; not pointwise equality."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("reflection-orbit comparison requires periodic presentations")
    return periodic_equal(left, right) or periodic_equal(reflect_periodic(left), right)


def exchange_binary_template(template: object) -> Template:
    checked = checked_template(template, 2, 5, name="binary cross template")
    return tuple(1 - label for label in checked)


def exchange_binary_support(offsets: object) -> tuple[Offset2, ...]:
    """Label exchange acts explicitly as identity on geometric support."""

    return checked_offsets(offsets)


def exchange_binary_anchor(anchor: object) -> Coord2:
    """Label exchange acts explicitly as identity on anchor coordinates."""

    return checked_coord(anchor, "label-exchange anchor")


def exchange_binary_relation(
    relation: AllowedOrientedTemplates,
) -> AllowedOrientedTemplates:
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("label exchange requires AllowedOrientedTemplates")
    if relation.alphabet_size != 2 or relation.offsets != BOOK_CROSS_OFFSETS:
        raise ValueError("label exchange requires the strict binary Book cross")
    return AllowedOrientedTemplates(
        2,
        exchange_binary_support(relation.offsets),
        tuple(exchange_binary_template(template) for template in relation.allowed),
    )


def exchange_binary_periodic(
    presentation: PeriodicPresentation,
) -> PeriodicPresentation:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("label exchange requires PeriodicPresentation")
    if presentation.alphabet_size != 2:
        raise ValueError("label exchange requires a binary model")
    return PeriodicPresentation(
        2,
        tuple(tuple(1 - label for label in row) for row in presentation.tile),
    )


def exchanged_report_signature(
    report: Verification,
) -> tuple[tuple[Coord2, Template], ...]:
    if type(report) is not Verification:
        raise TypeError("report label exchange requires Verification")
    return tuple(
        sorted(
            (
                exchange_binary_anchor(violation.anchor),
                exchange_binary_template(violation.observed),
            )
            for violation in report.violations
        )
    )


def same_binary_exchange_orbit(
    left: PeriodicPresentation,
    right: PeriodicPresentation,
) -> bool:
    """Explicit identity/complement observer orbit; not pointwise equality."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("label-exchange orbit comparison requires periodic presentations")
    if left.alphabet_size != 2 or right.alphabet_size != 2:
        raise ValueError("label-exchange orbit comparison requires binary models")
    return periodic_equal(left, right) or periodic_equal(
        exchange_binary_periodic(left), right
    )


def checked_slot_permutation(value: object, arity: int) -> tuple[int, ...]:
    raw = exact_tuple(value, "slot permutation")
    checked_arity = exact_int(arity, "slot arity")
    if len(raw) != checked_arity:
        raise ValueError("slot permutation length differs from relation arity")
    permutation = tuple(exact_int(item, "slot permutation index") for item in raw)
    if set(permutation) != set(range(checked_arity)):
        raise ValueError("slot permutation must contain every slot index exactly once")
    return permutation


def permute_word_slots(
    word: object,
    permutation: object,
    alphabet_size: int,
) -> Template:
    raw_word = exact_tuple(word, "word")
    checked = checked_template(raw_word, alphabet_size, len(raw_word), name="word")
    order = checked_slot_permutation(permutation, len(checked))
    return tuple(checked[index] for index in order)


def inverse_slot_permutation(permutation: object) -> tuple[int, ...]:
    raw = exact_tuple(permutation, "slot permutation")
    order = checked_slot_permutation(raw, len(raw))
    inverse = [0] * len(order)
    for new_index, old_index in enumerate(order):
        inverse[old_index] = new_index
    return tuple(inverse)


def permute_relation_slots(
    relation: AllowedOrientedTemplates,
    permutation: object,
) -> AllowedOrientedTemplates:
    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("slot permutation requires AllowedOrientedTemplates")
    order = checked_slot_permutation(permutation, len(relation.offsets))
    return AllowedOrientedTemplates(
        relation.alphabet_size,
        tuple(relation.offsets[index] for index in order),
        tuple(
            permute_word_slots(template, order, relation.alphabet_size)
            for template in relation.allowed
        ),
    )


def permuted_report_signature(
    report: Verification,
    permutation: object,
    alphabet_size: int,
) -> tuple[tuple[Coord2, Template], ...]:
    if type(report) is not Verification:
        raise TypeError("report slot permutation requires Verification")
    return tuple(
        sorted(
            (
                violation.anchor,
                permute_word_slots(
                    violation.observed,
                    permutation,
                    alphabet_size,
                ),
            )
            for violation in report.violations
        )
    )


@dataclass(frozen=True)
class ClaimedOccurrence:
    anchor: Coord2
    template: Template


def occurrence_assignment(
    occurrence: ClaimedOccurrence,
    relation: AllowedOrientedTemplates,
    periods: object,
) -> dict[Coord2, int] | None:
    if type(occurrence) is not ClaimedOccurrence:
        raise TypeError("occurrence must be an exact ClaimedOccurrence")
    anchor = checked_coord(occurrence.anchor, "occurrence anchor")
    template = checked_template(
        occurrence.template,
        relation.alphabet_size,
        len(relation.offsets),
        name="claimed occurrence template",
    )
    raw_periods = exact_tuple(periods, "periods")
    if len(raw_periods) != 2:
        raise ValueError("periods must contain height and width")
    height = exact_int(raw_periods[0], "period height")
    width = exact_int(raw_periods[1], "period width")
    if height <= 0 or width <= 0:
        raise ValueError("periods must be positive")
    assignment: dict[Coord2, int] = {}
    for (delta_row, delta_column), label in zip(relation.offsets, template):
        residue = ((anchor[0] + delta_row) % height, (anchor[1] + delta_column) % width)
        previous = assignment.get(residue)
        if previous is not None and previous != label:
            return None
        assignment[residue] = label
    return assignment


def occurrences_overlap_consistent(
    occurrences: object,
    relation: AllowedOrientedTemplates,
    periods: object,
) -> bool:
    raw = exact_tuple(occurrences, "claimed occurrences")
    combined: dict[Coord2, int] = {}
    for occurrence in raw:
        if type(occurrence) is not ClaimedOccurrence:
            raise TypeError("claimed occurrence entry has the wrong type")
        if not relation.contains(occurrence.template):
            return False
        assignment = occurrence_assignment(occurrence, relation, periods)
        if assignment is None:
            return False
        for residue, label in assignment.items():
            previous = combined.get(residue)
            if previous is not None and previous != label:
                return False
            combined[residue] = label
    return True


def extracted_occurrences(
    presentation: PeriodicPresentation,
    relation: AllowedOrientedTemplates,
) -> tuple[ClaimedOccurrence, ...]:
    height, width = presentation.periods
    return tuple(
        ClaimedOccurrence(
            (row, column),
            generic_read_periodic(presentation, relation, (row, column)),
        )
        for row in range(height)
        for column in range(width)
    )


CrossMatrix = tuple[tuple[int | None, int | None, int | None], ...]


def cross_to_matrix(template: object) -> CrossMatrix:
    north, west, center, east, south = checked_template(template, 2, 5)
    return (
        (None, north, None),
        (west, center, east),
        (None, south, None),
    )


def matrix_to_cross(value: object) -> Template:
    rows = exact_tuple(value, "cross matrix")
    if len(rows) != 3:
        raise ValueError("cross matrix must have three rows")
    checked_rows = tuple(exact_tuple(row, "cross matrix row") for row in rows)
    if any(len(row) != 3 for row in checked_rows):
        raise ValueError("cross matrix rows must have three entries")
    if any(
        checked_rows[row][column] is not None
        for row, column in ((0, 0), (0, 2), (2, 0), (2, 2))
    ):
        raise ValueError("cross-matrix corners are absent footprint slots, not labels")
    return checked_template(
        (
            checked_rows[0][1],
            checked_rows[1][0],
            checked_rows[1][1],
            checked_rows[1][2],
            checked_rows[2][1],
        ),
        2,
        5,
    )


@dataclass(frozen=True)
class PeriodBoundQuery:
    periods: tuple[int, int]

    def __post_init__(self) -> None:
        raw = exact_tuple(self.periods, "query periods")
        if len(raw) != 2:
            raise ValueError("query periods must contain height and width")
        height = exact_int(raw[0], "query period height")
        width = exact_int(raw[1], "query period width")
        if height <= 0 or width <= 0:
            raise ValueError("query periods must be positive")


@dataclass(frozen=True)
class Satisfiable:
    witness: PeriodicPresentation
    verification: Verification
    explored_candidates: int


@dataclass(frozen=True)
class Unknown:
    reason: str
    explored_periods: tuple[int, int]
    explored_candidates: int


QueryOutcome = Satisfiable | Unknown


def bounded_period_search(
    relation: AllowedOrientedTemplates,
    query: PeriodBoundQuery,
) -> QueryOutcome:
    """Explicit external test solver; bounded failure never proves global UNSAT."""

    if type(relation) is not AllowedOrientedTemplates:
        raise TypeError("search requires AllowedOrientedTemplates")
    if type(query) is not PeriodBoundQuery:
        raise TypeError("search requires PeriodBoundQuery")
    height, width = query.periods
    explored = 0
    for flat in product(range(relation.alphabet_size), repeat=height * width):
        explored += 1
        tile = tuple(
            tuple(flat[row * width : (row + 1) * width])
            for row in range(height)
        )
        witness = PeriodicPresentation(relation.alphabet_size, tile)
        verification = generic_verify_periodic(witness, relation)
        if verification.satisfied:
            return Satisfiable(witness, verification, explored)
    return Unknown("no witness in the declared period scope", query.periods, explored)


def native_tiles(height: int, width: int) -> tuple[NativeBinaryTorus, ...]:
    return tuple(
        NativeBinaryTorus(
            tuple(
                tuple(flat[row * width : (row + 1) * width])
                for row in range(height)
            )
        )
        for flat in product((0, 1), repeat=height * width)
    )


def direct_allowed_profiles() -> tuple[frozenset[Template], ...]:
    all_set = frozenset(BINARY_TEMPLATES)
    return (
        all_set,
        frozenset(),
        frozenset(template for template in BINARY_TEMPLATES if template[2] == 0),
        frozenset(template for template in BINARY_TEMPLATES if template[0] == template[3]),
        frozenset(template for template in BINARY_TEMPLATES if sum(template) % 2 == 0),
        frozenset({(1, 0, 0, 1, 0)}),
        frozenset({(0, 1, 0, 1, 0)}),
        frozenset(
            template
            for template in BINARY_TEMPLATES
            if (template[0], template[1]) in ((0, 1), (1, 0))
        ),
    )


CARDINAL_NEIGHBOR_OFFSETS: tuple[Offset2, ...] = (
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
)
BINARY_DEGREE4_HISTOGRAMS: tuple[Histogram, ...] = all_histograms(2, 4)


def binary_count_relation(row_zero_mask: object, row_one_mask: object) -> CenterConditionedHistogram:
    masks = (
        exact_int(row_zero_mask, "center-zero mask"),
        exact_int(row_one_mask, "center-one mask"),
    )
    if any(mask < 0 or mask >= 2 ** len(BINARY_DEGREE4_HISTOGRAMS) for mask in masks):
        raise ValueError("binary degree-four histogram mask is outside 0..31")
    rows = tuple(
        tuple(
            histogram
            for index, histogram in enumerate(BINARY_DEGREE4_HISTOGRAMS)
            if mask & (1 << index)
        )
        for mask in masks
    )
    return CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, rows)


def audit_histogram_compilation() -> tuple[int, int, int, int, int]:
    """Prove T31 direct-count semantics commute with the lossless T32 lowering."""

    exhaustive_relations = 0
    recovery_round_trips = 0
    commutations = 0
    local_checks = 0
    two_by_two_models = native_tiles(2, 2)
    for row_zero_mask in range(32):
        for row_one_mask in range(32):
            compact = binary_count_relation(row_zero_mask, row_one_mask)
            compiled = compile_histogram_relation(compact)
            recovered = recover_histogram_relation(compiled)
            assert recovered == compact
            assert compile_histogram_relation(recovered) == compiled
            exhaustive_relations += 1
            recovery_round_trips += 1
            for native in two_by_two_models:
                direct = direct_verify_count_periodic(native, compact)
                generic = generic_verify_periodic(encode_native(native), compiled)
                assert normalized_direct(direct) == normalized_generic(generic)
                commutations += 1
                local_checks += direct.checked_anchors

    adversarial_masks = (
        (0, 0),
        (31, 31),
        (1, 16),
        (4, 4),
        (10, 21),
        (31, 0),
        (0, 31),
        (5, 18),
    )
    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for native in native_tiles(height, width):
            for row_zero_mask, row_one_mask in adversarial_masks:
                compact = binary_count_relation(row_zero_mask, row_one_mask)
                compiled = compile_histogram_relation(compact)
                direct = direct_verify_count_periodic(native, compact)
                generic = generic_verify_periodic(encode_native(native), compiled)
                assert normalized_direct(direct) == normalized_generic(generic)
                commutations += 1
                local_checks += direct.checked_anchors

    oriented = AllowedOrientedTemplates(
        2,
        CARDINAL_NEIGHBOR_OFFSETS + ((0, 0),),
        ((1, 0, 1, 0, 0),),
    )
    expect_raises(ValueError, lambda: recover_histogram_relation(oriented))

    assert exhaustive_relations == 1_024
    assert recovery_round_trips == 1_024
    assert commutations == 21_712
    assert local_checks == 109_200
    return (
        exhaustive_relations,
        recovery_round_trips,
        commutations,
        local_checks,
        1,
    )


def audit_source_claims() -> int:
    root = Path(__file__).resolve().parents[1]
    book = root / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
    lines = book.read_text(encoding="utf-8").splitlines()
    for line_number, needle in SOURCE_CLAIMS:
        assert needle in lines[line_number - 1], (line_number, needle)
    assert 2 ** len(BINARY_TEMPLATES) == 4_294_967_296
    return len(SOURCE_CLAIMS)


def audit_guarded_source_repair() -> int:
    root = Path(__file__).resolve().parents[1]
    book = root / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
    source_line = book.read_text(encoding="utf-8").splitlines()[13513 - 1]
    assert RAW_BOOK_OFFSET_FRAGMENT in source_line
    assert r"\{(-1, 0)" in RAW_BOOK_OFFSET_FRAGMENT
    assert r"\{\{-1, 0\}" in REPAIRED_BOOK_OFFSET_FRAGMENT
    offsets, repaired = guarded_book_offset_repair(RAW_BOOK_OFFSET_FRAGMENT)
    assert offsets == BOOK_CROSS_OFFSETS
    assert repaired == REPAIRED_BOOK_OFFSET_FRAGMENT
    assert len(SOURCE_REPAIRS) == 1
    return len(SOURCE_REPAIRS)


def audit_book_enu_adapter() -> int:
    mapped = tuple(book_row_column_to_enu(offset) for offset in BOOK_CROSS_OFFSETS)
    assert mapped == ENU_CROSS_OFFSETS
    assert ADAPTER_DERIVED_DIRECTION_NAMES == (
        "North",
        "West",
        "Self",
        "East",
        "South",
    )
    for book_offset, enu_offset in zip(BOOK_CROSS_OFFSETS, ENU_CROSS_OFFSETS):
        assert enu_to_book_row_column(enu_offset) == book_offset
        assert book_row_column_to_enu(enu_to_book_row_column(enu_offset)) == enu_offset
    return len(BOOK_CROSS_OFFSETS)


def audit_cross_codec() -> int:
    for template in BINARY_TEMPLATES:
        matrix = cross_to_matrix(template)
        assert matrix_to_cross(matrix) == template
    return len(BINARY_TEMPLATES)


def audit_source_numeric_codec() -> tuple[int, int, int, tuple[int, ...]]:
    assert len(SOURCE_BINARY_CATALOG) == 32
    assert len(set(SOURCE_BINARY_CATALOG)) == 32
    assert SOURCE_BINARY_CATALOG[0] == (1, 1, 1, 1, 1)
    assert SOURCE_BINARY_CATALOG[-1] == (0, 0, 0, 0, 0)
    assert SOURCE_BINARY_CATALOG == tuple(
        fixed_binary_digits(value, 5) for value in range(31, -1, -1)
    )

    singleton_round_trips = 0
    for position in range(32):
        number = 1 << (31 - position)
        selected = selected_catalog_templates(number)
        assert selected == (SOURCE_BINARY_CATALOG[position],)
        relation = decode_constraint_number(number)
        assert relation.allowed == tuple(sorted(selected))
        assert encode_constraint_number(relation) == number
        singleton_round_trips += 1

    representatives = (0, 2**32 - 1, 1_384_774, 328_778_790)
    representative_counts: list[int] = []
    for number in representatives:
        selected = selected_catalog_templates(number)
        relation = decode_constraint_number(number)
        assert set(relation.allowed) == set(selected)
        assert encode_constraint_number(relation) == number
        assert decode_constraint_number(encode_constraint_number(relation)) == relation
        representative_counts.append(len(selected))
    assert tuple(representative_counts) == (0, 32, 8, 12)
    return (
        len(SOURCE_BINARY_CATALOG),
        singleton_round_trips,
        len(representatives),
        tuple(representative_counts),
    )


def audit_exhaustive_commutation() -> tuple[int, int, int, int]:
    shapes = ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3))
    profiles = direct_allowed_profiles()
    configurations = 0
    commutations = 0
    local_checks = 0
    round_trips = 0
    for height, width in shapes:
        for native in native_tiles(height, width):
            configurations += 1
            generic = encode_native(native)
            assert decode_native(generic) == native
            round_trips += 1
            for allowed in profiles:
                relation = book_cross_relation(tuple(allowed))
                direct = direct_verify_periodic(native, allowed)
                report = generic_verify_periodic(generic, relation)
                assert normalized_direct(direct) == normalized_generic(report)
                assert report.proves_global_model == report.satisfied
                commutations += 1
                local_checks += direct.checked_anchors
    assert configurations == 666
    assert commutations == 5_328
    assert local_checks == 43_664
    assert round_trips == configurations
    return configurations, commutations, local_checks, round_trips


def patch_for_cross(template: Template) -> OpenPatch:
    north, west, center, east, south = checked_template(template, 2, 5)
    return OpenPatch(
        2,
        (
            ((-1, 0), north),
            ((0, -1), west),
            ((0, 0), center),
            ((0, 1), east),
            ((1, 0), south),
        ),
    )


def audit_exact_coverage_and_orientation() -> tuple[int, int, int]:
    singleton_accepts = 0
    singleton_rejects = 0
    for index, template in enumerate(BINARY_TEMPLATES):
        relation = book_cross_relation((template,))
        accepted = verify_open(patch_for_cross(template), relation)
        assert accepted.checked_anchors == 1
        assert accepted.satisfied
        singleton_accepts += 1
        other = BINARY_TEMPLATES[(index + 1) % len(BINARY_TEMPLATES)]
        rejected = verify_open(patch_for_cross(other), relation)
        assert rejected.checked_anchors == 1
        assert not rejected.satisfied
        singleton_rejects += 1

    oriented = (1, 0, 0, 1, 0)
    same_histogram = (0, 1, 0, 1, 0)
    assert oriented[2] == same_histogram[2]
    assert sorted(oriented[:2] + oriented[3:]) == sorted(
        same_histogram[:2] + same_histogram[3:]
    )
    relation = book_cross_relation((oriented,))
    assert verify_open(patch_for_cross(oriented), relation).satisfied
    assert not verify_open(patch_for_cross(same_histogram), relation).satisfied

    full = book_cross_relation(BINARY_TEMPLATES)
    empty = book_cross_relation(())
    for native in native_tiles(2, 2):
        assert generic_verify_periodic(encode_native(native), full).satisfied
        assert not generic_verify_periodic(encode_native(native), empty).satisfied

    return singleton_accepts, singleton_rejects, 1


def audit_rotation_commutation_and_orbits() -> tuple[int, int, int, int, int]:
    """Rotate support, exact templates, models, and full violation reports together."""

    profiles = direct_allowed_profiles()
    symmetry_commutations = 0
    symmetry_local_checks = 0
    support_transforms = 0
    for turns in (1, 2, 3):
        transformed = tuple(
            rotate_coordinate(offset, turns) for offset in BOOK_CROSS_OFFSETS
        )
        assert set(transformed) == set(BOOK_CROSS_OFFSETS)
        assert len(set(transformed)) == 5
        support_transforms += 1

    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for native in native_tiles(height, width):
            model = encode_native(native)
            for allowed in profiles:
                relation = book_cross_relation(tuple(allowed))
                original = generic_verify_periodic(model, relation)
                for turns in (1, 2, 3):
                    rotated_model = rotate_periodic(model, turns)
                    rotated_relation = rotate_cross_relation(relation, turns)
                    rotated = generic_verify_periodic(rotated_model, rotated_relation)
                    assert rotated.checked_anchors == original.checked_anchors
                    assert rotated.satisfied == original.satisfied
                    assert rotated.proves_global_model == original.proves_global_model
                    assert report_signature(rotated) == rotated_report_signature(
                        original,
                        turns,
                        rotated_model.periods,
                    )
                    assert rotate_periodic(rotated_model, (4 - turns) % 4) == model
                    assert rotate_cross_relation(
                        rotated_relation, (4 - turns) % 4
                    ) == relation
                    symmetry_commutations += 1
                    symmetry_local_checks += rotated.checked_anchors

    oriented = (1, 0, 0, 1, 0)
    rotated_oriented = rotate_cross_template(oriented, 1)
    assert rotated_oriented != oriented
    original_relation = book_cross_relation((oriented,))
    rotated_relation = rotate_cross_relation(original_relation, 1)
    assert verify_open(patch_for_cross(oriented), original_relation).satisfied
    assert not verify_open(
        patch_for_cross(rotated_oriented), original_relation
    ).satisfied
    assert verify_open(
        patch_for_cross(rotated_oriented), rotated_relation
    ).satisfied
    implicit_rotation_rejections = 1

    asymmetric = PeriodicPresentation(
        2,
        (
            (1, 0, 0),
            (0, 0, 0),
        ),
    )
    quarter_rotated = rotate_periodic(asymmetric, 1)
    assert asymmetric.periods == (2, 3)
    assert quarter_rotated.periods == (3, 2)
    assert not periodic_equal(asymmetric, quarter_rotated)
    assert same_rotation_orbit(asymmetric, quarter_rotated)
    assert generic_verify_periodic(
        asymmetric, book_cross_relation(BINARY_TEMPLATES)
    ).satisfied
    assert generic_verify_periodic(
        quarter_rotated, book_cross_relation(BINARY_TEMPLATES)
    ).satisfied
    explicit_orbit_witnesses = 1

    assert symmetry_commutations == 15_984
    assert symmetry_local_checks == 130_992
    return (
        support_transforms,
        symmetry_commutations,
        symmetry_local_checks,
        implicit_rotation_rejections,
        explicit_orbit_witnesses,
    )


def audit_reflection_and_label_exchange() -> tuple[int, int, int, int, int, int, int, int, int, int]:
    """Commute one det-negative support symmetry and binary label exchange."""

    profiles = direct_allowed_profiles()
    reflected_support = tuple(reflect_coordinate(offset) for offset in BOOK_CROSS_OFFSETS)
    assert set(reflected_support) == set(BOOK_CROSS_OFFSETS)
    assert tuple(reflect_coordinate(offset) for offset in reflected_support) == BOOK_CROSS_OFFSETS
    determinant_negative_support_transforms = 1
    assert exchange_binary_support(BOOK_CROSS_OFFSETS) == BOOK_CROSS_OFFSETS
    assert exchange_binary_anchor((7, -3)) == (7, -3)
    label_support_identity_transforms = 1
    reflection_commutations = 0
    reflection_local_checks = 0
    label_commutations = 0
    label_local_checks = 0

    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for native in native_tiles(height, width):
            model = encode_native(native)
            for allowed in profiles:
                relation = book_cross_relation(tuple(allowed))
                original = generic_verify_periodic(model, relation)

                reflected_model = reflect_periodic(model)
                reflected_relation = reflect_cross_relation(relation)
                reflected = generic_verify_periodic(
                    reflected_model,
                    reflected_relation,
                )
                assert reflected.checked_anchors == original.checked_anchors
                assert reflected.satisfied == original.satisfied
                assert reflected.proves_global_model == original.proves_global_model
                assert report_signature(reflected) == reflected_report_signature(
                    original,
                    reflected_model.periods,
                )
                assert reflect_periodic(reflected_model) == model
                assert reflect_cross_relation(reflected_relation) == relation
                reflection_commutations += 1
                reflection_local_checks += reflected.checked_anchors

                exchanged_model = exchange_binary_periodic(model)
                exchanged_relation = exchange_binary_relation(relation)
                exchanged = generic_verify_periodic(
                    exchanged_model,
                    exchanged_relation,
                )
                assert exchanged.checked_anchors == original.checked_anchors
                assert exchanged.satisfied == original.satisfied
                assert exchanged.proves_global_model == original.proves_global_model
                assert report_signature(exchanged) == exchanged_report_signature(original)
                assert exchange_binary_periodic(exchanged_model) == model
                assert exchange_binary_relation(exchanged_relation) == relation
                label_commutations += 1
                label_local_checks += exchanged.checked_anchors

    oriented = (1, 0, 0, 1, 0)
    relation = book_cross_relation((oriented,))
    reflected_template = reflect_cross_template(oriented)
    assert reflected_template != oriented
    assert not verify_open(patch_for_cross(reflected_template), relation).satisfied
    assert verify_open(
        patch_for_cross(reflected_template), reflect_cross_relation(relation)
    ).satisfied
    implicit_reflection_rejections = 1

    exchanged_template = exchange_binary_template(oriented)
    assert exchanged_template != oriented
    assert not verify_open(patch_for_cross(exchanged_template), relation).satisfied
    assert verify_open(
        patch_for_cross(exchanged_template), exchange_binary_relation(relation)
    ).satisfied
    implicit_label_exchange_rejections = 1

    reflection_model = PeriodicPresentation(
        2,
        (
            (1, 1, 0),
            (0, 0, 0),
        ),
    )
    reflected_model = reflect_periodic(reflection_model)
    assert not periodic_equal(reflection_model, reflected_model)
    assert same_reflection_orbit(reflection_model, reflected_model)
    reflection_orbit_witnesses = 1

    exchanged_model = exchange_binary_periodic(reflection_model)
    assert not periodic_equal(reflection_model, exchanged_model)
    assert same_binary_exchange_orbit(reflection_model, exchanged_model)
    label_exchange_orbit_witnesses = 1

    assert reflection_commutations == 5_328
    assert reflection_local_checks == 43_664
    assert label_commutations == 5_328
    assert label_local_checks == 43_664
    return (
        determinant_negative_support_transforms,
        label_support_identity_transforms,
        reflection_commutations,
        reflection_local_checks,
        label_commutations,
        label_local_checks,
        implicit_reflection_rejections,
        implicit_label_exchange_rejections,
        reflection_orbit_witnesses,
        label_exchange_orbit_witnesses,
    )


def audit_generic_slot_order_separation() -> tuple[int, int, int, int]:
    """Simultaneous offset/word permutation preserves denotation, not source IDs."""

    order = checked_slot_permutation(GENERIC_SLOT_PERMUTATION, 5)
    inverse = inverse_slot_permutation(order)
    assert order != tuple(range(5))
    assert tuple(order[index] for index in inverse) == tuple(range(5))

    profiles = direct_allowed_profiles()
    relation_round_trips = 0
    for allowed in profiles:
        relation = book_cross_relation(tuple(allowed))
        permuted = permute_relation_slots(relation, order)
        assert permuted.offsets != relation.offsets
        assert set(permuted.offsets) == set(relation.offsets)
        assert permute_relation_slots(permuted, inverse) == relation
        relation_round_trips += 1

    commutations = 0
    local_checks = 0
    for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)):
        for native in native_tiles(height, width):
            model = encode_native(native)
            for allowed in profiles:
                relation = book_cross_relation(tuple(allowed))
                permuted = permute_relation_slots(relation, order)
                original = generic_verify_periodic(model, relation)
                reordered = generic_verify_periodic(model, permuted)
                assert reordered.checked_anchors == original.checked_anchors
                assert reordered.satisfied == original.satisfied
                assert reordered.proves_global_model == original.proves_global_model
                assert report_signature(reordered) == permuted_report_signature(
                    original,
                    order,
                    relation.alphabet_size,
                )
                commutations += 1
                local_checks += reordered.checked_anchors

    source_relation = decode_constraint_number(1_384_774)
    representation_equivalent = permute_relation_slots(source_relation, order)
    assert representation_equivalent.offsets != BOOK_CROSS_OFFSETS
    expect_raises(
        ValueError,
        lambda: encode_constraint_number(representation_equivalent),
    )
    source_metadata_guards = 1

    assert relation_round_trips == len(profiles)
    assert commutations == 5_328
    assert local_checks == 43_664
    return relation_round_trips, commutations, local_checks, source_metadata_guards


def audit_alias_and_overlap() -> tuple[int, int, int, int]:
    one = NativeBinaryTorus(((1,),))
    assert direct_cross_at(one, (0, 0)) == (1, 1, 1, 1, 1)

    narrow = NativeBinaryTorus(((0, 1),))
    observed = direct_cross_at(narrow, (0, 0))
    assert observed == (0, 1, 0, 1, 0)
    assert len(observed) == 5
    assert len(set(observed)) == 2
    assert generic_read_periodic(
        encode_native(narrow),
        book_cross_relation(BINARY_TEMPLATES),
        (0, 0),
    ) == observed

    checker = PeriodicPresentation(2, ((0, 1), (1, 0)))
    relation = book_cross_relation(BINARY_TEMPLATES)
    actual = extracted_occurrences(checker, relation)
    assert len(actual) == 4
    assert occurrences_overlap_consistent(actual, relation, checker.periods)

    zero = (0, 0, 0, 0, 0)
    one_template = (1, 1, 1, 1, 1)
    independent_allowed = book_cross_relation((zero, one_template))
    conflicting = (
        ClaimedOccurrence((0, 0), zero),
        ClaimedOccurrence((0, 1), one_template),
    )
    assert all(independent_allowed.contains(item.template) for item in conflicting)
    assert not occurrences_overlap_consistent(conflicting, independent_allowed, (1, 2))

    alias_inconsistent = (0, 1, 0, 1, 0)
    alias_relation = book_cross_relation((alias_inconsistent,))
    assert occurrence_assignment(
        ClaimedOccurrence((0, 0), alias_inconsistent),
        alias_relation,
        (1, 1),
    ) is None
    assert not occurrences_overlap_consistent(
        (ClaimedOccurrence((0, 0), alias_inconsistent),),
        alias_relation,
        (1, 1),
    )
    return 2, len(actual), 1, 1


def audit_scopes_identity_and_solver() -> tuple[int, int, int, int, int]:
    full = book_cross_relation(BINARY_TEMPLATES)
    empty_patch = OpenPatch(2, (((0, 0), 0),))
    vacuous = verify_open(empty_patch, full)
    assert vacuous.checked_anchors == 0
    assert vacuous.satisfied
    assert not vacuous.proves_global_model

    template = (1, 0, 0, 1, 0)
    values = patch_for_cross(template).values
    window = FiniteWindow(2, ((0, 0),), values)
    scoped = verify_window(window, book_cross_relation((template,)))
    assert scoped.satisfied
    assert scoped.checked_anchors == 1
    assert not scoped.proves_global_model

    minimal = PeriodicPresentation(2, ((0, 1),))
    redundant = PeriodicPresentation(
        2,
        (
            (0, 1, 0, 1),
            (0, 1, 0, 1),
        ),
    )
    translated = PeriodicPresentation(2, ((1, 0),))
    assert minimal != redundant
    assert periodic_equal(minimal, redundant)
    assert not periodic_equal(minimal, translated)

    zeros = book_cross_relation(((0, 0, 0, 0, 0),))
    satisfiable = bounded_period_search(zeros, PeriodBoundQuery((1, 1)))
    assert type(satisfiable) is Satisfiable
    assert satisfiable.verification.proves_global_model
    assert satisfiable.explored_candidates == 1

    no_templates = book_cross_relation(())
    bounded_failure = bounded_period_search(no_templates, PeriodBoundQuery((1, 1)))
    assert type(bounded_failure) is Unknown
    assert bounded_failure.explored_candidates == 2
    assert "period" in bounded_failure.reason

    assert type(scoped) is Verification
    assert type(scoped) not in (Satisfiable, Unknown)

    t33_required = (1, 1, 1, 1, 1)
    all_zero_model = PeriodicPresentation(2, ((0,),))
    local_report = generic_verify_periodic(all_zero_model, full)
    assert local_report.satisfied
    assert t33_required not in {
        generic_read_periodic(all_zero_model, full, (0, 0))
    }
    # T32 accepts this model.  Adding the existential test would change the
    # denotation and is therefore T33, not a T32 flag.

    return 2, 3, satisfiable.explored_candidates, bounded_failure.explored_candidates, 1


def audit_general_footprint_parameterization() -> tuple[int, int]:
    offsets_3x3 = tuple(
        (delta_row, delta_column)
        for delta_row in (-1, 0, 1)
        for delta_column in (-1, 0, 1)
    )
    zero_3x3 = (0,) * 9
    relation_3x3 = AllowedOrientedTemplates(2, offsets_3x3, (zero_3x3,))
    assert generic_verify_periodic(
        PeriodicPresentation(2, ((0,),)), relation_3x3
    ).satisfied

    offsets_2x2 = ((0, 0), (0, 1), (1, 0), (1, 1))
    relation_16_color = AllowedOrientedTemplates(
        16,
        offsets_2x2,
        ((0, 1, 2, 3),),
    )
    observed = generic_read_periodic(
        PeriodicPresentation(16, ((0, 1), (2, 3))),
        relation_16_color,
        (0, 0),
    )
    assert observed == (0, 1, 2, 3)
    return len(offsets_3x3), relation_16_color.alphabet_size


def expect_raises(exception: type[BaseException], function: object) -> None:
    if not callable(function):
        raise TypeError("hostile test body must be callable")
    try:
        function()
    except exception:
        return
    except Exception as error:
        raise AssertionError(
            f"expected {exception.__name__}, got {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {exception.__name__}")


def audit_hostile_validation() -> int:
    hostile: tuple[tuple[type[BaseException], object], ...] = (
        (TypeError, lambda: AllowedOrientedTemplates(True, BOOK_CROSS_OFFSETS, ())),
        (ValueError, lambda: AllowedOrientedTemplates(0, BOOK_CROSS_OFFSETS, ())),
        (TypeError, lambda: AllowedOrientedTemplates(2, list(BOOK_CROSS_OFFSETS), ())),
        (ValueError, lambda: AllowedOrientedTemplates(2, (), ())),
        (ValueError, lambda: AllowedOrientedTemplates(2, ((0, 1),), ((0,),))),
        (ValueError, lambda: AllowedOrientedTemplates(2, ((0, 0), (0, 0)), ((0, 0),))),
        (ValueError, lambda: AllowedOrientedTemplates(2, ((0, 0, 0),), ((0,),))),
        (TypeError, lambda: AllowedOrientedTemplates(2, ((0, True), (0, 0)), ((0, 0),))),
        (TypeError, lambda: AllowedOrientedTemplates(2, BOOK_CROSS_OFFSETS, [])),
        (ValueError, lambda: book_cross_relation(((0, 0),))),
        (ValueError, lambda: book_cross_relation(((0, 0, 0, 0, 2),))),
        (TypeError, lambda: book_cross_relation(((0, 0, 0, 0, False),))),
        (ValueError, lambda: book_cross_relation(((0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))),
        (TypeError, lambda: book_cross_relation((lambda value: value,))),
        (TypeError, lambda: AllowedOrientedTemplates(2, BOOK_CROSS_OFFSETS, (), required=(0,) * 5)),
        (TypeError, lambda: PeriodicPresentation(2, [[0]])),
        (ValueError, lambda: PeriodicPresentation(2, ())),
        (ValueError, lambda: PeriodicPresentation(2, ((),))),
        (ValueError, lambda: PeriodicPresentation(2, ((0,), (0, 1)))),
        (ValueError, lambda: PeriodicPresentation(2, ((2,),))),
        (TypeError, lambda: PeriodicPresentation(2, ((False,),))),
        (TypeError, lambda: OpenPatch(2, [((0, 0), 0)])),
        (ValueError, lambda: OpenPatch(2, (((0, 0), 0), ((0, 0), 1)))),
        (ValueError, lambda: OpenPatch(2, (((0,), 0),))),
        (ValueError, lambda: OpenPatch(2, (((0, 0), 2),))),
        (ValueError, lambda: FiniteWindow(2, ((0, 0), (0, 0)), (((0, 0), 0),))),
        (ValueError, lambda: verify_window(FiniteWindow(2, ((0, 0),), (((0, 0), 0),)), book_cross_relation(BINARY_TEMPLATES))),
        (ValueError, lambda: generic_verify_periodic(PeriodicPresentation(1, ((0,),)), book_cross_relation(BINARY_TEMPLATES))),
        (TypeError, lambda: PeriodBoundQuery((True, 1))),
        (ValueError, lambda: PeriodBoundQuery((0, 1))),
        (ValueError, lambda: PeriodBoundQuery((1,))),
        (TypeError, lambda: direct_verify_periodic(NativeBinaryTorus(((0,),)), set())),
        (ValueError, lambda: matrix_to_cross(((1, 0, None), (0, 0, 1), (None, 0, None)))),
        (TypeError, lambda: occurrences_overlap_consistent([], book_cross_relation(BINARY_TEMPLATES), (1, 1))),
        (ValueError, lambda: occurrence_assignment(ClaimedOccurrence((0, 0), (0,) * 5), book_cross_relation(BINARY_TEMPLATES), (0, 1))),
        (TypeError, lambda: CenterConditionedHistogram(True, CARDINAL_NEIGHBOR_OFFSETS, ())),
        (ValueError, lambda: CenterConditionedHistogram(0, CARDINAL_NEIGHBOR_OFFSETS, ())),
        (TypeError, lambda: CenterConditionedHistogram(2, list(CARDINAL_NEIGHBOR_OFFSETS), ((), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, (), ((), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, ((0, 0),), ((), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, ((1, 0), (1, 0)), ((), ()))),
        (TypeError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, [(), ()])),
        (ValueError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, ((),))),
        (ValueError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, ((((4,),)), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, ((((5, -1),)), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, ((((3, 0),)), ()))),
        (ValueError, lambda: CenterConditionedHistogram(2, CARDINAL_NEIGHBOR_OFFSETS, ((((4, 0), (4, 0))), ()) )),
        (TypeError, lambda: compile_histogram_relation(book_cross_relation(()))),
        (ValueError, lambda: recover_histogram_relation(book_cross_relation(((1, 0, 0, 1, 0),)))),
        (TypeError, lambda: rotate_coordinate((0, 0), True)),
        (ValueError, lambda: rotate_coordinate((0, 0), 4)),
        (ValueError, lambda: rotate_cross_relation(AllowedOrientedTemplates(2, ((0, 0),), ((0,),)), 1)),
        (TypeError, lambda: same_rotation_orbit(PeriodicPresentation(2, ((0,),)), object())),
        (TypeError, lambda: decode_constraint_number(True)),
        (ValueError, lambda: decode_constraint_number(-1)),
        (ValueError, lambda: decode_constraint_number(2**32)),
        (TypeError, lambda: encode_constraint_number(object())),
        (ValueError, lambda: encode_constraint_number(AllowedOrientedTemplates(3, BOOK_CROSS_OFFSETS, ()))),
        (ValueError, lambda: encode_constraint_number(AllowedOrientedTemplates(2, ((0, 0),), ((0,),)))),
        (TypeError, lambda: book_row_column_to_enu((0, True))),
        (ValueError, lambda: enu_to_book_row_column((0,))),
        (TypeError, lambda: guarded_book_offset_repair(13513)),
        (ValueError, lambda: guarded_book_offset_repair(RAW_BOOK_OFFSET_FRAGMENT.replace("(-1, 0)", "{-1, 0}"))),
        (ValueError, lambda: reflect_cross_relation(AllowedOrientedTemplates(2, ((0, 0),), ((0,),)))),
        (ValueError, lambda: exchange_binary_periodic(PeriodicPresentation(3, ((0,),)))),
        (TypeError, lambda: checked_slot_permutation([0, 1], 2)),
        (ValueError, lambda: checked_slot_permutation((0, 0), 2)),
        (ValueError, lambda: checked_slot_permutation((0, 1), 3)),
    )
    for exception, function in hostile:
        expect_raises(exception, function)
    return len(hostile)


def audit_no_transition_surface() -> tuple[int, int, int]:
    relation_fields = {item.name for item in fields(AllowedOrientedTemplates)}
    histogram_fields = {item.name for item in fields(CenterConditionedHistogram)}
    verification_fields = {item.name for item in fields(Verification)}
    forbidden = {
        "seed",
        "time",
        "frontier",
        "active",
        "writes",
        "update",
        "successor",
        "schedule",
        "executor",
        "control",
    }
    assert relation_fields.isdisjoint(forbidden)
    assert histogram_fields.isdisjoint(forbidden)
    assert verification_fields.isdisjoint(forbidden)
    assert relation_fields == {"alphabet_size", "offsets", "allowed"}
    assert histogram_fields == {
        "alphabet_size",
        "neighbor_offsets",
        "allowed_by_center",
    }
    assert verification_fields == {
        "scope",
        "checked_anchors",
        "violations",
        "proves_global_model",
    }
    return len(relation_fields), len(histogram_fields), len(verification_fields)


EXPECTED_DIGEST = "72b671c04ac5e5a27ab1c2c2e86612b4ac1e493ab5722e89dc187b4d0939cbd5"


def main() -> None:
    source_claims = audit_source_claims()
    guarded_source_repairs = audit_guarded_source_repair()
    book_enu_adapter_round_trips = audit_book_enu_adapter()
    codec_round_trips = audit_cross_codec()
    (
        source_catalog_templates,
        numeric_singleton_round_trips,
        numeric_representative_round_trips,
        numeric_representative_counts,
    ) = audit_source_numeric_codec()
    configurations, commutations, local_checks, representation_round_trips = (
        audit_exhaustive_commutation()
    )
    (
        histogram_relations,
        histogram_round_trips,
        histogram_commutations,
        histogram_local_checks,
        oriented_recovery_rejections,
    ) = audit_histogram_compilation()
    singleton_accepts, singleton_rejects, orientation_counterexamples = (
        audit_exact_coverage_and_orientation()
    )
    (
        support_transforms,
        symmetry_commutations,
        symmetry_local_checks,
        implicit_rotation_rejections,
        explicit_orbit_witnesses,
    ) = audit_rotation_commutation_and_orbits()
    (
        reflection_support_transforms,
        label_support_identity_transforms,
        reflection_commutations,
        reflection_local_checks,
        label_exchange_commutations,
        label_exchange_local_checks,
        implicit_reflection_rejections,
        implicit_label_exchange_rejections,
        reflection_orbit_witnesses,
        label_exchange_orbit_witnesses,
    ) = audit_reflection_and_label_exchange()
    (
        slot_permutation_round_trips,
        slot_permutation_commutations,
        slot_permutation_local_checks,
        source_order_metadata_guards,
    ) = audit_generic_slot_order_separation()
    alias_cases, extracted, overlap_conflicts, alias_conflicts = audit_alias_and_overlap()
    scope_cases, identity_cases, sat_explored, unknown_explored, t33_boundaries = (
        audit_scopes_identity_and_solver()
    )
    larger_arity, larger_alphabet = audit_general_footprint_parameterization()
    hostile = audit_hostile_validation()
    relation_field_count, histogram_field_count, verification_field_count = (
        audit_no_transition_surface()
    )

    facts = (
        ("source_claims", source_claims),
        ("guarded_source_repairs", guarded_source_repairs),
        ("book_enu_adapter_round_trips", book_enu_adapter_round_trips),
        ("open_source_matters", len(OPEN_SOURCE_MATTERS)),
        ("strict_templates", len(BINARY_TEMPLATES)),
        ("strict_allowed_sets", 2 ** len(BINARY_TEMPLATES)),
        ("codec_round_trips", codec_round_trips),
        ("source_catalog_templates", source_catalog_templates),
        ("numeric_singleton_round_trips", numeric_singleton_round_trips),
        ("numeric_representative_round_trips", numeric_representative_round_trips),
        ("numeric_representative_counts", numeric_representative_counts),
        ("configurations", configurations),
        ("commutations", commutations),
        ("local_checks", local_checks),
        ("representation_round_trips", representation_round_trips),
        ("histogram_relations", histogram_relations),
        ("histogram_round_trips", histogram_round_trips),
        ("histogram_commutations", histogram_commutations),
        ("histogram_local_checks", histogram_local_checks),
        ("oriented_recovery_rejections", oriented_recovery_rejections),
        ("singleton_accepts", singleton_accepts),
        ("singleton_rejects", singleton_rejects),
        ("orientation_counterexamples", orientation_counterexamples),
        ("support_transforms", support_transforms),
        ("symmetry_commutations", symmetry_commutations),
        ("symmetry_local_checks", symmetry_local_checks),
        ("implicit_rotation_rejections", implicit_rotation_rejections),
        ("explicit_orbit_witnesses", explicit_orbit_witnesses),
        ("reflection_support_transforms", reflection_support_transforms),
        ("label_support_identity_transforms", label_support_identity_transforms),
        ("reflection_commutations", reflection_commutations),
        ("reflection_local_checks", reflection_local_checks),
        ("label_exchange_commutations", label_exchange_commutations),
        ("label_exchange_local_checks", label_exchange_local_checks),
        ("implicit_reflection_rejections", implicit_reflection_rejections),
        ("implicit_label_exchange_rejections", implicit_label_exchange_rejections),
        ("reflection_orbit_witnesses", reflection_orbit_witnesses),
        ("label_exchange_orbit_witnesses", label_exchange_orbit_witnesses),
        ("slot_permutation_round_trips", slot_permutation_round_trips),
        ("slot_permutation_commutations", slot_permutation_commutations),
        ("slot_permutation_local_checks", slot_permutation_local_checks),
        ("source_order_metadata_guards", source_order_metadata_guards),
        ("alias_cases", alias_cases),
        ("extracted_occurrences", extracted),
        ("overlap_conflicts", overlap_conflicts),
        ("alias_conflicts", alias_conflicts),
        ("scope_cases", scope_cases),
        ("identity_cases", identity_cases),
        ("sat_candidates", sat_explored),
        ("unknown_candidates", unknown_explored),
        ("t33_boundaries", t33_boundaries),
        ("larger_footprint_arity", larger_arity),
        ("larger_alphabet", larger_alphabet),
        ("hostile_rejections", hostile),
        ("relation_field_count", relation_field_count),
        ("histogram_field_count", histogram_field_count),
        ("verification_field_count", verification_field_count),
        ("architecture_classes", len(ARCHITECTURE_CLASSIFICATION)),
        ("strict_relation", "AllowedOrientedTemplates(raw_sorted_Book_row_column_cross)"),
        ("direction_names", "derived_only_by_(row,column)_to_(east=column,north=-row)_adapter"),
        ("numeric_codec", "source_descending_binary_catalog_plus_fixed_32_bit_positional_subset"),
        ("source_repair", SOURCE_REPAIRS),
        ("proof_envelope", "native_cross_to_generic_offsets_full_violation_report"),
        ("histogram_lowering", "T31_center_conditioned_histograms_losslessly_compile_to_T32_exact_words"),
        ("square_symmetry", "explicit_C4_support_template_model_report_commutation_without_implicit_matching"),
        ("extended_symmetry", "det_negative_reflection_and_binary_label_exchange_are_explicit_not_implicit"),
        ("order_separation", "generic_offset_word_permutation_preserves_denotation_but_not_NKS_numeric_metadata"),
        ("model_identity", "pointwise_equality_distinct_from_explicit_rotation_orbit_observer"),
        ("overlap_semantics", "one_pointwise_field_not_independent_template_tiles"),
        ("scope_semantics", "periodic_global_proof_open_local_finite_window"),
        ("solver_boundary", "verified_periodic_SAT_bounded_failure_Unknown"),
        ("t33_boundary", "existential_required_occurrence_is_not_T32"),
        ("source_claims_table", SOURCE_CLAIMS),
        ("open_source_matters_table", OPEN_SOURCE_MATTERS),
        ("architecture_classification", ARCHITECTURE_CLASSIFICATION),
        ("goal2_delta", GOAL2_DELTA),
    )
    digest = sha256(repr(facts).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        assert digest == EXPECTED_DIGEST

    print("T32 semantic oracle: PASS")
    print(
        f"source_claims={source_claims}; open_source_matters={len(OPEN_SOURCE_MATTERS)}; "
        f"strict_templates={len(BINARY_TEMPLATES)}; allowed_sets={2 ** len(BINARY_TEMPLATES)}; "
        f"book_ENU_adapter_round_trips={book_enu_adapter_round_trips}; "
        f"guarded_source_repairs={guarded_source_repairs}"
    )
    print(
        f"exhaustive_configurations={configurations}; commutations={commutations}; "
        f"local_checks={local_checks}; representation_round_trips={representation_round_trips}"
    )
    print(
        f"histogram_relations={histogram_relations}; histogram_round_trips={histogram_round_trips}; "
        f"histogram_commutations={histogram_commutations}; histogram_local_checks={histogram_local_checks}; "
        f"oriented_recovery_rejections={oriented_recovery_rejections}"
    )
    print(
        f"cross_codec_round_trips={codec_round_trips}; singleton_accepts={singleton_accepts}; "
        f"singleton_rejects={singleton_rejects}; orientation_counterexamples={orientation_counterexamples}"
    )
    print(
        f"source_catalog_templates={source_catalog_templates}; "
        f"numeric_singleton_round_trips={numeric_singleton_round_trips}; "
        f"numeric_representative_round_trips={numeric_representative_round_trips}; "
        f"representative_allowed_counts={numeric_representative_counts}"
    )
    print(
        f"support_rotations={support_transforms}; symmetry_commutations={symmetry_commutations}; "
        f"symmetry_local_checks={symmetry_local_checks}; "
        f"implicit_rotation_rejections={implicit_rotation_rejections}; "
        f"explicit_rotation_orbit_witnesses={explicit_orbit_witnesses}"
    )
    print(
        f"reflection_support_transforms={reflection_support_transforms}; "
        f"reflection_commutations={reflection_commutations}; "
        f"reflection_local_checks={reflection_local_checks}; "
        f"implicit_reflection_rejections={implicit_reflection_rejections}; "
        f"reflection_orbit_witnesses={reflection_orbit_witnesses}"
    )
    print(
        f"label_support_identity_transforms={label_support_identity_transforms}; "
        f"label_exchange_commutations={label_exchange_commutations}; "
        f"label_exchange_local_checks={label_exchange_local_checks}; "
        f"implicit_label_exchange_rejections={implicit_label_exchange_rejections}; "
        f"label_exchange_orbit_witnesses={label_exchange_orbit_witnesses}"
    )
    print(
        f"slot_permutation_round_trips={slot_permutation_round_trips}; "
        f"slot_permutation_commutations={slot_permutation_commutations}; "
        f"slot_permutation_local_checks={slot_permutation_local_checks}; "
        f"source_order_metadata_guards={source_order_metadata_guards}"
    )
    print(
        f"alias_cases={alias_cases}; extracted_occurrences={extracted}; "
        f"overlap_conflicts={overlap_conflicts}; alias_conflicts={alias_conflicts}"
    )
    print(
        f"scope_cases={scope_cases}; pointwise_identity_cases={identity_cases}; "
        f"solver_sat_candidates={sat_explored}; bounded_unknown_candidates={unknown_explored}; "
        f"t33_boundary_cases={t33_boundaries}"
    )
    print(
        f"generalized_profile=3x3/{larger_arity}-slots+{larger_alphabet}-colors; "
        f"hostile_rejections={hostile}; transition_surface=absent"
    )
    print(
        "architecture=D058_T31_class_4_declarative_nonfit_to_rollout_inherited; "
        "incremental_T32_delta=classes_1_2_3; no_new_class_4_or_execution_algebra"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
