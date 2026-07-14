#!/usr/bin/env python3
"""Independent Stage 1 contract and publication-path checks."""

from __future__ import annotations

import hashlib
import base64
import json
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class GuardrailError(ValueError):
    """Raised when a frozen Goal 4 guardrail is violated."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GuardrailError(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GuardrailError(f"cannot load JSON {path}: {error}") from error
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """ANKOS-CJ-1 bytes for the Stage 1 integer/string/bool schemas."""

    def reject_float(item: Any) -> None:
        if isinstance(item, float):
            raise GuardrailError("ANKOS-CJ-1 forbids floating-point values")
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), "ANKOS-CJ-1 object keys must be strings")
                reject_float(child)
        elif isinstance(item, list):
            for child in item:
                reject_float(child)

    reject_float(value)
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def pretty_contract_json_bytes(value: Any) -> bytes:
    """ANKOS-PJ-1 bytes for hand-authored frozen policy JSON."""

    def reject_float(item: Any) -> None:
        if isinstance(item, float):
            raise GuardrailError("ANKOS-PJ-1 forbids floating-point values")
        if isinstance(item, dict):
            for key, child in item.items():
                require(isinstance(key, str), "ANKOS-PJ-1 object keys must be strings")
                reject_float(child)
        elif isinstance(item, list):
            for child in item:
                reject_float(child)

    reject_float(value)
    return (
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def safe_relative_posix(path_text: str, *, placeholders: bool = False) -> PurePosixPath:
    require("\\" not in path_text, f"path must use POSIX separators: {path_text}")
    path = PurePosixPath(path_text)
    require(not path.is_absolute(), f"path must be relative: {path_text}")
    require(path.parts, "path cannot be empty")
    require(".." not in path.parts and "." not in path.parts, f"unsafe path: {path_text}")
    if not placeholders:
        require("<" not in path_text and ">" not in path_text, f"placeholder not allowed: {path_text}")
    return path


def is_component_descendant(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return path != parent


def _existing_components_have_symlink(repo_root: Path, relative: PurePosixPath) -> bool:
    current = repo_root
    for part in relative.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink():
                return True
    return False


def _absolute_path_has_symlink_component(path: Path) -> bool:
    """Check lexical absolute path components without resolving aliases away."""

    require(path.is_absolute(), f"path must be absolute: {path}")
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            return True
    return False


def validate_root_relationship(
    repo_root: Path,
    legacy_relative: str,
    repaired_relative: str,
) -> tuple[Path, Path]:
    repo_root = repo_root.resolve(strict=True)
    legacy_rel = safe_relative_posix(legacy_relative)
    repaired_rel = safe_relative_posix(repaired_relative)
    require(not _existing_components_have_symlink(repo_root, legacy_rel), "legacy path has a symlink component")
    require(not _existing_components_have_symlink(repo_root, repaired_rel), "repaired path has a symlink component")
    legacy = (repo_root / Path(*legacy_rel.parts)).resolve(strict=False)
    repaired = (repo_root / Path(*repaired_rel.parts)).resolve(strict=False)
    require(legacy != repaired, "repaired root equals legacy root")
    require(not is_component_descendant(repaired, legacy), "repaired root is inside legacy root")
    require(legacy.parent == repaired.parent, "legacy and repaired roots must be siblings")
    require(legacy.name == "A-New-Kind-of-Science", "unexpected legacy root name")
    require(repaired.name == "A-New-Kind-of-Science-Repaired", "unexpected repaired root name")
    return legacy, repaired


def validate_exact_goal_output(
    repo_root: Path,
    output: Path,
    expected_relative: str,
) -> Path:
    repo_root = repo_root.resolve(strict=True)
    expected_rel = safe_relative_posix(expected_relative)
    require(expected_rel.parts[0] == "goal-4", "owned generated output must be under goal-4")
    expected = repo_root / Path(*expected_rel.parts)
    require(".." not in output.parts, "generated output path contains '..'")
    candidate = output if output.is_absolute() else repo_root / output
    require(
        not _absolute_path_has_symlink_component(candidate),
        "generated output path has a symlink component",
    )
    require(candidate.parent.resolve(strict=True) == expected.parent.resolve(strict=True), "generated output parent drift")
    require(candidate.name == expected.name, "generated output must use the exact owned filename")
    require(candidate.resolve(strict=False) == expected.resolve(strict=False), "generated output path alias drift")
    return expected


def _file_mode(path: Path) -> str:
    return format(stat.S_IMODE(path.stat(follow_symlinks=False).st_mode), "04o")


def validate_publication_target(
    target: Path,
    legacy: Path,
    trusted_manifest_path: Path | None = None,
) -> str:
    require(target.is_absolute() and legacy.is_absolute(), "publication paths must be absolute")
    require(".." not in target.parts and ".." not in legacy.parts, "publication path contains '..'")
    require(not _absolute_path_has_symlink_component(legacy), "legacy publication path has a symlink component")
    require(not _absolute_path_has_symlink_component(target), "publication target has a symlink component")
    legacy = legacy.resolve(strict=True)
    require(legacy.name == "A-New-Kind-of-Science", "unexpected legacy publication root")
    require(legacy.parent.name == "ref", "legacy publication root must be under ref")
    expected_target = legacy.parent / "A-New-Kind-of-Science-Repaired"
    require(target == expected_target, "publication target is not the exact repaired sibling")
    if not target.exists():
        return "ABSENT"
    require(target.is_dir(), "publication target must be a directory")
    entries = sorted(target.iterdir(), key=lambda item: item.name)
    if not entries:
        return "EMPTY"
    require(trusted_manifest_path is not None, "nonempty publication target lacks a trusted external manifest")
    require(trusted_manifest_path.is_absolute(), "trusted manifest path must be absolute")
    require(".." not in trusted_manifest_path.parts, "trusted manifest path contains '..'")
    require(
        not _absolute_path_has_symlink_component(trusted_manifest_path),
        "trusted manifest path has a symlink component",
    )
    trusted_root = legacy.parent.parent / "goal-4/releases"
    require(trusted_root.is_dir(), "trusted release-manifest registry is missing")
    require(
        not _absolute_path_has_symlink_component(trusted_root),
        "trusted release-manifest registry has a symlink component",
    )
    require(
        trusted_manifest_path.parent == trusted_root,
        "trusted manifest is outside the exact goal-4/releases registry",
    )
    require(trusted_manifest_path.suffix == ".json", "trusted manifest must be JSON")
    require(trusted_manifest_path.is_file(), "trusted manifest is not a regular file")
    require(trusted_manifest_path.stat().st_nlink == 1, "trusted manifest may not be hardlinked")
    trusted_manifest = load_json(trusted_manifest_path)
    require(trusted_manifest.get("schema_version") == "1.0.0", "trusted manifest schema drift")
    require(
        trusted_manifest.get("target") == "ref/A-New-Kind-of-Science-Repaired",
        "trusted manifest target drift",
    )
    rows = trusted_manifest.get("files")
    require(isinstance(rows, list), "trusted manifest files must be an array")
    expected: dict[str, dict[str, Any]] = {}
    for row in rows:
        require(isinstance(row, dict), "trusted manifest file row must be an object")
        relative = str(safe_relative_posix(row.get("path", "")))
        require(relative not in expected, f"duplicate trusted manifest path: {relative}")
        require(row.get("entry_type") in {"FILE", "DIRECTORY"}, f"unknown trusted entry type: {relative}")
        expected[relative] = row
    observed: dict[str, tuple[Path, str]] = {}
    for path in sorted(target.rglob("*"), key=lambda item: item.as_posix()):
        require(not path.is_symlink(), f"symlink in publication target: {path}")
        relative = path.relative_to(target).as_posix()
        if path.is_file():
            require(path.stat().st_nlink == 1, f"hardlinked publication file: {relative}")
            observed[relative] = (path, "FILE")
        else:
            require(path.is_dir(), f"unsupported target entry: {path}")
            observed[relative] = (path, "DIRECTORY")
    require(set(observed) == set(expected), "publication target has missing or unowned files")
    for relative, (path, entry_type) in observed.items():
        row = expected[relative]
        require(row.get("entry_type") == entry_type, f"owned target type drift: {relative}")
        require(row.get("mode") == _file_mode(path), f"owned target mode drift: {relative}")
        if entry_type == "FILE":
            require(row.get("sha256") == sha256_file(path), f"owned target hash drift: {relative}")
            require(row.get("byte_size") == path.stat().st_size, f"owned target size drift: {relative}")
        else:
            require("sha256" not in row and "byte_size" not in row, f"directory has file fields: {relative}")
    return "MANIFEST_OWNED"


def framed_behavior_digest(exit_code: int, stdout: bytes, stderr: bytes) -> str:
    frame = bytearray(b"ANKOS-ORACLE-BEHAVIOR-v1\0")
    frame.extend(str(exit_code).encode("ascii"))
    frame.extend(b"\0")
    for stream in (stdout, stderr):
        frame.extend(len(stream).to_bytes(8, "big"))
        frame.extend(stream)
    return sha256_bytes(bytes(frame))


def aggregate_behavior_digest(rows: list[dict[str, Any]]) -> str:
    projection = [
        {
            "path": row["path"],
            "status_kind": row["status_kind"],
            "exit_code": row["exit_code"],
            "stdout_sha256": row["stdout_sha256"],
            "stderr_sha256": row["stderr_sha256"],
            "framed_behavior_sha256": row["framed_behavior_sha256"],
        }
        for row in sorted(rows, key=lambda item: item["path"])
    ]
    return sha256_bytes(canonical_json_bytes(projection))


def filename_set_digest(names: Iterable[str]) -> str:
    payload = "".join(f"{name}\n" for name in sorted(names)).encode("utf-8")
    return sha256_bytes(payload)


def legacy_recursive_signature(root: Path) -> dict[str, Any]:
    """Diagnostic recursive signature used only to detect consumer contamination."""

    require(root.is_dir(), f"legacy fixture root is missing: {root}")
    markdown: list[str] = []
    jpeg: list[str] = []
    basenames: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        require(not path.is_symlink(), f"legacy fixture contains a symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix == ".md":
            markdown.append(relative)
        elif path.suffix == ".jpeg":
            jpeg.append(relative)
            basenames.setdefault(path.name, []).append(relative)
    signature_body = {
        "markdown_paths": markdown,
        "jpeg_paths": jpeg,
        "duplicate_jpeg_basenames": {
            name: paths for name, paths in sorted(basenames.items()) if len(paths) > 1
        },
    }
    return {
        **signature_body,
        "signature_sha256": sha256_bytes(canonical_json_bytes(signature_body)),
    }


def _frozen_path_list(value: Any, label: str) -> list[str]:
    require(isinstance(value, list) and value, f"{label} must be a nonempty array")
    paths: list[str] = []
    for item in value:
        require(isinstance(item, str), f"{label} contains a non-string path")
        normalized = str(safe_relative_posix(item))
        require(normalized == item, f"{label} path is not canonical: {item}")
        paths.append(item)
    require(len(paths) == len(set(paths)), f"{label} contains duplicate paths")
    require(paths == sorted(paths), f"{label} must be sorted")
    return paths


def derive_oracle_classifications(root: Path, contract: dict[str, Any]) -> list[dict[str, Any]]:
    """Re-derive the complete Goal 1 oracle census from frozen explicit scope."""

    compatibility = contract.get("compatibility", {})
    all_paths = _frozen_path_list(compatibility.get("all_oracle_paths"), "all oracle paths")
    affected_paths = _frozen_path_list(
        compatibility.get("recursive_affected_paths"), "recursive affected paths"
    )
    image_paths = _frozen_path_list(
        compatibility.get("recursive_image_or_basename_paths"),
        "recursive image/basename paths",
    )
    actual_paths = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "goal-1").glob("*-oracle.py")
        if path.is_file() and not path.is_symlink()
    )
    require(actual_paths == all_paths, "current Goal 1 oracle path set differs from frozen explicit scope")
    require(set(affected_paths) <= set(all_paths), "affected oracle scope is not a subset of all oracles")
    require(set(image_paths) <= set(affected_paths), "image oracle scope is not a subset of affected oracles")
    require(len(all_paths) == compatibility.get("goal_1_root_oracle_count"), "all-oracle count drift")
    require(
        len(affected_paths) == compatibility.get("goal_1_recursive_affected_count"),
        "affected-oracle count drift",
    )
    require(
        len(image_paths) == compatibility.get("goal_1_recursive_image_or_basename_count"),
        "image-oracle count drift",
    )
    require(
        filename_set_digest(path.removeprefix("goal-1/") for path in all_paths)
        == compatibility.get("all_oracle_filename_digest"),
        "all-oracle frozen digest drift",
    )
    require(
        filename_set_digest(path.removeprefix("goal-1/") for path in affected_paths)
        == compatibility.get("recursive_affected_filename_digest"),
        "affected-oracle frozen digest drift",
    )

    affected_set = set(affected_paths)
    image_set = set(image_paths)
    rows: list[dict[str, Any]] = []
    for relative in all_paths:
        path = root / relative
        require(path.is_file() and not path.is_symlink(), f"oracle path is not a regular file: {relative}")
        text = path.read_text(encoding="utf-8")
        recursive_markdown = bool(re.search(r"\.rglob\(\s*['\"]\*\.md['\"]\s*\)", text))
        recursive_image = bool(re.search(r"\.rglob\(\s*['\"]\*\.jpeg['\"]\s*\)", text)) or any(
            marker in text
            for marker in (
                ".rglob(basename)",
                ".rglob(spec.name)",
                ".rglob(Path(match.group(1)).name)",
            )
        )
        recursive_affected = relative in affected_set
        require(
            recursive_markdown is recursive_affected,
            f"frozen affected classification disagrees with recursive Markdown evidence: {relative}",
        )
        require(
            recursive_image is (relative in image_set),
            f"frozen image classification disagrees with recursive image evidence: {relative}",
        )
        direct_legacy = "A-New-Kind-of-Science" in text and not recursive_affected
        rows.append(
            {
                "path": relative,
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
    require(
        sum(row["direct_legacy_path"] for row in rows)
        == compatibility.get("goal_1_direct_legacy_semantic_count"),
        "direct legacy semantic census drift",
    )
    require(
        sum(row["kind"] == "NO_LEGACY_PATH" for row in rows)
        == compatibility.get("goal_1_no_legacy_path_count"),
        "no-legacy-path semantic census drift",
    )
    return rows


def governed_dependency_paths(root: Path, contract: dict[str, Any]) -> list[Path]:
    """Return the exact compatibility dependency closure declared by Stage 1."""

    compatibility = contract.get("compatibility", {})
    legacy = root / contract["architecture"]["legacy_root"]
    require(legacy.is_dir(), "legacy dependency root is missing")
    candidates: set[Path] = set()
    for path in sorted(legacy.rglob("*"), key=lambda item: item.as_posix()):
        require(not path.is_symlink(), f"legacy dependency scope contains a symlink: {path}")
        if path.is_file():
            candidates.add(path)
    require(
        len(candidates) == contract["legacy_input"]["expected_counts"]["all_regular_files"],
        "legacy dependency file count drift",
    )
    governed_relatives = _frozen_path_list(
        compatibility.get("recursive_affected_paths"), "recursive affected paths"
    ) + _frozen_path_list(
        compatibility.get("additional_dependency_paths"), "additional dependency paths"
    )
    require(len(governed_relatives) == len(set(governed_relatives)), "dependency scopes overlap")
    for relative in governed_relatives:
        path = root / relative
        require(path.is_file() and not path.is_symlink(), f"governed dependency is missing: {relative}")
        candidates.add(path)
    return sorted(candidates, key=lambda path: path.relative_to(root).as_posix())


def dependency_rows_and_fingerprint(
    root: Path, paths: Iterable[Path]
) -> tuple[list[dict[str, Any]], str]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        require(path.is_file() and not path.is_symlink(), f"dependency disappeared: {path}")
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "byte_size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    rows.sort(key=lambda row: row["path"])
    require(len(rows) == len({row["path"] for row in rows}), "duplicate dependency path")
    return rows, sha256_bytes(canonical_json_bytes(rows))


def row_subset_fingerprint(rows: list[dict[str, Any]], prefix: str) -> str:
    subset = [row for row in rows if row.get("path", "").startswith(prefix)]
    return sha256_bytes(canonical_json_bytes(subset))


def git_tree_identity(root: Path, revision: str, relative: str) -> str:
    safe_relative_posix(relative)
    result = subprocess.run(
        ["git", "rev-parse", f"{revision}:{relative}"],
        cwd=root,
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"cannot read Git tree {revision}:{relative}")
    return result.stdout.decode("ascii").strip()


EXPECTED_REPAIR_CLASSES = {
    "STRUCTURE_BOUNDARY",
    "MARKDOWN_STRUCTURE",
    "PROSE_OCR",
    "HEADING_OR_FURNITURE",
    "FORMULA_OR_SYMBOL",
    "WOLFRAM_CODE",
    "RULE_TABLE_OR_DATA",
    "FIGURE_OR_CAPTION",
    "INDEX_ENTRY",
    "NAVIGATION_METADATA",
    "SOURCE_ERRATUM_ANNOTATION",
    "SEARCH_NORMALIZATION",
}

EXPECTED_WORKFLOW_STATES = {
    "CAPTURED",
    "EVIDENCE_READY",
    "PENDING_SPECIALIST_REVIEW",
    "PENDING_INDEPENDENT_REVIEW",
    "SOURCE_BLOCKED",
    "CLOSED",
}

EXPECTED_DISPOSITIONS = {
    "APPLIED_MECHANICALLY_PROVEN",
    "APPLIED_WITNESS_VERIFIED",
    "ANNOTATED_SOURCE_ERRATUM",
    "REJECTED_VALID_SOURCE_TEXT",
    "DUPLICATE_CANDIDATE",
    "UNRESOLVED_SOURCE_NEEDED",
}

EXPECTED_NOT_APPLICABLE = {
    "BLANK_PAGE",
    "RUNNING_HEADER",
    "PRINTED_PAGE_NUMBER",
    "SCANNER_OR_EXTRACTION_ARTIFACT",
    "NONAUTHORIAL_BINDING_OR_CROP",
}

EXPECTED_HIGH_RISK = {
    "STRUCTURE_BOUNDARY",
    "MARKDOWN_STRUCTURE",
    "HEADING_OR_FURNITURE",
    "FORMULA_OR_SYMBOL",
    "WOLFRAM_CODE",
    "RULE_TABLE_OR_DATA",
    "FIGURE_OR_CAPTION",
    "INDEX_ENTRY",
}

EXPECTED_ROLE_KEYS = {
    "CANONICAL_AUTHOR_TEXT",
    "DERIVED_AGGREGATE",
    "GENERATED_METADATA",
    "EDITORIAL_SIDECAR",
    "SEARCH_DERIVATIVE",
    "GOVERNED_LEGACY_ASSET",
    "GOVERNED_WITNESS_ASSET",
    "RELEASE_METADATA",
}

EXPECTED_CONTRACT_PATHS = {
    "goal-4/fidelity-contract.md",
    "goal-4/style-guide.md",
    "goal-4/review-contract.md",
    "goal-4/quality-evaluation.json",
    "goal-4/licensing-contract.json",
    "goal-4/promotion-contract.md",
}

EXPECTED_SEPARATE_AUTHORIZATION = {
    "LEGACY_PROMOTION",
    "LEGACY_FILE_DELETION_RELOCATION_OR_RENAME",
    "GOAL_1_OR_GOAL_3_CONSUMER_MIGRATION",
    "CITATION_REWRITE",
    "COMMIT_PUSH_HOST_OR_EXTERNAL_REDISTRIBUTION",
}

EXPECTED_GUARDRAILS_CANONICAL_SHA256 = (
    "c446da937b7c174328364ca6e442781ed0270cd777cb0a86ef3a6917ae8a4a33"
)


def validate_quality(quality: dict[str, Any]) -> None:
    require(quality.get("protocol_version") == "1.0.0", "unexpected quality protocol version")
    require(
        quality.get("status") == "PROTOCOL_FROZEN_SAMPLE_IDS_PENDING_STAGE_2",
        "quality protocol is not frozen at the Stage 1 state",
    )
    require(quality.get("frozen_before_author_text_repairs") is True, "quality protocol was not pre-frozen")
    require(quality.get("materialized_sample") is None, "Stage 1 must not materialize outcome-aware samples")
    require(quality.get("results") is None, "Stage 1 quality results must be empty")
    seed = quality.get("seed", {})
    domain_hex = "414e4b4f532d474f414c342d484f4c444f55542d763100"
    require(seed.get("domain_separator_hex") == domain_hex, "quality domain separator bytes drift")
    known = seed.get("known_vector", {})
    require(known.get("manifest_material_utf8_hex") == "5b5d", "quality known-vector input drift")
    known_seed = sha256_bytes(bytes.fromhex(domain_hex) + bytes.fromhex("5b5d"))
    require(known.get("seed_sha256") == known_seed, "quality seed known vector fails")
    require(
        "0x00" in seed.get("rank_derivation", "") and "\\u0000" not in seed.get("rank_derivation", ""),
        "quality rank framing is ambiguous",
    )
    sample = quality.get("sample_size", {})
    require(
        sample.get("minimum_fraction_per_document") == {"numerator": 1, "denominator": 20},
        "quality sample fraction drift",
    )
    require(sample.get("minimum_blocks_per_document") == 20, "quality per-document minimum drift")
    require(
        sample.get("document_quota") == "q = min(N, max(ceil(N / 20), 20)), where N is the document's eligible-block count.",
        "quality document quota is not exact",
    )
    allocation = sample.get("risk_allocation", "")
    for term in ("a_s=R*c_s/C", "floor(a_s)", "(R*c_s) mod C"):
        require(term in allocation, f"quality risk allocation is underspecified: {term}")
    require(
        "before any author-text repair" in sample.get("held_out_selection", ""),
        "held-out membership is not frozen before repair",
    )
    require(
        "never alter membership" in sample.get("held_out_selection", ""),
        "held-out membership can change post hoc",
    )
    require("changed_unchanged_rule" not in sample, "outcome-aware held-out selection remains enabled")
    require(
        "only for reporting" in sample.get("post_repair_labels", ""),
        "post-repair labels can influence held-out selection",
    )
    require("Generated metadata alone" in sample.get("block_change_definition", ""), "block change semantics drift")
    risk_ids = [row.get("id") for row in quality.get("risk_strata", [])]
    require(
        risk_ids
        == [
            "INDEX_COLUMN_OR_ENTRY",
            "FORMULA_CODE_RULE_OR_DATA",
            "FIGURE_CAPTION_OR_VISUAL",
            "HEADING_LIST_OR_LAYOUT",
            "PROSE",
        ],
        "quality risk strata/order drift",
    )
    metrics = quality.get("metrics", {})
    exact_ratio = {"numerator": 1, "denominator": 1}
    zero_ratio = {"numerator": 0, "denominator": 1}
    require(
        metrics.get("author_text_character_projection_exactness", {}).get("minimum_ratio") == exact_ratio,
        "author text threshold weakened",
    )
    require(metrics.get("author_text_cer", {}).get("maximum_ratio") == zero_ratio, "CER threshold weakened")
    require(metrics.get("author_text_wer", {}).get("maximum_ratio") == zero_ratio, "WER threshold weakened")
    for name in (
        "heading_paragraph_list_boundary_exactness",
        "technical_token_exactness",
        "index_entry_column_sequence_exactness",
        "figure_caption_association_exactness",
        "known_defect_and_seeded_mutation_recall",
    ):
        require(metrics.get(name, {}).get("minimum_ratio") == exact_ratio, f"quality threshold weakened: {name}")
    require(
        quality.get("fixed_point", {}).get("required_consecutive_full_rounds_without_new_defect_class") == 2,
        "fixed-point round count drift",
    )
    require(quality.get("fixed_point", {}).get("open_queue_limit") == 0, "quality queue limit drift")
    severity = quality.get("severity", [])
    require(len(severity) == 5, "severity enum must contain five rows")
    for row in severity[:4]:
        require(row.get("full_release_blocker") is True, f"required severity no longer blocks: {row.get('id')}")
    require(severity[4].get("full_release_blocker") is False, "optional editorial severity must remain non-authorial")


def oracle_classification_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    names = [row["path"].removeprefix("goal-1/") for row in rows]
    affected_names = [
        row["path"].removeprefix("goal-1/")
        for row in rows
        if row["recursive_affected"]
    ]
    return {
        "all_count": len(rows),
        "all_filename_digest": filename_set_digest(names),
        "recursive_affected_count": len(affected_names),
        "recursive_affected_filename_digest": filename_set_digest(affected_names),
        "recursive_markdown_count": sum(row["recursive_markdown"] for row in rows),
        "recursive_image_or_basename_count": sum(
            row["recursive_image_or_basename"] for row in rows
        ),
        "direct_legacy_semantic_count": sum(row["direct_legacy_path"] for row in rows),
        "no_legacy_path_count": sum(row["kind"] == "NO_LEGACY_PATH" for row in rows),
    }


def validate_compatibility_baseline(
    baseline: dict[str, Any],
    contract: dict[str, Any],
    repo_root: Path,
    *,
    check_current_scripts: bool,
) -> None:
    require(baseline.get("schema_version") == "1.1.0", "unsupported compatibility baseline schema")
    require(baseline.get("contract_id") == contract.get("contract_id"), "baseline contract binding drift")
    compatibility = contract["compatibility"]
    execution = baseline.get("execution", {})
    require(execution.get("cwd") == ".", "compatibility cwd drift")
    require(execution.get("environment") == compatibility.get("environment"), "compatibility environment drift")
    require(execution.get("duration_excluded_from_behavior") is True, "duration entered behavior identity")
    require(execution.get("book_override_used") is False, "compatibility capture used a book override")
    require(
        execution.get("interpreter", {}).get("executable") == compatibility["argv_template"][0],
        "compatibility interpreter drift",
    )

    classifications = baseline.get("classifications", [])
    require(isinstance(classifications, list), "oracle classifications must be an array")
    require(
        [row.get("path") for row in classifications] == compatibility.get("all_oracle_paths"),
        "oracle classification paths differ from frozen explicit scope",
    )
    affected_paths = set(compatibility["recursive_affected_paths"])
    image_paths = set(compatibility["recursive_image_or_basename_paths"])
    for row in classifications:
        relative = row.get("path")
        require(row.get("recursive_affected") is (relative in affected_paths), f"affected flag drift: {relative}")
        require(row.get("recursive_markdown") is (relative in affected_paths), f"Markdown flag drift: {relative}")
        require(
            row.get("recursive_image_or_basename") is (relative in image_paths),
            f"image flag drift: {relative}",
        )
        require(isinstance(row.get("script_sha256"), str) and len(row["script_sha256"]) == 64, f"script hash missing: {relative}")
        expected_kind = (
            "RECURSIVE_SOURCE_OR_ASSET"
            if relative in affected_paths
            else "DIRECT_LEGACY_SEMANTIC"
            if row.get("direct_legacy_path") is True
            else "NO_LEGACY_PATH"
        )
        require(row.get("kind") == expected_kind, f"oracle kind drift: {relative}")
    summary = oracle_classification_summary(classifications)
    require(baseline.get("classification_summary") == summary, "classification summary drift")
    require(summary["all_count"] == compatibility["goal_1_root_oracle_count"], "oracle count mismatch")
    require(summary["recursive_affected_count"] == compatibility["goal_1_recursive_affected_count"], "affected count mismatch")
    require(summary["recursive_markdown_count"] == compatibility["goal_1_recursive_markdown_count"], "Markdown census mismatch")
    require(
        summary["recursive_image_or_basename_count"]
        == compatibility["goal_1_recursive_image_or_basename_count"],
        "image census mismatch",
    )
    require(
        summary["direct_legacy_semantic_count"] == compatibility["goal_1_direct_legacy_semantic_count"],
        "direct legacy semantic census mismatch",
    )
    require(
        summary["no_legacy_path_count"] == compatibility["goal_1_no_legacy_path_count"],
        "no-path semantic census mismatch",
    )

    context = baseline.get("closure", {})
    dependency_rows = context.get("dependency_rows")
    require(isinstance(dependency_rows, list), "baseline dependency rows are missing")
    require(
        [row.get("path") for row in dependency_rows]
        == sorted(row.get("path") for row in dependency_rows),
        "dependency rows are not sorted",
    )
    require(len(dependency_rows) == len({row.get("path") for row in dependency_rows}), "duplicate dependency row")
    for row in dependency_rows:
        safe_relative_posix(row.get("path", ""))
        require(isinstance(row.get("byte_size"), int) and row["byte_size"] >= 0, "invalid dependency size")
        require(isinstance(row.get("sha256"), str) and len(row["sha256"]) == 64, "invalid dependency hash")
    stored_dependency_fingerprint = sha256_bytes(canonical_json_bytes(dependency_rows))
    require(context.get("dependency_file_count") == len(dependency_rows), "dependency file count drift")
    require(
        context.get("dependency_fingerprint_before") == stored_dependency_fingerprint
        and context.get("dependency_fingerprint_after") == stored_dependency_fingerprint,
        "dependency closure fingerprint drift",
    )
    legacy_prefix = contract["architecture"]["legacy_root"] + "/"
    stored_legacy_fingerprint = row_subset_fingerprint(dependency_rows, legacy_prefix)
    require(
        context.get("legacy_content_fingerprint_before") == stored_legacy_fingerprint
        and context.get("legacy_content_fingerprint_after") == stored_legacy_fingerprint,
        "legacy content fingerprint drift",
    )
    require(
        context.get("legacy_regular_file_count")
        == contract["legacy_input"]["expected_counts"]["all_regular_files"],
        "legacy regular-file count drift",
    )
    require(context.get("git_head_before") == context.get("git_head_after"), "git HEAD moved during capture")
    require(context.get("legacy_git_tree_before") == context.get("legacy_git_tree_after"), "legacy Git tree moved during capture")
    require(context.get("legacy_tree_digest_before") == context.get("legacy_tree_digest_after"), "legacy recursive signature moved during capture")

    if check_current_scripts:
        current_classifications = derive_oracle_classifications(repo_root, contract)
        require(current_classifications == classifications, "current all-oracle classification or script bytes drift")
        current_paths = governed_dependency_paths(repo_root, contract)
        current_rows, current_fingerprint = dependency_rows_and_fingerprint(repo_root, current_paths)
        require(current_rows == dependency_rows, "current dependency closure rows drift")
        require(current_fingerprint == stored_dependency_fingerprint, "current dependency closure fingerprint drift")
        legacy_root = repo_root / contract["architecture"]["legacy_root"]
        current_signature = legacy_recursive_signature(legacy_root)
        require(
            current_signature["signature_sha256"] == context.get("legacy_tree_digest_before"),
            "current legacy recursive signature drift",
        )
        require(
            git_tree_identity(repo_root, "HEAD", contract["architecture"]["legacy_root"])
            == context.get("legacy_git_tree_before"),
            "current legacy Git tree drift",
        )

    records = baseline.get("oracles", [])
    require(len(records) == compatibility["expected_behavior_count"], "compatibility behavior count mismatch")
    require(
        [row.get("path") for row in records] == compatibility["recursive_affected_paths"],
        "behavior paths differ from frozen affected scope",
    )
    classification_by_path = {row["path"]: row for row in classifications}
    aggregate_rows: list[dict[str, Any]] = []
    for row in records:
        relative = row.get("path")
        require(row.get("repeat_count") == compatibility["repeat_runs_required"], f"oracle repeat count drift: {relative}")
        require(row.get("repeat_identical") is True, f"oracle repeat drift: {relative}")
        require(row.get("empty_sibling_identical") is True, f"empty sibling row drift: {relative}")
        require(row.get("post_removal_identical") is True, f"post-removal row drift: {relative}")
        require(row.get("argv") == [compatibility["argv_template"][0], "-B", relative], f"oracle argv drift: {relative}")
        require(isinstance(row.get("exit_code"), int), f"oracle exit code missing: {relative}")
        if row.get("status_kind") == "EXITED":
            require(row["exit_code"] >= 0, f"EXITED oracle has negative code: {relative}")
        elif row.get("status_kind") == "SIGNALED":
            require(row["exit_code"] < 0, f"SIGNALED oracle has nonnegative code: {relative}")
        else:
            require(row.get("status_kind") == "TIMED_OUT" and row["exit_code"] == 124, f"invalid status kind: {relative}")
        stdout = row.get("stdout", {})
        stderr = row.get("stderr", {})
        require(isinstance(stdout.get("base64"), str) and isinstance(stderr.get("base64"), str), "raw output bytes not captured")
        try:
            stdout_bytes = base64.b64decode(stdout["base64"], validate=True)
            stderr_bytes = base64.b64decode(stderr["base64"], validate=True)
        except (ValueError, TypeError) as error:
            raise GuardrailError(f"invalid raw output base64: {relative}") from error
        require(stdout.get("byte_count") == len(stdout_bytes), f"stdout byte count drift: {relative}")
        require(stderr.get("byte_count") == len(stderr_bytes), f"stderr byte count drift: {relative}")
        require(stdout.get("sha256") == sha256_bytes(stdout_bytes), f"stdout hash drift: {relative}")
        require(stderr.get("sha256") == sha256_bytes(stderr_bytes), f"stderr hash drift: {relative}")
        require(
            row.get("framed_behavior_sha256")
            == framed_behavior_digest(row["exit_code"], stdout_bytes, stderr_bytes),
            f"framed behavior drift: {relative}",
        )
        require(row.get("kind") == classification_by_path[relative]["kind"], f"oracle kind join drift: {relative}")
        require(
            row.get("script_sha256") == classification_by_path[relative]["script_sha256"],
            f"classification/behavior script hash drift: {relative}",
        )
        require(
            row.get("transitive_dependency_fingerprint") == stored_dependency_fingerprint,
            f"oracle dependency fingerprint drift: {relative}",
        )
        aggregate_rows.append(
            {
                "path": relative,
                "status_kind": row["status_kind"],
                "exit_code": row["exit_code"],
                "stdout_sha256": stdout["sha256"],
                "stderr_sha256": stderr["sha256"],
                "framed_behavior_sha256": row["framed_behavior_sha256"],
            }
        )
    recomputed_behavior = aggregate_behavior_digest(aggregate_rows)
    require(baseline.get("behavior_digest") == recomputed_behavior, "aggregate behavior digest drift")

    probe = baseline.get("empty_sibling_probe", {})
    require(probe.get("target") == contract["architecture"]["repaired_root"], "empty sibling target drift")
    require(probe.get("initial_state") == "ABSENT", "sibling probe did not start absent")
    require(probe.get("target_state") == "EMPTY", "sibling probe did not use an empty target")
    require(probe.get("final_state") == "ABSENT", "sibling probe did not restore absence")
    require(probe.get("cleanup_succeeded") is True, "sibling probe cleanup failed")
    require(probe.get("all_behavior_identical") is True, "sibling lifecycle changed oracle behavior")
    for field in (
        "baseline_behavior_digest",
        "empty_sibling_behavior_digest",
        "post_removal_behavior_digest",
    ):
        require(probe.get(field) == recomputed_behavior, f"sibling probe digest drift: {field}")

    health = baseline.get("health_summary", {})
    nonzero = [row["path"] for row in records if row["exit_code"] != 0]
    require(health.get("exit_zero") == len(records) - len(nonzero), "health zero count drift")
    require(health.get("exit_nonzero") == len(nonzero), "health nonzero count drift")
    require(health.get("nonzero_paths") == nonzero, "health nonzero paths drift")
    require(health.get("health_is_not_behavioral_identity") is True, "health/identity distinction drift")

    goal3 = baseline.get("goal_3", {})
    require(goal3.get("executable_validator_count") == 0, "Stage 1 Goal 3 executable census drift")
    require(
        goal3.get("planning_filename_digest") == filename_set_digest(goal3.get("planning_files", [])),
        "Goal 3 planning digest drift",
    )
    if check_current_scripts:
        current_goal3_files = sorted(
            path.relative_to(repo_root).as_posix()
            for path in (repo_root / "goal-3").rglob("*")
            if path.is_file() and not path.is_symlink()
        )
        require(goal3.get("planning_files") == current_goal3_files, "current Goal 3 planning scope drift")
    require(
        sha256_bytes(canonical_json_bytes(baseline)) == compatibility.get("baseline_sha256"),
        "whole compatibility baseline digest drift",
    )


def validate_contract(
    contract: dict[str, Any],
    quality: dict[str, Any],
    licensing: dict[str, Any],
    repo_root: Path,
    *,
    baseline: dict[str, Any] | None = None,
    check_files: bool = True,
    check_current_scripts: bool = True,
) -> None:
    require(contract.get("contract_id") == "ANKOS-GUARDRAILS-1", "unexpected guardrail contract ID")
    require(contract.get("version") == "1.0.0", "unexpected guardrail contract version")
    require(contract.get("status") == "FROZEN_STAGE_1", "guardrail contract is not frozen")
    require(contract.get("frozen_on") == "2026-07-14", "guardrail freeze date drift")
    architecture = contract.get("architecture", {})
    legacy, repaired = validate_root_relationship(
        repo_root,
        architecture.get("legacy_root", ""),
        architecture.get("repaired_root", ""),
    )
    require(legacy.is_dir(), "legacy root is missing")
    require(architecture.get("repository_root") == ".", "repository root drift")
    require(architecture.get("goal_root") == "goal-4", "goal root drift")
    require(architecture.get("allowed_write_roots") == ["goal-4", "ref/A-New-Kind-of-Science-Repaired"], "write scope drift")
    require(
        architecture.get("forbidden_write_roots")
        == ["ref/A-New-Kind-of-Science", "goal-1", "goal-2", "goal-3", "src", "tests"],
        "forbidden write scope drift",
    )
    paths = architecture.get("path_rules", {})
    for flag in (
        "component_aware_containment_required",
        "string_prefix_containment_forbidden",
        "legacy_equality_forbidden",
        "legacy_descendant_output_forbidden",
        "dotdot_alias_forbidden",
        "symlink_alias_forbidden",
    ):
        require(paths.get(flag) is True, f"path guard disabled: {flag}")
    require(
        paths.get("prefix_named_sibling_required_to_pass")
        == "ref/A-New-Kind-of-Science-Repaired",
        "prefix-named sibling path rule drift",
    )
    require(
        set(contract.get("separate_authorization_required", [])) == EXPECTED_SEPARATE_AUTHORIZATION,
        "separate-authorization scope drift",
    )
    raw = contract.get("legacy_input", {})
    require(raw.get("discovery") == "EXPLICIT_MANIFEST_ROWS_ONLY", "raw input is not explicit-manifest-only")
    require(raw.get("recursive_build_input_discovery_allowed") is False, "recursive raw build discovery enabled")
    require(raw.get("generated_output_may_be_build_input") is False, "generated output allowed as input")
    require(raw.get("expected_counts") == {"markdown": 19, "jpeg": 1444, "all_regular_files": 1463}, "raw expected counts drift")
    documents = contract.get("canonical_documents", [])
    require(len(documents) == 29, "canonical document count must be 29")
    require([row.get("order") for row in documents] == list(range(29)), "canonical order is not contiguous")
    ids = [row.get("id") for row in documents]
    anchor_slugs = [row.get("anchor_slug") for row in documents]
    doc_paths = [row.get("path") for row in documents]
    require(len(set(ids)) == 29 and len(set(doc_paths)) == 29, "canonical IDs/paths must be unique")
    require(len(set(anchor_slugs)) == 29, "canonical anchor slugs must be unique")
    require(all(isinstance(value, str) and re.fullmatch(r"[A-Z0-9_]+", value) for value in ids), "canonical ID grammar drift")
    require(
        all(
            isinstance(value, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value)
            for value in anchor_slugs
        ),
        "canonical anchor-slug grammar drift",
    )
    require(all(row.get("role") == "CANONICAL_AUTHOR_TEXT" for row in documents), "noncanonical role in document list")
    for path in doc_paths:
        safe_relative_posix(path)
        require(path.startswith("CANONICAL/"), f"canonical path outside CANONICAL: {path}")
    kind_counts = {kind: sum(row.get("kind") == kind for row in documents) for kind in {row.get("kind") for row in documents}}
    require(
        kind_counts == {"FRONT_MATTER": 2, "CHAPTER": 12, "NOTES": 13, "INDEX": 1, "COLOPHON": 1},
        f"canonical kind counts drift: {kind_counts}",
    )
    outputs = contract.get("declared_outputs", [])
    require(len(outputs) == 10, "declared output count drift")
    require(all(set(row) == {"path", "role"} for row in outputs), "declared output row shape drift")
    output_pairs = {(row.get("path"), row.get("role")) for row in outputs}
    required_outputs = {
        ("README.md", "GENERATED_METADATA"),
        ("corpus-manifest.json", "RELEASE_METADATA"),
        ("release-manifest.json", "RELEASE_METADATA"),
        ("DERIVED/A-New-Kind-of-Science.md", "DERIVED_AGGREGATE"),
        ("DERIVED/Contents.md", "GENERATED_METADATA"),
        ("EDITORIAL/Errata.md", "EDITORIAL_SIDECAR"),
        ("EDITORIAL/Alt-Text.md", "EDITORIAL_SIDECAR"),
        ("SEARCH/search-corpus.jsonl", "SEARCH_DERIVATIVE"),
        ("ASSETS/LEGACY/<legacy-relative-path>", "GOVERNED_LEGACY_ASSET"),
        ("ASSETS/WITNESS/<asset-id>/<source-basename>", "GOVERNED_WITNESS_ASSET"),
    }
    require(output_pairs == required_outputs, "declared output paths/roles drift")
    require(set(contract.get("role_definitions", {})) == EXPECTED_ROLE_KEYS, "output role definitions drift")
    asset = contract.get("asset_policy", {})
    require(asset.get("legacy_materialization") == "INDEPENDENT_BYTE_IDENTICAL_COPY", "legacy asset copy policy drift")
    require(asset.get("hardlinks_allowed") is False and asset.get("symlinks_allowed") is False, "fragile asset links enabled")
    require(asset.get("deduplicate_by_hash_allowed") is False, "hash deduplication enabled")
    require(asset.get("preserve_distinct_asset_ids") is True, "distinct asset identities may collapse")
    require(asset.get("witness_binary_insertions_require_inverse") is True, "binary insertion inverse disabled")
    require(
        asset.get("witness_binary_insertions_require_redistribution_permission") is True,
        "binary insertion licensing gate disabled",
    )
    evidence = contract.get("evidence_policy", {})
    require(set(evidence.get("not_applicable_reasons", [])) == EXPECTED_NOT_APPLICABLE, "NOT_APPLICABLE enum drift")
    require(evidence.get("not_applicable_for_authorial_or_illegible_content") is False, "NOT_APPLICABLE can hide authorial content")
    require(evidence.get("literal_source_errors_remain_canonical") is True, "source errors may be silently corrected")
    repair = contract.get("repair_policy", {})
    require(set(repair.get("classes", [])) == EXPECTED_REPAIR_CLASSES, "repair class enum drift")
    require(set(repair.get("workflow_states", [])) == EXPECTED_WORKFLOW_STATES, "workflow state enum drift")
    require(set(repair.get("final_dispositions", [])) == EXPECTED_DISPOSITIONS, "disposition enum drift")
    require(set(repair.get("high_risk_classes", [])) == EXPECTED_HIGH_RISK, "high-risk class enum drift")
    require(
        set(repair.get("mandatory_high_risk_operations", []))
        == {"WITNESS_ONLY_AUTHOR_TEXT_INSERTION", "AUTHORIAL_STRUCTURE_OR_HIERARCHY_CHANGE"},
        "mandatory high-risk operation tags drift",
    )
    require(repair.get("risk_is_union_of_class_and_operation_tags") is True, "operation-based risk tags disabled")
    require(repair.get("mechanically_proven_author_text_token_changes_allowed") is False, "mechanical author-text edits enabled")
    require(repair.get("all_author_text_changes_per_occurrence") is True, "author-text occurrence records disabled")
    review = contract.get("review_policy", {})
    for flag in (
        "every_author_text_change_independent_source_review",
        "creator_and_reviewer_must_differ",
        "high_risk_blind_preproposal_decision",
        "high_risk_specialist_review",
        "evidence_view_hash_required",
    ):
        require(review.get(flag) is True, f"review gate disabled: {flag}")
    require(review.get("unresolved_disagreement_may_close") is False, "unresolved review disagreement may close")
    require(review.get("blanket_document_review_allowed") is False, "blanket review enabled")
    require(
        contract.get("quality_policy")
        == {
            "path": "goal-4/quality-evaluation.json",
            "status_required_for_stage_1": "PROTOCOL_FROZEN_SAMPLE_IDS_PENDING_STAGE_2",
            "minimum_fraction_per_document": "1/20",
            "minimum_blocks_per_document": 20,
            "exact_authorial_metrics_required": True,
            "post_hoc_reranking_allowed": False,
        },
        "quality policy binding drift",
    )
    validate_quality(quality)
    require(licensing.get("contract_id") == "ANKOS-LICENSE-1", "licensing contract ID drift")
    license_rows = {row.get("artifact_class"): row for row in licensing.get("current_records", [])}
    require(license_rows.get("COMPLETE_PRIMARY_WITNESS", {}).get("state") == "NOT_ACQUIRED", "Stage 1 witness state is inaccurate")
    require(
        license_rows.get("EXTERNAL_REPAIRED_EDITION_REDISTRIBUTION", {}).get("state") == "USE_NOT_AUTHORIZED",
        "external redistribution became implicitly authorized",
    )
    require(len(license_rows) == len(licensing.get("current_records", [])), "duplicate licensing artifact class")
    require(
        contract.get("licensing", {}).get("credentials_or_secrets_may_be_recorded") is False,
        "licensing contract permits secrets",
    )
    modes = contract.get("modes", {})
    require(
        modes
        == {
            "BUILD": {
                "network_allowed": False,
                "witness_mount_required": False,
                "governed_unresolved_records_allowed": True,
                "certification": "UNCERTIFIED_WHEN_AUTHORIAL_BLOCKERS_EXIST",
            },
            "AUDIT": {
                "network_allowed": False,
                "authorized_read_only_witness_required": True,
                "witness_hashes_rechecked": True,
                "authorial_blockers_allowed_for_full_certification": False,
            },
        },
        "build/audit mode contract drift",
    )
    publication = contract.get("publication", {})
    require(publication.get("contract_id") == "ANKOS-PROMOTION-1", "publication contract ID drift")
    require(
        publication.get("target_must_be")
        == [
            "ABSENT",
            "EMPTY",
            "EXACTLY_OWNED_BY_TRUSTED_EXTERNAL_PRIOR_RELEASE_MANIFEST",
        ],
        "publication target-state policy drift",
    )
    require(publication.get("target_local_manifest_alone_is_trusted") is False, "target-local manifest trusted")
    require(publication.get("unowned_paths_allowed") is False, "unowned release paths allowed")
    require(publication.get("symlinks_allowed") is False, "release symlinks allowed")
    require(publication.get("legacy_promotion_authorized") is False, "legacy promotion implicitly authorized")
    require(publication.get("consumer_migration_authorized") is False, "consumer migration implicitly authorized")
    require(publication.get("external_redistribution_authorized") is False, "external redistribution implicitly authorized")
    for flag in (
        "atomic_same_filesystem_rename_required",
        "content_addressed_release_id_required",
        "last_known_good_preserved",
        "rollback_verified",
    ):
        require(publication.get(flag) is True, f"publication safety gate disabled: {flag}")
    required_blockers = {
        "RAW_ALLOWLIST_HASH_DRIFT",
        "WITNESS_IDENTITY_OR_REGION_GAP",
        "ILLEGIBLE_OR_UNTRANSCRIBED_AUTHORIAL_REGION",
        "UNRESOLVED_SOURCE_NEEDED_AUTHORIAL_ITEM",
        "UNRESOLVED_REVIEW_DISAGREEMENT",
        "MISSING_REQUIRED_INDEPENDENT_OR_SPECIALIST_REVIEW",
        "RAW_WITNESS_CANONICAL_PROVENANCE_GAP_OR_OVERLAP",
        "UNLOGGED_AUTHOR_TEXT_CHANGE_OR_INSERTION",
        "MISSING_OR_UNLICENSED_AUTHORIAL_VISUAL_COMPONENT",
        "NONDETERMINISTIC_OR_NONINVERTIBLE_BUILD",
        "OUTPUT_ROLE_LEAKAGE",
        "BROKEN_NAVIGATION_OR_GOVERNED_ASSET",
        "COMPATIBILITY_BEHAVIOR_DRIFT",
        "NONEMPTY_UNOWNED_PUBLICATION_TARGET",
        "LEGACY_OR_UNRELATED_WORKTREE_MODIFICATION",
    }
    require(set(contract.get("release_blockers", [])) == required_blockers, "release blocker enum drift")
    serialization = contract.get("serialization", {})
    require(serialization.get("profile_id") == "ANKOS-MD-1", "Markdown profile drift")
    require(serialization.get("ast_profile_id") == "ANKOS-AST-1", "AST profile drift")
    require(serialization.get("canonical_json_profile_id") == "ANKOS-CJ-1", "generated JSON profile drift")
    require(serialization.get("contract_json_profile_id") == "ANKOS-PJ-1", "contract JSON profile drift")
    require(serialization.get("encoding") == "UTF-8" and serialization.get("bom") is False, "encoding profile drift")
    require(serialization.get("line_ending") == "LF" and serialization.get("terminal_lf") == 1, "line ending profile drift")
    require(serialization.get("unicode_normalization") == "NONE", "Unicode normalization enabled")
    require(serialization.get("canonical_yaml_front_matter") is False, "canonical YAML front matter enabled")
    require(serialization.get("generated_namespace") == "ankos-", "generated namespace drift")
    require(serialization.get("generated_output_as_input") is False, "serialized output can become input")
    require(serialization.get("fixture_validation_owner_stage") == 7, "style fixture owner drift")
    require(
        serialization.get("identifier_grammar")
        == {
            "canonical_document_id_regex": "^[A-Z0-9_]+$",
            "canonical_anchor_slug_regex": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
            "raw_block_id_regex": "^[A-Z0-9][A-Z0-9_-]*$",
            "repair_id_regex": "^[A-Z0-9][A-Z0-9_-]*$",
            "generated_anchor_regex": "^ankos-[a-z0-9]+(?:-[a-z0-9]+)*$",
        },
        "identifier grammar drift",
    )
    compatibility = contract.get("compatibility", {})
    require(
        isinstance(compatibility.get("baseline_sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", compatibility["baseline_sha256"]),
        "compatibility baseline hash binding is missing",
    )
    all_oracle_paths = _frozen_path_list(compatibility.get("all_oracle_paths"), "all oracle paths")
    affected_paths = _frozen_path_list(compatibility.get("recursive_affected_paths"), "affected oracle paths")
    image_paths = _frozen_path_list(
        compatibility.get("recursive_image_or_basename_paths"), "image oracle paths"
    )
    _frozen_path_list(compatibility.get("additional_dependency_paths"), "additional dependency paths")
    require(len(all_oracle_paths) == compatibility.get("goal_1_root_oracle_count"), "Goal 1 oracle count drift")
    require(len(affected_paths) == compatibility.get("goal_1_recursive_affected_count"), "affected oracle count drift")
    require(
        compatibility.get("goal_1_recursive_markdown_count") == len(affected_paths),
        "recursive Markdown count drift",
    )
    require(len(image_paths) == compatibility.get("goal_1_recursive_image_or_basename_count"), "image oracle count drift")
    require(set(image_paths) <= set(affected_paths) <= set(all_oracle_paths), "oracle scope subset drift")
    require(compatibility.get("goal_1_direct_legacy_semantic_count") == 2, "direct semantic count drift")
    require(compatibility.get("goal_1_no_legacy_path_count") == 17, "no-path semantic count drift")
    require(
        filename_set_digest(path.removeprefix("goal-1/") for path in all_oracle_paths)
        == compatibility.get("all_oracle_filename_digest"),
        "all-oracle filename digest drift",
    )
    require(
        filename_set_digest(path.removeprefix("goal-1/") for path in affected_paths)
        == compatibility.get("recursive_affected_filename_digest"),
        "affected-oracle filename digest drift",
    )
    require(compatibility.get("capture_all_oracle_classifications") is True, "all-oracle capture disabled")
    require(compatibility.get("capture_recursive_affected_behaviors") is True, "affected behavior capture disabled")
    require(compatibility.get("book_override_allowed") is False, "unsafe BOOK override enabled")
    require(compatibility.get("repeat_runs_required") == 2, "oracle repeat count weakened")
    require(compatibility.get("empty_sibling_exact_match_required") is True, "empty sibling probe disabled")
    require(compatibility.get("empty_sibling_runs_required") == 1, "empty sibling run count drift")
    require(compatibility.get("after_removal_runs_required") == 1, "post-removal run count drift")
    require(compatibility.get("initial_sibling_absence_required") is True, "initial sibling absence disabled")
    require(compatibility.get("final_sibling_absence_required") is True, "final sibling absence disabled")
    require(compatibility.get("expected_behavior_count") == len(affected_paths), "compatibility behavior scope drift")
    require(
        compatibility.get("environment")
        == {
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
        },
        "compatibility environment contract drift",
    )
    require(compatibility.get("argv_template") == ["/usr/bin/python3", "-B", "goal-1/<oracle>"], "argv template drift")
    contract_rows = contract.get("contracts", [])
    require(isinstance(contract_rows, list) and len(contract_rows) == len(EXPECTED_CONTRACT_PATHS), "contract hash registry count drift")
    require(
        {row.get("path") for row in contract_rows} == EXPECTED_CONTRACT_PATHS
        and len({row.get("path") for row in contract_rows}) == len(contract_rows),
        "contract hash registry paths drift",
    )
    require(
        all(isinstance(row.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in contract_rows),
        "contract hash registry contains an invalid hash",
    )
    require(
        sha256_bytes(canonical_json_bytes(contract)) == EXPECTED_GUARDRAILS_CANONICAL_SHA256,
        "whole guardrail contract digest drift",
    )
    if check_files:
        require(
            (repo_root / "goal-4/guardrails.json").read_bytes() == pretty_contract_json_bytes(contract),
            "guardrails.json is not ANKOS-PJ-1",
        )
        require(
            (repo_root / "goal-4/quality-evaluation.json").read_bytes()
            == pretty_contract_json_bytes(quality),
            "quality-evaluation.json is not ANKOS-PJ-1",
        )
        require(
            (repo_root / "goal-4/licensing-contract.json").read_bytes()
            == pretty_contract_json_bytes(licensing),
            "licensing-contract.json is not ANKOS-PJ-1",
        )
        for row in contract_rows:
            path = repo_root / str(safe_relative_posix(row.get("path", "")))
            require(path.is_file(), f"contract file missing: {path}")
            require(sha256_file(path) == row.get("sha256"), f"frozen contract hash drift: {path}")
        validate_publication_target(repaired, legacy, None)
    if baseline is not None:
        validate_compatibility_baseline(
            baseline,
            contract,
            repo_root,
            check_current_scripts=check_current_scripts,
        )
