"""Closed writable capability envelopes built from raw regions.

The Goal 7 target layer in this module owns ``WritableRegion`` descriptors,
existing and fresh capability schemas, target contracts, namespaces, and
composition. A Frontier is the complete possible-write envelope for one
application. It does not select firing sites, expose readable values, resolve
collisions, or prescribe commit policy; those choices belong to Rule data and
the one generic application law.

The target shell builds only from ``loci.py`` and is inert. The incompatible
0.1 ``Frontier``/``time_slice`` contract remains complete below the explicit
legacy divider until the atomic G7-01 cutover.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Literal, NoReturn, TypeVar

from . import loci


C = TypeVar("C")
W = TypeVar("W")


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.1: Singular Writable Capabilities
# ---------------------------------------------------------------------------


class FrontierPrimitive(Enum):
    """Closed writable-envelope primitives."""

    CAPABILITY_SPACE = "frontier.capability-space"
    TARGET_CONTRACT = "frontier.target-contract"
    FRESH_NAMESPACE = "frontier.fresh-namespace"


@dataclass(frozen=True)
class WritableRegion(Generic[C, W]):
    """Closed resolver descriptor for one complete writable envelope."""

    descriptor: loci.Region


def _not_implemented() -> NoReturn:
    """Raise the standard error for an unfinished Goal 7 Frontier factory."""

    raise NotImplementedError("Goal 7 Frontier scaffold is not implemented")


def everywhere() -> WritableRegion[C, W]:
    """Authorize the complete support described by the configuration contract."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Goal 7 Phase 1.2: Writable-Envelope Composition
# ---------------------------------------------------------------------------


def union(parts: tuple[WritableRegion[C, W], ...]) -> WritableRegion[C, W]:
    """Compose complete writable envelopes by explicit union."""

    _not_implemented()


# ---------------------------------------------------------------------------
# Goal 7 Phase 2: Structural Writable Families
# ---------------------------------------------------------------------------

# Product, relative/dilated, matched-interface, dynamic-address, fresh-child,
# whole-region, and intensional envelopes enter here after their closed
# capability and reconstruction contracts are fixed.


# ---------------------------------------------------------------------------
# Goal 7 Phase 3: Presets and Aliases
# ---------------------------------------------------------------------------

# Presets delegate to the capability primitives and cannot add scheduling or
# collision behavior.


# ===========================================================================
# Legacy 0.1 implementation retained until atomic G7-01 cutover
# ===========================================================================


CombineMode = Literal["or", "and", "xor"]


@dataclass(frozen=True)
class Frontier:
    """Structured frontier definition.

    `components` stores one or more absolute-coordinate loci selectors.
    Singular frontiers use one component. Compound frontiers use multiple
    components and combine them with `combine`, usually OR, to determine the
    active update-site support for the current state slice.
    """

    components: tuple[loci.Selector, ...]
    combine: CombineMode = "or"
    name: str | None = None
    params: Mapping[str, Any] | None = None
    family: str | None = None


def time_slice(shape: Sequence[int]) -> Frontier:
    """Select the full current state slice.

    This is the default full-throttle cellular-automaton frontier: every active
    spatial site at the current time `t` is eligible to update. The selected
    coordinates are current-state sites `[t, x, y, z]`; the generator maps them
    to `[t+1, x, y, z]` when writing.

    This is a singular frontier built directly from `loci.absolute_universe`
    restricted to the current time and wrapped in `loci.selector`.
    """

    space = loci.coordinate_space(shape)

    universe = loci.absolute_universe(space, t=0)
    component = loci.selector(
        universe,
        order="lex",
        frame="absolute",
    )

    return Frontier(
        components=(component,),
        name="time_slice",
        params={"t": 0},
        family="time_slice",
    )
