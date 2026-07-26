"""Executable, code-shaped walkthrough of the ankos 0.2.0 API.

This is reference material, not package runtime code. It follows the public
construction order used by ``src/ca``:

    loci
    -> singular component values
    -> component composition
    -> SimpleProgram
    -> catalog constructors, presets, and aliases
    -> apply
    -> rollout
    -> canonical serialization

Run it from the repository root with:

    uv run python ref/notes/ca-scaffold.py

Every semantic value below comes from the live closed implementation. There
are no stand-in classes, callbacks, family registries, update-policy objects,
or alternate executors in this walkthrough.
"""

from __future__ import annotations

from dataclasses import fields
from fractions import Fraction
import inspect
import json

import ca


EXPECTED_ROOT = (
    "SimpleProgram",
    "apply",
    "rollout",
    "program",
    "catalog",
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "serialization",
)

CATALOG_NAMESPACES = (
    "entries",
    "automata",
    "substitua",
    "machina",
    "media",
    "criteria",
    "dynamica",
)


# ---------------------------------------------------------------------------
# 1. loci.py: structural identity before read or write authority
# ---------------------------------------------------------------------------


def binary_line_structure(
    width: int,
) -> tuple[
    ca.loci.CarrierContract,
    ca.loci.Region,
    ca.loci.Boundary[bool],
]:
    """Build closed carrier, support, and boundary values for one line."""

    carrier = ca.loci.CarrierContract(
        ca.loci.CarrierKind.GRID,
        rank=1,
        shape=(width,),
        axes=("x",),
    )
    support = ca.loci.literal(
        ca.loci.grid_loci((width,), axes=("x",)),
    )
    boundary = ca.loci.Boundary(
        ca.loci.BoundaryPolicy.FIXED,
        False,
    )
    return carrier, support, boundary


# A Region is only structural vocabulary. It grants neither observation nor
# mutation. The component owners below lift that vocabulary into authority.


# ---------------------------------------------------------------------------
# 2. Component modules: primitives -> compounds -> useful presets
# ---------------------------------------------------------------------------


def explicit_eca(
    *,
    number: int = 30,
    width: int = 79,
) -> ca.SimpleProgram:
    """Expand one ECA preset into the five ordinary component values."""

    carrier, support, boundary = binary_line_structure(width)

    # alphabets.py: one closed semantic value schema
    alphabet = ca.alphabets.boolean()

    # seeds.py: one closed source/law for initial configurations
    seed = ca.seeds.bernoulli(
        support,
        Fraction(1, 2),
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
        boundary=boundary,
    )

    # frontiers.py: the complete possible-write envelope
    frontier = ca.frontiers.everywhere(
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
    )

    # neighborhoods.py: the identity-preserving readable view
    neighborhood = ca.neighborhoods.eca(
        configuration_contract=carrier,
        value_profile=alphabet.value_profile,
    )

    # rules.py: applicability plus complete atomic replacement semantics
    rule = ca.rules.elementary(number)

    # program.py stores exactly these five values and validates their join.
    return ca.SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def demonstrate_component_composition(
    program: ca.SimpleProgram,
) -> None:
    """Show that composition still returns one value per component field."""

    product_alphabet = ca.alphabets.product(
        (program.alphabet, program.alphabet)
    )
    union_frontier = ca.frontiers.union(
        (program.frontier, program.frontier)
    )
    product_neighborhood = ca.neighborhoods.product(
        (
            ("first", program.neighborhood),
            ("second", program.neighborhood),
        )
    )
    parallel_rule = ca.rules.parallel((program.rule, program.rule))

    assert isinstance(product_alphabet, ca.alphabets.Alphabet)
    assert isinstance(union_frontier, ca.frontiers.WritableRegion)
    assert isinstance(product_neighborhood, ca.neighborhoods.ReadableRegion)
    assert isinstance(parallel_rule, ca.rules.Rule)


# ---------------------------------------------------------------------------
# 3. program.py: one immutable value and one family-blind application law
# ---------------------------------------------------------------------------


def demonstrate_application() -> ca.program.ApplicationComplete:
    """Apply one expanded program and retain its full result algebra."""

    program = explicit_eca(number=30, width=5)
    configuration = ca.loci.grid_configuration(
        (5,),
        (False, False, True, False, False),
        boundary=ca.loci.Boundary(
            ca.loci.BoundaryPolicy.FIXED,
            False,
        ),
    )

    result = ca.apply(program, configuration)
    assert isinstance(result, ca.program.ApplicationComplete)
    assert len(result.successor_quotient_with_derivation_fibers.atoms) == 1

    successor_group = (
        result.successor_quotient_with_derivation_fibers.atoms[0]
    )
    assert successor_group.derivations
    assert successor_group.successor != configuration
    return result


# ---------------------------------------------------------------------------
# 4. catalog/: canonical families -> presets -> aliases -> one qualified K
# ---------------------------------------------------------------------------


def demonstrate_catalog() -> ca.SimpleProgram:
    """Show that catalog spellings expand before identity or execution."""

    expanded = explicit_eca(number=30, width=5)
    qualified = ca.catalog.automata.eca(rule=30, width=5)
    convenient = ca.catalog.eca(rule=30, width=5)
    true_alias = ca.catalog.elementary_cellular_automaton(
        rule=30,
        width=5,
    )

    assert expanded == qualified == convenient == true_alias
    assert (
        expanded.canonical_identity
        == qualified.canonical_identity
        == convenient.canonical_identity
        == true_alias.canonical_identity
    )

    # Metadata is immutable, callable-free navigation—not a registry.
    entries = ca.catalog.entries
    assert len(entries.FAMILY_ENTRIES) == 60
    assert len(entries.ROLE_ENTRIES) == 2
    assert len(entries.LEGACY_ENTRIES) == 45
    assert len(entries.NAME_ENTRIES) == 105
    assert {
        kind: sum(entry.kind == kind for entry in entries.NAME_ENTRIES)
        for kind in ("C", "P", "A", "K")
    } == {"C": 60, "P": 40, "A": 4, "K": 1}

    # The sole K is deliberately category-qualified and not a flat export.
    assert hasattr(ca.catalog.machina, "extended_mobile_automaton")
    assert "extended_mobile_automaton" not in ca.catalog.__all__
    assert tuple(ca.catalog.__all__[:7]) == CATALOG_NAMESPACES
    assert len(ca.catalog.__all__) == 111
    return convenient


# ---------------------------------------------------------------------------
# 5. program.py rollout: traversal only through the owned apply operation
# ---------------------------------------------------------------------------


def demonstrate_rollout(
    program: ca.SimpleProgram,
) -> ca.program.RolloutTruncated:
    """Realize the Seed reproducibly and retain a typed depth truncation."""

    episode = ca.rollout(
        program,
        steps=2,
        replay_key=1234,
    )
    assert isinstance(episode, ca.program.RolloutTruncated)
    assert episode.cause is ca.program.TruncationCause.DEPTH_BOUND
    assert len(episode.raw_trace.applications.atoms) == 2
    assert len(episode.continuing_leaves.atoms) == 1
    return episode


# ---------------------------------------------------------------------------
# 6. serialization.py: one closed registry, expanded five-key program payload
# ---------------------------------------------------------------------------


def demonstrate_serialization(
    program: ca.SimpleProgram,
    application: ca.program.ApplicationComplete,
    episode: ca.program.RolloutTruncated,
) -> None:
    """Round-trip programs and other registered semantic records."""

    encoded_program = ca.serialization.dumps(program)
    envelope = json.loads(encoded_program)
    assert envelope["tag"] == "ca.simple-program"
    assert envelope["version"] == 1
    assert set(envelope["payload"]) == {
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    }

    decoded_program = ca.serialization.loads(encoded_program)
    assert decoded_program == ca.serialization.Decoded(program)
    assert ca.serialization.dumps(decoded_program.value) == encoded_program

    for value in (application, episode):
        encoded = ca.serialization.dumps(value)
        decoded = ca.serialization.loads(encoded)
        assert decoded == ca.serialization.Decoded(value)
        assert ca.serialization.dumps(decoded.value) == encoded


# ---------------------------------------------------------------------------
# 7. ca.__init__: small façade; details remain under their owners
# ---------------------------------------------------------------------------


def verify_public_surface() -> None:
    """Pin the implemented root spellings and operation signatures."""

    assert tuple(ca.__all__) == EXPECTED_ROOT
    assert tuple(field.name for field in fields(ca.SimpleProgram)) == (
        "seed",
        "alphabet",
        "frontier",
        "neighborhood",
        "rule",
    )
    assert tuple(inspect.signature(ca.apply).parameters) == (
        "program",
        "input",
    )
    assert tuple(inspect.signature(ca.rollout).parameters) == (
        "program",
        "steps",
        "initial",
        "replay_key",
    )

    # Component and whole-program meanings stay visually distinct.
    assert callable(ca.neighborhoods.eca)
    assert callable(ca.catalog.eca)
    assert not hasattr(ca, "eca")


def main() -> None:
    """Run the complete implemented-API walkthrough."""

    verify_public_surface()
    catalog_program = demonstrate_catalog()
    demonstrate_component_composition(catalog_program)
    application = demonstrate_application()
    episode = demonstrate_rollout(catalog_program)
    demonstrate_serialization(catalog_program, application, episode)
    print("ca-scaffold: ok")


if __name__ == "__main__":
    main()
