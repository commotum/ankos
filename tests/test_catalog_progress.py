"""Small contract joining the book-ordered taxonomy to its live API surface."""

from __future__ import annotations

import csv
from inspect import Parameter, signature
from pathlib import Path

import ca
from ca.catalog import entries


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


def test_taxonomy_rows_join_to_their_planned_builder_signatures() -> None:
    rows = {row["family_id"]: row for row in _type_rows()}
    families = {entry.family_id: entry for entry in entries.FAMILY_ENTRIES}

    assert rows.keys() == families.keys()
    for family_id, row in rows.items():
        entry = families[family_id]
        assert (row["home"], row["slug"]) == (entry.home, entry.slug)

        owner = getattr(ca.catalog, entry.home)
        builder = getattr(owner, entry.constructor_name)
        parameters = tuple(signature(builder).parameters.values())
        assert tuple(parameter.name for parameter in parameters) == (
            entry.closed_parameters
        )
        assert all(
            parameter.kind is Parameter.KEYWORD_ONLY
            and parameter.default is Parameter.empty
            for parameter in parameters
        )
        assert getattr(ca.catalog, entry.constructor_name) is builder
