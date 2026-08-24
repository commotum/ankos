"""Binary bundle helpers for the static ANKoS viewer."""

from __future__ import annotations

import json
import struct
from typing import Any


MAGIC = b"ANKOSV1\0"
HEADER_PREFIX_LENGTH = len(MAGIC) + 4
HEADER_ALIGNMENT = 8
FORMAT_NAME = "ankos.viz.bundle"
FORMAT_VERSION = 1


def align_offset(offset: int, alignment: int = HEADER_ALIGNMENT) -> int:
    """Return the next offset aligned to `alignment` bytes."""

    offset = int(offset)
    alignment = int(alignment)
    if alignment <= 0:
        raise ValueError(f"alignment must be positive, got {alignment}")
    remainder = offset % alignment
    return offset if remainder == 0 else offset + (alignment - remainder)


def encode_bundle(header: dict[str, Any], payload: bytes) -> bytes:
    """Return a complete `.ankos` bundle from a JSON header and payload bytes."""

    header_bytes = json.dumps(
        header,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    padded_header_length = align_offset(HEADER_PREFIX_LENGTH + len(header_bytes)) - HEADER_PREFIX_LENGTH
    header_bytes = header_bytes + (b" " * (padded_header_length - len(header_bytes)))
    return MAGIC + struct.pack("<I", padded_header_length) + header_bytes + payload


def decode_header(data: bytes) -> tuple[dict[str, Any], int]:
    """Decode a bundle header and return `(header, payload_base_offset)`."""

    if len(data) < HEADER_PREFIX_LENGTH:
        raise ValueError("bundle is shorter than header prefix")
    if data[: len(MAGIC)] != MAGIC:
        raise ValueError("bundle magic does not match ANKOSV1")

    header_length = struct.unpack("<I", data[len(MAGIC) : HEADER_PREFIX_LENGTH])[0]
    payload_base = HEADER_PREFIX_LENGTH + int(header_length)
    if len(data) < payload_base:
        raise ValueError("bundle is shorter than declared header length")

    header = json.loads(data[HEADER_PREFIX_LENGTH:payload_base].decode("utf-8"))
    return header, payload_base


__all__ = [
    "FORMAT_NAME",
    "FORMAT_VERSION",
    "HEADER_ALIGNMENT",
    "HEADER_PREFIX_LENGTH",
    "MAGIC",
    "align_offset",
    "decode_header",
    "encode_bundle",
]
