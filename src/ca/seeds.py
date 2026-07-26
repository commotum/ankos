"""Closed sources of initial configurations.

``Seed`` describes initial configurations; it never renders arrays, owns an
ambient random generator, or chooses a rollout horizon.  Every non-exact
source is a sealed structural value.  Realization and replay evidence belong
to :mod:`ca.program`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Generic, TypeAlias, TypeVar

from . import alphabets, loci


C = TypeVar("C")
ExactSeedValue: TypeAlias = alphabets.SemanticValue


class SeedValidationError(ValueError):
    """A Seed descriptor is malformed or contains an unknown node."""


def _is_exact_seed_value(value: object) -> bool:
    """Recognize only sealed semantic-value variants."""

    return type(value) in (bool, int, Fraction, str) or type(value) in (
        alphabets.RepresentedNumber,
        alphabets.ValueNode,
    )


class ExactnessProfile(Enum):
    """Exactness promised by a source descriptor."""

    EXACT = "exact"
    REPRESENTED = "represented"
    SYMBOLIC = "symbolic"


class EntropyInterface(Enum):
    """How a source may be realized."""

    NONE = "none"
    REPLAY_KEY = "replay-key"


@dataclass(frozen=True)
class SeedOutputContract:
    """Immutable compatibility declaration for every denoted configuration."""

    configuration_contract: loci.CarrierContract
    value_profile: alphabets.ValueProfile
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT
    entropy_interface: EntropyInterface = EntropyInterface.NONE

    def __post_init__(self) -> None:
        if type(self.configuration_contract) is not loci.CarrierContract:
            raise TypeError("configuration_contract must be loci.CarrierContract")
        if type(self.value_profile) is not alphabets.ValueProfile:
            raise TypeError("value_profile must be alphabets.ValueProfile")
        if type(self.exactness_profile) is not ExactnessProfile:
            raise TypeError("exactness_profile is not recognized")
        if type(self.entropy_interface) is not EntropyInterface:
            raise TypeError("entropy_interface is not recognized")


class ConstructionOp(Enum):
    """Closed constructive-source operations interpreted by ``program.py``."""

    EMPTY = "empty"
    FILL = "fill"
    POINT = "point"
    SEQUENCE = "sequence"
    RECORD = "record"
    GRID = "grid"


ConstructionArgument = (
    ExactSeedValue
    | loci.Locus
    | loci.Region
    | tuple[ExactSeedValue, ...]
    | tuple[tuple[str, ExactSeedValue], ...]
)


@dataclass(frozen=True)
class Construction:
    """One recognized constructive configuration expression."""

    operation: ConstructionOp
    arguments: tuple[ConstructionArgument, ...] = ()

    def __post_init__(self) -> None:
        if type(self.operation) is not ConstructionOp:
            raise TypeError("construction operation is not recognized")
        if type(self.arguments) is not tuple:
            raise TypeError("construction arguments must be an immutable tuple")
        if any(not _closed_construction_argument(item) for item in self.arguments):
            raise SeedValidationError(
                "construction contains an unclosed argument"
            )
        if self.operation is ConstructionOp.EMPTY and self.arguments:
            raise SeedValidationError("EMPTY construction takes no arguments")
        if self.operation is ConstructionOp.FILL:
            if len(self.arguments) != 1 or not _is_exact_seed_value(
                self.arguments[0]
            ):
                raise SeedValidationError(
                    "FILL construction takes one closed semantic value"
                )
        if self.operation is ConstructionOp.POINT:
            if (
                len(self.arguments) != 2
                or type(self.arguments[0]) is not loci.Locus
                or not _is_exact_seed_value(self.arguments[1])
            ):
                raise SeedValidationError(
                    "POINT construction takes one Locus and one semantic value"
                )
        if self.operation is ConstructionOp.SEQUENCE:
            if len(self.arguments) not in (0, 1):
                raise SeedValidationError(
                    "SEQUENCE construction takes one tuple or a law-supplied tuple"
                )
            if self.arguments and (
                type(self.arguments[0]) is not tuple
                or not self.arguments[0]
            ):
                raise SeedValidationError("SEQUENCE values cannot be empty")
            if self.arguments and any(
                not _is_exact_seed_value(value) for value in self.arguments[0]
            ):
                raise SeedValidationError(
                    "SEQUENCE construction contains a non-semantic value"
                )
        if self.operation is ConstructionOp.RECORD:
            if len(self.arguments) not in (0, 1):
                raise SeedValidationError(
                    "RECORD construction takes one field tuple or law values"
                )
            if self.arguments:
                fields = self.arguments[0]
                if (
                    type(fields) is not tuple
                    or not fields
                    or any(
                        type(field) is not tuple
                        or len(field) != 2
                        or type(field[0]) is not str
                        or not field[0]
                        or not _is_exact_seed_value(field[1])
                        for field in fields
                    )
                ):
                    raise SeedValidationError(
                        "RECORD construction needs closed named fields"
                    )
        if self.operation is ConstructionOp.GRID:
            if len(self.arguments) not in (0, 3):
                raise SeedValidationError(
                    "GRID construction takes shape, values, and boundary fields"
                )
            if self.arguments:
                shape, values, boundary_fields = self.arguments
                if (
                    type(shape) is not tuple
                    or not shape
                    or any(type(size) is not int or size <= 0 for size in shape)
                    or type(values) is not tuple
                    or any(not _is_exact_seed_value(value) for value in values)
                    or type(boundary_fields) is not tuple
                    or any(
                        type(field) is not tuple
                        or len(field) != 2
                        or type(field[0]) is not str
                        or not field[0]
                        or not _is_exact_seed_value(field[1])
                        for field in boundary_fields
                    )
                ):
                    raise SeedValidationError(
                        "GRID construction contains malformed closed fields"
                    )
                cell_count = 1
                for size in shape:
                    cell_count *= size
                if len(values) != cell_count:
                    raise SeedValidationError(
                        "GRID construction values do not fill its declared shape"
                    )
                field_names = tuple(name for name, _ in boundary_fields)
                if len(field_names) != len(set(field_names)):
                    raise SeedValidationError(
                        "GRID boundary fields must have unique names"
                    )
                fields = dict(boundary_fields)
                if set(fields) not in ({"policy"}, {"policy", "exterior"}):
                    raise SeedValidationError(
                        "GRID boundary fields must contain policy and optional exterior"
                    )
                policy_value = fields["policy"]
                if type(policy_value) is not str:
                    raise SeedValidationError(
                        "GRID boundary policy must be its closed string value"
                    )
                try:
                    policy = loci.BoundaryPolicy(policy_value)
                except ValueError as error:
                    raise SeedValidationError(
                        "GRID boundary policy is not recognized"
                    ) from error
                has_exterior = "exterior" in fields
                if (
                    policy is loci.BoundaryPolicy.FIXED
                    and not has_exterior
                ):
                    raise SeedValidationError(
                        "a fixed GRID boundary requires an exterior value"
                    )
                if (
                    policy is not loci.BoundaryPolicy.FIXED
                    and has_exterior
                ):
                    raise SeedValidationError(
                        "only a fixed GRID boundary carries an exterior value"
                    )


@dataclass(frozen=True)
class ExactSource(Generic[C]):
    """One fully specified initial configuration."""

    configuration: C

    def __post_init__(self) -> None:
        if type(self.configuration) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("exact source configuration is not recognized")


@dataclass(frozen=True)
class ConstructiveSource:
    """A closed constructor, never a host-language callable."""

    construction: Construction

    def __post_init__(self) -> None:
        if type(self.construction) is not Construction:
            raise TypeError("constructive source construction is not recognized")


@dataclass(frozen=True)
class PartialSource(Generic[C]):
    """A configuration with explicit unresolved roles and obligations."""

    configuration: C
    unresolved: tuple[loci.Locus, ...]
    obligations: tuple[loci.SelectorExpr, ...]

    def __post_init__(self) -> None:
        if type(self.configuration) not in (
            loci.FiniteConfiguration,
            loci.IntensionalConfiguration,
        ):
            raise TypeError("partial source configuration is not recognized")
        if type(self.unresolved) is not tuple or any(
            type(item) is not loci.Locus for item in self.unresolved
        ):
            raise TypeError("partial unresolved roles must be an immutable Locus tuple")
        if type(self.obligations) is not tuple or any(
            type(item) is not loci.SelectorExpr for item in self.obligations
        ):
            raise TypeError(
                "partial obligations must be an immutable SelectorExpr tuple"
            )
        if not self.unresolved:
            raise SeedValidationError("a partial source needs an unresolved role")
        if len(set(self.unresolved)) != len(self.unresolved):
            raise SeedValidationError("partial-source roles must be unique")


@dataclass(frozen=True)
class BernoulliLaw:
    """An exact independent Bernoulli law over a closed support."""

    support: loci.Region
    probability_true: Fraction
    false_value: ExactSeedValue = False
    true_value: ExactSeedValue = True
    boundary: loci.Boundary[ExactSeedValue] = loci.Boundary(
        loci.BoundaryPolicy.NONE
    )

    def __post_init__(self) -> None:
        if type(self.support) is not loci.Region:
            raise TypeError("Bernoulli support is not recognized")
        probability = self.probability_true
        if type(probability) is not Fraction:
            raise TypeError("probability_true must be fractions.Fraction")
        if probability < 0 or probability > 1:
            raise SeedValidationError("probability_true must lie in [0, 1]")
        if not _is_exact_seed_value(self.false_value) or not _is_exact_seed_value(
            self.true_value
        ):
            raise TypeError("Bernoulli outcomes must be closed semantic values")
        if type(self.boundary) is not loci.Boundary:
            raise TypeError("Bernoulli boundary is not recognized")
        if alphabets.semantic_equal(self.false_value, self.true_value):
            raise SeedValidationError("Bernoulli outcomes must be distinct")


@dataclass(frozen=True)
class UniformTupleLaw:
    """Uniform tuples over ``range(value_count)`` with explicit exclusions."""

    length: int
    value_count: int
    excluded: tuple[tuple[int, ...], ...] = ()

    def __post_init__(self) -> None:
        if type(self.length) is not int or self.length <= 0:
            raise SeedValidationError("uniform tuple length must be positive")
        if type(self.value_count) is not int or self.value_count <= 0:
            raise SeedValidationError("uniform tuple value_count must be positive")
        if type(self.excluded) is not tuple or any(
            type(item) is not tuple
            or any(type(value) is not int for value in item)
            for item in self.excluded
        ):
            raise TypeError("excluded values must be immutable integer tuples")
        for item in self.excluded:
            if len(item) != self.length:
                raise SeedValidationError("excluded tuple has the wrong length")
            if any(value < 0 or value >= self.value_count for value in item):
                raise SeedValidationError("excluded tuple value is outside the law")
        if len(set(self.excluded)) != len(self.excluded):
            raise SeedValidationError("excluded tuples must be unique")
        support_size = 1
        for _ in range(self.length):
            support_size *= self.value_count
            if support_size > len(self.excluded):
                break
        if support_size == len(self.excluded):
            raise SeedValidationError("uniform tuple law has empty support")
        ordered = tuple(sorted(self.excluded))
        if ordered != self.excluded:
            object.__setattr__(self, "excluded", ordered)


@dataclass(frozen=True)
class IntensionalProbabilityLaw:
    """A closed, non-enumerated probability-law presentation."""

    binder: str
    relation: loci.SelectorExpr

    def __post_init__(self) -> None:
        if type(self.binder) is not str or not self.binder:
            raise SeedValidationError("an intensional law binder cannot be empty")
        if type(self.relation) is not loci.SelectorExpr:
            raise TypeError("intensional law relation is not recognized")


ProbabilityLaw = BernoulliLaw | UniformTupleLaw | IntensionalProbabilityLaw


@dataclass(frozen=True)
class LawSource:
    """A replayable probability measure over initial configurations."""

    law: ProbabilityLaw
    construction: Construction | None = None

    def __post_init__(self) -> None:
        if type(self.law) not in (
            BernoulliLaw,
            UniformTupleLaw,
            IntensionalProbabilityLaw,
        ):
            raise TypeError("probability-law variant is not recognized")
        if self.construction is not None and type(
            self.construction
        ) is not Construction:
            raise TypeError("law construction is not recognized")


@dataclass(frozen=True)
class IntensionalSource:
    """A finite closed presentation of a non-enumerated initial object."""

    binder: str
    relation: loci.SelectorExpr

    def __post_init__(self) -> None:
        if type(self.binder) is not str or not self.binder:
            raise SeedValidationError("an intensional source binder cannot be empty")
        if type(self.relation) is not loci.SelectorExpr:
            raise TypeError("intensional source relation is not recognized")


@dataclass(frozen=True)
class ProductPart(Generic[C]):
    key: str
    seed: "Seed[C]"

    def __post_init__(self) -> None:
        if type(self.key) is not str or not self.key:
            raise SeedValidationError("product part keys cannot be empty")
        if type(self.seed) is not Seed:
            raise TypeError("product part seed is not recognized")


@dataclass(frozen=True)
class ProductSource(Generic[C]):
    parts: tuple[ProductPart[C], ...]

    def __post_init__(self) -> None:
        if type(self.parts) is not tuple or any(
            type(part) is not ProductPart for part in self.parts
        ):
            raise TypeError("product parts must be an immutable ProductPart tuple")
        _validate_keys(self.parts)


class OverlayConflict(Enum):
    """Explicit overlap semantics for source overlays."""

    REJECT = "reject"
    LEFT = "left"
    RIGHT = "right"
    REQUIRE_EQUAL = "require-equal"


@dataclass(frozen=True)
class OverlaySource(Generic[C]):
    parts: tuple["Seed[C]", ...]
    conflict: OverlayConflict

    def __post_init__(self) -> None:
        if type(self.parts) is not tuple or any(
            type(part) is not Seed for part in self.parts
        ):
            raise TypeError("overlay parts must be an immutable Seed tuple")
        if type(self.conflict) is not OverlayConflict:
            raise TypeError("overlay conflict mode is not recognized")
        if not self.parts:
            raise SeedValidationError("an overlay needs at least one part")


@dataclass(frozen=True)
class MixturePart(Generic[C]):
    weight: Fraction
    seed: "Seed[C]"

    def __post_init__(self) -> None:
        if type(self.weight) is not Fraction:
            raise TypeError("mixture weights must be fractions.Fraction")
        if self.weight <= 0:
            raise SeedValidationError("mixture weights must be positive")
        if type(self.seed) is not Seed:
            raise TypeError("mixture part seed is not recognized")


@dataclass(frozen=True)
class MixtureSource(Generic[C]):
    parts: tuple[MixturePart[C], ...]

    def __post_init__(self) -> None:
        if type(self.parts) is not tuple or any(
            type(part) is not MixturePart for part in self.parts
        ):
            raise TypeError("mixture parts must be an immutable MixturePart tuple")
        if not self.parts:
            raise SeedValidationError("a mixture needs at least one part")
        if sum((part.weight for part in self.parts), Fraction(0)) != 1:
            raise SeedValidationError("mixture weights must sum exactly to one")


@dataclass(frozen=True)
class ProductLawSource(Generic[C]):
    """Named source laws whose independence is stated explicitly."""

    parts: tuple[ProductPart[C], ...]

    def __post_init__(self) -> None:
        if type(self.parts) is not tuple or any(
            type(part) is not ProductPart for part in self.parts
        ):
            raise TypeError(
                "product-law parts must be an immutable ProductPart tuple"
            )
        _validate_keys(self.parts)
        if any(not _has_probability_law(part.seed.source) for part in self.parts):
            raise SeedValidationError("every product-law part must contain a law")


@dataclass(frozen=True)
class RefinedSource(Generic[C]):
    source: "Seed[C]"
    constraint: loci.SelectorExpr

    def __post_init__(self) -> None:
        if type(self.source) is not Seed:
            raise TypeError("refined source seed is not recognized")
        if type(self.constraint) is not loci.SelectorExpr:
            raise TypeError("refined source constraint is not recognized")


SeedSource = (
    ExactSource[C]
    | ConstructiveSource
    | PartialSource[C]
    | LawSource
    | IntensionalSource
    | ProductSource[C]
    | OverlaySource[C]
    | MixtureSource[C]
    | ProductLawSource[C]
    | RefinedSource[C]
)


@dataclass(frozen=True)
class SeedDenotation(Generic[C]):
    """Validated closed source plus its immutable compatibility declaration."""

    source: SeedSource[C]
    output_contract: SeedOutputContract

    def __post_init__(self) -> None:
        _validate_source(self.source)
        if type(self.output_contract) is not SeedOutputContract:
            raise TypeError("seed denotation output contract is not recognized")
        _validate_source_output(self.source, self.output_contract)

    @property
    def exact_configuration(self) -> C:
        if not isinstance(self.source, ExactSource):
            raise SeedValidationError("this denotation is not an exact source")
        return self.source.configuration


@dataclass(frozen=True)
class Seed(Generic[C]):
    """One exact, constructive, partial, law-valued, or intensional source."""

    source: SeedSource[C]
    output_contract: SeedOutputContract
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise SeedValidationError(
                f"unsupported Seed version {self.version!r}"
            )
        _validate_source(self.source)
        if type(self.output_contract) is not SeedOutputContract:
            raise TypeError("Seed output contract is not recognized")
        _validate_source_output(self.source, self.output_contract)
        if isinstance(self.source, (ExactSource, PartialSource)):
            configuration = self.source.configuration
            if type(configuration) not in (
                loci.FiniteConfiguration,
                loci.IntensionalConfiguration,
            ):
                raise SeedValidationError(
                    "exact/partial sources require a recognized configuration"
                )
            if not self.output_contract.configuration_contract.accepts(
                configuration.contract
            ):
                raise SeedValidationError(
                    "source configuration violates its output contract"
                )
        has_entropy = _has_probability_law(self.source)
        expected = (
            EntropyInterface.REPLAY_KEY if has_entropy else EntropyInterface.NONE
        )
        if self.output_contract.entropy_interface is not expected:
            raise SeedValidationError(
                "entropy_interface does not match the source denotation"
            )

    @property
    def configuration_contract(self) -> loci.CarrierContract:
        return self.output_contract.configuration_contract

    @property
    def value_profile(self) -> alphabets.ValueProfile:
        return self.output_contract.value_profile

    @property
    def exactness_profile(self) -> ExactnessProfile:
        return self.output_contract.exactness_profile

    @property
    def entropy_interface(self) -> EntropyInterface:
        return self.output_contract.entropy_interface

    def denote(self) -> SeedDenotation[C]:
        """Validate and return the complete closed source denotation."""

        _validate_source(self.source)
        return SeedDenotation(self.source, self.output_contract)


_SOURCE_TYPES = (
    ExactSource,
    ConstructiveSource,
    PartialSource,
    LawSource,
    IntensionalSource,
    ProductSource,
    OverlaySource,
    MixtureSource,
    ProductLawSource,
    RefinedSource,
)
_LAW_TYPES = (BernoulliLaw, UniformTupleLaw, IntensionalProbabilityLaw)


def _closed_construction_argument(value: object) -> bool:
    if _is_exact_seed_value(value) or type(value) in (loci.Locus, loci.Region):
        return True
    if type(value) is tuple:
        return all(_closed_construction_argument(item) for item in value)
    return False


def _validate_keys(parts: tuple[ProductPart[C], ...]) -> None:
    if not parts:
        raise SeedValidationError("a product needs at least one part")
    keys = tuple(part.key for part in parts)
    if len(set(keys)) != len(keys):
        raise SeedValidationError("product part keys must be unique")


def _validate_source(source: SeedSource[C]) -> None:
    if type(source) not in _SOURCE_TYPES:
        raise SeedValidationError(
            f"unknown Seed source node {type(source).__name__!r}"
        )
    if isinstance(source, LawSource) and type(source.law) not in _LAW_TYPES:
        raise SeedValidationError(
            f"unknown probability-law node {type(source.law).__name__!r}"
        )
    if isinstance(source, (ProductSource, OverlaySource, MixtureSource, ProductLawSource)):
        nested = (
            tuple(part.seed for part in source.parts)
            if isinstance(source, (ProductSource, MixtureSource, ProductLawSource))
            else source.parts
        )
        for seed in nested:
            _validate_source(seed.source)
    if isinstance(source, RefinedSource):
        _validate_source(source.source.source)


def _carrier_size(contract: loci.CarrierContract) -> int | None:
    if contract.shape is None:
        return None
    size = 1
    for extent in contract.shape:
        size *= extent
    return size


def _construction_kind_for_contract(
    contract: loci.CarrierContract,
) -> ConstructionOp | None:
    if contract.kind is loci.CarrierKind.HISTORY:
        return ConstructionOp.SEQUENCE
    if contract.kind is loci.CarrierKind.RECORD:
        return ConstructionOp.RECORD
    if contract.kind is loci.CarrierKind.GRID:
        return ConstructionOp.GRID
    return None


def _validate_construction_output(
    construction: Construction,
    contract: loci.CarrierContract,
    *,
    law_supplied: bool,
) -> None:
    """Prove a closed construction can produce the declared carrier."""

    operation = construction.operation
    arguments = construction.arguments
    if law_supplied:
        if arguments:
            raise SeedValidationError(
                "a law-supplied construction cannot also contain output values"
            )
        expected = _construction_kind_for_contract(contract)
        if expected is None or operation is not expected:
            raise SeedValidationError(
                "law construction does not match its output carrier"
            )
        return

    if operation in (
        ConstructionOp.SEQUENCE,
        ConstructionOp.RECORD,
        ConstructionOp.GRID,
    ) and not arguments:
        raise SeedValidationError(
            "a constructive source cannot omit construction values"
        )

    if operation is ConstructionOp.SEQUENCE:
        if contract.kind is not loci.CarrierKind.HISTORY:
            raise SeedValidationError(
                "SEQUENCE construction requires a history carrier"
            )
        values = arguments[0]
        concrete = loci.CarrierContract(
            loci.CarrierKind.HISTORY,
            rank=1,
            shape=(len(values),),
            axes=("history",),
        )
        if not contract.accepts(concrete):
            raise SeedValidationError(
                "SEQUENCE values disagree with the declared history carrier"
            )
        return

    if operation is ConstructionOp.RECORD:
        if contract.kind is not loci.CarrierKind.RECORD:
            raise SeedValidationError(
                "RECORD construction requires a record carrier"
            )
        concrete = loci.CarrierContract(
            loci.CarrierKind.RECORD,
            rank=0,
            shape=(),
            axes=(),
        )
        if not contract.accepts(concrete):
            raise SeedValidationError(
                "RECORD fields disagree with the declared record carrier"
            )
        return

    if operation is ConstructionOp.GRID:
        if contract.kind is not loci.CarrierKind.GRID:
            raise SeedValidationError("GRID construction requires a grid carrier")
        shape = arguments[0]
        if contract.rank is not None and contract.rank != len(shape):
            raise SeedValidationError(
                "GRID rank disagrees with the declared grid carrier"
            )
        if contract.shape is not None and contract.shape != shape:
            raise SeedValidationError(
                "GRID shape disagrees with the declared grid carrier"
            )
        if contract.axes and len(contract.axes) != len(shape):
            raise SeedValidationError(
                "GRID axes disagree with the declared grid carrier"
            )
        return

    if operation is ConstructionOp.FILL:
        if (
            contract.kind
            not in (
                loci.CarrierKind.HISTORY,
                loci.CarrierKind.GRID,
            )
            or contract.shape is None
            or (
                contract.kind is loci.CarrierKind.HISTORY
                and len(contract.shape) != 1
            )
            or (
                contract.kind is loci.CarrierKind.GRID
                and not contract.shape
            )
        ):
            raise SeedValidationError(
                "FILL requires a concrete history or grid carrier"
            )
        return

    if operation is ConstructionOp.POINT:
        if contract.kind is loci.CarrierKind.INTENSIONAL:
            raise SeedValidationError(
                "POINT cannot realize an intensional carrier"
            )
        target = arguments[0]
        if contract.kind is loci.CarrierKind.HISTORY and contract.shape is not None:
            expected = (
                loci.occurrence("history", 0),
            )
            if contract.shape != (1,) or target not in expected:
                raise SeedValidationError(
                    "POINT does not equal the declared history carrier"
                )
        if contract.kind is loci.CarrierKind.GRID and contract.shape is not None:
            expected = loci.grid_loci(
                contract.shape,
                axes=contract.axes or None,
            )
            if len(expected) != 1 or target not in expected:
                raise SeedValidationError(
                    "POINT does not equal the declared grid carrier"
                )
        return

    if operation is ConstructionOp.EMPTY:
        if contract.kind is loci.CarrierKind.INTENSIONAL:
            raise SeedValidationError(
                "EMPTY cannot realize an intensional carrier"
            )
        if (
            contract.kind in (
                loci.CarrierKind.HISTORY,
                loci.CarrierKind.GRID,
            )
            and contract.shape is not None
        ):
            raise SeedValidationError(
                "EMPTY cannot satisfy a nonempty concrete carrier"
            )
        return

    raise SeedValidationError("construction operation is not realizable")


def _validate_uniform_tuple_output(
    law: UniformTupleLaw,
    construction: Construction | None,
    contract: loci.CarrierContract,
) -> None:
    expected = _construction_kind_for_contract(contract)
    if expected is None:
        raise SeedValidationError(
            "uniform tuple laws require record, history, or grid carriers"
        )
    if construction is not None:
        _validate_construction_output(
            construction,
            contract,
            law_supplied=True,
        )
    if contract.kind is loci.CarrierKind.HISTORY:
        concrete = loci.CarrierContract(
            loci.CarrierKind.HISTORY,
            rank=1,
            shape=(law.length,),
            axes=("history",),
        )
        if not contract.accepts(concrete):
            raise SeedValidationError(
                "uniform tuple length disagrees with its history carrier"
            )
    elif contract.kind is loci.CarrierKind.RECORD:
        concrete = loci.CarrierContract(
            loci.CarrierKind.RECORD,
            rank=0,
            shape=(),
            axes=(),
        )
        if not contract.accepts(concrete):
            raise SeedValidationError(
                "uniform tuple fields disagree with its record carrier"
            )
    elif contract.kind is loci.CarrierKind.GRID:
        size = _carrier_size(contract)
        if size is None:
            raise SeedValidationError(
                "uniform tuple grid laws require a concrete shape"
            )
        if not contract.shape or size != law.length:
            raise SeedValidationError(
                "uniform tuple length disagrees with its grid carrier"
            )


def _validate_source_output(
    source: SeedSource[C],
    output_contract: SeedOutputContract,
) -> None:
    contract = output_contract.configuration_contract
    if isinstance(source, ConstructiveSource):
        _validate_construction_output(
            source.construction,
            contract,
            law_supplied=False,
        )
    elif isinstance(source, LawSource):
        if isinstance(source.law, UniformTupleLaw):
            _validate_uniform_tuple_output(
                source.law,
                source.construction,
                contract,
            )
        elif source.construction is not None:
            raise SeedValidationError(
                "only a uniform tuple law accepts a law-supplied construction"
            )


def _has_probability_law(source: SeedSource[C]) -> bool:
    if isinstance(source, (LawSource, MixtureSource, ProductLawSource)):
        return True
    if isinstance(source, ProductSource):
        return any(_has_probability_law(part.seed.source) for part in source.parts)
    if isinstance(source, OverlaySource):
        return any(_has_probability_law(seed.source) for seed in source.parts)
    if isinstance(source, RefinedSource):
        return _has_probability_law(source.source.source)
    return False


def _contract(
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    *,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
    entropy: bool = False,
) -> SeedOutputContract:
    return SeedOutputContract(
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        exactness_profile=exactness_profile,
        entropy_interface=(
            EntropyInterface.REPLAY_KEY if entropy else EntropyInterface.NONE
        ),
    )


def exact(
    configuration: C,
    *,
    configuration_contract: loci.CarrierContract | None = None,
    value_profile: alphabets.ValueProfile | None = None,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
) -> Seed[C]:
    """Describe one fully specified configuration."""

    if not isinstance(
        configuration, (loci.FiniteConfiguration, loci.IntensionalConfiguration)
    ):
        raise TypeError("exact Seeds require a recognized loci configuration")
    if configuration_contract is None:
        configuration_contract = configuration.contract
    elif not configuration_contract.accepts(configuration.contract):
        raise SeedValidationError(
            "declared configuration contract does not accept the configuration"
        )
    if value_profile is None:
        value_profile = _infer_value_profile(configuration)
    return Seed(
        ExactSource(configuration),
        _contract(
            configuration_contract,
            value_profile,
            exactness_profile=exactness_profile,
        ),
    )


def constructive(
    construction: Construction,
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
) -> Seed[C]:
    """Describe one closed constructive source."""

    return Seed(
        ConstructiveSource(construction),
        _contract(
            configuration_contract,
            value_profile,
            exactness_profile=exactness_profile,
        ),
    )


def partial(
    configuration: C,
    *,
    unresolved: tuple[loci.Locus, ...],
    obligations: tuple[loci.SelectorExpr, ...],
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
) -> Seed[C]:
    """Describe an explicitly incomplete configuration."""

    return Seed(
        PartialSource(configuration, unresolved, obligations),
        _contract(
            configuration_contract,
            value_profile,
            exactness_profile=exactness_profile,
        ),
    )


def law(
    probability_law: ProbabilityLaw,
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    construction: Construction | None = None,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
) -> Seed[C]:
    """Describe a replayable probability law over configurations."""

    return Seed(
        LawSource(probability_law, construction),
        _contract(
            configuration_contract,
            value_profile,
            exactness_profile=exactness_profile,
            entropy=True,
        ),
    )


def intensional(
    binder: str,
    relation: loci.SelectorExpr,
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    exactness_profile: ExactnessProfile = ExactnessProfile.SYMBOLIC,
) -> Seed[C]:
    """Describe a finite closed presentation of an unenumerated source."""

    return Seed(
        IntensionalSource(binder, relation),
        _contract(
            configuration_contract,
            value_profile,
            exactness_profile=exactness_profile,
        ),
    )


def product(parts: tuple[tuple[str, Seed[C]], ...]) -> Seed[C]:
    """Compose named structural source parts."""

    normalized = tuple(ProductPart(key, seed) for key, seed in parts)
    contract = _product_contract(tuple(part.seed for part in normalized))
    return Seed(ProductSource(normalized), contract)


def overlay(
    parts: tuple[Seed[C], ...],
    *,
    conflict: OverlayConflict = OverlayConflict.REJECT,
) -> Seed[C]:
    """Overlay source assignments under an explicit conflict law."""

    contract = _common_contract(parts)
    return Seed(OverlaySource(parts, conflict), contract)


def mixture(parts: tuple[tuple[Fraction, Seed[C]], ...]) -> Seed[C]:
    """Form an exact probability-law mixture."""

    normalized = tuple(MixturePart(weight, seed) for weight, seed in parts)
    common = _common_contract(tuple(part.seed for part in normalized))
    contract = SeedOutputContract(
        common.configuration_contract,
        common.value_profile,
        common.exactness_profile,
        EntropyInterface.REPLAY_KEY,
    )
    return Seed(MixtureSource(normalized), contract)


def product_law(parts: tuple[tuple[str, Seed[C]], ...]) -> Seed[C]:
    """Compose named probability laws while declaring independence."""

    normalized = tuple(ProductPart(key, seed) for key, seed in parts)
    common = _product_contract(tuple(part.seed for part in normalized))
    contract = SeedOutputContract(
        common.configuration_contract,
        common.value_profile,
        common.exactness_profile,
        EntropyInterface.REPLAY_KEY,
    )
    return Seed(ProductLawSource(normalized), contract)


def refine(source: Seed[C], constraint: loci.SelectorExpr) -> Seed[C]:
    """Add a closed constraint without changing the source contract."""

    return Seed(RefinedSource(source, constraint), source.output_contract)


def bernoulli(
    support: loci.Region,
    probability_true: Fraction = Fraction(1, 2),
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile = alphabets.ValueProfile.BOOLEAN,
    false_value: ExactSeedValue = False,
    true_value: ExactSeedValue = True,
    boundary: loci.Boundary[ExactSeedValue] = loci.Boundary(
        loci.BoundaryPolicy.NONE
    ),
) -> Seed[C]:
    """Build an exact Bernoulli law; floats and ambient RNGs are rejected."""

    if value_profile is alphabets.ValueProfile.BOOLEAN and not (
        isinstance(false_value, bool) and isinstance(true_value, bool)
    ):
        raise SeedValidationError(
            "boolean Bernoulli laws require boolean outcomes"
        )
    return law(
        BernoulliLaw(
            support,
            probability_true,
            false_value,
            true_value,
            boundary,
        ),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
    )


def sequence(
    values: tuple[ExactSeedValue, ...],
    *,
    value_profile: alphabets.ValueProfile | None = None,
) -> Seed[loci.FiniteConfiguration[ExactSeedValue]]:
    """Construct one exact ordered history/word configuration."""

    if not values:
        raise SeedValidationError("sequence values cannot be empty")
    return exact(
        loci.history_configuration(values),
        value_profile=value_profile,
    )


def pair(
    previous: ExactSeedValue,
    current: ExactSeedValue,
    *,
    value_profile: alphabets.ValueProfile | None = None,
) -> Seed[loci.FiniteConfiguration[ExactSeedValue]]:
    """Construct the ordered ``previous``/``current`` recurrence record."""

    return record(
        (("previous", previous), ("current", current)),
        value_profile=value_profile,
    )


def uniform_pair(
    *,
    value_count: int,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    reject_zero_zero: bool = True,
) -> Seed[C]:
    """Build a replayable uniform law over two finite values."""

    excluded = ((0, 0),) if reject_zero_zero else ()
    operation = (
        ConstructionOp.RECORD
        if configuration_contract.kind is loci.CarrierKind.RECORD
        else ConstructionOp.SEQUENCE
    )
    return law(
        UniformTupleLaw(2, value_count, excluded),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        construction=Construction(operation),
    )


def uniform_bits(
    *,
    length: int,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile = alphabets.ValueProfile.BOOLEAN,
    reject_all_zero: bool = False,
) -> Seed[C]:
    """Build a replayable uniform law over a fixed binary history."""

    excluded = ((0,) * length,) if reject_all_zero else ()
    return law(
        UniformTupleLaw(length, 2, excluded),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        construction=Construction(ConstructionOp.SEQUENCE),
    )


def finite_grid(
    shape: tuple[int, ...],
    values: tuple[ExactSeedValue, ...],
    *,
    boundary: loci.Boundary[ExactSeedValue],
    axes: tuple[str, ...] | None = None,
    value_profile: alphabets.ValueProfile | None = None,
) -> Seed[loci.FiniteConfiguration[ExactSeedValue]]:
    """Construct a positive-rank finite grid without rendering machinery."""

    if type(shape) is not tuple:
        raise TypeError("finite-grid shape must be an immutable tuple")
    if not shape:
        raise SeedValidationError("finite-grid rank must be positive")
    if any(type(size) is not int or size <= 0 for size in shape):
        raise SeedValidationError("finite-grid extents must be positive")
    if type(values) is not tuple:
        raise TypeError("finite-grid values must be an immutable tuple")
    if axes is not None:
        if type(axes) is not tuple:
            raise TypeError("finite-grid axes must be an immutable tuple")
        if len(axes) != len(shape):
            raise SeedValidationError(
                "finite-grid axes and shape must have equal rank"
            )
        if any(type(axis) is not str or not axis for axis in axes):
            raise TypeError("finite-grid axes must be nonempty strings")
        if len(set(axes)) != len(axes):
            raise SeedValidationError("finite-grid axes must be unique")
    cell_count = 1
    for size in shape:
        cell_count *= size
    if len(values) != cell_count:
        raise SeedValidationError(
            f"finite-grid needs {cell_count} values, got {len(values)}"
        )
    return exact(
        loci.grid_configuration(
            shape,
            values,
            boundary=boundary,
            axes=axes,
        ),
        value_profile=value_profile,
    )


def record(
    fields: tuple[tuple[str, ExactSeedValue], ...],
    *,
    value_profile: alphabets.ValueProfile | None = None,
) -> Seed[loci.FiniteConfiguration[ExactSeedValue]]:
    """Construct one exact named-record configuration."""

    return exact(
        loci.record_configuration(fields),
        value_profile=value_profile,
    )


def _infer_value_profile(
    configuration: loci.FiniteConfiguration[ExactSeedValue]
    | loci.IntensionalConfiguration,
) -> alphabets.ValueProfile:
    if isinstance(configuration, loci.IntensionalConfiguration):
        return alphabets.ValueProfile.SYMBOLIC
    values = tuple(value for _, value in configuration.entries)
    if values and all(
        isinstance(value, alphabets.RepresentedNumber) for value in values
    ):
        return alphabets.ValueProfile.REPRESENTED
    if values and all(isinstance(value, alphabets.ValueNode) for value in values):
        return alphabets.ValueProfile.STRUCTURAL
    if values and all(isinstance(value, bool) for value in values):
        return alphabets.ValueProfile.BOOLEAN
    if values and all(
        isinstance(value, int) and not isinstance(value, bool) for value in values
    ):
        return alphabets.ValueProfile.INTEGER
    if values and all(
        isinstance(value, (int, Fraction)) and not isinstance(value, bool)
        for value in values
    ):
        return alphabets.ValueProfile.RATIONAL
    if values and all(
        isinstance(value, (int, str)) and not isinstance(value, bool)
        for value in values
    ):
        return alphabets.ValueProfile.SYMBOLIC
    return alphabets.ValueProfile.STRUCTURAL


def _common_contract(seeds: tuple[Seed[C], ...]) -> SeedOutputContract:
    if not seeds:
        raise SeedValidationError("composition needs at least one Seed")
    first = seeds[0].output_contract
    for seed in seeds[1:]:
        current = seed.output_contract
        if (
            current.configuration_contract != first.configuration_contract
            or current.value_profile != first.value_profile
            or current.exactness_profile is not first.exactness_profile
        ):
            raise SeedValidationError("composed Seeds have incompatible contracts")
    entropy = any(
        seed.output_contract.entropy_interface is EntropyInterface.REPLAY_KEY
        for seed in seeds
    )
    return SeedOutputContract(
        first.configuration_contract,
        first.value_profile,
        first.exactness_profile,
        EntropyInterface.REPLAY_KEY if entropy else EntropyInterface.NONE,
    )


def _product_contract(seeds: tuple[Seed[C], ...]) -> SeedOutputContract:
    if not seeds:
        raise SeedValidationError("product needs at least one Seed")
    exactnesses = tuple(seed.exactness_profile for seed in seeds)
    if ExactnessProfile.SYMBOLIC in exactnesses:
        exactness = ExactnessProfile.SYMBOLIC
    elif ExactnessProfile.REPRESENTED in exactnesses:
        exactness = ExactnessProfile.REPRESENTED
    else:
        exactness = ExactnessProfile.EXACT
    entropy = any(
        seed.entropy_interface is EntropyInterface.REPLAY_KEY for seed in seeds
    )
    return SeedOutputContract(
        loci.CarrierContract(loci.CarrierKind.PRODUCT),
        alphabets.ValueProfile.STRUCTURAL,
        exactness,
        EntropyInterface.REPLAY_KEY if entropy else EntropyInterface.NONE,
    )
