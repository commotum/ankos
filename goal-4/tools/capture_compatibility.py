#!/usr/bin/env python3
"""Capture a quiescent, byte-exact Goal 1 oracle compatibility baseline."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from guardrail_lib import (
    GuardrailError,
    canonical_json_bytes,
    dependency_rows_and_fingerprint,
    derive_oracle_classifications,
    filename_set_digest,
    framed_behavior_digest,
    git_tree_identity,
    governed_dependency_paths,
    legacy_recursive_signature,
    load_json,
    oracle_classification_summary,
    require,
    row_subset_fingerprint,
    sha256_bytes,
    validate_contract,
    validate_exact_goal_output,
)


PINNED_ENV = {
    "PATH": "/usr/bin:/bin",
    "HOME": "/tmp",
    "LC_ALL": "C.utf8",
    "LANG": "C.utf8",
    "TZ": "UTC",
    "PYTHONHASHSEED": "0",
    "PYTHONOPTIMIZE": "0",
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONDONTWRITEBYTECODE": "1",
}


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        env={**PINNED_ENV, "PATH": "/usr/bin:/bin"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot read git HEAD: {result.stderr!r}")
    return result.stdout.decode("ascii").strip()


def run_oracle(root: Path, interpreter: Path, path_text: str, timeout: int) -> dict[str, Any]:
    argv = [str(interpreter), "-B", path_text]
    try:
        result = subprocess.run(
            argv,
            cwd=root,
            env=PINNED_ENV,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        exit_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        status_kind = "EXITED" if exit_code >= 0 else "SIGNALED"
    except subprocess.TimeoutExpired as error:
        exit_code = 124
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        status_kind = "TIMED_OUT"
    return {
        "path": path_text,
        "argv": argv,
        "status_kind": status_kind,
        "exit_code": exit_code,
        "stdout_bytes": stdout,
        "stderr_bytes": stderr,
        "framed_behavior_sha256": framed_behavior_digest(exit_code, stdout, stderr),
    }


def execute_round(
    root: Path,
    interpreter: Path,
    oracle_paths: list[str],
    timeout: int,
    workers: int,
) -> list[dict[str, Any]]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(run_oracle, root, interpreter, path, timeout): path for path in oracle_paths
        }
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return sorted(results, key=lambda row: row["path"])


def compare_rounds(first: list[dict[str, Any]], second: list[dict[str, Any]]) -> None:
    require(len(first) == len(second), "oracle round length drift")
    for left, right in zip(first, second, strict=True):
        require(left["path"] == right["path"], "oracle round path drift")
        for field in ("status_kind", "exit_code", "stdout_bytes", "stderr_bytes", "framed_behavior_sha256"):
            require(left[field] == right[field], f"nondeterministic oracle {left['path']}: {field}")


def probe_empty_sibling_lifecycle(
    repaired: Path,
    baseline_rows: list[dict[str, Any]],
    run_round: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Run the absent -> empty -> absent probe and clean up on failures."""

    require(not repaired.is_symlink(), "repaired root probe target is a symlink")
    require(not repaired.exists(), "repaired root must be absent before Stage 1 probe")
    created_probe = False
    try:
        repaired.mkdir(parents=False)
        created_probe = True
        require(repaired.is_dir() and not any(repaired.iterdir()), "sibling probe target is not empty")
        sibling_rows = run_round()
    finally:
        if created_probe:
            require(repaired.is_dir() and not repaired.is_symlink(), "sibling probe target changed type")
            require(not any(repaired.iterdir()), "sibling probe target became nonempty; refusing cleanup")
            repaired.rmdir()
    require(not repaired.exists() and not repaired.is_symlink(), "sibling probe did not restore absence")
    compare_rounds(baseline_rows, sibling_rows)
    post_removal_rows = run_round()
    compare_rounds(baseline_rows, post_removal_rows)
    require(not repaired.exists() and not repaired.is_symlink(), "post-removal run recreated sibling")
    return sibling_rows, post_removal_rows


def aggregate_behavior(rows: list[dict[str, Any]]) -> str:
    projection = [
        {
            "path": row["path"],
            "status_kind": row["status_kind"],
            "exit_code": row["exit_code"],
            "stdout_sha256": sha256_bytes(row["stdout_bytes"]),
            "stderr_sha256": sha256_bytes(row["stderr_bytes"]),
            "framed_behavior_sha256": row["framed_behavior_sha256"],
        }
        for row in rows
    ]
    return sha256_bytes(canonical_json_bytes(projection))


def interpreter_metadata(interpreter: Path) -> dict[str, Any]:
    program = (
        "import json,platform,sys,unicodedata;"
        "print(json.dumps({'implementation':platform.python_implementation(),"
        "'version':platform.python_version(),'unicode':unicodedata.unidata_version,"
        "'optimize':sys.flags.optimize,'executable':sys.executable,"
        "'platform':platform.platform()},sort_keys=True))"
    )
    result = subprocess.run(
        [str(interpreter), "-B", "-c", program],
        cwd="/tmp",
        env=PINNED_ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot inspect interpreter: {result.stderr!r}")
    return json.loads(result.stdout)


def make_baseline(
    root: Path,
    contract: dict[str, Any],
    quality: dict[str, Any],
    licensing: dict[str, Any],
    interpreter: Path,
    timeout: int,
    workers: int,
) -> dict[str, Any]:
    validate_contract(contract, quality, licensing, root, baseline=None, check_files=True)
    classifications = derive_oracle_classifications(root, contract)
    oracle_paths = [row["path"] for row in classifications if row["recursive_affected"]]
    require(
        oracle_paths == contract["compatibility"]["recursive_affected_paths"],
        "affected behavior order differs from frozen scope",
    )
    dependency_list = governed_dependency_paths(root, contract)
    head_before = git_head(root)
    dependency_rows_before, fingerprint_before = dependency_rows_and_fingerprint(root, dependency_list)
    legacy_content_before = row_subset_fingerprint(
        dependency_rows_before, "ref/A-New-Kind-of-Science/"
    )
    legacy_before = legacy_recursive_signature(root / contract["architecture"]["legacy_root"])
    legacy_git_tree_before = git_tree_identity(
        root, head_before, contract["architecture"]["legacy_root"]
    )

    repaired = root / contract["architecture"]["repaired_root"]
    require(not repaired.is_symlink(), "repaired root probe target is a symlink")
    require(not repaired.exists(), "repaired root must be absent before Stage 1 probe")

    baseline_first = execute_round(root, interpreter, oracle_paths, timeout, workers)
    baseline_second = execute_round(root, interpreter, oracle_paths, timeout, workers)
    compare_rounds(baseline_first, baseline_second)

    sibling_first, post_removal_first = probe_empty_sibling_lifecycle(
        repaired,
        baseline_first,
        lambda: execute_round(root, interpreter, oracle_paths, timeout, workers),
    )

    head_after = git_head(root)
    dependency_list_after = governed_dependency_paths(root, contract)
    require(
        [path.relative_to(root).as_posix() for path in dependency_list_after]
        == [path.relative_to(root).as_posix() for path in dependency_list],
        "dependency path set changed during capture",
    )
    dependency_rows_after, fingerprint_after = dependency_rows_and_fingerprint(
        root, dependency_list_after
    )
    legacy_content_after = row_subset_fingerprint(
        dependency_rows_after, "ref/A-New-Kind-of-Science/"
    )
    legacy_after = legacy_recursive_signature(root / contract["architecture"]["legacy_root"])
    legacy_git_tree_after = git_tree_identity(
        root, head_after, contract["architecture"]["legacy_root"]
    )
    require(head_before == head_after, "git HEAD moved during compatibility capture; discard and retry")
    require(fingerprint_before == fingerprint_after, "dependency bytes moved during compatibility capture; discard and retry")
    require(dependency_rows_before == dependency_rows_after, "dependency rows moved during compatibility capture; discard and retry")
    require(legacy_before == legacy_after, "legacy tree moved during compatibility capture; discard and retry")
    require(legacy_git_tree_before == legacy_git_tree_after, "legacy Git tree moved during compatibility capture")

    require(
        derive_oracle_classifications(root, contract) == classifications,
        "oracle classification or script bytes moved during capture",
    )
    baseline_aggregate = aggregate_behavior(baseline_first)
    sibling_aggregate = aggregate_behavior(sibling_first)
    post_removal_aggregate = aggregate_behavior(post_removal_first)
    oracle_rows: list[dict[str, Any]] = []
    classification_by_path = {row["path"]: row for row in classifications}
    for run in baseline_first:
        classification = classification_by_path[run["path"]]
        stdout = run["stdout_bytes"]
        stderr = run["stderr_bytes"]
        oracle_rows.append(
            {
                "path": run["path"],
                "kind": classification["kind"],
                "script_sha256": classification["script_sha256"],
                "transitive_dependency_fingerprint": fingerprint_before,
                "argv": run["argv"],
                "status_kind": run["status_kind"],
                "exit_code": run["exit_code"],
                "stdout": {
                    "byte_count": len(stdout),
                    "sha256": sha256_bytes(stdout),
                    "base64": base64.b64encode(stdout).decode("ascii"),
                },
                "stderr": {
                    "byte_count": len(stderr),
                    "sha256": sha256_bytes(stderr),
                    "base64": base64.b64encode(stderr).decode("ascii"),
                },
                "framed_behavior_sha256": run["framed_behavior_sha256"],
                "repeat_count": contract["compatibility"]["repeat_runs_required"],
                "repeat_identical": True,
                "empty_sibling_identical": True,
                "post_removal_identical": True,
            }
        )
    goal3_files = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "goal-3").rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    return {
        "schema_version": "1.1.0",
        "captured_on": contract["frozen_on"],
        "contract_id": contract["contract_id"],
        "execution": {
            "cwd": ".",
            "environment": PINNED_ENV,
            "interpreter": interpreter_metadata(interpreter),
            "timeout_seconds_per_oracle": timeout,
            "parallel_workers": workers,
            "duration_excluded_from_behavior": True,
            "book_override_used": False,
        },
        "classification_summary": oracle_classification_summary(classifications),
        "classifications": classifications,
        "closure": {
            "git_head_before": head_before,
            "git_head_after": head_after,
            "legacy_git_tree_before": legacy_git_tree_before,
            "legacy_git_tree_after": legacy_git_tree_after,
            "dependency_rows": dependency_rows_before,
            "dependency_file_count": len(dependency_rows_before),
            "dependency_fingerprint_before": fingerprint_before,
            "dependency_fingerprint_after": fingerprint_after,
            "legacy_regular_file_count": len(legacy_before["markdown_paths"]) + len(legacy_before["jpeg_paths"]),
            "legacy_tree_digest_before": legacy_before["signature_sha256"],
            "legacy_tree_digest_after": legacy_after["signature_sha256"],
            "legacy_content_fingerprint_before": legacy_content_before,
            "legacy_content_fingerprint_after": legacy_content_after,
        },
        "behavior_digest": baseline_aggregate,
        "oracles": oracle_rows,
        "empty_sibling_probe": {
            "target": contract["architecture"]["repaired_root"],
            "initial_state": "ABSENT",
            "target_state": "EMPTY",
            "final_state": "ABSENT",
            "cleanup_succeeded": True,
            "baseline_behavior_digest": baseline_aggregate,
            "empty_sibling_behavior_digest": sibling_aggregate,
            "post_removal_behavior_digest": post_removal_aggregate,
            "all_behavior_identical": (
                baseline_aggregate == sibling_aggregate == post_removal_aggregate
            ),
        },
        "health_summary": {
            "exit_zero": sum(row["exit_code"] == 0 for row in oracle_rows),
            "exit_nonzero": sum(row["exit_code"] != 0 for row in oracle_rows),
            "nonzero_paths": [row["path"] for row in oracle_rows if row["exit_code"] != 0],
            "health_is_not_behavioral_identity": True,
        },
        "goal_3": {
            "executable_validator_count": 0,
            "planning_files": goal3_files,
            "planning_filename_digest": filename_set_digest(goal3_files),
            "resync_before_release_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--interpreter", type=Path, default=Path("/usr/bin/python3"))
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve(strict=True)
    try:
        output = validate_exact_goal_output(
            root,
            args.output or Path("goal-4/compatibility-baseline.json"),
            "goal-4/compatibility-baseline.json",
        )
        require(args.interpreter.is_file(), f"interpreter missing: {args.interpreter}")
        require(not output.exists() or args.replace, f"refusing to overwrite baseline: {output}")
        contract = load_json(root / "goal-4/guardrails.json")
        quality = load_json(root / "goal-4/quality-evaluation.json")
        licensing = load_json(root / "goal-4/licensing-contract.json")
        baseline = make_baseline(
            root,
            contract,
            quality,
            licensing,
            args.interpreter,
            args.timeout,
            args.workers,
        )
        payload = canonical_json_bytes(baseline)
        candidate_sha256 = sha256_bytes(payload)
        require(
            candidate_sha256 == contract["compatibility"]["baseline_sha256"],
            "candidate baseline differs from the frozen Stage 1 hash; reopen and review the contract before replacement",
        )
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=".compatibility-baseline.",
                suffix=".tmp",
                dir=output.parent,
                delete=False,
            ) as handle:
                temporary_path = Path(handle.name)
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            temporary_path.chmod(0o644)
            os.replace(temporary_path, output)
            temporary_path = None
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
        validate_contract(
            contract,
            quality,
            licensing,
            root,
            baseline=baseline,
            check_files=True,
            check_current_scripts=True,
        )
    except (GuardrailError, OSError, subprocess.SubprocessError) as error:
        print(f"COMPATIBILITY CAPTURE FAIL: {error}", file=sys.stderr)
        return 1
    print(f"COMPATIBILITY CAPTURE OK {output.relative_to(root)} {baseline['behavior_digest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
