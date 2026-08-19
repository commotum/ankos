# Goal 8: Canonical Family Space Audit

Shorthand: **Space Envelope**

Status: **SCAFFOLDED — NOT STARTED**

## Big-Picture Objective

Review all 60 canonical families in [`ref/types.csv`](../ref/types.csv) and
determine the evidence-backed range of `SPACE` coordinate specifications each
family admits.

For every family, answer five questions:

1. What is its minimal native Space?
2. Which additional Spaces does *A New Kind of Science* show or state?
3. What broader parameterized range can be proved from the defining mechanics?
4. Where does that proof stop?
5. Which tempting alternatives are merely encodings, exclusions, or honest
   unknowns?

Do the family research directly. Prior goals are search aids, not work that
must be ceremonially re-audited.

## Settled Space Semantics

`SPACE` describes admissible coordinates, their relations, support behavior,
and boundary behavior. A Coordinate is one address. A concrete episode domain
is the subset of coordinates actually realized.

Time is always explicit:

```text
t-only   [t]
t+1D     [t,x]
t+2D     [t,x,y]
t+3D     [t,x,y,z]
```

For discrete dynamics, a step preserves every coordinate through `t`, adds a
complete slice at `t+1`, copies locations outside the Frontier into that slice
unchanged, and never overwrites time `t`.

Continuous, event-driven, one-shot, multiway, and relational families must
state their honest explicit-time form rather than being forced into integer
steps or Cartesian grids.

Use this dividing rule:

> Independently addressed, read, written, or related structure belongs in
> Space. Attributes of one addressed location belong in the Alphabet/value
> schema.

Graph adjacency, tree parenthood, order, and incidence can therefore be
relations over generic coordinates. Product/record structure usually belongs
to values. `INTENSIONAL` is a presentation mode, not a Space class.

## Sources

For each family, use only the sources needed to answer its Space question:

1. `ref/types.csv` for identity, order, and starting references.
2. [`goal-5/11-FAMILIES.md`](../goal-5/11-FAMILIES.md) and
   [`goal-5/candidates.md`](../goal-5/candidates.md) to locate defining
   mechanics, variants, and source passages.
3. The actual canonical Book documents under
   [`ref/A-New-Kind-of-Science/`](../ref/A-New-Kind-of-Science/) as semantic
   evidence.
4. Goal 1 family records or Goal 6's catalog crosswalk only when a concrete
   ambiguity or missing variant requires them.

Do not rebuild Goal 1 or Goal 5's exhaustive source audits. Follow additional
Book cross-references only when they can change a Space conclusion.

## Current Facts and Assumptions

- `ref/types.csv` contains exactly 60 unique canonical family rows.
- `book_index` is the review and final presentation order.
- One family may admit multiple Space variants.
- Shape, Seed realization, horizon, or rendering do not by themselves define
  a new Space, though topology and support laws can matter.
- A displayed dimension does not prove a maximum dimension.
- A family name, current `CarrierKind`, stub, or runtime limitation is not
  evidence of its Space.
- A genuine source limitation may remain `unknown`; completion requires that
  it be identified and bounded, not guessed away.

## Non-Negotiable Constraints

1. Cover exactly all 60 `family_id` values and present results by
   `book_index`.
2. Cite the actual Book for every `shown` or `stated` Space claim.
3. A `proved` generalization must state the invariant mechanics, generalized
   parameter, unchanged read/write law, topology requirements, and limit.
4. Never turn “probably,” “natural,” or “could be 3D” into support.
5. Separate native Space from simulations, encodings, renderings, observers,
   and derived graphs.
6. Keep Space separate from Alphabet values, concrete shape, Seed, Frontier,
   Neighborhood, Rule, horizon, and storage representation.
7. Time must be explicit in every admitted claim.
8. Do not require disposition of irrelevant historical leads merely to raise a
   coverage count.
9. Do not use tests, row counts, or a validator as semantic evidence.
10. Do not change `ref/types.csv`, runtime code, tests, prior goals, or the Book
    corpus during this research goal.

## Required Outputs

Create only two research artifacts.

### `spaces.csv`

This is the authoritative normalized result: one row per family x Space claim.

```text
book_index,family_id,home,slug,space_claim,claim_kind,evidence,
time,coordinates,relations,support,boundary,source,reason,limit
```

Allowed `claim_kind` values:

- `native` — part of the family's supported Space envelope;
- `variant` — another supported Space for the same family;
- `encoding` — non-native representation or simulation;
- `excluded` — contradicted or belongs to another family;
- `unknown` — plausible question not settled by available evidence.

Allowed `evidence` values:

- `shown` — directly used by a Book construction or example;
- `stated` — explicitly asserted by the Book;
- `proved` — derived from source-defined mechanics with a written closure
  argument;
- `unresolved` — not admitted; the missing fact is stated in `limit`.

Only `native` and `variant` rows with `shown`, `stated`, or `proved` evidence
belong to the supported Space envelope.

Parameterized claims such as `t+dD for d>=1` should be one proved row, not an
infinite list, and must include the proof and its boundary.

### `findings.md`

Keep this concise. It should contain:

- the final compact Space vocabulary;
- reasoning or closure proofs too large for one CSV cell;
- genuinely difficult or underdetermined families;
- cross-family conclusions; and
- the final answer in `book_index` order or a generated view of it.

Do not duplicate every CSV row in prose.

## Per-Family Completion Test

A family is complete only when:

- its minimal native Space is recorded;
- every Book-shown or Book-stated Space variant found through its defining
  references is recorded;
- any broader claimed closure is proved and bounded;
- relevant encodings, exclusions, and unknowns are identified;
- all admitted claims have actual source evidence or a source-grounded proof;
- explicit time and immutable next-slice semantics are addressed; and
- the five objective questions have direct answers.

## Final Success and Verification

The goal is complete when:

- `spaces.csv` covers the exact 60-family set with no duplicate claim keys;
- every family passes the per-family completion test;
- SPF030 has explicit conclusions for `[t,x]`, `[t,x,y]`, `[t,x,y,z]`, and any
  higher-dimensional or alternative-topology claim encountered;
- graph/tree, continuous, one-shot, multiway, dynamic-support, product, and
  intensional cases have been checked for category mistakes;
- every supported claim has a Book citation or complete proof;
- every remaining unknown states exactly what cannot be established;
- a lightweight final script or one-off command confirms CSV parsing, exact
  family coverage, unique keys, allowed statuses, ordering, and valid cited
  paths;
- `git diff --check` passes; and
- only Goal 8 research files changed.

Structural checks do not establish semantic truth; they only catch omissions
and malformed output.

## Stages

### 1-PILOT

#### Big Picture Objective

Start the real audit immediately by completing `B001` through `B005`, which
includes SPF030 `mobile-head-grid-rewrite`, while letting the minimal CSV
schema prove itself against actual evidence.

#### Detailed Implementation Plan

- Create `spaces.csv` and `findings.md` only when adding real conclusions.
- Audit B001-B005 using the per-family loop in `0-loop.md`.
- For SPF030, directly investigate 1D, 2D, 3D/higher-dimensional, lattice, and
  encoding evidence; do not pre-approve any claim.
- Adjust column wording only if an actual family cannot be expressed honestly.
- Record useful vocabulary in `findings.md` as it emerges from evidence.

#### Completion Requirements

- B001-B005 each pass the per-family completion test.
- SPF030 has evidence-backed rows for each dimensional question actually
  resolved and explicit unknown rows for the rest.
- The two artifacts are usable without a separate source ledger or summary.
- No preparatory work is counted unless it produced or corrected a family
  conclusion.

### 2-B006-B020

#### Big Picture Objective

Complete the next fifteen families in Book order.

#### Detailed Implementation Plan

- Audit B006-B020 directly and append validated claims.
- Reuse prior-goal evidence only to locate relevant Book passages.
- Revise earlier vocabulary or rows if structural, graph, sequence, or
  relation families expose a real defect.
- Record only reasoning that affects a Space conclusion.

#### Completion Requirements

- B001-B020 all pass the per-family completion test.
- `spaces.csv` contains no placeholder or metadata-only conclusions.
- Any schema revision is applied consistently to completed rows.
- Open questions name the missing evidence rather than triggering a general
  re-audit.

### 3-B021-B040

#### Big Picture Objective

Complete B021-B040, including the central multidimensional, graph, structural,
and continuous pressure cases in this range.

#### Detailed Implementation Plan

- Audit each row and add claims immediately.
- Challenge dimensional generalizations against actual mechanics and
  counterexamples.
- Distinguish addressed coordinates from values, relations, support growth,
  branch structure, and observer outputs.
- Revisit earlier rows only when a concrete cross-family contradiction appears.

#### Completion Requirements

- B001-B040 all pass the per-family completion test.
- Every `proved` claim in this range includes a bounded closure argument.
- Graph, tree/path, multiway, growing-support, and continuous claims use the
  same generic vocabulary without being collapsed into one geometry.
- No unresolved work is hidden behind a category label.

### 4-B041-B060

#### Big Picture Objective

Complete the remaining twenty families in Book order.

#### Detailed Implementation Plan

- Audit B041-B060 and finish exact 60-family coverage.
- Pay particular attention to media transforms, relations/search procedures,
  records/streams, continuous fields, and one-shot versus iterative variants.
- Keep transformation input/output coordinates distinct where the mechanics
  require it.
- Add only targeted cross-references that can change a conclusion.

#### Completion Requirements

- All 60 families pass the per-family completion test.
- Every supported claim has direct evidence or a complete proof.
- Every unknown is explicit and bounded.
- The CSV family set exactly matches `ref/types.csv`.

### 5-FINISH

#### Big Picture Objective

Resolve weak spots, check consistency, and deliver the actual answer without
creating another layer of process artifacts.

#### Detailed Implementation Plan

- Revisit only `unknown`, weakly sourced, or cross-family-conflicting claims.
- Challenge SPF030 and the graph/tree, continuous, one-shot, multiway,
  dynamic-support, product, and intensional pressure cases.
- Make vocabulary and proved generalizations consistent.
- Finish `findings.md` without reproducing the CSV.
- Run lightweight structural checks, citation/path checks, `git diff --check`,
  and changed-file inspection.

#### Completion Requirements

- Every requirement under Final Success and Verification passes.
- The result directly answers the Space range for all 60 families.
- No stage, ledger, verifier, or report exists solely to demonstrate activity.
- Any remaining unknown is a substantive source limit, not unfinished work.
