#!/usr/bin/env python3
"""Execute one declared command and emit an exact ANKOS execution receipt."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys


RUNNER_PATH = "goal-4/tools/execution_receipt_runner.py"


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_file(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError(f"unsafe repository tool path: {relative!r}")
    path = root / relative
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"tool is absent, non-regular, or symlinked: {relative}")
    return path


def receipt_sha256(receipt: dict[str, object]) -> str:
    payload = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    return sha256_bytes(canonical_json_bytes(payload)[:-1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt-id", required=True)
    parser.add_argument("--executed-tool")
    parser.add_argument("--not-executed-reason")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    runner = repo_file(root, RUNNER_PATH)
    runner_sha = sha256_bytes(runner.read_bytes())
    started = timestamp()
    empty_sha = sha256_bytes(b"")
    if args.not_executed_reason is not None:
        if command or args.executed_tool is not None:
            parser.error("not-executed receipts cannot declare a command or executed tool")
        execution_kind = "NOT_EXECUTED_NOT_APPLICABLE"
        status_kind = "NOT_EXECUTED"
        exit_code = None
        stdout = b""
        stderr = b""
        tool_path = None
        tool_sha = None
    else:
        if not command or args.executed_tool is None or args.executed_tool not in command:
            parser.error("executed receipts require a command containing --executed-tool")
        tool = repo_file(root, args.executed_tool)
        tool_path = args.executed_tool
        tool_sha = sha256_bytes(tool.read_bytes())
        execution_kind = "EXECUTED"
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=args.timeout_seconds,
                check=False,
            )
            exit_code = completed.returncode
            status_kind = "EXITED" if completed.returncode >= 0 else "SIGNALED"
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as exc:
            exit_code = None
            status_kind = "TIMED_OUT"
            stdout = exc.stdout or b""
            stderr = exc.stderr or b""
    finished = timestamp()
    receipt: dict[str, object] = {
        "command": command,
        "command_sha256": sha256_bytes(canonical_json_bytes(command)[:-1]),
        "contract_id": "ANKOS-EXECUTION-RECEIPT-1",
        "executed_tool_path": tool_path,
        "executed_tool_sha256": tool_sha,
        "execution_kind": execution_kind,
        "exit_code": exit_code,
        "finished_at": finished,
        "not_executed_reason": args.not_executed_reason,
        "receipt_id": args.receipt_id,
        "receipt_sha256": "0" * 64,
        "runner_path": RUNNER_PATH,
        "runner_sha256": runner_sha,
        "schema_version": "1.0.0",
        "started_at": started,
        "status_kind": status_kind,
        "stderr_byte_size": len(stderr),
        "stderr_sha256": sha256_bytes(stderr) if stderr else empty_sha,
        "stdout_byte_size": len(stdout),
        "stdout_sha256": sha256_bytes(stdout) if stdout else empty_sha,
    }
    receipt["receipt_sha256"] = receipt_sha256(receipt)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json_bytes(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
