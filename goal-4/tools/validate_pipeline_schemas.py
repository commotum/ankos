#!/usr/bin/env python3
"""Independently validate the externally pinned Stage 4 schema package."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from pipeline_schema_lib import PipelineSchemaError, validate_package


# The lock deliberately excludes this validator, avoiding a circular digest.
# Replaced only after schemas, library, and tests are final and independently
# hashed.  Self-consistent lock/schema tampering therefore fails here.
EXPECTED_PIPELINE_SCHEMA_LOCK_SHA256 = "923528eb64caf7a3d2df529da3a4608e11cced6852e62cd3ace269985d6b825c"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=repository_root())
    args = parser.parse_args(argv)
    try:
        result = validate_package(args.repo_root.resolve(), EXPECTED_PIPELINE_SCHEMA_LOCK_SHA256)
    except (OSError, PipelineSchemaError) as exc:
        print(f"Stage 4 pipeline schema validation: FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "Stage 4 pipeline schema validation: PASS "
        f"schemas={result['schema_count']} "
        f"ledger_schemas={result['ledger_schema_count']} "
        f"locked_artifacts={result['artifact_count']} "
        f"lock={result['lock_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
