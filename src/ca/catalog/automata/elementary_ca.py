"""Finite fixed-support elementary cellular automata."""

from __future__ import annotations

from collections.abc import Iterable, Iterator

from ...core import spaces as space_values
from ...core import seeds as seed_values
from ...core.rules import Rule
from ...core.seeds import Seed
from ...core.spaces import Space
from ...simpleprograms import SimpleProgram


ALPHABET = (0, 1)
NEIGHBORHOOD = (
    (-1,),
    (0,),
    (1,),
)
DEFAULT_SPACE = space_values.cartesian(
    ("t", "x"),
    boundary=space_values.fixed(0),
)


def _apply_rule(
    observed: tuple[int, int, int],
    table: tuple[int, ...],
) -> int:
    left, center, right = observed
    pattern = 4 * int(left) + 2 * int(center) + int(right)
    return table[pattern]


def rule(number: int) -> Rule:
    """Return one stable Wolfram-numbered elementary Rule."""

    if (
        isinstance(number, bool)
        or not isinstance(number, int)
        or not 0 <= number <= 255
    ):
        raise ValueError("ECA rule number must be an integer from 0 through 255")

    table = tuple((number >> pattern) & 1 for pattern in range(8))
    return Rule(
        name=f"eca_rule_{number}",
        function=_apply_rule,
        parameters=(table,),
        index=number,
    )


def rules(numbers: Iterable[int] = range(256)) -> Iterator[Rule]:
    """Yield one exact Rule for every requested Wolfram number."""

    for number in numbers:
        yield rule(number)


def program(number: int, *, space: Space = DEFAULT_SPACE) -> SimpleProgram:
    """Return one definite finite ECA SimpleProgram in a selected t+1D Space."""

    if space.axes != ("t", "x"):
        raise ValueError("elementary CA requires a t+1D Space")

    return SimpleProgram(
        space=space,
        alphabet=ALPHABET,
        neighborhood=NEIGHBORHOOD,
        rule=rule(number),
    )


def programs(
    numbers: Iterable[int] = range(256),
    spaces: Iterable[Space] = (DEFAULT_SPACE,),
) -> Iterator[SimpleProgram]:
    """Yield the real product of selected Spaces and Wolfram Rules."""

    selected_spaces = tuple(spaces)
    for number in numbers:
        for selected_space in selected_spaces:
            yield program(number, space=selected_space)


def centered_seed(width: int) -> Seed:
    """Return one black cell centered in an explicitly sized white row."""

    if (
        isinstance(width, bool)
        or not isinstance(width, int)
        or width <= 0
        or width % 2 == 0
    ):
        raise ValueError("centered ECA Seed width must be a positive odd integer")
    center = width // 2
    return seed_values.dense([int(x == center) for x in range(width)])


def centered_seeds(widths: Iterable[int]) -> Iterator[Seed]:
    """Yield centered single-cell Seeds for explicit widths."""

    for width in widths:
        yield centered_seed(width)


__all__ = [
    "ALPHABET",
    "DEFAULT_SPACE",
    "NEIGHBORHOOD",
    "centered_seed",
    "centered_seeds",
    "program",
    "programs",
    "rule",
    "rules",
]
