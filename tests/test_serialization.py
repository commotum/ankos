"""Goal 7 unit-contract skeleton for canonical semantic serialization.

These tests will cover generic owner-node codecs and the expanded five-field
program envelope without catalog recipes or legacy fallback. The module is
skipped until G7-03 implementation; no skipped assertion is evidence of
conformance.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="G7-03 owns the canonical serialization unit contract"
)


def _pending() -> NoReturn:
    raise NotImplementedError("G7-03 serialization tests are not implemented")


def test_decode_result_is_decoded_or_typed_rejection() -> None:
    """Decoding never returns a partial semantic object."""

    _pending()


def test_canonical_program_envelope_uses_tag_v1_and_exactly_five_keys() -> None:
    """The first canonical program schema is ca.simple-program version 1."""

    _pending()


def test_every_public_semantic_record_round_trips_canonically() -> None:
    """Components, results, evidence, and traces share the generic codec boundary."""

    _pending()


def test_unknown_or_lossy_payloads_fail_closed() -> None:
    """Unknown tags, versions, fields, primitives, and migrations are rejected."""

    _pending()


def test_catalog_invocation_and_legacy_dynamics_are_not_canonical_payloads() -> None:
    """Aliases and 0.1 manifests cannot be resolved or recovered by the codec."""

    _pending()
