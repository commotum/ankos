#!/usr/bin/env python3
"""Crash-recoverable transactions for the six mutable Goal 4 ledgers.

This module provides atomicity only to cooperating processes:

* writers call :func:`apply_transaction` or :func:`recover_transaction`;
* a reader that needs a consistent six-ledger snapshot holds
  :func:`read_guard` for the complete read;
* every operation uses the same advisory ``flock`` file.

POSIX does not make six separate ``os.replace`` calls atomically visible.
Lock-free readers can therefore observe an intermediate mixture while a
writer is alive.  After a writer crash, ``read_guard`` refuses access while
the canonical pending directory exists, until an exclusive recovery finishes.

The on-disk protocol is deliberately small:

1. fsync staged base and proposed bytes;
2. fsync a canonical ``PREPARED`` journal and atomically publish the pending
   directory;
3. replace and fsync each target;
4. fsync the canonical ``COMMITTED`` journal;
5. atomically retire the pending directory and fsync the goal directory.

Recovery validates the journal and both complete staged byte sets.  An
all-base state is cleared, an all-proposed state is finalized, and a mixed
base/proposed state is conservatively rolled back to the staged base.  A
target matching neither recorded digest causes fail-closed retention.

A process loss before step 2 can leave only a private
``.audit-transaction-build-*`` directory: no target has changed and no
pending journal has been published.  Readers ignore that orphan, and the next
exclusive apply/recovery removes it.  A loss after the pending directory has
been atomically retired can similarly leave a private cleanup directory; the
target decision is already complete and the next exclusive operation removes
the orphan.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ARTIFACT_NAMES = (
    "candidate-ledger.jsonl",
    "cross-reference-ledger.csv",
    "reading-ledger.csv",
    "asset-ledger.csv",
    "search-rounds.json",
    "review-history.jsonl",
)

LOCK_NAME = ".audit-transaction.lock"
PENDING_NAME = ".audit-transaction"
JOURNAL_NAME = "journal.json"
BASE_DIRECTORY_NAME = "base"
PROPOSED_DIRECTORY_NAME = "proposed"
WORK_DIRECTORY_NAME = "work"
BUILD_PREFIX = ".audit-transaction-build-"
CLEANUP_PREFIX = ".audit-transaction-cleanup-"

JOURNAL_SCHEMA_VERSION = 1
JOURNAL_STATES = ("PREPARED", "COMMITTED")
JOURNAL_FIELDS = {
    "schema_version",
    "transaction_id",
    "state",
    "artifact_names",
    "base_sha256",
    "proposed_sha256",
    "artifact_modes",
}

FaultInjector = Callable[[str], None]


class TransactionError(RuntimeError):
    """Base class for a rejected, failed, or unrecoverable transaction."""


class TransactionInputError(TransactionError):
    """The proposed transaction or current source snapshot is invalid."""


class TransactionBusyError(TransactionError):
    """Another cooperating reader or writer currently holds the goal lock."""


class PendingTransactionError(TransactionError):
    """A published transaction must be recovered before new work begins."""


class TransactionApplyError(TransactionError):
    """An ordinary apply failure was handled through the recovery protocol."""


class TransactionRecoveryError(TransactionError):
    """Recovery failed closed and retained the canonical pending directory."""


@dataclass(frozen=True)
class TransactionResult:
    """Result of a fully applied and retired transaction."""

    transaction_id: str
    state: str = "COMMITTED"
    cleanup_deferred: bool = False


@dataclass(frozen=True)
class RecoveryResult:
    """Result of inspecting and, when needed, recovering pending state."""

    action: str
    transaction_id: str | None
    journal_state: str | None


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _goal_path(goal_dir: Path | str) -> Path:
    raw = Path(goal_dir)
    if raw.is_symlink():
        raise TransactionInputError(f"goal directory cannot be a symlink: {raw}")
    try:
        goal = raw.resolve(strict=True)
    except FileNotFoundError as exc:
        raise TransactionInputError(
            f"goal directory does not exist: {raw}"
        ) from exc
    try:
        mode = goal.stat(follow_symlinks=False).st_mode
    except OSError as exc:
        raise TransactionInputError(
            f"cannot inspect goal directory: {goal}: {exc}"
        ) from exc
    if not stat.S_ISDIR(mode):
        raise TransactionInputError(f"goal path is not a directory: {goal}")
    return goal


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _fsync_regular_file(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        mode = os.fstat(fd).st_mode
        if not stat.S_ISREG(mode):
            raise TransactionError(f"expected regular file: {path}")
        os.fsync(fd)
    finally:
        os.close(fd)


def _write_fsynced(path: Path, data: bytes, mode: int) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, mode)
    try:
        os.fchmod(fd, mode)
        view = memoryview(data)
        written = 0
        while written < len(view):
            count = os.write(fd, view[written:])
            if count <= 0:
                raise OSError(f"short write while staging {path}")
            written += count
        os.fsync(fd)
    finally:
        os.close(fd)


def _call_fault(fault_injector: FaultInjector | None, event: str) -> None:
    if fault_injector is not None:
        fault_injector(event)


@contextmanager
def _goal_lock(
    goal: Path,
    *,
    exclusive: bool,
    blocking: bool = False,
) -> Iterator[None]:
    lock_path = goal / LOCK_NAME
    existed = _lexists(lock_path)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise TransactionError(f"cannot open transaction lock: {exc}") from exc
    try:
        mode = os.fstat(fd).st_mode
        if not stat.S_ISREG(mode):
            raise TransactionError(
                f"transaction lock is not a regular file: {lock_path}"
            )
        if not existed:
            os.fchmod(fd, 0o600)
            os.fsync(fd)
            _fsync_directory(goal)
        operation = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
        if not blocking:
            operation |= fcntl.LOCK_NB
        try:
            fcntl.flock(fd, operation)
        except BlockingIOError as exc:
            kind = "writer" if exclusive else "reader"
            raise TransactionBusyError(
                f"Goal 4 transaction lock is busy for {kind}: {goal}"
            ) from exc
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


@contextmanager
def read_guard(
    goal_dir: Path | str,
    *,
    blocking: bool = False,
) -> Iterator[None]:
    """Hold the shared lock for one consistent multi-ledger read.

    All six files must be opened and read before leaving this context.  This is
    the race-free reader protocol.  A simple call to :func:`require_clean`
    outside the lock is diagnostic only.
    """

    goal = _goal_path(goal_dir)
    with _goal_lock(goal, exclusive=False, blocking=blocking):
        require_clean(goal)
        yield


def require_clean(goal_dir: Path | str) -> None:
    """Reject a visible pending transaction.

    This check is useful for diagnostics.  It is not by itself a consistency
    boundary because a writer can begin immediately afterward; use
    :func:`read_guard` when reading multiple ledgers.
    """

    goal = _goal_path(goal_dir)
    pending = goal / PENDING_NAME
    if _lexists(pending):
        raise PendingTransactionError(
            f"pending Goal 4 transaction requires recovery: {pending}"
        )


def _strict_bytes_map(
    values: Mapping[str, bytes],
    *,
    label: str,
) -> dict[str, bytes]:
    if set(values) != set(ARTIFACT_NAMES):
        missing = sorted(set(ARTIFACT_NAMES) - set(values))
        extra = sorted(set(values) - set(ARTIFACT_NAMES))
        raise TransactionInputError(
            f"{label} must contain exactly the six mutable ledgers; "
            f"missing={missing} extra={extra}"
        )
    result: dict[str, bytes] = {}
    for name in ARTIFACT_NAMES:
        value = values[name]
        if not isinstance(value, bytes):
            raise TransactionInputError(f"{label}[{name!r}] must be bytes")
        result[name] = value
    return result


def _strict_mode_map(
    values: Mapping[str, int],
) -> dict[str, int]:
    if set(values) != set(ARTIFACT_NAMES):
        missing = sorted(set(ARTIFACT_NAMES) - set(values))
        extra = sorted(set(values) - set(ARTIFACT_NAMES))
        raise TransactionInputError(
            "artifact_modes must contain exactly the six mutable ledgers; "
            f"missing={missing} extra={extra}"
        )
    result: dict[str, int] = {}
    for name in ARTIFACT_NAMES:
        value = values[name]
        if isinstance(value, bool) or not isinstance(value, int):
            raise TransactionInputError(
                f"artifact_modes[{name!r}] must be an integer"
            )
        if value < 0 or value > 0o777:
            raise TransactionInputError(
                f"artifact_modes[{name!r}] is outside 0000..0777"
            )
        result[name] = value
    return result


def _regular_file_bytes_and_mode(path: Path) -> tuple[bytes, int]:
    try:
        mode = path.stat(follow_symlinks=False).st_mode
    except FileNotFoundError as exc:
        raise TransactionInputError(f"required ledger is missing: {path}") from exc
    if not stat.S_ISREG(mode):
        raise TransactionInputError(
            f"required ledger is not a regular file: {path}"
        )
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise TransactionInputError(f"cannot read ledger {path}: {exc}") from exc
    return data, mode & 0o777


def _journal_identity(
    base_sha256: Mapping[str, str],
    proposed_sha256: Mapping[str, str],
    artifact_modes: Mapping[str, int],
) -> dict[str, Any]:
    return {
        "schema_version": JOURNAL_SCHEMA_VERSION,
        "artifact_names": list(ARTIFACT_NAMES),
        "base_sha256": {
            name: base_sha256[name] for name in ARTIFACT_NAMES
        },
        "proposed_sha256": {
            name: proposed_sha256[name] for name in ARTIFACT_NAMES
        },
        "artifact_modes": {
            name: artifact_modes[name] for name in ARTIFACT_NAMES
        },
    }


def _make_journal(
    base_bytes: Mapping[str, bytes],
    proposed_bytes: Mapping[str, bytes],
    artifact_modes: Mapping[str, int],
    *,
    state: str,
) -> dict[str, Any]:
    if state not in JOURNAL_STATES:
        raise TransactionInputError(f"invalid transaction state: {state}")
    base_sha256 = {
        name: _sha256(base_bytes[name]) for name in ARTIFACT_NAMES
    }
    proposed_sha256 = {
        name: _sha256(proposed_bytes[name]) for name in ARTIFACT_NAMES
    }
    identity = _journal_identity(
        base_sha256,
        proposed_sha256,
        artifact_modes,
    )
    transaction_id = _sha256(_canonical_json_bytes(identity))
    return {
        **identity,
        "transaction_id": transaction_id,
        "state": state,
    }


def _write_journal(directory: Path, journal: Mapping[str, Any]) -> None:
    temporary = directory / f".{JOURNAL_NAME}.tmp"
    _write_fsynced(temporary, _canonical_json_bytes(journal), 0o600)
    _fsync_directory(directory)
    os.replace(temporary, directory / JOURNAL_NAME)
    _fsync_regular_file(directory / JOURNAL_NAME)
    _fsync_directory(directory)


def _validate_hash_map(value: Any, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != set(ARTIFACT_NAMES):
        raise TransactionRecoveryError(
            f"pending journal {label} does not name exactly six artifacts"
        )
    result: dict[str, str] = {}
    for name in ARTIFACT_NAMES:
        digest = value[name]
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise TransactionRecoveryError(
                f"pending journal has invalid {label} digest for {name}"
            )
        result[name] = digest
    return result


def _validate_journal(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TransactionRecoveryError(
            f"pending journal is not valid UTF-8 JSON: {exc}"
        ) from exc
    if not isinstance(value, dict) or set(value) != JOURNAL_FIELDS:
        raise TransactionRecoveryError(
            "pending journal fields do not match the closed transaction schema"
        )
    if _canonical_json_bytes(value) != raw:
        raise TransactionRecoveryError("pending journal is not canonical JSON")
    if value["schema_version"] != JOURNAL_SCHEMA_VERSION:
        raise TransactionRecoveryError(
            "pending journal schema_version is unsupported"
        )
    if value["state"] not in JOURNAL_STATES:
        raise TransactionRecoveryError("pending journal state is invalid")
    if value["artifact_names"] != list(ARTIFACT_NAMES):
        raise TransactionRecoveryError(
            "pending journal artifact order is not canonical"
        )
    base_sha256 = _validate_hash_map(value["base_sha256"], "base_sha256")
    proposed_sha256 = _validate_hash_map(
        value["proposed_sha256"],
        "proposed_sha256",
    )
    try:
        artifact_modes = _strict_mode_map(value["artifact_modes"])
    except TransactionInputError as exc:
        raise TransactionRecoveryError(
            f"pending journal modes are invalid: {exc}"
        ) from exc
    if all(
        base_sha256[name] == proposed_sha256[name]
        for name in ARTIFACT_NAMES
    ):
        raise TransactionRecoveryError(
            "pending journal describes a no-op transaction"
        )
    identity = _journal_identity(
        base_sha256,
        proposed_sha256,
        artifact_modes,
    )
    expected_id = _sha256(_canonical_json_bytes(identity))
    if value["transaction_id"] != expected_id:
        raise TransactionRecoveryError(
            "pending journal transaction_id does not match its content"
        )
    return value


def _validate_stage_directory(
    directory: Path,
    expected_sha256: Mapping[str, str],
    artifact_modes: Mapping[str, int],
    *,
    label: str,
) -> None:
    try:
        mode = directory.stat(follow_symlinks=False).st_mode
    except FileNotFoundError as exc:
        raise TransactionRecoveryError(
            f"pending {label} directory is missing"
        ) from exc
    if not stat.S_ISDIR(mode):
        raise TransactionRecoveryError(
            f"pending {label} path is not a directory"
        )
    try:
        entries = {entry.name for entry in directory.iterdir()}
    except OSError as exc:
        raise TransactionRecoveryError(
            f"cannot enumerate pending {label} directory: {exc}"
        ) from exc
    if entries != set(ARTIFACT_NAMES):
        raise TransactionRecoveryError(
            f"pending {label} directory does not contain exactly six ledgers"
        )
    for name in ARTIFACT_NAMES:
        path = directory / name
        try:
            staged_mode = path.stat(follow_symlinks=False).st_mode
        except OSError as exc:
            raise TransactionRecoveryError(
                f"cannot inspect pending {label} artifact {name}: {exc}"
            ) from exc
        if not stat.S_ISREG(staged_mode):
            raise TransactionRecoveryError(
                f"pending {label} artifact is not regular: {name}"
            )
        try:
            digest = _sha256(path.read_bytes())
        except OSError as exc:
            raise TransactionRecoveryError(
                f"cannot read pending {label} artifact {name}: {exc}"
            ) from exc
        if digest != expected_sha256[name]:
            raise TransactionRecoveryError(
                f"pending {label} artifact digest mismatch: {name}"
            )
        if (staged_mode & 0o777) != artifact_modes[name]:
            raise TransactionRecoveryError(
                f"pending {label} artifact mode mismatch: {name}"
            )


def _load_pending(goal: Path) -> tuple[Path, dict[str, Any]]:
    pending = goal / PENDING_NAME
    try:
        mode = pending.stat(follow_symlinks=False).st_mode
    except FileNotFoundError as exc:
        raise TransactionRecoveryError(
            f"pending transaction disappeared during recovery: {pending}"
        ) from exc
    if not stat.S_ISDIR(mode):
        raise TransactionRecoveryError(
            f"pending transaction path is not a directory: {pending}"
        )
    journal_path = pending / JOURNAL_NAME
    try:
        journal_mode = journal_path.stat(follow_symlinks=False).st_mode
    except FileNotFoundError as exc:
        raise TransactionRecoveryError(
            "pending transaction has no journal"
        ) from exc
    if not stat.S_ISREG(journal_mode):
        raise TransactionRecoveryError(
            "pending transaction journal is not a regular file"
        )
    try:
        journal = _validate_journal(journal_path.read_bytes())
    except OSError as exc:
        raise TransactionRecoveryError(
            f"cannot read pending transaction journal: {exc}"
        ) from exc
    allowed = {
        JOURNAL_NAME,
        f".{JOURNAL_NAME}.tmp",
        BASE_DIRECTORY_NAME,
        PROPOSED_DIRECTORY_NAME,
        WORK_DIRECTORY_NAME,
    }
    entries = {entry.name for entry in pending.iterdir()}
    unexpected = entries - allowed
    required = {
        JOURNAL_NAME,
        BASE_DIRECTORY_NAME,
        PROPOSED_DIRECTORY_NAME,
        WORK_DIRECTORY_NAME,
    }
    if unexpected or not required.issubset(entries):
        raise TransactionRecoveryError(
            "pending transaction layout is invalid; "
            f"missing={sorted(required - entries)} "
            f"unexpected={sorted(unexpected)}"
        )
    work = pending / WORK_DIRECTORY_NAME
    if not stat.S_ISDIR(work.stat(follow_symlinks=False).st_mode):
        raise TransactionRecoveryError(
            "pending transaction work path is not a directory"
        )
    _validate_stage_directory(
        pending / BASE_DIRECTORY_NAME,
        journal["base_sha256"],
        journal["artifact_modes"],
        label=BASE_DIRECTORY_NAME,
    )
    _validate_stage_directory(
        pending / PROPOSED_DIRECTORY_NAME,
        journal["proposed_sha256"],
        journal["artifact_modes"],
        label=PROPOSED_DIRECTORY_NAME,
    )
    return pending, journal


def _remove_internal_directory(goal: Path, path: Path) -> None:
    if not _lexists(path):
        return
    mode = path.stat(follow_symlinks=False).st_mode
    if not stat.S_ISDIR(mode):
        raise TransactionError(
            f"internal transaction path is not a directory: {path}"
        )
    shutil.rmtree(path)
    _fsync_directory(goal)


def _cleanup_orphans(goal: Path) -> None:
    for entry in sorted(goal.iterdir(), key=lambda item: item.name):
        if entry.name.startswith(BUILD_PREFIX) or entry.name.startswith(
            CLEANUP_PREFIX
        ):
            _remove_internal_directory(goal, entry)


def _publish_prepared(
    goal: Path,
    base_bytes: Mapping[str, bytes],
    proposed_bytes: Mapping[str, bytes],
    artifact_modes: Mapping[str, int],
    journal: Mapping[str, Any],
    *,
    fault_injector: FaultInjector | None,
) -> tuple[Path, Path]:
    build = Path(tempfile.mkdtemp(prefix=BUILD_PREFIX, dir=goal))
    pending = goal / PENDING_NAME
    try:
        base = build / BASE_DIRECTORY_NAME
        proposed = build / PROPOSED_DIRECTORY_NAME
        work = build / WORK_DIRECTORY_NAME
        base.mkdir(mode=0o700)
        proposed.mkdir(mode=0o700)
        work.mkdir(mode=0o700)
        _fsync_directory(build)
        for name in ARTIFACT_NAMES:
            _write_fsynced(
                base / name,
                base_bytes[name],
                artifact_modes[name],
            )
            _write_fsynced(
                proposed / name,
                proposed_bytes[name],
                artifact_modes[name],
            )
        _fsync_directory(base)
        _fsync_directory(proposed)
        _fsync_directory(work)
        _write_journal(build, journal)
        _fsync_directory(build)
        _call_fault(fault_injector, "apply:before_publish")
        os.replace(build, pending)
        _fsync_directory(goal)
        return pending, build
    except BaseException as exc:
        if isinstance(exc, Exception) and _lexists(build):
            _remove_internal_directory(goal, build)
        raise


def _install_from_stage(
    goal: Path,
    pending: Path,
    staged: Path,
    name: str,
    mode: int,
    *,
    purpose: str,
) -> None:
    work = pending / WORK_DIRECTORY_NAME
    scratch = work / f"{purpose}-{name}.tmp"
    try:
        data = staged.read_bytes()
    except OSError as exc:
        raise TransactionError(
            f"cannot read staged {purpose} artifact {name}: {exc}"
        ) from exc
    _write_fsynced(scratch, data, mode)
    _fsync_directory(work)
    os.replace(scratch, goal / name)
    _fsync_regular_file(goal / name)
    _fsync_directory(goal)
    _fsync_directory(work)


def _target_digests_and_modes(
    goal: Path,
) -> tuple[dict[str, str], dict[str, int]]:
    digests: dict[str, str] = {}
    modes: dict[str, int] = {}
    for name in ARTIFACT_NAMES:
        path = goal / name
        try:
            mode = path.stat(follow_symlinks=False).st_mode
        except FileNotFoundError as exc:
            raise TransactionRecoveryError(
                f"transaction target is missing: {name}"
            ) from exc
        if not stat.S_ISREG(mode):
            raise TransactionRecoveryError(
                f"transaction target is not a regular file: {name}"
            )
        try:
            digests[name] = _sha256(path.read_bytes())
        except OSError as exc:
            raise TransactionRecoveryError(
                f"cannot read transaction target {name}: {exc}"
            ) from exc
        modes[name] = mode & 0o777
    return digests, modes


def _verify_target_state(
    goal: Path,
    expected_sha256: Mapping[str, str],
    expected_modes: Mapping[str, int],
    *,
    label: str,
) -> None:
    digests, modes = _target_digests_and_modes(goal)
    mismatches = [
        name
        for name in ARTIFACT_NAMES
        if (
            digests[name] != expected_sha256[name]
            or modes[name] != expected_modes[name]
        )
    ]
    if mismatches:
        raise TransactionRecoveryError(
            f"{label} target verification failed: {mismatches}"
        )


def _retire_pending(
    goal: Path,
    pending: Path,
    transaction_id: str,
    *,
    fault_injector: FaultInjector | None,
    event_prefix: str,
) -> None:
    cleanup = goal / f"{CLEANUP_PREFIX}{transaction_id}"
    if _lexists(cleanup):
        _remove_internal_directory(goal, cleanup)
    os.replace(pending, cleanup)
    _fsync_directory(goal)
    _call_fault(fault_injector, f"{event_prefix}:after_pending_retired")
    try:
        shutil.rmtree(cleanup)
    finally:
        _fsync_directory(goal)


def _restore_all(
    goal: Path,
    pending: Path,
    journal: Mapping[str, Any],
    *,
    version: str,
    fault_injector: FaultInjector | None,
) -> None:
    if version not in {"base", "proposed"}:
        raise TransactionRecoveryError(
            f"invalid recovery version requested: {version}"
        )
    staged = pending / version
    for name in ARTIFACT_NAMES:
        _call_fault(
            fault_injector,
            f"recovery:before_restore:{name}",
        )
        _install_from_stage(
            goal,
            pending,
            staged / name,
            name,
            journal["artifact_modes"][name],
            purpose=f"recover-{version}",
        )
        _call_fault(
            fault_injector,
            f"recovery:after_restore:{name}",
        )


def _recover_locked(
    goal: Path,
    *,
    fault_injector: FaultInjector | None,
) -> RecoveryResult:
    pending_path = goal / PENDING_NAME
    if not _lexists(pending_path):
        return RecoveryResult("NO_PENDING", None, None)

    pending, journal = _load_pending(goal)
    digests, modes = _target_digests_and_modes(goal)
    base = journal["base_sha256"]
    proposed = journal["proposed_sha256"]
    unknown = [
        name
        for name in ARTIFACT_NAMES
        if digests[name] not in {base[name], proposed[name]}
    ]
    if unknown:
        raise TransactionRecoveryError(
            "pending transaction targets match neither staged version; "
            f"pending state retained: {unknown}"
        )

    all_base = all(digests[name] == base[name] for name in ARTIFACT_NAMES)
    all_proposed = all(
        digests[name] == proposed[name] for name in ARTIFACT_NAMES
    )
    transaction_id = journal["transaction_id"]
    journal_state = journal["state"]

    if all_proposed and not all_base:
        if any(
            modes[name] != journal["artifact_modes"][name]
            for name in ARTIFACT_NAMES
        ):
            _restore_all(
                goal,
                pending,
                journal,
                version="proposed",
                fault_injector=fault_injector,
            )
        _verify_target_state(
            goal,
            proposed,
            journal["artifact_modes"],
            label="proposed",
        )
        if journal_state != "COMMITTED":
            committed = dict(journal)
            committed["state"] = "COMMITTED"
            _write_journal(pending, committed)
            journal_state = "COMMITTED"
        _call_fault(fault_injector, "recovery:committed")
        _call_fault(fault_injector, "recovery:before_cleanup")
        _retire_pending(
            goal,
            pending,
            transaction_id,
            fault_injector=fault_injector,
            event_prefix="recovery",
        )
        return RecoveryResult(
            "FINALIZED_PROPOSED",
            transaction_id,
            journal_state,
        )

    if all_base:
        if any(
            modes[name] != journal["artifact_modes"][name]
            for name in ARTIFACT_NAMES
        ):
            _restore_all(
                goal,
                pending,
                journal,
                version="base",
                fault_injector=fault_injector,
            )
        _verify_target_state(
            goal,
            base,
            journal["artifact_modes"],
            label="base",
        )
        _call_fault(fault_injector, "recovery:before_cleanup")
        _retire_pending(
            goal,
            pending,
            transaction_id,
            fault_injector=fault_injector,
            event_prefix="recovery",
        )
        return RecoveryResult("CLEARED_BASE", transaction_id, journal_state)

    _restore_all(
        goal,
        pending,
        journal,
        version="base",
        fault_injector=fault_injector,
    )
    _verify_target_state(
        goal,
        base,
        journal["artifact_modes"],
        label="rolled-back base",
    )
    _call_fault(fault_injector, "recovery:before_cleanup")
    _retire_pending(
        goal,
        pending,
        transaction_id,
        fault_injector=fault_injector,
        event_prefix="recovery",
    )
    return RecoveryResult("ROLLED_BACK_MIXED", transaction_id, journal_state)


def recover_transaction(
    goal_dir: Path | str,
    *,
    fault_injector: FaultInjector | None = None,
) -> RecoveryResult:
    """Recover or clear the canonical pending transaction under an exclusive lock."""

    goal = _goal_path(goal_dir)
    with _goal_lock(goal, exclusive=True):
        try:
            result = _recover_locked(
                goal,
                fault_injector=fault_injector,
            )
            if result.action == "NO_PENDING":
                _cleanup_orphans(goal)
            return result
        except TransactionRecoveryError:
            raise
        except Exception as exc:
            raise TransactionRecoveryError(
                "transaction recovery failed; canonical staged state was "
                f"retained at {goal / PENDING_NAME}: {exc}"
            ) from exc


def apply_transaction(
    goal_dir: Path | str,
    base_bytes: Mapping[str, bytes],
    proposed_bytes: Mapping[str, bytes],
    artifact_modes: Mapping[str, int],
    *,
    fault_injector: FaultInjector | None = None,
) -> TransactionResult:
    """Apply one exact six-ledger proposal through the durable journal protocol."""

    goal = _goal_path(goal_dir)
    base = _strict_bytes_map(base_bytes, label="base_bytes")
    proposed = _strict_bytes_map(proposed_bytes, label="proposed_bytes")
    modes = _strict_mode_map(artifact_modes)
    if all(base[name] == proposed[name] for name in ARTIFACT_NAMES):
        raise TransactionInputError("refusing a no-op six-ledger transaction")

    with _goal_lock(goal, exclusive=True):
        pending_path = goal / PENDING_NAME
        if _lexists(pending_path):
            raise PendingTransactionError(
                "cannot apply while a pending transaction exists; run "
                f"recover_transaction first: {pending_path}"
            )
        _cleanup_orphans(goal)

        for name in ARTIFACT_NAMES:
            current, current_mode = _regular_file_bytes_and_mode(goal / name)
            if current != base[name]:
                raise TransactionInputError(
                    f"base snapshot is stale for {name}"
                )
            if current_mode != modes[name]:
                raise TransactionInputError(
                    f"base mode is stale for {name}"
                )

        journal = _make_journal(base, proposed, modes, state="PREPARED")
        pending: Path | None = None
        build: Path | None = None
        try:
            pending, build = _publish_prepared(
                goal,
                base,
                proposed,
                modes,
                journal,
                fault_injector=fault_injector,
            )
            _call_fault(fault_injector, "apply:prepared")

            for name in ARTIFACT_NAMES:
                current, current_mode = _regular_file_bytes_and_mode(
                    goal / name
                )
                if current != base[name] or current_mode != modes[name]:
                    raise TransactionInputError(
                        f"target changed during apply: {name}"
                    )
                _call_fault(
                    fault_injector,
                    f"apply:before_replace:{name}",
                )
                _install_from_stage(
                    goal,
                    pending,
                    pending / PROPOSED_DIRECTORY_NAME / name,
                    name,
                    modes[name],
                    purpose="apply-proposed",
                )
                _call_fault(
                    fault_injector,
                    f"apply:after_replace:{name}",
                )

            _verify_target_state(
                goal,
                journal["proposed_sha256"],
                modes,
                label="applied proposed",
            )
            committed = dict(journal)
            committed["state"] = "COMMITTED"
            _write_journal(pending, committed)
            _call_fault(fault_injector, "apply:committed")
            _call_fault(fault_injector, "apply:before_cleanup")
            _retire_pending(
                goal,
                pending,
                journal["transaction_id"],
                fault_injector=fault_injector,
                event_prefix="apply",
            )
            return TransactionResult(journal["transaction_id"])
        except BaseException as exc:
            if not isinstance(exc, Exception):
                raise
            if pending is None:
                if build is not None and _lexists(build):
                    _remove_internal_directory(goal, build)
                raise
            try:
                recovery = _recover_locked(goal, fault_injector=None)
            except Exception as recovery_exc:
                raise TransactionRecoveryError(
                    f"apply failed ({exc}); recovery also failed and pending "
                    f"state remains at {goal / PENDING_NAME}: {recovery_exc}"
                ) from exc
            if recovery.action == "FINALIZED_PROPOSED":
                return TransactionResult(journal["transaction_id"])
            if recovery.action == "NO_PENDING":
                try:
                    _verify_target_state(
                        goal,
                        journal["proposed_sha256"],
                        modes,
                        label="post-retirement proposed",
                    )
                    _fsync_directory(goal)
                except Exception as verification_exc:
                    raise TransactionRecoveryError(
                        f"apply failed ({exc}); the pending directory was "
                        "retired but proposed targets could not be verified: "
                        f"{verification_exc}"
                    ) from exc
                cleanup_deferred = False
                try:
                    _cleanup_orphans(goal)
                except TransactionError:
                    cleanup_deferred = True
                return TransactionResult(
                    journal["transaction_id"],
                    cleanup_deferred=cleanup_deferred,
                )
            raise TransactionApplyError(
                f"apply failed ({exc}); recovery action={recovery.action}"
            ) from exc
