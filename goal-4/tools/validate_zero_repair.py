#!/usr/bin/env python3
"""Validate and inversely replay a Goal 4 zero-repair staging tree."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from zero_repair_lib import ZeroRepairError, compare_zero_repair_trees
from zero_repair_verify import (
    IndependentVerificationError,
    independently_validate_zero_repair,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--goal-root", type=Path)
    parser.add_argument("--legacy-root", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--compare-root", type=Path)
    args = parser.parse_args()
    try:
        result = independently_validate_zero_repair(
            args.repo_root,
            args.output_root,
            goal_root=args.goal_root,
            legacy_root=args.legacy_root,
        )
        if args.compare_root is not None:
            result["comparison_build"] = independently_validate_zero_repair(
                args.repo_root,
                args.compare_root,
                goal_root=args.goal_root,
                legacy_root=args.legacy_root,
            )
            result["clean_build_equality"] = compare_zero_repair_trees(
                args.output_root,
                args.compare_root,
                repo_root=args.repo_root,
                goal_root=args.goal_root,
                legacy_root=args.legacy_root,
            )
    except (OSError, ZeroRepairError, IndependentVerificationError) as error:
        print(f"ZERO-REPAIR VALIDATION FAIL: {error}", file=sys.stderr)
        return 1
    print("ZERO-REPAIR VALIDATION OK " + json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
