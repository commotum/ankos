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

### Native semantics

| Dimension | Reconstructed T02 semantics |
|---|---|
| State | `STATE = SUPPORT + VALUES`; no control. Support is the same fixed ordered one-dimensional regular lattice as T01. Values form a total field in one declared finite ordered alphabet `A`; strict T02 has `k=|A|>=3`. |
| Alphabet | Colors are distinct values. The ordered rank map `rho:A->{0,...,k-1}` is part of rule-code interpretation but does not make colors arithmetic magnitudes. Palette/tone is representation. |
| Active loci | Every semantic site on every event, with finite causal-window lowering separated exactly as in T01. |
| Read | The ordered old-snapshot triple `(left,self,right)`. Context order is semantic and homogeneous at every site. |
| Rule | One total structural table `T:A^3->A`, containing exactly `k^3` entries. No reducer, symmetry, background default, wildcard, mutation generator, callback, or inverse is implicit. |
| Result/update | One typed same-site `Assign(T(left,self,right))` per site; T01's atomic parallel fixed-effects commit applies all results from the same old field. No new update law. |
| Successor/halting | One deterministic successor per valid field, including unchanged fields; no intrinsic halt, branch, rejection, or randomness. A finite horizon is an observation request. |
| Seed | An independent total initial field. Single-gray, random, uniform, periodic, purpose-encoded, and sparse inputs are profiles, never program identity. |
| Support/realization | Native integer line and explicit finite cycle/segment/causal-window realizations retain T01 meanings. No rule number or color count chooses a boundary. |
| Observers/provenance | Spacetime/raster views, behavior class, reversibility, symmetry/color-relabelling orbit, purpose/optimality, emulation relation, and random table-mutation history remain separate from native state and events. |

### Ordered base-`k` rule codec

For ranked colors `l,c,r in {0,...,k-1}`:

```text
context_index(l,c,r) = k^2*l + k*c + r
output(n,l,c,r)      = floor(n/k^context_index) mod k
code(T)              = sum(T(l,c,r) * k^context_index(l,c,r))
```

- Context index zero is `000`; index `k^3-1` is `(k-1)(k-1)(k-1)`.
- The padded base-`k` display table is ordered from the highest context down to `000`, while the output for `000` is the least-significant digit. This reduces exactly to T01's `4*l+2*c+r` bit codec at `k=2`.
- There are `S=k^3` contexts, `R=k^S=k^(k^3)` total tables, and valid codes are exactly `0..R-1`. Leading zero digits are required table entries.
- Structural `(alphabet,ordered table)` data are primary. The integer is a lossless optional codec tied to the alphabet order. Relabeling colors requires conjugating the table; changing only the palette does not change the program.
- A sparse dot display such as `BOOK:4684` must first expand every dot to the explicit center output. A table mutation is a meta-level edit of exactly one context entry plus optional draw provenance; it is not a stochastic cell event or hidden fallback.
- General `k` requires arbitrary-precision codes: at `k=4`, `R=4^64=2^128`, already beyond signed 64-bit storage. Batches therefore reference structural programs/stable IDs or lossless arbitrary-precision code strings rather than coercing semantic rule codes into `numpy.int64`.

### Variant disposition

| Profile | Semantic relation |
|---|---|
| `k=2` | Exactly the completed T01 specialization; T02 retains catalog traceability for `k>=3` without duplicating execution. |
| `k=3`, all 27-entry tables | Direct strict profile; exact count `3^27=7,625,597,484,987`. |
| General `k`, range one | Direct Notes generalization through `{n,k}` and `k^(k^3)`; same construction. |
| General range `r`, two-cell staggered neighborhoods, or higher dimensions | Supporting general-CA siblings with different read geometry; not smuggled into T02's radius-one identity. |
| Totalistic/weighted rules | Restricted alternate rule descriptions whose meaning depends on numeric color assignment for `k>2`; T03/T04/T05 own them. |
| Blank-preserving or left-right symmetric tables | Validated restrictions over the same tables; T06/T07 own catalog evidence. |
| Reversible tables | Scoped global property/certificate of the induced map, not a native inverse step or trusted Boolean flag. |
| Random table-mutation sequence | Program-generation/provenance experiment producing successive immutable T02 tables, not CA state or RNG-driven cell evolution. |
| Binary block encoding/emulation | Explicit relation between different programs, supports, steps, and decoders; never the native multi-color representation. |
| Universal/purpose-doubling/mobile/Turing/substitution/computer examples | Named T02 program/seed/emulation profiles; their encoded machine, purpose, search work, or behavior is not extra T02 state. |

## Current API Fit

| Construction element | Fit | Evidence and consequence |
|---|---|---|
| `ALPHABET` with `{0,...,K-1}` or symbols | DIRECT | `simple_programs.md:200-230` explicitly includes `K`-color and symbolic states; semantic alphabet order must be preserved. |
| State/trace address | DIRECT with T01 qualification | A finite 1D trace fits `[t,x,0,0]`; finite `SHAPE` remains a realization, not native topology. |
| Independent seed and explicit finite boundary | PARAMETERIZATION | Existing seed/boundary schemas can express finite profiles but must not enter program identity or imply an edge on `Z`. |
| Ordered radius-one current read | DIRECT/PARAMETERIZATION | Relative selectors and the Wolfram source-time convention express old `(left,self,right)` when order is pinned. |
| `EXHAUSTIVE T:A^3->A` | DIRECT conceptually | `simple_programs.md:1795-1829` states the correct structural table, but gives no normative arbitrary-base codec or table validator. |
| Base-`k` rule codec/arbitrary-precision identity | PRINCIPLED EXTENSION | Required by `BOOK:11897-11900`; code depends on alphabet order and exceeds 64 bits for `k>=4`. |
| Typed assignment/parallel commit | DIRECT T01 reuse | Same source, result, conflict-free atomic update, and deterministic successor; no eleventh law. |
| Totalistic/symmetric/background/reversible/mutation/emulation data | NOT APPLICABLE to base execution | These are restrictions, claims, provenance, or relations rather than rule flags. |

## Current Runtime Fit

| Component | Fit | Exact finding |
|---|---|---|
| `alphabets.int_range_alphabet(k)` | DIRECT data primitive | Supplies ordered digit colors `0..k-1` (`src/ca/alphabets.py:42-73`) but `Dynamics` does not carry/validate an alphabet. |
| `alphabets.symbolic(values)` | DIRECT declaration, incomplete execution | Preserves explicit deterministic order (`alphabets.py:145-179`), while rollout coerces spatial fields/reads to `int64`; symbolic execution needs a validated rank/value layer rather than object cells. |
| `neighborhoods.eca()` / loci / frontier | DIRECT T01 geometry for finite realization | Correct ordered radius-one component and full finite slice; native support/observation lowering remain absent. |
| `rules.exhaustive(...,alphabet_size=k)` | SEMANTIC MISMATCH | Declares `state_count=k` regardless of three-read arity (`rules.py:173-195`), so it cannot derive `S=k^3` or `R=k^(k^3)`. |
| `_channel_state` | SEMANTIC MISMATCH | Weights physical ordered reads by `[1,k,k^2]` (`rollout.py:748-760`), reversing the required left-most-significant context index just as T01 found. |
| Spatial rule application | SEMANTIC MISMATCH | Uses binary right shifts and `&1` (`rollout.py:650-682`); it cannot decode base `k`, return general colors, or store a structural table. |
| Generic lookup execution | SEMANTIC MISMATCH | Family whitelists still reject an ordinary `lookup`; no T02 branch may be added. |
| `Rule.rule_id` / `RawEpisode.rule_id` | PARAMETERIZATION only for small codes | Python `int` is arbitrary precision, but batch normalization forces `numpy.int64` (`rollout.py:264-288`) and output contracts use a numeric rule-id array. General T02 requires structural program references/lossless codecs. |
| `Dynamics` / seeds / boundary | PARAMETERIZATION / PRINCIPLED EXTENSION | Finite field mechanics fit, but alphabet, semantic support, typed result/update, table identity, and observation scope are missing. |
| Tests | SEMANTIC MISMATCH as T02 evidence | Current rule/rollout tests cover binary named families and parity only; none checks `k=3`, 27 contexts, base-3 codes, symbolic order, or `>2^63` identities. |

## Principles Audit

- General `k` is directly supported by the Notes rule-count/implementation and `{n,k}` syntax; strict examples concentrate on `k=3`. T02 is therefore the `k>=3`, radius-one slice of the generic finite-alphabet lookup construction.
- Alphabet cardinality parameterizes T01 without changing support, source coverage, reads, result, commit, or successor. Adding a separate update/executor would duplicate semantics.
- A base-`k` integer is a codec for a complete table, not the rule's only in-memory form. Structural tables avoid fixed-width overflow and make validation/serialization inspectable.
- Color rank for the codec, numeric value for totalistic aggregation, and palette tone for rendering are three different responsibilities.
- A sparse mutation label, reversibility claim, behavior classification, purpose search, raster, or binary block encoding cannot replace or feed the mathematical table/field.
- T03/T04/T05 aggregation, T06 quiescence, T07 reflection, and emulation/property analyzers remain compositional siblings rather than T02 flags.

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
