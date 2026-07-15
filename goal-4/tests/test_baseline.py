from __future__ import annotations

import copy
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
from guardrail_lib import GuardrailError, canonical_json_bytes, load_canonical_json  # noqa: E402
from validate_baseline import (  # noqa: E402
    EXPECTED_ARTIFACTS,
    _independent_sample_ids,
    _independent_structure_checks,
    _validate_raw_rows,
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

    def test_segment_gap_mutation_fails(self) -> None:
        mutated = copy.deepcopy(self.structure)
        first_block = next(row for row in mutated if row["record_type"] == "RAW_BLOCK")
        first_block["start_byte"] += 1
        with self.assertRaisesRegex(GuardrailError, "raw block gap/overlap"):
            _independent_structure_checks(ROOT, mutated)

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
