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
from typing import Generic, TypeVar

from . import alphabets, loci


C = TypeVar("C")
ExactSeedValue = bool | int | Fraction | str


class SeedValidationError(ValueError):
    """A Seed descriptor is malformed or contains an unknown node."""


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
        if not isinstance(self.value_profile, alphabets.ValueProfile):
            raise TypeError("value_profile must be alphabets.ValueProfile")


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


class BoundaryPolicy(Enum):
    """Closed finite-grid boundary policies."""

    FIXED = "fixed"
    PERIODIC = "periodic"
    REFLECTIVE = "reflective"


@dataclass(frozen=True)
class GridBoundary:
    """Boundary data carried by a finite-grid construction."""

    policy: BoundaryPolicy
    exterior: ExactSeedValue | None = None

    def __post_init__(self) -> None:
        if self.policy is BoundaryPolicy.FIXED and self.exterior is None:
            raise SeedValidationError("a fixed boundary requires an exterior value")
        if self.policy is not BoundaryPolicy.FIXED and self.exterior is not None:
            raise SeedValidationError(
                "only a fixed boundary may carry an exterior value"
            )


@dataclass(frozen=True)
class ExactSource(Generic[C]):
    """One fully specified initial configuration."""

    configuration: C


@dataclass(frozen=True)
class ConstructiveSource:
    """A closed constructor, never a host-language callable."""

    construction: Construction


@dataclass(frozen=True)
class PartialSource(Generic[C]):
    """A configuration with explicit unresolved roles and obligations."""

    configuration: C
    unresolved: tuple[loci.Locus, ...]
    obligations: tuple[loci.SelectorExpr, ...]

    def __post_init__(self) -> None:
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

    def __post_init__(self) -> None:
        probability = self.probability_true
        if isinstance(probability, bool) or not isinstance(probability, Fraction):
            raise TypeError("probability_true must be fractions.Fraction")
        if probability < 0 or probability > 1:
            raise SeedValidationError("probability_true must lie in [0, 1]")
        if self.false_value == self.true_value:
            raise SeedValidationError("Bernoulli outcomes must be distinct")


@dataclass(frozen=True)
class UniformTupleLaw:
    """Uniform tuples over ``range(value_count)`` with explicit exclusions."""

    length: int
    value_count: int
    excluded: tuple[tuple[int, ...], ...] = ()

    def __post_init__(self) -> None:
        if isinstance(self.length, bool) or self.length <= 0:
            raise SeedValidationError("uniform tuple length must be positive")
        if isinstance(self.value_count, bool) or self.value_count <= 0:
            raise SeedValidationError("uniform tuple value_count must be positive")
        for item in self.excluded:
            if len(item) != self.length:
                raise SeedValidationError("excluded tuple has the wrong length")
            if any(value < 0 or value >= self.value_count for value in item):
                raise SeedValidationError("excluded tuple value is outside the law")
        if len(set(self.excluded)) != len(self.excluded):
            raise SeedValidationError("excluded tuples must be unique")
        if len(self.excluded) >= self.value_count**self.length:
            raise SeedValidationError("uniform tuple law has empty support")


@dataclass(frozen=True)
class IntensionalProbabilityLaw:
    """A closed, non-enumerated probability-law presentation."""

    binder: str
    relation: loci.SelectorExpr

    def __post_init__(self) -> None:
        if not self.binder:
            raise SeedValidationError("an intensional law binder cannot be empty")


ProbabilityLaw = BernoulliLaw | UniformTupleLaw | IntensionalProbabilityLaw


@dataclass(frozen=True)
class LawSource:
    """A replayable probability measure over initial configurations."""

    law: ProbabilityLaw
    construction: Construction | None = None


@dataclass(frozen=True)
class IntensionalSource:
    """A finite closed presentation of a non-enumerated initial object."""

    binder: str
    relation: loci.SelectorExpr

    def __post_init__(self) -> None:
        if not self.binder:
            raise SeedValidationError("an intensional source binder cannot be empty")


@dataclass(frozen=True)
class ProductPart(Generic[C]):
    key: str
    seed: "Seed[C]"

    def __post_init__(self) -> None:
        if not self.key:
            raise SeedValidationError("product part keys cannot be empty")


@dataclass(frozen=True)
class ProductSource(Generic[C]):
    parts: tuple[ProductPart[C], ...]

    def __post_init__(self) -> None:
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
        if not self.parts:
            raise SeedValidationError("an overlay needs at least one part")


@dataclass(frozen=True)
class MixturePart(Generic[C]):
    weight: Fraction
    seed: "Seed[C]"

    def __post_init__(self) -> None:
        if isinstance(self.weight, bool) or not isinstance(self.weight, Fraction):
            raise TypeError("mixture weights must be fractions.Fraction")
        if self.weight <= 0:
            raise SeedValidationError("mixture weights must be positive")


@dataclass(frozen=True)
class MixtureSource(Generic[C]):
    parts: tuple[MixturePart[C], ...]

    def __post_init__(self) -> None:
        if not self.parts:
            raise SeedValidationError("a mixture needs at least one part")
        if sum((part.weight for part in self.parts), Fraction(0)) != 1:
            raise SeedValidationError("mixture weights must sum exactly to one")


@dataclass(frozen=True)
class ProductLawSource(Generic[C]):
    """Named source laws whose independence is stated explicitly."""

    parts: tuple[ProductPart[C], ...]

    def __post_init__(self) -> None:
        _validate_keys(self.parts)
        if any(not _has_probability_law(part.seed.source) for part in self.parts):
            raise SeedValidationError("every product-law part must contain a law")


@dataclass(frozen=True)
class RefinedSource(Generic[C]):
    source: "Seed[C]"
    constraint: loci.SelectorExpr


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

    def __post_init__(self) -> None:
        _validate_source(self.source)
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
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
    exactness_profile: ExactnessProfile = ExactnessProfile.EXACT,
) -> Seed[C]:
    """Describe one fully specified configuration."""

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
    contract = _common_contract(tuple(part.seed for part in normalized))
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
    common = _common_contract(tuple(part.seed for part in normalized))
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
) -> Seed[C]:
    """Build an exact Bernoulli law; floats and ambient RNGs are rejected."""

    return law(
        BernoulliLaw(support, probability_true, false_value, true_value),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
    )


def sequence(
    values: tuple[ExactSeedValue, ...],
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
) -> Seed[C]:
    """Construct one exact ordered history/word configuration."""

    if not values:
        raise SeedValidationError("sequence values cannot be empty")
    return constructive(
        Construction(ConstructionOp.SEQUENCE, (values,)),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
    )


def pair(
    previous: ExactSeedValue,
    current: ExactSeedValue,
    *,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
) -> Seed[C]:
    """Construct the two-value history used by second-order recurrences."""

    return sequence(
        (previous, current),
        configuration_contract=configuration_contract,
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
    return law(
        UniformTupleLaw(2, value_count, excluded),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
        construction=Construction(ConstructionOp.SEQUENCE),
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
    boundary: GridBoundary,
    configuration_contract: loci.CarrierContract,
    value_profile: alphabets.ValueProfile,
) -> Seed[C]:
    """Construct a rank-1/2/3 finite grid without rendering machinery."""

    if not 1 <= len(shape) <= 3:
        raise SeedValidationError("finite-grid rank must be 1, 2, or 3")
    if any(isinstance(size, bool) or size <= 0 for size in shape):
        raise SeedValidationError("finite-grid extents must be positive")
    cell_count = 1
    for size in shape:
        cell_count *= size
    if len(values) != cell_count:
        raise SeedValidationError(
            f"finite-grid needs {cell_count} values, got {len(values)}"
        )
    boundary_atom: tuple[tuple[str, ExactSeedValue], ...] = (
        ("policy", boundary.policy.value),
        *((("exterior", boundary.exterior),) if boundary.exterior is not None else ()),
    )
    return constructive(
        Construction(ConstructionOp.GRID, (shape, values, boundary_atom)),
        configuration_contract=configuration_contract,
        value_profile=value_profile,
    )


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
