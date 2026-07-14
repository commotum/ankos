# 34-T22-MOORE-CA

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T22 is CSV line 23, `Moore-Neighborhood Cellular Automata`. The taxonomy is search vocabulary; the Book, source-bound assets, and independently checked semantics remain authoritative.
- Chapter 5 explicitly changes T21's four surrounding cardinal cells to eight surrounding cells “including diagonals” (`BOOK:2212`). The center is retained separately by the rule. This is initial evidence for a NEIGHBORHOOD/RULE parameterization, not another executor.
- The direct examples use center-conditioned black-neighbor counts and codes `175850`, `746`, and `174826` (`BOOK:2226-2234`). Seeds, horizons, shapes, and stopped growth are run data/observers until exact evidence says otherwise.
- The Notes call this the `9-neighbor` profile because the eight surrounding cells plus self participate in the read. Their convolution assigns neighbor weight `2` and self weight `1`, yielding an 18-case `SelfValue x MooreCount` table (`BOOK:13475-13481`).
- The Notes distinguish `2^512` general positional rules, `2^18` outer-totalistic rules, `2^10` equal-sum totalistic rules, and `2^9` growth-totalistic rules for the nine-position square (`BOOK:13542-13549`). Those are distinct schema-tagged RULE representations/restrictions, not family modes.
- T21/D127 already proves the branch-free fixed-lattice runner, explicit Self access, square-grid support/realization separation, Book-frame ordering, and basis/table permutation. Its semantic oracle includes a same-runner T22 control, but T22 still requires its own exhaustive source/assets/rule fixtures and architecture closure.
- The current `dyadaxes_2d` access includes self, four cardinal, and four diagonal cells, so its geometry is a candidate realization. Its majority-gated cardinal/diagonal RULE is not automatically the Book's count table or a canonical T22 preset.
- The governing event remains:

  ```text
  active = FRONTIER.select(configuration)
  reads  = NEIGHBORHOOD.read(configuration, active)
  writes = RULE(active, reads)
  next   = UPDATE.apply(configuration, active, writes)
  ```

## Updated Assumptions

- DOMAIN remains discrete `t+2D`. Square `Z^2` support/topology belongs to CONFIGURATION. A finite array, periodic quotient, fixed exterior, sparse background representation, crop, and raster remain explicit realizations/views.
- Strict Moore access is a declared composition containing exactly one `SelfAt` and the eight unique offsets in `{-1,0,1}^2 \ {(0,0)}`. No center read is implicit, and equal resolved cells on a small torus remain distinct read occurrences.
- Raw Book row/column tuples plus their coordinate-frame tag are authoritative. Mapping to ENU must preserve order or permute every positional table; symmetric count rules cannot validate orientation.
- The 18-case center-conditioned count table is not the same schema as the ten-case equal sum of all nine values, and neither is the arbitrary 512-context positional table.
- Game of Life, other outer-totalistic presets, weighted/partitioned diagonal rules, block rules, stochastic rules, properties, growth shapes, and biological analogies remain typed presets/relations/observers unless strict T22 evidence imports them.
- A pattern that stops growing may still update to an unchanged successor. No fixed point or bounded picture silently becomes native halt.

## Big Picture Objective

Reconstruct Moore-neighborhood cellular automata from primary evidence and prove whether T22 is exactly the T21/T01 fixed-lattice CA preset with eight surrounding offsets and source-pinned RULE schemas. Produce an implementation-ready Goal 2 handoff without a Moore state class, executor, update law, hidden center, implicit boundary, or `dyadaxes_2d` semantic shortcut.

## Catalog Identity

- Stable ID: T22.
- Exact catalog name: Moore-Neighborhood Cellular Automata.
- CSV line: 23.
- Taxonomy section: 22.
- Entry kind: fixed-support synchronous local transition construction; expected neighborhood/RULE parameterization pending evidence closure.
- Initial vocabulary: Moore neighborhood, nine-neighbor/9-neighbor square, eight neighbors, diagonals, immediate and diagonal neighbors, outer totalistic, totalistic, growth totalistic, code 175850, code 746, code 174826, Game of Life, rough surface, circle, rows of black cells, periodic boundary, symmetry, Notes implementation, actual Index.

## Search Log

The exhaustive source and asset fixed-point oracles are in progress. No final count, digest, or zero-remainder claim is made yet.

## Initial Book Excerpts

### Excerpt 1 — eight surrounding neighbors including diagonals

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:2212-2218`
- Establishes: strict T22 changes the surrounding access set to eight cells and keeps the old center as a separate rule input.

> exactly three of its eight neighbors—including diagonals—are black, and otherwise it should stay the same color as it was before

### Excerpt 2 — named codes and independent seeds/horizons

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:2226-2234`
- Establishes: codes `175850`, `746`, and `174826` use the eight-neighbor center-conditioned convention; row lengths and step counts are run data; roughness, circularity, growth, and stopping are observations.

### Excerpt 3 — direct 18-case implementation

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13475-13481`
- Establishes: neighbor weight `2`, self weight `1`, and an 18-digit binary table implement the direct nine-position profile.

```text
ListConvolve[{{2,2,2},{2,1,2},{2,2,2}}, a, 2]
IntegerDigits[code, 2, 18]
```

### Excerpt 4 — the 512/18/10 schema split

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:13534-13549`
- Establishes: general positional, outer-totalistic, equal-sum totalistic, symmetry-reduced, and growth rules are distinct restrictions/representations over the same nine declared positions.

## Construction Model

- DOMAIN: expected discrete `t+2D` reuse.
- Configuration/support: expected total finite-alphabet field on fixed square-grid `Z^2`; finite realizations explicit.
- ALPHABET: expected binary strict profiles over the reusable finite alphabet axis.
- FRONTIER: expected `AllSites` direct reuse.
- NEIGHBORHOOD: expected explicit composition of one Self plus eight ordered Moore offsets.
- RULE: expected distinct complete 512-context positional, 18-case `SelfValue x MooreCount`, and ten-case self-plus-eight sum schemas; exact source code order must be frozen.
- UPDATE: expected one same-site assignment per source under old-snapshot parallel commit.
- Successor: expected one deterministic configuration; fixed points do not imply halt.
- Seed/realization: exact configurations, constructors/laws, boundary/work/horizon/viewport remain separate.
- Observers/relations: shapes, outlines, radius fits, growth stops, classes, Life structures, applications, histories, and renderings do not feed execution.

## First-Principles Fit Standard

The `src/ca` namespace and its Phase 1 fixed-lattice implementation do not define the library's semantic boundary. The intended library is the common SimpleProgram algebra reconstructed from the Book. Catalog names identify evidence obligations and presets; they never select runtime families.

T22 therefore passes by **native axis instantiation**, not merely because a Moore rule can be encoded in some cellular automaton. The required proof is that its complete configuration and one native event are already expressed by the shared axes:

```text
AllSites.select(X)
    -> (SelfAt + eight declared offsets).read(X, active)
    -> closed table writes one complete label per active site
    -> SnapshotParallelSameSite.apply(X, active, writes)
```

No hidden interpreter, microstep simulation, family test, alternate trace clock, or opaque whole-program packing occurs. A new closed implementation of an existing axis can be justified by evidence, but it remains an axis implementation. A new top-level semantic class or runner requires a concrete counterexample showing that the common protocol cannot retain T22's complete state and one-step semantics. No such counterexample is presently visible.

## Direct Named-Code Reconstruction

For binary outer-totalistic T22 rules, let `s in {0,1}` be the old center and `n in {0,...,8}` the number of black surrounding cells. The Notes convolution assigns self weight `1` and every surrounding cell weight `2`, so the table address is

```text
j = 2*n + s
output = bit_j(code)
```

This makes the prose/code relation inspectable rather than a family convention:

- The rule “stay unchanged except become black at neighbor counts 3 or 5” sets every odd bit `j=2*n+1` and also bits `6` and `10`: `174762 + 64 + 1024 = 175850`.
- The rule “stay unchanged except become black at count 3” sets every odd bit and bit `6`: `174762 + 64 = 174826`.
- Code `746` sets both count-3 bits `6,7` and the old-black bits for counts `0,1,2,4`, namely `1,3,5,9`: `64+128+2+8+32+512 = 746`. Thus count 3 becomes black, counts 0/1/2/4 retain self, and counts 5 through 8 become white.

The semantic oracle must derive these values independently and reject swapped center/count significance, digit reversal, a hidden-center convention, and accidental agreement on symmetric fixtures.

## Current Runtime/API Fit Audit

- `src/ca/neighborhoods.py:572-593` already constructs the radius-one `L_infinity` shell as the eight-cell Moore access. `compose((self_at(), moore()))` therefore preserves the exact two semantic input roles needed by the 18-case table without a T22 neighborhood class.
- `src/ca/neighborhoods.py:717-741` exposes the same nine raw positions as explicit self, four cardinals, and four diagonals. This is a lossless regrouping of geometry, but `src/ca/rules.py:472-493` majority-gates the two four-cell groups before lookup. That `dyadaxes_2d` RULE discards exact counts and positional information, so it is not a canonical T22 rule preset.
- The current rule-channel machinery can describe an exhaustive self channel plus an eight-cell count channel, and its mixed address `self + 2*count` matches the Notes. The current rollout nevertheless accepts spatial execution only for three named Dyadrads/Dyadaxes families (`src/ca/rollout.py:166-174,201-213`). Goal 2 must execute the closed channel/table specification generically; adding a `moore` family branch would preserve the defect.
- The Book's arbitrary positional rule orders its nine offsets lexicographically and treats the first position as the most-significant context digit (`BOOK:13491-13531`). The current exhaustive channel assigns its first gathered value the least-significant weight (`src/ca/rollout.py:750-759`). Goal 2 needs one explicit order/codec correction or table permutation, shared with T01/T21, not a T22 reversal shim.
- Scalar Python integers can hold a 512-bit general-rule code, but the batch path normalizes rule IDs to `numpy.int64` (`src/ca/rollout.py:264-274`). Complete typed tables or arbitrary-precision tagged codecs are the semantic representation; machine-width batch IDs are a realization limit, not a reason to shrink the rule family.
- Current fixed `shape`, boundary, dense arrays, canonical coordinates, and rasters are finite computation/trace realizations. They do not replace native square-grid support, the chosen exterior/background law, or the complete mathematical configuration.

## Audit Questions

1. Does any T22 evidence alter CONFIGURATION, FRONTIER, RULE result, UPDATE, successor cardinality, or outcome semantics rather than only access/RULE data?
2. What is the exact Book order of the nine raw positions, and how must it permute under the Book-row/column-to-ENU basis map?
3. Do named codes reconstruct exactly from their prose predicates under index `2 * MooreCount + SelfValue`?
4. Which rasters are strict fixtures, observers, T21/T23/T24 controls, Life relations, or mere adjacency candidates?
5. Does the current Dyadaxes access preserve all nine raw values, and where does its majority-gated RULE lose the Moore count or positional context?
6. Are finite periodic/fixed realizations and evolving backgrounds represented losslessly without becoming native support semantics?
7. Can every qualifying compact table expand/factor through the same `ClosedLocalMap`, with adversaries rejecting invalid quotients?
8. Is T23's 3D access a dimensional parameterization boundary and not a reason for another runner?

## Detailed Implementation Plan

1. Freeze direct/alias/mechanics/Notes/actual-Index/split source closure with explicit T21/T23/T24/Life controls and zero unresolved candidates.
2. Derive the complete source-bound asset candidate set, classify every governed/adjacent plate, bind metadata, and replay only source-determined fixtures.
3. Build an independent semantic oracle for direct 18-case codes, ten-case sums, positional order/basis permutation, and the generic Self-plus-eight access.
4. Audit current documents/modules/tests and D004-D008, D111-D121, and D127 from first principles.
5. Add D128 only if evidence warrants a T22 boundary; specify the smallest Goal 2 composition and conformance matrix.
6. Obtain final hostile review and run root/`/tmp`/optimized/import/compile/Markdown/diff/scope/status/test gates.

## Candidate Goal 2 Composition

```text
Domain        = DiscreteSpace(dimension=2)
Configuration = FixedLattice(SquareGrid(Z^2), Alphabet)
Frontier      = AllSites
Neighborhood  = Compose(
                    Offset(-1,-1), Offset(-1,0), Offset(-1,1),
                    Offset(0,-1), SelfAt, Offset(0,1),
                    Offset(1,-1), Offset(1,0), Offset(1,1))
Rule          = OrderedContextTable
              | ProductCaseTable(SelfValue, MooreCount)
              | SumCaseTable(SelfPlusMooreNeighbors)
Update        = SnapshotParallelSameSite
Seed          = IndependentValidatedConfiguration
```

This composition is a hypothesis to test, not a family API mandate. Public spelling remains a synthesis choice.

## No-Cheating Checks

- No `moore`, `nine_neighbor`, Life, or T22 rollout branch or executor.
- No hidden center read, flattened memory-order codec, or diagonal deduplication.
- No untagged interchange of 512-context, 18-case, and ten-case rule numbers.
- No symmetric/count-only fixture used as proof of positional orientation.
- No Dyadaxes majority gate substituted for an exact neighbor count or positional table.
- No finite tensor, periodic boundary, crop, palette, or raster presented as native `Z^2` semantics.
- No growth stop, circle fit, behavior class, Life structure, or application fed back into execution.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] Source-bound asset fixed point closes without pixel or random-replay overclaims.
- [ ] Exact Moore access, three RULE schemas, named codes, and orientation mappings are proven.
- [ ] Smallest reusable base is classified without a family executor or duplicate UPDATE.
- [ ] Current API/runtime/principles audit and Goal 2 handoff are implementation-ready.
- [ ] Independent hostile review and all oracle/test/Markdown/diff/scope/coverage gates pass.
- [ ] `0-plan.md`, `evidence-index.md`, `design-ledger.md`, and `architecture-audit.md` agree.

## Stage Results

In progress.
