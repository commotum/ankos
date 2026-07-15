from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
sys.path.insert(0, str(TOOLS))

from baseline_lib import (  # noqa: E402
    BLOCK_KIND_ENUM,
    LEGACY_RELATIVE,
    RISK_PRIORITY,
    _hamilton_allocation,
    risk_stratum,
    stable_json_bytes,
)
from capture_baseline import path_is_absent  # noqa: E402
from guardrail_lib import GuardrailError, canonical_json_bytes, load_canonical_json  # noqa: E402
from validate_baseline import (  # noqa: E402
    EXPECTED_ARTIFACTS,
    _independent_defect_checks,
    _independent_git_lfs_checks,
    _independent_image_checks,
    _independent_jpeg_metadata,
    _independent_routing_checks,
    _independent_sample_ids,
    _independent_structure_checks,
    _validate_lock,
    _validate_raw_rows,
    _validate_sample_artifact,
    load_jsonl,
    validate_baseline,
)


class FrozenBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact_root = ROOT / "goal-4"
        cls.manifest = load_canonical_json(cls.artifact_root / "corpus-manifest.json")
        cls.sample = load_canonical_json(cls.artifact_root / "held-out-sample.json")
        cls.structure = load_jsonl(cls.artifact_root / "structure-ledger.jsonl")
        cls.images = load_jsonl(cls.artifact_root / "image-reference-ledger.jsonl")
        cls.defects = load_jsonl(cls.artifact_root / "known-defect-regression.jsonl")
        cls.routing = load_canonical_json(cls.artifact_root / "routing-baseline.json")
        cls.detector_hits = load_jsonl(cls.artifact_root / "baseline-detector-hits.jsonl")
        cls.detector_report = load_canonical_json(cls.artifact_root / "baseline-detector-report.json")
        cls.lock = load_canonical_json(cls.artifact_root / "baseline-lock.json")
        cls.contract = json.loads((cls.artifact_root / "guardrails.json").read_text())
        cls.quality = json.loads((cls.artifact_root / "quality-evaluation.json").read_text())
        cls.segments = [row for row in cls.structure if row["record_type"] == "SEGMENT"]
        cls.blocks = [row for row in cls.structure if row["record_type"] == "RAW_BLOCK"]
        cls.legacy = ROOT / LEGACY_RELATIVE

    def test_current_baseline_validates(self) -> None:
        self.assertEqual(
            validate_baseline(ROOT),
            {"blocks": 20430, "defects": 55, "images": 1444, "sample": 1125, "segments": 29},
        )

    def test_manifest_scope_and_counts_are_exact(self) -> None:
        self.assertEqual(self.manifest["counts"], {"all_regular_files": 1463, "jpeg": 1444, "markdown": 19})
        self.assertEqual(
            self.manifest["role_counts"],
            {
                "INTERPRETIVE_METADATA": 1,
                "LEGACY_ASSET": 1444,
                "LEGACY_ROUTING_MARKDOWN": 17,
                "RAW_AUTHOR_TEXT_MONOLITH": 1,
            },
        )
        paths = [row["relative_path"] for row in self.manifest["raw_inputs"]]
        self.assertFalse(any("Repaired" in path or path.startswith("../") for path in paths))

    def test_git_lfs_and_equal_payload_identities_remain_distinct(self) -> None:
        jpeg = [row for row in self.manifest["raw_inputs"] if row["kind"] == "JPEG"]
        self.assertTrue(all(row["git_storage"] == "LFS_POINTER_V1" for row in jpeg))
        groups = self.manifest["duplicate_jpeg_payload_groups"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]["paths"]), 3)
        self.assertEqual(len({row["file_id"] for row in jpeg}), 1444)

    def test_structure_is_exact_cover_with_closed_kinds(self) -> None:
        segments, blocks = _independent_structure_checks(ROOT, self.structure)
        self.assertEqual(len(segments), 29)
        self.assertEqual(len(blocks), 20430)
        self.assertEqual(set(row["block_kind"] for row in blocks), set(BLOCK_KIND_ENUM))
        self.assertEqual(set(row["risk_stratum"] for row in blocks), set(RISK_PRIORITY))

    def test_image_ordinals_and_three_omissions_are_exact(self) -> None:
        self.assertEqual([row["raw_reference_ordinal"] for row in self.images], list(range(1, 1445)))
        self.assertEqual(
            [(row["raw_reference_ordinal"], row["monolith_line"], row["basename"]) for row in self.images if row["split_status"] == "OMITTED"],
            [
                (24, 680, "_page_66_Picture_0.jpeg"),
                (134, 1711, "_page_154_Figure_2.jpeg"),
                (135, 1744, "_page_156_Figure_1.jpeg"),
            ],
        )

    def test_sample_is_frozen_before_outcomes(self) -> None:
        self.assertEqual(self.sample["selected_count"], 1125)
        self.assertEqual(len(self.sample["rankings"]), 20430)
        self.assertNotIn("CHANGED", json.dumps(self.sample["rankings"]))
        self.assertIn("CHANGED_OR_UNCHANGED_LABEL", self.sample["selection_prohibited_inputs"])

    def test_known_defects_never_authorize_a_repair(self) -> None:
        self.assertEqual(len(self.defects), 55)
        self.assertTrue(all(row["repair_authorized"] is False for row in self.defects))
        self.assertEqual(Counter(row["sentinel_kind"] for row in self.defects), Counter({"EXACT_RAW_SPAN": 52, "AGGREGATE_GUARDRAIL": 3}))

    def test_hamilton_allocation_uses_exact_remainders(self) -> None:
        population = {
            "INDEX_COLUMN_OR_ENTRY": 0,
            "FORMULA_CODE_RULE_OR_DATA": 2,
            "FIGURE_CAPTION_OR_VISUAL": 2,
            "HEADING_LIST_OR_LAYOUT": 3,
            "PROSE": 13,
        }
        allocation = _hamilton_allocation(population, 7)
        self.assertEqual(sum(allocation.values()), 7)
        self.assertTrue(all(allocation[key] <= population[key] for key in RISK_PRIORITY))

    def test_hamilton_equal_remainder_tie_uses_risk_priority(self) -> None:
        population = {
            "INDEX_COLUMN_OR_ENTRY": 0,
            "FORMULA_CODE_RULE_OR_DATA": 2,
            "FIGURE_CAPTION_OR_VISUAL": 2,
            "HEADING_LIST_OR_LAYOUT": 0,
            "PROSE": 2,
        }
        self.assertEqual(
            _hamilton_allocation(population, 4),
            {
                "INDEX_COLUMN_OR_ENTRY": 0,
                "FORMULA_CODE_RULE_OR_DATA": 2,
                "FIGURE_CAPTION_OR_VISUAL": 1,
                "HEADING_LIST_OR_LAYOUT": 0,
                "PROSE": 1,
            },
        )

    def test_quality_seed_and_rank_known_vector_framing(self) -> None:
        seed_spec = self.quality["seed"]
        vector = seed_spec["known_vector"]
        domain = bytes.fromhex(seed_spec["domain_separator_hex"])
        self.assertEqual(domain[-1], 0)
        seed = hashlib.sha256(domain + bytes.fromhex(vector["manifest_material_utf8_hex"])).hexdigest()
        self.assertEqual(seed, vector["seed_sha256"])
        rank_payload = (
            bytes.fromhex(seed)
            + b"\0"
            + vector["rank_canonical_document_id"].encode("utf-8")
            + b"\0"
            + vector["rank_risk_stratum"].encode("utf-8")
            + b"\0"
            + vector["rank_raw_block_id"].encode("utf-8")
        )
        self.assertEqual(hashlib.sha256(rank_payload).hexdigest(), vector["rank_sha256"])

    def test_small_document_selects_all(self) -> None:
        population = {
            "INDEX_COLUMN_OR_ENTRY": 0,
            "FORMULA_CODE_RULE_OR_DATA": 1,
            "FIGURE_CAPTION_OR_VISUAL": 1,
            "HEADING_LIST_OR_LAYOUT": 2,
            "PROSE": 3,
        }
        self.assertEqual(_hamilton_allocation(population, 7), population)

    def test_unknown_block_kind_cannot_fall_through_to_prose(self) -> None:
        with self.assertRaisesRegex(GuardrailError, "unknown block kind"):
            risk_stratum("CH01", "UNKNOWN")

    def test_raw_mutation_fails_without_touching_legacy(self) -> None:
        relative = "A-New-Kind-of-Science.md"
        source = ROOT / LEGACY_RELATIVE / relative
        with tempfile.TemporaryDirectory() as temporary:
            mutated = Path(temporary) / relative
            payload = bytearray(source.read_bytes())
            payload[0] ^= 1
            mutated.write_bytes(payload)
            with self.assertRaisesRegex(GuardrailError, "raw SHA-256 drift"):
                _validate_raw_rows(ROOT, self.manifest, {relative: mutated})

    def test_manifest_filesystem_mode_and_link_count_mutations_fail_audit(self) -> None:
        mutations = {
            "filesystem_mode": ("filesystem_mode_at_capture", "0600", "raw filesystem-mode drift"),
            "link_count": ("link_count_at_capture", 2, "raw capture link-count claim drift"),
        }
        for label, (field, value, message) in mutations.items():
            with self.subTest(label=label):
                manifest = copy.deepcopy(self.manifest)
                manifest["raw_inputs"][0][field] = value
                with self.assertRaisesRegex(GuardrailError, message):
                    _validate_raw_rows(ROOT, manifest, None, audit_capture_metadata=True)

    def test_git_and_lfs_identity_mutations_fail_independent_checks(self) -> None:
        def first_jpeg(manifest: dict) -> dict:
            return next(row for row in manifest["raw_inputs"] if row["kind"] == "JPEG")

        mutations = {
            "tree_mode": (
                lambda manifest: manifest["raw_inputs"][0].__setitem__("git_tree_mode", "100755"),
                "Git entry drift",
            ),
            "lfs_oid": (
                lambda manifest: first_jpeg(manifest).__setitem__("git_lfs_oid_sha256", "0" * 64),
                "LFS OID drift",
            ),
            "lfs_size": (
                lambda manifest: first_jpeg(manifest).__setitem__(
                    "git_lfs_size", first_jpeg(manifest)["git_lfs_size"] + 1
                ),
                "LFS size drift",
            ),
        }
        for label, (mutate, message) in mutations.items():
            with self.subTest(label=label):
                manifest = copy.deepcopy(self.manifest)
                mutate(manifest)
                with self.assertRaisesRegex(GuardrailError, message):
                    _independent_git_lfs_checks(ROOT, manifest)

    def test_malformed_jpeg_is_rejected(self) -> None:
        jpeg = next(row for row in self.manifest["raw_inputs"] if row["kind"] == "JPEG")
        payload = (self.legacy / Path(jpeg["relative_path"])).read_bytes()
        with self.assertRaisesRegex(GuardrailError, "bytes after EOI"):
            _independent_jpeg_metadata(payload + b"trailing-garbage")

    def test_dangling_repaired_sibling_alias_is_not_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            absent = root / "absent"
            dangling = root / "dangling"
            dangling.symlink_to(root / "missing-target")
            self.assertTrue(path_is_absent(absent))
            self.assertFalse(dangling.exists())
            self.assertTrue(dangling.is_symlink())
            self.assertFalse(path_is_absent(dangling))

    def test_segment_gap_mutation_fails(self) -> None:
        mutated = copy.deepcopy(self.structure)
        first_block = next(row for row in mutated if row["record_type"] == "RAW_BLOCK")
        first_block["start_byte"] += 1
        with self.assertRaisesRegex(GuardrailError, "raw block gap/overlap"):
            _independent_structure_checks(ROOT, mutated)

    def test_structure_line_byte_and_kind_risk_mutations_fail(self) -> None:
        line_byte = copy.deepcopy(self.structure)
        line_byte_blocks = [row for row in line_byte if row["record_type"] == "RAW_BLOCK"]
        line_byte_blocks[0]["end_byte_exclusive"] += 1
        line_byte_blocks[1]["start_byte"] += 1
        with self.assertRaisesRegex(GuardrailError, "line/byte mismatch"):
            _independent_structure_checks(ROOT, line_byte)

        reclassified = copy.deepcopy(self.structure)
        prose = next(
            row
            for row in reclassified
            if row["record_type"] == "RAW_BLOCK"
            and row["block_kind"] == "PROSE"
            and row["canonical_document_id"] != "INDEX"
        )
        prose["block_kind"] = "CODE_BLOCK"
        prose["risk_stratum"] = "FORMULA_CODE_RULE_OR_DATA"
        with self.assertRaisesRegex(GuardrailError, "independent lexical classification drift"):
            _independent_structure_checks(ROOT, reclassified)

    def test_detector_or_outcome_fields_cannot_change_sample(self) -> None:
        contract = json.loads((ROOT / "goal-4/guardrails.json").read_text())
        quality = json.loads((ROOT / "goal-4/quality-evaluation.json").read_text())
        blocks = [row for row in self.structure if row["record_type"] == "RAW_BLOCK"]
        seed_a, ids_a, allocations_a = _independent_sample_ids(self.manifest, blocks, contract, quality)
        polluted = copy.deepcopy(blocks)
        for row in polluted[:10]:
            row["detector_output"] = "candidate"
            row["CHANGED"] = True
        seed_b, ids_b, allocations_b = _independent_sample_ids(self.manifest, polluted, contract, quality)
        self.assertEqual((seed_a, ids_a, allocations_a), (seed_b, ids_b, allocations_b))

    def test_full_sample_ranking_swap_and_digest_mutations_fail(self) -> None:
        mutations = {
            "row_swap": lambda sample: sample["rankings"].__setitem__(
                slice(0, 2),
                [sample["rankings"][1], sample["rankings"][0]],
            ),
            "rank_digest": lambda sample: sample["rankings"][0].__setitem__("rank_sha256", "0" * 64),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                sample = copy.deepcopy(self.sample)
                mutate(sample)
                with self.assertRaisesRegex(GuardrailError, "ranking rows/order drift"):
                    _validate_sample_artifact(
                        ROOT,
                        self.manifest,
                        self.structure,
                        self.blocks,
                        self.contract,
                        self.quality,
                        sample,
                    )

    def test_lock_extra_key_and_source_scope_mutations_fail(self) -> None:
        extra_key = copy.deepcopy(self.lock)
        extra_key["unexpected"] = True
        with self.assertRaisesRegex(GuardrailError, "baseline lock field set drift"):
            _validate_lock(ROOT, self.artifact_root, extra_key)

        missing_source = copy.deepcopy(self.lock)
        missing_source["sources"].pop()
        with self.assertRaisesRegex(GuardrailError, "source scope/order drift"):
            _validate_lock(ROOT, self.artifact_root, missing_source)

    def test_routing_mutations_fail_independent_checks(self) -> None:
        mutations = {
            "route_deletion": (
                lambda routing: routing["routing_spans"].pop(0),
                "routing span identity drift",
            ),
            "wrong_target": (
                lambda routing: routing["routing_spans"][0].__setitem__("target_document_id", "CH01"),
                "routing raw owner drift",
            ),
            "wrong_disposition": (
                lambda routing: routing["routing_spans"][0].__setitem__(
                    "disposition", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"
                ),
                "routing disposition census drift",
            ),
            "split_span_hash": (
                lambda routing: routing["routing_spans"][0].__setitem__("split_span_sha256", "0" * 64),
                "routing split span drift",
            ),
            "atlas_retype": (
                lambda routing: routing["atlas"].__setitem__("role", "RAW_AUTHOR_TEXT_MONOLITH"),
                "Atlas role/identity drift",
            ),
        }
        for label, (mutate, message) in mutations.items():
            with self.subTest(label=label):
                routing = copy.deepcopy(self.routing)
                mutate(routing)
                with self.assertRaisesRegex(GuardrailError, message):
                    _independent_routing_checks(
                        self.legacy,
                        self.manifest,
                        self.segments,
                        self.images,
                        routing,
                    )

    def test_image_ledger_mutations_fail_independent_checks(self) -> None:
        omitted_index = next(index for index, row in enumerate(self.images) if row["split_status"] == "OMITTED")
        mutations = {
            "ordinal": lambda rows: rows[0].__setitem__("raw_reference_ordinal", 2),
            "asset": lambda rows: rows[0].__setitem__("asset_sha256", "0" * 64),
            "block": lambda rows: rows[0].__setitem__("raw_block_id", "RAW-999999"),
            "omission": lambda rows: rows[omitted_index].__setitem__("split_status", "PRESENT"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                rows = copy.deepcopy(self.images)
                mutate(rows)
                with self.assertRaisesRegex(GuardrailError, "independent image ledger drift"):
                    _independent_image_checks(
                        self.legacy,
                        self.manifest,
                        self.segments,
                        self.blocks,
                        rows,
                    )

    def test_known_defect_and_d13_mutations_fail_independent_checks(self) -> None:
        def delete_defect(rows: list[dict], hits: list[dict]) -> None:
            rows.pop()

        def alter_span_hash(rows: list[dict], hits: list[dict]) -> None:
            next(row for row in rows if row["sentinel_kind"] == "EXACT_RAW_SPAN")["raw_span_sha256"] = "0" * 64

        def alter_workflow(rows: list[dict], hits: list[dict]) -> None:
            rows[0]["workflow_stages"] = []

        def authorize_repair(rows: list[dict], hits: list[dict]) -> None:
            rows[0]["repair_authorized"] = True

        def delete_d13_hit(rows: list[dict], hits: list[dict]) -> None:
            index = next(index for index, row in enumerate(hits) if row["detector_id"] == "D13_EXACT_SENTINEL")
            hits.pop(index)

        mutations = {
            "defect_deletion": (delete_defect, "known-defect identity drift"),
            "span_hash": (alter_span_hash, "known defect span drift"),
            "workflow": (alter_workflow, "known defect workflow route drift"),
            "authorization": (authorize_repair, "known defect authorizes repair"),
            "D13_hit": (delete_d13_hit, "exact sentinel detector coverage drift"),
        }
        for label, (mutate, message) in mutations.items():
            with self.subTest(label=label):
                rows = copy.deepcopy(self.defects)
                hits = copy.deepcopy(self.detector_hits)
                mutate(rows, hits)
                with self.assertRaisesRegex(GuardrailError, message):
                    _independent_defect_checks(
                        self.legacy,
                        self.artifact_root,
                        self.manifest,
                        self.segments,
                        self.blocks,
                        self.images,
                        self.routing,
                        rows,
                        hits,
                        self.detector_report,
                    )

    def test_noncanonical_jsonl_row_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.jsonl"
            path.write_bytes(b'{"b": 2, "a": 1}\n')
            with self.assertRaisesRegex(GuardrailError, "not canonical"):
                load_jsonl(path)

    def test_manifest_artifact_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            for name in EXPECTED_ARTIFACTS:
                shutil.copy2(self.artifact_root / name, target / name)
            manifest = json.loads((target / "corpus-manifest.json").read_text())
            manifest["raw_inputs"][0]["role"] = "LEGACY_ASSET"
            (target / "corpus-manifest.json").write_bytes(canonical_json_bytes(manifest))
            with self.assertRaises(GuardrailError):
                validate_baseline(ROOT, artifact_root=target, check_lock=False)


if __name__ == "__main__":
    unittest.main()
