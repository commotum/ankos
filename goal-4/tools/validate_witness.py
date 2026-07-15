#!/usr/bin/env python3
"""Validate Goal 4's Stage 3 witness schema and source-blocked state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from witness_lib import WitnessError, load_json, validate_all, validate_external_lock_root


EXPECTED_WITNESS_LOCK_SHA256 = "f348e4dd0ebf328c48066696eb70359d954e07cbdfd7b7fd827286e3268ba449"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--skip-payload-scan", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve(strict=True)
    try:
        validate_external_lock_root(root, EXPECTED_WITNESS_LOCK_SHA256)
        result = validate_all(
            root,
            contract=load_json(args.contract) if args.contract else None,
            registry=load_json(args.registry) if args.registry else None,
            state=load_json(args.state) if args.state else None,
            scan_payloads=not args.skip_payload_scan,
        )
    except WitnessError as error:
        print(f"WITNESS FAIL: {error}", file=sys.stderr)
        return 1
    print("WITNESS OK " + json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
