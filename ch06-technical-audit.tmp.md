# CH06 token-sensitive technical audit

Status: **COMPLETE** — 74/74 authoritative pages inspected (PDF 239–312; printed 223–296), 25 exact guarded correction candidates, 0 unresolved source readings.

## Scope and authority

- Authoritative source: `A New Kind of Science/A New Kind of Science.pdf`, PDF pages 239–312.
- Raw source audited: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`, byte interval `[418051, 488397)` (CH06 only).
- The PDF pixels were authoritative. Native PDF text and XML/font extraction were used only to find and diagnose possible token-sensitive sites.
- Checked classes: formulas and mathematical variables, Wolfram Language expressions, rule/code numbers, counts, ranges, percentages, powers, large integers, step/period labels, scientific notation, tables and graph scales, inline cell glyphs, figure-embedded numeric labels, italic technical labels, and `I/l/1`, `O/0`, punctuation, exponent, and brace ambiguities.

## Evidence and hashes

| Artifact | SHA-256 |
|---|---|
| Authoritative PDF | `a3cc5dd60e12d6b563aee86ea31a15b03f9cddfd4869b8f965d3a11bbc61a0d6` |
| Raw monolithic Markdown | `55537ca8cf7d99197b0e5ba043abbade76739e056e3b04b2f9eb6cf7e2ffee20` |
| Exact CH06 raw slice | `ea43e3fa83ef57beccd9954a61272579c4efc2d3f7c80f561b418745450460da` |
| Diagnostic PDF XML/font extraction | `b247aa59f6d75d566efe2883a35cb31f61f7e7aef2d1a9dafb5c706c35a8f814` |
| Sorted 220 dpi page-render checksum stream | `59f8fe1ffcdafc05f4aa0ace33561ae2b5c98b82c903b4e19bd6492d8e8791ac` |
| Sorted contact-sheet checksum stream | `b54679c98bfd5311e52c80fe79b363f841d9f747e0ce30f7789ec4ecad8c6874` |
| Final candidate JSONL | `c34cca5e8bd58787d8720edf894e34f0d5d06bb28f50f83c8db4f504c0d01897` |

All 74 pages were rendered individually at 220 dpi and viewed. Ambiguous inline material was rerendered at 600 or 1200 dpi. The PDF's inline raster objects were also decoded at native pixel resolution where available.

## Exact candidate set

The file `/tmp/ch06-technical-candidates.jsonl` contains 25 records. Every `before` value occurs exactly once in the CH06 source slice, all `raw_start_byte` guards match the original bytes, and no candidate spans overlap.

| PDF | Candidate label(s) | Disposition |
|---:|---|---|
| 252 | `italic-code-1815` | Restore printed italic `code 1815`. |
| 253 | `italic-code-2007` | Restore printed italic `code 2007`. |
| 254 | `delete-stray-page-number-238` | Delete OCR pickup of folio 238. The correct italic `code 1659` remains visible in the current raster asset. |
| 255 | `italic-code-2043` | Restore printed italic `code 2043`. |
| 260 | `continuous-label-0398`, `continuous-label-04`, `continuous-label-pair` | Correct `0.39` to `0.398`; restore italics on `0.398`, `0.4`, and `{0.5, 1.13}`. |
| 270 | `italic-one-cell-changed` | Restore italic `1 cell changed`. |
| 273 | `limited-system-function-math` | Restore all printed `t`/`n` variables and live `Mod[...]` / `MultiplicativeOrder[...]` math; normalize boundaries. |
| 274 | `limited-state-count-math`, `maximum-period-math-boundary` | Restore `n` variables and normalize both padded `$2^n$` spans. |
| 276 | `repetition-period-caption-math`, `limited-pattern-bound-math` | Normalize all graph-caption powers; restore `n = 29` and final `n` as math. |
| 283 | `repeated-block-bound-math`, `rule-126-inline-blocks` | Restore `n`, normalize `$2^n$`, and restore the inline blocks `■■□□` and `■■■□`. |
| 287 | `delete-rule-184-ocr-crumb` | Delete corrupt duplicate `nie 184`; the correct italic label remains in the current raster asset. |
| 288 | `rule-184-substitution-system` | Restore exact raster-decoded substitution: `■→■□■`, `□→□□■`, black seed; normalize math boundaries. |
| 293 | `rule-128-time-variables` | Restore both printed `t` variables as live math. |
| 294 | `network-node-bound-math`, `forbidden-length-12-block` | Normalize `$t^2$`, restore final `$t$`, and replace em-dash OCR with `□■■■□■■□■■■□`. |
| 298 | `italic-class4-code20-label`, `italic-class4-code357-label`, `italic-class4-code1329-label` | Restore all three printed italic code/color/neighborhood labels. |
| 304 | `italic-initial-condition-54889` | Restore italic `initial condition number 54,889`. |
| 312 | `structure-l-glyph` | Correct capital `I` to printed lowercase structure label `l`. |

Two deletion records carry explicit ordering dependencies: retain the raster `code 1659` label on PDF 254 and the raster `rule 184` label on PDF 287, or restore them as live italic labels if those assets are later recropped to exclude the labels.

## Inline raster glyph decisions

These were read from source pixels, not inferred from OCR:

- PDF 283: two 4×1 source objects decode to black-black-white-white and black-black-black-white (`■■□□`, `■■■□`).
- PDF 288: the five inline source objects are 1×1, 3×1, 1×1, 3×1, and 1×1 pixels. Their RGB values decode exactly to black; black-white-black; white; white-white-black; black. Thus the printed system is `■→■□■`, `□→□□■`, starting from `■`.
- PDF 294: the inline object is exactly 12×1 pixels with values white-black-black-black-white-black-black-white-black-black-black-white (`□■■■□■■□■■■□`).
- Other tiny source rasters on PDFs 279–280 and 293 are labels/blocks inside complete retained figure images and require no additional live-text serialization.

## Page-by-page coverage ledger

| PDF | Printed | Token-sensitive material checked | Disposition |
|---:|---:|---|---|
| 239 | 223 | Chapter number 6; opener typography | PASS |
| 240 | 224 | Rules 254, 0, 32, 160, 250; refs 24/53 | PASS |
| 241 | 225 | Rules 4, 108, 218, 232 | PASS |
| 242 | 226 | Rule 126 | PASS |
| 243 | 227 | Embedded rules 22, 30, 150, 182; 300 cells | PASS (raster labels intact) |
| 244 | 228 | Embedded rules 90, 105; page 32 | PASS (raster labels intact) |
| 245 | 229 | Rule 110 | PASS |
| 246 | 230 | 700 steps | PASS |
| 247 | 231 | Classes 1–4; year 1983 | PASS |
| 248 | 232 | Complete 32-rule grid from 0 through 254 | PASS (raster labels intact) |
| 249 | 233 | Even code grid 0 through 62 | PASS (raster labels intact) |
| 250 | 234 | Code grid 1002 through 1095 in increments of 3 | PASS (raster labels intact) |
| 251 | 235 | 1500 steps; three colors | PASS |
| 252 | 236 | Code 1815 | CANDIDATE: italic label |
| 253 | 237 | Code 2007 | CANDIDATE: italic label |
| 254 | 238 | Code 1659; folio 238 | CANDIDATE: delete stray folio; raster code correct |
| 255 | 239 | Code 2043 | CANDIDATE: italic label |
| 256 | 240 | Codes 219, 438, 1380, 1632; class combinations | PASS (raster labels intact) |
| 257 | 241 | Codes 1000816–1000940 in increments of 4 | PASS (raster labels intact) |
| 258 | 242 | Continuous parameter range 0 to 1; classes 1–4 | PASS |
| 259 | 243 | Parameter labels 0, 0.1, …, 0.9 | PASS (raster labels intact) |
| 260 | 244 | Parameters 0.398, 0.4, `{0.5, 1.13}`; multiplier 1.13 | CANDIDATES: value + italics |
| 261 | 245 | Pages 248/249; rule 110; class 4 | PASS |
| 262 | 246 | Codes 4, 12, 24, 30, 38, 52; steps 1/2/5/100/500; totals 5→0 | PASS (raster labels intact) |
| 263 | 247 | Even codes 2–60; 500 steps; 64 possibilities | PASS (raster labels intact) |
| 264 | 248 | Codes 4, 12, 24, 38, 30, 52 | PASS (raster labels intact) |
| 265 | 249 | Steps 200/500/1000; 8 neighbors; 9-neighbor code 224 | PASS |
| 266 | 250 | Rules 160, 108, 126, 110; classes 1–3 | PASS (raster labels intact) |
| 267 | 251 | Rules 22, 30, 126 | PASS (raster labels intact) |
| 268 | 252 | Classes 1–4; rule 110 | PASS |
| 269 | 253 | Labels 1–6 cells changed | PASS (complete raster labels) |
| 270 | 254 | Label 1 cell changed | CANDIDATE: italic label |
| 271 | 255 | Six positions; moves 1–5; periods 6/3/2/3/6 | PASS (raster labels intact) |
| 272 | 256 | Sizes 10/11; moves, periods, prime-factor statement | PASS (raster labels intact) |
| 273 | 257 | Sizes 6–14; periods; `Mod[2^t,n]`; `MultiplicativeOrder[2,n]` | CANDIDATE: variables/functions/boundaries |
| 274 | 258 | `$2^n$`; n = 5/10/20/30; 32/1024/1,048,576/1,073,741,824; rule 45 | CANDIDATES: variables/boundaries |
| 275 | 259 | Rule 90/30; sizes 15–25; all printed periods | PASS (raster labels intact) |
| 276 | 260 | Graph scales; rules 90/30/45/110; power laws; 29; 463,347,935; 86% | CANDIDATES: math normalization |
| 277 | 261 | Rule 30; page 27 | PASS |
| 278 | 262 | Rule 22; class 3 | PASS |
| 279 | 263 | Rule 22 initial-condition strips | PASS (tiny rasters retained in figure) |
| 280 | 264 | Rule 90; rule 30/22 comparisons; initial-condition strips | PASS (tiny rasters retained in figure) |
| 281 | 265 | Rules 22/90; levels 64/128/256/512 | PASS (raster labels intact) |
| 282 | 266 | Rule 30; repetition-period construction; page 210 | PASS |
| 283 | 267 | `$n$`, `$2^n$`; periods ≤15; rule 126; two inline blocks | CANDIDATES: math + glyphs |
| 284 | 268 | Periods 1–10; block sizes 1/2/12/7/5/84/15/4/15/155; period 11 requires 275 cells | PASS (raster labels read directly; native spacing artifact ignored) |
| 285 | 269 | Rules 126/90; two-cell blocks; alternate steps | PASS |
| 286 | 270 | Rule 90 self-emulation and two-cell blocks | PASS |
| 287 | 271 | Rules 150/184; three-cell blocks | CANDIDATE: delete duplicate OCR crumb |
| 288 | 272 | Rules 90/150/184; page 82/83; exact substitution glyphs | CANDIDATE: exact substitution/math |
| 289 | 273 | Rules 184/90; page 338 | PASS |
| 290 | 274 | Rule number 4067213884 | PASS |
| 291 | 275 | Rules 255 and 4; one step | PASS |
| 292 | 276 | Rule 4; attractor examples | PASS |
| 293 | 277 | Rules 255/4; steps 1–3; two printed t variables | CANDIDATE: `$t$` variables |
| 294 | 278 | Rules 108/128/132/160/184; steps 1–4; `$t^2$`; 12-cell block | CANDIDATES: math + exact glyphs |
| 295 | 279 | Rules 126/110; steps 1–4; exponential growth statement | PASS |
| 296 | 280 | Rules 204/240/30/90; steps 1–4 | PASS |
| 297 | 281 | Code 20; initial conditions 151/187/189/195; periods 2/9/1/22 | PASS |
| 298 | 282 | Codes 20/357/1329; color/neighborhood labels | CANDIDATES: three italic labels |
| 299 | 283 | Odd initial conditions 1–285; width <9; base 2; 195/219; period 22 | PASS (raster table intact) |
| 300 | 284 | Ten structure IDs and periods; 25 billion; widths 30–34; periods ≤15; exception 7; width 64 | PASS (raster labels intact) |
| 301 | 285 | Complete period-1–10 structure inventory and large initial-condition integers | PASS (raster labels intact) |
| 302 | 286 | Code 357; 28, 7,795, 1,706,588, 4,803,890, 154,596,664, 514,454,827; periods | PASS (raster reads `7,795`; native `7 ,795` is diagnostic noise) |
| 303 | 287 | Code 1329; nine structure IDs; periods 78/7/2/12/31R/9/48R/2/9; 54,889; 256 | PASS (raster labels intact) |
| 304 | 288 | Code 1329; 10 cells; 256 steps; 54,889; 97,439 | CANDIDATE: italic 54,889 label |
| 305 | 289 | Initial conditions 54,889/97,439/166,426/115,396/2,069,116 | PASS (raster labels intact) |
| 306 | 290 | Rule 110; blocks of 14; period 7 | PASS |
| 307 | 291 | Rule 110; widths <40 and 41; pages 293–296 | PASS |
| 308 | 292 | Structure labels a–n; exceptions a/j; alternate m/n | PASS (raster labels intact) |
| 309 | 293 | Rule 110; length 41; 77 steps; 20 cells; separations 37/107 | PASS |
| 310 | 294 | Structures o/j; four copies; page 292 | PASS |
| 311 | 295 | Structures e/o; page 292 | PASS |
| 312 | 296 | Structures l/i; >4000 steps; 8 structures; 2000/4300 steps | CANDIDATE: `I`→`l` |

## Residual detectors and recurrence checks

- Numeric inventory: after image-reference filenames were removed, the raw CH06 slice contained 415 numeric-token occurrences across 119 token spellings. Comparison against the authoritative source text and pixels found one true value mismatch: raw `0.39` versus source `0.398`. The raw `238` is not a value mismatch; it is an incorrectly serialized printed folio.
- Rule/code recurrence: 97 literal `rule N` occurrences and 22 literal `code N` occurrences in live raw prose/labels were searched in context. All digits agree with source pixels, including rule number `4067213884`. The only rule-label OCR fragment is `nie 184`, which is deleted because the correct label is already rasterized.
- Italic/font-run audit: all source italic technical runs that exist as live raw text were checked. Eleven live figure labels require restored italics. All source italic `n`/`t` variables in PDFs 273–276, 283, and 293–294 are covered by candidates.
- Math-boundary audit: the baseline has 14 occurrences of two spaces before `$` and 7 occurrences of two spaces after `$`, across eight affected raw lines. The virtual corrected slice has zero before-math and zero after-math double-space residues.
- Virtual application: 25/25 byte guards match; every `before` count is 1; spans are ordered and non-overlapping. The virtual corrected slice contains 58 dollar delimiters (balanced), with zero remaining exact occurrences of `nie 184`, `and and`, five-em-dash block OCR, standalone bad `0.39`, `structures (I) and (i)`, plain `after t steps`, plain `where n is`, or the audited plain figure labels.
- Glyph ambiguity detector: source inline-raster dimensions and pixel values were enumerated. All caption-level inline glyph sequences are either restored live (PDFs 283, 288, 294) or demonstrably retained inside complete figure rasters (PDFs 279–280, 293).
- Table/large-integer check: all high-risk comma-grouped labels on PDFs 300–305 were read directly from high-resolution source and compared with retained rasters. No live-text numeric correction beyond `0.398` is needed.

## Unresolved

None. The source readings are determinate. The only integration cautions are the two explicit raster-label retention dependencies recorded on the PDF 254 and PDF 287 deletion candidates.
