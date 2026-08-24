"""Elementary cellular automata as definite SimplePrograms and separate Seeds."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator

from ..core import spaces as space_values
from ..core.seeds import Coordinate, Seed
from ..core.spaces import Space
from ..simpleprograms import SimpleProgram


BINARY = frozenset({0, 1})
LEFT_SELF_RIGHT = (
    (0, -1),
    (0, 0),
    (0, 1),
)
FIXED_ZERO = space_values.fixed(0)
PERIODIC = "periodic"


def space(boundary: object = FIXED_ZERO) -> Space:
    """Return the seed-sized t+1D Space for one supported boundary law."""

    if boundary not in (FIXED_ZERO, PERIODIC):
        raise ValueError("ECA boundary must be fixed-zero or periodic")
    return Space(
        axes=("t", "x"),
        extent="finite-from-seed",
        boundary=boundary,
        coordinates=space_values.box_coordinates,
        normalize=space_values.box_wrap if boundary == PERIODIC else None,
    )


def spaces(
    boundaries: Iterable[object] = (FIXED_ZERO,),
) -> Iterator[Space]:
    """Yield one definite ECA Space per requested boundary law."""

    for boundary in boundaries:
        yield space(boundary)


def alphabets() -> Iterator[frozenset[int]]:
    """Yield the one binary ECA Alphabet."""

    yield BINARY


def neighborhoods(selected_space: Space) -> Iterator[tuple[Coordinate, ...]]:
    """Yield the ordered left/self/right Neighborhood for a t+1D Space."""

    if selected_space.axes != ("t", "x"):
        raise ValueError("ECA Neighborhood requires a t+1D Space")
    yield LEFT_SELF_RIGHT


def rule(number: int) -> Callable[[tuple[object, ...], Coordinate], int]:
    """Compile one Wolfram-numbered elementary cellular-automaton Rule."""

    if isinstance(number, bool) or not isinstance(number, int) or not 0 <= number <= 255:
        raise ValueError("ECA rule number must be an integer from 0 through 255")

    def exact_rule(observed: tuple[object, ...], source: Coordinate) -> int:
        del source
        if len(observed) != 3 or any(value not in BINARY for value in observed):
            raise ValueError("ECA Rule requires three ordered binary observations")
        left, self_value, right = observed
        pattern = (left << 2) | (self_value << 1) | right  # type: ignore[operator]
        return (number >> pattern) & 1

    exact_rule.__name__ = f"eca_rule_{number}"
    setattr(exact_rule, "rule_number", number)
    return exact_rule


def rules(numbers: Iterable[int] = range(256)) -> Iterator[Callable[..., int]]:
    """Yield one exact callable for every requested Wolfram rule number."""

    for number in numbers:
        yield rule(number)


def program(number: int, boundary: object = FIXED_ZERO) -> SimpleProgram:
    """Return one definite ECA SimpleProgram."""

    return SimpleProgram(
        space=space(boundary),
        alphabet=BINARY,
        neighborhood=LEFT_SELF_RIGHT,
        rule=rule(number),
    )


def programs(
    numbers: Iterable[int] = range(256),
    boundaries: Iterable[object] = (FIXED_ZERO,),
) -> Iterator[SimpleProgram]:
    """Yield definite ECA SimplePrograms over explicit Rule and Space choices."""

    selected_numbers = tuple(numbers)
    for selected_space in spaces(boundaries):
        for alphabet in alphabets():
            for neighborhood in neighborhoods(selected_space):
                for exact_rule in rules(selected_numbers):
                    yield SimpleProgram(
                        space=selected_space,
                        alphabet=alphabet,
                        neighborhood=neighborhood,
                        rule=exact_rule,
                    )


def centered_seed(width: int) -> Seed:
    """Return one black cell centered in an explicitly sized white row."""

    if isinstance(width, bool) or not isinstance(width, int) or width <= 0 or width % 2 == 0:
        raise ValueError("centered ECA Seed width must be a positive odd integer")
    center = width // 2
    return Seed(
        shape=(width,),
        values={(0, x): int(x == center) for x in range(width)},
    )


def seeds(widths: Iterable[int]) -> Iterator[Seed]:
    """Yield centered single-cell Seeds for explicit widths."""

    for width in widths:
        yield centered_seed(width)


__all__ = [
    "BINARY",
    "FIXED_ZERO",
    "LEFT_SELF_RIGHT",
    "PERIODIC",
    "alphabets",
    "centered_seed",
    "neighborhoods",
    "program",
    "programs",
    "rule",
    "rules",
    "seeds",
    "space",
    "spaces",
]
