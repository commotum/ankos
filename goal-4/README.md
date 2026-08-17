# Goal 4 Archive Record

Status: **RETIRED AND SUPERSEDED**.

Goal 4 was an attempted whole-book, source-blind construction audit of the
canonical *A New Kind of Science* corpus. It built corpus manifests, source-unit
segmentation, guardrails, review ledgers, candidate and cross-reference
ledgers, worker bundles, validators, per-chapter review scripts, and search
artifacts. The attempt progressed through Chapter 8 but did not complete the
intended whole-book audit.

The useful conceptual result was the discipline of separating physical source
assets, Markdown references, reading units, candidate evidence, and semantic
authority. Goal 5 subsequently completed the construction taxonomy and API
audit; Goals 6 and 7 replaced the architecture and implementation path.

## Why the machinery was removed

The frozen Goal 4 state described an older, flat corpus layout containing 31
Markdown files and 1,607 JPEGs, including 293 unreferenced extraction crops.
The canonical corpus was later reorganized into per-document directories and
those 293 redundant crops were removed. It now contains 1,314 JPEGs and 1,314
resolving image references, with no missing, unreferenced, or multiply owned
images.

Goal 4's manifests, hashes, paths, counts, ledgers, and validators were
therefore stale. A focused rerun of its corpus and audit tests against the
current tree produced 12 failures and 9 passes. No active package code or main
test imports Goal 4.

The cleanup removed 87 tracked Goal 4 files representing 47,205,085 bytes of
Git blobs. It also removed an ignored 155,823,909-byte `review-history.jsonl`
file and other ignored runtime caches. The tracked material remains available
in Git history; the ignored review-history file was intentionally not retained.

One exact image-content repetition remains in the canonical corpus: the same
pale Rule 30 background occurs at source pages 14, 862, and 1214. Each instance
is explicitly referenced at a distinct book location, so it is retained as
intentional source fidelity rather than extraction noise.

