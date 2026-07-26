"""CT06: laws, exact submeasures, Seed realization, and replay."""

from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
import random

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_fixtures import (
    certificate,
    derivation,
    diamond_program,
    finite_record_program,
    no_successor,
    rule_contract,
)


def test_rule_law_contains_no_draw_and_applied_mass_is_preserved() -> None:
    simple_program, source = diamond_program()

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    law = result.source_outcomes.probability_law
    assert law is not None
    assert sorted(item.mass for item in law.masses) == [
        Fraction(1, 3),
        Fraction(2, 3),
    ]
    assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
    assert result.applied_atom_measure.measure.total_mass == 1
    assert isinstance(result.successor_submeasure, program.MeasureAvailable)
    assert result.successor_submeasure.measure.total_mass == 1
    assert result.successor_submeasure.measure.masses[0].mass == 1
    assert isinstance(result.no_successor_submeasure, program.MeasureAvailable)
    assert result.no_successor_submeasure.measure.total_mass == 0
    assert not hasattr(law, "draw")


def test_terminal_measurement_keeps_successor_and_no_successor_submeasures() -> None:
    """PX09 measurement is a law over a stopped result and typed terminal."""

    def measured_gate(targets):
        return (
            derivation(
                "gate-open",
                existing=tuple(rules.replace(target, True) for target in targets),
                continuation=rules.Stop(
                    rules.literal_expr("measurement-complete"),
                    certificate(
                        rules.CertificateKind.TERMINALITY,
                        "measurement-complete",
                    ),
                ),
            ),
            no_successor(
                "gate-closed",
                rules.NoSuccessorOutcome.TERMINAL,
            ),
        )

    simple_program, source = finite_record_program(
        (("measured-gate", False),),
        measured_gate,
        probability=(Fraction(1, 4), Fraction(3, 4)),
    )

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert rules.cardinality_size(result.outcome_atom_cardinality) == 2
    assert rules.cardinality_size(result.derivation_cardinality) == 1
    assert rules.cardinality_size(result.successor_cardinality) == 1
    assert isinstance(result.applied_atom_measure, program.MeasureAvailable)
    assert result.applied_atom_measure.measure.total_mass == 1
    assert isinstance(result.successor_submeasure, program.MeasureAvailable)
    assert result.successor_submeasure.measure.total_mass == Fraction(1, 4)
    assert isinstance(result.no_successor_submeasure, program.MeasureAvailable)
    assert result.no_successor_submeasure.measure.total_mass == Fraction(3, 4)
    assert len(result.no_successor_partition.atoms) == 1
    assert (
        result.no_successor_partition.atoms[0].source.outcome
        is rules.NoSuccessorOutcome.TERMINAL
    )


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
    assert len(left.raw_trace.draw_evidence) == 1
    draw = left.raw_trace.draw_evidence[0]
    assert draw.sampler_profile is program.SamplerProfile.SHA256_REJECTION_V1
    assert draw.numeric_profile is program.NumericProfile.FRACTION_TICKETS_V1
    assert draw.application_identity
    assert draw.law_identity
    assert draw.subkey_identity
    assert draw.selected_witness_identity


def test_replay_ignores_ambient_rng_unrelated_draws_and_worker_presentation() -> None:
    simple_program, source = diamond_program()

    expected = ca.rollout(
        simple_program,
        steps=1,
        initial=source,
        replay_key="stable-coordinate",
    )
    ambient_state = random.getstate()
    try:
        random.seed(918273)
        _ = tuple(random.random() for _ in range(200))
        ambient_perturbed = ca.rollout(
            simple_program,
            steps=1,
            initial=source,
            replay_key="stable-coordinate",
        )
    finally:
        random.setstate(ambient_state)
    for unrelated_key in ("other-a", "other-b", "other-c"):
        ca.rollout(
            simple_program,
            steps=1,
            initial=source,
            replay_key=unrelated_key,
        )
    eager = [
        ca.rollout(
            simple_program,
            steps=1,
            initial=source,
            replay_key="stable-coordinate",
        )
        for _ in range(3)
    ]
    lazy = tuple(
        ca.rollout(
            simple_program,
            steps=1,
            initial=source,
            replay_key="stable-coordinate",
        )
        for _ in range(3)
    )
    with ThreadPoolExecutor(max_workers=1) as one_worker:
        serial_worker = tuple(
            one_worker.map(
                lambda _: ca.rollout(
                    simple_program,
                    steps=1,
                    initial=source,
                    replay_key="stable-coordinate",
                ),
                range(3),
            )
        )
    with ThreadPoolExecutor(max_workers=3) as three_workers:
        parallel_workers = tuple(
            three_workers.map(
                lambda _: ca.rollout(
                    simple_program,
                    steps=1,
                    initial=source,
                    replay_key="stable-coordinate",
                ),
                reversed(range(3)),
            )
        )

    assert ambient_perturbed == expected
    assert all(item == expected for item in eager)
    assert all(item == expected for item in lazy)
    assert all(item == expected for item in serial_worker)
    assert all(item == expected for item in parallel_workers)


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


def test_seed_law_is_immutable_across_keys_and_invalid_keys_fail_closed() -> None:
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(3,),
        axes=("history",),
    )
    seed = seeds.uniform_bits(length=3, configuration_contract=contract)
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
        rules.dyadlags_0d(rule=6),
    )
    seed_identity = loci.canonical_identity(seed)

    left = ca.rollout(simple_program, steps=0, replay_key="left-key")
    right = ca.rollout(simple_program, steps=0, replay_key="right-key")
    invalid = ca.rollout(
        simple_program,
        steps=0,
        replay_key=object(),  # type: ignore[arg-type]
    )

    assert isinstance(left, program.RolloutTruncated)
    assert isinstance(right, program.RolloutTruncated)
    assert left.raw_trace.roots == right.raw_trace.roots
    assert left.raw_trace.seed_evidence.denotation == right.raw_trace.seed_evidence.denotation
    assert loci.canonical_identity(simple_program.seed) == seed_identity
    assert isinstance(invalid, program.RolloutRejected)
    assert invalid.fault.evidence == ("TypeError",)
    assert not hasattr(invalid, "raw_trace")


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
    assert result.applied_atom_measure.measure.total_mass is None
    assert result.no_successor_submeasure.measure.total_mass is None

    rolled = ca.rollout(simple_program, steps=1, initial=source)
    assert isinstance(rolled, program.RolloutTruncated)
    assert rolled.cause is program.TruncationCause.INTENSIONAL_SUPPORT
    assert len(rolled.raw_trace.applications.atoms) == 1

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


def test_large_seed_law_is_retained_without_eager_enumeration_and_draws_directly() -> None:
    length = 20
    contract = loci.CarrierContract(
        loci.CarrierKind.HISTORY,
        rank=1,
        shape=(length,),
        axes=("history",),
    )
    seed = seeds.uniform_bits(
        length=length,
        configuration_contract=contract,
    )
    template = loci.history_configuration((False,) * length)
    alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=contract,
        value_profile=alphabet.value_profile,
    )
    atom = rules.Derivation(
        rules.TotalDisposition(
            tuple(rules.preserve(target) for target, _ in template.entries),
            (),
            certificate(rules.CertificateKind.TOTALITY, "large-seed:total"),
        ),
        rules.Progress.QUIESCENT,
        rules.Continue(),
        rules.Witness("large-seed", rules.literal_expr("large-seed")),
        ("test:large-seed",),
        certificate(rules.CertificateKind.DERIVATION, "large-seed:derived"),
    )
    rule = rules.finite_rule(
        (atom,),
        contract=rule_contract(template, alphabet, writable, readable),
    )
    simple_program = ca.SimpleProgram(
        seed,
        alphabet,
        writable,
        readable,
        rule,
    )

    unkeyed = ca.rollout(simple_program, steps=0)
    keyed = ca.rollout(simple_program, steps=0, replay_key="large-seed-key")

    assert isinstance(unkeyed, program.RolloutTruncated)
    assert (
        unkeyed.raw_trace.roots.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert rules.cardinality_size(
        unkeyed.raw_trace.roots.support.cardinality
    ) == 2**length
    assert unkeyed.cause is program.TruncationCause.INTENSIONAL_SUPPORT
    assert isinstance(keyed, program.RolloutTruncated)
    assert (
        keyed.raw_trace.roots.support.presentation
        is rules.SupportPresentation.INTENSIONAL
    )
    assert keyed.cause is program.TruncationCause.DEPTH_BOUND
    assert len(keyed.continuing_leaves.atoms) == 1
    assert len(keyed.raw_trace.seed_evidence.draws) == length
    assert keyed.raw_trace.seed_evidence.denotation is not None
