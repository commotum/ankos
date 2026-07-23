from __future__ import annotations

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


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
