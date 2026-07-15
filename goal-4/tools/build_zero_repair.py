#!/usr/bin/env python3
"""Build an opaque, byte-faithful Goal 4 zero-repair staging tree."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from zero_repair_lib import (
    ZeroRepairError,
    build_zero_repair,
    compare_zero_repair_trees,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--goal-root", type=Path)
    parser.add_argument("--legacy-root", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--comparison-output-root", type=Path)
    args = parser.parse_args()
    try:
        goal = args.goal_root
        if goal is None:
            goal = args.repo_root / "goal-4"
        elif not goal.is_absolute():
            goal = args.repo_root / goal
        declared_cli = Path(os.path.abspath(goal / "tools/build_zero_repair.py"))
        if Path(os.path.abspath(__file__)) != declared_cli:
            raise ZeroRepairError("executed build CLI path differs from declared Goal 4 build CLI")
        result = build_zero_repair(
            args.repo_root,
            args.output_root,
            goal_root=args.goal_root,
            legacy_root=args.legacy_root,
        )
        if args.comparison_output_root is not None:
            second = build_zero_repair(
                args.repo_root,
                args.comparison_output_root,
                goal_root=args.goal_root,
                legacy_root=args.legacy_root,
            )
            result["comparison_build"] = second
            result["clean_build_equality"] = compare_zero_repair_trees(
                args.output_root,
                args.comparison_output_root,
                repo_root=args.repo_root,
                goal_root=args.goal_root,
                legacy_root=args.legacy_root,
            )
    except (OSError, ZeroRepairError) as error:
        print(f"ZERO-REPAIR BUILD FAIL: {error}", file=sys.stderr)
        return 1
    print("ZERO-REPAIR BUILD OK " + json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
