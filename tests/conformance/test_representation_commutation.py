"""CT10: exact representation mechanics and staged full-result commutation.

G7-02 owns the closed exact/lossy relation and inverse-on-image mechanics.
G7-03 owns canonical codec mapping and the exhaustive comparison of complete
application results.
"""

from fractions import Fraction

import pytest

from ca import alphabets

from g7_mechanics import (
    MECHANICS_ROWS,
    assert_mechanics_run,
    run_mechanics_fixture,
)


def test_exact_representation_is_inverse_on_its_declared_image() -> None:
    """Decode of an encoded source recovers the exact semantic source."""

    row = next(row for row in MECHANICS_ROWS if row.spf == "SPF058")
    execution = run_mechanics_fixture(row)
    assert_mechanics_run(execution)
    relation = execution.representation

    assert relation is not None
    assert relation.profile is alphabets.RepresentationProfile.EXACT
    for pair in relation.mapping:
        assert relation.inverse(relation.forward(pair.source)) == pair.source
    with pytest.raises(ValueError, match="outside"):
        relation.inverse(-1)


@pytest.mark.skip(reason="G7-03 owns canonical full-result representation mapping")
def test_represented_and_native_one_step_results_commute_completely() -> None:
    """Mapped generic application equals the independent native application."""

    raise AssertionError("G7-03 full-result commutation is not active")


@pytest.mark.skip(reason="G7-03 owns codec mapping of all evidence and fibers")
def test_commutation_compares_all_outcomes_evidence_measures_and_fibers() -> None:
    """State-only equality cannot establish a representation relation."""

    raise AssertionError("G7-03 complete-result mapping is not active")


def test_lossy_approximate_or_out_of_image_translation_remains_explicit() -> None:
    """Qualified realizations never masquerade as exact aliases."""

    source = alphabets.enum((0, 1)).descriptor
    target = alphabets.enum((0,)).descriptor
    pairs = (
        alphabets.RepresentationPair(0, 0),
        alphabets.RepresentationPair(1, 0),
    )
    lossy = alphabets.RepresentationRelation(
        source,
        target,
        alphabets.RepresentationProfile.LOSSY,
        pairs,
        (0,),
        qualification=(("discarded-bits", 1),),
    )
    approximate = alphabets.RepresentationRelation(
        source,
        target,
        alphabets.RepresentationProfile.APPROXIMATE,
        pairs,
        (0,),
        qualification=(("error-bound", Fraction(1, 2)),),
    )

    assert lossy.forward(0) == lossy.forward(1) == 0
    assert approximate.qualification == (("error-bound", Fraction(1, 2)),)
    for relation in (lossy, approximate):
        with pytest.raises(ValueError, match="only exact"):
            relation.inverse(0)
        with pytest.raises(ValueError, match="outside"):
            relation.forward(2)
