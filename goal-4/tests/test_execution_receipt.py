#!/usr/bin/env python3
"""Hostile tests for the locked Stage 4 execution-receipt runner."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "goal-4/tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import pipeline_schema_lib as lib  # noqa: E402


RUNNER = "goal-4/tools/execution_receipt_runner.py"
TOOL = "goal-4/tools/validate_guardrails.py"


class ExecutionReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _, cls.registry = lib.validate_pipeline_contract(ROOT)

    def run_receipt(self, *, optimized: bool = False, cwd: Path | None = None, extra: list[str] | None = None):
        directory = tempfile.TemporaryDirectory()
        output = Path(directory.name) / "receipt.json"
        command = [
            sys.executable,
            *( ["-O"] if optimized else [] ),
            str(ROOT / RUNNER),
            "--repo-root",
            str(ROOT),
            "--output",
            str(output),
            "--receipt-id",
            "EXECUTION-TEST-1",
            "--executed-tool",
            TOOL,
            "--",
            sys.executable,
            TOOL,
            "--repo-root",
            ".",
            *(extra or []),
        ]
        completed = subprocess.run(command, cwd=cwd or ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode())
        return directory, lib.load_json(output, require_cj1=True)

    def test_01_runner_observes_exact_output_status_time_and_tool_bytes(self) -> None:
        directory, receipt = self.run_receipt()
        self.addCleanup(directory.cleanup)
        tool_map = {RUNNER: lib.sha256_file(ROOT / RUNNER), TOOL: lib.sha256_file(ROOT / TOOL)}
        lib.validate_execution_receipt(receipt, self.registry, release_tool_hashes=tool_map)
        observed = subprocess.run(receipt["command"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(receipt["stdout_byte_size"], len(observed.stdout))
        self.assertEqual(receipt["stderr_byte_size"], len(observed.stderr))
        self.assertEqual(receipt["stdout_sha256"], hashlib.sha256(observed.stdout).hexdigest())
        self.assertEqual(receipt["stderr_sha256"], hashlib.sha256(observed.stderr).hexdigest())
        self.assertEqual(receipt["exit_code"], observed.returncode)

    def test_02_runner_and_validation_work_optimized_from_tmp(self) -> None:
        directory, receipt = self.run_receipt(optimized=True, cwd=Path("/tmp"))
        self.addCleanup(directory.cleanup)
        lib.validate_execution_receipt(receipt, self.registry)

    def test_03_nonzero_status_is_observed_not_rewritten(self) -> None:
        directory, receipt = self.run_receipt(extra=["--definitely-invalid"])
        self.addCleanup(directory.cleanup)
        lib.validate_execution_receipt(receipt, self.registry)
        self.assertEqual(receipt["status_kind"], "EXITED")
        self.assertNotEqual(receipt["exit_code"], 0)
        self.assertGreater(receipt["stderr_byte_size"], 0)

    def test_04_time_reversal_and_tool_substitution_fail(self) -> None:
        directory, receipt = self.run_receipt()
        self.addCleanup(directory.cleanup)
        receipt["started_at"], receipt["finished_at"] = "2026-07-14T12:00:02Z", "2026-07-14T12:00:01Z"
        receipt["receipt_sha256"] = lib._receipt_payload_sha256(receipt)
        with self.assertRaises(lib.PipelineSchemaError):
            lib.validate_execution_receipt(receipt, self.registry)
        second_directory, receipt = self.run_receipt()
        self.addCleanup(second_directory.cleanup)
        receipt["executed_tool_sha256"] = "0" * 64
        receipt["receipt_sha256"] = lib._receipt_payload_sha256(receipt)
        with self.assertRaises(lib.PipelineSchemaError):
            lib.validate_execution_receipt(receipt, self.registry)

    def test_05_runner_rejects_symlinked_executed_tool(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runner = root / RUNNER
            runner.parent.mkdir(parents=True)
            shutil.copy2(ROOT / RUNNER, runner)
            target = root / "real.py"
            target.write_text("print('ok')\n", encoding="utf-8")
            link = root / "tool.py"
            link.symlink_to(target)
            output = root / "receipt.json"
            completed = subprocess.run(
                [sys.executable, str(runner), "--repo-root", str(root), "--output", str(output), "--receipt-id", "EXEC-SYMLINK", "--executed-tool", "tool.py", "--", sys.executable, "tool.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    def test_06_not_published_receipt_is_honest_and_runner_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "receipt.json"
            completed = subprocess.run(
                [sys.executable, "-O", str(ROOT / RUNNER), "--repo-root", str(ROOT), "--output", str(output), "--receipt-id", "ROLLBACK-NOT-PUBLISHED", "--not-executed-reason", "NOT_PUBLISHED"],
                cwd="/tmp",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr.decode())
            receipt = lib.load_json(output, require_cj1=True)
            lib.validate_execution_receipt(
                receipt,
                self.registry,
                release_tool_hashes={RUNNER: lib.sha256_file(ROOT / RUNNER)},
                expected_command=[],
                allow_not_executed=True,
            )
            self.assertEqual(receipt["execution_kind"], "NOT_EXECUTED_NOT_APPLICABLE")


if __name__ == "__main__":
    unittest.main()
