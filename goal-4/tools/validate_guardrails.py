#!/usr/bin/env python3
"""Validate the frozen Goal 4 Stage 1 contracts and compatibility baseline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from guardrail_lib import GuardrailError, load_json, validate_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--quality", type=Path)
    parser.add_argument("--licensing", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--without-baseline", action="store_true")
    parser.add_argument("--skip-current-script-hashes", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve(strict=True)
    contract_path = args.contract or root / "goal-4/guardrails.json"
    quality_path = args.quality or root / "goal-4/quality-evaluation.json"
    licensing_path = args.licensing or root / "goal-4/licensing-contract.json"
    baseline_path = args.baseline or root / "goal-4/compatibility-baseline.json"
    try:
        baseline = None if args.without_baseline else load_json(baseline_path)
        validate_contract(
            load_json(contract_path),
            load_json(quality_path),
            load_json(licensing_path),
            root,
            baseline=baseline,
            check_current_scripts=not args.skip_current_script_hashes,
        )
    except GuardrailError as error:
        print(f"GUARDRAILS FAIL: {error}", file=sys.stderr)
        return 1
    print("GUARDRAILS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
