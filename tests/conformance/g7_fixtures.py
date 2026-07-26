"""Small closed fixtures shared by the active G7-01 conformance tests."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds


Semantic = alphabets.SemanticValue


def certificate(kind: rules.CertificateKind, label: str) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def witness(identity: str) -> rules.Witness:
    return rules.Witness(identity, rules.literal_expr(identity))


def derivation(
    identity: str,
    *,
    existing: tuple[rules.Disposition[loci.Locus, Semantic], ...],
    fresh: tuple[
        rules.Disposition[loci.FreshReference, Semantic], ...
    ] = (),
    progress: rules.Progress = rules.Progress.ADVANCED,
    continuation: rules.Continuation = rules.Continue(),
) -> rules.Derivation[Semantic]:
    return rules.Derivation(
        rules.TotalDisposition(
            existing,
            fresh,
            certificate(rules.CertificateKind.TOTALITY, f"{identity}:total"),
        ),
        progress,
        continuation,
        witness(identity),
        (f"test:{identity}",),
        certificate(rules.CertificateKind.DERIVATION, f"{identity}:derived"),
    )


def no_successor(
    identity: str,
    outcome: rules.NoSuccessorOutcome = rules.NoSuccessorOutcome.TERMINAL,
) -> rules.NoSuccessor:
    kind = (
        rules.CertificateKind.DIVERGENCE
        if outcome is rules.NoSuccessorOutcome.DIVERGENT
        else rules.CertificateKind.TERMINALITY
    )
    return rules.NoSuccessor(
        outcome,
        rules.literal_expr(f"{identity}:reason"),
        witness(identity),
        (f"test:{identity}",),
        certificate(kind, f"{identity}:certificate"),
    )


def rule_contract(
    configuration: loci.FiniteConfiguration[Semantic],
    alphabet: alphabets.Alphabet[Semantic],
    frontier: frontiers.WritableRegion,
    neighborhood: neighborhoods.ReadableRegion,
    *,
    entropy: seeds.EntropyInterface = seeds.EntropyInterface.NONE,
) -> rules.RuleContract:
    return rules.RuleContract(
        configuration.contract,
        alphabet.value_profile,
        neighborhood.result_shape,
        neighborhood.join_shape,
        frontier.effect_profile,
        entropy_interface=entropy,
    )


def finite_record_program(
    fields: tuple[tuple[str, Semantic], ...],
    atoms_factory,
    *,
    alphabet: alphabets.Alphabet[Semantic] | None = None,
    effects: tuple[frontiers.Effect, ...] = (
        frontiers.Effect.REPLACE,
        frontiers.Effect.DELETE,
    ),
    probability: tuple[Fraction, ...] | None = None,
) -> tuple[ca.SimpleProgram, loci.FiniteConfiguration[Semantic]]:
    """Build a literal finite Rule after its canonical target order is known."""

    configuration = loci.record_configuration(fields)
    if alphabet is None:
        alphabet = alphabets.boolean()
    writable = frontiers.everywhere(
        configuration_contract=configuration.contract,
        value_profile=alphabet.value_profile,
        effects=effects,
    )
    readable = neighborhoods.global_view(
        configuration_contract=configuration.contract,
        value_profile=alphabet.value_profile,
    )
    atoms = tuple(atoms_factory(tuple(target for target, _ in configuration.entries)))
    law = None
    if probability is not None:
        law = rules.finite_probability_law(
            tuple(zip(atoms, probability, strict=True))
        )
    rule = rules.finite_rule(
        atoms,
        contract=rule_contract(
            configuration,
            alphabet,
            writable,
            readable,
            entropy=(
                seeds.EntropyInterface.REPLAY_KEY
                if probability is not None
                else seeds.EntropyInterface.NONE
            ),
        ),
        probability_law=law,
        label="g7-fixture",
    )
    return (
        ca.SimpleProgram(
            seeds.exact(
                configuration,
                value_profile=alphabet.value_profile,
            ),
            alphabet,
            writable,
            readable,
            rule,
        ),
        configuration,
    )


def native_program(
    case_id: str,
) -> tuple[ca.SimpleProgram, loci.FiniteConfiguration, tuple[Semantic, ...]]:
    """Return one of the six retained-native one-step oracle fixtures."""

    boundary = loci.Boundary(loci.BoundaryPolicy.FIXED, False)
    if case_id == "ar2":
        source = loci.record_configuration((("previous", 3), ("current", 5)))
        alphabet = alphabets.modular(97)
        neighborhood = neighborhoods.ar2_0d(
            configuration_contract=source.contract,
            value_profile=alphabets.ValueProfile.INTEGER,
        )
        rule = rules.ar2_modular_0d(rule=17)
        expected = (14, 5)
    elif case_id == "dyadlags":
        source = loci.history_configuration((True, False, False))
        alphabet = alphabets.boolean()
        neighborhood = neighborhoods.dyadlags_0d(
            configuration_contract=source.contract,
        )
        rule = rules.dyadlags_0d(rule=150)
        expected = (False, False, True)
    elif case_id == "lagcounts":
        source = loci.history_configuration(
            (True, False, True, True, False, False, True, False, True, True)
        )
        alphabet = alphabets.boolean()
        neighborhood = neighborhoods.lagcounts_0d(
            configuration_contract=source.contract,
        )
        rule = rules.lagcounts_0d(rule=91)
        expected = (
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            True,
            True,
            True,
        )
    elif case_id == "dyadrads":
        source = loci.grid_configuration(
            (5,),
            (True, False, True, False, False),
            boundary=boundary,
        )
        alphabet = alphabets.boolean()
        neighborhood = neighborhoods.dyadrads_1d(
            configuration_contract=source.contract,
        )
        rule = rules.dyadrads_1d(rule=30)
        expected = (False, True, False, True, True)
    elif case_id == "dyadaxes-2d":
        source = loci.grid_configuration(
            (3, 3),
            (True,) * 9,
            boundary=boundary,
        )
        alphabet = alphabets.boolean()
        neighborhood = neighborhoods.dyadaxes_2d(
            configuration_contract=source.contract,
        )
        rule = rules.dyadaxes_2d(rule=128)
        expected = (
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
        )
    elif case_id == "dyadaxes-3d":
        source = loci.grid_configuration(
            (3, 3, 3),
            (True,) * 27,
            boundary=boundary,
        )
        alphabet = alphabets.boolean()
        neighborhood = neighborhoods.dyadaxes_3d(
            configuration_contract=source.contract,
        )
        rule = rules.dyadaxes_3d(rule=128)
        expected = (
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
        )
    else:
        raise ValueError(case_id)

    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    simple_program = ca.SimpleProgram(
        seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet,
        writable,
        neighborhood,
        rule,
    )
    return simple_program, source, expected


def successor_values(
    result: program.ApplicationComplete,
) -> tuple[Semantic, ...]:
    assert result.successor_quotient_with_derivation_fibers.atoms
    successor = result.successor_quotient_with_derivation_fibers.atoms[0].successor
    assert isinstance(successor, loci.FiniteConfiguration)
    return tuple(value for _, value in successor.entries)


def diamond_program() -> tuple[
    ca.SimpleProgram,
    loci.FiniteConfiguration[Semantic],
]:
    def atoms(targets: tuple[loci.Locus, ...]):
        replacement = tuple(rules.replace(target, True) for target in targets)
        return (
            derivation("diamond-left", existing=replacement),
            derivation("diamond-right", existing=replacement),
        )

    return finite_record_program(
        (("cell", False),),
        atoms,
        probability=(Fraction(1, 3), Fraction(2, 3)),
    )


@dataclass(frozen=True)
class ClosedProbe:
    """A tiny closed value used only by descriptor-recursion tests."""

    name: str
    value: int
