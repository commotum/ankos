"""Downstream visualization export and local viewer conveniences.

The Goal 7 target surface in this package consumes only explicit
``DatasetEpisode`` and ``DatasetBatch`` tensor views. It does not infer a
representation from a semantic application or rollout result, define semantic
serialization, or influence program execution. Bundle format version 1 and
the local viewer remain independent presentation tooling.
"""


# ---------------------------------------------------------------------------
# Goal 7 Phase 1: Explicit Dataset-View Export
# ---------------------------------------------------------------------------

# ``save_viewer_bundle`` retains its spelling while its accepted source types
# move atomically from legacy Raw records to explicit dataset views.


# ---------------------------------------------------------------------------
# Goal 7 Phase 2: Presentation Convenience
# ---------------------------------------------------------------------------

# Local serving remains a downstream convenience with no semantic authority.


# ===========================================================================
# Legacy 0.1 implementation retained until atomic G7-01 cutover
# ===========================================================================

from .export import VizBundleInfo, save_viewer_bundle
from .server import serve

__all__ = [
    "VizBundleInfo",
    "save_viewer_bundle",
    "serve",
]
