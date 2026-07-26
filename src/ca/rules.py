"""Closed Rule denotations and their complete result algebra.

The Goal 7 target layer in this module owns sealed Rule ASTs/combinators,
finite or intensional outcome support, exact cardinality and probability-law
records, total writable dispositions, witnesses, provenance, progress,
continuation, and Rule-level rejection. It does not commit configurations,
draw samples, run solvers, traverse rollouts, or dispatch through catalog or
family identities. ``program.py`` maps these complete Rule results through the
single generic reconstruction and commit law.

The target ``Rule(descriptor=...)`` class cannot coexist truthfully with the
current callable recipe class. Non-colliding target records and factories are
therefore inert above the complete 0.1 implementation until the atomic G7-01
cutover.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Generic, Literal, NoReturn, TypeAlias, TypeVar


C = TypeVar("C")
W = TypeVar("W")
A = TypeVar("A")

RuleScalar: TypeAlias = bool | int | Fraction | str


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.1: Singular Rule Primitives
# ---------------------------------------------------------------------------


class RulePrimitive(Enum):
    """Closed Rule-denotation primitives."""

    PRODUCT = "rule.product"
    LOOKUP = "rule.lookup"
    PARALLEL = "rule.parallel"
    RELATION = "rule.relation"
    DISTRIBUTION = "rule.distribution"
    DIFFERENTIAL = "rule.differential"


class RuleResultPrimitive(Enum):
    """Closed Rule-result primitives."""

    TOTAL_DISPOSITION = "rule-result.total-disposition"
    FINITE_SUPPORT = "rule-result.finite-support"
    INTENSIONAL_SUPPORT = "rule-result.intensional-support"
    CARDINALITY = "rule-result.cardinality"
    PROBABILITY_LAW = "rule-result.probability-law"
    WITNESS = "rule-result.witness"
    MEASURE = "rule-result.measure"


@dataclass(frozen=True)
class RuleDescriptor:
    """Compact rules-owned node shell for the unfinished closed AST."""

    primitive: RulePrimitive | RuleResultPrimitive
    arguments: tuple[RuleScalar | "RuleDescriptor", ...]


def _not_implemented() -> NoReturn:
    """Raise the standard error for an unfinished Goal 7 Rule factory."""

    raise NotImplementedError("Goal 7 Rule scaffold is not implemented")


def table(
    input_shape: tuple[int, ...],
    outputs: tuple[RuleScalar, ...],
) -> "Rule":
    """Build one closed lookup-table denotation."""

    _not_implemented()


# The target frozen ``Rule`` stores one closed descriptor. Its class name
# remains owned by the incompatible 0.1 callable recipe until G7-01.


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.2: Complete Rule Results and Composition
# ---------------------------------------------------------------------------


class Progress(Enum):
    """Whether a replacement records semantic progress."""

    ADVANCED = "advanced"
    QUIESCENT = "quiescent"


class NoSuccessorOutcome(Enum):
    """Closed reasons for a valid result with no replacement successor."""

    TERMINAL = "terminal"
    UNDEFINED = "undefined"
    DECLARED_FAILURE = "declared-failure"
    DIVERGENT = "divergent"


@dataclass(frozen=True)
class TotalDisposition(Generic[W]):
    """Closed total Preserve/Replace/Delete and Absent/Create meaning."""

    descriptor: RuleDescriptor
    totality_evidence: RuleDescriptor


CardinalityClaim: TypeAlias = RuleDescriptor
Witness: TypeAlias = RuleDescriptor
Provenance: TypeAlias = tuple[str, ...]
ProbabilityLaw: TypeAlias = RuleDescriptor


@dataclass(frozen=True)
class SupportSpace(Generic[A]):
    """Closed finite or intensional support with coverage evidence."""

    descriptor: RuleDescriptor


@dataclass(frozen=True)
class OutcomeSpace(Generic[A]):
    """Complete support plus an optional, separately declared probability law."""

    support: SupportSpace[A]
    probability_law: ProbabilityLaw | None


@dataclass(frozen=True)
class Continue:
    """Continue this witnessed derivation during rollout."""


@dataclass(frozen=True)
class Stop:
    """Stop this witnessed derivation for a closed semantic reason."""

    reason: RuleDescriptor


Continuation: TypeAlias = Continue | Stop


@dataclass(frozen=True)
class Derivation(Generic[W]):
    """One witnessed, complete replacement alternative."""

    replacement: TotalDisposition[W]
    progress: Progress
    continuation: Continuation
    witness: Witness
    provenance: Provenance


@dataclass(frozen=True)
class NoSuccessor:
    """One witnessed semantic outcome without a replacement."""

    outcome: NoSuccessorOutcome
    reason: RuleDescriptor
    witness: Witness
    provenance: Provenance


RuleAtom: TypeAlias = Derivation[W] | NoSuccessor


@dataclass(frozen=True)
class RuleFault:
    """Closed Rule-denotation or result-validation fault."""

    phase: str
    reason: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class RuleRejected:
    """Rejected Rule denotation with no authoritative result space."""

    fault: RuleFault


@dataclass(frozen=True)
class RuleComplete(Generic[C, W]):
    """Authoritative complete Rule outcome space."""

    outcome_space: OutcomeSpace[RuleAtom[W]]


RuleResult: TypeAlias = RuleComplete[C, W] | RuleRejected


def parallel(parts: tuple["Rule", ...]) -> "Rule":
    """Compose Rule denotations over one immutable read/write binding."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Goal 7 Phase 2: General Rule Families
# ---------------------------------------------------------------------------


def relation(descriptor: RuleDescriptor) -> "Rule":
    """Build a finite or intensional closed relation."""

    _not_implemented()


def distribution(descriptor: RuleDescriptor) -> "Rule":
    """Build a probability law without drawing from it."""

    _not_implemented()


def differential(descriptor: RuleDescriptor) -> "Rule":
    """Build an exact or intensional differential relation."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Goal 7 Phase 3: Presets and Aliases
# ---------------------------------------------------------------------------


def elementary(number: int) -> "Rule":
    """Build the elementary binary lookup preset."""

    _not_implemented()


# The six retained native presets remain implemented below for the 0.1
# executor. They acquire concrete closed ``rule=`` data only at G7-01.


# ===========================================================================
# Legacy 0.1 implementation retained until atomic G7-01 cutover
# ===========================================================================


UpdateFn = Callable[..., Any]

Aggregate = Literal["sum", "count"]
DecodeMode = Literal["lsb_rule_bits"]
GateType = Literal[
    "any",
    "all",
    "majority",
    "atLeast",
    "atMost",
    "exactly",
    "min",
    "max",
    "clamp",
    "ceil",
    "floor",
]


@dataclass(frozen=True)
class RuleChannel:
    """One summarized input channel for a composed rule.

    `component` indexes the corresponding neighborhood component. `pipeline`
    records the rule-type transforms applied to that component in order, such
    as exhaustive, totalistic, then gate.
    """

    component: int
    pipeline: tuple[Mapping[str, Any], ...]
    name: str | None = None
    params: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class Rule:
    """Structured rule definition or instantiated update law.

    `family` and `params` preserve the catalog recipe. `rule_id` identifies one
    concrete member of the family when applicable. `fn` stores the tiny callable
    used by `rollout.py` after instantiation.
    """

    family: str
    params: Mapping[str, Any] | None = None
    rule_id: int | None = None
    fn: UpdateFn | None = None
    channels: tuple[RuleChannel, ...] = ()
    metadata: Mapping[str, Any] | None = None


def instantiate(rule: Rule, rule_id: int) -> Rule:
    """Instantiate one concrete callable from a rule family and `rule_id`.

    `rollout.py` should call this before rollout instead of decoding private
    rule-id semantics itself.
    """

    rule_id = int(rule_id)
    metadata = dict(rule.metadata or {})

    if "R" in metadata and not 0 <= rule_id < int(metadata["R"]):
        raise ValueError(
            f"rule_id {rule_id} is outside {rule.family!r} rule range 0..{int(metadata['R']) - 1}"
        )

    if rule.family == "ar2_modular_0d":
        params = dict(rule.params or {})
        grid_a, grid_b = params.get("coefficient_grid", (16, 16))
        a = rule_id // int(grid_b) + 1
        b = rule_id % int(grid_b)
        modulus = int(params["modulus"])
        constant = int(params.get("constant", 1))

        def fn(current: Any, previous: Any) -> Any:
            return (a * current + b * previous + constant) % modulus

        metadata.update({"a": a, "b": b})

        return Rule(
            family=rule.family,
            params=rule.params,
            rule_id=rule_id,
            fn=fn,
            channels=rule.channels,
            metadata=metadata,
        )

    return Rule(
        family=rule.family,
        params=rule.params,
        rule_id=rule_id,
        fn=rule.fn,
        channels=rule.channels,
        metadata=metadata,
    )


def rule_count(rule: Rule) -> int:
    """Return the number of valid concrete rule ids for a finite rule family."""

    metadata = dict(rule.metadata or {})
    if "R" not in metadata:
        raise ValueError(f"rule family {rule.family!r} does not declare a finite rule count")
    return int(metadata["R"])


def valid_rule_ids(rule: Rule) -> range:
    """Return the valid concrete rule-id range for a finite rule family."""

    return range(rule_count(rule))


def validate(a: int, *S_i: int) -> dict[str, int]:
    """Return basic finite-rule counts from already-known channel sizes.

    Args:
        a: Output alphabet size. For binary cellular automata, `a = 2`.
        *S_i: State count for each rule-input channel. For Dyadaxes, the three
            compressed binary channels are `S_i = (2, 2, 2)`.

    Returns:
        A dict with `a`, `S`, and `R`, where `S = product(S_i)` is the number
        of input table entries and `R = a**S` is the number of possible rules.
    """

    S = 1
    for channel_state_count in S_i:
        S *= channel_state_count

    return {
        "a": a,
        "S": S,
        "R": a**S,
    }



# ---------------------------------------------------------------------------
# Phase 1 Rule-Type Primitives
# ---------------------------------------------------------------------------


def exhaustive(component: int = 0, alphabet_size: int | None = None) -> RuleChannel:
    """Represent one component by its full ordered local pattern.

    For a single binary self component, this reduces to the self value. For
    larger components, this is the ordinary exhaustive cellular-automata input
    representation over the component's deterministic read order.
    """

    params = {
        "rule_type": "exhaustive",
        "component": component,
        "alphabet_size": alphabet_size,
    }

    if alphabet_size is not None:
        params["state_count"] = alphabet_size

    return RuleChannel(
        component=component,
        pipeline=(params,),
        name="exhaustive",
        params=params,
    )


def totalistic(component: int = 0, aggregate: Aggregate = "sum") -> RuleChannel:
    """Represent one component by a permutation-invariant aggregate.

    `aggregate="sum"` handles numeric alphabets. For binary alphabets, sum is
    the active count, so `aggregate="count"` and `aggregate="sum"` are the same
    Phase 1 information when values are only `0` and `1`.
    """

    params = {
        "rule_type": "totalistic",
        "component": component,
        "aggregate": aggregate,
    }

    return RuleChannel(
        component=component,
        pipeline=(params,),
        name="totalistic",
        params=params,
    )


def gate(
    source: RuleChannel | Mapping[str, Any],
    type: GateType,
    value: int | float | None = None,
    min: int | float | None = None,
    max: int | float | None = None,
) -> RuleChannel:
    """Map a source aggregate to a smaller state, usually binary.

    Supported gate types are `any`, `all`, `majority`, `atLeast`, `atMost`,
    `exactly`, `min`, `max`, `clamp`, `ceil`, and `floor`. This is a primitive
    transform/factory, not a dataclass.
    """

    if isinstance(source, RuleChannel):
        component = source.component
        pipeline = source.pipeline
        source_params = dict(source.params or {})
    else:
        component = source["component"]
        pipeline = tuple(source.get("pipeline", ()))
        source_params = dict(source.get("params", {}))

    gate_params = {
        "rule_type": "gate",
        "type": type,
        "value": value,
        "min": min,
        "max": max,
        "state_count": 2,
    }
    params = dict(source_params)
    params.update(gate_params)

    return RuleChannel(
        component=component,
        pipeline=(*pipeline, gate_params),
        name="gate",
        params=params,
    )


def lookup(
    channels: Sequence[RuleChannel],
    alphabet_size: int,
    decode: DecodeMode = "lsb_rule_bits",
) -> Rule:
    """Build an exhaustive final lookup over compressed channel outputs.

    Dyadrads and Dyadaxes use this after compressing each neighborhood
    component to a binary channel, giving an eight-entry binary lookup for
    three channels.
    """

    channels = tuple(channels)
    params = {
        "alphabet_size": alphabet_size,
        "decode": decode,
    }
    metadata = dict(params)

    channel_state_counts = []
    for channel in channels:
        if channel.params is None or "state_count" not in channel.params:
            break
        channel_state_counts.append(channel.params["state_count"])

    if len(channel_state_counts) == len(channels):
        metadata.update(validate(alphabet_size, *channel_state_counts))

    return Rule(
        family="lookup",
        params=params,
        channels=channels,
        metadata=metadata,
    )


def compose(channels: Sequence[RuleChannel], output: Rule) -> Rule:
    """Compose channel pipelines with a final output rule.

    This is the rule-level counterpart to neighborhood composition: channels
    preserve component boundaries, and the final output rule consumes the
    compressed channel states.
    """

    return Rule(
        family=output.family,
        params=output.params,
        rule_id=output.rule_id,
        fn=output.fn,
        channels=tuple(channels),
        metadata=output.metadata,
    )


def formulaic(fn: UpdateFn | None = None, params: Mapping[str, Any] | None = None) -> Rule:
    """Build a direct callable rule family.

    Formulaic rules compute outputs from reads and parameters without a lookup
    table. The 0D AR2 modular recurrence is the Phase 1 use case.
    """

    return Rule(
        family="formulaic",
        params=dict(params or {}),
        fn=fn,
        metadata={"rule_type": "formulaic"},
    )


# ---------------------------------------------------------------------------
# Phase 1 Named Experiment Rule Families
# ---------------------------------------------------------------------------


def ar2_modular_0d(
    modulus: int = 97,
    coefficient_grid: tuple[int, int] = (16, 16),
    constant: int = 1,
) -> Rule:
    """Build the 0D second-order modular recurrence rule family.

    The intended `rule_id` decode is:

    ```text
    a = floor(rule_id / 16) + 1
    b = rule_id % 16
    next = (a*x[t] + b*x[t-1] + constant) % modulus
    ```
    """

    params = {
        "modulus": modulus,
        "coefficient_grid": coefficient_grid,
        "constant": constant,
    }
    metadata = dict(params)
    metadata["rule_type"] = "formulaic"
    metadata["R"] = coefficient_grid[0] * coefficient_grid[1]

    return Rule(
        family="ar2_modular_0d",
        params=params,
        metadata=metadata,
    )


def dyadrads_1d() -> Rule:
    """Build the 1D Dyadrads composed binary rule family.

    Component 0 is self/exhaustive, component 1 is radius-1 any-gated
    totalistic count, component 2 is radius-2 any-gated totalistic count, and
    the final output is a binary exhaustive lookup over the three channel
    outputs.
    """

    channels = (
        exhaustive(component=0, alphabet_size=2),
        gate(totalistic(component=1, aggregate="count"), type="any"),
        gate(totalistic(component=2, aggregate="count"), type="any"),
    )
    output = lookup(channels, alphabet_size=2)

    return Rule(
        family="dyadrads_1d",
        params={},
        channels=channels,
        metadata=output.metadata,
    )


def dyadlags_0d() -> Rule:
    """Build the 0D binary temporal 3-lag lookup rule family."""

    channels = (
        exhaustive(component=0, alphabet_size=2),
        exhaustive(component=1, alphabet_size=2),
        exhaustive(component=2, alphabet_size=2),
    )
    output = lookup(channels, alphabet_size=2)

    return Rule(
        family="dyadlags_0d",
        params={},
        channels=channels,
        metadata=output.metadata,
    )


def _count_channel(component: int, max_count: int) -> RuleChannel:
    params = {
        "rule_type": "totalistic",
        "component": int(component),
        "aggregate": "count",
        "state_count": int(max_count) + 1,
    }
    return RuleChannel(
        component=int(component),
        pipeline=(params,),
        name="totalistic",
        params=params,
    )


def lagcounts_0d(
    band_size: int = 3,
    band_count: int = 3,
    sampled_rule_count: int = 256,
) -> Rule:
    """Build the 0D count-banded temporal sampled-lookup rule family.

    The default context is current self plus three 3-lag active counts:
    `2 * 4 * 4 * 4 = 128` possible contexts. Rule IDs select deterministic
    sampled 128-entry binary tables instead of enumerating the full `2**128`
    rule space.
    """

    band_size = int(band_size)
    band_count = int(band_count)
    sampled_rule_count = int(sampled_rule_count)
    if band_size <= 0:
        raise ValueError(f"band_size must be positive, got {band_size}")
    if band_count <= 0:
        raise ValueError(f"band_count must be positive, got {band_count}")
    if sampled_rule_count <= 0:
        raise ValueError(f"sampled_rule_count must be positive, got {sampled_rule_count}")

    channels = [exhaustive(component=0, alphabet_size=2)]
    channels.extend(
        _count_channel(component=component, max_count=band_size)
        for component in range(1, band_count + 1)
    )
    context_count = 2 * ((band_size + 1) ** band_count)

    return Rule(
        family="lagcounts_0d",
        params={
            "band_size": band_size,
            "band_count": band_count,
            "sampled_rule_count": sampled_rule_count,
        },
        channels=tuple(channels),
        metadata={
            "alphabet_size": 2,
            "context_count": context_count,
            "decode": "sampled_splitmix64_context_bits",
            "R": sampled_rule_count,
        },
    )


def dyadaxes_2d() -> Rule:
    """Build the 2D Dyadaxes composed binary rule family.

    Component 0 is self/exhaustive, component 1 is cardinal-neighbor majority,
    component 2 is diagonal-neighbor majority, and the final output is a binary
    exhaustive lookup over the three channel outputs.
    """

    channels = (
        exhaustive(component=0, alphabet_size=2),
        gate(totalistic(component=1, aggregate="count"), type="majority"),
        gate(totalistic(component=2, aggregate="count"), type="majority"),
    )
    output = lookup(channels, alphabet_size=2)

    return Rule(
        family="dyadaxes_2d",
        params={},
        channels=channels,
        metadata=output.metadata,
    )


def dyadaxes_3d() -> Rule:
    """Build the 3D Dyadaxes composed binary rule family.

    Component 0 is self/exhaustive, component 1 is face-neighbor majority,
    component 2 is edge/corner at-least-10, and the final output is a binary
    exhaustive lookup over the three channel outputs.
    """

    channels = (
        exhaustive(component=0, alphabet_size=2),
        gate(totalistic(component=1, aggregate="count"), type="majority"),
        gate(totalistic(component=2, aggregate="count"), type="atLeast", value=10),
    )
    output = lookup(channels, alphabet_size=2)

    return Rule(
        family="dyadaxes_3d",
        params={},
        channels=channels,
        metadata=output.metadata,
    )
