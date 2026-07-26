"""Closed, composable simple programs.

The package root is intentionally small: component constructors remain under
their plural owner modules, and complete named constructions live under the
single ``ca.catalog`` namespace.
"""

from . import (
    alphabets,
    catalog,
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
    "catalog",
    "loci",
    "alphabets",
    "seeds",
    "frontiers",
    "neighborhoods",
    "rules",
    "serialization",
]
