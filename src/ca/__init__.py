"""Closed, composable simple programs.

The package root is intentionally small: component constructors remain under
their plural owner modules, while complete named constructions will live under
``ca.catalog`` once that later Goal 7 stage lands.
"""

from . import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
    serialization,
)
from .program import SimpleProgram, apply, rollout


__all__ = [
    "SimpleProgram",
    "apply",
    "rollout",
    "program",
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "serialization",
]
