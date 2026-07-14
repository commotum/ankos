#!/usr/bin/env python3
"""Capture a quiescent, byte-exact Goal 1 oracle compatibility baseline."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any

from guardrail_lib import (
    GuardrailError,
    canonical_json_bytes,
    filename_set_digest,
    framed_behavior_digest,
    legacy_recursive_signature,
    load_json,
    require,
    sha256_bytes,
    sha256_file,
    validate_contract,
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


def git_tree(root: Path, revision_path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", revision_path],
        cwd=root,
        env={**PINNED_ENV, "PATH": "/usr/bin:/bin"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot read git tree {revision_path}: {result.stderr!r}")
    return result.stdout.decode("ascii").strip()


def dependency_paths(root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for subtree in (
        root / "ref/A-New-Kind-of-Science",
        root / "goal-1",
        root / "goal-3",
    ):
        if subtree.exists():
            candidates.update(path for path in subtree.rglob("*") if path.is_file() and not path.is_symlink())
    for relative in (
        "ref/notes/CA-Types.csv",
        "ref/notes/CA-Types.md",
        "api.md",
        "simple_programs.md",
        "principles.md",
    ):
        path = root / relative
        if path.is_file() and not path.is_symlink():
            candidates.add(path)
    return sorted(candidates, key=lambda path: path.relative_to(root).as_posix())


def closure_fingerprint(root: Path, paths: list[Path]) -> tuple[str, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        require(path.is_file() and not path.is_symlink(), f"dependency disappeared or became symlink: {path}")
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "byte_size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return sha256_bytes(canonical_json_bytes(rows)), rows


def classify_oracles(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((root / "goal-1").glob("*-oracle.py"), key=lambda item: item.name):
        text = path.read_text(encoding="utf-8")
        recursive_affected = path.name.endswith(("-source-oracle.py", "-asset-oracle.py"))
        recursive_markdown = ".rglob(" in text and "*.md" in text
        recursive_image = path.name.endswith("-asset-oracle.py") or (
            ".rglob(basename)" in text or ".rglob(Path(match.group(1)).name)" in text
        )
        require(not recursive_affected or recursive_markdown, f"expected recursive Markdown consumer: {path.name}")
        direct_legacy = "A-New-Kind-of-Science" in text and not recursive_affected
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "kind": (
                    "RECURSIVE_SOURCE_OR_ASSET"
                    if recursive_affected
                    else "DIRECT_LEGACY_SEMANTIC"
                    if direct_legacy
                    else "NO_LEGACY_PATH"
                ),
                "recursive_affected": recursive_affected,
                "recursive_markdown": recursive_markdown,
                "recursive_image_or_basename": recursive_image,
                "direct_legacy_path": direct_legacy,
                "script_sha256": sha256_file(path),
            }
        )
    require(len(rows) == 58, f"expected 58 Goal 1 oracles, found {len(rows)}")
    require(sum(row["recursive_affected"] for row in rows) == 39, "expected 39 recursive affected oracles")
    require(sum(row["recursive_markdown"] for row in rows) == 39, "expected 39 recursive Markdown oracles")
    require(sum(row["recursive_image_or_basename"] for row in rows) == 26, "expected 26 recursive image oracles")
    require(sum(row["direct_legacy_path"] for row in rows) == 2, "expected two direct legacy semantic oracles")
    return rows


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
    classifications = classify_oracles(root)
    oracle_paths = [row["path"] for row in classifications if row["recursive_affected"]]
    dependency_list = dependency_paths(root)
    head_before = git_head(root)
    fingerprint_before, dependency_rows_before = closure_fingerprint(root, dependency_list)
    legacy_before = legacy_recursive_signature(root / contract["architecture"]["legacy_root"])
    legacy_git_tree_before = git_tree(root, f"{head_before}:ref/A-New-Kind-of-Science")

    baseline_first = execute_round(root, interpreter, oracle_paths, timeout, workers)
    baseline_second = execute_round(root, interpreter, oracle_paths, timeout, workers)
    compare_rounds(baseline_first, baseline_second)

    repaired = root / contract["architecture"]["repaired_root"]
    require(not repaired.is_symlink(), "repaired root probe target is a symlink")
    if repaired.exists():
        require(repaired.is_dir() and not any(repaired.iterdir()), "repaired root must be absent or empty for Stage 1 probe")
    else:
        repaired.mkdir(parents=False)
    sibling_first = execute_round(root, interpreter, oracle_paths, timeout, workers)
    compare_rounds(baseline_first, sibling_first)

    head_after = git_head(root)
    dependency_list_after = dependency_paths(root)
    require(
        [path.relative_to(root).as_posix() for path in dependency_list_after]
        == [path.relative_to(root).as_posix() for path in dependency_list],
        "dependency path set changed during capture",
    )
    fingerprint_after, dependency_rows_after = closure_fingerprint(root, dependency_list_after)
    legacy_after = legacy_recursive_signature(root / contract["architecture"]["legacy_root"])
    legacy_git_tree_after = git_tree(root, f"{head_after}:ref/A-New-Kind-of-Science")
    require(head_before == head_after, "git HEAD moved during compatibility capture; discard and retry")
    require(fingerprint_before == fingerprint_after, "dependency bytes moved during compatibility capture; discard and retry")
    require(dependency_rows_before == dependency_rows_after, "dependency rows moved during compatibility capture; discard and retry")
    require(legacy_before == legacy_after, "legacy tree moved during compatibility capture; discard and retry")
    require(legacy_git_tree_before == legacy_git_tree_after, "legacy Git tree moved during compatibility capture")

    classification_names = [row["path"].removeprefix("goal-1/") for row in classifications]
    affected_names = [
        row["path"].removeprefix("goal-1/") for row in classifications if row["recursive_affected"]
    ]
    baseline_aggregate = aggregate_behavior(baseline_first)
    sibling_aggregate = aggregate_behavior(sibling_first)
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
                "repeat_count": 2,
                "repeat_identical": True,
                "empty_sibling_identical": True,
            }
        )
    goal3_files = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "goal-3").rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    return {
        "schema_version": "1.0.0",
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
        "classification_summary": {
            "all_count": len(classifications),
            "all_filename_digest": filename_set_digest(classification_names),
            "recursive_affected_count": len(affected_names),
            "recursive_affected_filename_digest": filename_set_digest(affected_names),
            "recursive_markdown_count": sum(row["recursive_markdown"] for row in classifications),
            "recursive_image_or_basename_count": sum(
                row["recursive_image_or_basename"] for row in classifications
            ),
            "direct_legacy_semantic_count": sum(row["direct_legacy_path"] for row in classifications),
            "no_legacy_path_count": sum(row["kind"] == "NO_LEGACY_PATH" for row in classifications),
        },
        "classifications": classifications,
        "closure": {
            "git_head_before": head_before,
            "git_head_after": head_after,
            "legacy_git_tree_before": legacy_git_tree_before,
            "legacy_git_tree_after": legacy_git_tree_after,
            "dependency_file_count": len(dependency_rows_before),
            "dependency_fingerprint_before": fingerprint_before,
            "dependency_fingerprint_after": fingerprint_after,
            "legacy_regular_file_count": len(legacy_before["markdown_paths"]) + len(legacy_before["jpeg_paths"]),
            "legacy_tree_digest_before": legacy_before["signature_sha256"],
            "legacy_tree_digest_after": legacy_after["signature_sha256"],
        },
        "behavior_digest": baseline_aggregate,
        "oracles": oracle_rows,
        "empty_sibling_probe": {
            "target": contract["architecture"]["repaired_root"],
            "target_state": "EMPTY",
            "baseline_behavior_digest": baseline_aggregate,
            "empty_sibling_behavior_digest": sibling_aggregate,
            "all_behavior_identical": baseline_aggregate == sibling_aggregate,
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
    output = args.output or root / "goal-4/compatibility-baseline.json"
    if not output.is_absolute():
        output = root / output
    try:
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
        output.write_bytes(canonical_json_bytes(baseline))
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
