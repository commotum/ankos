"""CT06: laws, exact submeasures, Seed realization, and replay."""

from fractions import Fraction

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import certificate, diamond_program, rule_contract


def test_rule_law_contains_no_draw_and_applied_mass_is_preserved() -> None:
    simple_program, source = diamond_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    law = result.source_outcomes.probability_law
    assert law is not None
    assert tuple(item.mass for item in law.masses) == (
        Fraction(1, 3),
        Fraction(2, 3),
    )
    assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
    assert result.applied_atom_measure.measure.total_mass == 1
    assert isinstance(result.successor_submeasure, program.MeasureAvailable)
    assert result.successor_submeasure.measure.total_mass == 1
    assert result.successor_submeasure.measure.masses[0].mass == 1
    assert isinstance(result.no_successor_submeasure, program.MeasureAvailable)
    assert result.no_successor_submeasure.measure.total_mass == 0
    assert not hasattr(law, "draw")


def test_replay_is_deterministic_and_lineage_bound() -> None:
    simple_program, source = diamond_program()

    left = ca.rollout(
        simple_program,
        steps=1,
        initial=source,
        replay_key="same-key",
    )
    right = ca.rollout(
        simple_program,
        steps=1,
        initial=source,
        replay_key="same-key",
    )

    assert isinstance(left, program.RolloutTruncated)
    assert isinstance(right, program.RolloutTruncated)
    assert left.raw_trace.derivation_edges.atoms == right.raw_trace.derivation_edges.atoms
    assert left.raw_trace.lineage_graph == right.raw_trace.lineage_graph
    assert len(left.raw_trace.derivation_edges.atoms) == 1


def test_seed_law_handles_no_key_keyed_realization_and_explicit_initial() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    seed = seeds.uniform_bits(
        length=3,
        configuration_contract=contract,
    )
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.dyadlags_0d(configuration_contract=contract)
    simple_program = ca.SimpleProgram(
        seed,
        alphabet,
        writable,
        readable,
        rules.dyadlags_0d(rule=150),
    )

    no_key = ca.rollout(simple_program, steps=0)
    keyed = ca.rollout(simple_program, steps=0, replay_key=17)
    initial = loci.history_configuration((True, False, True))
    explicit = ca.rollout(
        simple_program,
        steps=0,
        initial=initial,
        replay_key=17,
    )

    assert isinstance(no_key, program.RolloutTruncated)
    assert len(no_key.raw_trace.roots.support.atoms) == 8
    assert no_key.raw_trace.roots.probability_law is not None
    assert isinstance(keyed, program.RolloutTruncated)
    assert len(keyed.raw_trace.roots.support.atoms) == 8
    assert keyed.raw_trace.roots.probability_law is not None
    assert len(keyed.continuing_leaves.atoms) == 1
    assert keyed.raw_trace.seed_evidence.selected_identity is not None
    assert isinstance(explicit, program.RolloutTruncated)
    assert explicit.raw_trace.roots.support.atoms == (initial,)
    assert explicit.raw_trace.seed_evidence.source_identity == "explicit-initial"


def test_unavailable_is_narrowly_limited_to_successor_quotient_measure() -> None:
    source = loci.record_configuration((("cell", False),))
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    contract = rule_contract(
        source,
        alphabet,
        writable,
        readable,
        entropy=seeds.EntropyInterface.REPLAY_KEY,
    )
    unknown = rules.Undetermined(
        rules.literal_expr("law-support"),
        certificate(rules.CertificateKind.CARDINALITY, "law-cardinality"),
    )
    probability = rules.ProbabilityLaw(
        rules.ProbabilityPresentation.INTENSIONAL,
        (),
        rules.literal_expr("closed-measure"),
        certificate(rules.CertificateKind.NORMALIZATION, "normalized"),
        certificate(rules.CertificateKind.MEASURABILITY, "measurable"),
    )
    rule = rules.distribution(
        rules.literal_expr("closed-distribution-relation"),
        unknown,
        probability,
        contract=contract,
        completeness_evidence=certificate(
            rules.CertificateKind.COMPLETENESS,
            "complete",
        ),
        soundness_evidence=certificate(
            rules.CertificateKind.SOUNDNESS,
            "sound",
        ),
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(source),
        alphabet,
        writable,
        readable,
        rule,
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
    assert isinstance(result.no_successor_submeasure, program.MeasureAvailable)
    assert isinstance(result.successor_submeasure, program.MeasureUnavailable)

    with pytest.raises(ValueError, match="normalize"):
        rules.ProbabilityLaw(
            rules.ProbabilityPresentation.FINITE,
            (
                rules.AtomMass("a", Fraction(1, 3)),
                rules.AtomMass("b", Fraction(1, 3)),
            ),
            None,
            certificate(rules.CertificateKind.NORMALIZATION, "bad"),
            certificate(rules.CertificateKind.MEASURABILITY, "space"),
        )
