"""CT12: independent retained-native and generic one-step equivalence."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

import ca
from ca import alphabets, frontiers, loci, neighborhoods, program, rules

import test_oracles
from g7_fixtures import native_program, successor_values
from g7_mechanics import runtime_ct12_fixture
from helpers import assert_closed_descriptor, assert_full_application_equal


NATIVE_CASES = (
    "ar2",
    "dyadlags",
    "lagcounts",
    "dyadrads",
    "dyadaxes-2d",
    "dyadaxes-3d",
)

ORACLE_CASE_IDS = {
    "ar2": "native.scalar.ar2-modular",
    "dyadlags": "native.temporal.dyadlags-rule-150",
    "lagcounts": "native.temporal.lagcounts-rule-91",
    "dyadrads": "native.cellular.dyadrads-rule-30",
    "dyadaxes-2d": "native.multidimensional.dyadaxes-2d-rule-128",
    "dyadaxes-3d": "native.multidimensional.dyadaxes-3d-rule-128",
}

_ORACLES_BY_ID = {case.case_id: case for case in test_oracles.CT12_CASES}
assert len(_ORACLES_BY_ID) == len(test_oracles.CT12_CASES)
ORACLE_CASES = {
    case_id: _ORACLES_BY_ID[oracle_id]
    for case_id, oracle_id in ORACLE_CASE_IDS.items()
}


def _term(
    tag: str,
    *arguments: test_oracles.OracleValue,
) -> test_oracles.OracleTerm:
    return test_oracles.OracleTerm(tag, arguments)


def _oracle_scalar(value: object) -> test_oracles.OracleScalar:
    if type(value) is bool:
        return int(value)
    assert value is None or type(value) in (int, Fraction, str)
    return value


def _rule_expr_as_oracle_term(
    expression: rules.RuleExpr,
) -> test_oracles.OracleValue:
    if expression.primitive is rules.ExpressionPrimitive.LITERAL:
        assert len(expression.arguments) == 1
        value = expression.arguments[0]
        assert not isinstance(value, rules.RuleExpr)
        return _oracle_scalar(value)
    assert expression.primitive is rules.ExpressionPrimitive.TUPLE
    converted = tuple(
        _rule_expr_as_oracle_term(argument)
        for argument in expression.arguments
        if isinstance(argument, rules.RuleExpr)
    )
    assert len(converted) == len(expression.arguments)
    assert converted and isinstance(converted[0], str)
    return _term(converted[0], *converted[1:])


def _literal_value(expression: rules.RuleExpr) -> object:
    assert expression.primitive is rules.ExpressionPrimitive.LITERAL
    assert len(expression.arguments) == 1
    value = expression.arguments[0]
    assert not isinstance(value, rules.RuleExpr)
    return value


EvaluationFact = tuple[
    str,
    rules.RuleExpr,
    test_oracles.OracleValue | tuple[test_oracles.OracleValue, ...],
    tuple[str, ...],
]


def _evaluated_value(
    expression: rules.RuleExpr,
) -> test_oracles.OracleValue | tuple[test_oracles.OracleValue, ...]:
    if expression.primitive is rules.ExpressionPrimitive.LITERAL:
        return _oracle_scalar(_literal_value(expression))
    assert expression.primitive is rules.ExpressionPrimitive.TUPLE
    return tuple(
        _evaluated_value(argument)
        for argument in expression.arguments
        if isinstance(argument, rules.RuleExpr)
    )


def _evaluation_facts(
    expression: rules.RuleExpr,
    readable: neighborhoods.ReadableView,
    writable_targets: tuple[loci.Locus, ...],
) -> tuple[EvaluationFact, ...]:
    assert expression.primitive is rules.ExpressionPrimitive.TUPLE
    assert expression.arguments
    head = expression.arguments[0]
    assert isinstance(head, rules.RuleExpr)
    assert _literal_value(head) == "evaluation-proof-v1"
    assert len(expression.arguments) > 1
    allowed_reads = {
        loci.canonical_identity(
            (item.target, loci.canonical_identity(item.state))
        )
        for item in readable.observations
    }
    allowed_anchors = {
        "none",
        *(loci.canonical_identity(target) for target in writable_targets),
    }
    facts: list[EvaluationFact] = []
    saw_read = False
    for step in expression.arguments[1:]:
        assert isinstance(step, rules.RuleExpr)
        assert step.primitive is rules.ExpressionPrimitive.TUPLE
        assert len(step.arguments) == 5
        tag, anchor, evaluated_expression, result, reads = step.arguments
        assert isinstance(tag, rules.RuleExpr)
        assert _literal_value(tag) == "step"
        assert isinstance(anchor, rules.RuleExpr)
        anchor_identity = _literal_value(anchor)
        assert type(anchor_identity) is str
        assert anchor_identity in allowed_anchors
        assert isinstance(evaluated_expression, rules.RuleExpr)
        assert isinstance(result, rules.RuleExpr)
        assert isinstance(reads, rules.RuleExpr)
        assert reads.primitive is rules.ExpressionPrimitive.TUPLE
        assert reads.arguments
        read_tag = reads.arguments[0]
        assert isinstance(read_tag, rules.RuleExpr)
        assert _literal_value(read_tag) == "read-evidence"
        read_identities: list[str] = []
        for read in reads.arguments[1:]:
            assert isinstance(read, rules.RuleExpr)
            read_identity = _literal_value(read)
            assert type(read_identity) is str
            assert read_identity in allowed_reads
            read_identities.append(read_identity)
            saw_read = True
        facts.append(
            (
                anchor_identity,
                evaluated_expression,
                _evaluated_value(result),
                tuple(read_identities),
            )
        )
    assert saw_read
    return tuple(facts)


def _single_results_by_observation(
    facts: tuple[EvaluationFact, ...],
) -> dict[int, test_oracles.OracleValue]:
    results: dict[int, set[test_oracles.OracleValue]] = {}
    for _, expression, result, _ in facts:
        if expression.primitive is not rules.ExpressionPrimitive.OBSERVATION:
            continue
        assert len(expression.arguments) == 1
        index = expression.arguments[0]
        assert type(index) is int
        assert not isinstance(result, tuple)
        results.setdefault(index, set()).add(result)
    assert all(len(values) == 1 for values in results.values())
    return {index: next(iter(values)) for index, values in results.items()}


def _single_results_by_counted_group(
    facts: tuple[EvaluationFact, ...],
) -> dict[int, int]:
    results: dict[int, set[int]] = {}
    for _, expression, result, _ in facts:
        if expression.primitive is not rules.ExpressionPrimitive.COUNT:
            continue
        assert len(expression.arguments) == 1
        group = expression.arguments[0]
        assert isinstance(group, rules.RuleExpr)
        assert group.primitive is rules.ExpressionPrimitive.GROUP
        assert len(group.arguments) == 1
        channel = group.arguments[0]
        assert type(channel) is int
        assert type(result) is int
        results.setdefault(channel, set()).add(result)
    assert all(len(values) == 1 for values in results.values())
    return {channel: next(iter(values)) for channel, values in results.items()}


def _results_for_expression(
    facts: tuple[EvaluationFact, ...],
    expression: rules.RuleExpr,
) -> tuple[tuple[str, test_oracles.OracleValue], ...]:
    selected = {
        (anchor, result)
        for anchor, evaluated, result, _ in facts
        if evaluated == expression and not isinstance(result, tuple)
    }
    assert selected
    return tuple(sorted(selected))


def _configuration_as_oracle(
    case_id: str,
    actual: loci.FiniteConfiguration,
) -> test_oracles.OracleTerm:
    if case_id == "ar2":
        assert actual.contract.kind is loci.CarrierKind.RECORD
        fields = {
            str(target.path[-1]): _oracle_scalar(value)
            for target, value in actual.entries
        }
        assert set(fields) == {"previous", "current"}
        return _term(
            "configuration.record",
            _term("field-value", "previous", fields["previous"]),
            _term("field-value", "current", fields["current"]),
        )

    if case_id in ("dyadlags", "lagcounts"):
        assert actual.contract.kind is loci.CarrierKind.HISTORY
        indexed = {
            int(target.path[-1]): _oracle_scalar(value)
            for target, value in actual.entries
        }
        assert set(indexed) == set(range(len(indexed)))
        return _term(
            "history",
            _term(
                "values",
                *(indexed[index] for index in range(len(indexed))),
            ),
        )

    assert actual.contract.kind is loci.CarrierKind.GRID
    assert actual.contract.shape is not None
    boundary = actual.carrier.boundary
    assert boundary.policy is loci.BoundaryPolicy.FIXED
    default = _oracle_scalar(boundary.exterior)
    assert default == 0
    values = {
        loci.grid_coordinates(target): _oracle_scalar(value)
        for target, value in actual.entries
    }
    axes = tuple(
        loci.centered_axis_values(size)
        for size in actual.contract.shape
    )
    if case_id == "dyadrads":
        assert actual.contract.shape == (5,)
        return _term(
            "line1d",
            _term("topology", "finite-line", 5),
            _term("default", default),
            _term("values", *(values[(x,)] for x in axes[0])),
        )
    if case_id == "dyadaxes-2d":
        assert actual.contract.shape == (3, 3)
        return _term(
            "grid2d",
            _term("topology", "finite-grid", 3, 3),
            _term("default", default),
            *(
                _term("row", *(values[(x, y)] for y in axes[1]))
                for x in axes[0]
            ),
        )
    assert case_id == "dyadaxes-3d"
    assert actual.contract.shape == (3, 3, 3)
    return _term(
        "grid3d",
        _term("topology", "finite-grid", 3, 3, 3),
        _term("default", default),
        *(
            _term(
                "layer",
                *(
                    _term(
                        "row",
                        *(values[(x, y, z)] for z in axes[2]),
                    )
                    for y in axes[1]
                ),
            )
            for x in axes[0]
        ),
    )


def _target_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    target: loci.Locus,
) -> test_oracles.OracleTerm:
    if case_id == "ar2":
        assert target.kind is loci.LocusKind.NAMED
        assert target.scope == "record"
        return _term("field", str(target.path[-1]))
    if case_id in ("dyadlags", "lagcounts"):
        assert target.kind is loci.LocusKind.OCCURRENCE
        assert target.path[0] == "history"
        index = int(target.path[-1])
        if case_id == "dyadlags":
            role = {0: "older", 1: "previous", 2: "current"}[index]
            return _term("history-slot", role)
        return _term("history-index", index)

    coordinates = loci.grid_coordinates(target)
    if case_id == "dyadrads":
        assert source.contract.shape == (5,)
        axis = loci.centered_axis_values(5)
        return _term("cell1d", axis.index(coordinates[0]))
    if case_id == "dyadaxes-2d":
        assert len(coordinates) == 2
        return _term("cell2d", *coordinates)
    assert case_id == "dyadaxes-3d"
    assert len(coordinates) == 3
    return _term("cell3d", *coordinates)


def _target_order_key(
    case_id: str,
    target: loci.Locus,
) -> tuple[int, ...]:
    if case_id == "ar2":
        return ({"previous": 0, "current": 1}[str(target.path[-1])],)
    if case_id in ("dyadlags", "lagcounts"):
        return (int(target.path[-1]),)
    return loci.grid_coordinates(target)


def _writable_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    writable: frontiers.WritableCapabilities,
) -> tuple[test_oracles.OracleTerm, ...]:
    assert writable.snapshot_identity == source.identity
    assert not writable.fresh
    assert tuple(item.target for item in writable.existing) == tuple(
        lens.target for lens in writable.reconstruction.lenses
    )
    ordered = sorted(
        writable.existing,
        key=lambda item: _target_order_key(case_id, item.target),
    )
    return tuple(
        _target_as_oracle(case_id, source, item.target)
        for item in ordered
    )


def _dispositions_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    actual: rules.TotalDisposition,
    writable_targets: tuple[loci.Locus, ...],
) -> tuple[test_oracles.OracleDisposition, ...]:
    assert {item.target for item in actual.existing} == set(writable_targets)
    normalized: list[test_oracles.OracleDisposition] = []
    ordered = sorted(
        actual.existing,
        key=lambda item: _target_order_key(case_id, item.target),
    )
    for item in ordered:
        payload = (
            _oracle_scalar(item.payload.value)
            if isinstance(item.payload, rules.ValuePayload)
            else None
        )
        normalized.append(
            test_oracles.OracleDisposition(
                _target_as_oracle(case_id, source, item.target),
                item.action.value,
                payload,
            )
        )
    assert not actual.fresh
    return tuple(normalized)


def _observation_value(
    observation: neighborhoods.Observation,
) -> test_oracles.OracleValue:
    assert not isinstance(observation.state, neighborhoods.Absent)
    return _oracle_scalar(observation.value)


def _readable_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    readable: neighborhoods.ReadableView,
) -> test_oracles.OracleTerm:
    assert readable.snapshot_identity == source.identity
    assert all(
        type(observation.target) is loci.Locus
        and not isinstance(observation.state, neighborhoods.Absent)
        for observation in readable.observations
    )
    if case_id == "ar2":
        fields = {
            str(observation.target.path[-1]): _observation_value(observation)
            for observation in readable.observations
        }
        assert set(fields) == {"previous", "current"}
        return _term(
            "read.record",
            _term("field-value", "previous", fields["previous"]),
            _term("field-value", "current", fields["current"]),
        )
    if case_id == "dyadlags":
        indexed = {
            int(observation.target.path[-1]): _observation_value(observation)
            for observation in readable.observations
        }
        assert set(indexed) == {0, 1, 2}
        return _term(
            "temporal-lag-view",
            _term("values", *(indexed[index] for index in range(3))),
        )
    if case_id == "lagcounts":
        groups = {}
        for group in readable.groups:
            observations = sorted(
                (readable.observations[index] for index in group.indices),
                key=lambda observation: int(observation.target.path[-1]),
            )
            groups[group.key.channel] = tuple(
                _observation_value(observation)
                for observation in observations
            )
        assert set(groups) == {0, 1, 2, 3}
        assert tuple(map(len, (groups[0], groups[1], groups[2], groups[3]))) == (
            1,
            3,
            3,
            3,
        )
        return _term(
            "count-banded-history-view",
            _term("current", *groups[0]),
            _term("recent", *groups[1]),
            _term("middle", *groups[2]),
            _term("oldest", *groups[3]),
        )

    expected_sizes = {
        "dyadrads": (1, 2, 2),
        "dyadaxes-2d": (1, 4, 4),
        "dyadaxes-3d": (1, 6, 20),
    }[case_id]
    for target, _ in source.entries:
        groups = sorted(
            (
                group
                for group in readable.groups
                if group.key.anchor == target
            ),
            key=lambda group: group.key.channel,
        )
        assert tuple(group.key.channel for group in groups) == (0, 1, 2)
        assert tuple(len(group.indices) for group in groups) == expected_sizes
    source_term = _configuration_as_oracle(case_id, source)
    tag = {
        "dyadrads": "old-snapshot-stencils",
        "dyadaxes-2d": "old-snapshot-2d-stencils",
        "dyadaxes-3d": "old-snapshot-3d-stencils",
    }[case_id]
    return _term(tag, source_term)


def _static_witness_parts(
    expression: rules.RuleExpr,
) -> tuple[rules.RuleScalar | rules.RuleExpr, ...]:
    assert expression.primitive is rules.ExpressionPrimitive.TUPLE
    assert expression.arguments
    return expression.arguments


def _literal_part(
    parts: tuple[rules.RuleScalar | rules.RuleExpr, ...],
    index: int,
) -> test_oracles.OracleScalar:
    expression = parts[index]
    assert isinstance(expression, rules.RuleExpr)
    return _oracle_scalar(_literal_value(expression))


def _index_by_target(
    facts: tuple[EvaluationFact, ...],
    index_expression: rules.RuleExpr,
    targets: tuple[loci.Locus, ...],
) -> dict[loci.Locus, int]:
    target_by_anchor = {
        loci.canonical_identity(target): target for target in targets
    }
    results: dict[loci.Locus, set[int]] = {}
    for anchor, evaluated, result, _ in facts:
        if evaluated != index_expression:
            continue
        assert anchor in target_by_anchor
        assert type(result) is int
        results.setdefault(target_by_anchor[anchor], set()).add(result)
    assert set(results) == set(targets)
    assert all(len(values) == 1 for values in results.values())
    return {
        target: next(iter(values))
        for target, values in results.items()
    }


def _native_witness_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    static_witness: rules.RuleExpr,
    facts: tuple[EvaluationFact, ...],
    writable_targets: tuple[loci.Locus, ...],
) -> test_oracles.OracleTerm:
    parts = _static_witness_parts(static_witness)
    observations = _single_results_by_observation(facts)

    if case_id == "ar2":
        static = tuple(_literal_part(parts, index) for index in range(len(parts)))
        assert static == ("ar2-modular", 17, 2, 1, 1, 97)
        assert observations[0] == 3
        assert observations[1] == 5
        modulo_results = {
            result
            for _, expression, result, _ in facts
            if expression.primitive is rules.ExpressionPrimitive.MODULO
        }
        assert modulo_results == {14}
        return _term("witness.rule", "ar2-modular", "rule-id", 17)

    label = _literal_part(parts, 0)
    rule_number = _literal_part(parts, 1)
    index_expression = parts[2]
    assert isinstance(label, str)
    assert type(rule_number) is int
    assert isinstance(index_expression, rules.RuleExpr)

    if case_id == "dyadlags":
        assert (label, rule_number) == ("dyadlags-0d", 150)
        index_results = _results_for_expression(facts, index_expression)
        assert index_results == (("none", 4),)
        return _term(
            "lookup-witness",
            label,
            _term(
                "context",
                observations[0],
                observations[1],
                observations[2],
            ),
            _term("index", 4),
            _term("rule-id", rule_number),
        )

    if case_id == "lagcounts":
        assert (label, rule_number) == ("lagcounts-0d", 91)
        index_results = _results_for_expression(facts, index_expression)
        assert index_results == (("none", 77),)
        counts = _single_results_by_counted_group(facts)
        assert set(counts) >= {1, 2, 3}
        return _term(
            "count-band-witness",
            _term("current", observations[0]),
            _term("band-counts", counts[1], counts[2], counts[3]),
            _term("context", 77),
            _term("rule-id", rule_number),
        )

    indices = _index_by_target(facts, index_expression, writable_targets)
    if case_id == "dyadrads":
        assert (label, rule_number) == ("dyadrads-1d", 30)
        axis = loci.centered_axis_values(5)
        by_coordinate = {
            loci.grid_coordinates(target)[0]: value
            for target, value in indices.items()
        }
        ordered = tuple(by_coordinate[coordinate] for coordinate in axis)
        return _term(
            "lookup-witness",
            label,
            _term("indices", *ordered),
            _term("rule-id", rule_number),
        )
    if case_id == "dyadaxes-2d":
        assert (label, rule_number) == ("dyadaxes-2d", 128)
        by_coordinate = {
            loci.grid_coordinates(target): value
            for target, value in indices.items()
        }
        axis = loci.centered_axis_values(3)
        return _term(
            "lookup-witness",
            label,
            _term(
                "index-grid",
                *(
                    _term(
                        "row",
                        *(by_coordinate[(x, y)] for y in axis),
                    )
                    for x in axis
                ),
            ),
            _term("rule-id", rule_number),
        )

    assert case_id == "dyadaxes-3d"
    assert (label, rule_number) == ("dyadaxes-3d", 128)
    multiplicity = Counter(indices.values())
    assert set(multiplicity) == {1, 3, 7}
    return _term(
        "lookup-witness",
        label,
        _term(
            "index-multiplicity",
            _term("index", 7, multiplicity[7]),
            _term("index", 3, multiplicity[3]),
            _term("index", 1, multiplicity[1]),
        ),
        _term("rule-id", rule_number),
    )


def _cardinality_as_oracle(
    actual: rules.Cardinality,
) -> test_oracles.OracleCardinality:
    assert actual.evidence.kind is rules.CertificateKind.CARDINALITY
    assert actual.evidence.version == 1
    size = rules.cardinality_size(actual)
    if size is not None:
        return test_oracles.OracleCardinality("exact", size)
    assert isinstance(actual, rules.Many)
    assert actual.infinite is rules.InfiniteCardinality.UNCOUNTABLE
    return test_oracles.OracleCardinality("uncountable", None)


def _assert_support_evidence(support: rules.SupportSpace) -> None:
    assert support.version == 1
    assert (
        support.completeness_evidence.kind
        is rules.CertificateKind.COMPLETENESS
    )
    assert support.soundness_evidence.kind is rules.CertificateKind.SOUNDNESS
    assert support.completeness_evidence.version == 1
    assert support.soundness_evidence.version == 1


def _measure_as_oracle(
    actual: program.MeasureView,
) -> test_oracles.OracleMeasureView:
    assert isinstance(actual, program.MeasureAbsent)
    return test_oracles.OracleMeasureView("absent", (), None, None)


def _application_evidence_as_oracle(
    actual: program.ApplicationEvidence,
    *,
    oracle_case: test_oracles.OracleCase,
    simple_program: ca.SimpleProgram,
    source: loci.FiniteConfiguration,
    readable: neighborhoods.ReadableView,
    writable: frontiers.WritableCapabilities,
) -> test_oracles.OracleTerm:
    assert actual.phases == tuple(program.ApplicationPhase)
    runtime_identities = (
        actual.program_identity,
        actual.input_configuration_identity,
        actual.readable_binding_identity,
        actual.writable_binding_identity,
        actual.application_identity,
    )
    assert all(type(identity) is str and identity for identity in runtime_identities)
    assert actual.program_identity == simple_program.canonical_identity
    assert actual.input_configuration_identity == source.identity
    assert actual.readable_binding_identity == loci.canonical_identity(readable)
    assert actual.writable_binding_identity == loci.canonical_identity(writable)
    assert actual.application_identity == loci.canonical_identity(
        (
            simple_program.canonical_identity,
            source.identity,
            actual.readable_binding_identity,
            actual.writable_binding_identity,
        )
    )
    # The frozen oracle names an application semantically; runtime identity
    # fields are hashes.  Project only after validating every hashed field.
    return _term("application-evidence", oracle_case.case_id)


def _optional_relation_as_oracle(
    relation: rules.RuleExpr | None,
) -> test_oracles.OracleTerm | None:
    if relation is None:
        return None
    converted = _rule_expr_as_oracle_term(relation)
    assert isinstance(converted, test_oracles.OracleTerm)
    return converted


def _assert_complete_native_result(
    case_id: str,
    simple_program: ca.SimpleProgram,
    source: loci.FiniteConfiguration,
    actual: program.ApplicationComplete,
) -> test_oracles.OracleExpected:
    """Construct a complete oracle representation from runtime semantics."""

    oracle_case = ORACLE_CASES[case_id]
    assert _configuration_as_oracle(case_id, source) == oracle_case.source
    writable = simple_program.frontier.resolve(source)
    readable = simple_program.neighborhood.resolve(source)
    assert _writable_as_oracle(case_id, source, writable) == oracle_case.writable
    assert _readable_as_oracle(case_id, source, readable) == oracle_case.readable

    source_support = actual.source_outcomes.support
    assert source_support.presentation is rules.SupportPresentation.FINITE
    assert actual.source_outcomes.probability_law is None
    assert actual.source_outcomes.version == 1
    _assert_support_evidence(source_support)
    source_cardinality = _cardinality_as_oracle(source_support.cardinality)
    assert source_cardinality == _cardinality_as_oracle(
        actual.outcome_atom_cardinality
    )

    expected_by_witness = {
        atom.witness: atom for atom in oracle_case.expected.source_outcomes
    }
    assert len(expected_by_witness) == len(
        oracle_case.expected.source_outcomes
    )
    runtime_to_oracle_id: dict[str, str] = {}
    normalized_source_atoms: list[test_oracles.OracleSourceAtom] = []
    writable_targets = tuple(item.target for item in writable.existing)
    for runtime_atom in source_support.atoms:
        assert isinstance(runtime_atom, rules.Derivation)
        assert runtime_atom.version == 1
        assert runtime_atom.replacement.version == 1
        assert (
            runtime_atom.replacement.totality_evidence.kind
            is rules.CertificateKind.TOTALITY
        )
        assert runtime_atom.witness.version == 1
        assert runtime_atom.certificate.version == 1
        assert runtime_atom.certificate.kind is rules.CertificateKind.DERIVATION
        assert runtime_atom.witness.identity == loci.canonical_identity(
            runtime_atom.witness.descriptor
        )
        descriptor = runtime_atom.witness.descriptor
        assert descriptor.primitive is rules.ExpressionPrimitive.TUPLE
        assert len(descriptor.arguments) == 3
        static_witness, evaluation_proof, disposition_identity = (
            descriptor.arguments
        )
        assert isinstance(static_witness, rules.RuleExpr)
        assert isinstance(evaluation_proof, rules.RuleExpr)
        assert isinstance(disposition_identity, rules.RuleExpr)
        facts = _evaluation_facts(
            evaluation_proof,
            readable,
            writable_targets,
        )
        normalized_witness = _native_witness_as_oracle(
            case_id,
            source,
            static_witness,
            facts,
            writable_targets,
        )
        assert normalized_witness in expected_by_witness
        expected_atom = expected_by_witness[normalized_witness]
        runtime_identity = runtime_atom.canonical_identity
        assert runtime_identity not in runtime_to_oracle_id
        runtime_to_oracle_id[runtime_identity] = expected_atom.atom_id
        assert _rule_expr_as_oracle_term(disposition_identity) == (
            runtime_atom.replacement.canonical_identity
        )
        assert isinstance(runtime_atom.continuation, rules.Continue)
        assert runtime_atom.continuation.version == 1
        normalized_source_atoms.append(
            test_oracles.OracleSourceAtom(
                atom_id=expected_atom.atom_id,
                kind="derivation",
                witness=normalized_witness,
                provenance=runtime_atom.provenance,
                progress=runtime_atom.progress.value,
                continuation=_term("continue"),
                dispositions=_dispositions_as_oracle(
                    case_id,
                    source,
                    runtime_atom.replacement,
                    writable_targets,
                ),
                reason=None,
                certificate=_rule_expr_as_oracle_term(
                    runtime_atom.certificate.statement
                ),
                mass=None,
            )
        )
    normalized_source_atoms.sort(key=lambda atom: atom.atom_id)

    _assert_support_evidence(actual.applied_atoms)
    applied_cardinality = _cardinality_as_oracle(
        actual.applied_atoms.cardinality
    )
    derivation_cardinality = _cardinality_as_oracle(
        actual.derivation_cardinality
    )
    assert applied_cardinality == derivation_cardinality
    normalized_applied: list[test_oracles.OracleAppliedAtom] = []
    for runtime_applied in actual.applied_atoms.atoms:
        assert isinstance(runtime_applied, program.AppliedDerivation)
        source_identity = runtime_applied.source.canonical_identity
        assert source_identity in runtime_to_oracle_id
        oracle_atom_id = runtime_to_oracle_id[source_identity]
        assert not runtime_applied.fresh_bindings
        assert runtime_applied.evidence.version == 1
        assert type(runtime_applied.evidence.application_identity) is str
        assert type(runtime_applied.evidence.disposition_identity) is str
        assert runtime_applied.evidence.application_identity == (
            actual.evidence.application_identity
        )
        assert runtime_applied.evidence.disposition_identity == (
            runtime_applied.source.replacement.canonical_identity
        )
        direct_root = loci.canonical_identity(
            ("direct-application-root", source.identity)
        )
        assert runtime_applied.input_trace_lineage == program.TraceLineage(
            direct_root
        )
        assert runtime_applied.output_trace_lineage.root_identity == direct_root
        assert runtime_applied.output_trace_lineage.version == 1
        expected_edge = loci.canonical_identity(
            (
                loci.canonical_identity(program.TraceLineage(direct_root)),
                actual.evidence.application_identity,
                source_identity,
                runtime_applied.source.progress.value,
            )
        )
        assert runtime_applied.output_trace_lineage.path == (expected_edge,)
        normalized_applied.append(
            test_oracles.OracleAppliedAtom(
                atom_id=oracle_atom_id,
                source_atom_id=oracle_atom_id,
                successor=_configuration_as_oracle(
                    case_id,
                    runtime_applied.successor,
                ),
                fresh_bindings=(),
                output_trace_lineage=_term(
                    "lineage",
                    oracle_case.case_id,
                    oracle_atom_id,
                ),
                evidence=_term(
                    "applied-atom-evidence",
                    oracle_case.case_id,
                    oracle_atom_id,
                ),
            )
        )
    normalized_applied.sort(key=lambda atom: atom.atom_id)

    assert actual.no_successor_partition.atoms == ()
    _assert_support_evidence(actual.no_successor_partition)
    assert _cardinality_as_oracle(
        actual.no_successor_partition.cardinality
    ) == test_oracles.OracleCardinality("exact", 0)

    successor_support = actual.successor_quotient_with_derivation_fibers
    _assert_support_evidence(successor_support)
    successor_cardinality = _cardinality_as_oracle(
        actual.successor_cardinality
    )
    assert successor_cardinality == _cardinality_as_oracle(
        successor_support.cardinality
    )
    normalized_fibers: list[test_oracles.OracleFiber] = []
    for runtime_fiber in successor_support.atoms:
        atom_ids = tuple(
            runtime_to_oracle_id[item.source.canonical_identity]
            for item in runtime_fiber.derivations
        )
        normalized_fibers.append(
            test_oracles.OracleFiber(
                _configuration_as_oracle(
                    case_id,
                    runtime_fiber.successor,
                ),
                atom_ids,
            )
        )
    normalized_fibers.sort(
        key=lambda fiber: (repr(fiber.successor), fiber.atom_ids)
    )

    normalized_evidence = _application_evidence_as_oracle(
        actual.evidence,
        oracle_case=oracle_case,
        simple_program=simple_program,
        source=source,
        readable=readable,
        writable=writable,
    )
    return test_oracles.OracleExpected(
        support_kind="finite",
        source_outcomes=tuple(normalized_source_atoms),
        applied_atoms=tuple(normalized_applied),
        no_successor_partition=(),
        outcome_cardinality=source_cardinality,
        derivation_cardinality=derivation_cardinality,
        successor_cardinality=successor_cardinality,
        successor_fibers=tuple(normalized_fibers),
        measures=test_oracles.OracleMeasures(
            applied_atoms=_measure_as_oracle(actual.applied_atom_measure),
            successors=_measure_as_oracle(actual.successor_submeasure),
            no_successors=_measure_as_oracle(actual.no_successor_submeasure),
        ),
        source_intensional_relation=_optional_relation_as_oracle(
            source_support.relation
        ),
        applied_intensional_relation=_optional_relation_as_oracle(
            actual.applied_atoms.relation
        ),
        successor_intensional_relation=_optional_relation_as_oracle(
            successor_support.relation
        ),
        evidence=normalized_evidence,
    )


def test_reference_oracles_are_statically_independent_of_runtime_semantics() -> None:
    source = Path(test_oracles.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert not any(name == "ca" or name.startswith("ca.") for name in imported)
    assert not any(
        name == "ca" or (name is not None and name.startswith("ca."))
        for name in imported_from
    )
    assert called_names.isdisjoint({"apply", "rollout", "denote", "commit"})


@pytest.mark.parametrize("case_id", NATIVE_CASES)
def test_finite_native_fixtures_match_complete_generic_results(
    case_id: str,
) -> None:
    simple_program, source, expected = native_program(case_id)

    result = ca.apply(simple_program, source)

    assert isinstance(result, program.ApplicationComplete)
    assert successor_values(result) == expected
    assert_full_application_equal(
        _assert_complete_native_result(case_id, simple_program, source, result),
        ORACLE_CASES[case_id].expected,
    )


def _ct12_expression_as_oracle(
    expression: rules.RuleExpr,
) -> test_oracles.OracleValue:
    """Normalize closed fixture syntax without collapsing booleans to integers."""

    if expression.primitive is rules.ExpressionPrimitive.LITERAL:
        assert len(expression.arguments) == 1
        value = expression.arguments[0]
        assert type(value) in (bool, int, Fraction, str)
        return value
    assert expression.primitive is rules.ExpressionPrimitive.TUPLE
    converted = tuple(
        _ct12_expression_as_oracle(argument)
        for argument in expression.arguments
        if isinstance(argument, rules.RuleExpr)
    )
    assert len(converted) == len(expression.arguments)
    assert converted and isinstance(converted[0], str)
    return _term(converted[0], *converted[1:])


def _ct12_semantic_as_oracle(
    value: alphabets.SemanticValue,
) -> test_oracles.OracleValue:
    if type(value) in (bool, int, Fraction, str):
        return value
    assert isinstance(value, alphabets.ValueNode)
    assert not value.fields
    return _term(
        value.tag,
        *(_ct12_semantic_as_oracle(item) for item in value.items),
    )


def _ct12_fresh_target_as_oracle(
    case_id: str,
    reference: loci.FreshReference,
) -> test_oracles.OracleTerm:
    key = str(reference.local_key)
    if case_id == "px02.parallel-substitution":
        ordinal = {"old:0:0": 0, "old:0:1": 1}[key]
        return _term(
            "fresh-slot",
            "offspring",
            _term("occurrence", "old", 0),
            ordinal,
        )
    assert case_id == "px02.graph-interface-replacement"
    kind = "node" if key in {"x", "y"} else "edge"
    return _term("fresh-slot", kind, key)


def _ct12_target_as_oracle(
    case_id: str,
    target: loci.Locus | loci.FreshReference,
) -> test_oracles.OracleTerm:
    if isinstance(target, loci.FreshReference):
        return _ct12_fresh_target_as_oracle(case_id, target)
    if case_id == "px01.mobile-head-branching":
        assert target.kind is loci.LocusKind.OCCURRENCE
        index = int(target.path[-1])
        return _term("tape-cell", index - 1)
    if case_id == "px02.parallel-substitution":
        assert target.kind is loci.LocusKind.OCCURRENCE
        return _term("occurrence", "old", int(target.path[-1]))
    if case_id == "px04.multiway-diamond":
        assert target.kind is loci.LocusKind.OCCURRENCE
        return _term("word-occurrence", int(target.path[-1]))
    if case_id.startswith("px04.constraint-mod3-"):
        assert target.kind is loci.LocusKind.NAMED
        assert target.path == ("x",)
        return _term("unknown", "x")
    if case_id == "px02.graph-interface-replacement":
        assert target.kind is loci.LocusKind.GRAPH_ELEMENT
        kind, identity = target.path
        if kind == "node":
            return _term("node", str(identity))
        left, right = str(identity).split("-", maxsplit=1)
        return _term("edge", left, right)
    if case_id == "px06.stochastic-search-law":
        assert target.kind is loci.LocusKind.NAMED
        return _term("field", str(target.path[-1]))
    if case_id == "px05.exact-differential-flow":
        assert target.kind is loci.LocusKind.NAMED
        assert target.path == ("solution",)
        return _term("solution-slot", "x")
    assert case_id == "px05.constant-field-intensional"
    assert target.kind is loci.LocusKind.NAMED
    assert target.path == ("u",)
    return _term("field-capability", "u")


def _ct12_graph_payload_as_oracle(
    value: alphabets.SemanticValue,
) -> test_oracles.OracleTerm:
    assert isinstance(value, alphabets.ValueNode)
    if value.tag == "node-value":
        assert len(value.items) == 1 and isinstance(value.items[0], str)
        return _term("node-value", value.items[0])
    assert value.tag == "edge-value" and len(value.items) == 2
    endpoints = []
    for item in value.items:
        assert isinstance(item, alphabets.StructuralReference)
        reference = item.reference
        if isinstance(reference, loci.FreshReference):
            endpoints.append(
                _term(
                    "fresh-ref",
                    _ct12_fresh_target_as_oracle(
                        "px02.graph-interface-replacement",
                        reference,
                    ),
                )
            )
        else:
            assert reference.kind is loci.LocusKind.GRAPH_ELEMENT
            assert reference.path[0] == "node"
            endpoints.append(_term("existing-ref", str(reference.path[1])))
    return _term("edge-value", *endpoints)


def _ct12_payload_as_oracle(
    case_id: str,
    value: alphabets.SemanticValue,
) -> test_oracles.OracleValue:
    if case_id in {
        "px02.parallel-substitution",
        "px04.multiway-diamond",
    }:
        assert isinstance(value, str)
        return _term("symbol-value", value)
    if case_id == "px02.graph-interface-replacement":
        return _ct12_graph_payload_as_oracle(value)
    return _ct12_semantic_as_oracle(value)


def _ct12_bound_identity(
    case_id: str,
    reference: loci.FreshReference,
) -> test_oracles.OracleTerm:
    key = str(reference.local_key)
    if case_id == "px02.parallel-substitution":
        ordinal = {"old:0:0": 0, "old:0:1": 1}[key]
        return _term(
            "fresh-id",
            "px02.parallel-substitution",
            "old:0",
            ordinal,
        )
    assert case_id == "px02.graph-interface-replacement"
    return _term("fresh-id", case_id, "b", key)


def _ct12_configuration_as_oracle(
    case_id: str,
    actual: loci.FiniteConfiguration,
    *,
    bound_identities: dict[loci.Locus, test_oracles.OracleTerm] | None = None,
) -> test_oracles.OracleTerm:
    bound_identities = {} if bound_identities is None else bound_identities
    entries = dict(actual.entries)

    if case_id == "px01.mobile-head-branching":
        assert actual.contract.kind is loci.CarrierKind.HISTORY
        by_index = {
            int(target.path[-1]): _ct12_semantic_as_oracle(value)
            for target, value in actual.entries
        }
        assert set(by_index) == {0, 1, 2}
        return _term(
            "tape",
            *(
                _term("at", index - 1, by_index[index])
                for index in range(3)
            ),
        )

    if case_id in {
        "px02.parallel-substitution",
        "px04.multiway-diamond",
    }:
        assert actual.contract.kind is loci.CarrierKind.WORD
        symbols = []
        for target, value in actual.entries:
            if target in bound_identities:
                identity: test_oracles.OracleValue = bound_identities[target]
            elif case_id == "px02.parallel-substitution":
                identity = _term(
                    "occurrence",
                    "old",
                    int(target.path[-1]),
                )
            else:
                identity = _term("word-occurrence", int(target.path[-1]))
            assert isinstance(value, str)
            symbols.append(_term("symbol", identity, value))
        return _term("word", *symbols)

    if case_id.startswith("px04.constraint-mod3-"):
        fields = {str(target.path[-1]): value for target, value in actual.entries}
        assert fields["domain"] == "Z/3Z"
        assert fields["equation"] == "x^2=rhs"
        assert fields["rhs"] in (0, 1, 2)
        if fields["x"] == "unset":
            return _term(
                "constraint-state",
                _term("domain", "Z/3Z"),
                _term("equation", "x^2=rhs"),
                _term("rhs", fields["rhs"]),
                _term("slot", "x", "unset"),
            )
        assert type(fields["x"]) is int
        return _term("assignment", _term("value", "x", fields["x"]))

    if case_id == "px02.graph-interface-replacement":
        assert actual.contract.kind is loci.CarrierKind.GRAPH
        nodes: dict[str, test_oracles.OracleValue] = {}
        edges: dict[str, tuple[test_oracles.OracleValue, test_oracles.OracleValue, test_oracles.OracleValue]] = {}

        def endpoint(
            item: alphabets.SemanticValue,
        ) -> test_oracles.OracleValue:
            assert isinstance(item, alphabets.StructuralReference)
            reference = item.reference
            assert isinstance(reference, loci.Locus)
            if reference in bound_identities:
                return bound_identities[reference]
            assert reference.kind is loci.LocusKind.GRAPH_ELEMENT
            assert reference.path[0] == "node"
            return str(reference.path[1])

        for target, value in actual.entries:
            assert isinstance(value, alphabets.ValueNode)
            if value.tag == "node-value":
                label = str(value.items[0])
                nodes[label] = (
                    bound_identities[target]
                    if target in bound_identities
                    else label
                )
            else:
                assert value.tag == "edge-value" and len(value.items) == 2
                left, right = (endpoint(item) for item in value.items)
                identity = (
                    bound_identities[target]
                    if target in bound_identities
                    else _term("edge", left, right)
                )
                edges[f"{left!r}:{right!r}"] = (identity, left, right)
        if not bound_identities:
            assert nodes == {"a": "a", "b": "b", "c": "c"}
            return _term(
                "graph",
                _term("nodes", "a", "b", "c"),
                _term(
                    "edges",
                    _term("edge", "a", "b"),
                    _term("edge", "b", "c"),
                ),
            )
        assert set(nodes) == {"a", "c", "x", "y"}
        ordered_nodes = (nodes["a"], nodes["x"], nodes["y"], nodes["c"])
        by_key = {
            str(identity.arguments[-1]): (identity, left, right)
            for identity, left, right in edges.values()
            if isinstance(identity, test_oracles.OracleTerm)
            and identity.tag == "fresh-id"
        }
        assert set(by_key) == {"a-x", "x-y", "y-c"}
        return _term(
            "graph",
            _term("nodes", *ordered_nodes),
            _term(
                "edges",
                *(
                    _term("edge-record", *by_key[key])
                    for key in ("a-x", "x-y", "y-c")
                ),
            ),
        )

    if case_id == "px06.stochastic-search-law":
        fields = {str(target.path[-1]): value for target, value in actual.entries}
        assert set(fields) == {"x", "k"}
        return _term(
            "configuration.record",
            _term("field-value", "x", fields["x"]),
            _term("field-value", "k", fields["k"]),
        )

    if case_id == "px05.exact-differential-flow":
        fields = {str(target.path[-1]): value for target, value in actual.entries}
        assert _ct12_semantic_as_oracle(fields["equation"]) == _term(
            "derivative-equals",
            "x",
            "t",
            1,
        )
        assert _ct12_semantic_as_oracle(fields["initial"]) == _term(
            "initial-condition",
            "x",
            0,
            0,
        )
        solution = fields["solution"]
        normalized_solution: test_oracles.OracleValue = (
            "unset"
            if solution == "unset"
            else _ct12_semantic_as_oracle(solution)
        )
        return _term(
            "differential-state",
            _term("equation", _term("derivative", "x", "t"), 1),
            _term("initial-condition", _term("x-at", 0), 0),
            _term("solution", normalized_solution),
        )

    assert case_id == "px05.constant-field-intensional"
    fields = {str(target.path[-1]): value for target, value in actual.entries}
    assert _ct12_semantic_as_oracle(fields["domain"]) == _term(
        "closed-interval",
        0,
        1,
    )
    assert _ct12_semantic_as_oracle(fields["u"]) == _term(
        "unknown-field",
        "u",
    )
    return _term(
        "field-state",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("field", "u", "unknown"),
    )


def _ct12_readable_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    readable: neighborhoods.ReadableView,
) -> test_oracles.OracleTerm:
    assert readable.snapshot_identity == source.identity
    observed = {}
    for observation in readable.observations:
        assert not isinstance(observation.state, neighborhoods.Absent)
        observed[observation.target] = observation.value
    assert observed == dict(source.entries)
    source_term = _ct12_configuration_as_oracle(case_id, source)
    if case_id == "px01.mobile-head-branching":
        return _term("keyed-old-tape", source_term)
    if case_id == "px02.parallel-substitution":
        return _term("old-generation-items", source_term)
    if case_id == "px04.multiway-diamond":
        return _term("all-matches", source_term)
    if case_id.startswith("px04.constraint-mod3-"):
        rhs = dict(source.entries)[
            next(target for target, _ in source.entries if target.path == ("rhs",))
        ]
        return _term("constraint-view", f"x^2={rhs}", "Z/3Z")
    if case_id == "px02.graph-interface-replacement":
        return _term(
            "matched-interface-view",
            source_term,
            _term("external-ports", "a", "c"),
        )
    if case_id == "px06.stochastic-search-law":
        assert source.carrier.attributes == (
            ("objective", "(x-1)^2"),
            ("proposal-law", "closed"),
        )
        return _term(
            "search-view",
            source_term,
            _term("objective", "(x-1)^2"),
            _term("proposal-law", "closed"),
        )
    if case_id == "px05.exact-differential-flow":
        assert source.carrier.attributes == (
            ("duration-or-event-selector", "none"),
        )
        return _term(
            "differential-view",
            _term("equation", _term("derivative", "x", "t"), 1),
            _term("initial-condition", _term("x-at", 0), 0),
            _term("duration-or-event-selector", "none"),
        )
    assert case_id == "px05.constant-field-intensional"
    assert source.carrier.attributes == (
        ("differential-germ", "du/dx=0"),
        ("side-data", "none"),
    )
    return _term(
        "differential-view",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("germ", _term("derivative", "u", "x")),
        _term("side-data", "none"),
    )


def _ct12_writable_as_oracle(
    case_id: str,
    source: loci.FiniteConfiguration,
    writable: frontiers.WritableCapabilities,
) -> tuple[test_oracles.OracleTerm, ...]:
    assert writable.snapshot_identity == source.identity
    capabilities = (*writable.existing, *writable.fresh)
    assert tuple(item.target for item in capabilities) == tuple(
        lens.target for lens in writable.reconstruction.lenses
    )
    return tuple(
        _ct12_target_as_oracle(case_id, item.target)
        for item in capabilities
    )


def _ct12_ordered_writable_terms(
    case_id: str,
) -> tuple[test_oracles.OracleTerm, ...]:
    """Independent semantic order for each frozen non-native capability set."""

    if case_id == "px01.mobile-head-branching":
        return tuple(_term("tape-cell", index) for index in (-1, 0, 1))
    if case_id == "px02.parallel-substitution":
        old_a = _term("occurrence", "old", 0)
        return (
            old_a,
            _term("occurrence", "old", 1),
            _term("fresh-slot", "offspring", old_a, 0),
            _term("fresh-slot", "offspring", old_a, 1),
        )
    if case_id == "px04.multiway-diamond":
        return (_term("word-occurrence", 0),)
    if case_id.startswith("px04.constraint-mod3-"):
        return (_term("unknown", "x"),)
    if case_id == "px02.graph-interface-replacement":
        return (
            _term("node", "b"),
            _term("edge", "a", "b"),
            _term("edge", "b", "c"),
            _term("fresh-slot", "node", "x"),
            _term("fresh-slot", "node", "y"),
            _term("fresh-slot", "edge", "a-x"),
            _term("fresh-slot", "edge", "x-y"),
            _term("fresh-slot", "edge", "y-c"),
        )
    if case_id == "px06.stochastic-search-law":
        return (_term("field", "x"), _term("field", "k"))
    if case_id == "px05.exact-differential-flow":
        return (_term("solution-slot", "x"),)
    assert case_id == "px05.constant-field-intensional"
    return (_term("field-capability", "u"),)


def _ct12_atom_id(
    case_id: str,
    witness: test_oracles.OracleValue,
) -> str:
    """Derive the semantic oracle identifier from the runtime witness."""

    mappings: dict[str, dict[test_oracles.OracleValue, str]] = {
        "px01.mobile-head-branching": {
            _term(
                "transition-witness",
                "q",
                1,
                "p",
                0,
                "left",
            ): "mobile-left",
            _term(
                "transition-witness",
                "q",
                1,
                "p",
                0,
                "right",
            ): "mobile-right",
        },
        "px02.parallel-substitution": {
            _term(
                "generation-witness",
                "A->AB",
                "B->epsilon",
            ): "parallel-substitution",
        },
        "px04.multiway-diamond": {
            _term(
                "rewrite-witness",
                "rule-left",
                "match:0",
                "parent:a",
            ): "diamond-rule-left",
            _term(
                "rewrite-witness",
                "rule-right",
                "match:0",
                "parent:a",
            ): "diamond-rule-right",
        },
        "px04.constraint-mod3-zero": {
            _term(
                "relation-witness",
                "x^2=2",
                "Z/3Z",
            ): "constraint-no-solution",
        },
        "px04.constraint-mod3-one": {
            _term("solution-witness", "x", 0): "constraint-x-0",
        },
        "px04.constraint-mod3-many": {
            _term("solution-witness", "x", 1): "constraint-x-1",
            _term("solution-witness", "x", 2): "constraint-x-2",
        },
        "px02.graph-interface-replacement": {
            _term(
                "match",
                _term("node", "b"),
                _term("ports", "a", "c"),
            ): "graph-replacement",
        },
        "px06.stochastic-search-law": {
            _term(
                "proposal-witness",
                1,
                "accepted",
            ): "search-accept",
            _term(
                "proposal-witness",
                0,
                "rejected",
            ): "search-reject",
            _term(
                "proposal-witness",
                "none",
            ): "search-no-proposal",
        },
        "px05.exact-differential-flow": {
            _term(
                "differential-proof",
                _term("derivative-of", "t", "t", 1),
                _term("initial-value", 0, 0),
                _term("coverage", "maximal-exact-real-solution"),
            ): "exact-flow-x-equals-t",
        },
    }
    try:
        return mappings[case_id][witness]
    except KeyError as error:
        raise AssertionError(
            f"unexpected CT12 witness for {case_id}: {witness!r}"
        ) from error


def _ct12_atom_order(case_id: str, atom_id: str) -> int:
    orders = {
        "px01.mobile-head-branching": ("mobile-left", "mobile-right"),
        "px02.parallel-substitution": ("parallel-substitution",),
        "px04.multiway-diamond": (
            "diamond-rule-left",
            "diamond-rule-right",
        ),
        "px04.constraint-mod3-zero": ("constraint-no-solution",),
        "px04.constraint-mod3-one": ("constraint-x-0",),
        "px04.constraint-mod3-many": (
            "constraint-x-1",
            "constraint-x-2",
        ),
        "px02.graph-interface-replacement": ("graph-replacement",),
        "px06.stochastic-search-law": (
            "search-accept",
            "search-reject",
            "search-no-proposal",
        ),
        "px05.exact-differential-flow": ("exact-flow-x-equals-t",),
    }
    try:
        return orders[case_id].index(atom_id)
    except (KeyError, ValueError) as error:
        raise AssertionError(
            f"unexpected CT12 atom identifier for {case_id}: {atom_id!r}"
        ) from error


def _ct12_dispositions_as_oracle(
    case_id: str,
    actual: rules.TotalDisposition,
) -> tuple[test_oracles.OracleDisposition, ...]:
    assert actual.version == 1
    assert actual.totality_evidence.kind is rules.CertificateKind.TOTALITY
    normalized: dict[test_oracles.OracleTerm, test_oracles.OracleDisposition] = {}
    for item in actual.entries:
        target = _ct12_target_as_oracle(case_id, item.target)
        assert target not in normalized
        payload = (
            _ct12_payload_as_oracle(case_id, item.payload.value)
            if isinstance(item.payload, rules.ValuePayload)
            else None
        )
        normalized[target] = test_oracles.OracleDisposition(
            target,
            item.action.value,
            payload,
        )
    ordered_targets = _ct12_ordered_writable_terms(case_id)
    assert set(normalized) == set(ordered_targets)
    return tuple(normalized[target] for target in ordered_targets)


def _ct12_continuation_as_oracle(
    actual: rules.Continuation,
) -> test_oracles.OracleTerm:
    if isinstance(actual, rules.Continue):
        assert actual.version == 1
        return _term("continue")
    assert isinstance(actual, rules.Stop)
    assert actual.version == 1
    assert actual.certificate.kind is rules.CertificateKind.TERMINALITY
    assert _ct12_expression_as_oracle(actual.reason) == "completed"
    return _term("stop", "completed")


def _ct12_normalize_fresh_bindings(
    case_id: str,
    actual: program.AppliedDerivation,
    application: program.ApplicationComplete,
) -> tuple[
    tuple[test_oracles.OracleFreshBinding, ...],
    dict[loci.Locus, test_oracles.OracleTerm],
]:
    normalized = []
    bound_identities = {}
    for binding in actual.fresh_bindings:
        reference = binding.reference
        local_key = _ct12_fresh_target_as_oracle(case_id, reference)
        assert binding.identity == loci.bind_fresh(
            reference,
            input_configuration_identity=application.evidence.input_configuration_identity,
            canonical_rule_identity=application.evidence.canonical_rule_identity,
            witness_identity=actual.source.witness.canonical_identity,
        )
        semantic_identity = _ct12_bound_identity(case_id, reference)
        assert reference.namespace == case_id
        if case_id == "px02.parallel-substitution":
            assert reference.parent is not None
            assert _ct12_target_as_oracle(case_id, reference.parent) == _term(
                "occurrence",
                "old",
                0,
            )
            assert not reference.interface
            ordinal = {"old:0:0": 0, "old:0:1": 1}[
                str(reference.local_key)
            ]
            evidence = _term(
                "fresh-recipe",
                _term("input-identity", "word:old-generation"),
                _term("rule-identity", "A->AB"),
                _term("witness", "generation-witness"),
                _term("namespace", case_id),
                _term(
                    "parent-and-ordinal",
                    _term("occurrence", "old", 0),
                    ordinal,
                ),
            )
        else:
            key = str(reference.local_key)
            if key in {"x", "y"}:
                assert reference.parent is not None
                assert reference.parent.path == ("node", "b")
                assert not reference.interface
            else:
                assert reference.parent is None
                assert tuple(item.path for item in reference.interface) == (
                    ("node", "a"),
                    ("node", "c"),
                )
            evidence = _term(
                "fresh-recipe",
                _term("input-identity", "graph:a-b-c"),
                _term("rule-identity", "F029"),
                _term("match-witness", "node:b"),
                _term("interface", "a", "c"),
                _term("namespace", case_id),
                _term("local-key", key),
            )
        normalized.append(
            test_oracles.OracleFreshBinding(
                local_key,
                semantic_identity,
                evidence,
            )
        )
        bound_identities[binding.identity] = semantic_identity
    expected_local_keys = tuple(
        target
        for target in _ct12_ordered_writable_terms(case_id)
        if target.tag == "fresh-slot"
    )
    assert {item.local_key for item in normalized} == set(expected_local_keys)
    normalized.sort(
        key=lambda item: expected_local_keys.index(item.local_key)
    )
    return tuple(normalized), bound_identities


def _ct12_assert_applied_lineage(
    actual: program.AppliedDerivation | program.AppliedNoSuccessor,
    application: program.ApplicationComplete,
    source: loci.FiniteConfiguration,
) -> None:
    direct_root = loci.canonical_identity(("direct-application-root", source.identity))
    assert actual.input_trace_lineage == program.TraceLineage(direct_root)
    outcome = (
        actual.source.progress.value
        if isinstance(actual, program.AppliedDerivation)
        else actual.source.outcome.value
    )
    expected_edge = loci.canonical_identity(
        (
            actual.input_trace_lineage.canonical_identity,
            application.evidence.application_identity,
            actual.source.canonical_identity,
            outcome,
        )
    )
    assert actual.output_trace_lineage == program.TraceLineage(
        direct_root,
        (expected_edge,),
    )
    assert actual.evidence.application_identity == (
        application.evidence.application_identity
    )
    expected_disposition = (
        actual.source.replacement.canonical_identity
        if isinstance(actual, program.AppliedDerivation)
        else "no-disposition"
    )
    assert actual.evidence.disposition_identity == expected_disposition


def _ct12_measure_view_as_oracle(
    case_id: str,
    role: str,
    actual: program.MeasureView,
    point_mapping: dict[str, test_oracles.OracleValue],
) -> test_oracles.OracleMeasureView:
    if isinstance(actual, program.MeasureAbsent):
        return test_oracles.OracleMeasureView("absent", (), None, None)
    assert case_id == "px06.stochastic-search-law"
    assert role in {"applied-atoms", "successors", "no-successors"}
    if isinstance(actual, program.MeasureUnavailable):
        raise AssertionError("finite CT12 law unexpectedly lost a measure view")
    assert isinstance(actual, program.MeasureAvailable)
    measure = actual.measure
    assert measure.intensional_descriptor is None
    assert set(point_mapping) == {
        item.point_identity for item in measure.masses
    }
    normalized = tuple(
        (
            point_mapping[item.point_identity],
            item.mass,
        )
        for item in measure.masses
    )
    if role in {"applied-atoms", "no-successors"}:
        normalized = tuple(
            sorted(
                normalized,
                key=lambda item: _ct12_atom_order(
                    case_id,
                    str(item[0]),
                ),
            )
        )
    else:
        accept = _term(
            "configuration.record",
            _term("field-value", "x", 1),
            _term("field-value", "k", 1),
        )
        reject = _term(
            "configuration.record",
            _term("field-value", "x", 0),
            _term("field-value", "k", 1),
        )
        successor_order = (accept, reject)
        normalized = tuple(
            sorted(
                normalized,
                key=lambda item: successor_order.index(item[0]),
            )
        )

    evidence = {
        "applied-atoms": _term(
            "law-evidence",
            "closed-three-atom-law",
        ),
        "successors": _term(
            "pushforward-evidence",
            "derivation-atoms-only",
        ),
        "no-successors": _term(
            "restriction-evidence",
            "no-successor-atoms-only",
        ),
    }[role]
    return test_oracles.OracleMeasureView(
        "available",
        normalized,
        measure.total_mass,
        evidence,
    )


def _ct12_tagged(
    label: str,
    *arguments: rules.RuleExpr,
) -> rules.RuleExpr:
    return rules.RuleExpr(
        rules.ExpressionPrimitive.TUPLE,
        (rules.literal_expr(label), *arguments),
    )


def _ct12_expected_projection(
    phase: str,
    source_relation: rules.RuleExpr,
    evidence: program.ApplicationEvidence,
) -> rules.RuleExpr:
    """Independent spelling of the generic projection required by CT12."""

    context = _ct12_tagged(
        "application-context:v1",
        rules.literal_expr(evidence.program_identity),
        rules.literal_expr(evidence.canonical_rule_identity),
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.readable_binding_identity),
        rules.literal_expr(evidence.writable_binding_identity),
        rules.literal_expr(evidence.input_trace_lineage_identity),
        rules.literal_expr(evidence.application_identity),
    )
    source = _ct12_tagged("source-rule-relation", source_relation)
    conformance = _ct12_tagged(
        "map:source-conformance",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.readable_binding_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    bindings = _ct12_tagged(
        "map:fresh-bindings-by-source-witness",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.canonical_rule_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    commit = _ct12_tagged(
        "map:atomic-commit-and-successor-validation",
        rules.literal_expr(evidence.input_configuration_identity),
        rules.literal_expr(evidence.writable_binding_identity),
    )
    lineage = _ct12_tagged(
        "map:extend-trace-lineage",
        rules.literal_expr(evidence.input_trace_lineage_identity),
        rules.literal_expr(evidence.application_identity),
    )
    if phase == "applied-atoms":
        pipeline = (
            _ct12_tagged("filter:all-rule-atoms", source),
            _ct12_tagged(
                "union:typed-applied-atom-branches",
                _ct12_tagged(
                    "branch:derivation-to-applied",
                    _ct12_tagged("filter:derivation", source),
                    conformance,
                    bindings,
                    commit,
                    lineage,
                    _ct12_tagged("map:typed-applied-derivation"),
                ),
                _ct12_tagged(
                    "branch:no-successor-to-applied",
                    _ct12_tagged("filter:no-successor", source),
                    conformance,
                    lineage,
                    _ct12_tagged("map:typed-applied-no-successor"),
                ),
            ),
        )
    elif phase == "no-successor-partition":
        pipeline = (
            _ct12_tagged("filter:no-successor", source),
            conformance,
            lineage,
            _ct12_tagged("map:typed-applied-no-successor"),
        )
    else:
        assert phase == "successor-quotient"
        pipeline = (
            _ct12_tagged("filter:derivation", source),
            conformance,
            bindings,
            commit,
            lineage,
            _ct12_tagged(
                "quotient:semantic-successor-with-derivation-fibers"
            ),
        )
    return _ct12_tagged(f"application-projection:{phase}:v1", context, *pipeline)


def _ct12_intensional_projection_as_oracle(
    phase: str,
    actual: rules.RuleExpr,
    source_relation: rules.RuleExpr,
    evidence: program.ApplicationEvidence,
    source_configuration: loci.FiniteConfiguration,
) -> test_oracles.OracleTerm:
    """Interpret the validated generic projection into frozen semantic syntax."""

    assert phase in {"applied-atoms", "successor-quotient"}
    assert actual == _ct12_expected_projection(
        phase,
        source_relation,
        evidence,
    )
    source_term = _ct12_expression_as_oracle(source_relation)
    assert isinstance(source_term, test_oracles.OracleTerm)
    assert source_term.tag == "intensional-source-outcome-relation"
    binder_term, domain_term, template = source_term.arguments
    assert isinstance(binder_term, test_oracles.OracleTerm)
    assert binder_term.tag == "binder"
    assert len(binder_term.arguments) == 1
    binder = binder_term.arguments[0]
    assert binder == "c"
    assert domain_term == _term("domain", "exact-real")
    assert isinstance(template, test_oracles.OracleTerm)
    assert template.tag == "source-derivation-template"
    atom_term, disposition, witness, continuation = template.arguments
    assert isinstance(atom_term, test_oracles.OracleTerm)
    assert atom_term.tag == "atom-id"
    parameterized = atom_term.arguments[0]
    assert parameterized == _term("parameterized", "constant-field", binder)
    assert disposition == _term(
        "total-disposition",
        _term(
            "replace",
            _term("field-capability", "u"),
            _term("constant-field", binder),
        ),
    )
    assert witness == _term(
        "witness",
        _term("derivative", "u", "x"),
        0,
    )
    assert continuation == _term("stop", "completed")
    source_configuration_term = _ct12_configuration_as_oracle(
        "px05.constant-field-intensional",
        source_configuration,
    )
    assert source_configuration_term == _term(
        "field-state",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("field", "u", "unknown"),
    )
    successor = _term(
        "field-state",
        _term("domain", _term("closed-interval", 0, 1)),
        _term("field", "u", _term("constant-field", binder)),
    )

    if phase == "applied-atoms":
        return _term(
            "intensional-applied-atom-relation",
            binder_term,
            domain_term,
            _term(
                "applied-derivation-template",
                _term("source-atom-id", parameterized),
                _term("successor", successor),
                _term("fresh-bindings", "empty"),
                _term(
                    "output-lineage",
                    "px05.constant-field-intensional",
                    binder,
                ),
                _term(
                    "application-evidence",
                    "exact-differential-proof",
                    binder,
                ),
            ),
        )
    return _term(
        "intensional-successor-quotient-relation",
        binder_term,
        domain_term,
        _term(
            "successor-group-template",
            successor,
            _term(
                "derivation-fiber",
                _term("applied-atom-id", parameterized),
            ),
        ),
    )


def _assert_complete_non_native_result(
    oracle_case: test_oracles.OracleCase,
    execution,
    actual: program.ApplicationComplete,
) -> test_oracles.OracleExpected:
    """Normalize every independent finite/intensional CT12 obligation."""

    case_id = oracle_case.case_id
    source = execution.source
    assert isinstance(source, loci.FiniteConfiguration)
    assert _ct12_configuration_as_oracle(case_id, source) == oracle_case.source
    writable = execution.simple_program.frontier.resolve(source)
    readable = execution.simple_program.neighborhood.resolve(source)
    assert isinstance(writable, frontiers.WritableCapabilities)
    assert isinstance(readable, neighborhoods.ReadableView)
    normalized_writable = _ct12_writable_as_oracle(case_id, source, writable)
    assert set(normalized_writable) == set(oracle_case.writable)
    assert len(normalized_writable) == len(oracle_case.writable)
    assert _ct12_readable_as_oracle(case_id, source, readable) == (
        oracle_case.readable
    )

    support = actual.source_outcomes.support
    assert actual.source_outcomes.version == 1
    _assert_support_evidence(support)
    assert _cardinality_as_oracle(actual.outcome_atom_cardinality) == (
        _cardinality_as_oracle(support.cardinality)
    )
    _assert_support_evidence(actual.applied_atoms)
    _assert_support_evidence(actual.no_successor_partition)
    _assert_support_evidence(
        actual.successor_quotient_with_derivation_fibers
    )

    if support.presentation is rules.SupportPresentation.INTENSIONAL:
        assert support.presentation is rules.SupportPresentation.INTENSIONAL
        assert not support.atoms
        assert support.relation is not None
        source_relation = _ct12_expression_as_oracle(support.relation)
        assert not actual.applied_atoms.atoms
        assert not actual.no_successor_partition.atoms
        assert not actual.successor_quotient_with_derivation_fibers.atoms
        assert actual.applied_atoms.relation is not None
        applied_relation = _ct12_intensional_projection_as_oracle(
            "applied-atoms",
            actual.applied_atoms.relation,
            support.relation,
            actual.evidence,
            source,
        )
        assert actual.no_successor_partition.relation is not None
        assert actual.no_successor_partition.relation == (
            _ct12_expected_projection(
                "no-successor-partition",
                support.relation,
                actual.evidence,
            )
        )
        successor_relation_runtime = (
            actual.successor_quotient_with_derivation_fibers.relation
        )
        assert successor_relation_runtime is not None
        successor_relation = _ct12_intensional_projection_as_oracle(
            "successor-quotient",
            successor_relation_runtime,
            support.relation,
            actual.evidence,
            source,
        )
        normalized_measures = test_oracles.OracleMeasures(
            _ct12_measure_view_as_oracle(
                case_id,
                "applied-atoms",
                actual.applied_atom_measure,
                {},
            ),
            _ct12_measure_view_as_oracle(
                case_id,
                "successors",
                actual.successor_submeasure,
                {},
            ),
            _ct12_measure_view_as_oracle(
                case_id,
                "no-successors",
                actual.no_successor_submeasure,
                {},
            ),
        )
        assert _application_evidence_as_oracle(
            actual.evidence,
            oracle_case=oracle_case,
            simple_program=execution.simple_program,
            source=source,
            readable=readable,
            writable=writable,
        ) == _term("application-evidence", case_id)
        claims = actual.source_outcomes.projection_cardinalities
        assert claims is not None
        assert claims.mapping_evidence.kind is rules.CertificateKind.COMPOSITION
        assert _ct12_expression_as_oracle(
            claims.mapping_evidence.statement
        ) == "constant-field:injective-total-projection"
        normalized_evidence = _term(
            "application-evidence",
            case_id,
            _term("coverage", "all-exact-real-c"),
        )
        return test_oracles.OracleExpected(
            support_kind="intensional",
            source_outcomes=(),
            applied_atoms=(),
            no_successor_partition=(),
            outcome_cardinality=_cardinality_as_oracle(
                actual.outcome_atom_cardinality
            ),
            derivation_cardinality=_cardinality_as_oracle(
                actual.derivation_cardinality
            ),
            successor_cardinality=_cardinality_as_oracle(
                actual.successor_cardinality
            ),
            successor_fibers=(),
            measures=normalized_measures,
            source_intensional_relation=source_relation,
            applied_intensional_relation=applied_relation,
            successor_intensional_relation=successor_relation,
            evidence=normalized_evidence,
        )

    assert support.presentation is rules.SupportPresentation.FINITE
    assert support.relation is None
    assert actual.applied_atoms.relation is None
    assert actual.no_successor_partition.relation is None
    assert actual.successor_quotient_with_derivation_fibers.relation is None
    runtime_to_oracle_id = {}
    normalized_source_atoms = []
    law = actual.source_outcomes.probability_law
    for atom in support.atoms:
        assert atom.version == 1
        assert atom.witness.version == 1
        assert atom.witness.identity == loci.canonical_identity(
            atom.witness.descriptor
        )
        witness = _ct12_expression_as_oracle(atom.witness.descriptor)
        atom_id = _ct12_atom_id(case_id, witness)
        runtime_to_oracle_id[atom.canonical_identity] = atom_id
        mass = None if law is None else law.mass_for(atom.canonical_identity)
        assert atom.certificate.version == 1
        certificate = _ct12_expression_as_oracle(atom.certificate.statement)
        if isinstance(atom, rules.NoSuccessor):
            assert atom.outcome is rules.NoSuccessorOutcome.TERMINAL
            assert atom.certificate.kind is rules.CertificateKind.TERMINALITY
            normalized_source_atoms.append(
                test_oracles.OracleSourceAtom(
                    atom_id,
                    "no-successor",
                    witness,
                    atom.provenance,
                    None,
                    None,
                    (),
                    _ct12_expression_as_oracle(atom.reason),
                    certificate,
                    mass,
                )
            )
        else:
            assert atom.certificate.kind is rules.CertificateKind.DERIVATION
            normalized_source_atoms.append(
                test_oracles.OracleSourceAtom(
                    atom_id,
                    "derivation",
                    witness,
                    atom.provenance,
                    atom.progress.value,
                    _ct12_continuation_as_oracle(atom.continuation),
                    _ct12_dispositions_as_oracle(
                        case_id,
                        atom.replacement,
                    ),
                    None,
                    certificate,
                    mass,
                )
            )
    assert len(runtime_to_oracle_id) == len(support.atoms)
    normalized_source_atoms.sort(
        key=lambda item: _ct12_atom_order(case_id, item.atom_id)
    )
    normalized_applied = []
    applied_identity_to_point = {}
    no_successor_identity_to_point = {}
    applied_bound_identities: dict[
        str,
        dict[loci.Locus, test_oracles.OracleTerm],
    ] = {}
    for atom in actual.applied_atoms.atoms:
        source_id = atom.source.canonical_identity
        assert source_id in runtime_to_oracle_id
        atom_id = runtime_to_oracle_id[source_id]
        _ct12_assert_applied_lineage(atom, actual, source)
        applied_identity_to_point[atom.canonical_identity] = atom_id
        if isinstance(atom, program.AppliedNoSuccessor):
            no_successor_identity_to_point[atom.canonical_identity] = atom_id
            normalized = test_oracles.OracleAppliedAtom(
                atom_id,
                atom_id,
                None,
                (),
                _term("lineage", case_id, atom_id),
                _term("applied-atom-evidence", case_id, atom_id),
            )
        else:
            fresh_bindings, bound = _ct12_normalize_fresh_bindings(
                case_id,
                atom,
                actual,
            )
            applied_bound_identities[source_id] = bound
            normalized = test_oracles.OracleAppliedAtom(
                atom_id,
                atom_id,
                _ct12_configuration_as_oracle(
                    case_id,
                    atom.successor,
                    bound_identities=bound,
                ),
                fresh_bindings,
                _term("lineage", case_id, atom_id),
                _term("applied-atom-evidence", case_id, atom_id),
            )
        normalized_applied.append(normalized)
    normalized_applied.sort(
        key=lambda item: _ct12_atom_order(case_id, item.atom_id)
    )

    normalized_no_successors = tuple(
        item
        for item in normalized_applied
        if item.successor is None
    )
    actual_partition_ids = {
        item.source.canonical_identity
        for item in actual.no_successor_partition.atoms
    }
    assert actual_partition_ids == {
        item.source.canonical_identity
        for item in actual.applied_atoms.atoms
        if isinstance(item, program.AppliedNoSuccessor)
    }

    normalized_fibers = []
    successor_identity_to_point = {}
    for group in actual.successor_quotient_with_derivation_fibers.atoms:
        assert group.derivations
        first = group.derivations[0]
        bound = applied_bound_identities.get(
            first.source.canonical_identity,
            {},
        )
        successor = _ct12_configuration_as_oracle(
            case_id,
            group.successor,
            bound_identities=bound,
        )
        atom_ids = {
            runtime_to_oracle_id[item.source.canonical_identity]
            for item in group.derivations
        }
        for item in group.derivations:
            assert _ct12_configuration_as_oracle(
                case_id,
                item.successor,
                bound_identities=applied_bound_identities.get(
                    item.source.canonical_identity,
                    {},
                ),
            ) == successor
        ordered_atom_ids = tuple(
            sorted(
                atom_ids,
                key=lambda atom_id: _ct12_atom_order(case_id, atom_id),
            )
        )
        normalized_fibers.append(
            test_oracles.OracleFiber(successor, ordered_atom_ids)
        )
        successor_identity_to_point[group.canonical_identity] = successor
    normalized_fibers.sort(
        key=lambda item: min(
            _ct12_atom_order(case_id, atom_id)
            for atom_id in item.atom_ids
        )
    )

    if law is None:
        assert all(item.mass is None for item in normalized_source_atoms)
    else:
        assert law.presentation is rules.ProbabilityPresentation.FINITE
        assert law.version == 1
        assert law.normalization_evidence.kind is rules.CertificateKind.NORMALIZATION
        assert law.measurable_space_evidence.kind is rules.CertificateKind.MEASURABILITY
        assert {
            runtime_to_oracle_id[item.atom_identity]: item.mass
            for item in law.masses
        } == {
            item.atom_id: item.mass for item in normalized_source_atoms
        }
    normalized_measures = test_oracles.OracleMeasures(
        _ct12_measure_view_as_oracle(
            case_id,
            "applied-atoms",
            actual.applied_atom_measure,
            applied_identity_to_point,
        ),
        _ct12_measure_view_as_oracle(
            case_id,
            "successors",
            actual.successor_submeasure,
            successor_identity_to_point,
        ),
        _ct12_measure_view_as_oracle(
            case_id,
            "no-successors",
            actual.no_successor_submeasure,
            no_successor_identity_to_point,
        ),
    )

    normalized_evidence = _application_evidence_as_oracle(
        actual.evidence,
        oracle_case=oracle_case,
        simple_program=execution.simple_program,
        source=source,
        readable=readable,
        writable=writable,
    )
    return test_oracles.OracleExpected(
        support_kind="finite",
        source_outcomes=tuple(normalized_source_atoms),
        applied_atoms=tuple(normalized_applied),
        no_successor_partition=normalized_no_successors,
        outcome_cardinality=_cardinality_as_oracle(
            actual.outcome_atom_cardinality
        ),
        derivation_cardinality=_cardinality_as_oracle(
            actual.derivation_cardinality
        ),
        successor_cardinality=_cardinality_as_oracle(
            actual.successor_cardinality
        ),
        successor_fibers=tuple(normalized_fibers),
        measures=normalized_measures,
        source_intensional_relation=None,
        applied_intensional_relation=None,
        successor_intensional_relation=None,
        evidence=normalized_evidence,
    )


def _normalize_non_native_case(
    oracle_case: test_oracles.OracleCase,
) -> test_oracles.OracleExpected:
    execution = runtime_ct12_fixture(oracle_case.case_id)
    actual = execution.result

    assert isinstance(actual, program.ApplicationComplete)
    assert_closed_descriptor(execution.simple_program)
    assert_closed_descriptor(actual)
    assert actual.evidence.phases == tuple(program.ApplicationPhase)
    assert actual.evidence.program_identity == execution.simple_program.canonical_identity
    assert actual.evidence.input_configuration_identity == execution.source.identity
    return _assert_complete_non_native_result(
        oracle_case,
        execution,
        actual,
    )


def _assert_non_native_case(case_id: str) -> None:
    oracle = _ORACLES_BY_ID[case_id]
    assert_full_application_equal(
        _normalize_non_native_case(oracle),
        oracle.expected,
    )


@pytest.mark.parametrize(
    "oracle_case",
    test_oracles.CT12_CASES[6:14],
    ids=lambda case: case.case_id,
)
def test_variable_structure_and_stochastic_fixtures_match_completely(
    oracle_case: test_oracles.OracleCase,
) -> None:
    _assert_non_native_case(oracle_case.case_id)


@pytest.mark.parametrize(
    "oracle_case",
    test_oracles.CT12_CASES[14:],
    ids=lambda case: case.case_id,
)
def test_differential_and_intensional_fixtures_use_exact_tiny_oracles(
    oracle_case: test_oracles.OracleCase,
) -> None:
    _assert_non_native_case(oracle_case.case_id)


def test_fresh_binding_normalization_resists_mutated_frozen_evidence() -> None:
    oracle = _ORACLES_BY_ID["px02.parallel-substitution"]
    applied = oracle.expected.applied_atoms[0]
    binding = applied.fresh_bindings[0]
    mutated_binding = replace(
        binding,
        evidence=_term("mutated-fresh-recipe"),
    )
    mutated_applied = replace(
        applied,
        fresh_bindings=(
            mutated_binding,
            *applied.fresh_bindings[1:],
        ),
    )
    mutated_expected = replace(
        oracle.expected,
        applied_atoms=(
            mutated_applied,
            *oracle.expected.applied_atoms[1:],
        ),
    )
    mutated_case = replace(oracle, expected=mutated_expected)

    normalized = _normalize_non_native_case(mutated_case)

    assert normalized == oracle.expected
    assert normalized != mutated_expected


def test_intensional_normalization_resists_mutated_frozen_relations() -> None:
    oracle = _ORACLES_BY_ID["px05.constant-field-intensional"]
    mutated_expected = replace(
        oracle.expected,
        applied_intensional_relation=_term("mutated-applied-relation"),
        successor_intensional_relation=_term("mutated-successor-relation"),
    )
    mutated_case = replace(oracle, expected=mutated_expected)

    normalized = _normalize_non_native_case(mutated_case)

    assert normalized == oracle.expected
    assert normalized != mutated_expected


def test_measure_normalization_resists_mutated_frozen_evidence() -> None:
    oracle = _ORACLES_BY_ID["px06.stochastic-search-law"]
    applied_measure = replace(
        oracle.expected.measures.applied_atoms,
        evidence=_term("mutated-law-evidence"),
    )
    mutated_expected = replace(
        oracle.expected,
        measures=replace(
            oracle.expected.measures,
            applied_atoms=applied_measure,
        ),
    )
    mutated_case = replace(oracle, expected=mutated_expected)

    normalized = _normalize_non_native_case(mutated_case)

    assert normalized == oracle.expected
    assert normalized != mutated_expected
