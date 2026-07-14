#!/usr/bin/env python3
"""Independent Stage 1 contract and publication-path checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
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


def _file_mode(path: Path) -> str:
    return format(stat.S_IMODE(path.stat(follow_symlinks=False).st_mode), "04o")


def validate_publication_target(
    target: Path,
    legacy: Path,
    trusted_manifest: dict[str, Any] | None = None,
) -> str:
    legacy = legacy.resolve(strict=True)
    target_parent = target.parent.resolve(strict=True)
    target_lexical = target_parent / target.name
    require(target_lexical != legacy, "publication target equals legacy root")
    require(not is_component_descendant(target_lexical, legacy), "publication target is beneath legacy root")
    require(target_parent == legacy.parent, "publication target is not the required sibling")
    require(not target.is_symlink(), "publication target may not be a symlink")
    if not target.exists():
        return "ABSENT"
    require(target.is_dir(), "publication target must be a directory")
    entries = sorted(target.iterdir(), key=lambda item: item.name)
    if not entries:
        return "EMPTY"
    require(trusted_manifest is not None, "nonempty publication target lacks a trusted external manifest")
    rows = trusted_manifest.get("files")
    require(isinstance(rows, list), "trusted manifest files must be an array")
    expected: dict[str, dict[str, Any]] = {}
    for row in rows:
        require(isinstance(row, dict), "trusted manifest file row must be an object")
        relative = str(safe_relative_posix(row.get("path", "")))
        require(relative not in expected, f"duplicate trusted manifest path: {relative}")
        expected[relative] = row
    observed: dict[str, Path] = {}
    for path in sorted(target.rglob("*"), key=lambda item: item.as_posix()):
        require(not path.is_symlink(), f"symlink in publication target: {path}")
        if path.is_file():
            relative = path.relative_to(target).as_posix()
            observed[relative] = path
        else:
            require(path.is_dir(), f"unsupported target entry: {path}")
    require(set(observed) == set(expected), "publication target has missing or unowned files")
    for relative, path in observed.items():
        row = expected[relative]
        require(row.get("sha256") == sha256_file(path), f"owned target hash drift: {relative}")
        require(row.get("byte_size") == path.stat().st_size, f"owned target size drift: {relative}")
        require(row.get("mode") == _file_mode(path), f"owned target mode drift: {relative}")
    return "MANIFEST_OWNED"


def framed_behavior_digest(exit_code: int, stdout: bytes, stderr: bytes) -> str:
    frame = bytearray(b"ANKOS-ORACLE-BEHAVIOR-v1\0")
    frame.extend(str(exit_code).encode("ascii"))
    frame.extend(b"\0")
    for stream in (stdout, stderr):
        frame.extend(len(stream).to_bytes(8, "big"))
        frame.extend(stream)
    return sha256_bytes(bytes(frame))


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
    "FORMULA_OR_SYMBOL",
    "WOLFRAM_CODE",
    "RULE_TABLE_OR_DATA",
    "FIGURE_OR_CAPTION",
    "INDEX_ENTRY",
}


def validate_quality(quality: dict[str, Any]) -> None:
    require(quality.get("protocol_version") == "1.0.0", "unexpected quality protocol version")
    require(
        quality.get("status") == "PROTOCOL_FROZEN_SAMPLE_IDS_PENDING_STAGE_2",
        "quality protocol is not frozen at the Stage 1 state",
    )
    require(quality.get("frozen_before_author_text_repairs") is True, "quality protocol was not pre-frozen")
    require(quality.get("materialized_sample") is None, "Stage 1 must not materialize outcome-aware samples")
    require(quality.get("results") is None, "Stage 1 quality results must be empty")
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
    require("Hamilton" in sample.get("risk_allocation", ""), "quality risk allocation is underspecified")
    require("odd slot goes to CHANGED" in sample.get("changed_unchanged_rule", ""), "changed/unchanged tie is underspecified")
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


def validate_compatibility_baseline(
    baseline: dict[str, Any],
    contract: dict[str, Any],
    repo_root: Path,
    *,
    check_current_scripts: bool,
) -> None:
    require(baseline.get("schema_version") == "1.0.0", "unsupported compatibility baseline schema")
    compatibility = contract["compatibility"]
    classifications = baseline.get("classifications", [])
    require(len(classifications) == compatibility["goal_1_root_oracle_count"], "oracle classification count mismatch")
    names = [row.get("path", "").removeprefix("goal-1/") for row in classifications]
    require(len(names) == len(set(names)), "duplicate oracle classification")
    require(filename_set_digest(names) == compatibility["all_oracle_filename_digest"], "all-oracle name digest mismatch")
    affected = [row for row in classifications if row.get("recursive_affected") is True]
    require(len(affected) == compatibility["goal_1_recursive_affected_count"], "affected oracle count mismatch")
    affected_names = [row["path"].removeprefix("goal-1/") for row in affected]
    require(
        filename_set_digest(affected_names) == compatibility["recursive_affected_filename_digest"],
        "affected oracle name digest mismatch",
    )
    require(sum(row.get("recursive_markdown") is True for row in classifications) == 39, "recursive Markdown census mismatch")
    require(sum(row.get("recursive_image_or_basename") is True for row in classifications) == 26, "recursive image census mismatch")
    records = baseline.get("oracles", [])
    require(len(records) == 39, "compatibility behavior must cover all 39 recursive affected oracles")
    require(
        {row.get("path") for row in records} == {row.get("path") for row in affected},
        "behavior/affected-classification join mismatch",
    )
    context = baseline.get("closure", {})
    for row in records:
        require(row.get("repeat_count") == 2, f"oracle was not repeated twice: {row.get('path')}")
        require(row.get("repeat_identical") is True, f"oracle repeat drift: {row.get('path')}")
        stdout = row.get("stdout", {})
        stderr = row.get("stderr", {})
        require(isinstance(stdout.get("base64"), str) and isinstance(stderr.get("base64"), str), "raw output bytes not captured")
        require(
            row.get("transitive_dependency_fingerprint") == context.get("dependency_fingerprint_before"),
            f"oracle dependency fingerprint missing/drifted: {row.get('path')}",
        )
        if check_current_scripts:
            script = repo_root / row["path"]
            require(script.is_file(), f"oracle script missing: {row['path']}")
            require(sha256_file(script) == row.get("script_sha256"), f"oracle script drift: {row['path']}")
    require(context.get("git_head_before") == context.get("git_head_after"), "git HEAD moved during capture")
    require(context.get("dependency_fingerprint_before") == context.get("dependency_fingerprint_after"), "dependency closure moved during capture")
    require(context.get("legacy_tree_digest_before") == context.get("legacy_tree_digest_after"), "legacy tree moved during capture")
    require(
        context.get("legacy_content_fingerprint_before") == context.get("legacy_content_fingerprint_after"),
        "legacy content bytes moved during capture",
    )
    probe = baseline.get("empty_sibling_probe", {})
    require(probe.get("target_state") == "EMPTY", "empty sibling probe did not use an empty target")
    require(probe.get("all_behavior_identical") is True, "empty sibling changed oracle behavior")
    require(probe.get("baseline_behavior_digest") == probe.get("empty_sibling_behavior_digest"), "empty sibling aggregate mismatch")
    require(baseline.get("goal_3", {}).get("executable_validator_count") == 0, "Stage 1 Goal 3 executable census drift")


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
    architecture = contract.get("architecture", {})
    legacy, repaired = validate_root_relationship(
        repo_root,
        architecture.get("legacy_root", ""),
        architecture.get("repaired_root", ""),
    )
    require(legacy.is_dir(), "legacy root is missing")
    require(architecture.get("allowed_write_roots") == ["goal-4", "ref/A-New-Kind-of-Science-Repaired"], "write scope drift")
    require("ref/A-New-Kind-of-Science" in architecture.get("forbidden_write_roots", []), "legacy root is not write-protected")
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
    raw = contract.get("legacy_input", {})
    require(raw.get("discovery") == "EXPLICIT_MANIFEST_ROWS_ONLY", "raw input is not explicit-manifest-only")
    require(raw.get("recursive_build_input_discovery_allowed") is False, "recursive raw build discovery enabled")
    require(raw.get("generated_output_may_be_build_input") is False, "generated output allowed as input")
    require(raw.get("expected_counts") == {"markdown": 19, "jpeg": 1444, "all_regular_files": 1463}, "raw expected counts drift")
    documents = contract.get("canonical_documents", [])
    require(len(documents) == 29, "canonical document count must be 29")
    require([row.get("order") for row in documents] == list(range(29)), "canonical order is not contiguous")
    ids = [row.get("id") for row in documents]
    doc_paths = [row.get("path") for row in documents]
    require(len(set(ids)) == 29 and len(set(doc_paths)) == 29, "canonical IDs/paths must be unique")
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
    asset = contract.get("asset_policy", {})
    require(asset.get("legacy_materialization") == "INDEPENDENT_BYTE_IDENTICAL_COPY", "legacy asset copy policy drift")
    require(asset.get("hardlinks_allowed") is False and asset.get("symlinks_allowed") is False, "fragile asset links enabled")
    require(asset.get("deduplicate_by_hash_allowed") is False, "hash deduplication enabled")
    evidence = contract.get("evidence_policy", {})
    require(set(evidence.get("not_applicable_reasons", [])) == EXPECTED_NOT_APPLICABLE, "NOT_APPLICABLE enum drift")
    require(evidence.get("not_applicable_for_authorial_or_illegible_content") is False, "NOT_APPLICABLE can hide authorial content")
    require(evidence.get("literal_source_errors_remain_canonical") is True, "source errors may be silently corrected")
    repair = contract.get("repair_policy", {})
    require(set(repair.get("classes", [])) == EXPECTED_REPAIR_CLASSES, "repair class enum drift")
    require(set(repair.get("workflow_states", [])) == EXPECTED_WORKFLOW_STATES, "workflow state enum drift")
    require(set(repair.get("final_dispositions", [])) == EXPECTED_DISPOSITIONS, "disposition enum drift")
    require(set(repair.get("high_risk_classes", [])) == EXPECTED_HIGH_RISK, "high-risk class enum drift")
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
    validate_quality(quality)
    require(licensing.get("contract_id") == "ANKOS-LICENSE-1", "licensing contract ID drift")
    license_rows = {row.get("artifact_class"): row for row in licensing.get("current_records", [])}
    require(license_rows.get("COMPLETE_PRIMARY_WITNESS", {}).get("state") == "NOT_ACQUIRED", "Stage 1 witness state is inaccurate")
    require(
        license_rows.get("EXTERNAL_REPAIRED_EDITION_REDISTRIBUTION", {}).get("state") == "USE_NOT_AUTHORIZED",
        "external redistribution became implicitly authorized",
    )
    publication = contract.get("publication", {})
    require(publication.get("target_local_manifest_alone_is_trusted") is False, "target-local manifest trusted")
    require(publication.get("unowned_paths_allowed") is False, "unowned release paths allowed")
    require(publication.get("symlinks_allowed") is False, "release symlinks allowed")
    require(publication.get("legacy_promotion_authorized") is False, "legacy promotion implicitly authorized")
    require(publication.get("consumer_migration_authorized") is False, "consumer migration implicitly authorized")
    require(publication.get("external_redistribution_authorized") is False, "external redistribution implicitly authorized")
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
    compatibility = contract.get("compatibility", {})
    require(compatibility.get("goal_1_root_oracle_count") == 58, "Goal 1 oracle count drift")
    require(compatibility.get("goal_1_recursive_affected_count") == 39, "affected oracle count drift")
    require(compatibility.get("goal_1_recursive_image_or_basename_count") == 26, "image oracle count drift")
    require(compatibility.get("book_override_allowed") is False, "unsafe BOOK override enabled")
    require(compatibility.get("repeat_runs_required") == 2, "oracle repeat count weakened")
    require(compatibility.get("empty_sibling_exact_match_required") is True, "empty sibling probe disabled")
    require(compatibility.get("empty_sibling_runs_required") == 1, "empty sibling run count drift")
    require(compatibility.get("expected_behavior_count") == 39, "compatibility behavior scope drift")
    if check_files:
        for row in contract.get("contracts", []):
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
