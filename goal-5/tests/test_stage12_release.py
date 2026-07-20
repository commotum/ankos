from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


GOAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOAL_DIR))

import build  # noqa: E402
import validate  # noqa: E402


EXPECTED_PAYLOAD_FILE_COUNT = 1_636
EXPECTED_PAYLOAD_TREE_SHA256 = (
    "63d702f88f644df70158c1dbf31124bd56e9e2efa04325a8fbf754daf2bb8f61"
)


def length_prefixed_payload_tree(root: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    paths = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.relative_to(root).as_posix() not in {"README.md", "Contents.md"}
    )
    for path in paths:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest(), len(paths)


class Stage12ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.range_data = json.loads(build.RANGES_PATH.read_text(encoding="utf-8"))
        cls.raw, cls.documents, cls.corrections, cls.images = build.load_inputs()
        cls.added_assets = build.load_added_assets(cls.documents, cls.images)
        cls.coverage = validate.validate_coverage(cls.documents)

    def test_readme_modes_are_distinct_and_accurate(self) -> None:
        normal = build.readme_bytes().decode("utf-8")
        zero = build.readme_bytes(zero_corrections=True).decode("utf-8")

        self.assertNotEqual(normal, zero)
        for text in (normal, zero):
            self.assertIn("GENERATED FILE — DO NOT EDIT DIRECTLY", text)

        for required in (
            "source-verified repaired Markdown",
            "29 canonical book documents",
            "Sequential source comparison",
            "technical, figure/caption, Index, Colophon, and saturation reviews",
            "All OCR, ordering, and serialization defects discovered",
            "zero known author-text transcription ambiguity",
            "agent-reviewed",
            "not been human-proofread",
            "Literal errors actually printed in the source book",
            "editorial material, not author text",
            "immutable legacy OCR monolith and assets",
            "guarded source-verified corrections",
            "repaired-only asset overrides",
            "source-added assets",
            "Neither a previous repaired tree nor the local PDF is a build input",
            "review and validation witness",
            "not redistributed",
            "python3 goal-5/build.py\n",
            "python3 goal-5/validate.py\n",
            "[Book contents](Contents.md)",
            "[Goal 5 plan](../../goal-5/0-plan.md)",
            "[Release record](../../goal-5/12-RELEASE.md)",
            "[Source ranges and witness identity](../../goal-5/source-ranges.json)",
            "[Review coverage](../../goal-5/coverage.csv)",
            "[Guarded corrections](../../goal-5/corrections.jsonl)",
            "[Image map](../../goal-5/image-map.jsonl)",
            "[Source-added assets](../../goal-5/added-assets.jsonl)",
            "[Unresolved-item register](../../goal-5/unresolved.md)",
            "[Technical review](../../goal-5/9-TECHNICAL.md)",
            "[Figures, Index, and Colophon review](../../goal-5/10-FIGURES-INDEX.md)",
            "[Saturation review](../../goal-5/11-SATURATION.md)",
        ):
            with self.subTest(normal_required=required):
                self.assertIn(required, normal)
        self.assertNotIn("raw diagnostic projection", normal)

        for required in (
            "raw diagnostic projection",
            "uncorrected diagnostic projection",
            "29 canonical documents",
            "Guarded corrections, repaired-only asset overrides, and source-added "
            "assets are deliberately excluded",
            "proves raw monolith conservation",
            "not the repaired release or an OCR-corrected edition",
            "python3 goal-5/build.py --zero-corrections --output "
            "/tmp/ankos-zero-corrections",
            "python3 goal-5/validate.py --zero-corrections --output "
            "/tmp/ankos-zero-corrections",
        ):
            with self.subTest(zero_required=required):
                self.assertIn(required, zero)
        self.assertNotIn("source-verified repaired Markdown", zero)

    def test_contents_is_generated_editorial_navigation_with_29_links(self) -> None:
        contents = build.contents_bytes(self.documents).decode("utf-8")
        self.assertIn("GENERATED FILE — DO NOT EDIT DIRECTLY", contents)
        self.assertIn("Editorial navigation", contents)
        self.assertIn("not author text", contents)
        links = re.findall(r"^- \[[^]]+\]\(([^)]+)\)$", contents, re.MULTILINE)
        self.assertEqual(len(links), 29)
        self.assertEqual(links, [row["output_path"] for row in self.documents])

    def test_published_navigation_links_resolve(self) -> None:
        for name in ("README.md", "Contents.md"):
            source = build.OUTPUT_ROOT / name
            self.assertTrue(source.is_file(), name)
            targets = re.findall(
                r"(?<!!)\[[^]]+\]\(([^)\n]+)\)",
                source.read_text(encoding="utf-8"),
            )
            self.assertTrue(targets, name)
            for target in targets:
                with self.subTest(source=name, target=target):
                    self.assertTrue((source.parent / target).resolve().is_file())

    def test_current_release_state_passes(self) -> None:
        validate.validate_release_state(
            self.coverage,
            self.corrections,
            self.images,
            self.added_assets,
        )

    def test_release_state_mutations_are_rejected(self) -> None:
        with self.assertRaisesRegex(build.BuildError, "requires 29 coverage rows"):
            validate.validate_release_state(
                self.coverage[:-1],
                self.corrections,
                self.images,
                self.added_assets,
            )

        incomplete = copy.deepcopy(self.coverage)
        incomplete[0]["second_pass"] = "NO"
        with self.assertRaisesRegex(build.BuildError, "coverage is incomplete"):
            validate.validate_release_state(
                incomplete, self.corrections, self.images, self.added_assets
            )

        mislabeled_coverage = copy.deepcopy(self.coverage)
        mislabeled_coverage[0]["reviewer_type"] = "human"
        with self.assertRaisesRegex(build.BuildError, "coverage reviewer"):
            validate.validate_release_state(
                mislabeled_coverage,
                self.corrections,
                self.images,
                self.added_assets,
            )

        mislabeled_corrections = list(self.corrections)
        mislabeled_corrections[0] = {
            **mislabeled_corrections[0],
            "reviewer_type": "human",
        }
        with self.assertRaisesRegex(build.BuildError, "correction reviewer"):
            validate.validate_release_state(
                self.coverage,
                mislabeled_corrections,
                self.images,
                self.added_assets,
            )

        mislabeled_added = list(self.added_assets)
        mislabeled_added[0] = {**mislabeled_added[0], "reviewer_type": "human"}
        with self.assertRaisesRegex(build.BuildError, "added asset reviewer"):
            validate.validate_release_state(
                self.coverage,
                self.corrections,
                self.images,
                mislabeled_added,
            )

        disposition_index = next(
            index
            for index, row in enumerate(self.images)
            if "reference_disposition" in row
        )
        mislabeled_images = list(self.images)
        mislabeled_images[disposition_index] = {
            **mislabeled_images[disposition_index],
            "reference_reviewer_type": "human",
        }
        with self.assertRaisesRegex(
            build.BuildError, "image-reference disposition reviewer"
        ):
            validate.validate_release_state(
                self.coverage,
                self.corrections,
                mislabeled_images,
                self.added_assets,
            )

        with tempfile.TemporaryDirectory(prefix="g5-release-unresolved-") as directory:
            unresolved = Path(directory) / "unresolved.md"
            for status in ("OPEN", "BLOCKED", "UNRESOLVED"):
                with self.subTest(unresolved_status=status):
                    unresolved.write_text(
                        f"# Unresolved items\n\nStatus: {status}\n",
                        encoding="utf-8",
                    )
                    with self.assertRaisesRegex(
                        build.BuildError, "release-blocking Status"
                    ):
                        validate.validate_release_state(
                            self.coverage,
                            self.corrections,
                            self.images,
                            self.added_assets,
                            unresolved_path=unresolved,
                        )

    def test_builder_does_not_open_authoritative_pdf(self) -> None:
        missing_source = copy.deepcopy(self.range_data)
        missing_source["authoritative_source"]["path"] = (
            "missing-authoritative-source/A-New-Kind-of-Science.pdf"
        )
        self.assertEqual(
            len(build.validate_ranges(self.raw, missing_source)),
            29,
        )
        with self.assertRaisesRegex(build.BuildError, "source is missing"):
            validate.validate_authoritative_source(missing_source)

        with tempfile.TemporaryDirectory(prefix="g5-release-no-pdf-build-") as directory:
            root = Path(directory)
            ranges = root / "source-ranges.json"
            ranges.write_text(
                json.dumps(missing_source, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            output = root / "output"
            with patch.object(build, "RANGES_PATH", ranges):
                self.assertEqual(build.build(output), (29, 1_607, 4_834))
            self.assertEqual(
                (output / "README.md").read_bytes(),
                build.readme_bytes(),
            )

    def test_generated_corrected_payload_is_frozen_excluding_navigation(self) -> None:
        self.assertTrue(build.OUTPUT_ROOT.is_dir())
        digest, count = length_prefixed_payload_tree(build.OUTPUT_ROOT)
        self.assertEqual(count, EXPECTED_PAYLOAD_FILE_COUNT)
        self.assertEqual(digest, EXPECTED_PAYLOAD_TREE_SHA256)


if __name__ == "__main__":
    unittest.main()
