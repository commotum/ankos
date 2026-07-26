"""Canonical, fail-closed serialization for expanded semantic values.

The codec is deliberately catalog-free.  It serializes only the closed scalar
algebra and the explicitly registered frozen records and enums owned by the
seven semantic modules.  Registry membership is written out below; dataclass
inspection is used only to fail module initialization when a declared schema
drifts, never to discover a constructor or a wire path.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import hmac
import json
import re
from types import MappingProxyType
from typing import Generic, TypeAlias, TypeVar

from . import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
)


T = TypeVar("T")

_PROGRAM_SCHEMA_TAG = "ca.simple-program"
_PROGRAM_SCHEMA_VERSION = 1
_DIGEST_PREFIX = "sha256:"
_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
_DECIMAL_RE = re.compile(r"(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z")
_WIRE_TAG_RE = re.compile(
    r"ca(?:\.[a-z][a-z0-9]*(?:-[a-z0-9]+)*)+\Z"
)


# ---------------------------------------------------------------------------
# Public decode boundary
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DecodeFault:
    """Closed reason that canonical decoding could not produce a value."""

    phase: str
    reason: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class DecodeRejected:
    """Fail-closed decode result with no partially restored value."""

    fault: DecodeFault


@dataclass(frozen=True)
class Decoded(Generic[T]):
    """Successfully decoded and validated semantic value."""

    value: T


DecodeResult: TypeAlias = Decoded[T] | DecodeRejected


# ---------------------------------------------------------------------------
# Closed production schema registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _SchemaRow:
    """One explicit owner-type schema (enum values are variants of one type)."""

    owner: str
    type_name: str
    tag: str
    version: int
    fields: tuple[str, ...]
    enum_values: tuple[str, ...]
    value_type: type[object]


def _record(
    value_type: type[object],
    tag: str,
    field_names: tuple[str, ...],
) -> _SchemaRow:
    return _SchemaRow(
        value_type.__module__,
        value_type.__name__,
        tag,
        1,
        field_names,
        (),
        value_type,
    )


def _enum(
    value_type: type[object],
    tag: str,
    values: tuple[str, ...],
) -> _SchemaRow:
    return _SchemaRow(
        value_type.__module__,
        value_type.__name__,
        tag,
        1,
        ("value",),
        values,
        value_type,
    )


_SCHEMAS = (
    # loci enums
    _enum(loci.LocusKind, "ca.loci.locus-kind", (
        "coordinate", "named", "occurrence", "path", "span", "port",
        "interface", "product", "graph-element", "field-point", "continuous",
        "intensional", "fresh",
    )),
    _enum(loci.SelectorPrimitive, "ca.loci.selector-primitive", (
        "selector.literal", "selector.equal", "selector.tagged",
        "selector.relative", "selector.metric", "selector.path",
        "selector.incidence", "selector.reachable",
        "selector.field-restriction", "selector.differential-germ",
        "selector.history", "selector.membership", "selector.and",
        "selector.or", "selector.not",
    )),
    _enum(loci.RegionKind, "ca.loci.region-kind", (
        "literal", "all-support", "current-support", "relative", "product",
        "union", "intersection", "difference", "span", "path",
        "matched-interface", "dynamic-address", "fresh-children",
        "fresh-edges", "continuous", "differential", "intensional",
    )),
    _enum(loci.FreshTemplateKind, "ca.loci.fresh-template-kind", (
        "children", "edges",
    )),
    _enum(loci.BoundaryPolicy, "ca.loci.boundary-policy", (
        "none", "fixed", "periodic", "reflective",
    )),
    _enum(loci.CarrierKind, "ca.loci.carrier-kind", (
        "record", "history", "grid", "word", "tree", "graph", "field",
        "product", "intensional",
    )),
    _enum(
        loci.ConfigurationIdentityLaw,
        "ca.loci.configuration-identity-law",
        ("exact", "bound-fresh-alpha"),
    ),
    # alphabets enums
    _enum(alphabets.ValueKind, "ca.alphabets.value-kind", (
        "tag", "product", "record", "word", "map", "graph", "field",
        "instruction", "pattern", "equation", "distribution", "symbolic",
    )),
    _enum(
        alphabets.RepresentedNumberProfile,
        "ca.alphabets.represented-number-profile",
        (
            "ieee754-binary32", "ieee754-binary64", "fixed-point", "decimal",
            "interval",
        ),
    ),
    _enum(alphabets.AlphabetKind, "ca.alphabets.alphabet-kind", (
        "enum", "ordered", "naturals", "integers", "rationals",
        "rational-interval", "modular", "algebraic", "exact-complex",
        "represented-number", "tag", "union", "product", "record", "word",
        "map", "graph", "field", "instruction", "pattern", "equation",
        "distribution", "symbolic", "structural-reference", "refinement",
    )),
    _enum(alphabets.ValueProfile, "ca.alphabets.value-profile", (
        "boolean", "integer", "rational", "algebraic", "complex",
        "represented", "symbolic", "structural", "exact",
    )),
    _enum(
        alphabets.RepresentationProfile,
        "ca.alphabets.representation-profile",
        ("exact", "lossy", "approximate"),
    ),
    # seeds/frontiers/neighborhoods enums
    _enum(seeds.ExactnessProfile, "ca.seeds.exactness-profile", (
        "exact", "represented", "symbolic",
    )),
    _enum(seeds.EntropyInterface, "ca.seeds.entropy-interface", (
        "none", "replay-key",
    )),
    _enum(seeds.ConstructionOp, "ca.seeds.construction-op", (
        "empty", "fill", "point", "sequence", "record", "grid",
    )),
    _enum(seeds.OverlayConflict, "ca.seeds.overlay-conflict", (
        "reject", "left", "right", "require-equal",
    )),
    _enum(frontiers.Effect, "ca.frontiers.effect", (
        "replace", "delete", "create",
    )),
    _enum(frontiers.WriteFrame, "ca.frontiers.write-frame", (
        "current", "successor",
    )),
    _enum(neighborhoods.ReadArity, "ca.neighborhoods.read-arity", (
        "one", "fixed", "variable", "intensional",
    )),
    _enum(neighborhoods.JoinMode, "ca.neighborhoods.join-mode", (
        "none", "target-identity", "anchor-identity", "product", "global",
    )),
    _enum(neighborhoods.GroupingKind, "ca.neighborhoods.grouping-kind", (
        "single", "fixed-chunks", "product",
    )),
    # rules enums
    _enum(rules.RulePrimitive, "ca.rules.rule-primitive", (
        "rule.literal", "rule.expression", "rule.clause-kernel",
        "rule.relation", "rule.distribution", "rule.parallel",
        "rule.differential",
    )),
    _enum(rules.ExpressionPrimitive, "ca.rules.expression-primitive", (
        "expression.literal", "expression.observation", "expression.group",
        "expression.target-reference", "expression.bound-value",
        "expression.bound-index", "expression.project",
        "expression.tuple", "expression.add", "expression.subtract",
        "expression.multiply", "expression.divide", "expression.modulo",
        "expression.count", "expression.gate", "expression.lookup",
        "expression.equal", "expression.less", "expression.less-equal",
        "expression.conditional", "expression.all", "expression.any",
        "expression.record-field", "expression.record-update",
        "expression.length", "expression.item-at", "expression.slice",
        "expression.concatenate", "expression.reverse",
        "expression.replace-at", "expression.map-lookup",
        "expression.map-update", "expression.index-of",
        "expression.index-of-tag", "expression.floor-divide",
        "expression.absolute", "expression.fractional-part",
        "expression.integer-digits", "expression.from-digits",
        "expression.maximal-runs", "expression.product-value",
        "expression.word-value", "expression.flat-map-lookup",
        "expression.map-items", "expression.filter-items",
        "expression.flat-map-items", "expression.sliding-windows",
    )),
    _enum(rules.GateKind, "ca.rules.gate-kind", (
        "any", "all", "majority", "at-least", "at-most", "exactly",
    )),
    _enum(rules.SequenceBoundary, "ca.rules.sequence-boundary", (
        "fixed", "periodic", "reflective",
    )),
    _enum(rules.CertificateKind, "ca.rules.certificate-kind", (
        "soundness", "completeness", "cardinality", "totality",
        "normalization", "measurability", "derivation", "terminality",
        "divergence", "conformance", "composition",
    )),
    _enum(rules.InfiniteCardinality, "ca.rules.infinite-cardinality", (
        "countably-infinite", "uncountable",
    )),
    _enum(rules.DispositionAction, "ca.rules.disposition-action", (
        "preserve", "replace", "delete", "absent", "create",
    )),
    _enum(rules.Progress, "ca.rules.progress", (
        "advanced", "quiescent",
    )),
    _enum(rules.NoSuccessorOutcome, "ca.rules.no-successor-outcome", (
        "terminal", "undefined", "declared-failure", "divergent",
    )),
    _enum(rules.SupportPresentation, "ca.rules.support-presentation", (
        "finite", "intensional",
    )),
    _enum(rules.ProbabilityPresentation, "ca.rules.probability-presentation", (
        "finite", "intensional",
    )),
    _enum(rules.ExistingPlanKind, "ca.rules.existing-plan-kind", (
        "by-index", "by-target", "by-locus", "preserve",
    )),
    _enum(rules.EvaluationScope, "ca.rules.evaluation-scope", (
        "once", "each-target",
    )),
    _enum(rules.ClauseSelection, "ca.rules.clause-selection", (
        "all", "first",
    )),
    _enum(
        rules.CapabilitySelectorKind,
        "ca.rules.capability-selector-kind",
        ("index", "target", "every"),
    ),
    _enum(rules.RuleFaultPhase, "ca.rules.rule-fault-phase", (
        "rule-denotation", "result-validation", "composition",
    )),
    _enum(rules.RuleFaultReason, "ca.rules.rule-fault-reason", (
        "invalid-descriptor", "incompatible-read-view",
        "incompatible-writable", "evaluation-failure",
        "no-matching-clause", "incomplete-disposition",
        "unauthorized-effect", "conflicting-effect",
        "invalid-probability-law", "unsupported-exactness",
    )),
    # program enums
    _enum(program.ApplicationPhase, "ca.program.application-phase", (
        "program", "input", "frontier", "neighborhood", "join",
        "rule-denotation", "result-validation", "fresh-binding", "commit",
        "successor", "quotient-measure",
    )),
    _enum(
        program.SamplerProfile,
        "ca.program.sampler-profile",
        ("sha256-rejection-v1",),
    ),
    _enum(
        program.NumericProfile,
        "ca.program.numeric-profile",
        ("fraction-tickets-v1",),
    ),
    _enum(program.TruncationCause, "ca.program.truncation-cause", (
        "depth-bound", "intensional-support", "resource-exhausted",
        "cancelled", "pruned",
    )),
    # loci records
    _record(
        loci.Locus,
        "ca.loci.locus",
        ("kind", "scope", "path", "version"),
    ),
    _record(
        loci.FreshReference,
        "ca.loci.fresh-reference",
        ("namespace", "local_key", "parent", "interface", "version"),
    ),
    _record(
        loci.SelectorExpr,
        "ca.loci.selector-expr",
        ("primitive", "arguments", "children", "version"),
    ),
    _record(
        loci.FreshTemplate,
        "ca.loci.fresh-template",
        (
            "kind", "namespace", "local_keys", "parent_region",
            "interface_regions", "version",
        ),
    ),
    _record(
        loci.Region,
        "ca.loci.region",
        (
            "kind", "name", "loci", "fresh", "parts", "offsets", "relation",
            "templates", "version",
        ),
    ),
    _record(
        loci.CarrierContract,
        "ca.loci.carrier-contract",
        ("kind", "rank", "shape", "axes", "version", "identity_law"),
    ),
    _record(
        loci.Boundary,
        "ca.loci.boundary",
        ("policy", "exterior", "version"),
    ),
    _record(
        loci.Carrier,
        "ca.loci.carrier",
        ("contract", "boundary", "attributes", "version"),
    ),
    _record(
        loci.StructuralRelation,
        "ca.loci.structural-relation",
        ("tag", "arguments", "version"),
    ),
    _record(
        loci.FiniteConfiguration,
        "ca.loci.finite-configuration",
        ("carrier", "entries", "structure", "version"),
    ),
    _record(
        loci.IntensionalConfiguration,
        "ca.loci.intensional-configuration",
        ("contract", "relation", "identity_evidence", "version"),
    ),
    # alphabet records
    _record(
        alphabets.AlgebraicNumber,
        "ca.alphabets.algebraic-number",
        ("polynomial", "isolating_interval", "root_index", "version"),
    ),
    _record(
        alphabets.ExactComplex,
        "ca.alphabets.exact-complex",
        ("real", "imaginary", "version"),
    ),
    _record(
        alphabets.StructuralReference,
        "ca.alphabets.structural-reference",
        ("reference", "version"),
    ),
    _record(
        alphabets.ValueNode,
        "ca.alphabets.value-node",
        ("kind", "tag", "items", "fields", "version"),
    ),
    _record(
        alphabets.RepresentedNumber,
        "ca.alphabets.represented-number",
        ("profile", "representation", "version"),
    ),
    _record(
        alphabets.AlphabetDescriptor,
        "ca.alphabets.alphabet-descriptor",
        (
            "kind", "values", "scalars", "children", "fields",
            "represented_profile", "version",
        ),
    ),
    _record(
        alphabets.Alphabet,
        "ca.alphabets.alphabet",
        ("descriptor",),
    ),
    _record(
        alphabets.RepresentationPair,
        "ca.alphabets.representation-pair",
        ("source", "target", "version"),
    ),
    _record(
        alphabets.RepresentationRelation,
        "ca.alphabets.representation-relation",
        (
            "source_schema", "target_schema", "profile", "relation",
            "image_evidence", "inverse_evidence", "qualification", "version",
        ),
    ),
    # seed records
    _record(
        seeds.SeedOutputContract,
        "ca.seeds.seed-output-contract",
        (
            "configuration_contract", "value_profile", "exactness_profile",
            "entropy_interface",
        ),
    ),
    _record(
        seeds.Construction,
        "ca.seeds.construction",
        ("operation", "arguments"),
    ),
    _record(seeds.ExactSource, "ca.seeds.exact-source", ("configuration",)),
    _record(
        seeds.ConstructiveSource,
        "ca.seeds.constructive-source",
        ("construction",),
    ),
    _record(
        seeds.PartialSource,
        "ca.seeds.partial-source",
        ("configuration", "unresolved", "obligations"),
    ),
    _record(
        seeds.BernoulliLaw,
        "ca.seeds.bernoulli-law",
        (
            "support", "probability_true", "false_value", "true_value",
            "boundary",
        ),
    ),
    _record(
        seeds.UniformTupleLaw,
        "ca.seeds.uniform-tuple-law",
        ("length", "value_count", "excluded"),
    ),
    _record(
        seeds.IntensionalProbabilityLaw,
        "ca.seeds.intensional-probability-law",
        ("binder", "relation"),
    ),
    _record(
        seeds.LawSource,
        "ca.seeds.law-source",
        ("law", "construction"),
    ),
    _record(
        seeds.IntensionalSource,
        "ca.seeds.intensional-source",
        ("binder", "relation"),
    ),
    _record(seeds.ProductPart, "ca.seeds.product-part", ("key", "seed")),
    _record(seeds.ProductSource, "ca.seeds.product-source", ("parts",)),
    _record(
        seeds.OverlaySource,
        "ca.seeds.overlay-source",
        ("parts", "conflict"),
    ),
    _record(
        seeds.MixturePart,
        "ca.seeds.mixture-part",
        ("weight", "seed"),
    ),
    _record(seeds.MixtureSource, "ca.seeds.mixture-source", ("parts",)),
    _record(
        seeds.ProductLawSource,
        "ca.seeds.product-law-source",
        ("parts",),
    ),
    _record(
        seeds.RefinedSource,
        "ca.seeds.refined-source",
        ("source", "constraint"),
    ),
    _record(
        seeds.SeedDenotation,
        "ca.seeds.seed-denotation",
        ("source", "output_contract"),
    ),
    _record(
        seeds.Seed,
        "ca.seeds.seed",
        ("source", "output_contract", "version"),
    ),
    # frontier records
    _record(
        frontiers.EffectProfile,
        "ca.frontiers.effect-profile",
        ("existing", "fresh"),
    ),
    _record(
        frontiers.TargetContract,
        "ca.frontiers.target-contract",
        ("locus_kind", "value_profile", "frame"),
    ),
    _record(
        frontiers.FreshNamespace,
        "ca.frontiers.fresh-namespace",
        ("namespace", "parent"),
    ),
    _record(
        frontiers.ReconstructionLens,
        "ca.frontiers.reconstruction-lens",
        ("target", "frame"),
    ),
    _record(
        frontiers.ReconstructionEvidence,
        "ca.frontiers.reconstruction-evidence",
        ("snapshot_identity", "lenses", "preserves_outside", "complete"),
    ),
    _record(
        frontiers.ExistingCapability,
        "ca.frontiers.existing-capability",
        ("target", "contract", "effects"),
    ),
    _record(
        frontiers.FreshCapability,
        "ca.frontiers.fresh-capability",
        ("target", "contract", "namespace"),
    ),
    _record(
        frontiers.WritableCapabilities,
        "ca.frontiers.writable-capabilities",
        ("snapshot_identity", "existing", "fresh", "reconstruction"),
    ),
    _record(
        frontiers.IntensionalReconstructionEvidence,
        "ca.frontiers.intensional-reconstruction-evidence",
        (
            "snapshot_identity", "region", "target_contract",
            "preserves_outside", "complete", "version",
        ),
    ),
    _record(
        frontiers.IntensionalWritableCapabilities,
        "ca.frontiers.intensional-writable-capabilities",
        (
            "snapshot_identity", "region", "effect_profile",
            "target_contract", "reconstruction", "version",
        ),
    ),
    _record(
        frontiers.WritableRegion,
        "ca.frontiers.writable-region",
        (
            "descriptor", "configuration_contract", "value_profile",
            "effect_profile", "target_contract", "fresh_namespace",
            "exactness_profile", "parts", "version",
        ),
    ),
    # neighborhood records
    _record(
        neighborhoods.ReadField,
        "ca.neighborhoods.read-field",
        ("key", "arity", "size"),
    ),
    _record(
        neighborhoods.ResultShape,
        "ca.neighborhoods.result-shape",
        ("fields",),
    ),
    _record(
        neighborhoods.ReadDependency,
        "ca.neighborhoods.read-dependency",
        ("key", "region", "selector", "exactness_profile", "version"),
    ),
    _record(
        neighborhoods.JoinShape,
        "ca.neighborhoods.join-shape",
        ("mode", "fields"),
    ),
    _record(neighborhoods.Present, "ca.neighborhoods.present", ("value",)),
    _record(
        neighborhoods.BoundaryDefault,
        "ca.neighborhoods.boundary-default",
        ("value", "evidence", "boundary"),
    ),
    _record(neighborhoods.Absent, "ca.neighborhoods.absent", ("evidence",)),
    _record(
        neighborhoods.Observation,
        "ca.neighborhoods.observation",
        ("target", "state", "anchor"),
    ),
    _record(
        neighborhoods.GroupKey,
        "ca.neighborhoods.group-key",
        ("anchor", "channel"),
    ),
    _record(
        neighborhoods.ObservationGroup,
        "ca.neighborhoods.observation-group",
        ("key", "indices", "anchor"),
    ),
    _record(
        neighborhoods.ReadableView,
        "ca.neighborhoods.readable-view",
        (
            "snapshot_identity", "observations", "groups", "join_shape",
            "dependencies", "version",
        ),
    ),
    _record(
        neighborhoods.IntensionalReadableView,
        "ca.neighborhoods.intensional-readable-view",
        (
            "snapshot_identity", "dependencies", "join_shape",
            "configuration_relation", "version",
        ),
    ),
    _record(
        neighborhoods.GroupingPlan,
        "ca.neighborhoods.grouping-plan",
        ("kind", "key", "chunk_size"),
    ),
    _record(
        neighborhoods.ReadableField,
        "ca.neighborhoods.readable-field",
        ("key", "region"),
    ),
    _record(
        neighborhoods.ReadableRegion,
        "ca.neighborhoods.readable-region",
        (
            "descriptor", "configuration_contract", "value_profile",
            "result_shape", "join_shape", "grouping", "parts",
            "exactness_profile", "selector", "version",
        ),
    ),
    # rule records
    _record(
        rules.RuleExpr,
        "ca.rules.rule-expr",
        ("primitive", "arguments", "version"),
    ),
    _record(
        rules.RuleContract,
        "ca.rules.rule-contract",
        (
            "configuration_contract", "value_profile",
            "required_read_shape", "required_join_shape",
            "required_effect_profile", "exactness_profile",
            "entropy_interface", "version",
        ),
    ),
    _record(
        rules.Certificate,
        "ca.rules.certificate",
        ("kind", "statement", "version"),
    ),
    _record(rules.ExactlyZero, "ca.rules.exactly-zero", ("evidence",)),
    _record(rules.ExactlyOne, "ca.rules.exactly-one", ("evidence",)),
    _record(
        rules.Many,
        "ca.rules.many",
        ("exact_finite_size", "infinite", "evidence"),
    ),
    _record(
        rules.Undetermined,
        "ca.rules.undetermined",
        ("reason", "obligation"),
    ),
    _record(rules.NoPayload, "ca.rules.no-payload", ()),
    _record(rules.ValuePayload, "ca.rules.value-payload", ("value",)),
    _record(
        rules.Disposition,
        "ca.rules.disposition",
        ("target", "action", "payload", "evidence", "version"),
    ),
    _record(
        rules.TotalDisposition,
        "ca.rules.total-disposition",
        ("existing", "fresh", "totality_evidence", "version"),
    ),
    _record(rules.Continue, "ca.rules.continue", ("version",)),
    _record(rules.Stop, "ca.rules.stop", ("reason", "certificate", "version")),
    _record(
        rules.Witness,
        "ca.rules.witness",
        ("identity", "descriptor", "version"),
    ),
    _record(
        rules.Derivation,
        "ca.rules.derivation",
        (
            "replacement", "progress", "continuation", "witness",
            "provenance", "certificate", "version",
        ),
    ),
    _record(
        rules.NoSuccessor,
        "ca.rules.no-successor",
        (
            "outcome", "reason", "witness", "provenance", "certificate",
            "version",
        ),
    ),
    _record(
        rules.SupportSpace,
        "ca.rules.support-space",
        (
            "presentation", "atoms", "relation", "cardinality",
            "completeness_evidence", "soundness_evidence", "version",
        ),
    ),
    _record(
        rules.AtomMass,
        "ca.rules.atom-mass",
        ("atom_identity", "mass"),
    ),
    _record(
        rules.ProbabilityLaw,
        "ca.rules.probability-law",
        (
            "presentation", "masses", "measure", "normalization_evidence",
            "measurable_space_evidence", "version",
        ),
    ),
    _record(
        rules.OutcomeSpace,
        "ca.rules.outcome-space",
        ("support", "probability_law", "projection_cardinalities", "version"),
    ),
    _record(
        rules.ProjectionCardinalities,
        "ca.rules.projection-cardinalities",
        (
            "derivations", "no_successors", "successors",
            "mapping_evidence", "version",
        ),
    ),
    _record(
        rules.ExistingPlan,
        "ca.rules.existing-plan",
        ("kind", "expressions", "targets", "version"),
    ),
    _record(
        rules.EvidenceExpression,
        "ca.rules.evidence-expression",
        ("expression", "scope", "version"),
    ),
    _record(
        rules.FormattedEvidence,
        "ca.rules.formatted-evidence",
        ("template", "expression", "version"),
    ),
    _record(
        rules.EvidenceTerm,
        "ca.rules.evidence-term",
        ("tag", "arguments", "version"),
    ),
    _record(
        rules.ProvenanceTemplate,
        "ca.rules.provenance-template",
        ("template", "expressions", "version"),
    ),
    _record(
        rules.LiteralDenotation,
        "ca.rules.literal-denotation",
        ("outcomes",),
    ),
    _record(
        rules.ExpressionDenotation,
        "ca.rules.expression-denotation",
        (
            "existing_plan", "progress", "continuation", "witness",
            "provenance", "certificate", "certificate_template",
            "provenance_templates",
        ),
    ),
    _record(
        rules.IntensionalDenotation,
        "ca.rules.intensional-denotation",
        (
            "relation", "cardinality", "completeness_evidence",
            "soundness_evidence", "probability_law",
            "projection_cardinalities",
        ),
    ),
    _record(
        rules.CapabilitySelector,
        "ca.rules.capability-selector",
        ("kind", "index", "target", "version"),
    ),
    _record(
        rules.ExistingDispositionPlan,
        "ca.rules.existing-disposition-plan",
        ("selector", "action", "value", "version"),
    ),
    _record(
        rules.FreshDispositionPlan,
        "ca.rules.fresh-disposition-plan",
        ("selector", "action", "value", "version"),
    ),
    _record(
        rules.DerivationClauseResult,
        "ca.rules.derivation-clause-result",
        (
            "existing_plans", "fresh_plans", "progress", "continuation",
            "witness", "provenance", "certificate", "existing_default",
            "fresh_default", "certificate_template", "provenance_templates",
            "version",
        ),
    ),
    _record(
        rules.NoSuccessorClauseResult,
        "ca.rules.no-successor-clause-result",
        (
            "outcome", "reason", "witness", "provenance", "certificate",
            "certificate_template", "provenance_templates", "version",
        ),
    ),
    _record(
        rules.RuleClause,
        "ca.rules.rule-clause",
        ("condition", "result", "mass", "version"),
    ),
    _record(
        rules.ClauseKernelDenotation,
        "ca.rules.clause-kernel-denotation",
        ("clauses", "selection", "completeness_evidence", "version"),
    ),
    _record(
        rules.ParallelDenotation,
        "ca.rules.parallel-denotation",
        ("parts",),
    ),
    _record(
        rules.RuleDescriptor,
        "ca.rules.rule-descriptor",
        ("primitive", "denotation", "version"),
    ),
    _record(
        rules.RuleFault,
        "ca.rules.rule-fault",
        ("phase", "reason", "evidence", "detail", "version"),
    ),
    _record(rules.RuleRejected, "ca.rules.rule-rejected", ("fault",)),
    _record(
        rules.RuleComplete,
        "ca.rules.rule-complete",
        ("outcome_space",),
    ),
    _record(rules.Rule, "ca.rules.rule", ("descriptor", "contract")),
    _record(
        rules.EvaluationStep,
        "ca.rules.evaluation-step",
        ("expression", "anchor", "result", "read_evidence", "version"),
    ),
    _record(
        rules.EvaluationProof,
        "ca.rules.evaluation-proof",
        ("steps", "version"),
    ),
    # program records
    _record(
        program.CompatibilityEvidence,
        "ca.program.compatibility-evidence",
        ("configuration_contract", "value_profile", "clauses"),
    ),
    _record(
        program.SimpleProgram,
        _PROGRAM_SCHEMA_TAG,
        ("seed", "alphabet", "frontier", "neighborhood", "rule"),
    ),
    _record(
        program.TraceLineage,
        "ca.program.trace-lineage",
        ("root_identity", "path", "version"),
    ),
    _record(
        program.ApplicationInput,
        "ca.program.application-input",
        ("configuration", "trace_lineage"),
    ),
    _record(
        program.FreshBinding,
        "ca.program.fresh-binding",
        ("reference", "identity"),
    ),
    _record(
        program.AppliedEvidence,
        "ca.program.applied-evidence",
        ("application_identity", "disposition_identity", "version"),
    ),
    _record(
        program.AppliedDerivation,
        "ca.program.applied-derivation",
        (
            "successor", "source", "fresh_bindings", "input_trace_lineage",
            "output_trace_lineage", "evidence",
        ),
    ),
    _record(
        program.AppliedNoSuccessor,
        "ca.program.applied-no-successor",
        (
            "source", "input_trace_lineage", "output_trace_lineage",
            "evidence",
        ),
    ),
    _record(
        program.SuccessorGroup,
        "ca.program.successor-group",
        ("successor", "derivations"),
    ),
    _record(
        program.MeasureMass,
        "ca.program.measure-mass",
        ("point_identity", "mass"),
    ),
    _record(
        program.ProgramMeasure,
        "ca.program.program-measure",
        ("masses", "total_mass", "intensional_descriptor"),
    ),
    _record(program.MeasureAbsent, "ca.program.measure-absent", ()),
    _record(
        program.MeasureAvailable,
        "ca.program.measure-available",
        ("measure",),
    ),
    _record(
        program.MeasureUnavailable,
        "ca.program.measure-unavailable",
        ("reason", "retained_source_law_and_mapping_evidence"),
    ),
    _record(
        program.ApplicationEvidence,
        "ca.program.application-evidence",
        (
            "phases", "program_identity", "input_configuration_identity",
            "readable_binding_identity", "writable_binding_identity",
            "application_identity", "canonical_rule_identity",
            "input_trace_lineage_identity",
        ),
    ),
    _record(
        program.ApplicationComplete,
        "ca.program.application-complete",
        (
            "source_outcomes", "applied_atoms", "no_successor_partition",
            "outcome_atom_cardinality", "derivation_cardinality",
            "successor_cardinality",
            "successor_quotient_with_derivation_fibers",
            "applied_atom_measure", "successor_submeasure",
            "no_successor_submeasure", "evidence",
        ),
    ),
    _record(
        program.ApplicationFault,
        "ca.program.application-fault",
        ("phase", "reason", "evidence", "attempted_phases"),
    ),
    _record(
        program.ApplicationRejected,
        "ca.program.application-rejected",
        ("fault",),
    ),
    _record(
        program.DrawEvidence,
        "ca.program.draw-evidence",
        (
            "law_identity", "application_identity", "replay_key_identity",
            "subkey_identity", "coordinate", "sampler_profile",
            "numeric_profile", "selected_witness_identity",
            "rejection_rounds", "version",
        ),
    ),
    _record(
        program.SeedRealizationEvidence,
        "ca.program.seed-realization-evidence",
        (
            "source_identity", "replay_key_identity", "selected_identity",
            "denotation", "draws",
        ),
    ),
    _record(
        program.ContinuingLeaf,
        "ca.program.continuing-leaf",
        ("configuration", "trace_lineage"),
    ),
    _record(
        program.ClosedLeaf,
        "ca.program.closed-leaf",
        ("final_configuration", "source"),
    ),
    _record(
        program.TraceEdge,
        "ca.program.trace-edge",
        ("parent_lineage", "child_lineage", "applied_atom_identity"),
    ),
    _record(
        program.RawTrace,
        "ca.program.raw-trace",
        (
            "roots", "applications", "derivation_edges", "lineage_graph",
            "seed_evidence", "draw_evidence",
        ),
    ),
    _record(
        program.RolloutComplete,
        "ca.program.rollout-complete",
        ("raw_trace", "closed_leaves"),
    ),
    _record(
        program.RolloutTruncated,
        "ca.program.rollout-truncated",
        ("raw_trace", "continuing_leaves", "cause"),
    ),
    _record(
        program.RolloutFault,
        "ca.program.rollout-fault",
        ("reason", "evidence"),
    ),
    _record(
        program.RolloutRejected,
        "ca.program.rollout-rejected",
        ("fault",),
    ),
)


def _validate_registry() -> None:
    owner_modules = (
        loci,
        alphabets,
        seeds,
        frontiers,
        neighborhoods,
        rules,
        program,
    )
    owners = {owner.__name__ for owner in owner_modules}
    if len(_SCHEMAS) != 179:
        raise RuntimeError("canonical schema registry must contain 179 owner types")
    if len({row.value_type for row in _SCHEMAS}) != len(_SCHEMAS):
        raise RuntimeError("canonical schema registry contains a duplicate type")
    if len({row.tag for row in _SCHEMAS}) != len(_SCHEMAS):
        raise RuntimeError("canonical schema registry contains a duplicate tag")
    variant_count = sum(
        len(row.enum_values) if row.enum_values else 1 for row in _SCHEMAS
    )
    if variant_count != 418:
        raise RuntimeError("canonical schema registry must contain 418 variants")

    public_sealed_types: set[type[object]] = set()
    for owner in owner_modules:
        for name, value in vars(owner).items():
            if (
                name.startswith("_")
                or not isinstance(value, type)
                or value.__module__ != owner.__name__
            ):
                continue
            parameters = getattr(value, "__dataclass_params__", None)
            if issubclass(value, Enum) or (
                is_dataclass(value)
                and parameters is not None
                and parameters.frozen
            ):
                public_sealed_types.add(value)
    registered_types = {row.value_type for row in _SCHEMAS}
    if public_sealed_types != registered_types:
        missing = tuple(
            sorted(
                f"{value.__module__}.{value.__name__}"
                for value in public_sealed_types - registered_types
            )
        )
        stale = tuple(
            sorted(
                f"{value.__module__}.{value.__name__}"
                for value in registered_types - public_sealed_types
            )
        )
        raise RuntimeError(
            "canonical schema registry does not match the public sealed "
            f"owner surface; missing={missing!r}, stale={stale!r}"
        )

    for row in _SCHEMAS:
        value_type = row.value_type
        if row.owner not in owners or value_type.__module__ != row.owner:
            raise RuntimeError(f"invalid canonical schema owner for {row.tag}")
        if value_type.__name__ != row.type_name or row.version != 1:
            raise RuntimeError(f"invalid canonical schema identity for {row.tag}")
        if _WIRE_TAG_RE.fullmatch(row.tag) is None:
            raise RuntimeError(
                f"invalid canonical schema tag syntax for {row.tag!r}"
            )
        if row.enum_values:
            if not issubclass(value_type, Enum):
                raise RuntimeError(f"{row.tag} is declared as a non-enum")
            actual = tuple(
                member.value for member in value_type.__members__.values()
            )
            if actual != row.enum_values or any(
                type(value) is not str for value in actual
            ):
                raise RuntimeError(f"enum schema drift for {row.tag}")
        else:
            parameters = getattr(value_type, "__dataclass_params__", None)
            if (
                not is_dataclass(value_type)
                or parameters is None
                or not parameters.frozen
            ):
                raise RuntimeError(f"{row.tag} is not a frozen dataclass")
            actual_fields = tuple(field.name for field in fields(value_type))
            if actual_fields != row.fields:
                raise RuntimeError(f"record schema drift for {row.tag}")

    program_row = next(
        row for row in _SCHEMAS if row.value_type is program.SimpleProgram
    )
    if (
        program_row.tag != _PROGRAM_SCHEMA_TAG
        or program_row.version != _PROGRAM_SCHEMA_VERSION
        or program_row.fields
        != ("seed", "alphabet", "frontier", "neighborhood", "rule")
    ):
        raise RuntimeError("the canonical program schema is not exactly five-field v1")


_validate_registry()

_SCHEMA_BY_TYPE = MappingProxyType(
    {row.value_type: row for row in _SCHEMAS}
)
_SCHEMA_BY_TAG = MappingProxyType({row.tag: row for row in _SCHEMAS})


def _schema_rows() -> tuple[_SchemaRow, ...]:
    """Return the immutable closed registry for executable inventory joins."""

    return _SCHEMAS


# ---------------------------------------------------------------------------
# Canonical scalar and structural nodes
# ---------------------------------------------------------------------------


_NONE_TAG = "ca.scalar.none"
_BOOLEAN_TAG = "ca.scalar.boolean"
_INTEGER_TAG = "ca.scalar.integer"
_STRING_TAG = "ca.scalar.string"
_RATIONAL_TAG = "ca.scalar.rational"
_TUPLE_TAG = "ca.tuple"
_PRIMITIVE_TAGS = frozenset(
    {
        _NONE_TAG,
        _BOOLEAN_TAG,
        _INTEGER_TAG,
        _STRING_TAG,
        _RATIONAL_TAG,
        _TUPLE_TAG,
    }
)


class _DecodeFailure(Exception):
    def __init__(
        self,
        phase: str,
        reason: str,
        *evidence: str,
    ) -> None:
        super().__init__(reason)
        self.fault = DecodeFault(phase, reason, tuple(evidence))


class _DuplicateField(ValueError):
    def __init__(self, field: str) -> None:
        super().__init__(field)
        self.field = field


class _JsonNumberRejected(ValueError):
    pass


class _JsonInteger(str):
    pass


def _int_to_decimal(value: int) -> str:
    """Render an arbitrary Python integer without the interpreter digit cap."""

    if value == 0:
        return "0"
    negative = value < 0
    remaining = -value if negative else value
    chunks: list[int] = []
    while remaining:
        remaining, chunk = divmod(remaining, 1_000_000_000)
        chunks.append(chunk)
    rendered = str(chunks.pop())
    while chunks:
        rendered += f"{chunks.pop():09d}"
    return f"-{rendered}" if negative else rendered


def _decimal_to_int(value: str) -> int:
    """Parse canonical arbitrary signed decimal without the digit cap."""

    if type(value) is not str or _DECIMAL_RE.fullmatch(value) is None:
        raise _DecodeFailure(
            "scalar",
            "noncanonical-integer",
            "expected canonical signed decimal text",
        )
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    result = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start : start + 9]
        result = result * (10 ** len(chunk)) + int(chunk)
    return -result if negative else result


def _node(tag: str, payload: dict[str, object]) -> dict[str, object]:
    return {"tag": tag, "version": 1, "payload": payload}


def _exact_structure_equal(
    left: object,
    right: object,
    active: set[tuple[int, int]] | None = None,
) -> bool:
    """Compare closed values without Python's bool/int equality collapse."""

    if type(left) is not type(right):
        return False
    if left is None or type(left) in (bool, int, str, Fraction):
        return left == right
    if isinstance(left, Enum):
        return left is right
    if active is None:
        active = set()
    pair = (id(left), id(right))
    if pair in active:
        return False
    active.add(pair)
    try:
        if type(left) is tuple:
            return len(left) == len(right) and all(
                _exact_structure_equal(
                    left_item,
                    right_item,
                    active,
                )
                for left_item, right_item in zip(left, right, strict=True)
            )
        schema = _SCHEMA_BY_TYPE.get(type(left))
        if schema is None or schema.enum_values:
            return False
        return all(
            _exact_structure_equal(
                getattr(left, field_name),
                getattr(right, field_name),
                active,
            )
            for field_name in schema.fields
        )
    finally:
        active.remove(pair)


def _encode_node(value: object) -> dict[str, object]:
    value_type = type(value)
    if value is None:
        return _node(_NONE_TAG, {})
    if value_type is bool:
        return _node(_BOOLEAN_TAG, {"value": value})
    if value_type is int:
        return _node(_INTEGER_TAG, {"value": _int_to_decimal(value)})
    if value_type is str:
        return _node(_STRING_TAG, {"value": value})
    if value_type is Fraction:
        return _node(
            _RATIONAL_TAG,
            {
                "numerator": _int_to_decimal(value.numerator),
                "denominator": _int_to_decimal(value.denominator),
            },
        )
    if value_type is tuple:
        return _node(
            _TUPLE_TAG,
            {"items": [_encode_node(item) for item in value]},
        )

    schema = _SCHEMA_BY_TYPE.get(value_type)
    if schema is None:
        raise TypeError(
            f"{value_type.__module__}.{value_type.__qualname__} "
            "is not in the closed canonical schema registry"
        )
    if schema.enum_values:
        member_value = value.value
        if type(member_value) is not str or member_value not in schema.enum_values:
            raise TypeError(f"{schema.tag} has an undeclared enum value")
        try:
            canonical_member = schema.value_type(member_value)
        except (TypeError, ValueError) as error:
            raise TypeError(
                f"{schema.tag} is not a canonical enum member"
            ) from error
        if canonical_member is not value:
            raise TypeError(f"{schema.tag} is not a canonical enum member")
        return _node(schema.tag, {"value": member_value})
    try:
        field_values = tuple(
            getattr(value, field_name) for field_name in schema.fields
        )
        reconstructed = schema.value_type(
            **dict(zip(schema.fields, field_values, strict=True))
        )
        reconstructed_values = tuple(
            getattr(reconstructed, field_name)
            for field_name in schema.fields
        )
        if any(
            not _exact_structure_equal(original, canonical)
            for original, canonical in zip(
                field_values,
                reconstructed_values,
                strict=True,
            )
        ):
            raise ValueError("constructor normalization changed forged fields")
    except Exception as error:
        raise TypeError(
            f"{schema.tag} is not a validated canonical instance"
        ) from error
    payload = {
        field_name: _encode_node(field_value)
        for field_name, field_value in zip(
            schema.fields,
            field_values,
            strict=True,
        )
    }
    return _node(schema.tag, payload)


def _canonical_json(value: object) -> bytes:
    rendered = json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return rendered.encode("utf-8")


def _derived_digest(core: dict[str, object]) -> str:
    return _DIGEST_PREFIX + sha256(_canonical_json(core)).hexdigest()


def _exact_fields(
    value: object,
    expected: tuple[str, ...],
    *,
    phase: str,
    subject: str,
) -> dict[str, object]:
    if type(value) is not dict:
        raise _DecodeFailure(phase, "invalid-object", f"{subject} must be an object")
    actual = tuple(value)
    actual_set = set(actual)
    expected_set = set(expected)
    missing = tuple(sorted(expected_set - actual_set))
    extra = tuple(sorted(actual_set - expected_set))
    if missing:
        raise _DecodeFailure(
            phase,
            "missing-field",
            subject,
            *missing,
        )
    if extra:
        raise _DecodeFailure(
            phase,
            "extra-field",
            subject,
            *extra,
        )
    return value


def _require_version(value: object, *, tag: str) -> None:
    if type(value) is not _JsonInteger:
        raise _DecodeFailure(
            "schema",
            "invalid-version",
            tag,
            "schema version must be the JSON integer 1",
        )
    if value != "1":
        raise _DecodeFailure("schema", "unknown-version", tag, str(value))


def _decode_node(node: object) -> object:
    record = _exact_fields(
        node,
        ("tag", "version", "payload"),
        phase="schema",
        subject="node",
    )
    tag = record["tag"]
    if type(tag) is not str:
        raise _DecodeFailure("schema", "invalid-tag", "tag must be a string")
    _require_version(record["version"], tag=tag)
    payload = record["payload"]

    if tag == _NONE_TAG:
        _exact_fields(payload, (), phase="primitive", subject=tag)
        return None
    if tag == _BOOLEAN_TAG:
        body = _exact_fields(
            payload, ("value",), phase="primitive", subject=tag
        )
        if type(body["value"]) is not bool:
            raise _DecodeFailure("primitive", "invalid-boolean", tag)
        return body["value"]
    if tag == _INTEGER_TAG:
        body = _exact_fields(
            payload, ("value",), phase="primitive", subject=tag
        )
        return _decimal_to_int(body["value"])
    if tag == _STRING_TAG:
        body = _exact_fields(
            payload, ("value",), phase="primitive", subject=tag
        )
        if type(body["value"]) is not str:
            raise _DecodeFailure("primitive", "invalid-string", tag)
        return body["value"]
    if tag == _RATIONAL_TAG:
        body = _exact_fields(
            payload,
            ("numerator", "denominator"),
            phase="primitive",
            subject=tag,
        )
        numerator = _decimal_to_int(body["numerator"])
        denominator = _decimal_to_int(body["denominator"])
        if denominator <= 0:
            raise _DecodeFailure(
                "scalar",
                "noncanonical-rational",
                "denominator must be positive",
            )
        result = Fraction(numerator, denominator)
        if (
            _int_to_decimal(result.numerator) != body["numerator"]
            or _int_to_decimal(result.denominator) != body["denominator"]
        ):
            raise _DecodeFailure(
                "scalar",
                "noncanonical-rational",
                "rational must be normalized",
            )
        return result
    if tag == _TUPLE_TAG:
        body = _exact_fields(
            payload, ("items",), phase="primitive", subject=tag
        )
        items = body["items"]
        if type(items) is not list:
            raise _DecodeFailure("primitive", "invalid-tuple", tag)
        return tuple(_decode_node(item) for item in items)

    schema = _SCHEMA_BY_TAG.get(tag)
    if schema is None:
        reason = (
            "unknown-primitive"
            if tag.startswith("ca.scalar.") or tag.startswith("ca.tuple")
            else "unknown-tag"
        )
        raise _DecodeFailure("schema", reason, tag)
    if schema.enum_values:
        body = _exact_fields(
            payload, ("value",), phase="schema", subject=tag
        )
        member_value = body["value"]
        if type(member_value) is not str or member_value not in schema.enum_values:
            raise _DecodeFailure("schema", "unknown-enum-value", tag)
        try:
            return schema.value_type(member_value)
        except (TypeError, ValueError) as error:
            raise _DecodeFailure(
                "reconstruction",
                "invalid-enum",
                tag,
                type(error).__name__,
            ) from None

    body = _exact_fields(
        payload,
        schema.fields,
        phase="schema",
        subject=tag,
    )
    try:
        arguments = {
            field_name: _decode_node(body[field_name])
            for field_name in schema.fields
        }
        return schema.value_type(**arguments)
    except _DecodeFailure:
        raise
    except Exception as error:
        raise _DecodeFailure(
            "reconstruction",
            "invalid-descriptor",
            tag,
            type(error).__name__,
        ) from None


# ---------------------------------------------------------------------------
# Strict JSON boundary and public operations
# ---------------------------------------------------------------------------


def _object_without_duplicates(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateField(key)
        result[key] = value
    return result


def _reject_float(_: str) -> object:
    raise _JsonNumberRejected("floating JSON numbers are unsupported")


def _reject_constant(_: str) -> object:
    raise _JsonNumberRejected("non-finite JSON numbers are unsupported")


def _plain_json(value: object) -> object:
    """Convert parser number tokens to canonical JSON numbers for hashing."""

    if type(value) is _JsonInteger:
        if _DECIMAL_RE.fullmatch(value) is None:
            raise _DecodeFailure(
                "canonical",
                "noncanonical-json-number",
                str(value),
            )
        return _decimal_to_int(str(value))
    if type(value) is list:
        return [_plain_json(item) for item in value]
    if type(value) is dict:
        return {key: _plain_json(item) for key, item in value.items()}
    return value


def dumps(value: T) -> bytes:
    """Encode one validated public semantic value canonically."""

    core = _encode_node(value)
    envelope = dict(core)
    envelope["digest"] = _derived_digest(core)
    return _canonical_json(envelope)


def loads(data: bytes) -> DecodeResult[T]:
    """Decode one canonical value or return a typed rejection.

    The function is total over untrusted inputs: malformed or unsupported data
    becomes :class:`DecodeRejected`; no partially reconstructed value escapes.
    """

    if type(data) is not bytes:
        return DecodeRejected(
            DecodeFault(
                "input",
                "unsupported-input",
                ("canonical input must be exact bytes",),
            )
        )
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        return DecodeRejected(
            DecodeFault(
                "input",
                "malformed-utf8",
                (f"offset:{error.start}",),
            )
        )

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_int=_JsonInteger,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
        envelope = _exact_fields(
            parsed,
            ("tag", "version", "payload", "digest"),
            phase="envelope",
            subject="root",
        )
        digest = envelope["digest"]
        if type(digest) is not str or _DIGEST_RE.fullmatch(digest) is None:
            raise _DecodeFailure(
                "integrity",
                "invalid-digest",
                "expected sha256:<64 lowercase hex digits>",
            )
        core = {
            "tag": envelope["tag"],
            "version": envelope["version"],
            "payload": envelope["payload"],
        }
        plain_core = _plain_json(core)
        if type(plain_core) is not dict:
            raise _DecodeFailure("envelope", "invalid-object", "root")
        expected_digest = _derived_digest(plain_core)
        if not hmac.compare_digest(digest, expected_digest):
            raise _DecodeFailure("integrity", "forged-digest", digest)

        value = _decode_node(core)
        canonical = dumps(value)
        if canonical != data:
            raise _DecodeFailure(
                "canonical",
                "noncanonical-encoding",
                "accepted values must re-encode byte-for-byte",
            )
        return Decoded(value)  # type: ignore[arg-type]
    except _DuplicateField as error:
        return DecodeRejected(
            DecodeFault("json", "duplicate-field", (error.field,))
        )
    except _JsonNumberRejected as error:
        return DecodeRejected(
            DecodeFault("json", "unsupported-number", (str(error),))
        )
    except json.JSONDecodeError as error:
        return DecodeRejected(
            DecodeFault(
                "json",
                "malformed-json",
                (f"line:{error.lineno}", f"column:{error.colno}"),
            )
        )
    except _DecodeFailure as error:
        return DecodeRejected(error.fault)
    except (RecursionError, UnicodeError, ValueError, TypeError) as error:
        return DecodeRejected(
            DecodeFault(
                "decode",
                "invalid-input",
                (type(error).__name__,),
            )
        )


__all__ = [
    "DecodeFault",
    "DecodeRejected",
    "DecodeResult",
    "Decoded",
    "dumps",
    "loads",
]
