"""Keep the book taxonomy ordered while implementations remain honest."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _type_rows() -> tuple[dict[str, str], ...]:
    with (ROOT / "ref" / "types.csv").open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        assert reader.fieldnames is not None
        assert reader.fieldnames[:4] == ["book_index", "family_id", "home", "slug"]
        return tuple(reader)


def test_book_ordered_taxonomy_is_complete_and_unique() -> None:
    rows = _type_rows()

    assert tuple(row["book_index"] for row in rows) == tuple(
        f"B{index:03d}" for index in range(1, 61)
    )
    assert len({row["family_id"] for row in rows}) == len(rows) == 60
    assert len({(row["home"], row["slug"]) for row in rows}) == len(rows)
    assert len({row["canonical_name_development_stub"] for row in rows}) == len(rows)
