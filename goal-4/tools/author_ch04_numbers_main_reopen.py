#!/usr/bin/env python3
"""Author the governed Stage 8 Chapter 4 main-text epoch-2 reopen.

This helper is deliberately narrower than the original Stage 8 review
author.  It consumes a sealed reopened bundle for exactly
``CHAPTERS/04-Systems-Based-on-Numbers.md``, retains every existing global
candidate and route link, emits no new proposals, and changes only the review
identity plus eleven explicitly enumerated asset classifications.

The helper expects a pristine *prepared* worksheet (the nonsemantic scaffold
created by ``prepare_review_output.py --prepare``).  It writes the completed
rows atomically with ``prohibited_input_nonuse`` still false so that the
standard, separate declaration-finalization step remains explicit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

TOOLS = Path("/home/jake/Developer/ankos/goal-4/tools")
sys.path.insert(0, str(TOOLS))

import build_worker_bundle  # noqa: E402
import prepare_review_output  # noqa: E402
from audit_contract import (  # noqa: E402
    ASSET_HEADER,
    READING_HEADER,
    canonical_json_bytes,
)


EXPECTED_WORKER = "ch04-numbers-reopen-e2"
EXPECTED_PATHS = ["CHAPTERS/04-Systems-Based-on-Numbers.md"]
EXPECTED_PATH = EXPECTED_PATHS[0]
STAGE = 8
EPOCH = 2
EXPECTED_READING_COUNT = 306
EXPECTED_ASSET_COUNT = 63

# Canonical JSON hashes of the complete authoritative path projection that
# this correction reopens.  LOCAL search and route resolution do not mutate
# these rows, so a different hash is a stale or otherwise unexpected input.
EXPECTED_READING_INPUT_SHA256 = (
    "d431bed6608678e6c0544b43d9070e0998e1e9729c57538715890c3028e2961c"
)
EXPECTED_ASSET_INPUT_SHA256 = (
    "3a50214de7e45576f6af39860cc8dd3450620b33e1641bd5e62752185ea74b39"
)

# These hashes cover the deterministic row projections produced below.  They
# are filled from the reviewed specification, not from bundle output.
EXPECTED_REOPEN_READING_SHA256 = (
    "7fd995a9194f583d6c5af504bd3bda1b9106d6391556aac09bf83af0f6e6a456"
)
EXPECTED_REOPEN_ASSET_SHA256 = (
    "06f08c9e05b69cf968b4ad5037482ccbd33a74429e12e7fb6c69245c3a79bc10"
)

GLOBAL_CANDIDATE_RE = re.compile(r"B[0-9]{4}")
GLOBAL_ROUTE_RE = re.compile(r"R[0-9]{6}")
REVIEW_IDENTITY_FIELDS = {"review_epoch", "review_stage", "reviewer"}
ASSET_CORRECTION_FIELDS = {
    "visual_role",
    "risk_flags",
    "transcription_status",
    "evidence_statement",
}
TARGET_RISKS = ["CONSTRUCTION_BEARING", "TEXT_BEARING"]


class AuthoringError(ValueError):
    """The bundle or worksheet is not safe for this exact reopen."""


def compact(values: list[str]) -> str:
    return json.dumps(values, separators=(",", ":"))


def projection_sha256(rows: list[dict[str, str]]) -> str:
    return hashlib.sha256(canonical_json_bytes(rows)).hexdigest()


TARGET_ASSET_STATEMENTS = {
    "A000797": (
        "Original-resolution transcription check confirms the embedded "
        "recurrence formulas and their displayed detrending labels; the "
        "formula/label pairings are native construction-bearing identity "
        "evidence for the linked recurrence-sequence constructions."
    ),
    "A000799": (
        "Original-resolution transcription check confirms the embedded "
        "Prime[n], PrimePi[n], LogIntegral[n] comparison, residue-class "
        "excess, and successive-prime-gap labels; those labels natively "
        "identify the six linked number-theoretic constructions."
    ),
    "A000800": (
        "Original-resolution transcription check confirms the embedded label "
        "\"the number of divisors of n (including n)\"; the checked label "
        "natively identifies the linked divisor-count construction."
    ),
    "A000801": (
        "Original-resolution transcription check confirms the embedded label "
        "\"the sum of the divisors of n (excluding n) minus n\"; the checked "
        "label natively identifies the linked proper-divisor-sum difference "
        "construction."
    ),
    "A000802": (
        "Original-resolution transcription check confirms the embedded label "
        "\"the number of ways of expressing n as a sum of three squares\"; "
        "the checked label natively identifies the linked representation-count "
        "construction."
    ),
    "A000810": (
        "Original-resolution transcription check confirms all four embedded "
        "sine-sum formulas and their paired plots; the checked formulas "
        "natively identify the linked two- and three-frequency constructions."
    ),
    "A000811": (
        "Original-resolution transcription check confirms the four embedded "
        "cosine-difference formulas together with their axis-crossing and "
        "substitution encodings; the checked formulas and labels natively "
        "identify the linked constructions."
    ),
    "A000817": (
        "Original-resolution transcription check confirms the embedded "
        "initial-condition seed 0.785398163397448310 and its paired evolution; "
        "the checked seed label is native construction-bearing evidence for "
        "the linked nearby-seed construction."
    ),
    "A000818": (
        "Original-resolution transcription check confirms the embedded "
        "initial-condition seed 0.785398163397448311 and its paired evolution; "
        "the checked seed label is native construction-bearing evidence for "
        "the linked nearby-seed construction."
    ),
    "A000826": (
        "Original-resolution transcription check confirms the embedded "
        "additive-constant preset labels from c=0 through c=0.5 in 0.025 "
        "increments and their paired evolutions; the checked preset identities "
        "are native construction-bearing evidence for the linked continuous-CA "
        "family members."
    ),
    "A000827": (
        "Original-resolution transcription check confirms the embedded preset "
        "labels c=0.1, 0.3, 0.325, 0.3299, 0.35, 0.475, 0.495, and 0.9, plus "
        "the c=0.3299 differences label; the checked preset identities are "
        "native construction-bearing evidence for the linked continuous-CA "
        "constructions."
    ),
}
TARGET_ASSET_IDS = set(TARGET_ASSET_STATEMENTS)

# The exact current values are part of the correction specification.  This
# catches an input that has already been partly edited or was projected from a
# different ledger state even before the full projection hashes are checked.
EXPECTED_TARGET_PRESTATE = {
    "A000797": ("OBSERVER", ["TEXT_BEARING"], "CHECKED"),
    "A000799": ("OBSERVER", ["TEXT_BEARING"], "CHECKED"),
    "A000800": ("OBSERVER", [], "NOT_REQUIRED"),
    "A000801": ("OBSERVER", [], "NOT_REQUIRED"),
    "A000802": ("OBSERVER", [], "NOT_REQUIRED"),
    "A000810": (
        "CONTROL",
        ["CONSTRUCTION_BEARING", "TEXT_BEARING"],
        "CHECKED",
    ),
    "A000811": (
        "RELATION",
        ["CONSTRUCTION_BEARING", "TEXT_BEARING"],
        "CHECKED",
    ),
    "A000817": ("CONTROL", ["TEXT_BEARING"], "CHECKED"),
    "A000818": ("CONTROL", ["TEXT_BEARING"], "CHECKED"),
    "A000826": ("CONTROL", ["TEXT_BEARING"], "CHECKED"),
    "A000827": ("CONTROL", ["TEXT_BEARING"], "CHECKED"),
}

EXPECTED_UNCHANGED_SENTINELS = {
    "A000806": ("OBSERVER", ["TEXT_BEARING"], "CHECKED"),
    "A000821": ("CONTROL", [], "NOT_REQUIRED"),
}

EXPECTED_ROLE_COUNTS = {
    "NATIVE_EVIDENCE": 24,
    "RELATION": 0,
    "CONTROL": 6,
    "OBSERVER": 31,
    "DECORATIVE": 1,
    "SOURCE_DEFECT": 1,
}


def parse_links(
    value: str,
    pattern: re.Pattern[str],
    label: str,
) -> list[str]:
    try:
        links = json.loads(value)
    except json.JSONDecodeError as exc:
        raise AuthoringError(f"{label} is not a JSON array") from exc
    if (
        not isinstance(links, list)
        or not all(isinstance(item, str) for item in links)
        or len(links) != len(set(links))
        or any(pattern.fullmatch(item) is None for item in links)
    ):
        raise AuthoringError(
            f"{label} must contain unique existing global IDs only"
        )
    return links


def parse_risks(value: str, label: str) -> list[str]:
    try:
        risks = json.loads(value)
    except json.JSONDecodeError as exc:
        raise AuthoringError(f"{label} has invalid risk_flags") from exc
    if (
        not isinstance(risks, list)
        or not all(isinstance(item, str) for item in risks)
        or len(risks) != len(set(risks))
    ):
        raise AuthoringError(f"{label} has invalid risk_flags")
    return risks


def verify_input_projection(
    readings: list[dict[str, str]],
    assets: list[dict[str, str]],
) -> None:
    if len(readings) != EXPECTED_READING_COUNT:
        raise AuthoringError("reading projection count changed")
    if len(assets) != EXPECTED_ASSET_COUNT:
        raise AuthoringError("asset projection count changed")
    if any(row["path"] != EXPECTED_PATH for row in readings):
        raise AuthoringError("reading projection contains another source path")
    if any(row["assignment_path"] != EXPECTED_PATH for row in assets):
        raise AuthoringError("asset projection contains another assignment path")
    if len({row["source_unit_id"] for row in readings}) != len(readings):
        raise AuthoringError("reading projection contains duplicate unit IDs")
    if len({row["asset_id"] for row in assets}) != len(assets):
        raise AuthoringError("asset projection contains duplicate asset IDs")
    if projection_sha256(readings) != EXPECTED_READING_INPUT_SHA256:
        raise AuthoringError("reading projection is not the expected current state")
    if projection_sha256(assets) != EXPECTED_ASSET_INPUT_SHA256:
        raise AuthoringError("asset projection is not the expected current state")

    asset_by_id = {row["asset_id"]: row for row in assets}
    if not TARGET_ASSET_IDS <= set(asset_by_id):
        raise AuthoringError("correction assets do not exactly exist in assignment")
    for asset_id, expected in EXPECTED_TARGET_PRESTATE.items():
        row = asset_by_id[asset_id]
        observed = (
            row["visual_role"],
            parse_risks(row["risk_flags"], asset_id),
            row["transcription_status"],
        )
        if observed != expected:
            raise AuthoringError(f"{asset_id} pre-correction state changed")
    for asset_id, expected in EXPECTED_UNCHANGED_SENTINELS.items():
        row = asset_by_id[asset_id]
        observed = (
            row["visual_role"],
            parse_risks(row["risk_flags"], asset_id),
            row["transcription_status"],
        )
        if observed != expected:
            raise AuthoringError(f"{asset_id} unchanged sentinel state changed")

    for row in readings:
        if (
            row["review_status"] != "REVIEWED"
            or row["review_epoch"] != "1"
            or row["review_stage"] != str(STAGE)
        ):
            raise AuthoringError(
                f"{row['source_unit_id']} is not the reviewed epoch-1 projection"
            )
        parse_links(
            row["candidate_ids"],
            GLOBAL_CANDIDATE_RE,
            f"{row['source_unit_id']} candidate_ids",
        )
        parse_links(
            row["route_ids"],
            GLOBAL_ROUTE_RE,
            f"{row['source_unit_id']} route_ids",
        )
    for row in assets:
        if (
            row["inspection_status"] != "SCREENED"
            or row["review_epoch"] != "1"
            or row["review_stage"] != str(STAGE)
        ):
            raise AuthoringError(
                f"{row['asset_id']} is not the screened epoch-1 projection"
            )
        parse_links(
            row["candidate_ids"],
            GLOBAL_CANDIDATE_RE,
            f"{row['asset_id']} candidate_ids",
        )
        parse_links(
            row["route_ids"],
            GLOBAL_ROUTE_RE,
            f"{row['asset_id']} route_ids",
        )


def changed_fields(
    before: dict[str, str],
    after: dict[str, str],
) -> set[str]:
    return {
        field
        for field in before
        if before.get(field) != after.get(field)
    }


def build_reopened_rows(
    readings: list[dict[str, str]],
    assets: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    verify_input_projection(readings, assets)

    reading_updates: list[dict[str, str]] = []
    for original in readings:
        row = deepcopy(original)
        row.update(
            {
                "review_epoch": str(EPOCH),
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
            }
        )
        if changed_fields(original, row) - REVIEW_IDENTITY_FIELDS:
            raise AuthoringError(
                f"{row['source_unit_id']} changed beyond reopen identity"
            )
        if (
            row["candidate_ids"] != original["candidate_ids"]
            or row["route_ids"] != original["route_ids"]
        ):
            raise AuthoringError(
                f"{row['source_unit_id']} did not retain global links exactly"
            )
        reading_updates.append(row)

    asset_updates: list[dict[str, str]] = []
    for original in assets:
        row = deepcopy(original)
        row.update(
            {
                "review_epoch": str(EPOCH),
                "review_stage": str(STAGE),
                "reviewer": EXPECTED_WORKER,
            }
        )
        asset_id = row["asset_id"]
        if asset_id in TARGET_ASSET_IDS:
            row.update(
                {
                    "visual_role": "NATIVE_EVIDENCE",
                    "risk_flags": compact(TARGET_RISKS),
                    "transcription_status": "CHECKED",
                    "evidence_statement": TARGET_ASSET_STATEMENTS[asset_id],
                }
            )
            allowed_changes = REVIEW_IDENTITY_FIELDS | ASSET_CORRECTION_FIELDS
        else:
            allowed_changes = REVIEW_IDENTITY_FIELDS
        if changed_fields(original, row) - allowed_changes:
            raise AuthoringError(f"{asset_id} changed outside its correction scope")
        if (
            row["candidate_ids"] != original["candidate_ids"]
            or row["route_ids"] != original["route_ids"]
        ):
            raise AuthoringError(f"{asset_id} did not retain global links exactly")
        asset_updates.append(row)

    validate_reopened_rows(readings, assets, reading_updates, asset_updates)
    return reading_updates, asset_updates


def validate_reopened_rows(
    readings: list[dict[str, str]],
    assets: list[dict[str, str]],
    reading_updates: list[dict[str, str]],
    asset_updates: list[dict[str, str]],
) -> None:
    if [row["source_unit_id"] for row in reading_updates] != [
        row["source_unit_id"] for row in readings
    ]:
        raise AuthoringError("reopened reading rows changed assignment order")
    if [row["asset_id"] for row in asset_updates] != [
        row["asset_id"] for row in assets
    ]:
        raise AuthoringError("reopened asset rows changed assignment order")
    if any(set(row) != set(READING_HEADER) for row in reading_updates):
        raise AuthoringError("reopened reading row fields changed")
    if any(set(row) != set(ASSET_HEADER) for row in asset_updates):
        raise AuthoringError("reopened asset row fields changed")

    for original, row in zip(readings, reading_updates):
        if row["review_epoch"] != str(EPOCH):
            raise AuthoringError("reopened reading has wrong epoch")
        if row["review_stage"] != str(STAGE):
            raise AuthoringError("reopened reading has wrong stage")
        if row["reviewer"] != EXPECTED_WORKER:
            raise AuthoringError("reopened reading has wrong reviewer")
        if row["candidate_ids"] != original["candidate_ids"]:
            raise AuthoringError("reopened reading candidate links changed")
        if row["route_ids"] != original["route_ids"]:
            raise AuthoringError("reopened reading route links changed")

    original_assets = {row["asset_id"]: row for row in assets}
    updated_assets = {row["asset_id"]: row for row in asset_updates}
    for asset_id, row in updated_assets.items():
        original = original_assets[asset_id]
        if row["review_epoch"] != str(EPOCH):
            raise AuthoringError(f"{asset_id} has wrong reopen epoch")
        if row["review_stage"] != str(STAGE):
            raise AuthoringError(f"{asset_id} has wrong reopen stage")
        if row["reviewer"] != EXPECTED_WORKER:
            raise AuthoringError(f"{asset_id} has wrong reopen reviewer")
        if row["candidate_ids"] != original["candidate_ids"]:
            raise AuthoringError(f"{asset_id} candidate links changed")
        if row["route_ids"] != original["route_ids"]:
            raise AuthoringError(f"{asset_id} route links changed")
        risks = parse_risks(row["risk_flags"], asset_id)
        if asset_id in TARGET_ASSET_IDS:
            if (
                row["visual_role"] != "NATIVE_EVIDENCE"
                or risks != TARGET_RISKS
                or row["transcription_status"] != "CHECKED"
                or row["evidence_statement"]
                != TARGET_ASSET_STATEMENTS[asset_id]
            ):
                raise AuthoringError(f"{asset_id} correction is incomplete")
        elif changed_fields(original, row) - REVIEW_IDENTITY_FIELDS:
            raise AuthoringError(f"{asset_id} semantics changed unexpectedly")
        if row["visual_role"] == "NATIVE_EVIDENCE":
            if (
                "CONSTRUCTION_BEARING" not in risks
                or row["transcription_status"] != "CHECKED"
            ):
                raise AuthoringError(
                    f"{asset_id} native evidence lacks checked construction metadata"
                )
        if (
            "TEXT_BEARING" in risks
            and row["transcription_status"] != "CHECKED"
        ):
            raise AuthoringError(f"{asset_id} text-bearing evidence is not checked")

    for asset_id, expected in EXPECTED_UNCHANGED_SENTINELS.items():
        original = original_assets[asset_id]
        row = updated_assets[asset_id]
        observed = (
            row["visual_role"],
            parse_risks(row["risk_flags"], asset_id),
            row["transcription_status"],
        )
        if observed != expected:
            raise AuthoringError(f"{asset_id} sentinel semantics changed")
        if changed_fields(original, row) != REVIEW_IDENTITY_FIELDS - {
            field
            for field in REVIEW_IDENTITY_FIELDS
            if original[field] == row[field]
        }:
            raise AuthoringError(f"{asset_id} changed beyond review identity")

    observed_roles = Counter(row["visual_role"] for row in asset_updates)
    normalized_roles = {
        role: observed_roles.get(role, 0) for role in EXPECTED_ROLE_COUNTS
    }
    unexpected_roles = set(observed_roles) - set(EXPECTED_ROLE_COUNTS)
    if normalized_roles != EXPECTED_ROLE_COUNTS or unexpected_roles:
        raise AuthoringError(
            "reopened asset role totals changed: "
            f"{dict(sorted(normalized_roles.items()))}"
        )


def verify_manifest(manifest: dict[str, Any]) -> None:
    expected = {
        "worker_id": EXPECTED_WORKER,
        "stage": STAGE,
        "discovery_epoch": EPOCH,
        "source_paths": EXPECTED_PATHS,
        "source_unit_count": EXPECTED_READING_COUNT,
        "asset_count": EXPECTED_ASSET_COUNT,
    }
    changed = {
        field: (manifest.get(field), value)
        for field, value in expected.items()
        if manifest.get(field) != value
    }
    if changed:
        raise AuthoringError(
            "bundle is not the exact Stage 8 epoch-2 main-text assignment: "
            f"{changed}"
        )
    content_set = manifest.get("content_set_sha256")
    if (
        not isinstance(content_set, str)
        or re.fullmatch(r"[0-9a-f]{64}", content_set) is None
    ):
        raise AuthoringError("bundle lacks a valid sealed content-set digest")


def validate_proposed_output(
    bundle: Path,
    manifest: dict[str, Any],
    template: dict[str, Any],
    readings: list[dict[str, str]],
    assets: list[dict[str, str]],
    proposed: dict[str, Any],
) -> None:
    errors = prepare_review_output.validate_top_level_identity(
        proposed,
        template,
    )
    errors.extend(
        prepare_review_output.validate_row_identity(
            proposed["reading_updates"],
            readings,
            header=READING_HEADER,
            immutable_fields=prepare_review_output.READING_IMMUTABLE_FIELDS,
            id_field="source_unit_id",
            label="reading",
        )
    )
    errors.extend(
        prepare_review_output.validate_row_identity(
            proposed["asset_updates"],
            assets,
            header=ASSET_HEADER,
            immutable_fields=prepare_review_output.ASSET_IMMUTABLE_FIELDS,
            id_field="asset_id",
            label="asset",
        )
    )
    if errors:
        raise AuthoringError(
            "proposed output identity validation failed:\n- "
            + "\n- ".join(errors)
        )
    incomplete = prepare_review_output.incomplete_human_fields(
        proposed,
        manifest,
    )
    if incomplete:
        raise AuthoringError(
            "proposed output has incomplete review fields:\n- "
            + "\n- ".join(incomplete)
        )

    validation_value = deepcopy(proposed)
    validation_value["prohibited_input_nonuse"] = True
    verifier_errors = build_worker_bundle.verify_bundle(
        bundle,
        require_completed_output=True,
        worker_output_override=validation_value,
    )
    if verifier_errors:
        raise AuthoringError(
            "proposed completed output failed bundle verification:\n- "
            + "\n- ".join(verifier_errors)
        )


def build_output(bundle: Path) -> tuple[bytes, dict[str, Any]]:
    (
        manifest,
        template,
        readings,
        assets,
        original_bytes,
        output,
    ) = prepare_review_output.bundle_state(bundle)
    verify_manifest(manifest)
    verify_input_projection(readings, assets)
    scaffold = prepare_review_output.scaffold_output(
        template,
        readings,
        assets,
    )
    if output != scaffold:
        raise AuthoringError(
            "output is not the pristine prepared nonsemantic scaffold"
        )

    reading_updates, asset_updates = build_reopened_rows(readings, assets)
    proposed = deepcopy(output)
    proposed.update(
        {
            "prohibited_input_nonuse": False,
            "reading_updates": reading_updates,
            "candidate_proposals": [],
            "asset_updates": asset_updates,
            "route_proposals": [],
            "uncertainties": [],
        }
    )
    validate_proposed_output(
        bundle,
        manifest,
        template,
        readings,
        assets,
        proposed,
    )
    return original_bytes, proposed


def load_authoritative_projection(
    goal_dir: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    readings = [
        row
        for row in prepare_review_output.load_csv_exact(
            goal_dir / "reading-ledger.csv",
            READING_HEADER,
            "authoritative reading ledger",
        )
        if row["path"] == EXPECTED_PATH
    ]
    assets = [
        row
        for row in prepare_review_output.load_csv_exact(
            goal_dir / "asset-ledger.csv",
            ASSET_HEADER,
            "authoritative asset ledger",
        )
        if row["assignment_path"] == EXPECTED_PATH
    ]
    return readings, assets


def check_spec(goal_dir: Path) -> tuple[str, str]:
    readings, assets = load_authoritative_projection(goal_dir.resolve())
    reading_updates, asset_updates = build_reopened_rows(readings, assets)
    reading_sha = projection_sha256(reading_updates)
    asset_sha = projection_sha256(asset_updates)
    if reading_sha != EXPECTED_REOPEN_READING_SHA256:
        raise AuthoringError(
            f"reopened reading projection digest changed: {reading_sha}"
        )
    if asset_sha != EXPECTED_REOPEN_ASSET_SHA256:
        raise AuthoringError(
            f"reopened asset projection digest changed: {asset_sha}"
        )
    return reading_sha, asset_sha


def main() -> int:
    if len(sys.argv) in {2, 3} and sys.argv[1] == "--check-spec":
        goal_dir = (
            Path(sys.argv[2])
            if len(sys.argv) == 3
            else TOOLS.parent
        )
        try:
            reading_sha, asset_sha = check_spec(goal_dir)
        except (
            OSError,
            csv.Error,
            json.JSONDecodeError,
            AuthoringError,
            prepare_review_output.PreparationError,
            ValueError,
        ) as exc:
            print(f"Chapter 4 main reopen specification failed: {exc}", file=sys.stderr)
            return 1
        print(
            "Stage 8 Chapter 4 main epoch-2 reopen specification OK: "
            f"reading={EXPECTED_READING_COUNT} assets={EXPECTED_ASSET_COUNT} "
            f"corrected={len(TARGET_ASSET_IDS)} "
            f"reading_sha256={reading_sha} asset_sha256={asset_sha}"
        )
        return 0

    if len(sys.argv) != 2:
        print(
            f"usage: {Path(sys.argv[0]).name} BUNDLE\n"
            f"       {Path(sys.argv[0]).name} --check-spec [GOAL_DIR]",
            file=sys.stderr,
        )
        return 2

    bundle = Path(sys.argv[1]).resolve()
    try:
        with prepare_review_output.output_lock(bundle):
            original_bytes, proposed = build_output(bundle)
            prepare_review_output.atomic_replace(
                bundle / "output" / "output.json",
                canonical_json_bytes(proposed),
                original_bytes,
            )
    except (
        OSError,
        csv.Error,
        json.JSONDecodeError,
        AuthoringError,
        prepare_review_output.PreparationError,
        ValueError,
    ) as exc:
        print(f"Chapter 4 main reopen authoring failed: {exc}", file=sys.stderr)
        return 1

    print(
        "recorded Stage 8 Chapter 4 main epoch-2 reopen: "
        f"reading={EXPECTED_READING_COUNT} assets={EXPECTED_ASSET_COUNT} "
        f"corrected_assets={len(TARGET_ASSET_IDS)} candidates=0 routes=0 "
        "declaration=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
