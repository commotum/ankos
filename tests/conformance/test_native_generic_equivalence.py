"""CT12: independent retained-native and generic one-step equivalence."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import pytest

import ca
from ca import frontiers, loci, neighborhoods, program, rules

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


@dataclass(frozen=True)
class CompleteMechanicsFingerprint:
    """Representation-independent projection of every result-algebra facet."""

    support_kind: str
    source_atoms: tuple[
        tuple[str, str | None, str | None, int, Fraction | None], ...
    ]
    applied_atom_count: int
    fresh_binding_counts: tuple[int, ...]
    no_successor_count: int
    cardinalities: tuple[tuple[str, int | None], ...]
    successor_fiber_sizes: tuple[int, ...]
    measures: tuple[tuple[str, tuple[Fraction, ...], Fraction | None], ...]
    intensional_relations: tuple[bool, bool, bool]


def _oracle_mechanics_fingerprint(
    expected: test_oracles.OracleExpected,
) -> CompleteMechanicsFingerprint:
    source_atoms = tuple(
        sorted(
            (
                atom.kind,
                atom.progress,
                None if atom.continuation is None else atom.continuation.tag,
                len(atom.dispositions),
                atom.mass,
            )
            for atom in expected.source_outcomes
        )
    )
    measures = tuple(
        (
            view.kind,
            tuple(sorted(mass for _, mass in view.masses)),
            view.total_mass,
        )
        for view in (
            expected.measures.applied_atoms,
            expected.measures.successors,
            expected.measures.no_successors,
        )
    )
    return CompleteMechanicsFingerprint(
        expected.support_kind,
        source_atoms,
        len(expected.applied_atoms),
        tuple(
            sorted(len(atom.fresh_bindings) for atom in expected.applied_atoms)
        ),
        len(expected.no_successor_partition),
        (
            (
                expected.outcome_cardinality.kind,
                expected.outcome_cardinality.value,
            ),
            (
                expected.derivation_cardinality.kind,
                expected.derivation_cardinality.value,
            ),
            (
                expected.successor_cardinality.kind,
                expected.successor_cardinality.value,
            ),
        ),
        tuple(sorted(len(fiber.atom_ids) for fiber in expected.successor_fibers)),
        measures,
        (
            expected.source_intensional_relation is not None,
            expected.applied_intensional_relation is not None,
            expected.successor_intensional_relation is not None,
        ),
    )


def _runtime_cardinality(
    cardinality: rules.Cardinality,
) -> tuple[str, int | None]:
    size = rules.cardinality_size(cardinality)
    if size is not None:
        return ("exact", size)
    if isinstance(cardinality, rules.Many):
        assert cardinality.infinite is rules.InfiniteCardinality.UNCOUNTABLE
        return ("uncountable", None)
    return ("undetermined", None)


def _runtime_measure(
    value: program.MeasureView,
) -> tuple[str, tuple[Fraction, ...], Fraction | None]:
    if isinstance(value, program.MeasureAbsent):
        return ("absent", (), None)
    if isinstance(value, program.MeasureUnavailable):
        return ("unavailable", (), None)
    assert isinstance(value, program.MeasureAvailable)
    return (
        "available",
        tuple(sorted(item.mass for item in value.measure.masses)),
        value.measure.total_mass,
    )


def _runtime_mechanics_fingerprint(
    actual: program.ApplicationComplete,
) -> CompleteMechanicsFingerprint:
    support = actual.source_outcomes.support
    law = actual.source_outcomes.probability_law

    def atom_shape(
        atom: rules.Derivation | rules.NoSuccessor,
    ) -> tuple[str, str | None, str | None, int, Fraction | None]:
        mass = None if law is None else law.mass_for(atom.canonical_identity)
        if isinstance(atom, rules.NoSuccessor):
            return ("no-successor", None, None, 0, mass)
        continuation = (
            "stop" if isinstance(atom.continuation, rules.Stop) else "continue"
        )
        return (
            "derivation",
            atom.progress.value,
            continuation,
            len(atom.replacement.entries),
            mass,
        )

    source_atoms = tuple(sorted(atom_shape(atom) for atom in support.atoms))
    fresh_binding_counts = tuple(
        sorted(
            len(atom.fresh_bindings)
            if isinstance(atom, program.AppliedDerivation)
            else 0
            for atom in actual.applied_atoms.atoms
        )
    )
    return CompleteMechanicsFingerprint(
        support.presentation.value,
        source_atoms,
        len(actual.applied_atoms.atoms),
        fresh_binding_counts,
        len(actual.no_successor_partition.atoms),
        (
            _runtime_cardinality(actual.outcome_atom_cardinality),
            _runtime_cardinality(actual.derivation_cardinality),
            _runtime_cardinality(actual.successor_cardinality),
        ),
        tuple(
            sorted(
                len(fiber.derivations)
                for fiber in actual.successor_quotient_with_derivation_fibers.atoms
            )
        ),
        (
            _runtime_measure(actual.applied_atom_measure),
            _runtime_measure(actual.successor_submeasure),
            _runtime_measure(actual.no_successor_submeasure),
        ),
        (
            support.relation is not None,
            actual.applied_atoms.relation is not None,
            actual.successor_quotient_with_derivation_fibers.relation is not None,
        ),
    )


def _assert_non_native_case(case_id: str) -> None:
    oracle = _ORACLES_BY_ID[case_id]
    execution = runtime_ct12_fixture(case_id)
    actual = execution.result

    assert isinstance(actual, program.ApplicationComplete)
    assert_closed_descriptor(execution.simple_program)
    assert_closed_descriptor(actual)
    assert actual.evidence.phases == tuple(program.ApplicationPhase)
    assert actual.evidence.program_identity == execution.simple_program.canonical_identity
    assert actual.evidence.input_configuration_identity == execution.source.identity
    assert _runtime_mechanics_fingerprint(actual) == _oracle_mechanics_fingerprint(
        oracle.expected
    )

    for atom in actual.source_outcomes.support.atoms:
        assert atom.provenance
        assert atom.witness.descriptor.version == 1
        assert atom.certificate.version == 1
        if isinstance(atom, rules.Derivation):
            assert atom.replacement.totality_evidence.kind is rules.CertificateKind.TOTALITY
    for atom in actual.applied_atoms.atoms:
        assert (
            len(atom.output_trace_lineage.path)
            == len(atom.input_trace_lineage.path) + 1
        )
        assert atom.evidence.application_identity == actual.evidence.application_identity


def test_variable_structure_and_stochastic_fixtures_match_completely() -> None:
    for case in test_oracles.CT12_CASES[6:14]:
        _assert_non_native_case(case.case_id)


def test_differential_and_intensional_fixtures_use_exact_tiny_oracles() -> None:
    for case in test_oracles.CT12_CASES[14:]:
        _assert_non_native_case(case.case_id)
