"""Independent helpers for reading and serving existing viewer bundles.

Episode projection and bundle export are deliberately outside the primitive
kernel. This downstream module does not participate in program execution.
"""

from .format import decode_header
from .server import serve

__all__ = [
    "decode_header",
    "serve",
]
