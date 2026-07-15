#!/usr/bin/env python3
"""Deterministic Stage 2 corpus, structure, routing, and sample primitives."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator

from guardrail_lib import (
    GuardrailError,
    canonical_json_bytes,
    git_tree_identity,
    load_json,
    require,
    safe_relative_posix,
    sha256_bytes,
    sha256_file,
)


BASELINE_SCHEMA_VERSION = "1.0.0"
LEGACY_RELATIVE = "ref/A-New-Kind-of-Science"
REPAIRED_RELATIVE = "ref/A-New-Kind-of-Science-Repaired"
MONOLITH_RELATIVE = "A-New-Kind-of-Science.md"
ATLAS_RELATIVE = "ANKoS-Atlas.md"
MONOLITH_SHA256 = "55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20"
LEGACY_GIT_TREE = "52b84494ab310afd64762bf0983106414419655e"

ROUTING_MARKDOWN_PATHS = (
    "BACK-MATTER/Colophon/Colophon.md",
    "BACK-MATTER/Index/Index.md",
    "BACK-MATTER/Notes/Notes.md",
    "CHAPTERS/1-The-Foundations-for-a-New-Kind-of-Science/The-Foundations-for-a-New-Kind-of-Science.md",
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md",
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md",
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md",
    "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md",
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md",
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md",
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md",
    "CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md",
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md",
    "CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md",
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md",
    "FRONT-MATTER/Contents/Contents.md",
    "FRONT-MATTER/Preface/Preface.md",
)

ROUTING_SPAN_SPECS: dict[str, tuple[tuple[int, int, int | None, int | None, str, str], ...]] = {
    "FRONT-MATTER/Contents/Contents.md": (
        (1, 26, None, None, "GENERATED_METADATA", "GENERATED_NAVIGATION_NO_AUTHOR_TEXT_PROJECTION"),
    ),
    "FRONT-MATTER/Preface/Preface.md": (
        (1, 74, 86, 166, "PREFACE", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/1-The-Foundations-for-a-New-Kind-of-Science/The-Foundations-for-a-New-Kind-of-Science.md": (
        (1, 205, 168, 396, "CH01", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/2-The-Crucial-Experiment/The-Crucial-Experiment.md": (
        (1, 239, 400, 678, "CH02", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md": (
        (1, 683, 682, 1366, "CH03", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/4-Systems-Based-on-Numbers/Systems-Based-on-Numbers.md": (
        (1, 595, 1370, 2142, "CH04", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md": (
        (1, 521, 2144, 2698, "CH05", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/6-Starting-from-Randomness/Starting-from-Randomness.md": (
        (1, 715, 2702, 3420, "CH06", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/7-Mechanisms-in-Programs-and-Nature/Mechanisms-in-Programs-and-Nature.md": (
        (1, 907, 3422, 4336, "CH07", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/8-Implications-for-Everyday-Systems/Implications-for-Everyday-Systems.md": (
        (1, 797, 4338, 5164, "CH08", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/9-Fundamental-Physics/Fundamental-Physics.md": (
        (1, 1413, 5166, 6584, "CH09", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/10-Processes-of-Perception-and-Analysis/Processes-of-Perception-and-Analysis.md": (
        (1, 1043, 6588, 7692, "CH10", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/11-The-Notion-of-Computation/The-Notion-of-Computation.md": (
        (1, 869, 7694, 8608, "CH11", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
    ),
    "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md": (
        (1, 2003, 8610, 10622, "CH12", "REFLOWED_OR_NORMALIZED_ROUTING_ONLY"),
        (2004, 2198, 10623, 10817, "GENERAL_NOTES", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (2199, 2275, 10818, 10894, "N01", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (2276, 3011, 10895, 11630, "N02", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (3012, 3463, 11631, 12082, "N03", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
    ),
    "BACK-MATTER/Notes/Notes.md": (
        (1, 1, 12085, 12085, "N03", "ONE_LINE_STRAY_ROUTE"),
    ),
    "BACK-MATTER/Index/Index.md": (
        (1, 401, 12089, 12498, "N03", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (402, 1360, 12499, 13459, "N04", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (1361, 2099, 13460, 14198, "N05", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (2100, 2748, 14199, 14847, "N06", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (2749, 3483, 14848, 15582, "N07", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (3484, 3912, 15583, 16011, "N08", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (3913, 4987, 16012, 17086, "N09", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (4988, 5345, 17087, 17442, "N10", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
    ),
    "BACK-MATTER/Colophon/Colophon.md": (
        (1, 751, 17444, 18194, "N10", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (752, 1584, 18195, 19027, "N11", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (1585, 3382, 19028, 20825, "N12", "MALFORMED_CROSS_DOCUMENT_ROUTE"),
        (3383, 5014, 20826, 22457, "INDEX", "ACTUAL_INDEX_INSIDE_NOMINAL_COLOPHON"),
        (5015, 5053, 22458, 22498, "COLOPHON", "ACTUAL_COLOPHON_AT_FILE_TAIL"),
    ),
}

SEGMENT_STARTS = (
    ("PUBLICATION_AND_CONTENTS", 1, "# STEPHEN WOLFRAM ANEW KIND OF SCIENCE"),
    ("PREFACE", 86, "#### **Preface**"),
    ("CH01", 168, "## The Foundations for a New Kind of Science"),
    ("CH02", 400, "#### The Crucial Experiment"),
    ("CH03", 682, "#### The World of Simple Programs"),
    ("CH04", 1370, "#### Systems Based on Numbers"),
    ("CH05", 2144, "#### Two Dimensions and Beyond"),
    ("CH06", 2702, "#### Starting from Randomness"),
    ("CH07", 3422, "## Mechanisms in Programs and Nature"),
    ("CH08", 4338, "## Implications for Everyday Systems"),
    ("CH09", 5166, "#### Fundamental Physics"),
    ("CH10", 6588, "## Processes of Perception and Analysis"),
    ("CH11", 7694, "#### The Notion of Computation"),
    ("CH12", 8610, "### The Principle of Computational Equivalence"),
    ("GENERAL_NOTES", 10623, "#### General Notes"),
    ("N01", 10818, "#### The Foundations for a New Kind of Science"),
    ("N02", 10895, "#### The Crucial Experiment"),
    ("N03", 11631, "#### The World of Simple Programs"),
    ("N04", 12499, "#### Systems Based on Numbers"),
    ("N05", 13460, "#### Two Dimensions and Beyond"),
    ("N06", 14199, "#### Starting from Randomness"),
    ("N07", 14848, "#### Mechanisms in Programs and Nature"),
    ("N08", 15583, "#### Implications for Everyday Systems"),
    ("N09", 16012, "#### **Fundamental Physics**"),
    ("N10", 17087, "#### Processes of Perception and Analysis"),
    ("N11", 18195, "#### The Notion of Computation"),
    ("N12", 19028, "#### The Principle of Computational Equivalence"),
    ("INDEX", 20826, "#### Index"),
    ("COLOPHON", 22458, "#### Colophon"),
)

EXPECTED_SEGMENT_SIGNATURES = (
    ("PUBLICATION_AND_CONTENTS", "8ef06068dd37197c7c08b45edd5a682834f4603a66075a61a7c72ae990d9e313", "458c549530df22b6d47be952d1381d989d1bed37caceb943073ba85319d62978"),
    ("PREFACE", "c485e293f373b02cfde1c9de89f49f5139b7cee984c804e6b5d0e130f0a6d5d9", "73999c042b197a4c32cb9c1a08bb4bf2a2e3543553b09a40fd5758164cfc4da9"),
    ("CH01", "6997d786bef122c3a8a89724d8c08c90a9cd3cc4e295007f0675c67ccd7e6e0d", "283d3157f9e1947e6225d1399bc8a3e5669bc4e5c4b3b699bb5f4664cf170a01"),
    ("CH02", "4dbf451fdd5efcd0e94ee74d93bb43403359514986e3122208a63f36efe9b12c", "cc5e35e0c2d85574a21c24314d9999d17976c193b75e8053ef18e97d506f1600"),
    ("CH03", "dcac1784fdb6ae6d6e9b1fa6ca739f1ee24c291cb2c5093b60afc2d7d211dcd3", "f1c0c75625fc07959fd88021ad95f34e7408126273f7f7574aedacd809fb8c57"),
    ("CH04", "c60e55e9a7b0bbd03c332ddb48535eab2e2ddbd2d2ce27da10faca7d191e3c53", "b297ee0eccf45e70168d6493ebd04798680ee105269e18ec3618149fc5a30bcc"),
    ("CH05", "0c12e8df3a14a07297f3f92d197d213538a9265a6b231723c753f4ef82e1cae5", "1fc33877e38b6b32c11c4719eac86a5b6ed5967dcce628a177985999d552af70"),
    ("CH06", "025191d7d74f08979e522b89ecf360d49ca14675c61defce16fb550dbcbda1b5", "9c9cd471d53d76fdabd9e6dc3e07f54503c442403ebe40b5cc6eb62e7ce56183"),
    ("CH07", "f4909a5db09376033e990f92f009cc4345144e6ed8583b1869777c1d7972a937", "e4178f673077dfff13a9923ad31bbd654b93f91819ff30ddc5feb785dfcfda98"),
    ("CH08", "fb8d8c89397c17a5daac6b905f03e2eba1485ea567d3140d9d9975784f3e52fa", "d423e74d945b5e795a24463e0a2053ff4e22abe3534dfb0fed8924fe191999cf"),
    ("CH09", "6abd7033ba736857dae430d4b5c6ff32e6c4bb1801ec59c157fcdf7aea5f4130", "49bb0f2754dd991b0191e3939d22ed489281523a54f69f50e3c6b335ba500267"),
    ("CH10", "859c933e7ef3b4f15d9f16d31b0ba07763fb9253cb7d695cd7ffdfafa0dd1f19", "0527885a8b6b8202df02a09b772ef120f68af65f274640f59becec826ce38cde"),
    ("CH11", "a0beedfbac0cb35be08237d95606347e041321d98d4a9ead64adb1239fb47671", "8b15e4c97d25503b14133415500e9349a118de4cea0ed6675027cde8512950fb"),
    ("CH12", "573ab81948dc5fdcc7420466b60ddce31330e63962a8c43f37bc157ccc50a39f", "22b691a60d0c1044d74489fa994faa04ebef87bf0e2dee26e72e1dc758031110"),
    ("GENERAL_NOTES", "9d553220a4077c36a16888ec0658af3a16916f0d1416a185d212fc2a63c29841", "38d0c2b644a8beab0f326b87b08769b715bbe589c97cab44f52037a7e5d8f1cc"),
    ("N01", "501636c9c8535d4299c67bd84a8e50af168eb132bb89133a9a17aa36d0756599", "cc1cdc9398113d528f9efc7986104fe9534e3bfab1eb5d9d3ba395d9eaccbe8d"),
    ("N02", "4971910a76371ba9dba9242e0651f4e83313fbcc108726d5ad1e8f745270d912", "aa419153087b4a4f7a01086b20e15f7709b805c1c143e39d3ee9de67a36e7dc8"),
    ("N03", "5df4c168afeb17d4979f1fbab558a60104ca00076a193ec5dcb06901c2b2879a", "7914ed003cbbd35f63afaa5d8473ed0ba33889535631ba75cebfe58e232653c1"),
    ("N04", "42fd6a2562549ecda30e0ec198c293c188686d198cf2662406add629a53d220b", "b1c16e20f559229ac1ac388ee07e1e735272aacbf4275871dde5de7b3721e12f"),
    ("N05", "4114584ca8e10cc5b3cc9983ba7174f7f4666af5211c90c2dd7ba6cd9f6803d9", "c87ae21687fde9e6d8a7e1285992991ac7ef34e4bda75539c403dbbbb7850d5a"),
    ("N06", "997643316572268d085256331cb0162f39a7daed336b274b74314a2f31c97053", "fc46b986d0d75fd61d14ce670dd0115feb6e70945eb3e0a11627cc3684c11d40"),
    ("N07", "db8e01a78ed36d143cf7e117ceaab09be03108447185a289b17f82e6a9a48a84", "c5db32ed5bfbca277cc44cdf905cb95bf50d2a6fc8e03c8949463c77f23492a3"),
    ("N08", "4b6ba64f644d388bdc6d937c2433cf4196b8c63391da06ebd611eafbfe77bc41", "d2b7003bb34955c33a0f37be5d247bc1ed977613f39689de1b09563c5cdd3146"),
    ("N09", "7efca524c6f30687a7a14c20da6d6fb9e4518c62b6c17bf7992d0efa9322fd6f", "9788a6dba710b990839f266d5f75b5583fea0a1ee6abbc1704dd9308876de2fc"),
    ("N10", "eb7cf5b2548df7419a2d1f8217526dc4d8d512c59a2fb51bd70c7fd2421d458e", "a76e9a1b45105d31222d96b9776122de67c66296f18bd592124194bab6006dde"),
    ("N11", "d16de3985db98c1ed6433f4941d9ec0b5d24746260fc3ddc6221c9a043992730", "972fedfa44f9c1437d0311591e0ae222985c035d7291415ad350a8005ddc1d42"),
    ("N12", "e0db83da8653b3c793a6bf9906d1ba148cc1ca9fa461c600bd24ee185b353cac", "c75c3155c8c482fc58d973d70a3d08550366abc79a0590749799f1872ba91ce2"),
    ("INDEX", "b187b13d34f632b39f98e4900e0293d9335ec01d4398870ce4009798917062ce", "4a4823cb040deb460627bb98f265a332122303133e7fc997b0b4be2b3c506bd0"),
    ("COLOPHON", "6e278b56ae7a0734bf3de0099b580268eebdc0548286541f86a792be6ef46d78", "4bd5961ba0134508c82139eb3a331b6b95f5a6662d328bfb8049ef924bd541dd"),
)

BLOCK_KIND_ENUM = (
    "STRUCTURE_BOUNDARY",
    "PROSE",
    "LIST_ITEM",
    "MATH_INLINE",
    "IMAGE_REFERENCE",
    "HEADING",
    "CODE_BLOCK",
    "MATH_BLOCK",
    "LAYOUT_TABLE",
    "CAPTION",
    "BLOCKQUOTE",
)

RISK_PRIORITY = (
    "INDEX_COLUMN_OR_ENTRY",
    "FORMULA_CODE_RULE_OR_DATA",
    "FIGURE_CAPTION_OR_VISUAL",
    "HEADING_LIST_OR_LAYOUT",
    "PROSE",
)

IMAGE_PATTERN = re.compile(r"!\[[^\]\n]*\]\((?:<)?([^)>\n]+?\.jpeg)(?:>)?(?:\s+[^)\n]+)?\)")
ATX_HEADING_PATTERN = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
LIST_ITEM_PATTERN = re.compile(r"^ {0,3}(?:[-+*]|\d+[.)])[ \t]+")
BLOCKQUOTE_PATTERN = re.compile(r"^ {0,3}>[ \t]?")
FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
PIPE_TABLE_PATTERN = re.compile(r"^\s*\|.*\|\s*$")
MATH_ONLY_PATTERN = re.compile(r"^\s*(?:\$\$.*\$\$|\\\[.*\\\]|\$[^$]+\$)\s*$")
CAPTION_PATTERN = re.compile(r"^\s*(?:Figure|Fig\.|Picture|Plate)\s+[A-Za-z0-9]", re.IGNORECASE)

LEX_BLANK = lambda line: not line.strip()
LEX_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LEX_ATX = re.compile(r"^ {0,3}#{1,6}(?:\s|$)")
LEX_IMAGE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
LEX_PIPE_TABLE = re.compile(r"^\s*\|.*\|\s*$")
LEX_LIST = re.compile(r"^\s{0,3}(?:[-+*]|[•■])\s+")
LEX_BLOCKQUOTE = re.compile(r"^\s{0,3}>")
LEX_MATH_ONLY = re.compile(r"^\s*\${1,2}.*\${1,2}\s*$")
LEX_CAPTION = re.compile(
    r"^\s*(?:<sup>[^<]*(?:◆|■)[^<]*</sup>|(?:Figure|Figures|Picture|Pictures)\b)",
    re.IGNORECASE,
)
LEX_INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$).*?(?<!\\)\$")


def stable_json_bytes(value: Any, *, terminal_lf: bool = True) -> bytes:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return payload + (b"\n" if terminal_lf else b"")


def jsonl_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(stable_json_bytes(row) for row in rows)


def git_command(root: Path, args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"Git command failed: git {' '.join(args)}")
    return result.stdout


def split_raw_lines(data: bytes) -> list[dict[str, Any]]:
    """Return logical line records, preserving exact byte extents."""

    if not data:
        return []
    records: list[dict[str, Any]] = []
    start = 0
    line_number = 1
    while start < len(data):
        newline = data.find(b"\n", start)
        if newline < 0:
            end = len(data)
            content_end = end
            terminal_lf = False
        else:
            end = newline + 1
            content_end = newline
            terminal_lf = True
        records.append(
            {
                "line": line_number,
                "byte_start": start,
                "byte_end": end,
                "content": data[start:content_end],
                "terminal_lf": terminal_lf,
            }
        )
        start = end
        line_number += 1
    return records


def line_window_signature(lines: list[dict[str, Any]], focal_line: int) -> str:
    require(1 <= focal_line <= len(lines), "line-window focal line is out of range")
    payload = bytearray(b"ANKOS-LINE-WINDOW-V1\0")
    for number in range(focal_line - 2, focal_line + 3):
        if number < 1:
            item = b"<BOF>"
        elif number > len(lines):
            item = b"<EOF>"
        else:
            item = lines[number - 1]["content"]
        payload.extend(len(item).to_bytes(8, "big"))
        payload.extend(item)
    return sha256_bytes(bytes(payload))


def git_blob_sha1(payload: bytes) -> str:
    framed = b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload
    return hashlib.sha1(framed).hexdigest()  # noqa: S324 - Git object format is SHA-1.


def git_head_entries(root: Path, legacy_relative: str) -> dict[str, dict[str, str]]:
    raw = git_command(root, ["ls-tree", "-rz", "--full-tree", "HEAD", legacy_relative])
    entries: dict[str, dict[str, str]] = {}
    prefix = legacy_relative + "/"
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path_bytes = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split(" ")
        path = path_bytes.decode("utf-8")
        require(kind == "blob", f"unexpected non-blob Git entry: {path}")
        require(path.startswith(prefix), f"Git entry escaped legacy root: {path}")
        relative = path[len(prefix) :]
        require(relative not in entries, f"duplicate Git entry: {relative}")
        entries[relative] = {"mode": mode, "oid": oid}
    return entries


def git_blob_payload(root: Path, oid: str) -> bytes:
    require(re.fullmatch(r"[0-9a-f]{40}", oid) is not None, "invalid Git SHA-1 object ID")
    return git_command(root, ["cat-file", "blob", oid])


def parse_lfs_pointer(payload: bytes) -> dict[str, Any] | None:
    match = re.fullmatch(
        rb"version https://git-lfs\.github\.com/spec/v1\n"
        rb"oid sha256:([0-9a-f]{64})\n"
        rb"size ([0-9]+)\n",
        payload,
    )
    if match is None:
        return None
    return {
        "oid_sha256": match.group(1).decode("ascii"),
        "size": int(match.group(2)),
    }


def parse_jpeg(payload: bytes) -> dict[str, Any]:
    require(payload.startswith(b"\xff\xd8"), "JPEG is missing SOI")
    require(payload.endswith(b"\xff\xd9"), "JPEG is missing terminal EOI")
    index = 2
    while index < len(payload):
        require(payload[index] == 0xFF, "invalid JPEG marker prefix")
        while index < len(payload) and payload[index] == 0xFF:
            index += 1
        require(index < len(payload), "truncated JPEG marker")
        marker = payload[index]
        index += 1
        if marker == 0xD9:
            break
        if marker in {0x01, *range(0xD0, 0xD8)}:
            continue
        require(index + 2 <= len(payload), "truncated JPEG segment length")
        length = int.from_bytes(payload[index : index + 2], "big")
        require(length >= 2 and index + length <= len(payload), "invalid JPEG segment length")
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            require(length >= 8, "truncated JPEG SOF")
            precision = payload[index + 2]
            height = int.from_bytes(payload[index + 3 : index + 5], "big")
            width = int.from_bytes(payload[index + 5 : index + 7], "big")
            components = payload[index + 7]
            require(width > 0 and height > 0, "invalid JPEG dimensions")
            return {
                "width": width,
                "height": height,
                "sof_marker": f"SOF{marker - 0xC0}",
                "sample_precision": precision,
                "component_count": components,
            }
        index += length
    raise GuardrailError("JPEG has no supported SOF marker")


def discover_legacy_files(legacy: Path) -> list[str]:
    require(legacy.is_dir() and not legacy.is_symlink(), "legacy root is missing or aliased")
    rows: list[str] = []
    for path in sorted(legacy.rglob("*"), key=lambda item: item.relative_to(legacy).as_posix().encode("utf-8")):
        require(not path.is_symlink(), f"legacy tree contains a symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file(), f"legacy tree contains an unsupported entry: {path}")
        relative = path.relative_to(legacy).as_posix()
        require(str(safe_relative_posix(relative)) == relative, f"unsafe legacy path: {relative}")
        rows.append(relative)
    return rows


def role_for_path(relative: str) -> str:
    if relative == MONOLITH_RELATIVE:
        return "RAW_AUTHOR_TEXT_MONOLITH"
    if relative == ATLAS_RELATIVE:
        return "INTERPRETIVE_METADATA"
    if relative in ROUTING_MARKDOWN_PATHS:
        return "LEGACY_ROUTING_MARKDOWN"
    if relative.endswith(".jpeg"):
        return "LEGACY_ASSET"
    raise GuardrailError(f"unclassified legacy input: {relative}")


def path_list_digest(paths: Iterable[str]) -> str:
    return sha256_bytes(b"".join(path.encode("utf-8") + b"\n" for path in paths))


def tree_allocated_bytes(legacy: Path) -> int:
    total = legacy.stat(follow_symlinks=False).st_blocks * 512
    for path in legacy.rglob("*"):
        total += path.stat(follow_symlinks=False).st_blocks * 512
    return total


def manifest_input_rows(root: Path, contract: dict[str, Any]) -> list[dict[str, Any]]:
    legacy = root / LEGACY_RELATIVE
    actual_paths = discover_legacy_files(legacy)
    require(len(actual_paths) == 1463, "legacy regular-file count drift")
    require(sum(path.endswith(".md") for path in actual_paths) == 19, "Markdown count drift")
    require(sum(path.endswith(".jpeg") for path in actual_paths) == 1444, "JPEG count drift")
    require(set(ROUTING_MARKDOWN_PATHS) <= set(actual_paths), "routing Markdown allowlist drift")
    head = git_head_entries(root, LEGACY_RELATIVE)
    require(set(head) == set(actual_paths), "Git HEAD and working legacy path sets differ")
    rows: list[dict[str, Any]] = []
    for index, relative in enumerate(actual_paths, 1):
        path = legacy / Path(*PurePosixPath(relative).parts)
        before = path.stat(follow_symlinks=False)
        require(stat.S_ISREG(before.st_mode), f"legacy input is not regular: {relative}")
        require(before.st_nlink == 1, f"legacy input is hardlinked: {relative}")
        payload = path.read_bytes()
        after = path.stat(follow_symlinks=False)
        require(
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            f"legacy input changed during read: {relative}",
        )
        entry = head[relative]
        stored = git_blob_payload(root, entry["oid"])
        role = role_for_path(relative)
        common: dict[str, Any] = {
            "allocated_byte_size_at_capture": before.st_blocks * 512,
            "basename": path.name,
            "byte_size": len(payload),
            "file_id": f"RAW-FILE-{index:04d}",
            "filesystem_mode_at_capture": format(stat.S_IMODE(before.st_mode), "04o"),
            "git_head_blob_oid": entry["oid"],
            "git_object_format": "sha1",
            "git_tree_mode": entry["mode"],
            "relative_path": relative,
            "role": role,
            "sha256": sha256_bytes(payload),
        }
        if relative.endswith(".md"):
            text = payload.decode("utf-8", errors="strict")
            require(not payload.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM drift: {relative}")
            require(b"\r" not in payload, f"CR byte in Markdown: {relative}")
            lines = split_raw_lines(payload)
            require(git_blob_sha1(payload) == entry["oid"], f"direct Git blob mismatch: {relative}")
            common.update(
                {
                    "git_storage": "DIRECT_BLOB",
                    "image": None,
                    "kind": "MARKDOWN",
                    "logical_line_count": len(lines),
                    "media_type": "text/markdown",
                    "text": {
                        "cr_count": 0,
                        "encoding": "UTF-8",
                        "lf_count": payload.count(b"\n"),
                        "mojibake_signature_count": sum(text.count(marker) for marker in ("Ã", "Â", "â€", "ðŸ")),
                        "replacement_character_count": text.count("\ufffd"),
                        "terminal_lf": payload.endswith(b"\n"),
                        "utf8_bom": False,
                    },
                }
            )
        else:
            parsed = parse_jpeg(payload)
            lfs = parse_lfs_pointer(stored)
            require(lfs is not None, f"JPEG HEAD blob is not a strict LFS pointer: {relative}")
            require(lfs["oid_sha256"] == sha256_bytes(payload), f"LFS OID mismatch: {relative}")
            require(lfs["size"] == len(payload), f"LFS size mismatch: {relative}")
            require(git_blob_sha1(stored) == entry["oid"], f"LFS pointer blob mismatch: {relative}")
            common.update(
                {
                    "git_lfs_oid_sha256": lfs["oid_sha256"],
                    "git_lfs_size": lfs["size"],
                    "git_storage": "LFS_POINTER_V1",
                    "image": {**parsed, "decoded_color_mode": "RGB"},
                    "kind": "JPEG",
                    "logical_line_count": None,
                    "media_type": "image/jpeg",
                    "text": None,
                }
            )
        rows.append(common)
    require([row["relative_path"] for row in rows] == actual_paths, "manifest row order drift")
    return rows


def quality_manifest_material(rows: list[dict[str, Any]]) -> bytes:
    projection = [
        {
            "relative_path": row["relative_path"],
            "role": row["role"],
            "byte_size": row["byte_size"],
            "logical_line_count": row["logical_line_count"],
            "sha256": row["sha256"],
        }
        for row in rows
    ]
    return stable_json_bytes(projection, terminal_lf=False)


def build_corpus_manifest(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    rows = manifest_input_rows(root, contract)
    roles = Counter(row["role"] for row in rows)
    kinds = Counter(row["kind"] for row in rows)
    legacy = root / LEGACY_RELATIVE
    jpeg_rows = [row for row in rows if row["kind"] == "JPEG"]
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for row in jpeg_rows:
        hash_groups[row["sha256"]].append(row["relative_path"])
    duplicate_hash_groups = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(hash_groups.items())
        if len(paths) > 1
    ]
    material = quality_manifest_material(rows)
    all_paths = [row["relative_path"] for row in rows]
    markdown_paths = [row["relative_path"] for row in rows if row["kind"] == "MARKDOWN"]
    jpeg_paths = [row["relative_path"] for row in rows if row["kind"] == "JPEG"]
    require(len({row["basename"] for row in jpeg_rows}) == 1444, "JPEG basenames are not unique")
    manifest = {
        "contract_id": contract["contract_id"],
        "counts": {
            "all_regular_files": len(rows),
            "jpeg": kinds["JPEG"],
            "markdown": kinds["MARKDOWN"],
        },
        "discovery_policy": {
            "build_inputs": "EXPLICIT_MANIFEST_ROWS_ONLY",
            "capture_census_root": LEGACY_RELATIVE,
            "capture_census_root_component_exact": True,
            "repaired_sibling_excluded": REPAIRED_RELATIVE,
        },
        "duplicate_jpeg_payload_groups": duplicate_hash_groups,
        "git": {
            "legacy_tree_oid": git_tree_identity(root, "HEAD", LEGACY_RELATIVE),
            "object_format": "sha1",
        },
        "legacy_root": LEGACY_RELATIVE,
        "ordering": "relative_path ascending by raw UTF-8 bytes",
        "path_digests": {
            "all_terminal_lf_sha256": path_list_digest(all_paths),
            "jpeg_terminal_lf_sha256": path_list_digest(jpeg_paths),
            "markdown_terminal_lf_sha256": path_list_digest(markdown_paths),
        },
        "quality_seed_material": {
            "byte_size": len(material),
            "serialization": "UTF-8 sorted-key compact JSON array without terminal LF",
            "sha256": sha256_bytes(material),
        },
        "raw_inputs": rows,
        "role_counts": dict(sorted(roles.items())),
        "schema_version": BASELINE_SCHEMA_VERSION,
        "totals": {
            "logical_bytes": sum(row["byte_size"] for row in rows),
            "markdown_logical_lines": sum(row["logical_line_count"] or 0 for row in rows),
            "regular_file_allocated_bytes_at_capture": sum(row["allocated_byte_size_at_capture"] for row in rows),
            "tree_allocated_bytes_at_capture": tree_allocated_bytes(legacy),
        },
    }
    require(manifest["git"]["legacy_tree_oid"] == LEGACY_GIT_TREE, "legacy Git tree drift")
    require(manifest["role_counts"] == {
        "INTERPRETIVE_METADATA": 1,
        "LEGACY_ASSET": 1444,
        "LEGACY_ROUTING_MARKDOWN": 17,
        "RAW_AUTHOR_TEXT_MONOLITH": 1,
    }, "raw role census drift")
    require(manifest["totals"]["logical_bytes"] == 115037515, "legacy logical-byte total drift")
    require(manifest["totals"]["tree_allocated_bytes_at_capture"] == 118206464, "legacy tree allocation drift")
    require(manifest["quality_seed_material"] == {
        "byte_size": 331724,
        "serialization": "UTF-8 sorted-key compact JSON array without terminal LF",
        "sha256": "ba4146db2e5d54965ce4173656dc5f5cfe91fd2f1c420698b2a6181aff3a98ad",
    }, "quality manifest material drift")
    return manifest


def segment_for_line(segments: list[dict[str, Any]], line: int) -> dict[str, Any]:
    for segment in segments:
        if segment["raw_start_line"] <= line <= segment["raw_end_line"]:
            return segment
    raise GuardrailError(f"logical line lacks a segment owner: {line}")


def build_segments(monolith: bytes, contract: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    require(sha256_bytes(monolith) == MONOLITH_SHA256, "monolith SHA-256 drift")
    lines = split_raw_lines(monolith)
    require(len(lines) == 22498, "monolith logical-line count drift")
    require(monolith.count(b"\n") == 22497 and not monolith.endswith(b"\n"), "monolith newline profile drift")
    documents = contract["canonical_documents"]
    require([row["id"] for row in documents] == [row[0] for row in SEGMENT_STARTS], "canonical document/segment IDs drift")
    expected_signatures = {row[0]: row[1:] for row in EXPECTED_SEGMENT_SIGNATURES}
    segments: list[dict[str, Any]] = []
    for order, ((segment_id, start, marker), document) in enumerate(zip(SEGMENT_STARTS, documents, strict=True)):
        require(lines[start - 1]["content"].decode("utf-8") == marker, f"segment start marker drift: {segment_id}")
        end = SEGMENT_STARTS[order + 1][1] - 1 if order + 1 < len(SEGMENT_STARTS) else len(lines)
        start_byte = lines[start - 1]["byte_start"]
        end_byte = lines[end - 1]["byte_end"]
        start_signature = line_window_signature(lines, start)
        end_signature = line_window_signature(lines, end)
        require((start_signature, end_signature) == expected_signatures[segment_id], f"segment signature drift: {segment_id}")
        segments.append(
            {
                "boundary_status": "PROPOSED_RAW_BOUNDARY_PENDING_STAGE_3_5_WITNESS_VALIDATION",
                "canonical_path": document["path"],
                "document_kind": document["kind"],
                "heading_text": marker,
                "order": order,
                "raw_byte_count": end_byte - start_byte,
                "raw_end_byte_exclusive": end_byte,
                "raw_end_line": end,
                "raw_line_count": end - start + 1,
                "raw_segment_sha256": sha256_bytes(monolith[start_byte:end_byte]),
                "raw_source_path": MONOLITH_RELATIVE,
                "raw_source_sha256": MONOLITH_SHA256,
                "raw_start_byte": start_byte,
                "raw_start_line": start,
                "role": document["role"],
                "segment_id": segment_id,
                "signature": {
                    "algorithm": "SHA-256",
                    "domain": "ANKOS-LINE-WINDOW-V1+NUL",
                    "end_focal_line": end,
                    "end_sha256": end_signature,
                    "expected_occurrence_count": 1,
                    "radius_lines": 2,
                    "start_focal_line": start,
                    "start_sha256": start_signature,
                },
                "title": document["title"],
            }
        )
    require(segments[0]["raw_start_line"] == 1 and segments[-1]["raw_end_line"] == 22498, "segment edge coverage drift")
    require(sum(row["raw_line_count"] for row in segments) == 22498, "segment line arithmetic drift")
    require(sum(row["raw_byte_count"] for row in segments) == len(monolith), "segment byte arithmetic drift")
    for left, right in zip(segments, segments[1:]):
        require(left["raw_end_line"] + 1 == right["raw_start_line"], "segment line gap/overlap")
        require(left["raw_end_byte_exclusive"] == right["raw_start_byte"], "segment byte gap/overlap")
    signature_values = [
        row["signature"][key]
        for row in segments
        for key in ("start_sha256", "end_sha256")
    ]
    require(len(signature_values) == len(set(signature_values)) == 58, "segment boundary signatures are not unique")
    return segments, lines


def _lexical_line_texts(lines: list[dict[str, Any]]) -> list[str]:
    return [row["content"].decode("utf-8", errors="strict") for row in lines]


def _is_indented_code(line: str) -> bool:
    return line.startswith("    ") or line.startswith("\t")


def _starts_nonprose_unit(line: str) -> bool:
    return any(
        pattern.match(line) is not None
        for pattern in (
            LEX_ATX,
            LEX_IMAGE,
            LEX_FENCE,
            LEX_PIPE_TABLE,
            LEX_LIST,
            LEX_BLOCKQUOTE,
            LEX_MATH_ONLY,
            LEX_CAPTION,
        )
    ) or _is_indented_code(line)


def _starts_list_terminator(line: str) -> bool:
    return any(
        pattern.match(line) is not None
        for pattern in (
            LEX_LIST,
            LEX_ATX,
            LEX_IMAGE,
            LEX_FENCE,
            LEX_PIPE_TABLE,
            LEX_BLOCKQUOTE,
        )
    )


def _starts_caption_terminator(line: str) -> bool:
    return any(
        pattern.match(line) is not None
        for pattern in (
            LEX_ATX,
            LEX_IMAGE,
            LEX_FENCE,
            LEX_PIPE_TABLE,
            LEX_LIST,
            LEX_BLOCKQUOTE,
        )
    )


def lexical_partition(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Partition raw lines using frozen, outcome-blind lexical precedence."""

    texts = _lexical_line_texts(lines)
    base: list[dict[str, Any]] = []
    cursor = 0
    while cursor < len(texts):
        start = cursor
        line = texts[cursor]
        kind: str
        if LEX_BLANK(line):
            cursor += 1
            while cursor < len(texts) and LEX_BLANK(texts[cursor]):
                cursor += 1
            kind = "STRUCTURE_BOUNDARY"
        elif (fence_match := LEX_FENCE.match(line)) is not None:
            marker = fence_match.group(1)
            close = re.compile(r"^ {0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*$")
            cursor += 1
            while cursor < len(texts) and close.match(texts[cursor]) is None:
                cursor += 1
            require(cursor < len(texts), f"unterminated raw fence at logical line {start + 1}")
            cursor += 1
            kind = "CODE_BLOCK"
        elif LEX_ATX.match(line) is not None:
            cursor += 1
            kind = "HEADING"
        elif LEX_IMAGE.match(line) is not None:
            cursor += 1
            kind = "IMAGE_REFERENCE"
        elif LEX_PIPE_TABLE.match(line) is not None:
            cursor += 1
            while cursor < len(texts) and LEX_PIPE_TABLE.match(texts[cursor]) is not None:
                cursor += 1
            kind = "LAYOUT_TABLE"
        elif LEX_LIST.match(line) is not None:
            cursor += 1
            while (
                cursor < len(texts)
                and not LEX_BLANK(texts[cursor])
                and not _starts_list_terminator(texts[cursor])
            ):
                cursor += 1
            kind = "LIST_ITEM"
        elif LEX_BLOCKQUOTE.match(line) is not None:
            cursor += 1
            while cursor < len(texts) and LEX_BLOCKQUOTE.match(texts[cursor]) is not None:
                cursor += 1
            kind = "BLOCKQUOTE"
        elif LEX_MATH_ONLY.match(line) is not None:
            cursor += 1
            kind = "MATH_BLOCK"
        elif LEX_CAPTION.match(line) is not None:
            cursor += 1
            while (
                cursor < len(texts)
                and not LEX_BLANK(texts[cursor])
                and not _starts_caption_terminator(texts[cursor])
            ):
                cursor += 1
            kind = "CAPTION"
        elif _is_indented_code(line):
            cursor += 1
            while cursor < len(texts) and _is_indented_code(texts[cursor]):
                cursor += 1
            kind = "CODE_BLOCK"
        else:
            cursor += 1
            while (
                cursor < len(texts)
                and not LEX_BLANK(texts[cursor])
                and not _starts_nonprose_unit(texts[cursor])
            ):
                cursor += 1
            kind = "PROSE"
        require(cursor > start, "raw lexer failed to advance")
        base.append({"start_line": start + 1, "end_line": cursor, "base_kind": kind})
    require(base[0]["start_line"] == 1 and base[-1]["end_line"] == len(lines), "block partition edge drift")
    for left, right in zip(base, base[1:]):
        require(left["end_line"] + 1 == right["start_line"], "block partition gap/overlap")
    return base


def _block_kind_with_inline_math(
    base_kind: str,
    texts: list[str],
    start_line: int,
    end_line: int,
) -> tuple[str, str | None]:
    if base_kind not in {"PROSE", "LIST_ITEM", "BLOCKQUOTE", "CAPTION"}:
        return base_kind, None
    # Match independently per physical line. This cannot manufacture a span by
    # joining unmatched dollar signs across a hard wrap.
    if any(LEX_INLINE_MATH.search(texts[number - 1]) is not None for number in range(start_line, end_line + 1)):
        return "MATH_INLINE", base_kind
    return base_kind, None


def risk_stratum(document_id: str, block_kind: str) -> str:
    if document_id == "INDEX":
        return "INDEX_COLUMN_OR_ENTRY"
    if block_kind in {"MATH_INLINE", "MATH_BLOCK", "CODE_BLOCK"}:
        return "FORMULA_CODE_RULE_OR_DATA"
    if block_kind in {"IMAGE_REFERENCE", "CAPTION"}:
        return "FIGURE_CAPTION_OR_VISUAL"
    if block_kind in {
        "HEADING",
        "LIST_ITEM",
        "BLOCKQUOTE",
        "LAYOUT_TABLE",
        "STRUCTURE_BOUNDARY",
    }:
        return "HEADING_LIST_OR_LAYOUT"
    require(block_kind == "PROSE", f"unknown block kind cannot fall through to prose: {block_kind}")
    return "PROSE"


def build_raw_blocks(
    monolith: bytes,
    lines: list[dict[str, Any]],
    segments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    base = lexical_partition(lines)
    texts = _lexical_line_texts(lines)
    blocks: list[dict[str, Any]] = []
    for ordinal, item in enumerate(base, 1):
        start_line = item["start_line"]
        end_line = item["end_line"]
        segment = segment_for_line(segments, start_line)
        require(end_line <= segment["raw_end_line"], f"raw block crosses a proposed segment boundary: {ordinal}")
        start_byte = lines[start_line - 1]["byte_start"]
        end_byte = lines[end_line - 1]["byte_end"]
        payload = monolith[start_byte:end_byte]
        kind, container_kind = _block_kind_with_inline_math(
            item["base_kind"], texts, start_line, end_line
        )
        require(kind in BLOCK_KIND_ENUM, f"raw block kind is outside the frozen enum: {kind}")
        secondary_tags: list[str] = []
        if container_kind is not None:
            secondary_tags.append(f"CONTAINER_{container_kind}")
        if any("<sup>" in texts[number - 1] for number in range(start_line, end_line + 1)):
            secondary_tags.append("HAS_HTML_SUP")
        if item["base_kind"] == "STRUCTURE_BOUNDARY":
            secondary_tags.append("BLANK_RUN")
        blocks.append(
            {
                "block_kind": kind,
                "byte_size": len(payload),
                "canonical_document_id": segment["segment_id"],
                "canonical_path": segment["canonical_path"],
                "container_kind": container_kind,
                "end_byte_exclusive": end_byte,
                "end_line": end_line,
                "line_count": end_line - start_line + 1,
                "order": ordinal,
                "raw_block_id": f"RAW-{ordinal:06d}",
                "raw_sha256": sha256_bytes(payload),
                "risk_stratum": risk_stratum(segment["segment_id"], kind),
                "secondary_risk_tags": sorted(secondary_tags),
                "segment_id": segment["segment_id"],
                "start_byte": start_byte,
                "start_line": start_line,
                "terminal_lf": payload.endswith(b"\n"),
            }
        )
    require(len(blocks) == 20430, f"raw-block count drift: {len(blocks)}")
    require(sum(row["byte_size"] for row in blocks) == len(monolith), "raw-block byte conservation drift")
    require(blocks[0]["start_byte"] == 0 and blocks[-1]["end_byte_exclusive"] == len(monolith), "raw-block byte edges drift")
    for left, right in zip(blocks, blocks[1:]):
        require(left["end_byte_exclusive"] == right["start_byte"], "raw-block byte gap/overlap")
        require(left["end_line"] + 1 == right["start_line"], "raw-block line gap/overlap")
    expected_base = {
        "BLOCKQUOTE": 8,
        "CAPTION": 11,
        "CODE_BLOCK": 254,
        "HEADING": 286,
        "IMAGE_REFERENCE": 1444,
        "LAYOUT_TABLE": 45,
        "LIST_ITEM": 1624,
        "MATH_BLOCK": 135,
        "PROSE": 6780,
        "STRUCTURE_BOUNDARY": 9843,
    }
    require(dict(sorted(Counter(item["base_kind"] for item in base).items())) == expected_base, "base raw-block kind census drift")
    return blocks


def structure_ledger_rows(
    root: Path,
    contract: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    monolith = (root / LEGACY_RELATIVE / MONOLITH_RELATIVE).read_bytes()
    segments, lines = build_segments(monolith, contract)
    blocks = build_raw_blocks(monolith, lines, segments)
    rows: list[dict[str, Any]] = []
    for segment in segments:
        rows.append({"record_type": "SEGMENT", "schema_version": BASELINE_SCHEMA_VERSION, **segment})
    classifier_sha256 = sha256_file(Path(__file__).resolve())
    for block in blocks:
        rows.append(
            {
                "classifier_id": "ANKOS-RAW-LEXER-1",
                "classifier_source_sha256": classifier_sha256,
                "record_type": "RAW_BLOCK",
                "schema_version": BASELINE_SCHEMA_VERSION,
                **block,
            }
        )
    return rows, segments, blocks


def extract_image_references(payload: bytes) -> list[dict[str, Any]]:
    lines = split_raw_lines(payload)
    references: list[dict[str, Any]] = []
    for line in lines:
        text = line["content"].decode("utf-8", errors="strict")
        for match in IMAGE_PATTERN.finditer(text):
            target = match.group(1).strip()
            basename = PurePosixPath(target).name
            require(basename.endswith(".jpeg"), "image reference suffix drift")
            references.append(
                {
                    "basename": basename,
                    "line": line["line"],
                    "line_sha256": sha256_bytes(payload[line["byte_start"] : line["byte_end"]]),
                    "target": target,
                }
            )
    return references


def _block_for_line(blocks: list[dict[str, Any]], line: int) -> str:
    # There are only 20,430 blocks; a monotone index is unnecessary for this
    # small, frozen census and this direct search is intentionally independent.
    for block in blocks:
        if block["start_line"] <= line <= block["end_line"]:
            return block["raw_block_id"]
    raise GuardrailError(f"image/sentinel line has no raw block: {line}")


def build_image_reference_ledger(
    root: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    legacy = root / LEGACY_RELATIVE
    asset_rows = [row for row in manifest["raw_inputs"] if row["kind"] == "JPEG"]
    asset_by_basename = {row["basename"]: row for row in asset_rows}
    require(len(asset_by_basename) == len(asset_rows) == 1444, "asset basename map drift")
    split_by_basename: dict[str, list[dict[str, Any]]] = defaultdict(list)
    split_reference_count = 0
    for relative in ROUTING_MARKDOWN_PATHS:
        path = legacy / Path(*PurePosixPath(relative).parts)
        for reference in extract_image_references(path.read_bytes()):
            split_reference_count += 1
            candidate = path.parent / Path(*PurePosixPath(reference["target"]).parts)
            require(candidate.is_file() and not candidate.is_symlink(), f"split image target does not resolve: {relative}:{reference['line']}")
            resolved_relative = candidate.relative_to(legacy).as_posix()
            require(resolved_relative == asset_by_basename[reference["basename"]]["relative_path"], "split image target/basename join drift")
            split_by_basename[reference["basename"]].append(
                {
                    "line": reference["line"],
                    "line_sha256": reference["line_sha256"],
                    "path": relative,
                    "resolved_asset_path": resolved_relative,
                    "target": reference["target"],
                }
            )
    require(split_reference_count == 1441, "split image-reference count drift")
    require(len(split_by_basename) == 1441, "split image basenames are duplicated")
    monolith_path = legacy / MONOLITH_RELATIVE
    monolith_references = extract_image_references(monolith_path.read_bytes())
    require(len(monolith_references) == 1444, "monolith image-reference count drift")
    require(len({row["basename"] for row in monolith_references}) == 1444, "monolith image basenames are duplicated")
    rows: list[dict[str, Any]] = []
    for ordinal, reference in enumerate(monolith_references, 1):
        asset = asset_by_basename.get(reference["basename"])
        require(asset is not None, f"monolith image has no physical asset: {reference['basename']}")
        segment = segment_for_line(segments, reference["line"])
        direct = monolith_path.parent / Path(*PurePosixPath(reference["target"]).parts)
        split_references = sorted(
            split_by_basename.get(reference["basename"], []),
            key=lambda item: (item["path"], item["line"]),
        )
        require(len(split_references) <= 1, f"duplicate split image reference: {reference['basename']}")
        rows.append(
            {
                "asset_byte_size": asset["byte_size"],
                "asset_file_id": asset["file_id"],
                "asset_height": asset["image"]["height"],
                "asset_relative_path": asset["relative_path"],
                "asset_sha256": asset["sha256"],
                "asset_width": asset["image"]["width"],
                "basename": reference["basename"],
                "canonical_document_id": segment["segment_id"],
                "monolith_direct_target_resolves": direct.is_file(),
                "monolith_line": reference["line"],
                "monolith_line_sha256": reference["line_sha256"],
                "monolith_target": reference["target"],
                "raw_block_id": _block_for_line(blocks, reference["line"]),
                "raw_reference_ordinal": ordinal,
                "record_type": "IMAGE_REFERENCE",
                "schema_version": BASELINE_SCHEMA_VERSION,
                "split_references": split_references,
                "split_status": "PRESENT" if split_references else "OMITTED",
            }
        )
    require(not any(row["monolith_direct_target_resolves"] for row in rows), "a bare monolith image target unexpectedly resolves")
    omissions = [
        (row["raw_reference_ordinal"], row["monolith_line"], row["basename"])
        for row in rows
        if row["split_status"] == "OMITTED"
    ]
    require(
        omissions
        == [
            (24, 680, "_page_66_Picture_0.jpeg"),
            (134, 1711, "_page_154_Figure_2.jpeg"),
            (135, 1744, "_page_156_Figure_1.jpeg"),
        ],
        "split image omissions/ordinals drift",
    )
    require(Counter(row["canonical_document_id"] for row in rows) == Counter({
        "PREFACE": 2,
        "CH01": 2,
        "CH02": 20,
        "CH03": 85,
        "CH04": 60,
        "CH05": 76,
        "CH06": 100,
        "CH07": 92,
        "CH08": 43,
        "CH09": 109,
        "CH10": 68,
        "CH11": 107,
        "CH12": 58,
        "GENERAL_NOTES": 1,
        "N02": 54,
        "N03": 40,
        "N04": 71,
        "N05": 59,
        "N06": 64,
        "N07": 88,
        "N08": 32,
        "N09": 70,
        "N10": 91,
        "N11": 14,
        "N12": 38,
    }), "per-segment image-reference census drift")
    return rows


def _routing_span_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    input_by_path = {row["relative_path"]: row for row in manifest["raw_inputs"]}
    rows: list[dict[str, Any]] = []
    route_number = 1
    for path in ROUTING_MARKDOWN_PATHS:
        source = input_by_path[path]
        specs = ROUTING_SPAN_SPECS[path]
        require(specs[0][0] == 1 and specs[-1][1] == source["logical_line_count"], f"routing split-line edge drift: {path}")
        for left, right in zip(specs, specs[1:]):
            require(left[1] + 1 == right[0], f"routing split-line gap/overlap: {path}")
        for split_start, split_end, raw_start, raw_end, owner, disposition in specs:
            rows.append(
                {
                    "disposition": disposition,
                    "raw_end_line": raw_end,
                    "raw_start_line": raw_start,
                    "route_id": f"ROUTE-{route_number:03d}",
                    "source_path": path,
                    "source_sha256": source["sha256"],
                    "split_end_line": split_end,
                    "split_start_line": split_start,
                    "target_document_id": owner,
                }
            )
            route_number += 1
    require(len(rows) == 32, "routing disposition count drift")
    require(sum(row["raw_start_line"] is not None for row in rows) == 31, "raw routing span count drift")
    return rows


def build_routing_baseline(
    root: Path,
    manifest: dict[str, Any],
    image_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    input_by_path = {row["relative_path"]: row for row in manifest["raw_inputs"]}
    routes = _routing_span_rows(manifest)
    legacy = root / LEGACY_RELATIVE
    routing_files = []
    for path in ROUTING_MARKDOWN_PATHS:
        row = input_by_path[path]
        routing_files.append(
            {
                "byte_size": row["byte_size"],
                "image_reference_count": len(extract_image_references((legacy / path).read_bytes())),
                "logical_line_count": row["logical_line_count"],
                "path": path,
                "sha256": row["sha256"],
                "terminal_lf": row["text"]["terminal_lf"],
            }
        )
    atlas = input_by_path[ATLAS_RELATIVE]
    monolith = input_by_path[MONOLITH_RELATIVE]
    fence_counts = {
        row["relative_path"]: sum(
            1
            for line in split_raw_lines((legacy / row["relative_path"]).read_bytes())
            if re.match(rb"^ {0,3}(`{3,}|~{3,})", line["content"]) is not None
        )
        for row in manifest["raw_inputs"]
        if row["kind"] == "MARKDOWN"
    }
    omissions = [
        {
            "asset_sha256": row["asset_sha256"],
            "basename": row["basename"],
            "canonical_document_id": row["canonical_document_id"],
            "monolith_line": row["monolith_line"],
            "raw_reference_ordinal": row["raw_reference_ordinal"],
        }
        for row in image_rows
        if row["split_status"] == "OMITTED"
    ]
    return {
        "atlas": {
            "byte_size": atlas["byte_size"],
            "image_reference_count": 0,
            "logical_line_count": atlas["logical_line_count"],
            "path": ATLAS_RELATIVE,
            "role": "INTERPRETIVE_METADATA",
            "sha256": atlas["sha256"],
            "terminal_lf": atlas["text"]["terminal_lf"],
            "textual_witness_allowed": False,
        },
        "consumer_compatibility_baseline": "goal-4/compatibility-baseline.json",
        "fence_delimiters": {
            "all_markdown_count": sum(fence_counts.values()),
            "by_path": dict(sorted(fence_counts.items())),
            "monolith_count": fence_counts[MONOLITH_RELATIVE],
        },
        "image_references": {
            "all_monolith_targets_broken_relative_to_monolith": True,
            "ledger_path": "goal-4/image-reference-ledger.jsonl",
            "monolith_count": len(image_rows),
            "monolith_source_sha256": monolith["sha256"],
            "split_count": sum(row["image_reference_count"] for row in routing_files),
            "split_omissions": omissions,
        },
        "nonrouting_link_shapes": {
            "monolith_lines": [15347, 16774, 17356, 18922, 20385],
            "status": "FORMULA_OR_CODE_TEXT_NOT_NAVIGATION",
        },
        "omitted_transition_or_malformed_raw_lines": [
            {"lines": [398, 399], "reason": "PRINTED_TRANSITION_FURNITURE_NOT_IN_SPLITS"},
            {"lines": [1368, 1369], "reason": "PRINTED_TRANSITION_FURNITURE_NOT_IN_SPLITS"},
            {"lines": [2700, 2701], "reason": "PRINTED_TRANSITION_FURNITURE_NOT_IN_SPLITS"},
            {"lines": [6586, 6587], "reason": "PRINTED_TRANSITION_FURNITURE_NOT_IN_SPLITS"},
            {"lines": [12083, 12084], "reason": "MALFORMED_EMPTY_HEADING_AND_BLANK_OMITTED"},
            {"lines": [12086, 12088], "reason": "MALFORMED_BLANK_OR_EMPTY_HEADING_RUN_OMITTED"},
            {"lines": [17443, 17443], "reason": "BLANK_AT_NOMINAL_FILE_SEAM_OMITTED"},
        ],
        "routing_files": routing_files,
        "routing_spans": routes,
        "schema_version": BASELINE_SCHEMA_VERSION,
        "textual_evidence_limit": "CORRELATED_DERIVATIVES_FOR_ROUTING_ONLY_NOT_TRANSCRIPTION_PROOF",
    }


def _rank_sha256(seed_hex: str, document_id: str, stratum: str, raw_block_id: str) -> str:
    payload = (
        bytes.fromhex(seed_hex)
        + b"\0"
        + document_id.encode("utf-8")
        + b"\0"
        + stratum.encode("utf-8")
        + b"\0"
        + raw_block_id.encode("utf-8")
    )
    return sha256_bytes(payload)


def _hamilton_allocation(populations: dict[str, int], quota: int) -> dict[str, int]:
    require(set(populations) == set(RISK_PRIORITY), "risk population enum drift")
    total = sum(populations.values())
    require(0 <= quota <= total, "document quota is outside its population")
    allocation = {stratum: 0 for stratum in RISK_PRIORITY}
    slots = quota
    for stratum in RISK_PRIORITY:
        if stratum != "PROSE" and populations[stratum] > 0 and slots > 0:
            allocation[stratum] = 1
            slots -= 1
    if slots == 0:
        return allocation
    capacities = {
        stratum: populations[stratum] - allocation[stratum]
        for stratum in RISK_PRIORITY
    }
    capacity_total = sum(capacities.values())
    require(capacity_total >= slots > 0, "Hamilton residual capacity drift")
    floors: dict[str, int] = {}
    remainders: dict[str, int] = {}
    for stratum in RISK_PRIORITY:
        numerator = slots * capacities[stratum]
        floors[stratum], remainders[stratum] = divmod(numerator, capacity_total)
        allocation[stratum] += floors[stratum]
    remaining = quota - sum(allocation.values())
    order = sorted(
        RISK_PRIORITY,
        key=lambda stratum: (
            -remainders[stratum],
            RISK_PRIORITY.index(stratum),
            stratum,
        ),
    )
    for stratum in order[:remaining]:
        allocation[stratum] += 1
    require(sum(allocation.values()) == quota, "Hamilton allocation does not sum to quota")
    for stratum in RISK_PRIORITY:
        require(allocation[stratum] <= populations[stratum], "Hamilton allocation exceeds population")
    return allocation


def build_held_out_sample(
    root: Path,
    manifest: dict[str, Any],
    structure_rows: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    contract: dict[str, Any],
    quality: dict[str, Any],
) -> dict[str, Any]:
    material = quality_manifest_material(manifest["raw_inputs"])
    domain = bytes.fromhex(quality["seed"]["domain_separator_hex"])
    seed = sha256_bytes(domain + material)
    require(seed == "edb7d55b015326755574afbf5513e2bacefe04fbdad875fb8901555edf8e5f0d", "held-out seed drift")
    known = quality["seed"]["known_vector"]
    require(
        sha256_bytes(domain + bytes.fromhex(known["manifest_material_utf8_hex"]))
        == known["seed_sha256"],
        "quality seed known vector fails during materialization",
    )
    require(
        _rank_sha256(
            known["seed_sha256"],
            known["rank_canonical_document_id"],
            known["rank_risk_stratum"],
            known["rank_raw_block_id"],
        )
        == known["rank_sha256"],
        "quality rank known vector fails during materialization",
    )
    document_order = [row["id"] for row in contract["canonical_documents"]]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for block in blocks:
        rank = _rank_sha256(
            seed,
            block["canonical_document_id"],
            block["risk_stratum"],
            block["raw_block_id"],
        )
        grouped[(block["canonical_document_id"], block["risk_stratum"])].append(
            {"rank_sha256": rank, "raw_block_id": block["raw_block_id"]}
        )
    allocations: list[dict[str, Any]] = []
    selected: set[str] = set()
    selected_ordered: list[str] = []
    for document_id in document_order:
        populations = {
            stratum: len(grouped[(document_id, stratum)])
            for stratum in RISK_PRIORITY
        }
        population = sum(populations.values())
        require(population > 0, f"canonical document has no raw blocks: {document_id}")
        quota = min(population, max((population + 19) // 20, 20))
        allocation = _hamilton_allocation(populations, quota)
        allocations.append(
            {
                "allocations": allocation,
                "canonical_document_id": document_id,
                "population": population,
                "populations": populations,
                "quota": quota,
            }
        )
        for stratum in RISK_PRIORITY:
            ranked = sorted(
                grouped[(document_id, stratum)],
                key=lambda item: (int(item["rank_sha256"], 16), item["raw_block_id"]),
            )
            chosen = ranked[: allocation[stratum]]
            for item in chosen:
                require(item["raw_block_id"] not in selected, "held-out block selected twice")
                selected.add(item["raw_block_id"])
                selected_ordered.append(item["raw_block_id"])
    rankings: list[dict[str, Any]] = []
    for document_id in document_order:
        for stratum in RISK_PRIORITY:
            ranked = sorted(
                grouped[(document_id, stratum)],
                key=lambda item: (int(item["rank_sha256"], 16), item["raw_block_id"]),
            )
            for position, item in enumerate(ranked, 1):
                rankings.append(
                    {
                        "canonical_document_id": document_id,
                        "position_in_stratum": position,
                        "rank_sha256": item["rank_sha256"],
                        "raw_block_id": item["raw_block_id"],
                        "risk_stratum": stratum,
                        "selected": item["raw_block_id"] in selected,
                    }
                )
    require(len(rankings) == len(blocks) == 20430, "held-out ranking coverage drift")
    require(len(selected) == len(selected_ordered) == 1125, "held-out selected count drift")
    require(sum(row["quota"] for row in allocations) == 1125, "held-out document quota total drift")
    structure_bytes = jsonl_bytes(structure_rows)
    selection_bytes = stable_json_bytes(selected_ordered, terminal_lf=False)
    return {
        "bindings": {
            "guardrails_sha256": sha256_file(root / "goal-4/guardrails.json"),
            "manifest_material_sha256": sha256_bytes(material),
            "quality_protocol_sha256": sha256_file(root / "goal-4/quality-evaluation.json"),
            "raw_manifest_sha256": sha256_bytes(canonical_json_bytes(manifest)),
            "structure_ledger_sha256": sha256_bytes(structure_bytes),
        },
        "classifier": {
            "block_kind_enum": list(BLOCK_KIND_ENUM),
            "classifier_id": "ANKOS-RAW-LEXER-1",
            "inline_math_policy": "MATCH_VALID_LEXICAL_PAIR_INDEPENDENTLY_WITHIN_ONE_PHYSICAL_LINE",
            "source_path": "goal-4/tools/baseline_lib.py",
            "source_sha256": sha256_file(Path(__file__).resolve()),
        },
        "document_allocations": allocations,
        "manifest_material": {
            "byte_size": len(material),
            "path_base": LEGACY_RELATIVE,
            "sha256": sha256_bytes(material),
        },
        "protocol_version": quality["protocol_version"],
        "rankings": rankings,
        "risk_priority": list(RISK_PRIORITY),
        "schema_version": BASELINE_SCHEMA_VERSION,
        "seed_sha256": seed,
        "selected_count": len(selected_ordered),
        "selected_raw_block_ids": selected_ordered,
        "selected_raw_block_ids_sha256": sha256_bytes(selection_bytes),
        "selection_inputs": [
            "raw manifest five-field projection",
            "raw syntax classifier",
            "canonical document assignment",
            "risk stratum",
            "raw block ID",
        ],
        "selection_prohibited_inputs": [
            "detector output",
            "known-defect status",
            "witness answer",
            "repair proposal",
            "repair outcome",
            "CHANGED_OR_UNCHANGED_LABEL",
        ],
        "status": "MATERIALIZED_AND_FROZEN_BEFORE_AUTHOR_TEXT_REPAIR",
    }


def _content_stage_for_document(document_id: str) -> str:
    if document_id in {"PUBLICATION_AND_CONTENTS", "PREFACE", "COLOPHON"}:
        return "8-BOOKENDS"
    if re.fullmatch(r"CH\d{2}", document_id):
        return f"{8 + int(document_id[2:]):d}-{document_id}"
    if document_id == "GENERAL_NOTES":
        return "21-GENERAL-NOTES"
    if re.fullmatch(r"N\d{2}", document_id):
        return f"{21 + int(document_id[1:]):d}-{document_id}"
    if document_id == "INDEX":
        return "34-36-INDEX"
    if document_id in {"INTERPRETIVE_METADATA", "GENERATED_METADATA"}:
        return "39-NAVIGATION"
    raise GuardrailError(f"unknown defect owner document: {document_id}")


def _specialist_stages(defect_classes: list[str]) -> list[str]:
    stages: set[str] = set()
    if set(defect_classes) & {"FORMULA_OR_SYMBOL", "WOLFRAM_CODE", "RULE_TABLE_OR_DATA"}:
        stages.add("37-MATH-CODE")
    if "FIGURE_OR_CAPTION" in defect_classes:
        stages.add("38-FIGURES")
    if set(defect_classes) & {"STRUCTURE_BOUNDARY", "MARKDOWN_STRUCTURE", "HEADING_OR_FURNITURE", "NAVIGATION_METADATA"}:
        stages.add("39-NAVIGATION")
    if "INDEX_ENTRY" in defect_classes:
        stages.update({"34-INDEX-AF", "35-INDEX-GM", "36-INDEX-NZ"})
    return sorted(stages)


def _defect_span_specs() -> list[dict[str, Any]]:
    monolith = MONOLITH_RELATIVE
    ch12 = "CHAPTERS/12-The-Principle-of-Computational-Equivalence/The-Principle-of-Computational-Equivalence.md"
    nominal_notes = "BACK-MATTER/Notes/Notes.md"
    nominal_index = "BACK-MATTER/Index/Index.md"
    nominal_colophon = "BACK-MATTER/Colophon/Colophon.md"
    specs: list[dict[str, Any]] = [
        {"label": "CH12_SPLIT_CROSSES_GENERAL_NOTES", "path": ch12, "start": 2004, "end": 2004, "owner": "GENERAL_NOTES", "classes": ["STRUCTURE_BOUNDARY"], "detectors": ["D04_SPLIT_ROUTING"]},
        {"label": "NOMINAL_NOTES_IS_ONE_STRAY_N03_LINE", "path": nominal_notes, "start": 1, "end": 1, "owner": "N03", "classes": ["STRUCTURE_BOUNDARY"], "detectors": ["D04_SPLIT_ROUTING"]},
        {"label": "NOMINAL_INDEX_STARTS_IN_N03_NOT_INDEX", "path": nominal_index, "start": 1, "end": 1, "owner": "N03", "classes": ["STRUCTURE_BOUNDARY"], "detectors": ["D04_SPLIT_ROUTING"]},
        {"label": "NOMINAL_COLOPHON_STARTS_IN_N10_NOT_COLOPHON", "path": nominal_colophon, "start": 1, "end": 1, "owner": "N10", "classes": ["STRUCTURE_BOUNDARY", "HEADING_OR_FURNITURE"], "detectors": ["D04_SPLIT_ROUTING", "D07_HEADING"]},
        {"label": "ACTUAL_INDEX_INSIDE_NOMINAL_COLOPHON", "path": nominal_colophon, "start": 3383, "end": 3383, "owner": "INDEX", "classes": ["STRUCTURE_BOUNDARY", "INDEX_ENTRY"], "detectors": ["D04_SPLIT_ROUTING", "D12_INDEX"]},
        {"label": "ACTUAL_COLOPHON_AT_NOMINAL_COLOPHON_TAIL", "path": nominal_colophon, "start": 5015, "end": 5015, "owner": "COLOPHON", "classes": ["STRUCTURE_BOUNDARY"], "detectors": ["D04_SPLIT_ROUTING"]},
        {"label": "SPLIT_IMAGE_OMISSION_PAGE_66", "path": monolith, "start": 680, "end": 680, "classes": ["FIGURE_OR_CAPTION", "NAVIGATION_METADATA"], "detectors": ["D05_IMAGE_REFERENCE"]},
        {"label": "SPLIT_IMAGE_OMISSION_PAGE_154", "path": monolith, "start": 1711, "end": 1711, "classes": ["FIGURE_OR_CAPTION", "NAVIGATION_METADATA"], "detectors": ["D05_IMAGE_REFERENCE"]},
        {"label": "SPLIT_IMAGE_OMISSION_PAGE_156", "path": monolith, "start": 1744, "end": 1744, "classes": ["FIGURE_OR_CAPTION", "NAVIGATION_METADATA"], "detectors": ["D05_IMAGE_REFERENCE"]},
        {"label": "CAPTION_PROSE_INTERLEAVING", "path": monolith, "start": 2130, "end": 2132, "classes": ["FIGURE_OR_CAPTION", "PROSE_OCR"], "detectors": ["D08_CAPTION_ASSOCIATION"]},
        {"label": "PROSE_MATH_SPLIT", "path": monolith, "start": 12891, "end": 12893, "classes": ["PROSE_OCR", "FORMULA_OR_SYMBOL"], "detectors": ["D09_WORD_BOUNDARY", "D10_TECHNICAL"]},
        {"label": "PROSE_ACCIDENTALLY_FENCED_AND_HYPHEN_SPLIT", "path": monolith, "start": 16433, "end": 16438, "classes": ["MARKDOWN_STRUCTURE", "PROSE_OCR", "WOLFRAM_CODE"], "detectors": ["D06_FENCE", "D09_WORD_BOUNDARY"]},
    ]
    for line in (12083, 12087, 18328, 18810):
        specs.append({"label": f"EMPTY_HEADING_LINE_{line}", "path": monolith, "start": line, "end": line, "classes": ["HEADING_OR_FURNITURE"], "detectors": ["D07_HEADING"]})
    for line in (398, 412, 696, 1368, 1752, 2338, 2360, 2700, 2840, 3952, 6586, 10031, 17444):
        specs.append({"label": f"PAGE_FURNITURE_OR_FALSE_HEADING_LINE_{line}", "path": monolith, "start": line, "end": line, "classes": ["HEADING_OR_FURNITURE"], "detectors": ["D07_HEADING"]})
    specs.extend(
        [
            {"label": "CORRUPTED_BOOLEAN_RULE_FORMULAS", "path": monolith, "start": 11711, "end": 11841, "classes": ["FORMULA_OR_SYMBOL", "RULE_TABLE_OR_DATA"], "detectors": ["D10_TECHNICAL"]},
            {"label": "TRUNCATED_PROGRAM_MATERIAL_LINE_12377", "path": monolith, "start": 12377, "end": 12377, "classes": ["WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL"]},
            {"label": "MANGLED_MAXIMA_MATERIAL_LINE_12382", "path": monolith, "start": 12382, "end": 12382, "classes": ["FORMULA_OR_SYMBOL", "WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL"]},
            {"label": "TRUNCATED_PDE_MATERIAL_LINE_13453", "path": monolith, "start": 13453, "end": 13453, "classes": ["FORMULA_OR_SYMBOL"], "detectors": ["D10_TECHNICAL"]},
            {"label": "DAMAGED_WOLFRAM_DEFINITION_LINE_17301", "path": monolith, "start": 17301, "end": 17301, "classes": ["WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL"]},
            {"label": "DAMAGED_WOLFRAM_DEFINITION_LINE_17442", "path": monolith, "start": 17442, "end": 17442, "classes": ["WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL"]},
            {"label": "DAMAGED_MATH_DELIMITERS_LINE_19567", "path": monolith, "start": 19567, "end": 19567, "classes": ["FORMULA_OR_SYMBOL", "MARKDOWN_STRUCTURE"], "detectors": ["D10_TECHNICAL"]},
            {"label": "SEVERE_INDEX_COLUMN_FLATTENING_LINE_21877", "path": monolith, "start": 21877, "end": 21877, "classes": ["INDEX_ENTRY", "STRUCTURE_BOUNDARY"], "detectors": ["D12_INDEX"]},
        ]
    )
    for line in (10631, 12079, 13294, 14031, 16429, 17273, 17793, 20109):
        specs.append({"label": f"JOINED_OR_SPLIT_WORD_CANDIDATE_LINE_{line}", "path": monolith, "start": line, "end": line, "classes": ["PROSE_OCR"], "detectors": ["D09_WORD_BOUNDARY"]})
    specs.extend(
        [
            {"label": "REPEATED_OR_TRUNCATED_PHRASE_LINE_1740", "path": monolith, "start": 1740, "end": 1740, "classes": ["PROSE_OCR"], "detectors": ["D11_REPETITION"]},
            {"label": "ZERO_DATA_FALSE_HEADING_LINE_12348", "path": monolith, "start": 12348, "end": 12348, "classes": ["HEADING_OR_FURNITURE", "RULE_TABLE_OR_DATA"], "detectors": ["D07_HEADING", "D10_TECHNICAL"]},
            {"label": "OCR_CONFUSION_OUANTUM_LINE_16946", "path": monolith, "start": 16946, "end": 16946, "classes": ["PROSE_OCR", "FORMULA_OR_SYMBOL"], "detectors": ["D09_WORD_BOUNDARY", "D10_TECHNICAL"]},
            {"label": "PROSE_PROMOTED_TO_HEADING_LINE_17259", "path": monolith, "start": 17259, "end": 17259, "classes": ["HEADING_OR_FURNITURE", "PROSE_OCR"], "detectors": ["D07_HEADING"]},
            {"label": "REPEATED_CORRUPTED_RULE_BODY_A", "path": monolith, "start": 18231, "end": 18235, "classes": ["RULE_TABLE_OR_DATA", "WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL", "D11_REPETITION"]},
            {"label": "REPEATED_CORRUPTED_RULE_BODY_B", "path": monolith, "start": 18237, "end": 18241, "classes": ["RULE_TABLE_OR_DATA", "WOLFRAM_CODE"], "detectors": ["D10_TECHNICAL", "D11_REPETITION"]},
            {"label": "INDEX_OPENING_COLUMN_INTERLEAVE", "path": monolith, "start": 20828, "end": 20834, "classes": ["INDEX_ENTRY", "STRUCTURE_BOUNDARY"], "detectors": ["D12_INDEX"]},
        ]
    )
    return specs


def build_known_defect_rows(
    root: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    image_rows: list[dict[str, Any]],
    routing: dict[str, Any],
) -> list[dict[str, Any]]:
    legacy = root / LEGACY_RELATIVE
    input_by_path = {row["relative_path"]: row for row in manifest["raw_inputs"]}
    image_by_line = {row["monolith_line"]: row for row in image_rows}
    rows: list[dict[str, Any]] = []
    for spec in _defect_span_specs():
        source = input_by_path[spec["path"]]
        payload = (legacy / spec["path"]).read_bytes()
        lines = split_raw_lines(payload)
        require(1 <= spec["start"] <= spec["end"] <= len(lines), f"defect span is out of range: {spec['label']}")
        start_byte = lines[spec["start"] - 1]["byte_start"]
        end_byte = lines[spec["end"] - 1]["byte_end"]
        span = payload[start_byte:end_byte]
        owner = spec.get("owner")
        raw_block_ids: list[str] = []
        if spec["path"] == MONOLITH_RELATIVE:
            owner = segment_for_line(segments, spec["start"])["segment_id"]
            require(segment_for_line(segments, spec["end"])["segment_id"] == owner, f"defect span crosses documents: {spec['label']}")
            raw_block_ids = [
                block["raw_block_id"]
                for block in blocks
                if block["start_line"] <= spec["end"] and block["end_line"] >= spec["start"]
            ]
            require(raw_block_ids, f"defect span has no raw blocks: {spec['label']}")
        require(owner is not None, f"defect owner is missing: {spec['label']}")
        start_text = lines[spec["start"] - 1]["content"].decode("utf-8")
        end_text = lines[spec["end"] - 1]["content"].decode("utf-8")
        row: dict[str, Any] = {
            "closure_stages": ["40-SATURATION", "42-RELEASE"],
            "defect_classes": sorted(spec["classes"]),
            "expected_detector_classes": sorted(set(spec["detectors"] + ["D13_EXACT_SENTINEL"])),
            "label": spec["label"],
            "owner_document_id": owner,
            "primary_content_stage": _content_stage_for_document(owner),
            "raw_block_ids": raw_block_ids,
            "raw_end_line": spec["end"],
            "raw_source_role": source["role"],
            "raw_source_sha256": source["sha256"],
            "raw_span_byte_size": len(span),
            "raw_span_occurrence_count": payload.count(span),
            "raw_span_sha256": sha256_bytes(span),
            "raw_start_line": spec["start"],
            "repair_authorized": False,
            "sentinel_kind": "EXACT_RAW_SPAN",
            "source_path": spec["path"],
            "specialist_stages": _specialist_stages(spec["classes"]),
            "start_line_prefix": start_text[:160],
            "start_line_suffix": start_text[-160:],
            "end_line_prefix": end_text[:160],
            "end_line_suffix": end_text[-160:],
            "status": "BASELINE_OPEN_SOURCE_NEEDED",
        }
        if spec["start"] in image_by_line and "FIGURE_OR_CAPTION" in spec["classes"]:
            image = image_by_line[spec["start"]]
            row["image_reference"] = {
                "basename": image["basename"],
                "raw_reference_ordinal": image["raw_reference_ordinal"],
                "split_status": image["split_status"],
            }
        rows.append(row)
    aggregate_rows = [
        {
            "artifact_path": ATLAS_RELATIVE,
            "artifact_sha256": input_by_path[ATLAS_RELATIVE]["sha256"],
            "defect_classes": ["NAVIGATION_METADATA"],
            "expected_detector_classes": ["D04_SPLIT_ROUTING", "D13_EXACT_SENTINEL"],
            "label": "ATLAS_MUST_REMAIN_INTERPRETIVE_METADATA",
            "owner_document_id": "INTERPRETIVE_METADATA",
            "primary_content_stage": "39-NAVIGATION",
            "repair_authorized": False,
            "sentinel_kind": "AGGREGATE_GUARDRAIL",
            "specialist_stages": ["39-NAVIGATION"],
            "status": "BASELINE_ROLE_GUARDRAIL",
        },
        {
            "artifact_path": "goal-4/image-reference-ledger.jsonl",
            "artifact_sha256": sha256_bytes(jsonl_bytes(image_rows)),
            "defect_classes": ["NAVIGATION_METADATA", "FIGURE_OR_CAPTION"],
            "expected_detector_classes": ["D05_IMAGE_REFERENCE", "D13_EXACT_SENTINEL"],
            "label": "ALL_1444_MONOLITH_IMAGE_TARGETS_BROKEN_RELATIVE_TO_MONOLITH",
            "owner_document_id": "GENERATED_METADATA",
            "primary_content_stage": "6-MEDIA",
            "repair_authorized": False,
            "sentinel_kind": "AGGREGATE_GUARDRAIL",
            "specialist_stages": ["38-FIGURES", "39-NAVIGATION"],
            "status": "BASELINE_MECHANICAL_ROUTE_OPEN",
        },
        {
            "artifact_path": "goal-4/routing-baseline.json",
            "artifact_sha256": sha256_bytes(canonical_json_bytes(routing)),
            "defect_classes": ["NAVIGATION_METADATA", "STRUCTURE_BOUNDARY"],
            "expected_detector_classes": ["D04_SPLIT_ROUTING", "D13_EXACT_SENTINEL"],
            "label": "CONTENTS_LINKS_RESOLVE_LEXICALLY_BUT_FOUR_SEMANTIC_DESTINATIONS_ARE_MALFORMED",
            "owner_document_id": "GENERATED_METADATA",
            "primary_content_stage": "39-NAVIGATION",
            "repair_authorized": False,
            "sentinel_kind": "AGGREGATE_GUARDRAIL",
            "specialist_stages": ["39-NAVIGATION"],
            "status": "BASELINE_MECHANICAL_ROUTE_OPEN",
        },
    ]
    rows.extend(aggregate_rows)
    for number, row in enumerate(rows, 1):
        row["schema_version"] = BASELINE_SCHEMA_VERSION
        row["sentinel_id"] = f"DEFECT-{number:04d}"
        row.setdefault("closure_stages", ["40-SATURATION", "42-RELEASE"])
        row.setdefault("raw_block_ids", [])
    require(len(rows) == 55, f"known-defect regression row count drift: {len(rows)}")
    require(len({row["sentinel_id"] for row in rows}) == len(rows), "duplicate defect sentinel ID")
    require(all(row["repair_authorized"] is False for row in rows), "baseline defect row authorizes repair")
    return rows


def build_detector_artifacts(
    root: Path,
    manifest: dict[str, Any],
    segments: list[dict[str, Any]],
    blocks: list[dict[str, Any]],
    image_rows: list[dict[str, Any]],
    routing: dict[str, Any],
    defect_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    legacy = root / LEGACY_RELATIVE
    monolith = (legacy / MONOLITH_RELATIVE).read_bytes()
    lines = split_raw_lines(monolith)
    hits: list[dict[str, Any]] = []

    def add_hit(
        detector_id: str,
        source_path: str,
        start_line: int | None,
        end_line: int | None,
        route: str,
        fingerprint: str,
        raw_block_ids: list[str] | None = None,
    ) -> None:
        hits.append(
            {
                "detector_id": detector_id,
                "end_line": end_line,
                "fingerprint_sha256": fingerprint,
                "raw_block_ids": raw_block_ids or [],
                "repair_authorized": False,
                "route": route,
                "schema_version": BASELINE_SCHEMA_VERSION,
                "source_path": source_path,
                "start_line": start_line,
            }
        )

    for row in routing["routing_spans"]:
        if row["disposition"] not in {"REFLOWED_OR_NORMALIZED_ROUTING_ONLY"}:
            add_hit(
                "D04_SPLIT_ROUTING",
                row["source_path"],
                row["split_start_line"],
                row["split_end_line"],
                row["disposition"],
                sha256_bytes(stable_json_bytes(row, terminal_lf=False)),
            )
    for row in image_rows:
        add_hit(
            "D05_IMAGE_REFERENCE",
            MONOLITH_RELATIVE,
            row["monolith_line"],
            row["monolith_line"],
            "BROKEN_MONOLITH_RELATIVE_TARGET",
            row["monolith_line_sha256"],
            [row["raw_block_id"]],
        )
        if row["split_status"] == "OMITTED":
            add_hit(
                "D05_IMAGE_REFERENCE",
                MONOLITH_RELATIVE,
                row["monolith_line"],
                row["monolith_line"],
                "SPLIT_REFERENCE_OMISSION",
                sha256_bytes(
                    stable_json_bytes(
                        {
                            "basename": row["basename"],
                            "ordinal": row["raw_reference_ordinal"],
                            "line": row["monolith_line"],
                        },
                        terminal_lf=False,
                    )
                ),
                [row["raw_block_id"]],
            )
    for line in lines:
        text = line["content"].decode("utf-8")
        heading = LEX_ATX.match(text)
        if heading is not None:
            body = re.sub(r"^ {0,3}#{1,6}\s*", "", text).strip().strip("*").strip()
            suspicious = (
                not body
                or re.fullmatch(r"[0-9]+", body) is not None
                or re.fullmatch(r"[-–—]+", body) is not None
                or "STEPHEN WOLFRAM" in body.upper()
                or body == "In n dimensions, it can be done using"
            )
            if suspicious:
                add_hit(
                    "D07_HEADING",
                    MONOLITH_RELATIVE,
                    line["line"],
                    line["line"],
                    "HEADING_OR_PAGE_FURNITURE_REVIEW",
                    sha256_bytes(monolith[line["byte_start"] : line["byte_end"]]),
                    [_block_for_line(blocks, line["line"])],
                )
        unescaped_dollars = len(re.findall(r"(?<!\\)\$", text))
        if unescaped_dollars % 2 == 1:
            add_hit(
                "D10_TECHNICAL",
                MONOLITH_RELATIVE,
                line["line"],
                line["line"],
                "ODD_UNESCAPED_DOLLAR_COUNT_REVIEW",
                sha256_bytes(monolith[line["byte_start"] : line["byte_end"]]),
                [_block_for_line(blocks, line["line"])],
            )
    index_segment = next(row for row in segments if row["segment_id"] == "INDEX")
    for number in range(index_segment["raw_start_line"], index_segment["raw_end_line"] + 1):
        line = lines[number - 1]
        text = line["content"].decode("utf-8")
        if len(line["content"]) > 1000 or "Ouantum" in text:
            add_hit(
                "D12_INDEX",
                MONOLITH_RELATIVE,
                number,
                number,
                "INDEX_COLUMN_OR_OCR_REVIEW",
                sha256_bytes(monolith[line["byte_start"] : line["byte_end"]]),
                [_block_for_line(blocks, number)],
            )
    for row in defect_rows:
        add_hit(
            "D13_EXACT_SENTINEL",
            row.get("source_path", row.get("artifact_path", "")),
            row.get("raw_start_line"),
            row.get("raw_end_line"),
            row["sentinel_id"],
            row.get("raw_span_sha256", row.get("artifact_sha256", "")),
            row.get("raw_block_ids", []),
        )
    hits.sort(
        key=lambda row: (
            row["detector_id"],
            row["source_path"],
            -1 if row["start_line"] is None else row["start_line"],
            row["route"],
            row["fingerprint_sha256"],
        )
    )
    for number, row in enumerate(hits, 1):
        row["hit_id"] = f"HIT-{number:06d}"
    generic_by_location: dict[tuple[str, int | None], set[str]] = defaultdict(set)
    for hit in hits:
        if hit["detector_id"] != "D13_EXACT_SENTINEL":
            generic_by_location[(hit["source_path"], hit["start_line"])].add(hit["detector_id"])
    known_routes = []
    for row in defect_rows:
        source = row.get("source_path", row.get("artifact_path", ""))
        generic = sorted(generic_by_location[(source, row.get("raw_start_line"))])
        known_routes.append(
            {
                "generic_detector_ids": generic,
                "route_kind": "GENERIC_DETECTOR_PLUS_EXACT_REGRESSION" if generic else "EXACT_REGRESSION_MANUAL_ROUTE",
                "sentinel_id": row["sentinel_id"],
            }
        )
    detector_descriptions = {
        "D01_RAW_MANIFEST": "Exact type/path/hash/mode/Git/LFS/image-dimension census; failures are fatal rather than candidate hits.",
        "D02_TEXT_PROFILE": "Strict UTF-8/LF/final-LF/logical-line-map census; failures are fatal.",
        "D03_STRUCTURE": "Unique boundary signatures and gap/overlap/order/byte conservation checks; failures are fatal.",
        "D04_SPLIT_ROUTING": "Routing ownership and malformed derivative seam diagnostics only.",
        "D05_IMAGE_REFERENCE": "Image ordinal, target resolution, basename, physical join, and split omission diagnostics.",
        "D06_FENCE": "Fence-aware raw-block balance and code/prose candidate routing; never authorizes a text change.",
        "D07_HEADING": "Empty, numeric, punctuation, running-header, data, and prose-heading lexical candidates.",
        "D08_CAPTION_ASSOCIATION": "Figure/caption adjacency and interleaving candidates requiring full-page evidence.",
        "D09_WORD_BOUNDARY": "Joined/split/hyphen/orphan-continuation candidates requiring source review.",
        "D10_TECHNICAL": "Math/code delimiter, bracket, token, truncation, and rule-table candidates.",
        "D11_REPETITION": "Repeated n-gram and abnormal expansion candidates.",
        "D12_INDEX": "Index line-length, density, column-order, and OCR-confusable candidates.",
        "D13_EXACT_SENTINEL": "Exact pre-repair regression presence/route check; not a discovery detector.",
    }
    hit_counts = Counter(row["detector_id"] for row in hits)
    families = [
        {
            "description": description,
            "detector_id": detector_id,
            "hit_count": hit_counts[detector_id],
            "writes_author_text": False,
        }
        for detector_id, description in detector_descriptions.items()
    ]
    report = {
        "baseline_only": True,
        "detector_families": families,
        "hit_count": len(hits),
        "hits_path": "goal-4/baseline-detector-hits.jsonl",
        "known_defect_registry": {
            "exact_presence_count": len(defect_rows),
            "exact_presence_denominator": len(defect_rows),
            "generic_detector_plus_exact_count": sum(bool(row["generic_detector_ids"]) for row in known_routes),
            "registry_path": "goal-4/known-defect-regression.jsonl",
            "registry_sha256": sha256_bytes(jsonl_bytes(defect_rows)),
            "routes": known_routes,
            "unrouted_count": 0,
        },
        "measurements": {
            "all_markdown_fence_delimiter_count": routing["fence_delimiters"]["all_markdown_count"],
            "monolith_fence_delimiter_count": routing["fence_delimiters"]["monolith_count"],
            "monolith_image_reference_count": len(image_rows),
            "raw_block_count": len(blocks),
            "segment_count": len(segments),
            "split_image_reference_count": routing["image_references"]["split_count"],
        },
        "repairs_applied": 0,
        "schema_version": BASELINE_SCHEMA_VERSION,
        "status": "PRE_REPAIR_DIAGNOSTIC_BASELINE",
    }
    require(report["known_defect_registry"]["unrouted_count"] == 0, "known defect lacks a baseline route")
    return hits, report


def _command_version(root: Path, argv: list[str]) -> str:
    result = subprocess.run(
        argv,
        cwd=root,
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    require(result.returncode == 0, f"version command failed: {' '.join(argv)}")
    return result.stdout.decode("utf-8", errors="strict").strip()


def build_environment_snapshot(
    root: Path,
    manifest: dict[str, Any],
    status_before: bytes,
    status_after: bytes,
    head_before: str,
    head_after: str,
) -> dict[str, Any]:
    old_umask = os.umask(0)
    os.umask(old_umask)
    return {
        "capture_scope": {
            "git_head_after": head_after,
            "git_head_before": head_before,
            "git_head_stable_during_capture": head_before == head_after,
            "git_status_after_sha256": sha256_bytes(status_after),
            "git_status_after_utf8": status_after.decode("utf-8", errors="strict").splitlines(),
            "git_status_before_sha256": sha256_bytes(status_before),
            "git_status_before_utf8": status_before.decode("utf-8", errors="strict").splitlines(),
            "legacy_git_tree": manifest["git"]["legacy_tree_oid"],
            "legacy_manifest_rows_sha256": sha256_bytes(canonical_json_bytes(manifest["raw_inputs"])),
            "repaired_sibling_absent_after": not (root / REPAIRED_RELATIVE).exists(),
            "repaired_sibling_absent_before": not (root / REPAIRED_RELATIVE).exists(),
            "repository_root_at_capture": root.as_posix(),
        },
        "environment": {
            "byteorder": sys.byteorder,
            "filesystem_encoding": sys.getfilesystemencoding(),
            "filesystem_utf8_mode": sys.flags.utf8_mode,
            "locale_environment": {
                key: os.environ.get(key)
                for key in ("LANG", "LC_ALL", "TZ", "PYTHONHASHSEED", "SOURCE_DATE_EPOCH")
            },
            "platform": sys.platform,
            "python_executable": sys.executable,
            "python_implementation": sys.implementation.name,
            "python_version": sys.version,
            "unicode_version": __import__("unicodedata").unidata_version,
            "umask": format(old_umask, "04o"),
        },
        "schema_version": BASELINE_SCHEMA_VERSION,
        "tools": {
            "git": _command_version(root, ["/usr/bin/git", "--version"]),
            "python": _command_version(root, ["/usr/bin/python3", "--version"]),
            "tools_source_sha256": {
                path.name: sha256_file(path)
                for path in sorted((root / "goal-4/tools").glob("*.py"), key=lambda item: item.name)
            },
        },
    }
