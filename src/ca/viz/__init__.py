"""Downstream visualization export and local viewer conveniences.

The Goal 7 target surface in this package consumes only explicit
``DatasetEpisode`` and ``DatasetBatch`` tensor views. It does not infer a
representation from a semantic application or rollout result, define semantic
serialization, or influence program execution. Bundle format version 1 and
the local viewer remain independent presentation tooling.
"""


from .export import VizBundleInfo, save_viewer_bundle
from .server import serve

__all__ = [
    "VizBundleInfo",
    "save_viewer_bundle",
    "serve",
]
