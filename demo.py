"""One-file sketch of a minimal neighborhood layer and a dyad catalog."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ca import loci


# =============================================================================
# Imagined file: neighborhood.py
# =============================================================================

NEIGHBORHOOD_PY_DOCSTRING = """Minimal neighborhood composition built from loci.

A neighborhood is the ordered coordinate selection read around one source
address. ``loci.py`` owns canonical ``[t, x, y, z]`` offset universes, metric
calculations, Boolean selection algebra, and coordinate ordering. This module
adds only a small immutable record for preserving independent read groups.

A singular neighborhood component is an ordinary tuple of relative offsets.
A compound Neighborhood contains several such components so a Rule can treat
them independently. There is no Selector wrapper, family metadata, parameter
record, or combine mode here: one component means one read group, while
multiple components preserve multiple read groups.

Ordinary spatial neighborhoods use a zero time offset. Negative time offsets
express explicit temporal memory. Execution later translates these offsets
relative to a source address and constructs values at a new explicit time.
"""


Offset = tuple[int, int, int, int]
Component = tuple[Offset, ...]
Metric = Literal["l1", "l2", "linf"]


@dataclass(frozen=True)
class Neighborhood:
    """One or more ordered, independently observable offset selections."""

    components: tuple[Component, ...]


def _ordered_offsets(coordinates: np.ndarray) -> Component:
    """Freeze canonical loci coordinates as an ordered ordinary value."""

    ordered = loci.order_lex(np.asarray(coordinates, dtype=np.int64))
    return tuple(tuple(int(value) for value in row) for row in ordered.tolist())


def self_at(time_offset: int = 0) -> Component:
    """Select the source address at one relative time."""

    coordinates = loci.offset_universe(
        time_offsets=(time_offset,),
        ranges={},
        active_axes=(),
    )
    return _ordered_offsets(coordinates)


def shell(
    axes: tuple[str, ...],
    *,
    metric: Metric,
    radius: int = 1,
    time_offset: int = 0,
) -> Component:
    """Select offsets exactly one metric radius from the source."""

    radius = int(radius)
    if radius < 0:
        raise ValueError("radius must be nonnegative")

    axis_values = tuple(range(-radius, radius + 1))
    universe = loci.offset_universe(
        time_offsets=(time_offset,),
        ranges={axis: axis_values for axis in axes},
        active_axes=axes,
    )
    distances = loci.norm(universe, axes, metric=metric)
    selected = (
        np.isclose(distances, radius)
        if metric == "l2"
        else distances == radius
    )
    return _ordered_offsets(universe[selected])


def difference(left: Component, right: Component) -> Component:
    """Keep the ordered offsets in ``left`` that do not occur in ``right``."""

    excluded = set(right)
    return tuple(offset for offset in left if offset not in excluded)


def compose(*components: Component) -> Neighborhood:
    """Preserve singular selections as independent read groups."""

    return Neighborhood(components=tuple(components))


# =============================================================================
# Imagined file: dyad.py
# =============================================================================

DYAD_PY_DOCSTRING = """Definite dyad neighborhoods assembled from loci selections.

This catalog declares reusable singular selections first, then combines them
into the four Dyadlags, Dyadrads, and Dyadaxes Neighborhoods. The definitions
contain no selector objects or named factory machinery: their complete meaning
is visible in ordinary offset values and their component grouping.

Dyadlags preserves three temporal reads of the same address. Dyadrads preserves
self and two one-dimensional radial shells. The two Dyadaxes definitions
preserve self, axis-adjacent neighbors, and the remaining surrounding neighbors
in two and three spatial dimensions respectively.
"""


# Singular selections.

SELF = self_at(0)
LAG_1 = self_at(-1)
LAG_2 = self_at(-2)

RADIUS_1 = shell(("x",), metric="linf", radius=1)
RADIUS_2 = shell(("x",), metric="linf", radius=2)

CARDINALS_2D = shell(("x", "y"), metric="l1", radius=1)
SURROUNDING_2D = shell(("x", "y"), metric="linf", radius=1)
DIAGONALS_2D = difference(SURROUNDING_2D, CARDINALS_2D)

FACES_3D = shell(("x", "y", "z"), metric="l1", radius=1)
SURROUNDING_3D = shell(("x", "y", "z"), metric="linf", radius=1)
EDGES_AND_CORNERS_3D = difference(SURROUNDING_3D, FACES_3D)


# Compound neighborhoods.

DYADLAGS_0D = compose(SELF, LAG_1, LAG_2)
DYADRADS_1D = compose(SELF, RADIUS_1, RADIUS_2)
DYADAXES_2D = compose(SELF, CARDINALS_2D, DIAGONALS_2D)
DYADAXES_3D = compose(SELF, FACES_3D, EDGES_AND_CORNERS_3D)


def main() -> None:
    """Display the read-group sizes of the four composed Neighborhoods."""

    neighborhoods = {
        "dyadlags_0d": DYADLAGS_0D,
        "dyadrads_1d": DYADRADS_1D,
        "dyadaxes_2d": DYADAXES_2D,
        "dyadaxes_3d": DYADAXES_3D,
    }
    for name, neighborhood in neighborhoods.items():
        sizes = tuple(len(component) for component in neighborhood.components)
        print(f"{name}: {sizes}")


if __name__ == "__main__":
    main()
