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
        and template in relation.local.allowed
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
