"""Honest public-boundary tests for unfinished differential builders."""

from __future__ import annotations

import inspect

import pytest

from ca.catalog import dynamica


def test_currently_unimplemented_ode_builder_fails_explicitly() -> None:
    """An unfinished builder must not masquerade as a completed construction.

    Replace this smoke test with semantic lowering tests when the ODE builder is
    implemented.  Deliberately testing one representative avoids freezing an
    inventory of sixty stubs into the public contract.
    """

    with pytest.raises(NotImplementedError):
        dynamica.ordinary_differential_flow(
            seed=object(),
            rhs=object(),
            parameters=object(),
            duration_or_event=object(),
        )


def test_pde_is_a_same_signature_forwarding_alias(monkeypatch) -> None:
    canonical_signature = inspect.signature(
        dynamica.partial_differential_relation
    )
    expected = object()
    received: list[tuple[object, object, object, object]] = []

    def delegate(
        *,
        domain,
        coefficients,
        differential_relation,
        side_data,
    ):
        received.append(
            (domain, coefficients, differential_relation, side_data)
        )
        return expected

    arguments = {
        "domain": object(),
        "coefficients": object(),
        "differential_relation": object(),
        "side_data": object(),
    }
    monkeypatch.setattr(
        dynamica,
        "partial_differential_relation",
        delegate,
    )

    assert inspect.signature(dynamica.pde) == canonical_signature
    assert dynamica.pde(**arguments) is expected
    assert received == [tuple(arguments.values())]
