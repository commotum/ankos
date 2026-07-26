"""Closed representative values for the exhaustive G7-03 codec contract.

The mechanics ledger already supplies the richest realistic object graphs in
the suite.  This module traverses those graphs and a deliberately small set of
codec-only edge fixtures, then selects one valid instance of every registered
record type.  Enum coverage is stronger: every member is included.

Nothing here is a production registry or constructor fallback.  The helper is
test-owned, imports only semantic owners, and fails if a newly sealed type has
no intentional representative.
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
import importlib
from types import ModuleType

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules, seeds

from g7_mechanics import MECHANICS_ROWS, run_mechanics_fixture


OWNER_NAMES = (
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "program",
)


def owner_modules() -> tuple[ModuleType, ...]:
    return tuple(importlib.import_module(f"ca.{name}") for name in OWNER_NAMES)


def public_sealed_types() -> tuple[type[object], ...]:
    result: list[type[object]] = []
    for module in owner_modules():
        for name, value in vars(module).items():
            if (
                name.startswith("_")
                or not isinstance(value, type)
                or value.__module__ != module.__name__
            ):
                continue
            parameters = getattr(value, "__dataclass_params__", None)
            if issubclass(value, Enum) or (
                is_dataclass(value)
                and parameters is not None
                and parameters.frozen
            ):
                result.append(value)
    return tuple(result)


def _certificate(
    kind: rules.CertificateKind = rules.CertificateKind.CONFORMANCE,
    label: str = "codec-sample",
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _seed_samples(
    source: loci.FiniteConfiguration[bool],
) -> tuple[object, ...]:
    history = loci.history_configuration((True, False))
    contract = history.contract
    selector = loci.selector_literal(history.entries[0][0])
    left = seeds.sequence((True, False))
    right = seeds.sequence((False, True))
    bernoulli = seeds.bernoulli(
        loci.literal(tuple(target for target, _ in history.entries)),
        Fraction(1, 3),
        configuration_contract=contract,
    )
    uniform = seeds.uniform_bits(
        length=len(source.entries),
        configuration_contract=contract,
        reject_all_zero=True,
    )
    intensional_law = seeds.IntensionalProbabilityLaw("x", selector)
    intensional_contract = loci.CarrierContract(loci.CarrierKind.INTENSIONAL)
    return (
        seeds.exact(history),
        seeds.constructive(
            seeds.Construction(seeds.ConstructionOp.FILL, (True,)),
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        seeds.partial(
            history,
            unresolved=(history.entries[0][0],),
            obligations=(selector,),
            configuration_contract=contract,
            value_profile=alphabets.ValueProfile.BOOLEAN,
        ),
        bernoulli,
        uniform,
        seeds.law(
            intensional_law,
            configuration_contract=intensional_contract,
            value_profile=alphabets.ValueProfile.SYMBOLIC,
            exactness_profile=seeds.ExactnessProfile.SYMBOLIC,
        ),
        seeds.intensional(
            "x",
            selector,
            configuration_contract=intensional_contract,
            value_profile=alphabets.ValueProfile.SYMBOLIC,
        ),
        seeds.product((("left", left), ("right", right))),
        seeds.overlay((left, right), conflict=seeds.OverlayConflict.LEFT),
        seeds.mixture(
            ((Fraction(1, 3), left), (Fraction(2, 3), right))
        ),
        seeds.product_law((("left", uniform), ("right", uniform))),
        seeds.refine(left, selector),
        bernoulli.denote(),
        uniform.denote(),
    )


def _resolved_samples() -> tuple[object, ...]:
    source = loci.record_configuration((("a", True), ("b", False)))
    a, b = tuple(target for target, _ in source.entries)
    reference = loci.fresh_reference(
        "codec-children",
        "child",
        parent=a,
        interface_loci=(a, b),
    )
    writable = frontiers.union(
        (
            frontiers.literal(
                (a, b),
                configuration_contract=source.contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
                effects=(frontiers.Effect.REPLACE, frontiers.Effect.DELETE),
                frame=frontiers.WriteFrame.CURRENT,
            ),
            frontiers.fresh(
                loci.literal(fresh=(reference,)),
                namespace=frontiers.FreshNamespace("codec-children", a),
                configuration_contract=source.contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
        )
    ).resolve(source)

    fixed = loci.grid_configuration(
        (2,),
        (False, True),
        boundary=loci.Boundary(loci.BoundaryPolicy.FIXED, False),
    )
    open_grid = loci.grid_configuration(
        (2,),
        (False, True),
        boundary=loci.Boundary(loci.BoundaryPolicy.NONE),
    )
    fixed_view = neighborhoods.eca(
        configuration_contract=fixed.contract
    ).resolve(fixed)
    absent_view = neighborhoods.eca(
        configuration_contract=open_grid.contract
    ).resolve(open_grid)

    relation = loci.selector_tagged("codec-intensional")
    intensional_contract = loci.CarrierContract(
        loci.CarrierKind.INTENSIONAL
    )
    intensional_configuration = loci.IntensionalConfiguration(
        intensional_contract,
        relation,
        "codec-intensional-identity",
    )
    intensional_read = neighborhoods.intensional(
        "x",
        relation,
        configuration_contract=intensional_contract,
        value_profile=alphabets.ValueProfile.SYMBOLIC,
        exactness_profile=seeds.ExactnessProfile.SYMBOLIC,
    ).resolve(intensional_configuration)
    intensional_write = frontiers.intensional(
        "x",
        relation,
        configuration_contract=intensional_contract,
        value_profile=alphabets.ValueProfile.SYMBOLIC,
    ).resolve(intensional_configuration)

    structural = loci.FiniteConfiguration(
        source.carrier,
        source.entries,
        (
            loci.StructuralRelation("edge", (a, b)),
            loci.StructuralRelation("weight", (Fraction(2, 3),)),
        ),
    )
    dynamic = loci.fresh_children_dynamic(
        loci.literal((a, b)),
        "codec-dynamic",
        ("left", "right"),
    )
    dependency = neighborhoods.ReadDependency(
        "codec-dependency",
        loci.literal((a,)),
        loci.selector_literal(a),
        seeds.ExactnessProfile.EXACT,
    )
    value_anchor = alphabets.ValueAnchor(
        alphabets.value_tagged("head"),
        alphabets.AnchorCardinality.ZERO_OR_MORE,
    )
    return (
        source,
        structural,
        dynamic,
        writable,
        fixed_view,
        absent_view,
        intensional_configuration,
        intensional_read,
        intensional_write,
        dependency,
        value_anchor,
        neighborhoods.ReadableField(
            "field",
            neighborhoods.global_view(
                configuration_contract=source.contract,
                value_profile=alphabets.ValueProfile.BOOLEAN,
            ),
        ),
        *_seed_samples(source),
    )


def _exact_value_samples() -> tuple[object, ...]:
    sqrt_two = alphabets.AlgebraicNumber(
        (1, 0, -2),
        (Fraction(1), Fraction(2)),
    )
    fresh = loci.fresh_reference("codec", Fraction(2, 3))
    represented = tuple(
        alphabets.RepresentedNumber(profile, representation)
        for profile, representation in (
            (alphabets.RepresentedNumberProfile.DECIMAL, "0.125"),
            (alphabets.RepresentedNumberProfile.FIXED_POINT, Fraction(1, 8)),
            (alphabets.RepresentedNumberProfile.IEEE754_BINARY32, 0x3E000000),
            (
                alphabets.RepresentedNumberProfile.IEEE754_BINARY64,
                0x3FC0000000000000,
            ),
            (
                alphabets.RepresentedNumberProfile.INTERVAL,
                (Fraction(1, 8), Fraction(1, 4)),
            ),
        )
    )
    return (
        sqrt_two,
        alphabets.ExactComplex(sqrt_two, Fraction(-1, 3)),
        alphabets.StructuralReference(loci.named("codec-reference")),
        alphabets.StructuralReference(fresh),
        *represented,
    )


def _rule_samples() -> tuple[object, ...]:
    expression = rules.literal_expr("codec")
    conformance = _certificate()
    cardinality = _certificate(
        rules.CertificateKind.CARDINALITY,
        "codec-cardinality",
    )
    composition = _certificate(
        rules.CertificateKind.COMPOSITION,
        "codec-projection",
    )
    unknown = rules.Undetermined(expression, cardinality)
    support = rules.intensional_support(
        expression,
        unknown,
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "codec-complete",
        ),
        soundness_evidence=_certificate(
            rules.CertificateKind.SOUNDNESS,
            "codec-sound",
        ),
    )
    outcome = rules.OutcomeSpace(
        support,
        projection_cardinalities=rules.ProjectionCardinalities(
            unknown,
            rules.finite_cardinality(0),
            unknown,
            composition,
        ),
    )
    literal_rule = rules.literal(
        outcome,
        contract=rules.RuleContract(
            loci.CarrierContract(loci.CarrierKind.INTENSIONAL),
            alphabets.ValueProfile.SYMBOLIC,
            neighborhoods.ResultShape(
                (
                    neighborhoods.ReadField(
                        "intensional",
                        neighborhoods.ReadArity.INTENSIONAL,
                    ),
                )
            ),
            neighborhoods.JoinShape(
                neighborhoods.JoinMode.GLOBAL,
                ("target", "channel"),
            ),
            frontiers.EffectProfile(),
            exactness_profile=seeds.ExactnessProfile.SYMBOLIC,
        ),
    )
    existing_plan = rules.ExistingPlan(
        rules.ExistingPlanKind.BY_INDEX,
        (rules.literal_expr(True),),
    )
    evidence_term = rules.EvidenceTerm(
        "codec-term",
        (
            rules.EvidenceExpression(
                expression,
                rules.EvaluationScope.EACH_TARGET,
            ),
            rules.FormattedEvidence("{}", expression),
        ),
    )
    expression_rule = rules.expression(
        existing_plan,
        contract=rules.RuleContract(
            loci.CarrierContract(
                loci.CarrierKind.HISTORY,
                rank=1,
                shape=(1,),
                axes=("history",),
            ),
            alphabets.ValueProfile.BOOLEAN,
            neighborhoods.ResultShape(
                (neighborhoods.ReadField("self", neighborhoods.ReadArity.ONE),)
            ),
            neighborhoods.JoinShape(
                neighborhoods.JoinMode.ANCHOR_IDENTITY,
                ("target", "channel"),
            ),
            frontiers.EffectProfile(),
        ),
        progress=rules.Progress.ADVANCED,
        continuation=rules.Continue(),
        witness=expression,
        provenance=("codec:expression",),
        certificate=conformance,
        certificate_template=evidence_term,
        provenance_templates=(
            rules.ProvenanceTemplate("codec:{0}", (expression,)),
        ),
    )
    rejected = rules.RuleRejected(
        rules.RuleFault(
            rules.RuleFaultPhase.DENOTATION,
            rules.RuleFaultReason.INVALID_DESCRIPTOR,
            (conformance,),
            "codec rejection",
        )
    )
    return (
        unknown,
        outcome,
        literal_rule,
        expression_rule,
        rules.parallel((expression_rule, expression_rule)),
        existing_plan,
        evidence_term,
        rules.EvaluationProof(
            (
                rules.EvaluationStep(
                    expression,
                    None,
                    "codec",
                    ("codec-read",),
                ),
            )
        ),
        rules.RuleComplete(outcome),
        rejected,
    )


def _program_samples() -> tuple[object, ...]:
    execution = run_mechanics_fixture(MECHANICS_ROWS[0])
    simple_program = execution.simple_program
    source = execution.source
    application = execution.result
    rollout = ca.rollout(
        simple_program,
        steps=1,
        initial=source,
        replay_key="codec-replay",
    )
    zero_step = ca.rollout(simple_program, steps=0, initial=source)
    rejected = ca.rollout(simple_program, steps=-1)
    assert isinstance(application, program.ApplicationComplete)
    assert isinstance(rollout, program.RolloutTruncated)
    assert isinstance(zero_step, program.RolloutTruncated)
    assert isinstance(rejected, program.RolloutRejected)

    applied = next(
        atom
        for atom in application.applied_atoms.atoms
        if isinstance(atom, program.AppliedDerivation)
    )
    closed = program.ClosedLeaf(applied.successor, applied)
    complete = program.RolloutComplete(
        rollout.raw_trace,
        rules.finite_support((closed,), label="codec-closed"),
    )
    fault = program.ApplicationFault(
        program.ApplicationPhase.INPUT,
        "codec application rejection",
        ("codec-evidence",),
        (program.ApplicationPhase.PROGRAM, program.ApplicationPhase.INPUT),
    )
    compatibility = program._require_compatible_five_fields(simple_program)
    draw = program.DrawEvidence(
        "law",
        "application",
        "replay-key",
        "subkey",
        ("codec", "draw"),
        program.SamplerProfile.SHA256_REJECTION_V1,
        program.NumericProfile.FRACTION_TICKETS_V1,
        "witness",
        0,
    )
    seed_evidence = program.SeedRealizationEvidence(
        "seed-source",
        "replay-key",
        loci.configuration_identity(source),
        simple_program.seed.denote(),
        (draw,),
    )
    return (
        compatibility,
        program.ApplicationInput(
            source,
            program.TraceLineage("codec-root"),
        ),
        fault,
        program.ApplicationRejected(fault),
        rollout,
        zero_step,
        complete,
        closed,
        rejected,
        draw,
        seed_evidence,
        program.MeasureUnavailable(
            "codec-intensional-measure",
            ("source-law-retained", "mapping-retained"),
        ),
        program.RolloutFault("codec fault", ("codec evidence",)),
    )


def _walk_registered(
    value: object,
    registered: frozenset[type[object]],
    selected: dict[type[object], object],
    visited: set[int],
) -> None:
    identity = id(value)
    if identity in visited:
        return
    visited.add(identity)
    value_type = type(value)
    if value_type in registered:
        selected.setdefault(value_type, value)
    if isinstance(value, Enum):
        return
    if is_dataclass(value):
        for field in fields(value):
            _walk_registered(
                getattr(value, field.name),
                registered,
                selected,
                visited,
            )
        return
    if isinstance(value, tuple):
        for item in value:
            _walk_registered(item, registered, selected, visited)


def representative_values() -> tuple[object, ...]:
    """Return one record of each sealed type plus every enum member."""

    registered = frozenset(public_sealed_types())
    selected: dict[type[object], object] = {}
    visited: set[int] = set()
    roots = (
        *(run_mechanics_fixture(row) for row in MECHANICS_ROWS),
        *_resolved_samples(),
        *_exact_value_samples(),
        *_rule_samples(),
        *_program_samples(),
    )
    for root in roots:
        _walk_registered(root, registered, selected, visited)

    enum_types = tuple(
        value for value in registered if issubclass(value, Enum)
    )
    record_types = registered.difference(enum_types)
    missing = tuple(
        sorted(
            (
                f"{value.__module__}.{value.__name__}"
                for value in record_types.difference(selected)
            )
        )
    )
    if missing:
        raise AssertionError(
            "codec sample graph is missing sealed records: "
            + ", ".join(missing)
        )

    records = tuple(
        selected[value]
        for value in sorted(
            record_types,
            key=lambda item: (item.__module__, item.__name__),
        )
    )
    enum_members = tuple(
        member
        for value in sorted(
            enum_types,
            key=lambda item: (item.__module__, item.__name__),
        )
        for member in value
    )
    return (*records, *enum_members)


__all__ = [
    "OWNER_NAMES",
    "owner_modules",
    "public_sealed_types",
    "representative_values",
]
