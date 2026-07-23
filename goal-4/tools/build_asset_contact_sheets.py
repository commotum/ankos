#!/usr/bin/env python3
"""Build labelled, nonsemantic contact sheets from a sealed worker bundle.

This helper is only a visual-screening aid.  It reads immutable asset
identities from ``input/asset-input.csv`` and canonical image bytes from the
Book tree, then writes page-numbered PNG contact sheets outside the bundle.
It never writes audit dispositions or modifies source material.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO_ROOT / "ref" / "A-New-Kind-of-Science"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--tile-width", type=int, default=320)
    parser.add_argument("--tile-height", type=int, default=300)
    return parser.parse_args()


def load_assets(bundle: Path) -> list[dict[str, str]]:
    with (bundle / "input" / "asset-input.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        return list(csv.DictReader(handle))


def render_tile(
    row: dict[str, str],
    *,
    width: int,
    height: int,
    font: ImageFont.ImageFont,
) -> Image.Image:
    label_height = 54
    tile = Image.new("RGB", (width, height), "white")
    image_path = SOURCE_ROOT / row["physical_path"]
    with Image.open(image_path) as source:
        source = ImageOps.exif_transpose(source).convert("RGB")
        shown = ImageOps.contain(
            source,
            (width - 12, height - label_height - 12),
            Image.Resampling.LANCZOS,
        )
    tile.paste(
        shown,
        ((width - shown.width) // 2, 6 + (height - label_height - 12 - shown.height) // 2),
    )
    draw = ImageDraw.Draw(tile)
    basename = Path(row["physical_path"]).name
    text = f"{row['asset_id']} · {row['source_unit_id']}\n{basename}"
    draw.multiline_text((7, height - label_height + 4), text, fill="black", font=font)
    draw.rectangle((0, 0, width - 1, height - 1), outline="#777777")
    return tile


def main() -> int:
    args = parse_args()
    bundle = args.bundle.resolve()
    output_dir = args.output_dir.resolve()
    if args.columns < 1 or args.rows < 1:
        raise ValueError("columns and rows must be positive")
    assets = load_assets(bundle)
    output_dir.mkdir(parents=True, exist_ok=True)
    per_sheet = args.columns * args.rows
    sheet_count = math.ceil(len(assets) / per_sheet)
    font = ImageFont.load_default()
    for sheet_index in range(sheet_count):
        subset = assets[
            sheet_index * per_sheet : (sheet_index + 1) * per_sheet
        ]
        sheet = Image.new(
            "RGB",
            (args.columns * args.tile_width, args.rows * args.tile_height),
            "#dddddd",
        )
        for offset, row in enumerate(subset):
            tile = render_tile(
                row,
                width=args.tile_width,
                height=args.tile_height,
                font=font,
            )
            x = (offset % args.columns) * args.tile_width
            y = (offset // args.columns) * args.tile_height
            sheet.paste(tile, (x, y))
        output_path = output_dir / f"contact-{sheet_index + 1:03d}.png"
        sheet.save(output_path, format="PNG", optimize=True)
        print(output_path)
    print(f"assets={len(assets)} sheets={sheet_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
