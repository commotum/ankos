"""Unit tests for closed Seed denotations."""

from fractions import Fraction

import pytest

from ca import alphabets, loci, seeds


def test_exact_seed_infers_carrier_and_value_profile() -> None:
    configuration = loci.history_configuration((True, False, True))
    seed = seeds.exact(configuration)

    assert isinstance(seed.source, seeds.ExactSource)
    assert seed.configuration_contract == configuration.contract
    assert seed.value_profile is alphabets.ValueProfile.BOOLEAN
    assert seed.denote().exact_configuration is configuration
    assert seed.entropy_interface is seeds.EntropyInterface.NONE


def test_constructive_partial_and_intensional_sources_are_explicit() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(2,),
        axes=("history",),
    )
    construction = seeds.Construction(
        seeds.ConstructionOp.SEQUENCE,
        ((True, False),),
    )
    constructive = seeds.constructive(
        construction,
        configuration_contract=contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    configuration = loci.history_configuration((True, False))
    obligation = loci.SelectorExpr(loci.SelectorPrimitive.MEMBERSHIP)
    partial = seeds.partial(
        configuration,
        unresolved=(configuration.entries[0][0],),
        obligations=(obligation,),
        configuration_contract=contract,
        value_profile=alphabets.ValueProfile.BOOLEAN,
    )
    intensional = seeds.intensional(
        "x",
        obligation,
        configuration_contract=loci.CarrierContract(
            loci.CarrierKind.INTENSIONAL
        ),
        value_profile=alphabets.ValueProfile.SYMBOLIC,
    )

    assert isinstance(constructive.source, seeds.ConstructiveSource)
    assert isinstance(partial.source, seeds.PartialSource)
    assert isinstance(intensional.source, seeds.IntensionalSource)


def test_probability_seed_requires_exact_law_and_replay_key_interface() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    seed = seeds.uniform_bits(
        length=3,
        configuration_contract=contract,
        reject_all_zero=True,
    )

    assert isinstance(seed.source, seeds.LawSource)
    assert isinstance(seed.source.law, seeds.UniformTupleLaw)
    assert seed.source.law.excluded == ((0, 0, 0),)
    assert seed.entropy_interface is seeds.EntropyInterface.REPLAY_KEY
    assert not hasattr(seed, "rng")
    with pytest.raises(TypeError):
        seeds.bernoulli(
            loci.literal((loci.named("cell"),)),
            0.5,  # type: ignore[arg-type]
            configuration_contract=loci.CarrierContract(
                loci.CarrierKind.RECORD,
                rank=0,
                shape=(),
            ),
        )


def test_seed_composition_preserves_one_closed_component() -> None:
    left = seeds.sequence((True, False))
    right = seeds.sequence((False, True))
    overlay = seeds.overlay(
        (left, right),
        conflict=seeds.OverlayConflict.REQUIRE_EQUAL,
    )
    mixture = seeds.mixture(
        ((Fraction(1, 2), left), (Fraction(1, 2), right))
    )

    assert isinstance(overlay, seeds.Seed)
    assert isinstance(overlay.source, seeds.OverlaySource)
    assert isinstance(mixture.source, seeds.MixtureSource)
    assert mixture.entropy_interface is seeds.EntropyInterface.REPLAY_KEY


def test_named_helpers_build_structural_configurations_not_arrays() -> None:
    pair = seeds.pair(3, 5)
    grid = seeds.finite_grid(
        (3,),
        (False, True, False),
        boundary=loci.Boundary(loci.BoundaryPolicy.FIXED, False),
    )

    assert pair.configuration_contract.kind is loci.CarrierKind.RECORD
    assert grid.configuration_contract.kind is loci.CarrierKind.GRID
    assert isinstance(pair.denote().exact_configuration, loci.FiniteConfiguration)
    assert isinstance(grid.denote().exact_configuration, loci.FiniteConfiguration)
    assert not hasattr(seeds, "render")
    assert not hasattr(seeds, "structured")


def test_seed_descriptors_reject_callbacks_and_malformed_composition() -> None:
    with pytest.raises(seeds.SeedValidationError):
        seeds.Construction(
            seeds.ConstructionOp.SEQUENCE,
            ((lambda: None,),),  # type: ignore[arg-type]
        )
    with pytest.raises(seeds.SeedValidationError):
        seeds.mixture(())
    with pytest.raises(seeds.SeedValidationError):
        seeds.uniform_bits(
            length=0,
            configuration_contract=loci.CarrierContract(
                loci.CarrierKind.HISTORY,
                rank=1,
                shape=(1,),
                axes=("history",),
            ),
        )
    with pytest.raises(TypeError):
        seeds.Construction(
            seeds.ConstructionOp.SEQUENCE,
            [(True, False)],  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        seeds.OverlaySource(
            (seeds.sequence((True, False)),),
            "opaque",  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        seeds.UniformTupleLaw(
            2,
            2,
            [[0, 0]],  # type: ignore[arg-type]
        )
    with pytest.raises(TypeError):
        seeds.RefinedSource(
            seeds.sequence((True, False)),
            "opaque",  # type: ignore[arg-type]
        )
