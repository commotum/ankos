# 21-T02-MULTICOLOR-CA

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T02, CSV line 3, `Multi-Color Nearest-Neighbor Cellular Automata`; taxonomy vocabulary is `ref/notes/CA-Types.md:45-66` and remains a search/API seed rather than book evidence.
- The strict Chapter 3 transition at `BOOK:770-776` directly states three colors, the exact count `7,625,597,484,987`, and the ordered-neighborhood/totalistic contrast. Most immediately following examples are totalistic and belong primarily to T03/T04, so their rule aggregation cannot be imported into T02.
- `BOOK:4684` directly describes arbitrary three-color nearest-neighbor tables over all 27 ordered three-cell neighborhoods and a mutation profile that adds or changes individual neighborhood entries.
- `BOOK:5218-5222` directly identifies all `3^27` three-color nearest-neighbor rules and the 1,800 reversible members. Reversibility is a property/restriction, not a different forward update construction.
- T01 already establishes a fixed ordered one-dimensional lattice, total field, synchronous old left/self/right reads, arbitrary finite lookup, typed same-site assignment, atomic parallel commit, and separate native/finite support, seed, trace, and view identities.
- The central question is therefore whether T02 is exactly T01 parameterized by a finite alphabet of cardinality `k>2` plus a base-`k` ordered table codec, or whether direct evidence forces any new state/read/update primitive.
- Current runtime alphabet declarations can represent finite integer/symbolic colors, but the documented/executable exhaustive binary codec and family-dispatched rollout were already defective for T01. Existing nominal color capacity is not proof of an executable general `k^(k^3)` rule table.

## Updated Assumptions

- Treat `k=3` as the strict directly enumerated profile. General `k` remains a candidate generalization until the Notes/Index/general-definition evidence is audited.
- Preserve colors as distinct symbols or validated digits `0..k-1`; visual white/gray/black tones are a view convention unless a numeric aggregate such as totalistic averaging explicitly gives them arithmetic meaning.
- Preserve ordered neighborhoods. A totalistic, semi-totalistic, symmetric, reversible, background-preserving, mutation-generated, or emulation profile is a restriction/property/relation unless evidence makes it defining.
- Do not infer a single-gray-cell seed, unchanged white background, random seed, finite periodic boundary, or figure horizon as native T02 semantics.
- Do not add an eleventh update law unless T02 evidence contradicts T01's fixed-effects atomic commit.

## Big Picture Objective

Determine exhaustively whether multi-color nearest-neighbor cellular automata are the finite-alphabet/base-`k` parameterization of the T01 construction, while preserving exact table ordering/coding, background/seed/reversibility restrictions, mutation provenance, numerical-versus-symbolic color roles, support/realization/trace/view boundaries, and implementation-ready Goal 2 conformance without a family rollout branch.

## Catalog Identity

- Stable ID: T02.
- Exact CSV name: `Multi-Color Nearest-Neighbor Cellular Automata` at `ref/notes/CA-Types.csv:3`.
- Taxonomy: `ref/notes/CA-Types.md:45-66`; vocabulary seed only.
- Candidate entry kind: parameterized fixed-lattice parallel lookup construction, subject to complete evidence audit.
- Initial vocabulary: multi-color/multicolor, three/four/many colors, possible colors/states, nearest-neighbor rules, 27 possible three-cell neighborhoods, `7,625,597,484,987`, base-3 rule/table/code, reversible three-color CA, mutation of neighborhood rules, color encoding, and emulation of colors.

## Search Log

The controlled oracle, exact manifests, split/Notes/actual-Index routing, and zero-remainder dispositions are being built. Initial high-signal anchors are:

- `BOOK:772-776`: three-color count and totalistic contrast;
- `BOOK:4684`: arbitrary 27-entry ordered-neighborhood rule labels and mutation operations;
- `BOOK:5218-5222`: reversible subset of the full three-color nearest-neighbor space;
- `BOOK:7900-7912`: binary block emulation of multi-color rules, retained only as a relation unless it adds native mechanics;
- actual-Index aliases around `BOOK:21134,21187,21323,21542` route color-encoding vocabulary and must be followed rather than counted as construction evidence.

No search is yet called exhaustive and no candidate is silently excluded.

## Book Excerpts

### E1 — Three colors and the full rule-space count

- Provenance: `BOOK:772`, strict Chapter 3 transition.
- Establishes: more than two cell colors and the exact full three-color rule count; totalistic rules are a smaller restriction.

> “The 256 "elementary" rules that we have discussed so far are by most measures the simplest possible—and were the first ones I studied. But one can for example also look at rules that involve three colors, rather than two, so that cells can not only be black and white, but also gray. The total number of possible rules of this kind turns out to be immense—7,625,597,484,987 in all—but by considering only so-called "totalistic" ones, the number becomes much more manageable.”

### E2 — Explicit 27-neighborhood arbitrary-table profile

- Provenance: `BOOK:4684`, supporting caption.
- Establishes: three colors, nearest-neighbor rules, all 27 possible ordered three-cell neighborhoods, and mutations that add or modify individual table entries. A dot means retain the center color in this figure's sparse rule representation.

> “The behavior of a sequence of cellular automaton programs obtained by successive random mutations. The first program contains no rules for changing the color of a cell with any neighborhood. Mutations in successive programs add rules for changing the colors of cells with specific neighborhoods, or modify these rules. Each program in the sequence differs from the previous one by a single mutation, made completely at random. The sequence provides a very simple idealization of biological evolution without explicit natural selection. The cellular automata shown here all have 3 possible colors and nearest-neighbor rules. The label for each picture gives a representation of the rules for each of the 27 possible 3-cell neighborhoods. A dot signifies that the rule does not change the color of the center cell in the neighborhood.”

### E3 — Reversibility is a subset property

- Provenance: `BOOK:5218-5222`, supporting Chapter 9 discussion/caption.
- Establishes: the full three-color nearest-neighbor space has the same exact count, 1,800 members are reversible, and forward complexity does not erase backwards determinability.

> “So is it possible to get more complex behavior while maintaining reversibility? There are a total of 7,625,597,484,987 cellular automata with three colors and nearest-neighbor rules, and searching through these one finds just 1800 that are reversible. Of these 1800, many again exhibit simple behavior, much like the pictures above. But some exhibit more complex behavior, as in the pictures below.”

> “Examples of some of the 1800 reversible cellular automata with three colors and nearest-neighbor rules. Even though these systems exhibit complex behavior that scrambles the initial conditions, all of them are still reversible, so that starting from the configuration of cells at the bottom of each picture, it is always possible to deduce the configurations on all previous steps.”

## Construction Model

Active derivation: test the hypothesis `T02 = T01` with `FiniteAlphabet(k>2)` and a total ordered table `Sigma^3 -> Sigma`. The final model must pin color identity/order, table-index and integer-code conventions, background/seed restrictions, state/update/trace identity, variants, and all evidence boundaries before this section closes.

## Current API Fit

Audit active. T01's semantic fixed-lattice/source/read/result/update responsibilities are candidate `DIRECT` reuse; finite alphabet/table data and base-`k` codecs are candidate `PARAMETERIZATION`; current formula callbacks, totalistic reducers, family dispatch, and binary-only rule helpers are not presumed compatible.

## Current Runtime Fit

Audit active across `src/ca/alphabets.py`, `loci.py`, `neighborhoods.py`, `rules.py`, `specs.py`, `rollout.py`, seeds, datasets, visualization, and corresponding tests. Existing finite-color declarations will be tested separately from arbitrary-table execution and exact codec coverage.

## Principles Audit

- Evidence must establish whether `k` is general or only three in the strict construction.
- Alphabet cardinality may parameterize T01 only if support, reads, result, commit, and successor semantics remain unchanged.
- A base-3 digit string, sparse mutation label, raster tone, or binary block encoding cannot replace the mathematical table/field.
- Totalistic aggregation must stay in T03/T04; reversibility/background preservation/symmetry stay explicit restrictions or claims.

## Detailed Implementation Plan

1. Complete controlled searches and exact line manifests across strict, Notes, actual Index, splits, aliases, formulas, variants, applications, and emulation routes.
2. Record every unique construction-relevant excerpt verbatim and disposition every candidate.
3. Audit every relevant asset and exact/source-permitted semantic or raster oracle.
4. Reconstruct table ordering/code, state/update/successor/boundary/seed semantics and variants before evaluating reuse.
5. Audit current API/runtime/tests and completed decisions for exact reuse versus extension.
6. Write concrete Goal 2 files/tests and no-cheating gates; independently review and integrate all global ledgers.

## Goal 2 Implementation Stage

Pending evidence completion. Expected pressure is a generic finite-alphabet ordered lookup/table codec and conformance presets, not a T02 executor branch. Exact modules, migrations, and tests will be named after the construction audit.

## No-Cheating Checks

- No T02 family branch, binary packing/emulation, totalistic reduction, callback, sparse default hidden in the executor, or raster-decoded rule.
- No binary-only rule cardinality/bit-order helper advertised as general `k` support.
- No view tone or integer digit arithmetic substituted for symbolic color identity.
- No seed/background/boundary/reversibility restriction silently fused into the base rule.
- No finite figure width/horizon presented as native lattice capacity or halt.

## Completion Requirements

- [ ] Every strict/Notes/split/actual-Index/alias/variant/application/emulation textual candidate is dispositioned with reproducible searches.
- [ ] All relevant assets and source-permitted semantic/raster oracles are closed with hashes, geometry, labels, repairs, and exclusions.
- [ ] Exact state/alphabet/table/code/read/update/successor/boundary/seed semantics and variants are explicit.
- [ ] T01/T03/T04/T06/T07/reversible/emulation boundaries and current API/runtime fit are proved.
- [ ] Goal 2 files/dependencies/tests and no-cheating gates are implementation-ready.
- [ ] Global plan/evidence/design ledgers, independent review, diff checks, and repository tests are integrated.

## Stage Results

In progress. Initial direct evidence supports a three-color ordered 27-entry lookup as the same forward construction shape as T01, but neither exhaustive search closure nor general-`k` status is yet proved.

## Integration Results

In progress. No completed stage is contradicted or reopened. T01 parameterization is a hypothesis under active evidence audit; the public transition-update family remains at ten members.
