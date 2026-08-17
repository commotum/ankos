"""Tests for genuine Substitua aliases, not canonical identity wrappers."""

from __future__ import annotations

import inspect

import pytest

from ca.catalog import substitua


@pytest.mark.parametrize(
    ("alias_name", "delegate_name"),
    (
        ("multiway_system", "multiway_rewrite"),
        ("network_rewrite", "parallel_network_rewrite"),
    ),
)
def test_true_alias_forwards_its_semantic_arguments(
    monkeypatch,
    alias_name: str,
    delegate_name: str,
) -> None:
    alias = getattr(substitua, alias_name)
    delegate = getattr(substitua, delegate_name)
    canonical_signature = inspect.signature(delegate)
    arguments = {
        name: object()
        for name in canonical_signature.parameters
    }
    expected = object()
    received: list[dict[str, object]] = []

    def replacement(**values):
        received.append(values)
        return expected

    monkeypatch.setattr(substitua, delegate_name, replacement)

    assert inspect.signature(alias) == canonical_signature
    assert alias(**arguments) is expected
    assert received == [arguments]
