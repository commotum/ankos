import hashlib
import json
from pathlib import Path


RAW_PATH = Path("ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md")
OUT_PATH = Path("/tmp/ch06-technical-candidates.jsonl")
CH06_START = 418_051
CH06_END = 488_397


rows = [
    {
        "label": "italic-code-1815",
        "before": "code 1815",
        "after": "*code 1815*",
        "authoritative_location": "pdf:0252",
        "reason": "Restore the printed italic code label beneath the full-page pattern.",
    },
    {
        "label": "italic-code-2007",
        "before": "code 2007",
        "after": "*code 2007*",
        "authoritative_location": "pdf:0253",
        "reason": "Restore the printed italic code label beneath the full-page pattern.",
    },
    {
        "label": "delete-stray-page-number-238",
        "before": "![](_page_253_Picture_1.jpeg)\n\n238\n\n![](_page_254_Picture_1.jpeg)",
        "after": "![](_page_253_Picture_1.jpeg)\n\n![](_page_254_Picture_1.jpeg)",
        "authoritative_location": "pdf:0254",
        "reason": "Delete the OCR pickup of printed page number 238; the source's italic `code 1659` label is already preserved inside _page_253_Picture_1.jpeg.",
    },
    {
        "label": "italic-code-2043",
        "before": "code 2043",
        "after": "*code 2043*",
        "authoritative_location": "pdf:0255",
        "reason": "Restore the printed italic code label beneath the full-page pattern.",
    },
    {
        "label": "continuous-label-0398",
        "before": "![](_page_259_Picture_2.jpeg)\n\n0.39",
        "after": "![](_page_259_Picture_2.jpeg)\n\n*0.398*",
        "authoritative_location": "pdf:0260",
        "reason": "Restore the final digit in the printed parameter 0.398 and its italic figure-label styling.",
    },
    {
        "label": "continuous-label-04",
        "before": "![](_page_259_Picture_4.jpeg)\n\n0.4",
        "after": "![](_page_259_Picture_4.jpeg)\n\n*0.4*",
        "authoritative_location": "pdf:0260",
        "reason": "Restore the printed italic styling of the parameter label 0.4.",
    },
    {
        "label": "continuous-label-pair",
        "before": "![](_page_259_Picture_6.jpeg)\n\n{0.5, 1.13}",
        "after": "![](_page_259_Picture_6.jpeg)\n\n*{0.5, 1.13}*",
        "authoritative_location": "pdf:0260",
        "reason": "Restore the printed italic styling of the two-parameter figure label.",
    },
    {
        "label": "italic-one-cell-changed",
        "before": "1 cell changed",
        "after": "*1 cell changed*",
        "authoritative_location": "pdf:0270",
        "reason": "Restore the printed italic label beneath the full-page sensitivity example.",
    },
    {
        "label": "limited-system-function-math",
        "before": "A system where the number that represents the position of the dot doubles at each step, wrapping around whenever it reaches the right-hand end. (After t steps the dot is thus at position  $Mod[2^t, n]$  in a size n system.) The plot at left gives the repetition period for this system as a function of its size; for odd n this period is equal to MultiplicativeOrder[2, n].",
        "after": "A system where the number that represents the position of the dot doubles at each step, wrapping around whenever it reaches the right-hand end. (After $t$ steps the dot is thus at position $Mod[2^t, n]$ in a size $n$ system.) The plot at left gives the repetition period for this system as a function of its size; for odd $n$ this period is equal to $MultiplicativeOrder[2, n]$.",
        "authoritative_location": "pdf:0273",
        "reason": "Restore every printed italic variable and Wolfram Language expression, and remove extraction-only padding around live math.",
    },
    {
        "label": "limited-state-count-math",
        "before": "But in a cellular automaton, every possible arrangement of black and white cells corresponds to a possible state of the system. With n cells there are thus  $2^n$  possible states. And this number increases very rapidly with the size n: for 5 cells there are already 32 states, for 10 cells 1024 states, for 20 cells 1,048,576 states, and for 30 cells 1,073,741,824 states.",
        "after": "But in a cellular automaton, every possible arrangement of black and white cells corresponds to a possible state of the system. With $n$ cells there are thus $2^n$ possible states. And this number increases very rapidly with the size $n$: for 5 cells there are already 32 states, for 10 cells 1024 states, for 20 cells 1,048,576 states, and for 30 cells 1,073,741,824 states.",
        "authoritative_location": "pdf:0274",
        "reason": "Restore both printed italic n variables and normalize the padded 2^n math boundary.",
    },
    {
        "label": "maximum-period-math-boundary",
        "before": "The pictures on the next page show the actual repetition periods for various cellular automata. In general, a rapid increase with size is characteristic of class 3 behavior. Of the elementary rules, however, only rule 45 seems to yield periods that always stay close to the maximum of  $2^n$ . And in all cases, there are considerable fluctuations in the periods that occur as the size changes.",
        "after": "The pictures on the next page show the actual repetition periods for various cellular automata. In general, a rapid increase with size is characteristic of class 3 behavior. Of the elementary rules, however, only rule 45 seems to yield periods that always stay close to the maximum of $2^n$. And in all cases, there are considerable fluctuations in the periods that occur as the size changes.",
        "authoritative_location": "pdf:0274",
        "reason": "Remove extraction-only padding around the printed 2^n expression.",
    },
    {
        "label": "repetition-period-caption-math",
        "before": "Repetition periods for various cellular automata as a function of size. The initial conditions used in each case consist of a single black cell, as in the pictures on the previous page. The dashed gray line indicates the maximum possible repetition period of  $2^n$ . The maximum repetition period for rule 90 is  $2^{(n-1)/2} - 1$ . For rule 30, the peak repetition periods are of order  $2^{0.63n}$ , while for rule 45, they are close to  $2^n$  (for n = 29, for example, the period is 463,347,935, which is 86% of the maximum possible). For rule 110, the peaks seem to increase roughly like  $n^3$ .",
        "after": "Repetition periods for various cellular automata as a function of size. The initial conditions used in each case consist of a single black cell, as in the pictures on the previous page. The dashed gray line indicates the maximum possible repetition period of $2^n$. The maximum repetition period for rule 90 is $2^{(n-1)/2} - 1$. For rule 30, the peak repetition periods are of order $2^{0.63n}$, while for rule 45, they are close to $2^n$ (for $n = 29$, for example, the period is 463,347,935, which is 86% of the maximum possible). For rule 110, the peaks seem to increase roughly like $n^3$.",
        "authoritative_location": "pdf:0276",
        "reason": "Normalize all five formula boundaries in the graph caption and restore the printed italic n in n = 29.",
    },
    {
        "label": "limited-pattern-bound-math",
        "before": "such case, the pattern must repeat itself with a period of at most  $2^n$  steps, where n is the size of the pattern.",
        "after": "such case, the pattern must repeat itself with a period of at most $2^n$ steps, where $n$ is the size of the pattern.",
        "authoritative_location": "pdf:0276",
        "reason": "Normalize the 2^n math boundary and restore the printed italic n variable.",
    },
    {
        "label": "repeated-block-bound-math",
        "before": "For what happens is that each block in effect independently acts like a system of limited size. The right-hand neighbor of the rightmost cell in any particular block is the leftmost cell in the next block, but since all the blocks are identical, this cell always has the same color as the leftmost cell in the block itself. And as a result, the block evolves just like one of the systems of limited size that we discussed on page 255. So this means that given a block that is n cells wide, the repetition period that is obtained must be at most  $2^n$  steps.",
        "after": "For what happens is that each block in effect independently acts like a system of limited size. The right-hand neighbor of the rightmost cell in any particular block is the leftmost cell in the next block, but since all the blocks are identical, this cell always has the same color as the leftmost cell in the block itself. And as a result, the block evolves just like one of the systems of limited size that we discussed on page 255. So this means that given a block that is $n$ cells wide, the repetition period that is obtained must be at most $2^n$ steps.",
        "authoritative_location": "pdf:0283",
        "reason": "Restore the printed italic n and normalize the padded 2^n math boundary.",
    },
    {
        "label": "rule-126-inline-blocks",
        "before": "Rule 126 with a typical random initial condition, and with an initial condition that consists of a random sequence of the blocks and and Rule 126 in general shows class 3 behavior, as on the left. But with the special initial condition on the right it acts like a simple class 2 rule. Note the patches of class 2 behavior even in the picture on the left.",
        "after": "Rule 126 with a typical random initial condition, and with an initial condition that consists of a random sequence of the blocks $\\blacksquare\\blacksquare\\Box\\Box$ and $\\blacksquare\\blacksquare\\blacksquare\\Box$. Rule 126 in general shows class 3 behavior, as on the left. But with the special initial condition on the right it acts like a simple class 2 rule. Note the patches of class 2 behavior even in the picture on the left.",
        "authoritative_location": "pdf:0283",
        "reason": "Restore the two omitted four-cell inline raster blocks exactly as printed: black-black-white-white and black-black-black-white.",
    },
    {
        "label": "delete-rule-184-ocr-crumb",
        "before": "![](_page_286_Picture_9.jpeg)\n\nnie 184\n\n![](_page_286_Picture_11.jpeg)",
        "after": "![](_page_286_Picture_9.jpeg)\n\n![](_page_286_Picture_11.jpeg)",
        "authoritative_location": "pdf:0287",
        "reason": "Delete a corrupt duplicate OCR crumb; the printed italic `rule 184` label is already present inside _page_286_Picture_9.jpeg.",
    },
    {
        "label": "rule-184-substitution-system",
        "before": "The pattern produced by rule 184 (shown at left) evolving from a nested initial condition. The particular initial condition shown can be obtained by applying the substitution system  $\\blacksquare \\to \\blacksquare \\blacksquare$ ,  $\\Box \\to \\blacksquare \\blacksquare$ , starting from a single black element  $\\blacksquare$  (see page 83). With this initial condition, rule 184 exhibits an equal number of black and white stripes, which annihilate in pairs so as to yield a regular nested pattern.",
        "after": "The pattern produced by rule 184 (shown at left) evolving from a nested initial condition. The particular initial condition shown can be obtained by applying the substitution system $\\blacksquare \\to \\blacksquare \\Box \\blacksquare$, $\\Box \\to \\Box \\Box \\blacksquare$, starting from a single black element $\\blacksquare$ (see page 83). With this initial condition, rule 184 exhibits an equal number of black and white stripes, which annihilate in pairs so as to yield a regular nested pattern.",
        "authoritative_location": "pdf:0288",
        "reason": "Decode the five source raster glyph runs exactly: black maps to black-white-black, white maps to white-white-black, with a black seed; also normalize all math boundaries.",
    },
    {
        "label": "rule-128-time-variables",
        "before": "In rule 128, for example, the fact that regions of black shrink by one cell on each side at each step means that any region of black that exists after t steps must have at least t white cells on either side of it.",
        "after": "In rule 128, for example, the fact that regions of black shrink by one cell on each side at each step means that any region of black that exists after $t$ steps must have at least $t$ white cells on either side of it.",
        "authoritative_location": "pdf:0293",
        "reason": "Restore both printed italic t variables as live math.",
    },
    {
        "label": "network-node-bound-math",
        "before": "Networks representing possible sequences of black and white cells that can occur at successive steps in the evolution of several class 1 and 2 cellular automata. These networks never have more than about  $t^2$  nodes after t steps.",
        "after": "Networks representing possible sequences of black and white cells that can occur at successive steps in the evolution of several class 1 and 2 cellular automata. These networks never have more than about $t^2$ nodes after $t$ steps.",
        "authoritative_location": "pdf:0294",
        "reason": "Normalize the t^2 math boundary and restore the second printed italic t variable.",
    },
    {
        "label": "forbidden-length-12-block",
        "before": "length 12 block —————.",
        "after": "length 12 block $\\Box\\blacksquare\\blacksquare\\blacksquare\\Box\\blacksquare\\blacksquare\\Box\\blacksquare\\blacksquare\\blacksquare\\Box$.",
        "authoritative_location": "pdf:0294",
        "reason": "Replace five OCR em dashes with the exact twelve-cell source raster sequence white-black-black-black-white-black-black-white-black-black-black-white.",
    },
    {
        "label": "italic-class4-code20-label",
        "before": "2 colors, next-nearest neighbors, code 20",
        "after": "*2 colors, next-nearest neighbors, code 20*",
        "authoritative_location": "pdf:0298",
        "reason": "Restore the printed italic technical label for the first class 4 example.",
    },
    {
        "label": "italic-class4-code357-label",
        "before": "3 colors, nearest neighbors, code 357",
        "after": "*3 colors, nearest neighbors, code 357*",
        "authoritative_location": "pdf:0298",
        "reason": "Restore the printed italic technical label for the second class 4 example.",
    },
    {
        "label": "italic-class4-code1329-label",
        "before": "3 colors, nearest neighbors, code 1329",
        "after": "*3 colors, nearest neighbors, code 1329*",
        "authoritative_location": "pdf:0298",
        "reason": "Restore the printed italic technical label for the third class 4 example.",
    },
    {
        "label": "italic-initial-condition-54889",
        "before": "initial condition number 54,889",
        "after": "*initial condition number 54,889*",
        "authoritative_location": "pdf:0304",
        "reason": "Restore the printed italic initial-condition label beneath the unbounded-growth figure.",
    },
    {
        "label": "structure-l-glyph",
        "before": "A collision between structures (I) and (i) from page 292. It takes more than 4000 steps for the final outcome involving 8 separate structures to become clear. The height of the picture corresponds to 2000 steps, and the third picture ends at step 4300.",
        "after": "A collision between structures (l) and (i) from page 292. It takes more than 4000 steps for the final outcome involving 8 separate structures to become clear. The height of the picture corresponds to 2000 steps, and the third picture ends at step 4300.",
        "authoritative_location": "pdf:0312",
        "reason": "Correct the OCR ambiguity between capital I and the printed lowercase structure label l.",
    },
]


raw = RAW_PATH.read_bytes()
chapter = raw[CH06_START:CH06_END]
assert hashlib.sha256(chapter).hexdigest() == "ea43e3fa83ef57beccd9954a61272579c4efc2d3f7c80f561b418745450460da"

encoded_rows = []
for row in rows:
    before = row["before"].encode("utf-8")
    expected_count = chapter.count(before)
    if expected_count != 1:
        raise SystemExit(f"{row['label']}: expected one CH06 occurrence, found {expected_count}")
    local_start = chapter.find(before)
    record = {
        "document_id": "CH06",
        "label": row["label"],
        "raw_start_byte": CH06_START + local_start,
        "before": row["before"],
        "after": row["after"],
        "expected_count": expected_count,
        "authoritative_location": row["authoritative_location"],
        "reason": row["reason"],
        "ordering_dependency": [],
    }
    encoded_rows.append(record)

encoded_rows.sort(key=lambda item: item["raw_start_byte"])
for previous, current in zip(encoded_rows, encoded_rows[1:]):
    previous_end = previous["raw_start_byte"] + len(previous["before"].encode("utf-8"))
    if previous_end > current["raw_start_byte"]:
        raise SystemExit(f"overlap: {previous['label']} -> {current['label']}")

OUT_PATH.write_text(
    "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in encoded_rows),
    encoding="utf-8",
)
print(f"wrote {len(encoded_rows)} records to {OUT_PATH}")
print(hashlib.sha256(OUT_PATH.read_bytes()).hexdigest())
