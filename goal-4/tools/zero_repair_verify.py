"""Independent verifier for an ANKOS-ZERO-REPAIR-1 staging tree.

This module deliberately imports nothing from ``zero_repair_lib``.  It owns a
second parser, inventory walker, projection derivation, inverse replay, and
manifest derivation.  The small frozen contract is hashed here rather than
being produced by the compiler, so compiler and verifier cannot silently
agree on a changed conservation claim.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any


class IndependentVerificationError(RuntimeError):
    """A standalone zero-repair proof failed closed."""


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise IndependentVerificationError(message)


CONTRACT_SHA256 = "3fd15222dfac4735640056e2ae786e36d5e96638454a4741ac1662ebfba3b964"
CONTRACT_FILE = "zero-repair-contract.json"
IMPLEMENTATION_LOCK_FILE = "zero-repair-implementation-lock.json"
IMPLEMENTATION_LOCK_SHA256 = "041503bc521ac760f1499ddf520c105ac2b1608ee452f13ef4937c72e8986360"
SCHEMA_VERSION = "1.0.0"
CONTRACT_ID = "ANKOS-ZERO-REPAIR-1"
LEGACY_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science")
REPAIRED_RELATIVE = PurePosixPath("ref/A-New-Kind-of-Science-Repaired")
MONOLITH_RELATIVE = PurePosixPath("A-New-Kind-of-Science.md")
TAPE_RELATIVE = PurePosixPath("BUILD-METADATA/projection-tape.jsonl")
MANIFEST_RELATIVE = PurePosixPath("BUILD-METADATA/zero-repair-manifest.json")
TOOL_RELATIVES = (
    PurePosixPath("tools/zero_repair_lib.py"),
    PurePosixPath("tools/build_zero_repair.py"),
    PurePosixPath("tools/validate_zero_repair.py"),
    PurePosixPath("tools/zero_repair_verify.py"),
)
LOCKED_RELATIVES = (
    "zero-repair-contract.json",
    "tools/build_zero_repair.py",
    "tools/validate_zero_repair.py",
    "tools/zero_repair_lib.py",
    "tests/test_zero_repair.py",
)
FILE_MODE = 0o644
DIRECTORY_MODE = 0o755
VERIFICATION_BOUNDARY = "SAME_UID_NON_ADVERSARIAL_BETWEEN_FINAL_RECHECK_AND_RENAME"


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def _no_float(value: Any) -> None:
    if isinstance(value, float):
        raise IndependentVerificationError("canonical JSON contains a float")
    if isinstance(value, dict):
        for key, child in value.items():
            _check(isinstance(key, str), "canonical JSON has a non-string key")
            _no_float(child)
    elif isinstance(value, list):
        for child in value:
            _no_float(child)


def _canonical(value: Any, *, lf: bool = True) -> bytes:
    _no_float(value)
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return raw + (b"\n" if lf else b"")


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise IndependentVerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _float(_: str) -> Any:
    raise IndependentVerificationError("JSON contains a floating-point value")


def _json(raw: bytes, label: str, *, canonical: bool) -> Any:
    _check(not raw.startswith(b"\xef\xbb\xbf"), f"{label} has a BOM")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(text, object_pairs_hook=_unique, parse_float=_float)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as error:
        raise IndependentVerificationError(f"{label} is not strict JSON") from error
    _no_float(value)
    if canonical:
        _check(_canonical(value) == raw, f"{label} is not canonical ANKOS-CJ-1")
    return value


def _jsonl(raw: bytes, label: str) -> list[dict[str, Any]]:
    _check(raw.endswith(b"\n"), f"{label} has no terminal LF")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(raw.splitlines(keepends=True), 1):
        _check(line != b"\n" and line.endswith(b"\n"), f"{label} has a malformed row {index}")
        row = _json(line, f"{label} row {index}", canonical=True)
        _check(isinstance(row, dict), f"{label} row {index} is not an object")
        rows.append(row)
    return rows


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _exists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def _within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _no_symlink_chain(path: Path, label: str) -> None:
    absolute = _absolute(path)
    for component in [*reversed(absolute.parents), absolute]:
        if _exists(component):
            _check(not stat.S_ISLNK(os.lstat(component).st_mode), f"{label} has a symlink component")


def _plain_directory(path: Path, label: str, *, exact_mode: int | None = None) -> os.stat_result:
    _no_symlink_chain(path, label)
    _check(_exists(path), f"{label} does not exist")
    status = os.lstat(path)
    _check(stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"{label} is not a real directory")
    if exact_mode is not None:
        _check(stat.S_IMODE(status.st_mode) == exact_mode, f"{label} mode drift")
    return status


def _plain_file(path: Path, label: str) -> bytes:
    _no_symlink_chain(path, label)
    _check(_exists(path), f"{label} is missing")
    status = os.lstat(path)
    _check(stat.S_ISREG(status.st_mode) and not stat.S_ISLNK(status.st_mode), f"{label} is not a regular file")
    _check(stat.S_IMODE(status.st_mode) & 0o7111 == 0, f"{label} has executable or special mode bits")
    return path.read_bytes()


def _validate_runtime_and_implementation_lock(
    goal: Path,
    *,
    expected_runtime_sha256: str | None,
) -> tuple[str, dict[str, Any]]:
    """Bind this running oracle to its declared path and one-way tool lock.

    The implementation lock intentionally excludes this verifier.  The
    verifier pins that lock; the enclosing Stage 4 proof pins the verifier.
    This one-way chain avoids an impossible content-hash cycle.
    """

    declared = _join(goal, PurePosixPath("tools/zero_repair_verify.py"))
    actual = _absolute(Path(__file__))
    _check(actual == declared, "executed verifier path differs from declared Goal 4 verifier")
    verifier_raw = _plain_file(declared, "declared independent verifier")
    verifier_sha256 = _sha(verifier_raw)
    if expected_runtime_sha256 is not None:
        _check(
            verifier_sha256 == expected_runtime_sha256,
            "executed verifier hash differs from loader-declared verifier hash",
        )

    lock_path = goal / IMPLEMENTATION_LOCK_FILE
    lock_raw = _plain_file(lock_path, "zero-repair implementation lock")
    _check(_sha(lock_raw) == IMPLEMENTATION_LOCK_SHA256, "zero-repair implementation lock hash drift")
    lock = _json(lock_raw, "zero-repair implementation lock", canonical=True)
    _check(
        isinstance(lock, dict)
        and lock.get("lock_id") == "ANKOS-ZERO-REPAIR-IMPLEMENTATION-LOCK-1"
        and lock.get("schema_version") == SCHEMA_VERSION,
        "zero-repair implementation lock identity drift",
    )
    artifacts = lock.get("artifacts")
    _check(isinstance(artifacts, list), "zero-repair implementation lock artifacts missing")
    _check(
        [row.get("path") for row in artifacts if isinstance(row, dict)] == list(LOCKED_RELATIVES),
        "zero-repair implementation lock path set/order drift",
    )
    for row in artifacts:
        _check(isinstance(row, dict), "zero-repair implementation lock artifact type drift")
        relative = _relative(row.get("path"), "implementation-lock artifact path")
        payload = _plain_file(_join(goal, relative), f"locked artifact {relative.as_posix()}")
        _check(row.get("type") == "REGULAR_FILE", f"locked artifact type drift: {relative.as_posix()}")
        _check(row.get("byte_size") == len(payload), f"locked artifact size drift: {relative.as_posix()}")
        _check(row.get("sha256") == _sha(payload), f"locked artifact hash drift: {relative.as_posix()}")
    return verifier_sha256, lock


def _relative(value: Any, label: str) -> PurePosixPath:
    _check(isinstance(value, str) and bool(value), f"{label} is not a nonempty string")
    _check("\\" not in value and "\x00" not in value and "%" not in value, f"{label} spelling is unsafe")
    path = PurePosixPath(value)
    _check(not path.is_absolute(), f"{label} is absolute")
    _check(path.as_posix() == value and all(part not in {"", ".", ".."} for part in path.parts), f"{label} traverses")
    return path


def _join(root: Path, relative: PurePosixPath) -> Path:
    return root.joinpath(*relative.parts)


def _override(repo: Path, value: Path | None, default: PurePosixPath) -> Path:
    if value is None:
        return _join(repo, default)
    return _absolute(value if value.is_absolute() else repo / value)


def _exact_int(value: Any) -> bool:
    return type(value) is int


def _source_sequence(blocks: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(b"ANKOS-SOURCE-BLOCK-SEQUENCE-1\0")
    for block in blocks:
        for key in ("raw_block_id", "raw_sha256"):
            encoded = block[key].encode("ascii")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
    return digest.hexdigest()


def _tree_digest(records: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(b"ANKOS-ZERO-REPAIR-PAYLOAD-TREE-1\0")
    for record in sorted(records, key=lambda item: item["path"]):
        encoded = _canonical(record, lf=False)
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


def _file_record(path: str, role: str, raw: bytes) -> dict[str, Any]:
    return {
        "byte_size": len(raw),
        "mode": "0644",
        "path": path,
        "role": role,
        "sha256": _sha(raw),
        "type": "REGULAR_FILE",
    }


def _load_source(
    repo: Path,
    goal: Path,
    legacy: Path,
    *,
    expected_runtime_sha256: str | None,
) -> dict[str, Any]:
    verifier_sha256, implementation_lock = _validate_runtime_and_implementation_lock(
        goal,
        expected_runtime_sha256=expected_runtime_sha256,
    )
    contract_raw = _plain_file(goal / CONTRACT_FILE, "zero-repair contract")
    _check(_sha(contract_raw) == CONTRACT_SHA256, "zero-repair contract hash drift")
    contract = _json(contract_raw, "zero-repair contract", canonical=True)
    _check(isinstance(contract, dict) and contract.get("contract_id") == CONTRACT_ID, "zero-repair contract identity drift")
    _check(contract.get("schema_version") == SCHEMA_VERSION, "zero-repair contract schema drift")
    frozen = contract.get("frozen_inputs")
    counts = contract.get("counts")
    proof = contract.get("proof")
    _check(isinstance(frozen, dict) and isinstance(counts, dict) and isinstance(proof, dict), "zero-repair contract sections missing")

    sources = {
        "guardrails": goal / "guardrails.json",
        "baseline": goal / "baseline-lock.json",
        "corpus": goal / "corpus-manifest.json",
        "ledger": goal / "structure-ledger.jsonl",
        "monolith": _join(legacy, MONOLITH_RELATIVE),
    }
    expected_hashes = {
        "guardrails": frozen.get("guardrails_sha256"),
        "baseline": frozen.get("baseline_lock_sha256"),
        "corpus": frozen.get("corpus_manifest_sha256"),
        "ledger": frozen.get("structure_ledger_sha256"),
        "monolith": frozen.get("monolith_sha256"),
    }
    raw: dict[str, bytes] = {}
    for name, path in sources.items():
        payload = _plain_file(path, name)
        _check(_sha(payload) == expected_hashes[name], f"{name} frozen hash drift")
        raw[name] = payload

    guardrails = _json(raw["guardrails"], "guardrails", canonical=False)
    baseline = _json(raw["baseline"], "baseline lock", canonical=True)
    corpus = _json(raw["corpus"], "corpus manifest", canonical=True)
    ledger = _jsonl(raw["ledger"], "structure ledger")
    _check(all(isinstance(value, dict) for value in (guardrails, baseline, corpus)), "frozen source root type drift")

    artifacts = {
        row.get("path"): row
        for row in baseline.get("artifacts", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    _check(artifacts.get("goal-4/corpus-manifest.json", {}).get("sha256") == expected_hashes["corpus"], "baseline/corpus binding drift")
    _check(artifacts.get("goal-4/structure-ledger.jsonl", {}).get("sha256") == expected_hashes["ledger"], "baseline/ledger binding drift")
    architecture = guardrails.get("architecture")
    _check(isinstance(architecture, dict), "guardrails architecture missing")
    _check(architecture.get("legacy_root") == LEGACY_RELATIVE.as_posix(), "legacy architecture drift")
    _check(architecture.get("repaired_root") == REPAIRED_RELATIVE.as_posix(), "repaired architecture drift")
    _check(contract.get("architecture") == {"legacy_root": LEGACY_RELATIVE.as_posix(), "repaired_root": REPAIRED_RELATIVE.as_posix()}, "contract architecture drift")

    declared_documents = guardrails.get("canonical_documents")
    expected_document_count = counts.get("canonical_documents")
    _check(_exact_int(expected_document_count) and expected_document_count == 29, "contract document count drift")
    _check(isinstance(declared_documents, list) and len(declared_documents) == expected_document_count, "canonical document count drift")
    documents: list[dict[str, Any]] = []
    ids: set[str] = set()
    paths: set[str] = set()
    for order, item in enumerate(declared_documents):
        _check(isinstance(item, dict), f"canonical document {order} type drift")
        path = _relative(item.get("path"), f"canonical document {order} path")
        identifier = item.get("id")
        _check(path.parts[0] == "CANONICAL" and path.suffix == ".md", f"canonical document {order} path drift")
        _check(item.get("order") == order and item.get("role") == "CANONICAL_AUTHOR_TEXT", f"canonical document {order} metadata drift")
        _check(isinstance(identifier, str) and identifier and identifier not in ids and path.as_posix() not in paths, "canonical document collision")
        ids.add(identifier)
        paths.add(path.as_posix())
        documents.append({"id": identifier, "order": order, "path": path.as_posix(), "role": "CANONICAL_AUTHOR_TEXT"})

    monolith = raw["monolith"]
    _check(len(monolith) == frozen.get("monolith_byte_size") == counts.get("source_projection_bytes"), "monolith byte count drift")
    _check(monolith.count(b"\n") + 1 == frozen.get("monolith_logical_lines"), "monolith logical-line count drift")
    _check(not monolith.endswith(b"\n"), "monolith terminal LF drift")
    monolith.decode("utf-8", errors="strict")
    raw_inputs = corpus.get("raw_inputs")
    _check(isinstance(raw_inputs, list), "corpus raw inputs missing")
    mono_rows = [row for row in raw_inputs if isinstance(row, dict) and row.get("role") == "RAW_AUTHOR_TEXT_MONOLITH"]
    _check(len(mono_rows) == 1, "corpus monolith role drift")
    _check(mono_rows[0].get("relative_path") == MONOLITH_RELATIVE.as_posix() and mono_rows[0].get("sha256") == expected_hashes["monolith"], "corpus monolith binding drift")

    segments = [row for row in ledger if row.get("record_type") == "SEGMENT"]
    blocks = [row for row in ledger if row.get("record_type") == "RAW_BLOCK"]
    _check(len(segments) == 29 and len(blocks) == counts.get("source_blocks") == 20430, "ledger count drift")
    _check(ledger == [*segments, *blocks], "ledger record ordering drift")
    segment_by_id: dict[str, dict[str, Any]] = {}
    cursor = 0
    for order, (segment, document) in enumerate(zip(segments, documents)):
        start = segment.get("raw_start_byte")
        end = segment.get("raw_end_byte_exclusive")
        _check(segment.get("schema_version") == SCHEMA_VERSION and segment.get("order") == order, f"segment {order} metadata drift")
        _check(segment.get("segment_id") == document["id"] and segment.get("canonical_path") == document["path"], f"segment {order} document drift")
        _check(segment.get("role") == "CANONICAL_AUTHOR_TEXT" and segment.get("raw_source_path") == MONOLITH_RELATIVE.as_posix(), f"segment {order} role drift")
        _check(segment.get("raw_source_sha256") == expected_hashes["monolith"], f"segment {order} source hash drift")
        _check(_exact_int(start) and _exact_int(end) and start == cursor and start < end <= len(monolith), f"segment {order} range drift")
        fragment = monolith[start:end]
        _check(segment.get("raw_byte_count") == len(fragment) and segment.get("raw_segment_sha256") == _sha(fragment), f"segment {order} payload drift")
        cursor = end
        segment_by_id[document["id"]] = segment
    _check(cursor == len(monolith), "segments do not conserve monolith bytes")

    block_counts = {document["id"]: 0 for document in documents}
    cursor = 0
    line_cursor = 0
    for order, block in enumerate(blocks, 1):
        start = block.get("start_byte")
        end = block.get("end_byte_exclusive")
        start_line = block.get("start_line")
        end_line = block.get("end_line")
        segment_id = block.get("segment_id")
        _check(block.get("schema_version") == SCHEMA_VERSION and block.get("order") == order, f"raw block {order} metadata drift")
        _check(block.get("raw_block_id") == f"RAW-{order:06d}", f"raw block {order} identity drift")
        _check(_exact_int(start) and _exact_int(end) and start == cursor and start < end <= len(monolith), f"raw block {order} range drift")
        fragment = monolith[start:end]
        _check(block.get("byte_size") == len(fragment) and block.get("raw_sha256") == _sha(fragment), f"raw block {order} payload drift")
        _check(_exact_int(start_line) and _exact_int(end_line) and start_line == line_cursor + 1 and start_line <= end_line, f"raw block {order} line drift")
        _check(segment_id in segment_by_id and block.get("canonical_document_id") == segment_id, f"raw block {order} segment drift")
        segment = segment_by_id[segment_id]
        _check(block.get("canonical_path") == segment.get("canonical_path"), f"raw block {order} path drift")
        _check(segment["raw_start_byte"] <= start < end <= segment["raw_end_byte_exclusive"], f"raw block {order} crosses segment")
        block_counts[segment_id] += 1
        cursor = end
        line_cursor = end_line
    _check(cursor == len(monolith) and line_cursor == frozen.get("monolith_logical_lines"), "raw blocks do not conserve source extent")
    _check(all(value > 0 for value in block_counts.values()), "document has no source block")

    tool_sources: list[dict[str, Any]] = []
    tool_paths: list[Path] = []
    for relative in TOOL_RELATIVES:
        path = _join(goal, relative)
        _plain_file(path, f"tool {relative.as_posix()}")
        tool_paths.append(path)
        tool_sources.append({"path": f"goal-4/{relative.as_posix()}", "sha256": _sha_file(path)})
    return {
        "contract": contract,
        "contract_sha256": CONTRACT_SHA256,
        "implementation_lock": implementation_lock,
        "implementation_lock_sha256": IMPLEMENTATION_LOCK_SHA256,
        "documents": documents,
        "segments": segments,
        "blocks": blocks,
        "monolith": monolith,
        "source_sequence": _source_sequence(blocks),
        "tool_sources": tool_sources,
        "verifier_sha256": verifier_sha256,
        "inputs": [goal / CONTRACT_FILE, goal / IMPLEMENTATION_LOCK_FILE, *sources.values(), *tool_paths],
    }


def _receipt_record(path: str, kind: str, status: os.stat_result, sha256: str | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {
        "ctime_ns": status.st_ctime_ns,
        "device": status.st_dev,
        "inode": status.st_ino,
        "mode": f"{stat.S_IMODE(status.st_mode):04o}",
        "mtime_ns": status.st_mtime_ns,
        "nlink": status.st_nlink,
        "path": path,
        "size": status.st_size,
        "type": kind,
    }
    if sha256 is not None:
        record["sha256"] = sha256
    return record


def _stable_file_receipt(path: Path, relative: str) -> dict[str, Any]:
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        _check(
            (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            f"output file changed while opening: {relative}",
        )
        digest = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    stable_fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns")
    _check(
        all(getattr(opened, field) == getattr(after, field) for field in stable_fields),
        f"output file mutated while hashing: {relative}",
    )
    return _receipt_record(relative, "REGULAR_FILE", after, digest.hexdigest())


def _inventory(output: Path, documents: list[dict[str, Any]]) -> dict[str, Any]:
    expected_files = {document["path"] for document in documents} | {TAPE_RELATIVE.as_posix(), MANIFEST_RELATIVE.as_posix()}
    expected_directories: set[str] = set()
    for name in expected_files:
        current = PurePosixPath(name).parent
        while current != PurePosixPath("."):
            expected_directories.add(current.as_posix())
            current = current.parent
    files: set[str] = set()
    directories: set[str] = set()
    inodes: set[tuple[int, int]] = set()
    records: list[dict[str, Any]] = []
    root_before = os.lstat(output)
    records.append(_receipt_record(".", "DIRECTORY", root_before))

    def walk(directory: Path) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as error:
            raise IndependentVerificationError(f"cannot inventory output directory: {directory}") from error
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(output).as_posix()
            status = os.lstat(path)
            _check(not stat.S_ISLNK(status.st_mode), f"output contains a symlink: {relative}")
            if stat.S_ISDIR(status.st_mode):
                _check(stat.S_IMODE(status.st_mode) == DIRECTORY_MODE, f"output directory mode drift: {relative}")
                directories.add(relative)
                walk(path)
                after = os.lstat(path)
                _check(
                    (after.st_dev, after.st_ino, after.st_mode, after.st_mtime_ns, after.st_ctime_ns)
                    == (status.st_dev, status.st_ino, status.st_mode, status.st_mtime_ns, status.st_ctime_ns),
                    f"output directory mutated during inventory: {relative}",
                )
                records.append(_receipt_record(relative, "DIRECTORY", after))
            elif stat.S_ISREG(status.st_mode):
                _check(stat.S_IMODE(status.st_mode) == FILE_MODE, f"output file mode drift: {relative}")
                _check(status.st_nlink == 1, f"output file has a hardlink: {relative}")
                inode = (status.st_dev, status.st_ino)
                _check(inode not in inodes, f"output files share an inode: {relative}")
                inodes.add(inode)
                files.add(relative)
                record = _stable_file_receipt(path, relative)
                _check(
                    (record["device"], record["inode"], record["mode"], record["size"], record["mtime_ns"], record["ctime_ns"])
                    == (status.st_dev, status.st_ino, f"{stat.S_IMODE(status.st_mode):04o}", status.st_size, status.st_mtime_ns, status.st_ctime_ns),
                    f"output file changed during inventory: {relative}",
                )
                records.append(record)
            else:
                raise IndependentVerificationError(f"output contains an unexpected filesystem type: {relative}")

    walk(output)
    _check(files == expected_files, "output file ownership drift")
    _check(directories == expected_directories, "output directory ownership drift")
    root_after = os.lstat(output)
    _check(
        (root_after.st_dev, root_after.st_ino, root_after.st_mode, root_after.st_mtime_ns, root_after.st_ctime_ns)
        == (root_before.st_dev, root_before.st_ino, root_before.st_mode, root_before.st_mtime_ns, root_before.st_ctime_ns),
        "output root mutated during inventory",
    )
    records[0] = _receipt_record(".", "DIRECTORY", root_after)
    records.sort(key=lambda row: (row["path"], row["type"]))
    return {
        "boundary": VERIFICATION_BOUNDARY,
        "records": records,
    }


def _expected_projection(snapshot: dict[str, Any], output: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    monolith = snapshot["monolith"]
    documents = snapshot["documents"]
    segments = snapshot["segments"]
    blocks = snapshot["blocks"]
    grouped = {document["id"]: [] for document in documents}
    for block in blocks:
        grouped[block["segment_id"]].append(block)
    tape: list[dict[str, Any]] = []
    document_records: list[dict[str, Any]] = []
    file_records: list[dict[str, Any]] = []
    tape_order = 0
    lf_hash = _sha(b"\n")
    for document, segment in zip(documents, segments):
        source = monolith[segment["raw_start_byte"]:segment["raw_end_byte_exclusive"]]
        expected = source + (b"\n" if document["id"] == "COLOPHON" else b"")
        path = _join(output, PurePosixPath(document["path"]))
        actual = path.read_bytes()
        _check(actual == expected, f"canonical zero-repair bytes drift: {document['id']}")
        file_records.append(_file_record(document["path"], "CANONICAL_AUTHOR_TEXT", actual))
        owned = grouped[document["id"]]
        for block in owned:
            tape_order += 1
            output_start = block["start_byte"] - segment["raw_start_byte"]
            output_end = block["end_byte_exclusive"] - segment["raw_start_byte"]
            tape.append({
                "document_id": document["id"],
                "document_order": document["order"],
                "output_end_byte_exclusive": output_end,
                "output_path": document["path"],
                "output_sha256": block["raw_sha256"],
                "output_start_byte": output_start,
                "projection": "IDENTITY",
                "raw_block_id": block["raw_block_id"],
                "raw_end_byte_exclusive": block["end_byte_exclusive"],
                "raw_order": block["order"],
                "raw_sha256": block["raw_sha256"],
                "raw_start_byte": block["start_byte"],
                "record_type": "SOURCE_BLOCK",
                "schema_version": SCHEMA_VERSION,
                "tape_order": tape_order,
            })
        generated = 0
        if document["id"] == "COLOPHON":
            generated = 1
            tape_order += 1
            tape.append({
                "author_text_projection_byte_size": 0,
                "document_id": document["id"],
                "document_order": document["order"],
                "generated_kind": "FILE_TERMINATOR_LF",
                "inverse": "DROP_EXACT_BYTES",
                "output_end_byte_exclusive": len(actual),
                "output_path": document["path"],
                "output_sha256": lf_hash,
                "output_start_byte": len(actual) - 1,
                "record_type": "GENERATED_METADATA",
                "schema_version": SCHEMA_VERSION,
                "tape_order": tape_order,
            })
        document_records.append({
            "block_count": len(owned),
            "first_raw_block_id": owned[0]["raw_block_id"],
            "generated_span_count": generated,
            "id": document["id"],
            "last_raw_block_id": owned[-1]["raw_block_id"],
            "order": document["order"],
            "output_byte_size": len(actual),
            "output_sha256": _sha(actual),
            "path": document["path"],
            "raw_projection_byte_size": len(source),
            "raw_projection_sha256": segment["raw_segment_sha256"],
            "role": "CANONICAL_AUTHOR_TEXT",
        })
    return tape, document_records, file_records


def _inverse(output: Path, tape: list[dict[str, Any]], documents: list[dict[str, Any]]) -> bytes:
    payloads = {document["path"]: _join(output, PurePosixPath(document["path"])).read_bytes() for document in documents}
    recovered = bytearray()
    next_raw = 1
    for tape_order, row in enumerate(tape, 1):
        _check(row.get("tape_order") == tape_order, f"inverse tape order drift: {tape_order}")
        payload = payloads.get(row.get("output_path"))
        _check(payload is not None, f"inverse path drift: {tape_order}")
        start = row.get("output_start_byte")
        end = row.get("output_end_byte_exclusive")
        _check(_exact_int(start) and _exact_int(end) and 0 <= start < end <= len(payload), f"inverse span drift: {tape_order}")
        fragment = payload[start:end]
        _check(_sha(fragment) == row.get("output_sha256"), f"inverse span hash drift: {tape_order}")
        if row.get("record_type") == "SOURCE_BLOCK":
            _check(row.get("projection") == "IDENTITY" and row.get("raw_order") == next_raw, f"inverse raw order drift: {next_raw}")
            _check(row.get("raw_block_id") == f"RAW-{next_raw:06d}" and row.get("raw_sha256") == _sha(fragment), f"inverse raw identity drift: {next_raw}")
            recovered.extend(fragment)
            next_raw += 1
        else:
            _check(row.get("record_type") == "GENERATED_METADATA", f"inverse record type drift: {tape_order}")
            _check(row.get("generated_kind") == "FILE_TERMINATOR_LF" and row.get("inverse") == "DROP_EXACT_BYTES", "generated inverse drift")
            _check(row.get("author_text_projection_byte_size") == 0 and fragment == b"\n", "generated inverse payload drift")
    _check(next_raw == len(snapshot_blocks := [row for row in tape if row.get("record_type") == "SOURCE_BLOCK"]) + 1, "inverse source-block count drift")
    _check(len(snapshot_blocks) == 20430, "inverse source-block contract drift")
    return bytes(recovered)


def _manifest(snapshot: dict[str, Any], tape_raw: bytes, tape: list[dict[str, Any]], documents: list[dict[str, Any]], files: list[dict[str, Any]], inverse: bytes) -> dict[str, Any]:
    contract = snapshot["contract"]
    counts = contract["counts"]
    tape_record = _file_record(TAPE_RELATIVE.as_posix(), "RELEASE_METADATA", tape_raw)
    payload_records = [*files, tape_record]
    return {
        "certification": "UNCERTIFIED_ZERO_REPAIR",
        "contract_id": CONTRACT_ID,
        "counts": {"canonical_documents": 29, "generated_author_file_spans": 1, "metadata_files": 2, "output_author_file_bytes": counts["output_author_file_bytes"], "projection_tape_rows": len(tape), "source_blocks": 20430, "source_projection_bytes": len(snapshot["monolith"])},
        "documents": documents,
        "inputs": {
            "baseline_lock_sha256": contract["frozen_inputs"]["baseline_lock_sha256"],
            "corpus_manifest_sha256": contract["frozen_inputs"]["corpus_manifest_sha256"],
            "guardrails_sha256": contract["frozen_inputs"]["guardrails_sha256"],
            "legacy_monolith_relative_path": f"{LEGACY_RELATIVE.as_posix()}/{MONOLITH_RELATIVE.as_posix()}",
            "monolith_byte_size": len(snapshot["monolith"]),
            "monolith_sha256": _sha(snapshot["monolith"]),
            "structure_ledger_sha256": contract["frozen_inputs"]["structure_ledger_sha256"],
            "tool_sources": snapshot["tool_sources"],
            "zero_repair_contract_sha256": CONTRACT_SHA256,
            "zero_repair_implementation_lock_sha256": IMPLEMENTATION_LOCK_SHA256,
        },
        "inverse_proof": {"algorithm": "READ_OUTPUT_SPANS_IN_TAPE_ORDER_DROP_TYPED_GENERATED_METADATA", "recovered_byte_size": len(inverse), "recovered_sha256": _sha(inverse), "source_block_sequence_sha256": snapshot["source_sequence"]},
        "output_payload": {"file_count_excluding_manifest": len(payload_records), "files": sorted(payload_records, key=lambda item: item["path"]), "tree_sha256_excluding_manifest": _tree_digest(payload_records)},
        "profile": contract["projection_profile"],
        "schema_version": SCHEMA_VERSION,
    }


def independently_validate_zero_repair(
    repo_root: Path,
    output_root: Path,
    *,
    goal_root: Path | None = None,
    legacy_root: Path | None = None,
    expected_runtime_sha256: str | None = None,
    include_receipt: bool = False,
) -> dict[str, Any]:
    """Validate one complete tree without consulting compiler implementation."""

    _check(output_root.is_absolute(), "output root must be absolute")
    repo = _absolute(repo_root)
    goal = _override(repo, goal_root, PurePosixPath("goal-4"))
    legacy = _override(repo, legacy_root, LEGACY_RELATIVE)
    repaired = _join(repo, REPAIRED_RELATIVE)
    output = _absolute(output_root)
    _plain_directory(repo, "repository root")
    _plain_directory(goal, "Goal 4 root")
    _plain_directory(legacy, "legacy root")
    _check(output not in {repo, goal, legacy, repaired}, "output aliases a governed root")
    _check(not _within(output, legacy) and not _within(output, repaired), "output is inside a governed corpus root")
    if _within(output, repo):
        _check(_within(output, goal), "repository-local output is outside Goal 4")
    _plain_directory(output, "zero-repair output root", exact_mode=DIRECTORY_MODE)
    snapshot = _load_source(
        repo,
        goal,
        legacy,
        expected_runtime_sha256=expected_runtime_sha256,
    )
    for source in snapshot["inputs"]:
        _check(not _within(source, output), "output contains a frozen input")
    initial_receipt = _inventory(output, snapshot["documents"])

    tape_raw = _join(output, TAPE_RELATIVE).read_bytes()
    manifest_raw = _join(output, MANIFEST_RELATIVE).read_bytes()
    tape = _jsonl(tape_raw, "projection tape")
    manifest = _json(manifest_raw, "zero-repair manifest", canonical=True)
    _check(isinstance(manifest, dict), "zero-repair manifest is not an object")
    expected_tape, document_records, file_records = _expected_projection(snapshot, output)
    _check(tape == expected_tape, "projection tape differs from independently derived mapping")
    _check(_sha(tape_raw) == snapshot["contract"]["proof"]["projection_tape_sha256"], "projection tape contract hash drift")
    inverse = _inverse(output, tape, snapshot["documents"])
    _check(inverse == snapshot["monolith"], "independent inverse differs from frozen monolith")
    expected_manifest = _manifest(snapshot, tape_raw, tape, document_records, file_records, inverse)
    _check(manifest == expected_manifest and manifest_raw == _canonical(expected_manifest), "zero-repair manifest differs from independent derivation")
    payload_hash = expected_manifest["output_payload"]["tree_sha256_excluding_manifest"]
    _check(payload_hash == snapshot["contract"]["proof"]["payload_tree_sha256_excluding_manifest"], "payload tree contract hash drift")
    _check(_sha(inverse) == snapshot["contract"]["proof"]["inverse_sha256"], "inverse contract hash drift")
    final_receipt = _inventory(output, snapshot["documents"])
    _check(initial_receipt == final_receipt, "output mutated during independent validation")
    receipt_sha256 = _sha(_canonical(final_receipt, lf=False))
    result = {
        "canonical_documents": 29,
        "contract_sha256": CONTRACT_SHA256,
        "implementation_lock_sha256": IMPLEMENTATION_LOCK_SHA256,
        "generated_spans": 1,
        "independent_oracle": True,
        "inverse_byte_size": len(inverse),
        "inverse_sha256": _sha(inverse),
        "manifest_sha256": _sha(manifest_raw),
        "payload_tree_sha256": payload_hash,
        "projection_tape_rows": len(tape),
        "projection_tape_sha256": _sha(tape_raw),
        "source_blocks": 20430,
        "verification_boundary": VERIFICATION_BOUNDARY,
        "verification_receipt_sha256": receipt_sha256,
        "verifier_sha256": snapshot["verifier_sha256"],
    }
    if include_receipt:
        result["verification_receipt"] = final_receipt
    return result
