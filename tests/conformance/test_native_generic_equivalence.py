"""CT12 skeleton: independent native and generic equivalence.

The implemented suite will use test-only reference steps and tiny exact
fixtures that share no runtime implementation with ``program.apply``. This
module remains skipped until implementation; skips are not conformance
evidence.
"""

from typing import NoReturn

import pytest


pytestmark = pytest.mark.skip(
    reason="Goal 7 CT12 native/generic skeleton; implementation is pending"
)


def _pending() -> NoReturn:
    raise NotImplementedError("Goal 7 CT12 tests are not implemented")


def test_reference_oracles_are_statically_independent_of_runtime_semantics() -> None:
    """Fixtures import no apply, catalog constructor, evaluator, or commit helper."""

    _pending()


def test_finite_native_fixtures_match_complete_generic_results() -> None:
    """Cellular, mobile/Turing, substitution, multiway, and constraint cases agree."""

    _pending()


def test_variable_structure_and_stochastic_fixtures_match_completely() -> None:
    """Bindings, witnesses, measures, and fibers join the independent result."""

    _pending()


def test_differential_and_intensional_fixtures_use_exact_tiny_oracles() -> None:
    """Canonical AST or exact finite characterizations avoid a hidden solver."""

    _pending()
