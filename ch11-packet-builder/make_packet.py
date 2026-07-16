#!/usr/bin/env python3
"""Build and independently verify the CH11 second-pass correction packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


REPO = Path("/home/jake/Developer/ankos")
OUT = Path("/tmp/ch11-packet-builder")
RAW_PATH = REPO / "ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md"
FINAL_PATH = REPO / "ref/A-New-Kind-of-Science-Repaired/CHAPTERS/11-The-Notion-of-Computation.md"
CORRECTIONS_PATH = REPO / "goal-5/corrections.jsonl"
RANGES_PATH = REPO / "goal-5/source-ranges.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


raw_bytes = RAW_PATH.read_bytes()
raw = raw_bytes.decode("utf-8")
current_bytes = FINAL_PATH.read_bytes()
current = current_bytes.decode("utf-8")
old = [json.loads(line) for line in CORRECTIONS_PATH.read_text(encoding="utf-8").splitlines() if line]
ranges = json.loads(RANGES_PATH.read_text(encoding="utf-8"))
chapter = next(row for row in ranges["documents"] if row["id"] == "CH11")
old_by_id = {row["id"]: row for row in old}

assert len(old) == 707
assert old[-1]["id"] == "G5-C-0707"
assert sha256(current_bytes) == "3dfc34e4a99364e3fa48b555ed7399a8a8c8a1acd3b977763554c89b836cfd63"
assert raw_bytes[chapter["raw_start_byte"] : chapter["raw_end_byte_exclusive"]].decode("utf-8") == raw[raw.index("![](_page_652_Picture_0.jpeg)") : raw.index("![](_page_730_Picture_0.jpeg)")]


drafts: list[dict[str, object]] = []


def add(
    before: str,
    after: str,
    location: str,
    reason: str,
    findings: list[str],
) -> None:
    encoded = before.encode("utf-8")
    start = raw_bytes.find(encoded)
    assert start >= 0, (findings, before[:80])
    assert raw_bytes.count(encoded, chapter["raw_start_byte"], chapter["raw_end_byte_exclusive"]) == 1
    assert before != after and before
    drafts.append(
        {
            "document_id": "CH11",
            "raw_start_byte": start,
            "before": before,
            "after": after,
            "expected_count": 1,
            "authoritative_location": location,
            "reason": reason,
            "reviewer_type": "agent",
            "verification_status": "SOURCE_VERIFIED",
            "_findings": findings,
        }
    )


def raw_slice(start_anchor: str, end_anchor: str) -> str:
    start = raw.index(start_anchor)
    end = raw.index(end_anchor, start)
    return raw[start:end]


def reordered(before: str, prefix: str, continuation_start: str, *, group_replace: tuple[str, str] | None = None) -> str:
    separator = "\n\n" + continuation_start
    left, tail = before.split(separator, 1)
    assert left.startswith(prefix + "\n\n")
    group = left[len(prefix) + 2 :]
    if group_replace is not None:
        old_text, new_text = group_replace
        assert group.count(old_text) == 1
        group = group.replace(old_text, new_text)
    continuation = continuation_start + tail
    assert continuation.endswith("\n\n")
    return prefix + " " + continuation + group + "\n\n"


# PDF 654–655 and detector typography/spacing findings.
add(
    "row of n black cells, 0 black cells survive if n is even, and 1 black cell survives if n is odd.",
    "row of $n$ black cells, 0 black cells survive if $n$ is even, and 1 black cell survives if $n$ is odd.",
    "pdf:0654",
    "Restore all three source-italic n variables in the even/odd cellular-automaton caption.",
    ["CH11-S2-SRC-D001"],
)
add(
    "exactly  $5 \\times 5 = 25$  black squares.",
    "exactly $5 \\times 5 = 25$ black squares.",
    "pdf:0655",
    "Normalize extraction-only doubled spaces outside the already-correct inline formula.",
    ["CH11-S2-RES-D002"],
)
add(
    "adding the original number n together n times.",
    "adding the original number $n$ together $n$ times.",
    "pdf:0655",
    "Restore both source-italic n variables in the squaring cellular-automaton caption.",
    ["CH11-S2-SRC-D002"],
)
add(
    "command such as Log[15], what actually happens",
    "command such as $Log[15]$, what actually happens",
    "pdf:0658",
    "Restore the source technical-expression treatment of Log[15] as inline mathematics.",
    ["CH11-S2-RES-D001"],
)

# PDF 672–673: move the complete figure group after the joined paragraph and
# fold the wildcard-expression external-spacing repair into the moved caption.
d3_before = raw_slice(
    "while in a cellular\n\n![](_page_672_Picture_1.jpeg)",
    "The same basic approach can be used to construct a cellular automaton",
)
d3_after = reordered(
    d3_before,
    "while in a cellular",
    "automaton all cells are always effectively treated as being exactly the same.",
    group_replace=(
        "cellular automaton,  $\\boxminus$  indicates a cell",
        "cellular automaton, $\\boxminus$ indicates a cell",
    ),
)
add(
    d3_before,
    d3_after,
    "pdf:0672; through pdf:0673",
    "Join the source paragraph across the page turn, move the intact three-image/caption group after it, and normalize extraction-only spaces around the wildcard formula.",
    ["CH11-S2-SRC-D003", "CH11-S2-RES-D003"],
)

# PDF 676–677: move the register-machine figure group after the joined paragraph.
d4_before = raw_slice(
    "registers of\n\n![](_page_676_Picture_1.jpeg)",
    "So what about systems based on numbers?",
)
d4_after = reordered(
    d4_before,
    "registers of",
    "the register machine. In the center of the cellular automaton",
)
add(
    d4_before,
    d4_after,
    "pdf:0676; through pdf:0677",
    "Join the source paragraph across the page turn and move the intact register-machine figure group after the completed paragraph.",
    ["CH11-S2-SRC-D004"],
)

# PDF 678 and PDF 684 source typography.
add(
    "AND, OR and Not. In the examples above, two variables, p and q, are used, and in each case the behavior obtained with all four possible combinations of values for p and q are shown.",
    "AND, OR and NOT. In the examples above, two variables, $p$ and $q$, are used, and in each case the behavior obtained with all four possible combinations of values for $p$ and $q$ are shown.",
    "pdf:0678",
    "Restore source capitalization of NOT and all four source-italic p/q variable occurrences in the logic-circuit caption.",
    ["CH11-S2-SRC-D005"],
)
add(
    "three symbols, p, q and r.",
    "three symbols, $p$, $q$ and $r$.",
    "pdf:0684",
    "Restore all three source-italic variables in the symbolic-system caption.",
    ["CH11-S2-SRC-D006"],
)

# PDF 685–687: G5-C-0705 occupies the loose label between the two halves, so
# delete the pre-label figure block at the paragraph break and reinsert it from
# the strictly post-label guard together with the remaining caption.
d7_full = raw_slice(
    "such a Turing\n\n![](_page_684_Figure_4.jpeg)",
    "This leaves only one remaining type of system from Chapter 3",
)
d7_label = old_by_id["G5-C-0705"]["before"]
d7_label_index = d7_full.index(d7_label)
d7_a_before = d7_full[:d7_label_index]
d7_b_before = d7_full[d7_label_index + len(d7_label) :]
d7_prefix = "such a Turing"
assert d7_a_before.startswith(d7_prefix + "\n\n")
d7_group_pre = d7_a_before[len(d7_prefix) + 2 :]
d7_caption, d7_cont_tail = d7_b_before.split("\n\nmachine can readily", 1)
d7_continuation = "machine can readily" + d7_cont_tail
assert d7_continuation.endswith("\n\n") and d7_group_pre.endswith("\n\n")
add(
    d7_a_before,
    d7_prefix + " ",
    "pdf:0685; through pdf:0686",
    "Remove the pre-label portion of the intervening PDF685–686 figure sequence from the middle of the source paragraph; paired with the strictly post-G5-C-0705 reinsertion guard.",
    ["CH11-S2-SRC-D007"],
)
add(
    d7_b_before,
    d7_continuation + d7_group_pre + d7_caption + "\n\n",
    "pdf:0685; through pdf:0687",
    "Complete the source paragraph and then reinsert the intact ordered PDF685–686 figure/caption sequence, without touching installed loose-label deletion G5-C-0705.",
    ["CH11-S2-SRC-D007"],
)

add(
    "a whole number n, and at each step one finds the remainder after dividing by a constant, and based on the value of this remainder one then applies some specified arithmetic operation to n.",
    "a whole number $n$, and at each step one finds the remainder after dividing by a constant, and based on the value of this remainder one then applies some specified arithmetic operation to $n$.",
    "pdf:0687",
    "Restore both source-italic n variables in the arithmetic-system prose.",
    ["CH11-S2-SRC-D008"],
)

# PDF 696–698 plate relocation.
d9_before = raw_slice(
    "rule 110: the basic\n\n![](_page_696_Picture_2.jpeg)",
    "But at the outset it is by no means clear",
)
d9_after = reordered(
    d9_before,
    "rule 110: the basic",
    "idea is to have each of the various kinds of lines in the picture",
)
add(
    d9_before,
    d9_after,
    "pdf:0696; through pdf:0698",
    "Join the source paragraph across the intervening PDF697 plate and move its intact figure/caption group after the completed paragraph.",
    ["CH11-S2-SRC-D009"],
)

# PDF 698–703 plate sequence. G5-C-0706 owns the PDF701 marker itself; the
# two new guards end before and start after that immutable installed span.
d10_full = raw_slice(
    "as a side-effect two\n\n![](_page_698_Picture_1.jpeg)",
    "Region (c) shows what happens when the information",
)
d10_marker = old_by_id["G5-C-0706"]["before"]
d10_marker_index = d10_full.index(d10_marker)
d10_a_before = d10_full[:d10_marker_index]
d10_b_before = d10_full[d10_marker_index + len(d10_marker) :]
d10_prefix = "as a side-effect two"
assert d10_a_before.startswith(d10_prefix + "\n\n")
d10_group_pre = d10_a_before[len(d10_prefix) + 2 :]
assert d10_b_before.startswith("\n\n") and d10_b_before.endswith("\n\n")
d10_continuation = d10_b_before[2:-2]
add(
    d10_a_before,
    d10_prefix + " " + d10_continuation + "\n\n" + d10_group_pre,
    "pdf:0698; through pdf:0702",
    "Complete the split source paragraph before serializing the first three intact plate groups; this guard ends strictly before installed PDF701 marker correction G5-C-0706.",
    ["CH11-S2-SRC-D010"],
)
add(
    d10_b_before,
    "\n\n",
    "pdf:0702; through pdf:0703",
    "Delete the now-relocated continuation from its raw post-marker position while retaining the paragraph break after the G5-C-0706 PDF701 continuation caption.",
    ["CH11-S2-SRC-D010"],
)

# PDF 707–708 page-top plate.
d11_before = raw_slice(
    "if one looks sufficiently hard at any\n\n![](_page_707_Figure_1.jpeg)",
    "The final demonstration that a given rule is universal",
)
d11_after = reordered(
    d11_before,
    "if one looks sufficiently hard at any",
    "particular rule, then one will always eventually be able to find",
)
add(
    d11_before,
    d11_after,
    "pdf:0707; through pdf:0708",
    "Join the source paragraph across the page-top class-4 figure and move the intact figure/caption group after the completed paragraph.",
    ["CH11-S2-SRC-D011"],
)

# PDF 710–711 page-top plate. The following additive plate remains in place.
d12_before = raw_slice(
    "they produce more complicated patterns of behavior—as the pictures at\n\n![](_page_710_Picture_1.jpeg)",
    "![](_page_710_Picture_4.jpeg)",
)
d12_after = reordered(
    d12_before,
    "they produce more complicated patterns of behavior—as the pictures at",
    "the bottom of this page illustrate. As we saw on page 264",
)
add(
    d12_before,
    d12_after,
    "pdf:0710; through pdf:0711",
    "Join the source paragraph across the top plate, move that intact plate group after the completed paragraph, and leave the following additive plate in its original order.",
    ["CH11-S2-SRC-D012"],
)

# PDF 713: guard A ends exactly where G5-C-0693 begins; guard B starts exactly
# where it ends. This both restores upright ordinal superscripts and removes
# extraction-only external spaces without overlapping the installed formula fix.
d16_a_before = "the  $n^{th}$  new stripe on the right is produced at step  $2 n^2 + 8 n - 9$ . Even in the last case shown, the arrangement of stripes eventually becomes completely regular, with the  $n^{th}$  new stripe being produced at step  $n^2 + 21 n/2 - "
d16_a_after = "the $n^{\\text{th}}$ new stripe on the right is produced at step $2 n^2 + 8 n - 9$. Even in the last case shown, the arrangement of stripes eventually becomes completely regular, with the $n^{\\text{th}}$ new stripe being produced at step $n^2 + 21 n/2 - "
add(
    d16_a_before,
    d16_a_after,
    "pdf:0713",
    "Restore upright ordinal superscripts for both source-italic n variables and normalize extraction-only spaces; this guard ends strictly before installed G5-C-0693.",
    ["CH11-S2-SRC-D016", "CH11-S2-RES-D004"],
)
add(
    "$ . Pairs of cells are grouped",
    "$. Pairs of cells are grouped",
    "pdf:0713",
    "Remove the extraction-only space before the formula-closing punctuation using a guard strictly after installed G5-C-0693.",
    ["CH11-S2-RES-D004"],
)

# PDF 719–720 plate relocation.
d13_before = raw_slice(
    "rule 30 can actually be made to emulate\n\n![](_page_719_Figure_1.jpeg)",
    "So what about other underlying rules?",
)
d13_after = reordered(
    d13_before,
    "rule 30 can actually be made to emulate",
    "one step in the evolution of every single one of the 256 possible",
)
add(
    d13_before,
    d13_after,
    "pdf:0719; through pdf:0720",
    "Join the source paragraph across the full-width rule-30 figure and move the intact figure/caption group after the completed paragraph.",
    ["CH11-S2-SRC-D013"],
)

add(
    'should "halt" with the head staying',
    "should “halt” with the head staying",
    "pdf:0722",
    "Restore the source typographic quotation marks around halt.",
    ["CH11-S2-SRC-D014"],
)

# PDF 727–729: G5-C-0702 owns the Mathematica operator phrase embedded in the
# caption. The first guard ends at its start; the second starts at its end.
d15_full = raw_slice(
    "But with initial condition (e) of length 8 the pictures show\n\n![](_page_727_Figure_1.jpeg)",
    "Other combinators yield still more complicated behavior",
)
d15_installed = old_by_id["G5-C-0702"]["before"]
d15_installed_index = d15_full.index(d15_installed)
d15_a_before = d15_full[:d15_installed_index]
d15_b_before = d15_full[d15_installed_index + len(d15_installed) :]
d15_prefix = "But with initial condition (e) of length 8 the pictures show"
assert d15_a_before.startswith(d15_prefix + "\n\n")
d15_group_prefix = d15_a_before[len(d15_prefix) + 2 :]
assert d15_b_before.startswith("\n\n") and d15_b_before.endswith("\n\n")
d15_continuation = d15_b_before[2:-2]
add(
    d15_a_before,
    d15_prefix + " " + d15_continuation + "\n\n" + d15_group_prefix,
    "pdf:0727; through pdf:0728",
    "Complete the source paragraph before the full-page combinator plate and move the plate/caption prefix after it; this guard ends strictly before installed G5-C-0702.",
    ["CH11-S2-SRC-D015"],
)
add(
    d15_b_before,
    "\n\n",
    "pdf:0728; through pdf:0729",
    "Delete the now-relocated continuation from its raw post-G5-C-0702 position while preserving the paragraph break after the completed caption.",
    ["CH11-S2-SRC-D015"],
)


# Assign append IDs in deterministic raw-coordinate order, then strip the
# private provenance field from the integration-ready JSONL rows.
drafts.sort(key=lambda row: int(row["raw_start_byte"]))
for number, row in enumerate(drafts, 708):
    row["id"] = f"G5-C-{number:04d}"

packet_rows = [
    {key: value for key, value in row.items() if not key.startswith("_")}
    for row in drafts
]

# Load the production validator directly and validate the 707+22 raw union.
spec = importlib.util.spec_from_file_location("goal5_build", REPO / "goal-5/build.py")
assert spec and spec.loader
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
documents = build.validate_ranges(raw_bytes, ranges)
checked = build.validate_corrections(old + packet_rows, raw_bytes, documents)
assert len(checked) == 729

# Independent full-document proof: replay each exact new preimage once against
# the already-built 707-correction Markdown by current-output coordinates, then
# compare byte-for-byte with a fresh immutable-raw build of the 729-correction
# union. This does not use repaired output as build input; it is only an oracle.
current_spans: list[tuple[int, int, dict[str, object]]] = []
for row in drafts:
    before = str(row["before"])
    assert current.count(before) == 1, row["id"]
    start = current.index(before)
    current_spans.append((start, start + len(before), row))
for left, right in zip(sorted(current_spans), sorted(current_spans)[1:]):
    assert right[0] >= left[1], (left[2]["id"], right[2]["id"])

intended = current
for start, end, row in sorted(current_spans, reverse=True):
    assert intended[start:end] == row["before"]
    intended = intended[:start] + str(row["after"]) + intended[end:]

union_segment = build.apply_corrections(
    chapter,
    raw_bytes[chapter["raw_start_byte"] : chapter["raw_end_byte_exclusive"]],
    old + packet_rows,
)
union_text = union_segment.decode("utf-8")
assert union_text == intended

image_pattern = re.compile(r"!\[\]\(([^)]+\.jpeg)\)")
images_before = image_pattern.findall(current)
images_after = image_pattern.findall(union_text)
assert len(images_before) == 108
assert images_after == images_before

# Every requested finding must be covered and all desired source joins must
# precede their still-ordered figure groups in the final text.
all_findings = [f"CH11-S2-SRC-D{i:03d}" for i in range(1, 17)] + [f"CH11-S2-RES-D{i:03d}" for i in range(1, 5)]
finding_to_ids: dict[str, list[str]] = {finding: [] for finding in all_findings}
for row in drafts:
    for finding in row["_findings"]:
        finding_to_ids[str(finding)].append(str(row["id"]))
assert all(finding_to_ids.values())

ordering_checks = {
    "D003": ("while in a cellular automaton all cells are always effectively treated as being exactly the same.", "![](_page_672_Picture_1.jpeg)"),
    "D004": ("registers of the register machine. In the center of the cellular automaton", "![](_page_676_Picture_1.jpeg)"),
    "D007": ("such a Turing machine can readily be made to emulate a Turing machine with any number of colors.", "![](_page_684_Figure_4.jpeg)"),
    "D009": ("rule 110: the basic idea is to have each of the various kinds of lines", "![](_page_696_Picture_2.jpeg)"),
    "D010": ("as a side-effect two additional localized structures are produced", "![](_page_698_Picture_1.jpeg)"),
    "D011": ("if one looks sufficiently hard at any particular rule, then one will always eventually", "![](_page_707_Figure_1.jpeg)"),
    "D012": ("they produce more complicated patterns of behavior—as the pictures at the bottom of this page illustrate.", "![](_page_710_Picture_1.jpeg)"),
    "D013": ("rule 30 can actually be made to emulate one step in the evolution of every single one", "![](_page_719_Figure_1.jpeg)"),
    "D015": ("But with initial condition (e) of length 8 the pictures show that no fixed point is reached", "![](_page_727_Figure_1.jpeg)"),
}
ordering_results: dict[str, dict[str, int | bool]] = {}
for name, (joined, first_image) in ordering_checks.items():
    joined_index = union_text.index(joined)
    image_index = union_text.index(first_image, joined_index)
    ordering_results[name] = {
        "joined_text_index": joined_index,
        "first_figure_index": image_index,
        "joined_text_precedes_figure": joined_index < image_index,
    }

old_693 = old_by_id["G5-C-0693"]
old_693_start = old_693["raw_start_byte"]
old_693_end = old_693_start + len(old_693["before"].encode("utf-8"))
d16_rows = [row for row in drafts if "CH11-S2-RES-D004" in row["_findings"]]
assert len(d16_rows) == 2
d16_rows.sort(key=lambda row: int(row["raw_start_byte"]))
d16_a_end = int(d16_rows[0]["raw_start_byte"]) + len(str(d16_rows[0]["before"]).encode("utf-8"))
d16_b_start = int(d16_rows[1]["raw_start_byte"])
assert d16_a_end == old_693_start
assert d16_b_start == old_693_end

for phrase in (
    "row of $n$ black cells, 0 black cells survive if $n$ is even, and 1 black cell survives if $n$ is odd.",
    "adding the original number $n$ together $n$ times.",
    "command such as $Log[15]$",
    "AND, OR and NOT",
    "three symbols, $p$, $q$ and $r$.",
    "a whole number $n$",
    "operation to $n$.",
    "$n^{\\text{th}}$ new stripe",
    "should “halt” with the head staying",
):
    assert phrase in union_text, phrase
assert "cellular automaton,  $\\boxminus$  indicates" not in union_text
assert "exactly  $5 \\times 5 = 25$  black squares." not in union_text
assert "$ . Pairs of cells are grouped" not in union_text

packet_path = OUT / "integration-ready-corrections.jsonl"
packet_data = ("\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in packet_rows) + "\n").encode("utf-8")
packet_path.write_bytes(packet_data)

verification = {
    "status": "PASS",
    "ambiguities": 0,
    "source_current_sha256": sha256(current_bytes),
    "source_current_bytes": len(current_bytes),
    "source_current_lines": len(current.splitlines()),
    "existing_correction_count": len(old),
    "new_correction_count": len(packet_rows),
    "union_correction_count": len(checked),
    "new_id_first": packet_rows[0]["id"],
    "new_id_last": packet_rows[-1]["id"],
    "new_ids_contiguous": [row["id"] for row in packet_rows] == [f"G5-C-{number:04d}" for number in range(708, 730)],
    "packet_sha256": sha256(packet_data),
    "union_output_sha256": sha256(union_segment),
    "union_output_bytes": len(union_segment),
    "union_output_lines": len(union_text.splitlines()),
    "independent_current_replay_equals_raw_union": union_text == intended,
    "image_reference_count_before": len(images_before),
    "image_reference_count_after": len(images_after),
    "image_reference_sequence_preserved": images_after == images_before,
    "finding_to_ids": finding_to_ids,
    "ordering_checks": ordering_results,
    "pdf713_installed_guard": {
        "id": "G5-C-0693",
        "raw_start_byte": old_693_start,
        "raw_end_byte_exclusive": old_693_end,
        "new_guard_a_end_byte_exclusive": d16_a_end,
        "new_guard_b_start_byte": d16_b_start,
        "strictly_non_overlapping": d16_a_end <= old_693_start and d16_b_start >= old_693_end,
        "exactly_adjacent": d16_a_end == old_693_start and d16_b_start == old_693_end,
    },
    "operations": [
        {
            "id": row["id"],
            "raw_start_byte": row["raw_start_byte"],
            "raw_end_byte_exclusive": int(row["raw_start_byte"]) + len(str(row["before"]).encode("utf-8")),
            "raw_occurrence_count": raw_bytes[chapter["raw_start_byte"] : chapter["raw_end_byte_exclusive"]].count(str(row["before"]).encode("utf-8")),
            "findings": row["_findings"],
        }
        for row in drafts
    ],
}
verification_path = OUT / "verification.json"
verification_data = (json.dumps(verification, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
verification_path.write_bytes(verification_data)

coverage_lines = [
    f"- `{finding}` → {', '.join(f'`{correction_id}`' for correction_id in ids)}"
    for finding, ids in finding_to_ids.items()
]
operation_lines = [
    f"| `{row['id']}` | {row['raw_start_byte']} | {int(row['raw_start_byte']) + len(str(row['before']).encode('utf-8'))} | {', '.join(row['_findings'])} |"
    for row in drafts
]
report = f"""# CH11 Integration-Ready Correction Packet Verification

Status: **PASS**. Ambiguities: **0**.

The packet contains {len(packet_rows)} exact append-only CH11 guards, tentatively numbered `{packet_rows[0]['id']}`–`{packet_rows[-1]['id']}` in deterministic raw-coordinate order. Together with the 707 installed corrections, production validation accepts a 729-correction union with no overlapping raw spans and with every preimage occurring exactly once in the immutable CH11 interval.

## Full-document proof

- Current 707-correction target: `{sha256(current_bytes)}` ({len(current_bytes)} bytes; {len(current.splitlines())} logical lines).
- Independently replaying every new exact preimage once against that current target produced the same full byte string as rebuilding from the immutable monolith with the complete 707+22 union.
- Union target: `{sha256(union_segment)}` ({len(union_segment)} bytes; {len(union_text.splitlines())} logical lines).
- All 108 image references are retained in exactly their prior basename order.
- The nine paragraph/plate repairs each place the now-contiguous source paragraph before its intact figure sequence. The PDF710 additive plate remains after the relocated top plate.
- `CH11-S2-RES-D003` is folded into the `D003` relocation guard. `CH11-S2-SRC-D016` is folded into the two `RES-D004` spacing guards.
- PDF713 guard A ends at byte {d16_a_end}, exactly where installed `G5-C-0693` begins; guard B begins at byte {d16_b_start}, exactly where `G5-C-0693` ends. Neither overlaps it.
- Installed guards `G5-C-0705`, `G5-C-0706`, and `G5-C-0702` forced the minimal two-guard implementations of D007, D010, and D015 respectively; each new pair remains strictly outside the installed span.

## Finding coverage

{chr(10).join(coverage_lines)}

## Raw spans

| ID | Start | End (exclusive) | Findings |
|---|---:|---:|---|
{chr(10).join(operation_lines)}

The machine-readable proof, full operation coordinates, ordering checks, finding map, target hashes, and PDF713 adjacency proof are in `verification.json`.
"""
report_path = OUT / "verification-report.md"
report_data = report.encode("utf-8")
report_path.write_bytes(report_data)

hash_lines = []
for path in (packet_path, verification_path, report_path):
    hash_lines.append(f"{sha256(path.read_bytes())}  {path.name}")
hashes_path = OUT / "SHA256SUMS"
hashes_path.write_text("\n".join(hash_lines) + "\n", encoding="utf-8")

print(json.dumps({
    "status": "PASS",
    "new_corrections": len(packet_rows),
    "ids": [packet_rows[0]["id"], packet_rows[-1]["id"]],
    "packet_sha256": sha256(packet_data),
    "union_output_sha256": sha256(union_segment),
    "union_output_bytes": len(union_segment),
    "union_output_lines": len(union_text.splitlines()),
    "image_refs": len(images_after),
}, indent=2))
