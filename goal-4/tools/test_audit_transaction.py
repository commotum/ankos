from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

import pytest


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import audit_transaction as transaction  # noqa: E402


class SimulatedCrash(BaseException):
    """A fault that behaves like process loss instead of a handled error."""


def _state_bytes(goal: Path) -> dict[str, bytes]:
    return {
        name: (goal / name).read_bytes()
        for name in transaction.ARTIFACT_NAMES
    }


def _state_modes(goal: Path) -> dict[str, int]:
    return {
        name: (goal / name).stat().st_mode & 0o777
        for name in transaction.ARTIFACT_NAMES
    }


def _make_goal(
    tmp_path: Path,
) -> tuple[Path, dict[str, bytes], dict[str, bytes], dict[str, int]]:
    goal = tmp_path / "goal-4"
    goal.mkdir()
    base: dict[str, bytes] = {}
    proposed: dict[str, bytes] = {}
    modes: dict[str, int] = {}
    for ordinal, name in enumerate(transaction.ARTIFACT_NAMES, start=1):
        base[name] = f"base-{ordinal}\n".encode()
        proposed[name] = f"proposed-{ordinal}\n".encode()
        modes[name] = 0o640 if ordinal % 2 else 0o600
        path = goal / name
        path.write_bytes(base[name])
        path.chmod(modes[name])
    return goal, base, proposed, modes


def _crash_on(expected_event: str) -> Any:
    def inject(event: str) -> None:
        if event == expected_event:
            raise SimulatedCrash(expected_event)

    return inject


def _error_on(expected_event: str) -> Any:
    def inject(event: str) -> None:
        if event == expected_event:
            raise OSError(expected_event)

    return inject


def _pending_journal(goal: Path) -> tuple[bytes, dict[str, Any]]:
    raw = (
        goal
        / transaction.PENDING_NAME
        / transaction.JOURNAL_NAME
    ).read_bytes()
    return raw, json.loads(raw)


def test_apply_commits_exact_six_files_and_retires_pending(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    result = transaction.apply_transaction(goal, base, proposed, modes)

    assert result.state == "COMMITTED"
    assert len(result.transaction_id) == 64
    assert _state_bytes(goal) == proposed
    assert _state_modes(goal) == modes
    assert not os.path.lexists(goal / transaction.PENDING_NAME)
    with transaction.read_guard(goal):
        assert _state_bytes(goal) == proposed


def test_shared_reader_lock_excludes_writer(tmp_path: Path) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    with transaction.read_guard(goal):
        with pytest.raises(transaction.TransactionBusyError):
            transaction.apply_transaction(goal, base, proposed, modes)

    transaction.apply_transaction(goal, base, proposed, modes)


def test_prepared_journal_is_canonical_and_binds_staged_bytes(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on("apply:prepared"),
        )

    raw, journal = _pending_journal(goal)
    assert raw == transaction._canonical_json_bytes(journal)
    assert journal["state"] == "PREPARED"
    assert journal["artifact_names"] == list(transaction.ARTIFACT_NAMES)
    assert journal["base_sha256"] == {
        name: hashlib.sha256(base[name]).hexdigest()
        for name in transaction.ARTIFACT_NAMES
    }
    assert journal["proposed_sha256"] == {
        name: hashlib.sha256(proposed[name]).hexdigest()
        for name in transaction.ARTIFACT_NAMES
    }
    for name in transaction.ARTIFACT_NAMES:
        pending = goal / transaction.PENDING_NAME
        assert (pending / "base" / name).read_bytes() == base[name]
        assert (pending / "proposed" / name).read_bytes() == proposed[name]


def test_pending_refuses_new_apply_and_cooperating_reader(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    first = transaction.ARTIFACT_NAMES[0]

    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on(f"apply:after_replace:{first}"),
        )

    with pytest.raises(transaction.PendingTransactionError):
        transaction.apply_transaction(goal, base, proposed, modes)
    with pytest.raises(transaction.PendingTransactionError):
        with transaction.read_guard(goal):
            pass
    with pytest.raises(transaction.PendingTransactionError):
        transaction.require_clean(goal)


def test_recovery_clears_all_base_prepared_state(tmp_path: Path) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on("apply:prepared"),
        )

    recovered = transaction.recover_transaction(goal)

    assert recovered.action == "CLEARED_BASE"
    assert recovered.journal_state == "PREPARED"
    assert _state_bytes(goal) == base
    assert _state_modes(goal) == modes
    assert not os.path.lexists(goal / transaction.PENDING_NAME)


def test_recovery_finalizes_all_proposed_with_prepared_journal(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    last = transaction.ARTIFACT_NAMES[-1]
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on(f"apply:after_replace:{last}"),
        )
    assert _pending_journal(goal)[1]["state"] == "PREPARED"

    recovered = transaction.recover_transaction(goal)

    assert recovered.action == "FINALIZED_PROPOSED"
    assert recovered.journal_state == "COMMITTED"
    assert _state_bytes(goal) == proposed
    assert _state_modes(goal) == modes
    assert not os.path.lexists(goal / transaction.PENDING_NAME)


def test_recovery_keeps_all_proposed_after_committed_journal(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on("apply:committed"),
        )
    assert _pending_journal(goal)[1]["state"] == "COMMITTED"

    recovered = transaction.recover_transaction(goal)

    assert recovered.action == "FINALIZED_PROPOSED"
    assert recovered.journal_state == "COMMITTED"
    assert _state_bytes(goal) == proposed


@pytest.mark.parametrize(
    "event",
    [
        f"apply:after_replace:{transaction.ARTIFACT_NAMES[-1]}",
        "apply:committed",
        "apply:after_pending_retired",
    ],
)
def test_handled_error_after_physical_commit_returns_committed_success(
    tmp_path: Path,
    event: str,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    result = transaction.apply_transaction(
        goal,
        base,
        proposed,
        modes,
        fault_injector=_error_on(event),
    )

    assert result.state == "COMMITTED"
    assert _state_bytes(goal) == proposed
    assert _state_modes(goal) == modes
    assert not os.path.lexists(goal / transaction.PENDING_NAME)


def test_crash_before_pending_publication_leaves_safe_removable_orphan(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on("apply:before_publish"),
        )

    assert _state_bytes(goal) == base
    assert not os.path.lexists(goal / transaction.PENDING_NAME)
    orphans = sorted(goal.glob(f"{transaction.BUILD_PREFIX}*"))
    assert len(orphans) == 1
    with transaction.read_guard(goal):
        assert _state_bytes(goal) == base

    assert transaction.recover_transaction(goal).action == "NO_PENDING"
    assert sorted(goal.glob(f"{transaction.BUILD_PREFIX}*")) == []


def test_mixed_prepared_state_rolls_back_to_staged_base(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    second = transaction.ARTIFACT_NAMES[1]
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on(f"apply:after_replace:{second}"),
        )
    assert _state_bytes(goal) != base
    assert _state_bytes(goal) != proposed

    recovered = transaction.recover_transaction(goal)

    assert recovered.action == "ROLLED_BACK_MIXED"
    assert recovered.journal_state == "PREPARED"
    assert _state_bytes(goal) == base
    assert _state_modes(goal) == modes
    assert not os.path.lexists(goal / transaction.PENDING_NAME)


def test_rollback_failure_retains_complete_staging_and_is_retryable(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    second = transaction.ARTIFACT_NAMES[1]
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on(f"apply:after_replace:{second}"),
        )

    def fail_second_restore(event: str) -> None:
        if event == f"recovery:before_restore:{second}":
            raise OSError("injected rollback failure")

    with pytest.raises(
        transaction.TransactionRecoveryError,
        match="canonical staged state was retained",
    ):
        transaction.recover_transaction(
            goal,
            fault_injector=fail_second_restore,
        )

    pending = goal / transaction.PENDING_NAME
    assert pending.is_dir()
    for name in transaction.ARTIFACT_NAMES:
        assert (pending / "base" / name).read_bytes() == base[name]
        assert (pending / "proposed" / name).read_bytes() == proposed[name]

    recovered = transaction.recover_transaction(goal)
    assert recovered.action in {"ROLLED_BACK_MIXED", "CLEARED_BASE"}
    assert _state_bytes(goal) == base
    assert not os.path.lexists(pending)


def test_unknown_target_bytes_fail_closed_and_retain_pending(
    tmp_path: Path,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    first = transaction.ARTIFACT_NAMES[0]
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on(f"apply:after_replace:{first}"),
        )
    (goal / first).write_bytes(b"neither staged version\n")

    with pytest.raises(
        transaction.TransactionRecoveryError,
        match="match neither staged version",
    ):
        transaction.recover_transaction(goal)

    assert (goal / transaction.PENDING_NAME).is_dir()


def test_corrupt_staged_original_fails_closed(tmp_path: Path) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    with pytest.raises(SimulatedCrash):
        transaction.apply_transaction(
            goal,
            base,
            proposed,
            modes,
            fault_injector=_crash_on("apply:prepared"),
        )
    first = transaction.ARTIFACT_NAMES[0]
    (
        goal
        / transaction.PENDING_NAME
        / transaction.BASE_DIRECTORY_NAME
        / first
    ).write_bytes(b"corrupt\n")

    with pytest.raises(
        transaction.TransactionRecoveryError,
        match="artifact digest mismatch",
    ):
        transaction.recover_transaction(goal)

    assert (goal / transaction.PENDING_NAME).is_dir()


def test_apply_and_recovery_fsync_regular_files_and_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)
    real_fsync = transaction.os.fsync
    observed: set[str] = set()

    def recording_fsync(fd: int) -> None:
        mode = os.fstat(fd).st_mode
        if stat.S_ISDIR(mode):
            observed.add("directory")
        if stat.S_ISREG(mode):
            observed.add("regular")
        real_fsync(fd)

    monkeypatch.setattr(transaction.os, "fsync", recording_fsync)
    transaction.apply_transaction(goal, base, proposed, modes)

    assert observed == {"directory", "regular"}


def test_no_op_and_incomplete_maps_are_rejected(tmp_path: Path) -> None:
    goal, base, proposed, modes = _make_goal(tmp_path)

    with pytest.raises(transaction.TransactionInputError, match="no-op"):
        transaction.apply_transaction(goal, base, dict(base), modes)

    incomplete = dict(proposed)
    incomplete.pop(transaction.ARTIFACT_NAMES[-1])
    with pytest.raises(
        transaction.TransactionInputError,
        match="exactly the six mutable ledgers",
    ):
        transaction.apply_transaction(goal, base, incomplete, modes)


def test_recovery_without_pending_is_idempotent(tmp_path: Path) -> None:
    goal, _, _, _ = _make_goal(tmp_path)

    result = transaction.recover_transaction(goal)

    assert result == transaction.RecoveryResult("NO_PENDING", None, None)
