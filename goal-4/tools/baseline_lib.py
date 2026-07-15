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
