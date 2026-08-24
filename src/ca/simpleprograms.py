"""Composition of four definite mechanics values into a SimpleProgram."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .core import alphabets
from .core.seeds import Coordinate
from .core.spaces import Space


@dataclass(frozen=True)
class SimpleProgram:
    """One definite reusable dynamics, independent of Seed."""

    space: Space
    alphabet: object
    neighborhood: object
    rule: Callable[[tuple[object, ...], Coordinate], object]

    def __post_init__(self) -> None:
        if not isinstance(self.space, Space):
            raise TypeError("SimpleProgram.space must be a Space")
        if not callable(self.neighborhood) and not isinstance(
            self.neighborhood, tuple
        ):
            raise TypeError("Neighborhood must be an offset tuple or callable")
        if isinstance(self.neighborhood, tuple) and any(
            not isinstance(offset, tuple) or len(offset) != len(self.space.axes)
            for offset in self.neighborhood
        ):
            raise ValueError("Neighborhood offsets must match Space coordinate rank")
        if not callable(self.rule):
            raise TypeError("Rule must be callable")

        boundary = self.space.boundary
        if (
            isinstance(boundary, tuple)
            and len(boundary) == 2
            and boundary[0] == "fixed"
            and not alphabets.accepts(self.alphabet, boundary[1])
        ):
            raise ValueError("fixed boundary value is not admitted by Alphabet")


__all__ = ["SimpleProgram"]
