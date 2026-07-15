#!/usr/bin/env python3
"""Synthetic success and mutation tests for the Stage 4 overlay engine."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "goal-4" / "tools"))

from overlay_lib import (  # noqa: E402
    ApplicationAuthority,
    AnchoredInsert,
    AuthorityGrant,
    Block,
    CANONICAL_AUTHOR_TEXT,
    DERIVED_AGGREGATE,
    Delete,
    DependencyError,
    EDITORIAL_SIDECAR,
    EvidenceError,
    FORMULA_OR_SYMBOL,
    GENERATED_METADATA,
    GuardError,
    IndependentReview,
    InverseError,
    MARKDOWN_STRUCTURE,
    Merge,
    Move,
    NAVIGATION_METADATA,
    OperationMeta,
    OverlayState,
    PROSE_OCR,
    ReplayResult,
    Replace,
    RoleError,
    SEARCH_DERIVATIVE,
    SEARCH_NORMALIZATION,
    SOURCE_ERRATUM_ANNOTATION,
    STRUCTURE_BOUNDARY,
    SchemaError,
    Split,
    WitnessEvidence,
    apply_overlays,
    inverse_replay,
    sha256_bytes,
    target_sha256,
    test_only_application_authority,
)


CREATOR = "principal-creator"
SOURCE_REVIEWER = "principal-source-reviewer"
SPECIALIST = "principal-specialist"
VIEW_SHA256 = sha256_bytes(b"sealed evidence view")
REGION_SHA256 = sha256_bytes(b"edition-identical page region")
TEST_TARGET = "CHAPTER-01"


def state_for(
    blocks: tuple[Block, ...],
    role: str = CANONICAL_AUTHOR_TEXT,
    target_id: str = TEST_TARGET,
    **extra_targets: tuple[Block, ...],
) -> OverlayState:
    targets: dict[tuple[str, str], tuple[Block, ...]] = {(target_id, role): blocks}
    targets.update({(target_id, extra_role): value for extra_role, value in extra_targets.items()})
    return OverlayState.from_mapping(targets)


def witness(**changes: object) -> WitnessEvidence:
    values: dict[str, object] = {
        "witness_id": "OFFICIAL-PRINT-1",
        "edition_id": "FIRST-EDITION-FOURTH-PRINTING",
        "region_id": "PAGE-0042-REGION-01",
        "region_sha256": REGION_SHA256,
        "evidence_view_sha256": VIEW_SHA256,
        "authorized": True,
        "edition_identical": True,
        "legible_for_change": True,
    }
    values.update(changes)
    return WitnessEvidence(**values)  # type: ignore[arg-type]


def review(*, high_risk: bool = False, **changes: object) -> IndependentReview:
    values: dict[str, object] = {
        "review_id": "REVIEW-SOURCE-0001",
        "creator_principal_id": CREATOR,
        "source_reviewer_principal_id": SOURCE_REVIEWER,
        "source_reviewer_type": "AGENT",
        "source_reviewer_session_id": "source-session-1",
        "source_reviewer_role": "SOURCE_REVIEWER",
        "source_decision": "APPROVED",
        "evidence_view_sha256": VIEW_SHA256,
        "blind_preproposal": high_risk,
        "specialist_review_id": "REVIEW-SPECIALIST-0001" if high_risk else None,
        "specialist_principal_id": SPECIALIST if high_risk else None,
        "specialist_type": "AGENT" if high_risk else None,
        "specialist_session_id": "specialist-session-1" if high_risk else None,
        "specialist_decision": "APPROVED" if high_risk else None,
        "specialist_evidence_view_sha256": VIEW_SHA256 if high_risk else None,
    }
    values.update(changes)
    return IndependentReview(**values)  # type: ignore[arg-type]


def meta_for(
    before: OverlayState,
    after: tuple[Block, ...],
    *,
    repair_id: str,
    role: str = CANONICAL_AUTHOR_TEXT,
    target_id: str = TEST_TARGET,
    repair_class: str = PROSE_OCR,
    dependencies: tuple[str, ...] = (),
    author_evidence: bool = True,
    high_risk_review: bool = True,
    witness_value: WitnessEvidence | None = None,
    review_value: IndependentReview | None = None,
) -> OperationMeta:
    if author_evidence:
        witness_value = witness_value if witness_value is not None else witness()
        review_value = review_value if review_value is not None else review(high_risk=high_risk_review)
        disposition = "APPLIED_WITNESS_VERIFIED"
    else:
        disposition = "APPLIED_MECHANICALLY_PROVEN"
    return OperationMeta(
        repair_id=repair_id,
        target_id=target_id,
        target_role=role,
        repair_class=repair_class,
        expected_target_sha256=before.target_sha256(role, target_id),
        expected_result_sha256=target_sha256(target_id, role, after),
        creator_principal_id=CREATOR,
        workflow_state="CLOSED",
        final_disposition=disposition,
        dependencies=dependencies,
        witness=witness_value,
        review=review_value,
    )


_raw_apply_overlays = apply_overlays


def apply_overlays(
    initial: OverlayState, records: object
) -> ReplayResult:
    """Unit-test convenience: use the conspicuous synthetic authority factory."""

    closed = tuple(records)  # type: ignore[arg-type]
    return _raw_apply_overlays(
        initial,
        closed,
        authority=test_only_application_authority(initial, closed),
    )


class OverlaySuccessTests(unittest.TestCase):
    def assertRoundTrip(self, initial: OverlayState, record: object, expected: OverlayState) -> None:
        result = apply_overlays(initial, [record])  # type: ignore[list-item]
        self.assertEqual(result.state, expected)
        self.assertEqual(result.final_state_sha256, expected.sha256)
        self.assertEqual(inverse_replay(result), initial)

    def test_guarded_replace_and_inverse(self) -> None:
        initial = state_for((Block("RAW-000001", "hello wrld"),))
        after = (Block("RAW-000001", "hello world"),)
        record = Replace(
            meta_for(initial, after, repair_id="REPAIR-0001"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "wrld",
            "world",
            1,
        )
        result = apply_overlays(initial, [record])
        self.assertEqual(result.state.blocks(CANONICAL_AUTHOR_TEXT)[0].text(), "hello world")
        self.assertEqual(result.receipts[0].inverse_operation, "REPLACE_EXACT_POSTIMAGE")
        self.assertEqual(inverse_replay(result), initial)

    def test_guarded_delete_and_inverse(self) -> None:
        initial = state_for((Block("RAW-000001", b"alpha [noise] omega"),))
        after = (Block("RAW-000001", b"alpha  omega"),)
        record = Delete(
            meta_for(initial, after, repair_id="REPAIR-0002"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            b"[noise]",
            1,
        )
        self.assertRoundTrip(initial, record, state_for(after))

    def test_two_sided_anchored_insert_and_inverse(self) -> None:
        initial = state_for((Block("RAW-000001", "left right"),))
        after = (Block("RAW-000001", "left middle right"),)
        record = AnchoredInsert(
            meta_for(
                initial,
                after,
                repair_id="REPAIR-0003",
                high_risk_review=True,
            ),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "left ",
            "right",
            "middle ",
            1,
        )
        self.assertRoundTrip(initial, record, state_for(after))

    def test_guarded_move_and_inverse(self) -> None:
        blocks = tuple(Block(name, name.encode("ascii")) for name in ("A", "B", "C", "D"))
        initial = state_for(blocks)
        after = (blocks[0], blocks[2], blocks[1], blocks[3])
        record = Move(
            meta_for(
                initial,
                after,
                repair_id="REPAIR-0004",
                repair_class=MARKDOWN_STRUCTURE,
                high_risk_review=True,
            ),
            "B",
            blocks[1].sha256,
            "A",
            "C",
            "C",
            "D",
            1,
            1,
        )
        self.assertRoundTrip(initial, record, state_for(after))

    def test_byte_conserving_split_needs_no_witness_and_inverts(self) -> None:
        original = Block("RAW-000001", b"alphaomega")
        initial = state_for((original,))
        parts = (Block("RAW-000001-A", b"alpha"), Block("RAW-000001-B", b"omega"))
        record = Split(
            meta_for(
                initial,
                parts,
                repair_id="REPAIR-0005",
                repair_class=STRUCTURE_BOUNDARY,
                author_evidence=False,
            ),
            original.block_id,
            original.sha256,
            parts,
            1,
        )
        self.assertRoundTrip(initial, record, state_for(parts))

    def test_byte_conserving_merge_needs_no_witness_and_inverts(self) -> None:
        sources = (Block("RAW-000001-A", b"alpha"), Block("RAW-000001-B", b"omega"))
        initial = state_for(sources)
        merged = Block("RAW-000001", b"alphaomega")
        after = (merged,)
        record = Merge(
            meta_for(
                initial,
                after,
                repair_id="REPAIR-0006",
                repair_class=STRUCTURE_BOUNDARY,
                author_evidence=False,
            ),
            tuple(block.block_id for block in sources),
            tuple(block.sha256 for block in sources),
            merged,
            1,
        )
        self.assertRoundTrip(initial, record, state_for(after))

    def test_role_specific_noncanonical_overlays(self) -> None:
        cases = (
            (GENERATED_METADATA, NAVIGATION_METADATA),
            (EDITORIAL_SIDECAR, SOURCE_ERRATUM_ANNOTATION),
            (SEARCH_DERIVATIVE, SEARCH_NORMALIZATION),
        )
        for index, (role, repair_class) in enumerate(cases, 1):
            with self.subTest(role=role):
                initial = state_for((Block("SIDE-0001", "old"),), role=role)
                after = (Block("SIDE-0001", "new"),)
                meta = meta_for(
                    initial,
                    after,
                    repair_id=f"SIDE-REPAIR-{index:04d}",
                    role=role,
                    repair_class=repair_class,
                    author_evidence=False,
                )
                if role == EDITORIAL_SIDECAR:
                    meta = replace(meta, final_disposition="ANNOTATED_SOURCE_ERRATUM")
                record = Replace(
                    meta,
                    "SIDE-0001",
                    initial.blocks(role)[0].sha256,
                    "old",
                    "new",
                    1,
                )
                self.assertRoundTrip(initial, record, state_for(after, role=role))

    def test_noncanonical_overlay_must_be_closed_and_applicable(self) -> None:
        block = Block("META-0001", b"old")
        initial = state_for((block,), role=GENERATED_METADATA)
        after = (Block("META-0001", b"new"),)
        base = Replace(
            meta_for(
                initial,
                after,
                repair_id="REPAIR-0300",
                role=GENERATED_METADATA,
                repair_class=NAVIGATION_METADATA,
                author_evidence=False,
            ),
            block.block_id,
            block.sha256,
            b"old",
            b"new",
            1,
        )
        for state in (
            "CAPTURED",
            "EVIDENCE_READY",
            "PENDING_SPECIALIST_REVIEW",
            "PENDING_INDEPENDENT_REVIEW",
            "SOURCE_BLOCKED",
        ):
            record = replace(base, meta=replace(base.meta, workflow_state=state))
            with self.assertRaisesRegex(EvidenceError, "must be CLOSED"):
                apply_overlays(initial, [record])
        for disposition in (
            "REJECTED_VALID_SOURCE_TEXT",
            "DUPLICATE_CANDIDATE",
            "UNRESOLVED_SOURCE_NEEDED",
            "APPLIED_WITNESS_VERIFIED",
            "ANNOTATED_SOURCE_ERRATUM",
        ):
            record = replace(base, meta=replace(base.meta, final_disposition=disposition))
            with self.assertRaisesRegex(EvidenceError, "not applicable"):
                apply_overlays(initial, [record])

    def test_editorial_annotation_requires_annotation_disposition(self) -> None:
        block = Block("EDITORIAL-0001", b"old")
        initial = state_for((block,), role=EDITORIAL_SIDECAR)
        after = (Block("EDITORIAL-0001", b"new"),)
        meta = meta_for(
            initial,
            after,
            repair_id="REPAIR-0301",
            role=EDITORIAL_SIDECAR,
            repair_class=SOURCE_ERRATUM_ANNOTATION,
            author_evidence=False,
        )
        invalid = Replace(meta, block.block_id, block.sha256, b"old", b"new", 1)
        with self.assertRaisesRegex(EvidenceError, "not applicable"):
            apply_overlays(initial, [invalid])
        valid = replace(
            invalid,
            meta=replace(invalid.meta, final_disposition="ANNOTATED_SOURCE_ERRATUM"),
        )
        self.assertEqual(inverse_replay(apply_overlays(initial, [valid])), initial)

    def test_ordered_dependency_chain_is_deterministic_and_reversible(self) -> None:
        initial = state_for((Block("RAW-000001", "one two"),))
        middle_blocks = (Block("RAW-000001", "ONE two"),)
        middle = state_for(middle_blocks)
        final_blocks = (Block("RAW-000001", "ONE TWO"),)
        first = Replace(
            meta_for(initial, middle_blocks, repair_id="REPAIR-0100"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "one",
            "ONE",
            1,
        )
        second = Replace(
            meta_for(
                middle,
                final_blocks,
                repair_id="REPAIR-0101",
                dependencies=("REPAIR-0100",),
            ),
            "RAW-000001",
            middle.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "two",
            "TWO",
            1,
        )
        result = apply_overlays(initial, [first, second])
        self.assertEqual(result.state.blocks(CANONICAL_AUTHOR_TEXT)[0].text(), "ONE TWO")
        self.assertEqual([row.repair_id for row in result.receipts], ["REPAIR-0100", "REPAIR-0101"])
        self.assertEqual(inverse_replay(result), initial)

    def test_utf8_text_is_encoded_deterministically(self) -> None:
        block = Block("TEXT-0001", "λ → Ω")
        self.assertEqual(block.data, "λ → Ω".encode("utf-8"))
        self.assertEqual(block.text(), "λ → Ω")

    def test_state_digest_is_independent_of_mapping_insertion_order(self) -> None:
        a = (Block("A", b"a"),)
        b = (Block("B", b"b"),)
        first = OverlayState.from_mapping({SEARCH_DERIVATIVE: b, CANONICAL_AUTHOR_TEXT: a})
        second = OverlayState.from_mapping({CANONICAL_AUTHOR_TEXT: a, SEARCH_DERIVATIVE: b})
        self.assertEqual(first, second)
        self.assertEqual(first.sha256, second.sha256)


class OverlayMutationTests(unittest.TestCase):
    def replacement_fixture(
        self,
        *,
        repair_class: str = PROSE_OCR,
        role: str = CANONICAL_AUTHOR_TEXT,
        author_evidence: bool = True,
        high_risk_review: bool = False,
        witness_value: WitnessEvidence | None = None,
        review_value: IndependentReview | None = None,
    ) -> tuple[OverlayState, Replace]:
        initial = state_for((Block("RAW-000001", "bad value"),), role=role)
        after = (Block("RAW-000001", "good value"),)
        record = Replace(
            meta_for(
                initial,
                after,
                repair_id="REPAIR-0200",
                role=role,
                repair_class=repair_class,
                author_evidence=author_evidence,
                high_risk_review=high_risk_review,
                witness_value=witness_value,
                review_value=review_value,
            ),
            "RAW-000001",
            initial.blocks(role)[0].sha256,
            "bad",
            "good",
            1,
        )
        return initial, record

    def test_state_refuses_unknown_role_and_duplicate_block_ids(self) -> None:
        with self.assertRaisesRegex(SchemaError, "unknown target role"):
            state_for((Block("A", b"a"),), role="UNKNOWN_ROLE")
        with self.assertRaisesRegex(SchemaError, "duplicate block ID"):
            state_for((Block("A", b"a"), Block("A", b"b")))

    def test_complete_pre_and_post_state_hash_mutations_fail(self) -> None:
        initial, record = self.replacement_fixture()
        for field in ("expected_target_sha256", "expected_result_sha256"):
            with self.subTest(field=field):
                mutated = replace(record, meta=replace(record.meta, **{field: "0" * 64}))
                with self.assertRaisesRegex(GuardError, "target .*state hash guard failed"):
                    apply_overlays(initial, [mutated])

    def test_block_hash_mutation_fails(self) -> None:
        initial, record = self.replacement_fixture()
        mutated = replace(record, expected_block_sha256="0" * 64)
        with self.assertRaisesRegex(GuardError, "block hash guard failed"):
            apply_overlays(initial, [mutated])

    def test_replace_and_delete_exact_count_mutations_fail(self) -> None:
        initial, replacement = self.replacement_fixture()
        with self.assertRaisesRegex(GuardError, "preimage count guard failed"):
            apply_overlays(initial, [replace(replacement, expected_count=2)])

        after = (Block("RAW-000001", "bad "),)
        deletion = Delete(
            meta_for(initial, after, repair_id="REPAIR-0201"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "value",
            2,
        )
        with self.assertRaisesRegex(GuardError, "preimage count guard failed"):
            apply_overlays(initial, [deletion])

    def test_canonical_bulk_replacement_is_rejected_per_occurrence(self) -> None:
        initial = state_for((Block("RAW-000001", "bad bad"),))
        after = (Block("RAW-000001", "good good"),)
        record = Replace(
            meta_for(initial, after, repair_id="REPAIR-0202"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "bad",
            "good",
            2,
        )
        with self.assertRaisesRegex(EvidenceError, "per occurrence"):
            apply_overlays(initial, [record])

    def test_anchored_insert_refuses_missing_or_ambiguous_adjacency(self) -> None:
        for text, expected_found in (("left--right", "0"), ("leftright leftright", "2")):
            with self.subTest(text=text):
                initial = state_for((Block("RAW-000001", text),))
                after = (Block("RAW-000001", text + " changed"),)
                record = AnchoredInsert(
                    meta_for(
                        initial,
                        after,
                        repair_id="REPAIR-0203",
                        high_risk_review=True,
                    ),
                    "RAW-000001",
                    initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
                    "left",
                    "right",
                    "middle",
                    1,
                )
                with self.assertRaisesRegex(GuardError, f"found {expected_found}"):
                    apply_overlays(initial, [record])

    def test_author_text_refuses_missing_witness_or_review(self) -> None:
        initial, valid = self.replacement_fixture()
        no_witness = replace(valid, meta=replace(valid.meta, witness=None))
        with self.assertRaisesRegex(EvidenceError, "lacks witness evidence"):
            apply_overlays(initial, [no_witness])
        no_review = replace(valid, meta=replace(valid.meta, review=None))
        with self.assertRaisesRegex(EvidenceError, "lacks independent review"):
            apply_overlays(initial, [no_review])

    def test_witness_authorization_identity_and_legibility_are_required(self) -> None:
        for field, message in (
            ("authorized", "not authorized"),
            ("edition_identical", "not edition-identical"),
            ("legible_for_change", "not legible"),
        ):
            with self.subTest(field=field):
                initial, record = self.replacement_fixture(
                    witness_value=witness(**{field: False}),
                    review_value=review(),
                )
                with self.assertRaisesRegex(EvidenceError, message):
                    apply_overlays(initial, [record])

    def test_review_must_be_independent_source_approved_and_hash_bound(self) -> None:
        cases = (
            (
                review(source_reviewer_principal_id=CREATOR),
                "creator cannot independently source-review",
            ),
            (review(source_reviewer_role="SPECIALIST_REVIEWER"), "not a SOURCE_REVIEWER"),
            (review(source_decision="REJECTED"), "not approved"),
            (review(evidence_view_sha256="0" * 64), "evidence-view hash mismatch"),
            (review(creator_principal_id="some-other-creator"), "creator does not match"),
        )
        for review_value, message in cases:
            with self.subTest(message=message):
                initial, record = self.replacement_fixture(review_value=review_value)
                with self.assertRaisesRegex(EvidenceError, message):
                    apply_overlays(initial, [record])

    def test_high_risk_change_requires_blind_specialist_review(self) -> None:
        initial, record = self.replacement_fixture(
            repair_class=FORMULA_OR_SYMBOL,
            review_value=review(high_risk=False),
        )
        with self.assertRaisesRegex(EvidenceError, "lacks blind preproposal"):
            apply_overlays(initial, [record])

        initial, record = self.replacement_fixture(
            repair_class=FORMULA_OR_SYMBOL,
            review_value=review(
                high_risk=True,
                specialist_principal_id=None,
                specialist_type=None,
                specialist_session_id=None,
                specialist_decision=None,
                specialist_evidence_view_sha256=None,
            ),
        )
        with self.assertRaisesRegex(EvidenceError, "lacks specialist review"):
            apply_overlays(initial, [record])

    def test_unclosed_or_mechanically_claimed_author_text_fails(self) -> None:
        initial, record = self.replacement_fixture()
        unclosed = replace(record, meta=replace(record.meta, workflow_state="EVIDENCE_READY"))
        with self.assertRaisesRegex(EvidenceError, "not CLOSED"):
            apply_overlays(initial, [unclosed])
        mechanical = replace(
            record,
            meta=replace(record.meta, final_disposition="APPLIED_MECHANICALLY_PROVEN"),
        )
        with self.assertRaisesRegex(EvidenceError, "not APPLIED_WITNESS_VERIFIED"):
            apply_overlays(initial, [mechanical])

    def test_target_role_separation_refuses_cross_class_leaks(self) -> None:
        cases = (
            (CANONICAL_AUTHOR_TEXT, SEARCH_NORMALIZATION),
            (CANONICAL_AUTHOR_TEXT, SOURCE_ERRATUM_ANNOTATION),
            (CANONICAL_AUTHOR_TEXT, NAVIGATION_METADATA),
            (SEARCH_DERIVATIVE, PROSE_OCR),
            (EDITORIAL_SIDECAR, SEARCH_NORMALIZATION),
            (GENERATED_METADATA, SOURCE_ERRATUM_ANNOTATION),
            (DERIVED_AGGREGATE, PROSE_OCR),
        )
        for role, repair_class in cases:
            with self.subTest(role=role, repair_class=repair_class):
                initial, record = self.replacement_fixture(
                    role=role,
                    repair_class=repair_class,
                    author_evidence=False,
                )
                with self.assertRaisesRegex(RoleError, "cannot target"):
                    apply_overlays(initial, [record])

    def test_missing_later_and_duplicate_dependencies_fail(self) -> None:
        initial, first = self.replacement_fixture()
        missing = replace(first, meta=replace(first.meta, dependencies=("REPAIR-9999",)))
        with self.assertRaisesRegex(DependencyError, "unresolved dependencies"):
            apply_overlays(initial, [missing])

        dependent = replace(
            first,
            meta=replace(first.meta, repair_id="REPAIR-0201", dependencies=("REPAIR-0200",)),
        )
        with self.assertRaisesRegex(DependencyError, "not ordered before"):
            apply_overlays(initial, [dependent, first])

        with self.assertRaisesRegex(DependencyError, "duplicate repair IDs"):
            apply_overlays(initial, [first, first])

    def test_split_refuses_nonconservation_and_id_collision(self) -> None:
        original = Block("RAW-000001", b"alphabeta")
        initial = state_for((original, Block("COLLISION", b"x")))
        cases = (
            (Block("PART-A", b"alpha"), Block("PART-B", b"WRONG")),
            (Block("PART-A", b"alpha"), Block("COLLISION", b"beta")),
        )
        for parts in cases:
            with self.subTest(parts=parts):
                # The declared post-hash may be internally self-consistent; the
                # operation guard must still reject the invalid transformation.
                declared_after = (
                    Block("PART-A", b"alpha"),
                    Block("PART-B", b"beta"),
                    Block("COLLISION", b"x"),
                )
                record = Split(
                    meta_for(
                        initial,
                        declared_after,
                        repair_id="REPAIR-0300",
                        repair_class=STRUCTURE_BOUNDARY,
                        author_evidence=False,
                    ),
                    original.block_id,
                    original.sha256,
                    tuple(parts),
                    1,
                )
                with self.assertRaises(GuardError):
                    apply_overlays(initial, [record])

    def test_merge_refuses_nonadjacency_hash_and_nonconservation(self) -> None:
        a, b, c = Block("A", b"a"), Block("B", b"b"), Block("C", b"c")
        initial = state_for((a, b, c))
        mutations = (
            Merge(
                meta_for(
                    initial,
                    (Block("AB", b"ac"), b),
                    repair_id="REPAIR-0301",
                    repair_class=STRUCTURE_BOUNDARY,
                    author_evidence=False,
                ),
                ("A", "C"),
                (a.sha256, c.sha256),
                Block("AB", b"ac"),
                1,
            ),
            Merge(
                meta_for(
                    initial,
                    (Block("AB", b"ab"), c),
                    repair_id="REPAIR-0302",
                    repair_class=STRUCTURE_BOUNDARY,
                    author_evidence=False,
                ),
                ("A", "B"),
                ("0" * 64, b.sha256),
                Block("AB", b"ab"),
                1,
            ),
            Merge(
                meta_for(
                    initial,
                    (Block("AB", b"wrong"), c),
                    repair_id="REPAIR-0303",
                    repair_class=STRUCTURE_BOUNDARY,
                    author_evidence=False,
                ),
                ("A", "B"),
                (a.sha256, b.sha256),
                Block("AB", b"wrong"),
                1,
            ),
        )
        for record in mutations:
            with self.subTest(repair_id=record.meta.repair_id):
                with self.assertRaises(GuardError):
                    apply_overlays(initial, [record])

    def test_move_refuses_wrong_source_and_destination_adjacency(self) -> None:
        blocks = tuple(Block(name, name.encode("ascii")) for name in ("A", "B", "C", "D"))
        initial = state_for(blocks)
        after = (blocks[0], blocks[2], blocks[1], blocks[3])
        valid_meta = meta_for(
            initial,
            after,
            repair_id="REPAIR-0304",
            repair_class=MARKDOWN_STRUCTURE,
            high_risk_review=True,
        )
        wrong_source = Move(valid_meta, "B", blocks[1].sha256, None, "C", "C", "D", 1, 1)
        with self.assertRaisesRegex(GuardError, "source adjacency"):
            apply_overlays(initial, [wrong_source])
        wrong_destination = Move(valid_meta, "B", blocks[1].sha256, "A", "C", "A", "D", 1, 1)
        with self.assertRaisesRegex(GuardError, "destination adjacency"):
            apply_overlays(initial, [wrong_destination])

    def test_inverse_replay_refuses_any_postimage_mutation(self) -> None:
        initial, record = self.replacement_fixture()
        result = apply_overlays(initial, [record])
        tampered = result.state.with_blocks(
            CANONICAL_AUTHOR_TEXT, (Block("RAW-000001", "good value!"),)
        )
        with self.assertRaisesRegex(InverseError, "final-state hash guard"):
            inverse_replay(result, tampered)

    def test_failed_batch_is_atomic_for_the_immutable_input(self) -> None:
        initial = state_for((Block("RAW-000001", "one two"),))
        middle_blocks = (Block("RAW-000001", "ONE two"),)
        middle = state_for(middle_blocks)
        first = Replace(
            meta_for(initial, middle_blocks, repair_id="REPAIR-0400"),
            "RAW-000001",
            initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
            "one",
            "ONE",
            1,
        )
        final_blocks = (Block("RAW-000001", "ONE TWO"),)
        second = Replace(
            meta_for(
                middle,
                final_blocks,
                repair_id="REPAIR-0401",
                dependencies=("REPAIR-0400",),
            ),
            "RAW-000001",
            "0" * 64,
            "two",
            "TWO",
            1,
        )
        original_hash = initial.sha256
        with self.assertRaisesRegex(GuardError, "block hash guard failed"):
            apply_overlays(initial, [first, second])
        self.assertEqual(initial.sha256, original_hash)
        self.assertEqual(initial.blocks(CANONICAL_AUTHOR_TEXT)[0].text(), "one two")

    def test_schema_rejects_empty_insert_anchors_and_invalid_hashes(self) -> None:
        initial = state_for((Block("RAW-000001", b"leftright"),))
        after = (Block("RAW-000001", b"leftmiddleright"),)
        valid_meta = meta_for(
            initial,
            after,
            repair_id="REPAIR-0500",
            high_risk_review=True,
        )
        with self.assertRaisesRegex(SchemaError, "two nonempty anchors"):
            AnchoredInsert(
                valid_meta,
                "RAW-000001",
                initial.blocks(CANONICAL_AUTHOR_TEXT)[0].sha256,
                b"",
                b"right",
                b"middle",
                1,
            )
        with self.assertRaisesRegex(SchemaError, "lowercase SHA-256"):
            replace(valid_meta, expected_target_sha256="not-a-hash")


if __name__ == "__main__":
    unittest.main(verbosity=2)
