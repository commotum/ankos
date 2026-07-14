#!/usr/bin/env python3
"""Dependency-free semantic oracle for T33 seeded template constraints.

T33 is not seeded in the event-zero sense.  Its strict denotation is the
conjunction of T32's translation-invariant allowed-local-pattern relation and
one global existential relation saying that a specified local pattern occurs
at some (unfixed) lattice anchor::

    Models(local AND Somewhere(required)) =
      {X | (forall p, observe(X,p) in local.allowed)
           and (exists q, observe(X,q) == required)}.

The occurrence anchor is a witness, not program data.  There is no native
time, seed, FRONTIER, RULE, UPDATE, successor, or solver.  The Book's
137,438,953,472 count is 32 * 2**32; constructor validity therefore cannot
require the marked template to belong to the allowed set.  An incompatible
marked template instead gives valid syntax with an empty model set.

Primary evidence reconstructed here:

* BOOK:2634 and 2640 require one specified allowed-shape template to occur at
  least somewhere; the picture merely displays its witness at the center.
* BOOK:2644-2658 separate constraint semantics from external search,
  backtracking, finite obstructions, and proof.
* BOOK:2664 treats a centered occurrence as the start of a search procedure,
  not as an initial configuration or a fixed semantic anchor.
* BOOK:2672-2678 give the translation qualification, the 12-template nested
  example, and the exact strict-family count 137,438,953,472.
* BOOK:2680-2694 generalize the same conjunction to complete 3x3 templates
  and relate two examples to rule-60/rule-30 spacetime fields.
* BOOK:14080-14083 make solver incompleteness explicit; BOOK:14097 evidences
  the finite conjunction variant in which every allowed template must occur.

This file is proof code, not a proposed runtime API.  It deliberately has no
third-party dependency and is silent when imported.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256
from itertools import product
from math import comb, lcm
from typing import TypeAlias


if not __debug__:
    raise RuntimeError("T33 semantic oracle must run with assertions enabled")


Coord2: TypeAlias = tuple[int, int]
Offset2: TypeAlias = tuple[int, int]
Template: TypeAlias = tuple[int, ...]
ValueTable: TypeAlias = tuple[tuple[Coord2, int], ...]

BOOK_CROSS_OFFSETS: tuple[Offset2, ...] = (
    (-1, 0),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, 0),
)
BINARY_CROSS_TEMPLATES: tuple[Template, ...] = tuple(product((0, 1), repeat=5))

SOURCE_CLAIMS = (
    ("BOOK:2634", "one specified local template must occur at least somewhere"),
    ("BOOK:2640", "the required template is shown at the center as a presentation choice"),
    ("BOOK:2644-2658", "finding or disproving a model is external solver/proof work"),
    ("BOOK:2664", "a centered occurrence initializes the described search, not model time"),
    ("BOOK:2672-2674", "twelve local templates plus one somewhere occurrence force the nested example"),
    ("BOOK:2674", "the claimed model is unique only up to translation"),
    ("BOOK:2678", "the strict marked-template family has 137438953472 records"),
    ("BOOK:2680-2684", "the same relation supports complete 3x3 words and a rule-60 encoding"),
    ("BOOK:2688-2694", "a 56-word relation plus first-word occurrence encodes rule-30 spacetime"),
    ("BOOK:14080-14083", "search, backtracking, bounds, undecidability, and NP-completeness are not semantics"),
    ("BOOK:14095", "the nonperiodic example retains arbitrary coordinate origin"),
    ("BOOK:14097", "the evidenced multi-requirement variant requires every allowed template somewhere"),
)

ARCHITECTURE_CLASSIFICATION = (
    "1: reuse T31/T32 static configurations, presentations, scopes, reports, query outcomes, witnesses, and certificates",
    "2: restrict the T32 model set by a closed global existential relation; an occurrence anchor is certificate data only",
    "3: add RequiredPatternSomewhere as a tagged declarative relation node and compose it with AllowedLocalPatterns",
    "4: inherit D058's declarative nonfit to rollout; T33 adds no new category or execution algebra",
)

GOAL2_DELTA = (
    "Build on the planned T31/T32 declarative layer; do not use src/ca/seeds.py or rollout.",
    "Add closed RequiredPatternSomewhere(template) and generic finite conjunction data, not a callback or T33 state class.",
    "Evaluate required occurrences from the same exact local words already read by AllowedLocalPatterns.",
    "Keep periodic-global, exact finite-window, and partial open-patch occurrence scopes explicit.",
    "Store occurrence anchors only in recheckable witnesses/reports; no semantic fixed anchor or hidden origin.",
    "Accept required-not-allowed syntax and return a replayable global emptiness certificate rather than constructor failure.",
    "Keep bounded periodic failure Unknown and search/backtracking state outside relation identity.",
    "Add explicit translation/D4/color transforms over local and required words; never enable implicit matching.",
    "Add no seed, time, FRONTIER, RULE, writes, UPDATE, successor, executor, family branch, or solver callback.",
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
        raise ValueError(f"{name} must have two coordinates")
    return exact_int(raw[0], f"{name}[0]"), exact_int(raw[1], f"{name}[1]")


def checked_alphabet_size(value: object) -> int:
    size = exact_int(value, "alphabet_size")
    if size <= 0:
        raise ValueError("alphabet_size must be positive")
    return size


def checked_label(value: object, alphabet_size: int, name: str) -> int:
    label = exact_int(value, name)
    if not 0 <= label < alphabet_size:
        raise ValueError(f"{name} is outside the declared alphabet")
    return label


def checked_offsets(value: object) -> tuple[Offset2, ...]:
    raw = exact_tuple(value, "offsets")
    if not raw:
        raise ValueError("offsets must be nonempty")
    offsets = tuple(checked_coord(item, "offset") for item in raw)
    if len(set(offsets)) != len(offsets):
        raise ValueError("offsets must be unique")
    if (0, 0) not in offsets:
        raise ValueError("offsets must contain the anchor offset")
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
        raise ValueError(f"{name} has the wrong arity")
    return tuple(
        checked_label(item, alphabet_size, f"{name}[{index}]")
        for index, item in enumerate(raw)
    )


@dataclass(frozen=True)
class AllowedLocalPatterns:
    """T32's finite exact local relation, with semantic support canonically sorted."""

    alphabet_size: int
    offsets: tuple[Offset2, ...]
    allowed: tuple[Template, ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        source_offsets = checked_offsets(self.offsets)
        offsets = tuple(sorted(source_offsets))
        source_index = {offset: index for index, offset in enumerate(source_offsets)}
        raw_allowed = exact_tuple(self.allowed, "allowed templates")
        allowed_list: list[Template] = []
        for item in raw_allowed:
            source_word = checked_template(
                item,
                size,
                len(offsets),
                name="allowed template",
            )
            allowed_list.append(
                tuple(source_word[source_index[offset]] for offset in offsets)
            )
        allowed = tuple(allowed_list)
        if len(set(allowed)) != len(allowed):
            raise ValueError("allowed templates must be unique")
        object.__setattr__(self, "offsets", offsets)
        object.__setattr__(self, "allowed", tuple(sorted(allowed)))

    def contains(self, value: object) -> bool:
        template = checked_template(
            value,
            self.alphabet_size,
            len(self.offsets),
            name="observed template",
        )
        return template in self.allowed


@dataclass(frozen=True)
class RequireEachPatternSomewhere:
    """Finite conjunction of global existential occurrence relations.

    The strict T33 constructor below requires exactly one entry.  An empty
    tuple is retained as the conjunction identity so the source-evidenced
    ``require every allowed word`` adapter remains total even for an empty
    allowed set; that vacuous record is extension data, not a strict T33 row.
    """

    templates: tuple[Template, ...]

    def __post_init__(self) -> None:
        raw = exact_tuple(self.templates, "required templates")
        entries = tuple(
            exact_tuple(item, "required template")
            for item in raw
        )
        object.__setattr__(self, "templates", tuple(sorted(set(entries))))


@dataclass(frozen=True)
class OccurrenceConstrainedPatterns:
    """Proof-model spelling of ``AllowedLocalPatterns AND requirements``."""

    local: AllowedLocalPatterns
    requirements: RequireEachPatternSomewhere

    def __post_init__(self) -> None:
        if type(self.local) is not AllowedLocalPatterns:
            raise TypeError("local must be exact AllowedLocalPatterns")
        if type(self.requirements) is not RequireEachPatternSomewhere:
            raise TypeError("requirements must be exact RequireEachPatternSomewhere")
        checked = tuple(
            checked_template(
                item,
                self.local.alphabet_size,
                len(self.local.offsets),
                name="required template",
            )
            for item in self.requirements.templates
        )
        object.__setattr__(
            self,
            "requirements",
            RequireEachPatternSomewhere(tuple(sorted(checked))),
        )


def strict_t33(
    local: AllowedLocalPatterns,
    required: object,
) -> OccurrenceConstrainedPatterns:
    """Construct the strict one-required-word T33 profile.

    Deliberately does *not* test membership in ``local.allowed``.  The Book's
    exact family count requires those incompatible records to remain
    well-formed, with empty denotation.
    """

    if type(local) is not AllowedLocalPatterns:
        raise TypeError("strict T33 requires AllowedLocalPatterns")
    template = checked_template(
        required,
        local.alphabet_size,
        len(local.offsets),
        name="required template",
    )
    return OccurrenceConstrainedPatterns(
        local,
        RequireEachPatternSomewhere((template,)),
    )


def require_every_allowed(
    local: AllowedLocalPatterns,
) -> OccurrenceConstrainedPatterns:
    """BOOK:14097's explicitly evidenced finite all-required variant."""

    if type(local) is not AllowedLocalPatterns:
        raise TypeError("all-required adapter requires AllowedLocalPatterns")
    return OccurrenceConstrainedPatterns(
        local,
        RequireEachPatternSomewhere(local.allowed),
    )


def forget_occurrences(
    relation: OccurrenceConstrainedPatterns,
) -> AllowedLocalPatterns:
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("forgetful projection requires occurrence-constrained relation")
    return relation.local


def book_cross_local(allowed: object) -> AllowedLocalPatterns:
    return AllowedLocalPatterns(2, BOOK_CROSS_OFFSETS, exact_tuple(allowed, "allowed"))


@dataclass(frozen=True)
class PeriodicPresentation:
    alphabet_size: int
    tile: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        rows = exact_tuple(self.tile, "tile")
        if not rows:
            raise ValueError("tile must have positive height")
        checked_rows: list[tuple[int, ...]] = []
        width: int | None = None
        for row_index, row in enumerate(rows):
            raw_row = exact_tuple(row, f"tile row {row_index}")
            if not raw_row:
                raise ValueError("tile must have positive width")
            if width is None:
                width = len(raw_row)
            elif len(raw_row) != width:
                raise ValueError("tile must be rectangular")
            checked_rows.append(
                tuple(
                    checked_label(item, size, f"tile[{row_index}][{column}]")
                    for column, item in enumerate(raw_row)
                )
            )
        object.__setattr__(self, "tile", tuple(checked_rows))

    @property
    def periods(self) -> tuple[int, int]:
        return len(self.tile), len(self.tile[0])

    def value_at(self, coordinate: object) -> int:
        row, column = checked_coord(coordinate, "coordinate")
        height, width = self.periods
        return self.tile[row % height][column % width]


def periodic_equal(left: object, right: object) -> bool:
    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("pointwise equality requires periodic presentations")
    if left.alphabet_size != right.alphabet_size:
        return False
    height = lcm(left.periods[0], right.periods[0])
    width = lcm(left.periods[1], right.periods[1])
    return all(
        left.value_at((row, column)) == right.value_at((row, column))
        for row in range(height)
        for column in range(width)
    )


def read_periodic(
    presentation: PeriodicPresentation,
    local: AllowedLocalPatterns,
    anchor: object,
) -> Template:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("periodic reader requires PeriodicPresentation")
    if type(local) is not AllowedLocalPatterns:
        raise TypeError("periodic reader requires AllowedLocalPatterns")
    if presentation.alphabet_size != local.alphabet_size:
        raise ValueError("presentation and relation alphabets differ")
    row, column = checked_coord(anchor, "anchor")
    return tuple(
        presentation.value_at((row + delta_row, column + delta_column))
        for delta_row, delta_column in local.offsets
    )


@dataclass(frozen=True)
class LocalViolation:
    anchor: Coord2
    observed: Template


@dataclass(frozen=True)
class OccurrenceHit:
    template: Template
    anchors: tuple[Coord2, ...]


@dataclass(frozen=True)
class Verification:
    scope: str
    checked_anchors: int
    occurrence_search_complete: bool
    local_violations: tuple[LocalViolation, ...]
    occurrence_hits: tuple[OccurrenceHit, ...]
    absent_required: tuple[Template, ...]
    not_observed_required: tuple[Template, ...]
    unresolved_required: tuple[Template, ...]
    proves_global_model: bool

    @property
    def locally_consistent(self) -> bool:
        return not self.local_violations

    @property
    def requirements_verified(self) -> bool:
        return not (
            self.absent_required
            or self.not_observed_required
            or self.unresolved_required
        )

    @property
    def refuted(self) -> bool:
        return bool(self.local_violations or self.absent_required)

    @property
    def status(self) -> str:
        if self.refuted:
            return "refuted"
        if self.proves_global_model:
            return "verified-global-model"
        if self.occurrence_search_complete and self.requirements_verified:
            return "verified-finite-scope"
        if self.not_observed_required:
            return "not-observed-in-finite-scope"
        return "undetermined"


def build_report(
    *,
    scope: str,
    anchors: tuple[Coord2, ...],
    words: tuple[Template, ...],
    relation: OccurrenceConstrainedPatterns,
    occurrence_search_complete: bool,
    global_scope: bool,
) -> Verification:
    if type(scope) is not str or not scope:
        raise TypeError("scope must be a nonempty string")
    if len(anchors) != len(words):
        raise ValueError("anchors and observed words must align")
    violations = tuple(
        LocalViolation(anchor, word)
        for anchor, word in zip(anchors, words)
        if word not in relation.local.allowed
    )
    hits = tuple(
        OccurrenceHit(
            required,
            tuple(anchor for anchor, word in zip(anchors, words) if word == required),
        )
        for required in relation.requirements.templates
    )
    absent = tuple(
        hit.template
        for hit in hits
        if global_scope and occurrence_search_complete and not hit.anchors
    )
    not_observed = tuple(
        hit.template
        for hit in hits
        if not global_scope and occurrence_search_complete and not hit.anchors
    )
    unresolved = tuple(
        hit.template
        for hit in hits
        if not occurrence_search_complete and not hit.anchors
    )
    proves_global = bool(
        global_scope and not violations and not absent and not unresolved
    )
    return Verification(
        scope,
        len(anchors),
        occurrence_search_complete,
        violations,
        hits,
        absent,
        not_observed,
        unresolved,
        proves_global,
    )


def verify_periodic(
    presentation: PeriodicPresentation,
    relation: OccurrenceConstrainedPatterns,
) -> Verification:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("periodic verifier requires PeriodicPresentation")
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("periodic verifier requires occurrence-constrained relation")
    if presentation.alphabet_size != relation.local.alphabet_size:
        raise ValueError("presentation and relation alphabets differ")
    height, width = presentation.periods
    anchors = tuple((row, column) for row in range(height) for column in range(width))
    words = tuple(read_periodic(presentation, relation.local, anchor) for anchor in anchors)
    return build_report(
        scope="periodic-global-proof",
        anchors=anchors,
        words=words,
        relation=relation,
        occurrence_search_complete=True,
        global_scope=True,
    )


def checked_value_table(value: object, alphabet_size: int, name: str) -> ValueTable:
    raw = exact_tuple(value, name)
    entries: list[tuple[Coord2, int]] = []
    seen: set[Coord2] = set()
    for index, item in enumerate(raw):
        pair = exact_tuple(item, f"{name}[{index}]")
        if len(pair) != 2:
            raise ValueError(f"{name} entries must be coordinate/label pairs")
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
            checked_value_table(self.values, size, "open-patch values"),
        )


@dataclass(frozen=True)
class FiniteWindow:
    alphabet_size: int
    anchors: tuple[Coord2, ...]
    values: ValueTable

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        raw_anchors = exact_tuple(self.anchors, "finite-window anchors")
        anchors = tuple(
            checked_coord(item, "finite-window anchor") for item in raw_anchors
        )
        if len(set(anchors)) != len(anchors):
            raise ValueError("finite-window anchors must be unique")
        object.__setattr__(self, "anchors", tuple(sorted(anchors)))
        object.__setattr__(
            self,
            "values",
            checked_value_table(self.values, size, "finite-window values"),
        )


def read_table(
    table: dict[Coord2, int],
    local: AllowedLocalPatterns,
    anchor: Coord2,
) -> Template | None:
    word: list[int] = []
    for delta_row, delta_column in local.offsets:
        coordinate = (anchor[0] + delta_row, anchor[1] + delta_column)
        if coordinate not in table:
            return None
        word.append(table[coordinate])
    return tuple(word)


def verify_open(
    patch: OpenPatch,
    relation: OccurrenceConstrainedPatterns,
) -> Verification:
    """Check every fully visible anchor; non-observation remains unresolved."""

    if type(patch) is not OpenPatch:
        raise TypeError("open verifier requires OpenPatch")
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("open verifier requires occurrence-constrained relation")
    if patch.alphabet_size != relation.local.alphabet_size:
        raise ValueError("patch and relation alphabets differ")
    table = dict(patch.values)
    anchors_and_words = tuple(
        (anchor, word)
        for anchor in sorted(table)
        for word in (read_table(table, relation.local, anchor),)
        if word is not None
    )
    return build_report(
        scope="open-partial-extension-check",
        anchors=tuple(item[0] for item in anchors_and_words),
        words=tuple(item[1] for item in anchors_and_words),
        relation=relation,
        occurrence_search_complete=False,
        global_scope=False,
    )


def verify_window(
    window: FiniteWindow,
    relation: OccurrenceConstrainedPatterns,
) -> Verification:
    """Verify the exact relation over the declared finite anchor set.

    A positive occurrence proves the finite existential clause.  Its absence
    refutes only this finite-window claim, never the infinite relation or the
    extendibility of the supplied values beyond the declared anchor set.
    """

    if type(window) is not FiniteWindow:
        raise TypeError("window verifier requires FiniteWindow")
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("window verifier requires occurrence-constrained relation")
    if window.alphabet_size != relation.local.alphabet_size:
        raise ValueError("window and relation alphabets differ")
    table = dict(window.values)
    words: list[Template] = []
    for anchor in window.anchors:
        word = read_table(table, relation.local, anchor)
        if word is None:
            raise ValueError("finite window is missing a declared anchor's halo")
        words.append(word)
    return build_report(
        scope="exact-finite-window",
        anchors=window.anchors,
        words=tuple(words),
        relation=relation,
        occurrence_search_complete=True,
        global_scope=False,
    )


@dataclass(frozen=True)
class OccurrenceWitness:
    template: Template
    anchor: Coord2

    def __post_init__(self) -> None:
        template = exact_tuple(self.template, "witness template")
        if any(type(item) is not int for item in template):
            raise TypeError("witness template entries must be exact ints")
        object.__setattr__(self, "template", template)
        object.__setattr__(self, "anchor", checked_coord(self.anchor, "witness anchor"))


def replay_occurrence_witness(
    relation: OccurrenceConstrainedPatterns,
    presentation: PeriodicPresentation,
    witness: OccurrenceWitness,
) -> bool:
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("witness replay requires occurrence-constrained relation")
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("witness replay requires PeriodicPresentation")
    if type(witness) is not OccurrenceWitness:
        raise TypeError("witness replay requires OccurrenceWitness")
    template = checked_template(
        witness.template,
        relation.local.alphabet_size,
        len(relation.local.offsets),
        name="witness template",
    )
    anchor = checked_coord(witness.anchor, "witness anchor")
    return bool(
        template in relation.requirements.templates
        and read_periodic(presentation, relation.local, anchor) == template
    )


@dataclass(frozen=True)
class NativeBinaryTorus:
    tile: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        checked = PeriodicPresentation(2, self.tile)
        object.__setattr__(self, "tile", checked.tile)

    @property
    def periods(self) -> tuple[int, int]:
        return len(self.tile), len(self.tile[0])


@dataclass(frozen=True)
class DirectStrictConstraint:
    allowed: frozenset[Template]
    required: Template

    def __post_init__(self) -> None:
        if type(self.allowed) is not frozenset:
            raise TypeError("direct allowed words must be a frozenset")
        allowed = frozenset(
            checked_template(item, 2, 5, name="direct allowed word")
            for item in self.allowed
        )
        required = checked_template(self.required, 2, 5, name="direct required word")
        object.__setattr__(self, "allowed", allowed)
        object.__setattr__(self, "required", required)


@dataclass(frozen=True)
class DirectViolation:
    anchor: Coord2
    observed: Template


@dataclass(frozen=True)
class DirectReport:
    checked_anchors: int
    local_violations: tuple[DirectViolation, ...]
    occurrence_anchors: tuple[Coord2, ...]
    required_absent: bool
    proves_global_model: bool


def direct_cross_word(native: NativeBinaryTorus, anchor: object) -> Template:
    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct reader requires NativeBinaryTorus")
    row, column = checked_coord(anchor, "direct anchor")
    height, width = native.periods
    return tuple(
        native.tile[(row + delta_row) % height][(column + delta_column) % width]
        for delta_row, delta_column in BOOK_CROSS_OFFSETS
    )


def direct_verify_periodic(
    native: NativeBinaryTorus,
    constraint: DirectStrictConstraint,
) -> DirectReport:
    if type(native) is not NativeBinaryTorus:
        raise TypeError("direct verifier requires NativeBinaryTorus")
    if type(constraint) is not DirectStrictConstraint:
        raise TypeError("direct verifier requires DirectStrictConstraint")
    height, width = native.periods
    violations: list[DirectViolation] = []
    hits: list[Coord2] = []
    for row in range(height):
        for column in range(width):
            anchor = (row, column)
            observed = direct_cross_word(native, anchor)
            if observed not in constraint.allowed:
                violations.append(DirectViolation(anchor, observed))
            if observed == constraint.required:
                hits.append(anchor)
    absent = not hits
    return DirectReport(
        height * width,
        tuple(violations),
        tuple(hits),
        absent,
        not violations and not absent,
    )


def encode_native(native: NativeBinaryTorus) -> PeriodicPresentation:
    if type(native) is not NativeBinaryTorus:
        raise TypeError("encoding requires NativeBinaryTorus")
    return PeriodicPresentation(2, native.tile)


def decode_native(presentation: PeriodicPresentation) -> NativeBinaryTorus:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("decoding requires PeriodicPresentation")
    if presentation.alphabet_size != 2:
        raise ValueError("native strict profile is binary")
    return NativeBinaryTorus(presentation.tile)


def encode_direct_constraint(
    constraint: DirectStrictConstraint,
) -> OccurrenceConstrainedPatterns:
    if type(constraint) is not DirectStrictConstraint:
        raise TypeError("constraint encoding requires DirectStrictConstraint")
    return strict_t33(book_cross_local(tuple(constraint.allowed)), constraint.required)


def normalized_direct(report: DirectReport) -> tuple[object, ...]:
    return (
        report.checked_anchors,
        tuple((item.anchor, item.observed) for item in report.local_violations),
        report.occurrence_anchors,
        report.required_absent,
        report.proves_global_model,
    )


def normalized_generic(report: Verification) -> tuple[object, ...]:
    if len(report.occurrence_hits) != 1:
        raise ValueError("strict normalization requires one occurrence relation")
    return (
        report.checked_anchors,
        tuple((item.anchor, item.observed) for item in report.local_violations),
        report.occurrence_hits[0].anchors,
        bool(report.absent_required),
        report.proves_global_model,
    )


@dataclass(frozen=True)
class RequiredOutsideAllowedCertificate:
    required: Template


@dataclass(frozen=True)
class CenterLabelObstructionCertificate:
    required: Template
    offending_offset: Offset2
    unavailable_center_label: int


EmptinessCertificate: TypeAlias = (
    RequiredOutsideAllowedCertificate | CenterLabelObstructionCertificate
)


def find_structural_emptiness_certificate(
    relation: OccurrenceConstrainedPatterns,
) -> EmptinessCertificate | None:
    """Find only two closed, independently replayable sufficient obstructions."""

    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("certificate search requires occurrence-constrained relation")
    local = relation.local
    center_index = local.offsets.index((0, 0))
    center_labels = {word[center_index] for word in local.allowed}
    for required in relation.requirements.templates:
        if required not in local.allowed:
            return RequiredOutsideAllowedCertificate(required)
        for offset, label in zip(local.offsets, required):
            if label not in center_labels:
                return CenterLabelObstructionCertificate(required, offset, label)
    return None


def replay_emptiness_certificate(
    relation: OccurrenceConstrainedPatterns,
    certificate: EmptinessCertificate,
) -> bool:
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("certificate replay requires occurrence-constrained relation")
    if type(certificate) is RequiredOutsideAllowedCertificate:
        required = checked_template(
            certificate.required,
            relation.local.alphabet_size,
            len(relation.local.offsets),
            name="certificate required template",
        )
        return bool(
            required in relation.requirements.templates
            and required not in relation.local.allowed
        )
    if type(certificate) is CenterLabelObstructionCertificate:
        required = checked_template(
            certificate.required,
            relation.local.alphabet_size,
            len(relation.local.offsets),
            name="certificate required template",
        )
        offset = checked_coord(certificate.offending_offset, "certificate offset")
        label = checked_label(
            certificate.unavailable_center_label,
            relation.local.alphabet_size,
            "certificate center label",
        )
        if required not in relation.requirements.templates:
            return False
        if required not in relation.local.allowed:
            return False
        if offset not in relation.local.offsets:
            return False
        offset_index = relation.local.offsets.index(offset)
        center_index = relation.local.offsets.index((0, 0))
        return bool(
            required[offset_index] == label
            and all(word[center_index] != label for word in relation.local.allowed)
        )
    raise TypeError("unknown emptiness certificate type")


@dataclass(frozen=True)
class PeriodicSearchQuery:
    periods: tuple[int, int]
    candidate_limit: int | None = None

    def __post_init__(self) -> None:
        raw = exact_tuple(self.periods, "query periods")
        if len(raw) != 2:
            raise ValueError("query periods must contain height and width")
        periods = tuple(exact_int(item, "query period") for item in raw)
        if any(item <= 0 for item in periods):
            raise ValueError("query periods must be positive")
        if self.candidate_limit is not None:
            limit = exact_int(self.candidate_limit, "candidate_limit")
            if limit <= 0:
                raise ValueError("candidate_limit must be positive")


@dataclass(frozen=True)
class Satisfiable:
    witness: PeriodicPresentation
    verification: Verification
    occurrence_witnesses: tuple[OccurrenceWitness, ...]
    explored_candidates: int


@dataclass(frozen=True)
class Unsatisfiable:
    certificate: EmptinessCertificate
    explored_candidates: int


@dataclass(frozen=True)
class Unknown:
    reason: str
    explored_periods: tuple[int, int]
    explored_candidates: int


@dataclass(frozen=True)
class ResourceLimit:
    reason: str
    explored_periods: tuple[int, int]
    explored_candidates: int


QueryOutcome: TypeAlias = Satisfiable | Unsatisfiable | Unknown | ResourceLimit


def bounded_period_search(
    relation: OccurrenceConstrainedPatterns,
    query: PeriodicSearchQuery,
) -> QueryOutcome:
    """Explicit test solver; bounded failure is Unknown, never global UNSAT."""

    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("search requires occurrence-constrained relation")
    if type(query) is not PeriodicSearchQuery:
        raise TypeError("search requires PeriodicSearchQuery")
    certificate = find_structural_emptiness_certificate(relation)
    if certificate is not None:
        assert replay_emptiness_certificate(relation, certificate)
        return Unsatisfiable(certificate, 0)
    height, width = query.periods
    explored = 0
    for flat in product(
        range(relation.local.alphabet_size),
        repeat=height * width,
    ):
        if query.candidate_limit is not None and explored >= query.candidate_limit:
            return ResourceLimit(
                "candidate limit reached before completing the declared period scope",
                query.periods,
                explored,
            )
        explored += 1
        tile = tuple(
            tuple(flat[row * width : (row + 1) * width])
            for row in range(height)
        )
        witness = PeriodicPresentation(relation.local.alphabet_size, tile)
        verification = verify_periodic(witness, relation)
        if verification.proves_global_model:
            witnesses = tuple(
                OccurrenceWitness(hit.template, hit.anchors[0])
                for hit in verification.occurrence_hits
            )
            assert all(
                replay_occurrence_witness(relation, witness, item)
                for item in witnesses
            )
            return Satisfiable(witness, verification, witnesses, explored)
    return Unknown(
        "no witness in the declared periodic scope",
        query.periods,
        explored,
    )


@dataclass(frozen=True)
class ExactTransform:
    """Closed D4 spatial transform plus a finite label permutation."""

    matrix: tuple[tuple[int, int], tuple[int, int]]
    label_permutation: tuple[int, ...]

    def __post_init__(self) -> None:
        raw_matrix = exact_tuple(self.matrix, "transform matrix")
        if len(raw_matrix) != 2:
            raise ValueError("transform matrix must have two rows")
        rows = tuple(
            tuple(exact_int(item, "matrix entry") for item in exact_tuple(row, "matrix row"))
            for row in raw_matrix
        )
        if any(len(row) != 2 for row in rows):
            raise ValueError("transform matrix must be 2x2")
        if rows not in D4_MATRICES:
            raise ValueError("transform matrix must be a signed axis permutation")
        permutation = exact_tuple(self.label_permutation, "label permutation")
        checked = tuple(exact_int(item, "label permutation entry") for item in permutation)
        if tuple(sorted(checked)) != tuple(range(len(checked))):
            raise ValueError("label permutation must be a finite bijection")
        object.__setattr__(self, "matrix", rows)
        object.__setattr__(self, "label_permutation", checked)


D4_MATRICES: tuple[tuple[tuple[int, int], tuple[int, int]], ...] = (
    ((1, 0), (0, 1)),
    ((0, -1), (1, 0)),
    ((-1, 0), (0, -1)),
    ((0, 1), (-1, 0)),
    ((1, 0), (0, -1)),
    ((-1, 0), (0, 1)),
    ((0, 1), (1, 0)),
    ((0, -1), (-1, 0)),
)


def apply_matrix(matrix: object, coordinate: object) -> Coord2:
    raw = exact_tuple(matrix, "matrix")
    if len(raw) != 2:
        raise ValueError("matrix must have two rows")
    first = exact_tuple(raw[0], "matrix row")
    second = exact_tuple(raw[1], "matrix row")
    if len(first) != 2 or len(second) != 2:
        raise ValueError("matrix must be 2x2")
    a, b, c, d = (
        exact_int(first[0], "matrix entry"),
        exact_int(first[1], "matrix entry"),
        exact_int(second[0], "matrix entry"),
        exact_int(second[1], "matrix entry"),
    )
    row, column = checked_coord(coordinate, "coordinate")
    return a * row + b * column, c * row + d * column


def inverse_matrix(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    if matrix not in D4_MATRICES:
        raise ValueError("inverse requires a D4 matrix")
    return (
        (matrix[0][0], matrix[1][0]),
        (matrix[0][1], matrix[1][1]),
    )


def transform_word(
    source_offsets: tuple[Offset2, ...],
    word: Template,
    transform: ExactTransform,
) -> tuple[tuple[Offset2, ...], Template]:
    if type(transform) is not ExactTransform:
        raise TypeError("word transform requires ExactTransform")
    if len(transform.label_permutation) <= max(word, default=-1):
        raise ValueError("label permutation does not cover the word alphabet")
    mapping = {
        apply_matrix(transform.matrix, offset): transform.label_permutation[label]
        for offset, label in zip(source_offsets, word)
    }
    target_offsets = tuple(sorted(mapping))
    return target_offsets, tuple(mapping[offset] for offset in target_offsets)


def transform_relation(
    relation: OccurrenceConstrainedPatterns,
    transform: ExactTransform,
) -> OccurrenceConstrainedPatterns:
    if type(relation) is not OccurrenceConstrainedPatterns:
        raise TypeError("relation transform requires occurrence-constrained relation")
    if len(transform.label_permutation) != relation.local.alphabet_size:
        raise ValueError("transform label permutation has the wrong alphabet")
    target_offsets = tuple(
        sorted(apply_matrix(transform.matrix, item) for item in relation.local.offsets)
    )
    transformed_allowed = tuple(
        transform_word(relation.local.offsets, word, transform)[1]
        for word in relation.local.allowed
    )
    transformed_required = tuple(
        transform_word(relation.local.offsets, word, transform)[1]
        for word in relation.requirements.templates
    )
    return OccurrenceConstrainedPatterns(
        AllowedLocalPatterns(
            relation.local.alphabet_size,
            target_offsets,
            transformed_allowed,
        ),
        RequireEachPatternSomewhere(transformed_required),
    )


def transform_periodic(
    presentation: PeriodicPresentation,
    transform: ExactTransform,
) -> PeriodicPresentation:
    if type(presentation) is not PeriodicPresentation:
        raise TypeError("model transform requires PeriodicPresentation")
    if len(transform.label_permutation) != presentation.alphabet_size:
        raise ValueError("transform label permutation has the wrong alphabet")
    old_height, old_width = presentation.periods
    matrix = transform.matrix
    new_height = old_height if matrix[0][0] else old_width
    new_width = old_height if matrix[1][0] else old_width
    inverse = inverse_matrix(matrix)
    tile = tuple(
        tuple(
            transform.label_permutation[
                presentation.value_at(apply_matrix(inverse, (row, column)))
            ]
            for column in range(new_width)
        )
        for row in range(new_height)
    )
    return PeriodicPresentation(presentation.alphabet_size, tile)


def translate_periodic(
    presentation: PeriodicPresentation,
    shift: object,
) -> PeriodicPresentation:
    """Return Y(p)=X(p-shift); T33 relation data is unchanged."""

    if type(presentation) is not PeriodicPresentation:
        raise TypeError("translation requires PeriodicPresentation")
    delta_row, delta_column = checked_coord(shift, "translation shift")
    height, width = presentation.periods
    return PeriodicPresentation(
        presentation.alphabet_size,
        tuple(
            tuple(
                presentation.value_at((row - delta_row, column - delta_column))
                for column in range(width)
            )
            for row in range(height)
        ),
    )


def same_explicit_transform_orbit(
    left: PeriodicPresentation,
    right: PeriodicPresentation,
) -> bool:
    """Observer only; never used by verification or pointwise identity."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("orbit observer requires periodic presentations")
    if left.alphabet_size != right.alphabet_size:
        return False
    identity_labels = tuple(range(left.alphabet_size))
    label_maps = (identity_labels,)
    if left.alphabet_size == 2:
        label_maps = (identity_labels, (1, 0))
    return any(
        periodic_equal(left, transform_periodic(right, ExactTransform(matrix, labels)))
        for matrix in D4_MATRICES
        for labels in label_maps
    )


def report_signature(report: Verification) -> tuple[object, ...]:
    if type(report) is not Verification:
        raise TypeError("report signature requires Verification")
    return (
        report.scope,
        report.checked_anchors,
        report.occurrence_search_complete,
        tuple((item.anchor, item.observed) for item in report.local_violations),
        tuple((item.template, item.anchors) for item in report.occurrence_hits),
        report.absent_required,
        report.not_observed_required,
        report.unresolved_required,
        report.proves_global_model,
        report.status,
    )


def transformed_report_signature(
    report: Verification,
    relation: OccurrenceConstrainedPatterns,
    presentation: PeriodicPresentation,
    transform: ExactTransform,
) -> tuple[object, ...]:
    """Map every coordinate/template payload in a periodic report."""

    if type(report) is not Verification:
        raise TypeError("report transform requires Verification")
    target_model = transform_periodic(presentation, transform)
    target_periods = target_model.periods

    def mapped_anchor(anchor: Coord2) -> Coord2:
        row, column = apply_matrix(transform.matrix, anchor)
        return row % target_periods[0], column % target_periods[1]

    def mapped_word(word: Template) -> Template:
        return transform_word(relation.local.offsets, word, transform)[1]

    violations = tuple(
        sorted(
            (mapped_anchor(item.anchor), mapped_word(item.observed))
            for item in report.local_violations
        )
    )
    hits = tuple(
        sorted(
            (
                mapped_word(item.template),
                tuple(sorted(mapped_anchor(anchor) for anchor in item.anchors)),
            )
            for item in report.occurrence_hits
        )
    )
    return (
        report.scope,
        report.checked_anchors,
        report.occurrence_search_complete,
        violations,
        hits,
        tuple(sorted(mapped_word(item) for item in report.absent_required)),
        tuple(sorted(mapped_word(item) for item in report.not_observed_required)),
        tuple(sorted(mapped_word(item) for item in report.unresolved_required)),
        report.proves_global_model,
        report.status,
    )


def translated_report_signature(
    report: Verification,
    presentation: PeriodicPresentation,
    shift: object,
) -> tuple[object, ...]:
    if type(report) is not Verification:
        raise TypeError("report translation requires Verification")
    delta_row, delta_column = checked_coord(shift, "translation shift")
    height, width = presentation.periods

    def moved(anchor: Coord2) -> Coord2:
        return (anchor[0] + delta_row) % height, (anchor[1] + delta_column) % width

    return (
        report.scope,
        report.checked_anchors,
        report.occurrence_search_complete,
        tuple(
            sorted((moved(item.anchor), item.observed) for item in report.local_violations)
        ),
        tuple(
            sorted(
                (item.template, tuple(sorted(moved(anchor) for anchor in item.anchors)))
                for item in report.occurrence_hits
            )
        ),
        report.absent_required,
        report.not_observed_required,
        report.unresolved_required,
        report.proves_global_model,
        report.status,
    )


@dataclass(frozen=True)
class PointDefectField:
    alphabet_size: int
    background: int
    defect_coordinate: Coord2
    defect_label: int

    def __post_init__(self) -> None:
        size = checked_alphabet_size(self.alphabet_size)
        checked_label(self.background, size, "background")
        checked_coord(self.defect_coordinate, "defect coordinate")
        checked_label(self.defect_label, size, "defect label")
        if self.background == self.defect_label:
            raise ValueError("point defect must differ from its background")

    def value_at(self, coordinate: object) -> int:
        point = checked_coord(coordinate, "point-defect coordinate")
        return self.defect_label if point == self.defect_coordinate else self.background


def read_point_defect(
    field: PointDefectField,
    local: AllowedLocalPatterns,
    anchor: object,
) -> Template:
    if type(field) is not PointDefectField:
        raise TypeError("point-defect reader requires PointDefectField")
    if field.alphabet_size != local.alphabet_size:
        raise ValueError("field and local relation alphabets differ")
    row, column = checked_coord(anchor, "point-defect anchor")
    return tuple(
        field.value_at((row + delta_row, column + delta_column))
        for delta_row, delta_column in local.offsets
    )


def native_tiles(height: int, width: int) -> tuple[NativeBinaryTorus, ...]:
    checked_height = exact_int(height, "tile height")
    checked_width = exact_int(width, "tile width")
    if checked_height <= 0 or checked_width <= 0:
        raise ValueError("tile periods must be positive")
    return tuple(
        NativeBinaryTorus(
            tuple(
                tuple(flat[row * checked_width : (row + 1) * checked_width])
                for row in range(checked_height)
            )
        )
        for flat in product((0, 1), repeat=checked_height * checked_width)
    )


def direct_allowed_profiles() -> tuple[frozenset[Template], ...]:
    return (
        frozenset(BINARY_CROSS_TEMPLATES),
        frozenset(),
        frozenset(word for word in BINARY_CROSS_TEMPLATES if word[2] == 0),
        frozenset(word for word in BINARY_CROSS_TEMPLATES if word[0] == word[3]),
        frozenset(word for word in BINARY_CROSS_TEMPLATES if sum(word) % 2 == 0),
        frozenset({(1, 0, 0, 1, 0)}),
        frozenset({(0, 0, 0, 0, 0), (1, 0, 0, 0, 0)}),
        frozenset(
            word
            for word in BINARY_CROSS_TEMPLATES
            if (word[0], word[1]) in ((0, 1), (1, 0))
        ),
    )


def audit_source_claims() -> int:
    assert len(SOURCE_CLAIMS) == 12
    assert SOURCE_CLAIMS[0][0] == "BOOK:2634"
    assert any(reference == "BOOK:2678" for reference, _ in SOURCE_CLAIMS)
    assert any(reference == "BOOK:14097" for reference, _ in SOURCE_CLAIMS)
    assert not any("initial condition" in fact for _, fact in SOURCE_CLAIMS)
    return len(SOURCE_CLAIMS)


def audit_strict_family_count() -> tuple[int, int, int, int]:
    local_words = 2**5
    allowed_masks = 2**local_words
    source_total = local_words * allowed_masks
    membership_conditioned = sum(
        comb(local_words, size) * size for size in range(local_words + 1)
    )
    incompatible_records = local_words * (2 ** (local_words - 1))
    assert local_words == 32
    assert allowed_masks == 4_294_967_296
    assert source_total == 137_438_953_472
    assert membership_conditioned == 68_719_476_736
    assert source_total == 2 * membership_conditioned
    assert incompatible_records == membership_conditioned

    empty_local = book_cross_local(())
    incompatible = strict_t33(empty_local, (0, 0, 0, 0, 0))
    certificate = find_structural_emptiness_certificate(incompatible)
    assert type(certificate) is RequiredOutsideAllowedCertificate
    assert replay_emptiness_certificate(incompatible, certificate)
    return source_total, membership_conditioned, incompatible_records, 1


def audit_exhaustive_periodic_commutation() -> tuple[int, int, int, int, int]:
    carriers = tuple(
        native
        for height, width in ((1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3))
        for native in native_tiles(height, width)
    )
    profiles = direct_allowed_profiles()
    constraints = tuple(
        DirectStrictConstraint(allowed, required)
        for allowed in profiles
        for required in BINARY_CROSS_TEMPLATES
    )
    encoded_constraints = tuple(encode_direct_constraint(item) for item in constraints)
    commutations = 0
    anchor_checks = 0
    model_implications = 0
    representation_round_trips = 0
    for native in carriers:
        presentation = encode_native(native)
        assert decode_native(presentation) == native
        representation_round_trips += 1
        for direct_constraint, generic_relation in zip(constraints, encoded_constraints):
            direct = direct_verify_periodic(native, direct_constraint)
            generic = verify_periodic(presentation, generic_relation)
            assert normalized_direct(direct) == normalized_generic(generic)
            assert generic.proves_global_model == (
                generic.locally_consistent and generic.requirements_verified
            )
            if generic.proves_global_model:
                model_implications += 1
                local_only = OccurrenceConstrainedPatterns(
                    generic_relation.local,
                    RequireEachPatternSomewhere(()),
                )
                assert verify_periodic(presentation, local_only).proves_global_model
            commutations += 1
            anchor_checks += generic.checked_anchors
    assert len(carriers) == 666
    assert len(constraints) == 256
    assert commutations == len(carriers) * len(constraints)
    return (
        len(carriers),
        len(constraints),
        commutations,
        anchor_checks,
        representation_round_trips,
    )


def audit_complete_toy_constraint_space() -> tuple[int, int, int, int]:
    offsets = ((0, 0),)
    words = ((0,), (1,))
    masks = tuple(
        tuple(word for index, word in enumerate(words) if mask & (1 << index))
        for mask in range(4)
    )
    constraints = tuple(
        strict_t33(AllowedLocalPatterns(2, offsets, allowed), required)
        for allowed in masks
        for required in words
    )
    models = tuple(
        encode_native(native)
        for height, width in ((1, 1), (1, 2), (2, 1), (2, 2))
        for native in native_tiles(height, width)
    )
    checks = 0
    for relation in constraints:
        for model in models:
            report = verify_periodic(model, relation)
            observed = tuple(
                model.value_at((row, column))
                for row in range(model.periods[0])
                for column in range(model.periods[1])
            )
            direct_local = all((label,) in relation.local.allowed for label in observed)
            direct_required = all(
                required[0] in observed for required in relation.requirements.templates
            )
            assert report.proves_global_model == (direct_local and direct_required)
            checks += 1

    all_required_checks = 0
    anchors_by_model = tuple(
        tuple(
            (row, column)
            for row in range(model.periods[0])
            for column in range(model.periods[1])
        )
        for model in models
    )
    for allowed in masks:
        relation = require_every_allowed(AllowedLocalPatterns(2, offsets, allowed))
        for model, anchors in zip(models, anchors_by_model):
            observed_words = tuple((model.value_at(anchor),) for anchor in anchors)
            report = verify_periodic(model, relation)
            expected_violations = tuple(
                (anchor, word)
                for anchor, word in zip(anchors, observed_words)
                if word not in allowed
            )
            expected_hits = tuple(
                (required, tuple(
                    anchor
                    for anchor, word in zip(anchors, observed_words)
                    if word == required
                ))
                for required in tuple(sorted(allowed))
            )
            expected_absent = tuple(
                required for required, hits in expected_hits if not hits
            )
            assert tuple(
                (item.anchor, item.observed) for item in report.local_violations
            ) == expected_violations
            assert tuple(
                (item.template, item.anchors) for item in report.occurrence_hits
            ) == expected_hits
            assert report.absent_required == expected_absent
            assert report.proves_global_model == (
                not expected_violations and not expected_absent
            )
            all_required_checks += 1
    assert len(models) == 26
    return len(constraints), len(models), checks, all_required_checks


def same_translation_orbit(
    left: PeriodicPresentation,
    right: PeriodicPresentation,
) -> bool:
    """Explicit observer; pointwise equality remains ``periodic_equal``."""

    if type(left) is not PeriodicPresentation or type(right) is not PeriodicPresentation:
        raise TypeError("translation-orbit observer requires periodic presentations")
    if left.alphabet_size != right.alphabet_size:
        return False
    height = lcm(left.periods[0], right.periods[0])
    width = lcm(left.periods[1], right.periods[1])
    return any(
        periodic_equal(left, translate_periodic(right, (row, column)))
        for row in range(height)
        for column in range(width)
    )


def word_patch(
    local: AllowedLocalPatterns,
    word: object,
    anchor: object = (0, 0),
) -> ValueTable:
    template = checked_template(
        word,
        local.alphabet_size,
        len(local.offsets),
        name="patch word",
    )
    row, column = checked_coord(anchor, "patch anchor")
    assignments: dict[Coord2, int] = {}
    for (delta_row, delta_column), label in zip(local.offsets, template):
        coordinate = (row + delta_row, column + delta_column)
        previous = assignments.get(coordinate)
        if previous is not None and previous != label:
            raise ValueError("word aliases one coordinate with inconsistent labels")
        assignments[coordinate] = label
    return tuple(sorted(assignments.items()))


def audit_projection_and_empty_models() -> tuple[int, int, int, int, int]:
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    required_one = (1, 1, 1, 1, 1)
    relation = strict_t33(full, required_one)
    zeros = PeriodicPresentation(2, ((0,),))
    ones = PeriodicPresentation(2, ((1,),))

    local_only = OccurrenceConstrainedPatterns(
        forget_occurrences(relation),
        RequireEachPatternSomewhere(()),
    )
    assert verify_periodic(zeros, local_only).proves_global_model
    assert not verify_periodic(zeros, relation).proves_global_model
    assert verify_periodic(ones, relation).proves_global_model
    assert forget_occurrences(strict_t33(full, (0, 0, 0, 0, 0))) == full
    assert relation != strict_t33(full, (0, 0, 0, 0, 0))

    # Compatible-but-empty T33: the local base admits the all-zero field and
    # contains the required word, but that word creates a north cell labelled
    # 1 while every allowed word requires center 0 at that neighboring anchor.
    all_zero = (0, 0, 0, 0, 0)
    north_one = (1, 0, 0, 0, 0)
    compatible_local = book_cross_local((all_zero, north_one))
    compatible_empty = strict_t33(compatible_local, north_one)
    assert verify_periodic(zeros, OccurrenceConstrainedPatterns(
        compatible_local, RequireEachPatternSomewhere(())
    )).proves_global_model
    assert north_one in compatible_local.allowed
    certificate = find_structural_emptiness_certificate(compatible_empty)
    assert type(certificate) is CenterLabelObstructionCertificate
    assert replay_emptiness_certificate(compatible_empty, certificate)

    outside = strict_t33(book_cross_local((all_zero,)), north_one)
    outside_certificate = find_structural_emptiness_certificate(outside)
    assert type(outside_certificate) is RequiredOutsideAllowedCertificate
    assert replay_emptiness_certificate(outside, outside_certificate)
    return 2, 1, 1, 1, 1


def audit_scopes_and_anchor_distinction() -> tuple[int, int, int, int, int, int]:
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    zero = (0, 0, 0, 0, 0)
    one = (1, 1, 1, 1, 1)
    zero_relation = strict_t33(full, zero)
    one_relation = strict_t33(full, one)
    values = word_patch(full, zero)

    positive_window = verify_window(
        FiniteWindow(2, ((0, 0),), values),
        zero_relation,
    )
    assert positive_window.status == "verified-finite-scope"
    assert positive_window.requirements_verified
    assert not positive_window.proves_global_model

    missing_window = verify_window(
        FiniteWindow(2, ((0, 0),), values),
        one_relation,
    )
    assert missing_window.status == "not-observed-in-finite-scope"
    assert missing_window.not_observed_required == (one,)
    assert not missing_window.absent_required
    assert not missing_window.refuted

    positive_open = verify_open(OpenPatch(2, values), zero_relation)
    assert positive_open.status == "undetermined"
    assert positive_open.requirements_verified
    assert not positive_open.proves_global_model

    missing_open = verify_open(OpenPatch(2, values), one_relation)
    assert missing_open.status == "undetermined"
    assert missing_open.unresolved_required == (one,)
    assert not missing_open.absent_required

    global_positive = verify_periodic(PeriodicPresentation(2, ((0,),)), zero_relation)
    global_negative = verify_periodic(PeriodicPresentation(2, ((0,),)), one_relation)
    assert global_positive.status == "verified-global-model"
    assert global_negative.status == "refuted"
    assert global_negative.absent_required == (one,)

    alternating = PeriodicPresentation(2, ((0, 1),))
    origin_word = read_periodic(alternating, full, (0, 0))
    other_word = read_periodic(alternating, full, (0, 1))
    assert origin_word != other_word
    anywhere = strict_t33(full, other_word)
    anywhere_report = verify_periodic(alternating, anywhere)
    assert anywhere_report.proves_global_model
    assert not replay_occurrence_witness(
        anywhere,
        alternating,
        OccurrenceWitness(other_word, (0, 0)),
    )
    assert replay_occurrence_witness(
        anywhere,
        alternating,
        OccurrenceWitness(other_word, (0, 1)),
    )
    return 2, 2, 2, 1, 1, 1


def audit_translation_gauge() -> tuple[int, int, int, int, int]:
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    models = tuple(native.tile for native in native_tiles(2, 3))
    shifts = ((0, 0), (0, 1), (1, 0), (1, 2), (-1, -1))
    commutations = 0
    anchor_maps = 0
    for tile in models:
        model = PeriodicPresentation(2, tile)
        required = read_periodic(model, full, (0, 0))
        relation = strict_t33(full, required)
        report = verify_periodic(model, relation)
        for shift in shifts:
            moved_model = translate_periodic(model, shift)
            moved_report = verify_periodic(moved_model, relation)
            assert report_signature(moved_report) == translated_report_signature(
                report,
                model,
                shift,
            )
            assert moved_report.proves_global_model == report.proves_global_model
            commutations += 1
            anchor_maps += sum(len(hit.anchors) for hit in moved_report.occurrence_hits)

    asymmetric = PeriodicPresentation(2, ((0, 0, 1), (1, 0, 1)))
    translated = translate_periodic(asymmetric, (0, 1))
    assert not periodic_equal(asymmetric, translated)
    assert same_translation_orbit(asymmetric, translated)
    relation_fields = {item.name for item in fields(OccurrenceConstrainedPatterns)}
    assert "anchor" not in relation_fields and "origin" not in relation_fields
    return len(models), len(shifts), commutations, anchor_maps, 1


def audit_symmetry_commutation() -> tuple[int, int, int, int, int, int, int]:
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    requirements = (
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (0, 1, 0, 1, 0),
        (1, 1, 0, 0, 1),
    )
    relations = tuple(strict_t33(full, word) for word in requirements)
    transforms = (
        ExactTransform(((0, -1), (1, 0)), (0, 1)),
        ExactTransform(((1, 0), (0, -1)), (0, 1)),
        ExactTransform(((1, 0), (0, 1)), (1, 0)),
    )
    models = tuple(
        encode_native(item)
        for height, width in ((2, 2), (2, 3))
        for item in native_tiles(height, width)
    )
    commutations = 0
    anchor_checks = 0
    for model in models:
        for relation in relations:
            original = verify_periodic(model, relation)
            for transform in transforms:
                mapped_model = transform_periodic(model, transform)
                mapped_relation = transform_relation(relation, transform)
                mapped = verify_periodic(mapped_model, mapped_relation)
                assert report_signature(mapped) == transformed_report_signature(
                    original,
                    relation,
                    model,
                    transform,
                )
                commutations += 1
                anchor_checks += mapped.checked_anchors

    asymmetric = PeriodicPresentation(2, ((0, 0, 1), (0, 1, 1)))
    reflected = transform_periodic(
        asymmetric,
        ExactTransform(((1, 0), (0, -1)), (0, 1)),
    )
    assert not periodic_equal(asymmetric, reflected)
    assert same_explicit_transform_orbit(asymmetric, reflected)
    exchanged = transform_periodic(asymmetric, transforms[2])
    assert not periodic_equal(asymmetric, exchanged)
    assert same_explicit_transform_orbit(asymmetric, exchanged)

    # Each evidenced transform is explicit: the old patch does not silently
    # match the transformed requirement, while transforming patch and relation
    # together restores the finite-scope witness.
    rejection_fixtures = (
        ((1, 0, 0, 0, 0), transforms[0]),  # quarter turn
        ((0, 1, 0, 0, 0), transforms[1]),  # determinant-negative reflection
        ((0, 0, 0, 0, 0), transforms[2]),  # black/white exchange
    )
    implicit_rejections = 0
    for required, transform in rejection_fixtures:
        relation = strict_t33(full, required)
        mapped_relation = transform_relation(relation, transform)
        original_window = FiniteWindow(2, ((0, 0),), word_patch(full, required))
        assert verify_window(original_window, relation).requirements_verified
        assert not verify_window(original_window, mapped_relation).requirements_verified
        mapped_values = tuple(
            sorted(
                (
                    apply_matrix(transform.matrix, coordinate),
                    transform.label_permutation[label],
                )
                for coordinate, label in original_window.values
            )
        )
        assert verify_window(
            FiniteWindow(2, ((0, 0),), mapped_values),
            mapped_relation,
        ).requirements_verified
        implicit_rejections += 1
    return (
        len(models),
        len(relations),
        len(transforms),
        commutations,
        anchor_checks,
        implicit_rejections,
        2,
    )


def audit_multiple_requirements_and_aliases() -> tuple[int, int, int, int, int, int, int]:
    self_local = AllowedLocalPatterns(2, ((0, 0),), ((0,), (1,)))
    all_required = require_every_allowed(self_local)
    alternating = PeriodicPresentation(2, ((0, 1),))
    report = verify_periodic(alternating, all_required)
    assert report.proves_global_model
    assert len(report.occurrence_hits) == 2
    assert report.occurrence_hits[0].anchors != report.occurrence_hits[1].anchors

    duplicated = OccurrenceConstrainedPatterns(
        self_local,
        RequireEachPatternSomewhere(((0,), (0,), (1,), (1,))),
    )
    assert duplicated == all_required

    vacuous = require_every_allowed(AllowedLocalPatterns(2, ((0, 0),), ()))
    assert not vacuous.requirements.templates
    assert vacuous != strict_t33(self_local, (0,))
    assert len(strict_t33(self_local, (0,)).requirements.templates) == 1

    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    period_one = PeriodicPresentation(2, ((0,),))
    alias_impossible = (0, 1, 0, 1, 0)
    alias_relation = strict_t33(full, alias_impossible)
    alias_report = verify_periodic(period_one, alias_relation)
    assert alias_report.locally_consistent
    assert alias_report.absent_required == (alias_impossible,)
    assert not alias_report.proves_global_model

    period_two = PeriodicPresentation(2, ((0, 1),))
    words = tuple(read_periodic(period_two, full, (0, column)) for column in range(2))
    multi = OccurrenceConstrainedPatterns(
        full,
        RequireEachPatternSomewhere(words),
    )
    multi_report = verify_periodic(period_two, multi)
    assert multi_report.proves_global_model
    assert len(multi_report.occurrence_hits) == 2
    forged = OccurrenceWitness(words[1], (0, 0))
    assert not replay_occurrence_witness(multi, period_two, forged)

    # An occurrence witness proves only its existential conjunct.  It must
    # remain replayable even when the same candidate violates the independent
    # T32 base relation; full verification composes those two facts.  Requiring
    # membership in local.allowed here would silently collapse valid
    # required-not-allowed syntax back to the rejected subset interpretation.
    zero = (0, 0, 0, 0, 0)
    one = (1, 1, 1, 1, 1)
    outside_relation = strict_t33(book_cross_local((zero,)), one)
    all_ones = PeriodicPresentation(2, ((1,),))
    assert one not in outside_relation.local.allowed
    assert replay_occurrence_witness(
        outside_relation,
        all_ones,
        OccurrenceWitness(one, (0, 0)),
    )
    outside_report = verify_periodic(all_ones, outside_relation)
    assert outside_report.requirements_verified
    assert not outside_report.locally_consistent
    assert not outside_report.proves_global_model
    return 2, 2, 1, 1, 2, 1, 1


def audit_nonlocality_counterexample() -> tuple[int, int, int, int]:
    """Show why the existential cannot be a finite local T32 matching flag.

    A local relation accepting a single-defect field necessarily observes and
    accepts the all-background word at anchors far from the defect.  It must
    therefore also accept the all-background field.  Yet the occurrence
    conjunct distinguishes those fields.  Moving the defect arbitrarily far
    additionally defeats any fixed-origin finite observation.
    """

    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    required = (0, 0, 1, 0, 0)
    relation = strict_t33(full, required)
    background_word = (0, 0, 0, 0, 0)
    radii = tuple(range(13))
    local_equalities = 0
    occurrence_witnesses = 0
    for radius in radii:
        defect = (3 * radius + 5, 0)
        field = PointDefectField(2, 0, defect, 1)
        for row in range(-radius, radius + 1):
            for column in range(-radius, radius + 1):
                assert read_point_defect(field, full, (row, column)) == background_word
                local_equalities += 1
        assert read_point_defect(field, full, defect) == required
        occurrence_witnesses += 1
    assert required in relation.requirements.templates
    assert background_word in relation.local.allowed
    assert required in relation.local.allowed
    # The all-zero periodic model is locally valid but fails the existential.
    zeros = PeriodicPresentation(2, ((0,),))
    assert verify_periodic(
        zeros,
        OccurrenceConstrainedPatterns(full, RequireEachPatternSomewhere(())),
    ).proves_global_model
    assert not verify_periodic(zeros, relation).proves_global_model
    return len(radii), local_equalities, occurrence_witnesses, 1


def audit_support_order_separation() -> tuple[int, int, int]:
    canonical_words = (
        (1, 0, 0, 1, 0),
        (0, 1, 1, 0, 1),
    )
    canonical = book_cross_local(canonical_words)
    source_offsets = tuple(reversed(BOOK_CROSS_OFFSETS))
    canonical_index = {offset: index for index, offset in enumerate(BOOK_CROSS_OFFSETS)}
    source_words = tuple(
        tuple(word[canonical_index[offset]] for offset in source_offsets)
        for word in canonical_words
    )
    reordered = AllowedLocalPatterns(2, source_offsets, source_words)
    assert reordered == canonical
    relation = strict_t33(canonical, canonical_words[0])
    reordered_relation = strict_t33(reordered, canonical_words[0])
    assert relation == reordered_relation

    model = PeriodicPresentation(2, ((0, 1), (1, 0)))
    assert report_signature(verify_periodic(model, relation)) == report_signature(
        verify_periodic(model, reordered_relation)
    )
    return len(source_offsets), len(source_words), 1


def audit_larger_support_and_alphabet() -> tuple[int, int, int]:
    """Exercise the BOOK:2680-2694 support generalization without raster data."""

    offsets_3x3 = tuple(
        (delta_row, delta_column)
        for delta_row in (-1, 0, 1)
        for delta_column in (-1, 0, 1)
    )
    zero_3x3 = (0,) * 9
    local_3x3 = AllowedLocalPatterns(2, offsets_3x3, (zero_3x3,))
    relation_3x3 = strict_t33(local_3x3, zero_3x3)
    assert verify_periodic(
        PeriodicPresentation(2, ((0,),)),
        relation_3x3,
    ).proves_global_model

    offsets_2x2 = ((0, 0), (0, 1), (1, 0), (1, 1))
    zero_2x2 = (0,) * 4
    local_16 = AllowedLocalPatterns(16, offsets_2x2, (zero_2x2,))
    relation_16 = strict_t33(local_16, zero_2x2)
    assert verify_periodic(
        PeriodicPresentation(16, ((0,),)),
        relation_16,
    ).proves_global_model
    return len(offsets_3x3), local_16.alphabet_size, 2


def audit_queries_and_certificates() -> tuple[int, int, int, int, int, int, int]:
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    zero = (0, 0, 0, 0, 0)
    one = (1, 1, 1, 1, 1)

    sat = bounded_period_search(strict_t33(full, zero), PeriodicSearchQuery((1, 1)))
    assert type(sat) is Satisfiable
    assert sat.explored_candidates == 1
    assert sat.verification.proves_global_model
    assert len(sat.occurrence_witnesses) == 1
    assert replay_occurrence_witness(
        strict_t33(full, zero),
        sat.witness,
        sat.occurrence_witnesses[0],
    )

    alias_word = (0, 1, 0, 1, 0)
    unknown = bounded_period_search(
        strict_t33(full, alias_word),
        PeriodicSearchQuery((1, 1)),
    )
    assert type(unknown) is Unknown
    assert unknown.explored_candidates == 2

    limited = bounded_period_search(
        strict_t33(full, one),
        PeriodicSearchQuery((1, 1), candidate_limit=1),
    )
    assert type(limited) is ResourceLimit
    assert limited.explored_candidates == 1

    outside = strict_t33(book_cross_local((zero,)), one)
    unsat_outside = bounded_period_search(outside, PeriodicSearchQuery((2, 2)))
    assert type(unsat_outside) is Unsatisfiable
    assert type(unsat_outside.certificate) is RequiredOutsideAllowedCertificate
    assert unsat_outside.explored_candidates == 0
    assert replay_emptiness_certificate(outside, unsat_outside.certificate)

    north_one = (1, 0, 0, 0, 0)
    center_obstructed = strict_t33(book_cross_local((zero, north_one)), north_one)
    unsat_center = bounded_period_search(
        center_obstructed,
        PeriodicSearchQuery((2, 2)),
    )
    assert type(unsat_center) is Unsatisfiable
    assert type(unsat_center.certificate) is CenterLabelObstructionCertificate
    assert replay_emptiness_certificate(center_obstructed, unsat_center.certificate)

    forged = CenterLabelObstructionCertificate(north_one, (0, 0), 0)
    assert not replay_emptiness_certificate(center_obstructed, forged)

    self_local = AllowedLocalPatterns(2, ((0, 0),), ((0,), (1,)))
    all_required = require_every_allowed(self_local)
    multi_sat = bounded_period_search(all_required, PeriodicSearchQuery((1, 2)))
    assert type(multi_sat) is Satisfiable
    assert len(multi_sat.occurrence_witnesses) == 2
    return 1, 2, 1, 2, 2, 1, 2


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
    zero = (0, 0, 0, 0, 0)
    full = book_cross_local(BINARY_CROSS_TEMPLATES)
    relation = strict_t33(full, zero)
    hostile: tuple[tuple[type[BaseException], object], ...] = (
        (TypeError, lambda: AllowedLocalPatterns(True, BOOK_CROSS_OFFSETS, ())),
        (ValueError, lambda: AllowedLocalPatterns(0, BOOK_CROSS_OFFSETS, ())),
        (TypeError, lambda: AllowedLocalPatterns(2, list(BOOK_CROSS_OFFSETS), ())),
        (ValueError, lambda: AllowedLocalPatterns(2, (), ())),
        (ValueError, lambda: AllowedLocalPatterns(2, ((1, 0),), ((0,),))),
        (ValueError, lambda: AllowedLocalPatterns(2, ((0, 0), (0, 0)), ((0, 0),))),
        (ValueError, lambda: AllowedLocalPatterns(2, ((0, 0, 0),), ((0,),))),
        (TypeError, lambda: AllowedLocalPatterns(2, ((0, True), (0, 0)), ((0, 0),))),
        (TypeError, lambda: AllowedLocalPatterns(2, BOOK_CROSS_OFFSETS, [])),
        (ValueError, lambda: book_cross_local(((0, 0),))),
        (ValueError, lambda: book_cross_local(((0, 0, 0, 0, 2),))),
        (TypeError, lambda: book_cross_local(((0, 0, 0, 0, False),))),
        (ValueError, lambda: book_cross_local((zero, zero))),
        (TypeError, lambda: book_cross_local((lambda item: item,))),
        (TypeError, lambda: RequireEachPatternSomewhere([zero])),
        (TypeError, lambda: RequireEachPatternSomewhere((lambda item: item,))),
        (TypeError, lambda: OccurrenceConstrainedPatterns(object(), RequireEachPatternSomewhere(()))),
        (TypeError, lambda: OccurrenceConstrainedPatterns(full, object())),
        (ValueError, lambda: strict_t33(full, (0, 0))),
        (ValueError, lambda: strict_t33(full, (0, 0, 0, 0, 2))),
        (TypeError, lambda: strict_t33(full, (0, 0, 0, 0, False))),
        (TypeError, lambda: strict_t33(full, zero, anchor=(0, 0))),
        (TypeError, lambda: forget_occurrences(full)),
        (TypeError, lambda: require_every_allowed(object())),
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
        (ValueError, lambda: verify_window(FiniteWindow(2, ((0, 0),), (((0, 0), 0),)), relation)),
        (ValueError, lambda: verify_periodic(PeriodicPresentation(1, ((0,),)), relation)),
        (TypeError, lambda: verify_periodic(object(), relation)),
        (TypeError, lambda: verify_periodic(PeriodicPresentation(2, ((0,),)), full)),
        (TypeError, lambda: OccurrenceWitness(list(zero), (0, 0))),
        (TypeError, lambda: replay_occurrence_witness(relation, PeriodicPresentation(2, ((0,),)), object())),
        (TypeError, lambda: PeriodicSearchQuery([1, 1])),
        (ValueError, lambda: PeriodicSearchQuery((0, 1))),
        (TypeError, lambda: PeriodicSearchQuery((True, 1))),
        (ValueError, lambda: PeriodicSearchQuery((1,))),
        (TypeError, lambda: PeriodicSearchQuery((1, 1), candidate_limit=True)),
        (ValueError, lambda: PeriodicSearchQuery((1, 1), candidate_limit=0)),
        (TypeError, lambda: bounded_period_search(relation, object())),
        (TypeError, lambda: replay_emptiness_certificate(relation, object())),
        (ValueError, lambda: ExactTransform(((1, 1), (0, 1)), (0, 1))),
        (TypeError, lambda: ExactTransform([[1, 0], [0, 1]], (0, 1))),
        (ValueError, lambda: ExactTransform(((1, 0), (0, 1)), (0, 0))),
        (TypeError, lambda: ExactTransform(((1, 0), (0, 1)), [0, 1])),
        (ValueError, lambda: transform_relation(relation, ExactTransform(((1, 0), (0, 1)), (0, 1, 2)))),
        (TypeError, lambda: translate_periodic(PeriodicPresentation(2, ((0,),)), (0, True))),
        (TypeError, lambda: periodic_equal(PeriodicPresentation(2, ((0,),)), object())),
        (ValueError, lambda: PointDefectField(2, 0, (0, 0), 0)),
        (TypeError, lambda: PointDefectField(2, False, (0, 0), 1)),
        (ValueError, lambda: word_patch(full, (0, 0))),
        (TypeError, lambda: DirectStrictConstraint(set(BINARY_CROSS_TEMPLATES), zero)),
        (TypeError, lambda: direct_verify_periodic(NativeBinaryTorus(((0,),)), object())),
        (ValueError, lambda: decode_native(PeriodicPresentation(3, ((0,),)))),
    )
    for exception, function in hostile:
        expect_raises(exception, function)

    # This is semantically inconsistent but explicitly valid syntax.
    incompatible = strict_t33(book_cross_local((zero,)), (1, 1, 1, 1, 1))
    assert type(find_structural_emptiness_certificate(incompatible)) is RequiredOutsideAllowedCertificate
    return len(hostile)


def audit_no_transition_surface() -> tuple[int, int, int, int]:
    local_fields = {item.name for item in fields(AllowedLocalPatterns)}
    requirement_fields = {item.name for item in fields(RequireEachPatternSomewhere)}
    conjunction_fields = {item.name for item in fields(OccurrenceConstrainedPatterns)}
    report_fields = {item.name for item in fields(Verification)}
    forbidden = {
        "seed",
        "initial_state",
        "time",
        "frontier",
        "active",
        "neighborhood",
        "rule",
        "writes",
        "update",
        "successor",
        "schedule",
        "executor",
        "solver",
        "anchor",
        "origin",
    }
    assert local_fields.isdisjoint(forbidden)
    assert requirement_fields.isdisjoint(forbidden)
    assert conjunction_fields.isdisjoint(forbidden)
    assert report_fields.isdisjoint(forbidden)
    assert local_fields == {"alphabet_size", "offsets", "allowed"}
    assert requirement_fields == {"templates"}
    assert conjunction_fields == {"local", "requirements"}
    assert report_fields == {
        "scope",
        "checked_anchors",
        "occurrence_search_complete",
        "local_violations",
        "occurrence_hits",
        "absent_required",
        "not_observed_required",
        "unresolved_required",
        "proves_global_model",
    }
    return len(local_fields), len(requirement_fields), len(conjunction_fields), len(report_fields)


EXPECTED_DIGEST = "54276cd1279b01e75ebe8495c528e5991f0b6c6387ec9744dc65db85539626e7"


def main() -> None:
    source_claims = audit_source_claims()
    (
        source_family_records,
        subset_conditioned_records,
        incompatible_syntax_records,
        incompatible_certificate_cases,
    ) = audit_strict_family_count()
    (
        configurations,
        strict_constraints,
        direct_generic_commutations,
        direct_generic_anchor_checks,
        representation_round_trips,
    ) = audit_exhaustive_periodic_commutation()
    (
        toy_constraints,
        toy_models,
        toy_singleton_checks,
        toy_all_required_checks,
    ) = audit_complete_toy_constraint_space()
    (
        projection_models,
        strict_subset_witnesses,
        compatible_empty_relations,
        outside_allowed_empty_relations,
        projection_noninjectivity_witnesses,
    ) = audit_projection_and_empty_models()
    (
        periodic_scope_cases,
        finite_window_cases,
        open_patch_cases,
        anywhere_not_anchor_cases,
        positive_window_witnesses,
        finite_nonobservation_cases,
    ) = audit_scopes_and_anchor_distinction()
    (
        translation_models,
        translation_shifts,
        translation_commutations,
        translated_anchor_witnesses,
        pointwise_orbit_separations,
    ) = audit_translation_gauge()
    (
        symmetry_models,
        symmetry_relations,
        explicit_transforms,
        symmetry_commutations,
        symmetry_anchor_checks,
        implicit_matching_rejections,
        explicit_orbit_witnesses,
    ) = audit_symmetry_commutation()
    (
        all_required_templates,
        separate_requirement_witnesses,
        duplicate_canonicalizations,
        vacuous_conjunction_normalizations,
        alias_cases,
        forged_witness_rejections,
        conjunct_local_witnesses,
    ) = audit_multiple_requirements_and_aliases()
    (
        nonlocal_radii,
        fixed_origin_local_equalities,
        arbitrarily_far_occurrence_witnesses,
        no_local_flag_counterexamples,
    ) = audit_nonlocality_counterexample()
    (
        reordered_support_slots,
        reordered_words,
        support_order_commutations,
    ) = audit_support_order_separation()
    larger_support_arity, larger_alphabet, generalized_profile_checks = (
        audit_larger_support_and_alphabet()
    )
    (
        sat_candidates,
        unknown_candidates,
        resource_candidates,
        outside_unsat_certificates,
        center_unsat_certificates,
        forged_certificates,
        multi_requirement_witnesses,
    ) = audit_queries_and_certificates()
    hostile_rejections = audit_hostile_validation()
    (
        local_field_count,
        requirement_field_count,
        conjunction_field_count,
        report_field_count,
    ) = audit_no_transition_surface()

    facts = (
        ("source_claims", source_claims),
        ("strict_cross_templates", len(BINARY_CROSS_TEMPLATES)),
        ("source_family_records", source_family_records),
        ("subset_conditioned_records", subset_conditioned_records),
        ("incompatible_syntax_records", incompatible_syntax_records),
        ("incompatible_certificate_cases", incompatible_certificate_cases),
        ("configurations", configurations),
        ("strict_constraints", strict_constraints),
        ("direct_generic_commutations", direct_generic_commutations),
        ("direct_generic_anchor_checks", direct_generic_anchor_checks),
        ("representation_round_trips", representation_round_trips),
        ("toy_constraints", toy_constraints),
        ("toy_models", toy_models),
        ("toy_singleton_checks", toy_singleton_checks),
        ("toy_all_required_checks", toy_all_required_checks),
        ("projection_models", projection_models),
        ("strict_subset_witnesses", strict_subset_witnesses),
        ("compatible_empty_relations", compatible_empty_relations),
        ("outside_allowed_empty_relations", outside_allowed_empty_relations),
        ("projection_noninjectivity_witnesses", projection_noninjectivity_witnesses),
        ("periodic_scope_cases", periodic_scope_cases),
        ("finite_window_cases", finite_window_cases),
        ("open_patch_cases", open_patch_cases),
        ("anywhere_not_anchor_cases", anywhere_not_anchor_cases),
        ("positive_window_witnesses", positive_window_witnesses),
        ("finite_nonobservation_cases", finite_nonobservation_cases),
        ("translation_models", translation_models),
        ("translation_shifts", translation_shifts),
        ("translation_commutations", translation_commutations),
        ("translated_anchor_witnesses", translated_anchor_witnesses),
        ("pointwise_orbit_separations", pointwise_orbit_separations),
        ("symmetry_models", symmetry_models),
        ("symmetry_relations", symmetry_relations),
        ("explicit_transforms", explicit_transforms),
        ("symmetry_commutations", symmetry_commutations),
        ("symmetry_anchor_checks", symmetry_anchor_checks),
        ("implicit_matching_rejections", implicit_matching_rejections),
        ("explicit_orbit_witnesses", explicit_orbit_witnesses),
        ("all_required_templates", all_required_templates),
        ("separate_requirement_witnesses", separate_requirement_witnesses),
        ("duplicate_canonicalizations", duplicate_canonicalizations),
        ("vacuous_conjunction_normalizations", vacuous_conjunction_normalizations),
        ("alias_cases", alias_cases),
        ("forged_witness_rejections", forged_witness_rejections),
        ("conjunct_local_witnesses", conjunct_local_witnesses),
        ("nonlocal_radii", nonlocal_radii),
        ("fixed_origin_local_equalities", fixed_origin_local_equalities),
        ("arbitrarily_far_occurrence_witnesses", arbitrarily_far_occurrence_witnesses),
        ("no_local_flag_counterexamples", no_local_flag_counterexamples),
        ("reordered_support_slots", reordered_support_slots),
        ("reordered_words", reordered_words),
        ("support_order_commutations", support_order_commutations),
        ("larger_support_arity", larger_support_arity),
        ("larger_alphabet", larger_alphabet),
        ("generalized_profile_checks", generalized_profile_checks),
        ("sat_candidates", sat_candidates),
        ("unknown_candidates", unknown_candidates),
        ("resource_candidates", resource_candidates),
        ("outside_unsat_certificates", outside_unsat_certificates),
        ("center_unsat_certificates", center_unsat_certificates),
        ("forged_certificates", forged_certificates),
        ("multi_requirement_witnesses", multi_requirement_witnesses),
        ("hostile_rejections", hostile_rejections),
        ("local_field_count", local_field_count),
        ("requirement_field_count", requirement_field_count),
        ("conjunction_field_count", conjunction_field_count),
        ("report_field_count", report_field_count),
        ("source_claims_table", SOURCE_CLAIMS),
        ("architecture_classification", ARCHITECTURE_CLASSIFICATION),
        ("goal2_delta", GOAL2_DELTA),
        ("strict_denotation", "AllowedLocalPatterns_AND_exists_anchor_exact_required_word"),
        ("all_required_denotation", "finite_conjunction_of_independent_exists_anchor_relations"),
        ("empty_requirement_identity", "generic_conjunction_identity_normalizes_behaviorally_to_T32_not_strict_T33"),
        ("counting_seam", "32_times_2^32_accepts_required_outside_allowed_as_well_formed_empty_syntax"),
        ("anchor_boundary", "witness_and_translation_gauge_not_relation_data_or_initial_state"),
        ("scope_boundary", "periodic_global_vs_finite_not_observed_vs_open_unresolved"),
        ("projection_boundary", "forget_requirements_is_sound_noninjective_and_strict_on_models"),
        ("nonlocal_boundary", "global_existential_cannot_be_a_finite_local_matching_flag"),
        ("solver_boundary", "rechecked_SAT_replayed_UNSAT_bounded_Unknown_typed_ResourceLimit"),
        ("transition_surface", "absent"),
    )
    digest = sha256(repr(facts).encode("utf-8")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        assert digest == EXPECTED_DIGEST

    print("T33 semantic oracle: PASS")
    print(
        f"source_claims={source_claims}; strict_templates={len(BINARY_CROSS_TEMPLATES)}; "
        f"source_family_records={source_family_records}; "
        f"subset_conditioned_records={subset_conditioned_records}; "
        f"well_formed_required_outside_allowed={incompatible_syntax_records}"
    )
    print(
        f"configurations={configurations}; strict_constraints={strict_constraints}; "
        f"direct_generic_full_report_commutations={direct_generic_commutations}; "
        f"anchor_checks={direct_generic_anchor_checks}; "
        f"representation_round_trips={representation_round_trips}"
    )
    print(
        f"complete_self_support_constraints={toy_constraints}; toy_models={toy_models}; "
        f"singleton_checks={toy_singleton_checks}; "
        f"all_required_checks={toy_all_required_checks}"
    )
    print(
        f"translation_models={translation_models}; shifts={translation_shifts}; "
        f"translation_report_commutations={translation_commutations}; "
        f"translated_occurrence_anchors={translated_anchor_witnesses}; "
        f"pointwise_vs_translation_orbit={pointwise_orbit_separations}"
    )
    print(
        f"symmetry_models={symmetry_models}; symmetry_relations={symmetry_relations}; "
        f"D4_color_transforms={explicit_transforms}; "
        f"symmetry_report_commutations={symmetry_commutations}; "
        f"symmetry_anchor_checks={symmetry_anchor_checks}; "
        f"implicit_matching_rejections={implicit_matching_rejections}; "
        f"explicit_orbit_witnesses={explicit_orbit_witnesses}"
    )
    print(
        f"periodic_scope={periodic_scope_cases}; finite_window_scope={finite_window_cases}; "
        f"open_patch_scope={open_patch_cases}; anywhere_not_anchor={anywhere_not_anchor_cases}; "
        f"finite_positive={positive_window_witnesses}; "
        f"finite_not_observed={finite_nonobservation_cases}"
    )
    print(
        f"projection_models={projection_models}; strict_subset={strict_subset_witnesses}; "
        f"compatible_but_empty={compatible_empty_relations}; "
        f"required_outside_allowed_empty={outside_allowed_empty_relations}; "
        f"projection_noninjective={projection_noninjectivity_witnesses}"
    )
    print(
        f"all_required_templates={all_required_templates}; "
        f"separate_witnesses={separate_requirement_witnesses}; "
        f"duplicate_canonicalizations={duplicate_canonicalizations}; "
        f"empty_conjunction_T32_identity={vacuous_conjunction_normalizations}; "
        f"alias_cases={alias_cases}; forged_witness_rejections={forged_witness_rejections}; "
        f"conjunct_local_witnesses={conjunct_local_witnesses}"
    )
    print(
        f"nonlocal_radii={nonlocal_radii}; fixed_origin_equalities={fixed_origin_local_equalities}; "
        f"arbitrarily_far_witnesses={arbitrarily_far_occurrence_witnesses}; "
        f"finite_local_flag_counterexamples={no_local_flag_counterexamples}; "
        f"support_order_commutations={support_order_commutations}; "
        f"generalized_profile=3x3/{larger_support_arity}-slots+{larger_alphabet}-colors; "
        f"generalized_checks={generalized_profile_checks}"
    )
    print(
        f"solver_sat_candidates={sat_candidates}; bounded_unknown_candidates={unknown_candidates}; "
        f"resource_candidates={resource_candidates}; "
        f"global_unsat_certificates={outside_unsat_certificates + center_unsat_certificates}; "
        f"forged_certificate_rejections={forged_certificates}; "
        f"multi_requirement_witnesses={multi_requirement_witnesses}"
    )
    print(
        f"hostile_rejections={hostile_rejections}; transition_surface=absent; "
        "architecture=D058_T31_T32_declarative_category_reused; "
        "incremental_T33_delta=classes_1_2_3_only"
    )
    print(f"semantic_digest={digest}")


if __name__ == "__main__":
    main()
