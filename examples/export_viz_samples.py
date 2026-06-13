"""Export small visualization bundles for the built-in CA datasets."""

from __future__ import annotations

import argparse
from pathlib import Path

import ca


def main() -> None:
    args = _parser().parse_args()
    output_dir = Path(args.output_dir) if args.output_dir else Path(__file__).resolve().parent / "viz-samples"
    output_dir.mkdir(parents=True, exist_ok=True)

    for dataset_id in ca.datasets.DATASET_IDS:
        episode = next(
            ca.datasets.stream(
                dataset_id,
                kind="held-out-seed",
                count=1,
                profile="compact",
            )
        )
        path = output_dir / f"{dataset_id}-held-out-seed.ankos"
        ca.viz.save_viewer_bundle(
            episode,
            path,
            include_coords=True,
            title=f"{dataset_id} held-out seed",
            metadata={"dataset_id": dataset_id, "source": "examples/export_viz_samples.py"},
        )
        print(path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Directory for generated .ankos bundles. Defaults to examples/viz-samples.",
    )
    return parser


if __name__ == "__main__":
    main()
