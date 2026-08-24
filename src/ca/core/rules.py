"""Small stable values and helpers for exact transition Rules."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    """One named callable with stable identity and ordinary parameters."""

    name: str
    function: Callable[..., object]
    parameters: tuple[object, ...] = ()
    index: object | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Rule name must be nonempty")
        if not callable(self.function):
            raise TypeError("Rule function must be callable")
        object.__setattr__(self, "parameters", tuple(self.parameters))

    @property
    def __name__(self) -> str:
        """Expose the familiar function-name attribute."""

        return self.name

    def __call__(self, observed: tuple[object, ...]) -> object:
        return self.function(observed, *self.parameters)


__all__ = ["Rule"]
