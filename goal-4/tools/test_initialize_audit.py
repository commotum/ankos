from __future__ import annotations

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import initialize_audit  # noqa: E402


def test_check_initial_holds_read_guard_for_generation_and_comparison(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    goal = tmp_path / "goal-4"
    goal.mkdir()
    artifact = goal / "reading-ledger.csv"
    artifact.write_bytes(b"expected\n")
    guard_held = False

    @contextmanager
    def guarded(_: Path) -> Iterator[None]:
        nonlocal guard_held
        guard_held = True
        try:
            yield
        finally:
            guard_held = False

    def expected_artifacts() -> dict[Path, bytes]:
        assert guard_held
        return {artifact: b"expected\n"}

    monkeypatch.setattr(initialize_audit, "GOAL_DIR", goal)
    monkeypatch.setattr(
        initialize_audit.audit_transaction,
        "read_guard",
        guarded,
    )
    monkeypatch.setattr(
        initialize_audit,
        "expected_artifacts",
        expected_artifacts,
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["initialize_audit.py", "--check-initial"],
    )

    assert initialize_audit.main() == 0
    assert not guard_held
    assert capsys.readouterr().out == (
        "initial audit artifacts reproduce exactly\n"
    )


def test_check_initial_refuses_a_pending_transaction_before_reads(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    goal = tmp_path / "goal-4"
    goal.mkdir()
    (goal / initialize_audit.audit_transaction.PENDING_NAME).mkdir()
    called = False

    def expected_artifacts() -> dict[Path, bytes]:
        nonlocal called
        called = True
        return {}

    monkeypatch.setattr(initialize_audit, "GOAL_DIR", goal)
    monkeypatch.setattr(
        initialize_audit,
        "expected_artifacts",
        expected_artifacts,
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["initialize_audit.py", "--check-initial"],
    )

    assert initialize_audit.main() == 1
    assert not called
    output = capsys.readouterr().out
    assert "refusing initial-state comparison" in output
    assert "requires recovery" in output


def test_initialization_refuses_every_existing_mutable_ledger(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    goal = tmp_path / "goal-4"
    goal.mkdir()
    ledger_paths = {
        "READING_PATH": goal / "reading-ledger.csv",
        "CANDIDATE_PATH": goal / "candidate-ledger.jsonl",
        "CROSS_REFERENCE_PATH": goal / "cross-reference-ledger.csv",
        "ASSET_PATH": goal / "asset-ledger.csv",
        "REVIEW_HISTORY_PATH": goal / "review-history.jsonl",
        "SEARCH_PATH": goal / "search-rounds.json",
    }
    original = b"authoritative existing ledger\n"
    for attribute, path in ledger_paths.items():
        monkeypatch.setattr(initialize_audit, attribute, path)
        path.write_bytes(original)

    monkeypatch.setattr(initialize_audit, "GOAL_DIR", goal)
    monkeypatch.setattr(
        initialize_audit,
        "expected_artifacts",
        lambda: {
            path: b"unsafe replacement\n" for path in ledger_paths.values()
        },
    )
    monkeypatch.setattr(sys, "argv", ["initialize_audit.py"])

    assert initialize_audit.main() == 1
    assert all(path.read_bytes() == original for path in ledger_paths.values())
    output = capsys.readouterr().out
    assert "refusing to overwrite existing audit ledgers" in output
    assert all(path.name in output for path in ledger_paths.values())


def test_force_option_is_not_available(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["initialize_audit.py", "--force"],
    )

    with pytest.raises(SystemExit) as caught:
        initialize_audit.main()
    assert caught.value.code == 2
    assert "unrecognized arguments: --force" in capsys.readouterr().err
