#!/usr/bin/env python3
"""Hostile tests for the Stage 4 outer implementation/proof lock."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
sys.path.insert(0, os.fspath(TOOLS))

import validate_stage4 as stage4  # noqa: E402


def outer_lock_digest(root: Path = ROOT) -> str:
    return hashlib.sha256(
        (root / "goal-4/stage4-implementation-lock.json").read_bytes()
    ).hexdigest()


class CanonicalJsonTests(unittest.TestCase):
    def test_canonical_round_trip_and_duplicate_key_rejection(self) -> None:
        value = {"alpha": [1, True, None], "zeta": "Ω"}
        raw = stage4.canonical_json_bytes(value)
        self.assertEqual(stage4.parse_json_bytes(raw, "fixture", canonical=True), value)
        with self.assertRaises(stage4.Stage4ValidationError):
            stage4.parse_json_bytes(b'{"a":1,"a":2}\n', "duplicate", canonical=False)

    def test_noncanonical_bom_float_and_nan_fail_closed(self) -> None:
        bad = (
            b'{"b":2, "a":1}\n',
            b'\xef\xbb\xbf{"a":1}\n',
            b'{"a":1.0}\n',
            b'{"a":NaN}\n',
            b'{"a":1}',
        )
        for raw in bad:
            with self.subTest(raw=raw), self.assertRaises(stage4.Stage4ValidationError):
                stage4.parse_json_bytes(raw, "bad fixture", canonical=True)

    def test_path_spelling_is_component_safe(self) -> None:
        self.assertEqual(
            stage4.safe_relative("goal-4/tools/a.py", "path").as_posix(),
            "goal-4/tools/a.py",
        )
        for value in (
            "",
            "/tmp/a",
            "../a",
            "goal-4/../a",
            "goal-4\\a",
            "goal-4/%2e/a",
            "goal-4/a\n",
        ):
            with self.subTest(value=value), self.assertRaises(stage4.Stage4ValidationError):
                stage4.safe_relative(value, "path")


class FilesystemTypeTests(unittest.TestCase):
    def test_plain_file_rejects_symlink_hardlink_fifo_and_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plain = root / "plain"
            plain.write_bytes(b"payload")
            os.chmod(plain, 0o600)
            self.assertEqual(stage4.read_plain_file(plain, "plain")[0], b"payload")

            symlink = root / "symlink"
            symlink.symlink_to(plain)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.read_plain_file(symlink, "symlink")

            hardlink = root / "hardlink"
            os.link(plain, hardlink)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.read_plain_file(plain, "hardlinked plain")
            hardlink.unlink()

            os.chmod(plain, 0o700)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.read_plain_file(plain, "executable")
            os.chmod(plain, 0o600)

            fifo = root / "fifo"
            os.mkfifo(fifo)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.read_plain_file(fifo, "fifo")

    def test_symlinked_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real"
            real.mkdir()
            (real / "file").write_bytes(b"x")
            alias = root / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.read_plain_file(alias / "file", "aliased file")

    def test_locked_artifact_detects_size_and_hash_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = b"accepted"
            path = root / "artifact"
            path.write_bytes(payload)
            os.chmod(path, 0o600)
            row = {
                "byte_size": len(payload),
                "category": "TEST",
                "mode": "0600",
                "path": "artifact",
                "sha256": hashlib.sha256(payload).hexdigest(),
                "type": "REGULAR_FILE",
            }
            stage4._verify_artifact(root, row)
            path.write_bytes(payload + b" drift")
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4._verify_artifact(root, row)

    def test_empty_sibling_is_exact_and_mutation_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sibling = root.joinpath(*stage4.REPAIRED_RELATIVE.parts)
            sibling.mkdir(parents=True)
            before = stage4.validate_empty_sibling(root)
            self.assertEqual(before["entries"], ())
            (sibling / "unexpected").write_bytes(b"x")
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.validate_empty_sibling(root)
            (sibling / "unexpected").unlink()
            sibling.rmdir()
            sibling.symlink_to(root, target_is_directory=True)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4.validate_empty_sibling(root)

    def test_pre_post_snapshot_comparator_rejects_any_change(self) -> None:
        stable = {"a": (1, 2)}
        stage4._assert_static_unchanged(stable, stable, stable, stable, stable, stable)
        with self.assertRaises(stage4.Stage4ValidationError):
            stage4._assert_static_unchanged(stable, {"a": (1, 3)}, stable, stable, stable, stable)


class FrozenPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        lock_path = ROOT / "goal-4/stage4-implementation-lock.json"
        if not lock_path.is_file():
            raise unittest.SkipTest("outer lock is not frozen yet")
        cls.lock_digest = outer_lock_digest()

    def test_artifact_surface_includes_validator_and_excludes_only_lock(self) -> None:
        self.assertIn("goal-4/tools/validate_stage4.py", stage4.EXPECTED_ARTIFACT_PATHS)
        self.assertIn("goal-4/tests/test_stage4.py", stage4.EXPECTED_ARTIFACT_PATHS)
        self.assertNotIn(stage4.LOCK_RELATIVE.as_posix(), stage4.EXPECTED_ARTIFACT_PATHS)
        self.assertEqual(tuple(sorted(stage4.EXPECTED_ARTIFACT_PATHS)), stage4.EXPECTED_ARTIFACT_PATHS)

    def test_outer_lock_and_every_accepted_artifact_validate(self) -> None:
        lock, artifacts, raw = stage4._load_outer_lock(ROOT, self.lock_digest)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), self.lock_digest)
        self.assertEqual(len(artifacts), len(stage4.EXPECTED_ARTIFACT_PATHS))
        self.assertEqual(len(stage4.validate_locked_artifacts(ROOT, artifacts)), len(artifacts))
        stage4._validate_direct_bindings(ROOT, lock, artifacts)
        stage4._validate_zero_contract(ROOT, lock)

    def test_wrong_external_lock_digest_fails_before_acceptance(self) -> None:
        with self.assertRaises(stage4.Stage4ValidationError):
            stage4._load_outer_lock(ROOT, "0" * 64)

    def test_duplicate_key_lock_fails_even_with_matching_external_digest(self) -> None:
        original = (ROOT / stage4.LOCK_RELATIVE).read_bytes()
        forged = b'{"lock_id":"forged",' + original[1:]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root.joinpath(*stage4.LOCK_RELATIVE.parts)
            target.parent.mkdir(parents=True)
            target.write_bytes(forged)
            with self.assertRaises(stage4.Stage4ValidationError):
                stage4._load_outer_lock(root, hashlib.sha256(forged).hexdigest())

    def test_stable_zero_proof_is_domain_separated_and_mutation_sensitive(self) -> None:
        lock, _, _ = stage4._load_outer_lock(ROOT, self.lock_digest)
        proof = dict(lock["stable_zero_repair_proof"])
        core = {key: value for key, value in proof.items() if key != "proof_sha256"}
        self.assertEqual(stage4.stable_zero_proof_digest(core), proof["proof_sha256"])
        core["source_blocks"] += 1
        self.assertNotEqual(stage4.stable_zero_proof_digest(core), proof["proof_sha256"])

    def test_actual_source_blocked_state_and_empty_sibling(self) -> None:
        lock, _, _ = stage4._load_outer_lock(ROOT, self.lock_digest)
        blocked = stage4._validate_source_blocked(ROOT, lock)
        self.assertEqual(blocked["status"], "SOURCE_BLOCKED")
        self.assertEqual(stage4.validate_empty_sibling(ROOT)["entries"], ())

    def test_actual_legacy_allowlist_is_exact(self) -> None:
        lock, _, _ = stage4._load_outer_lock(ROOT, self.lock_digest)
        result = stage4.validate_legacy_allowlist(
            ROOT, lock["bindings"]["legacy_allowlist_sha256"]
        )
        self.assertEqual(result["regular_files"], 1463)
        self.assertEqual(result["directory_count"], 36)

    def test_lock_only_validator_is_relocation_safe_and_no_git(self) -> None:
        lock, artifacts, _ = stage4._load_outer_lock(ROOT, self.lock_digest)
        self.assertEqual(len(artifacts), len(stage4.EXPECTED_ARTIFACT_PATHS))
        with tempfile.TemporaryDirectory(dir="/tmp") as directory:
            relocated = Path(directory) / "relocated"
            for relative in (*stage4.EXPECTED_ARTIFACT_PATHS, stage4.LOCK_RELATIVE.as_posix()):
                source = ROOT.joinpath(*Path(relative).parts)
                target = relocated.joinpath(*Path(relative).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                os.chmod(target, 0o644)
            command = [
                sys.executable,
                "-B",
                os.fspath(relocated / "goal-4/tools/validate_stage4.py"),
                "--repo-root",
                os.fspath(relocated),
                "--mode",
                "lock-only",
                "--expected-lock-sha256",
                self.lock_digest,
            ]
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment.pop("PYTHONPATH", None)
            result = subprocess.run(
                command,
                cwd="/tmp",
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
            self.assertTrue(result.stdout.startswith(b"STAGE4 LOCK-ONLY OK "))
            payload = json.loads(result.stdout.split(b" ", 3)[3])
            self.assertIs(payload["closure_claim"], False)
            self.assertEqual(payload["lock_sha256"], self.lock_digest)
            self.assertFalse((relocated / ".git").exists())

    def test_lock_only_api_never_claims_stage_closure(self) -> None:
        result = stage4.run_lock_only(ROOT, self.lock_digest)
        self.assertEqual(result["mode"], "LOCK_ONLY")
        self.assertIs(result["closure_claim"], False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
