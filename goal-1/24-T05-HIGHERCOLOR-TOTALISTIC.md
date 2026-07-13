# 24-T05-HIGHERCOLOR-TOTALISTIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T05, CSV line 6, `Higher-Color Totalistic Cellular Automata`; taxonomy section 5 at `ref/notes/CA-Types.md:126-145` is search vocabulary only, not book evidence.
- The taxonomy hypothesis is a radius-one totalistic profile with four, five, or more values. It claims no new support, read, update, successor, or halt semantics beyond T03; the book audit must prove or revise that grouping.
- The strict five-color comparison states 13 sum cases and `5^13 = 1,220,703,125` possible rules, while a separate Notes/application example names a four-color totalistic code `1004600`. These are initial evidence routes, not yet an exhaustive closure.
- If canonical values are `A_k=(0,...,k-1)` with `nu_k(i)=i` and `r=1`, T03 gives arity `q=3`, sum domain `0..3(k-1)`, table length `M=3k-2`, and rule count `R=k^(3k-2)`. The stage must independently verify the color valuation, range, code direction, examples, and whether “higher-color” means exactly `k>=4`.
- T01/T02/T03/T04 already establish fixed ordered support, all-site old-snapshot reads, typed same-site assignment, atomic parallel update, structural table identity, arbitrary-precision tagged code identity, and the preset/restriction/property/run/view boundary. D118 currently predicts that T05 is the higher-color radius-one preset over T03; this is a hypothesis under evidence audit.
- The current API/runtime remains semantically incomplete for this profile: `simple_programs.md` and `src/ca/rules.py` conflate exact numeric sums with counts/histograms; spatial rollout is family-dispatched and binary-decoded; batch rule IDs use `numpy.int64`; no current test executes a four-or-more-color totalistic sum table.
- Goal 1 remains evidence/design only. This stage may edit only `goal-1/` and must not implement a T05 runtime family.

## Updated Assumptions

- Working hypothesis: T05 is a strictly validated catalog preset/range fixing `r=1`, canonical integer alphabet/valuation, and `k>=4`, then resolving to an ordinary generic T03 program with identical structural identity and executor types.
- A finite `k` is required for every concrete program. “Four, five, or more” does not authorize an unbounded or lazily partial table, wildcard rows, implicit defaults, or fake fixed capacity.
- Structural sum-table identity remains primary. The optional numeric code is an arbitrary-precision relation whose digit count grows with `k`; fixed-width integers, floating values, or JSON numbers cannot define identity.
- Alphabet order, exact numeric valuation, palette, and displayed color names remain distinct. Noncanonical valuations belong to generic T03 unless the source proves them part of T05.
- Rule program, seed/background, finite realization, behavior class, property/proof, gallery selection, raster, and application relation remain separate identities.
- No new decision will be added unless exhaustive evidence contradicts D115-D118 or proves a genuinely new semantic responsibility.

## Big Picture Objective

Determine the exact higher-color totalistic parameter domain and evidence bundle, prove whether it is only a strict T03 preset/range, and produce the smallest implementation-ready Goal 2 constructor and conformance plan without a higher-color executor or fixed-width shortcut.

## Catalog Identity

- Stable ID: T05.
- Exact CSV name: `Higher-Color Totalistic Cellular Automata` at `ref/notes/CA-Types.csv:6`.
- Taxonomy section: 5, vocabulary seed only.
- Entry hypothesis: parameter-range preset/profile over T03, presently expected to fix radius one, canonical valuation, and `k>=4`.
- Initial vocabulary: higher-color/higher colour, more colors, four-color/4-color, five-color/5-color, four/five possible colors, `k=4`, `k=5`, `r=1`, 10 cases, 13 cases, `4^10`, `5^13`, `1,048,576`, `1,220,703,125`, code `1004600`, totalistic, average color, assignment of values to colors, rule complexity, dying out/undecidability, class behavior, and related non-totalistic color-count controls.

## Search Log

IN PROGRESS. Direct terms, aliases, formulas, examples, captions, Notes, actual Index, split files, linked assets, and cross-references are being saturated. Every candidate will be placed in one exact manifest with zero remainder.

## Book Excerpts

IN PROGRESS. Unique construction-relevant excerpts will be recorded verbatim with canonical line provenance after the candidate partition is closed.

## Construction Model

IN PROGRESS. The initial model is a canonical `k>=4,r=1` restriction of T03, but its exact domain, validation, fixtures, relations, and observer boundaries remain under evidence audit.

## Current API Fit

IN PROGRESS. Relevant portions of `simple_programs.md` are being reread against the evidence rather than inherited by assertion.

## Current Runtime Fit

IN PROGRESS. Relevant `src/ca` modules and tests are being reread; no runtime changes are authorized in Goal 1.

## Principles Audit

IN PROGRESS. Principles 0, 1, 2, 7, 9, 10, 12, 13, 15, and 16 currently favor a strict preset resolving to T03, but evidence controls the final result.

## Detailed Implementation Plan

1. Close an exact source query manifest across strict text, captions, Notes, actual Index, splits, aliases, named codes, formulas, applications, and neighboring non-totalistic controls.
2. Close a bidirectional linked-asset manifest with exact file identity, dimensions, hashes, caption/provenance roles, inclusion status, and source-permitted semantic or raster checks.
3. Reconstruct the precise `k`/radius/value/sum/table/code state and prove all finite validation/count boundaries with adversarial examples.
4. Re-audit current documentation, runtime, tests, prior decisions, and T03/T04/T06/T07/T08 boundaries.
5. Write the concrete Goal 2 constructor, migration, conformance, rejection, and no-cheating plan.
6. Run embedded evidence/semantic/asset checks, independent review, repository tests, coverage/fence/diff gates, then reintegrate all global ledgers.

## Goal 2 Implementation Stage

IN PROGRESS. Expected dependency: the shared G2-T03 numeric valuation, exact-sum structural table/codec, fixed-lattice executor, stable program identity, and conformance suite. T05 must add only discoverability and strict preset validation unless evidence proves otherwise.

## No-Cheating Checks

- No `higher_color`, `k>=4`, four-color, five-color, or code-`1004600` runtime branch, family dispatch, duplicate executor, or update law.
- No finite-capacity ceiling, sparse/partial table, wildcard/default row, opaque exhaustive-table substitution, fixed-width/float/JSON-number rule identity, or binary shift decoder.
- No palette-derived valuation, implicit alphabet ordering, histogram/nonzero-count substitute, tolerant average, callback escape, or global formula bypass.
- No seed, blank/quiescent condition, application outcome, dying-out predicate, behavior label, crop, horizon, raster, or view data fused into program identity.
- The preset and corresponding generic T03 program must resolve to identical structural identity and executor types; invalid `k`, radius, valuation, table, and code inputs must fail visibly.

## Completion Requirements

- [ ] Every direct/alias/formula/code/caption/Notes/actual-Index/split/cross-reference/application/control candidate is dispositioned with zero remainder.
- [ ] Every relevant source-linked asset is hash-pinned and classified, with every source-permitted semantic/raster oracle closed.
- [ ] The exact higher-color parameter domain, table/cardinality/code rules, canonical fixtures, and T03/T04/T06/T07/T08 boundaries are proved.
- [ ] Current API/runtime fit and a concrete Goal 2 preset/conformance stage are implementation-ready.
- [ ] Global ledgers, independent review, embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS. No completion or new architecture claim is made until all requirements close.

## Integration Results

IN PROGRESS. The ten-question reintegration audit will be answered after the evidence and design close.
