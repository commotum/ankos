# 42-T35-PIECEWISE-INTEGER

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, D136 ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED**

## Current Facts

- T35 is CSV physical line 36, `Piecewise Integer Maps`; the exact catalog phrase does not occur in the Book, so the taxonomy section is search vocabulary rather than primary mechanics.
- The strict main systems keep one whole number and apply one parity-selected arithmetic expression at every step (`BOOK:1497-1529`). They are ordinary unary `t+0D` transitions, not digit lattices, branch sets, or hidden-history recurrences.
- The page-122 rule is `A(n) = 3n/2` for even `n` and `3(n+1)/2` for odd `n`; seed `1` yields the exact printed prefix `1,3,6,9,15,24,36,54,81,123,186,279,420,630,945,1419,2130,3195,4794` (`BOOK:1499-1507`).
- The page-123 rule is `B(n) = 5n/2` for even `n` and `(n+1)/2` for odd `n`; seed `1` is fixed, while other positive seeds can be periodic or apparently grow irregularly (`BOOK:1513-1529`).
- The exact Notes implementation uses `NestList`, so `h` applications produce `h+1` scalar states (`BOOK:12598`). Fixed points and cycles still execute events; they do not natively halt.
- The source-backed normal form computes `Mod[n,m]` and selects one residue-owned arithmetic expression. The Notes explicitly encode page 122 as `{2,{0 -> 3#/2, 1 -> 3(#+1)/2}}` (`BOOK:8086-8100`, `18626-18646`). Complete residue tables are disjoint direct lookup and have no row precedence.
- Arithmetic expressions read the complete old integer. Digit rows, parity strings, logarithmic size, stopping times, cycles, randomness approximations, prime observations, and register/CA/continuous encodings are observers, analyses, or relations—not native configuration components.
- T34 already owns the discrete `t+0D` singleton configuration, `UniqueScalar` frontier, self read, same-locus assignment, atomic update, exact scalar trace, and arbitrary-precision serialization responsibility. T35 adds closed integer predicate/expression data and validation, not a state, UPDATE, executor, or family branch.
- T43's closed predicate/piecewise-expression syntax is reusable by responsibility, but T35 retains a typed exact-integer carrier and mechanically checked integer closure. A numeric union must not erase this invariant.
- Conway fraction systems use ordered first-applicable selection, `First[Select[fracs n,IntegerQ,1]]` (`BOOK:18648-18664`). That is a separately tagged ordered unary RULE schema or compilation relation, not precedence semantics for canonical residue tables. The generic no-applicable outcome is not source-defined and must remain explicitly partial rather than silently called halt.
- The main text's contrast with cellular automata is specifically that digit-level arithmetic is usually nonlocal (`BOOK:1531-1539`). It changes the native ALPHABET/configuration and NEIGHBORHOOD choice—a complete scalar read rather than a local digit stencil—not the shared SimpleProgram runner or execution algebra.

## Updated Assumptions

- **Retained:** strict main configurations are positive arbitrary-precision integers; natural and signed carriers are explicit sibling profiles. “Whole number” does not silently settle zero or signed seed semantics.
- **Retained:** direct residue tables contain exactly one row for every residue `0..m-1`; duplicates or omissions are invalid, and Euclidean `Mod` is explicit for signed extensions.
- **Retained:** exact affine quotient rows `(a*n+b)/d` require a proof of integer closure on their declared residue. Float division, truncation, or sampled closure is invalid.
- **Retained:** a branch witness records modulus, residue, selected row, old integer, and exact result in the event report. It is not semantic state or a second successor.
- **Rejected:** `PiecewiseIntegerState`, digit-array native state, implicit `numpy.int64`, callback RULEs, branch-as-multiway semantics, precedence among complete residue rows, history in the current scalar, cycle-as-halt, observer-dependent execution, or a T35 rollout branch.

## Big Picture Objective

Reconstruct T35 as a closed complete residue-indexed unary integer RULE representation over T34's shared scalar SimpleProgram event. Close the two main maps, standard `3n+1`, exact seeds/prefixes/cycles, general residue arithmetic systems, register/CA/continuous relations, reconstruction/reversible variants, ordered fraction-system sibling, observers, assets, Notes/Index/splits, extraction defects, arbitrary-precision runtime fit, and Goal 2 handoff. Prove exactly which pieces are reuse, restriction, representation, or genuinely new execution algebra.

## Catalog Identity

- Stable ID: T35.
- Exact CSV name: Piecewise Integer Maps.
- CSV physical line: 36.
- Taxonomy section: 35.
- Canonical main core: `BOOK:1497-1541`.
- Native Notes core: `BOOK:12598-12633`.
- General arithmetic-system core: `BOOK:8086-8100`, `18626-18664`.
- Entry kind: deterministic exact unary integer transition with a closed residue-selected RULE representation.
- Strict DOMAIN: discrete `t+0D`.

## Source Audit

`42-T35-source-oracle.py` is the frozen fail-closed textual evidence record. Its 43 redundant query lanes produce a 104-line union at `70 pre-Index / 34 actual Index`. It retains 127 lines partitioned `46 native / 63 relation / 18 control`, including 64 governed continuations, excludes seven false positives, routes the 34 Index rows as `20 core/observer / 10 arithmetic-emulation / 4 ordered-fraction`, and leaves zero unresolved mechanics. Seven independent broad Index lanes reproduce exactly the same 34-row boundary rather than merely partitioning whatever the main queries happened to find. The source-model record has 41 clauses and digest `6cdc79d6a8e7b149afd4d45843fa8ecb212b8f769c72ffff4928255ce656b2bc`.

Known source hazards requiring guarded disposition include the page-122 extracted parity bit string, missing punctuation in the reconstruction code, damaged pattern underscores in `ASEvolveList`, the apparent `Table`/`Product` register-encoding conflict, and badly corrupt Turing/number-theory text near `BOOK:19460`. None may be silently repaired into executable semantics.

The split reverse join is a complete 104-record bijection to all monolith query hits: `85 exact + 10 image-basename + 9 normalized`. It explicitly maps the two identical monolith `Recursive Sequences` headings to different structural owners instead of using global text membership. All 127 retained records independently close at `98 exact + 13 image-basename + 16 normalized`, with minimum normalized score `0.991511`. Three Index-only context routes point to 26 general-locality or upstream multiregister lines that remain explicitly out-of-scope related controls rather than silently entering T35 mechanics; those targets independently reverse-close to 26 exact structural split owners under crosswalk digest `504f98c258c8d461384cc0c1c8a2e18f52583d51e7b842767ffda5274660085e`. Flattened Index rows are owner-guarded: `BOOK:20946` belongs to `Carry digits`, not nearby `Ceiling`, and `BOOK:21360`'s `of integers, 122` belongs to `Iterated maps`, not intervening `Join` text. The candidate image interface is 24 files = 13 governed (`5/5/3`) + 11 exclusions and matches the asset oracle; all 26 referenced files, including two explicitly outside that candidate boundary, are independently path/size/SHA-bound under manifest digest `21580ddc004136889d5d6aa6d3e26df42bd375924b4e391ae55b048e56f758b3`. The catalog/taxonomy phrase remains search vocabulary absent from the primary Book; five Atlas hits are summary-only. The oracle SHA is `af06b40b5e35fe97a97b58ad148336c7e9884029d2785a4186f4456e39de6108`.

## Asset Audit

`42-T35-asset-oracle.py` binds an exact 24-image candidate universe: 13 governed assets partition `5 native / 5 relation / 3 control`, and 11 adjacency assets are physically bound exclusions. The governed ledger closes 26 references (13 monolith plus 13 split), 13 distinct hashes, 832,651 bytes, and two assemblies/four files; the excluded ledger independently closes 22 references, 11 hashes, 1,994,355 bytes, and two assemblies. The governed ledger SHA is `0d7fd98dea61d513b7d4a0c795e4fef7958e7e24f13f844bfada294eadae288a`; the excluded-ledger SHA is `3c8501aa32306e4134a0197d4d359c30ada6752cbf6b1dbacb73817e9111c206`; the oracle SHA is `c618c25202a496fc9f3cdac94fe748dbf2183c72932a72e10dd7b9dab249fb23`.

All 13 governed assets are `HASH_BOUND`; none is `LIMITED_TRANSCRIBED` or `PIXEL_REPLAYED`. No raster supplies an untranscribed formula, rule row, seed, trace, palette, cycle, stopping-time result, branch order, or numeric codec. Page-122/123 formulas, printed sequence values, Notes rules, register correspondence, and Conway order remain source-text evidence rather than pixel transcriptions. The source/asset image interface matches exactly and leaves zero unresolved image dispositions.

## Construction Model

The source-faithful strict normal form is closed data:

```text
ResidueIntegerMap = {
    modulus: PositiveInteger,
    rows: TotalMap[{0,...,modulus-1}, ClosedIntegerExpr],
    state_invariant: IntegerSubset,
    integer_closure_evidence: ReplayableValidation,
    carrier_invariance_evidence: ReplayableValidation,
}
```

Operationally, it reuses the shared unary event:

```text
active  = UniqueScalar.select(state)
n       = Self.read(state, active)
r       = EuclideanMod(n, program.modulus)
value   = ExactEval(program.rows[r], n)
writes  = Assign(active, value)
next    = AtomicAssign.apply(state, active, writes)
```

`ResidueIntegerMap` is a named closed RULE constructor or schema, not a top-level state class or executor. The strict maps are:

```text
A = modulus 2:
    0 -> (3*n    ) / 2
    1 -> (3*n + 3) / 2

B = modulus 2:
    0 -> (5*n    ) / 2
    1 -> (1*n + 1) / 2

Collatz = modulus 2:
    0 -> (1*n    ) / 2
    1 -> (3*n + 1) / 2
```

For an affine quotient row `(a*n+b)/d` declared on `n = r mod m`, exact integer closure over the full residue class follows from `d | a*m` and `d | a*r+b`. This does not by itself prove preservation of a positive, natural, or otherwise restricted state carrier; carrier invariance is a separate obligation. More general closed expressions require their own complete validator/certificate for both obligations; a host callback or bounded sample is not a substitute.

The strict main seed profile is positive integers. A natural profile must decide and record zero explicitly; a signed profile must declare Euclidean remainder semantics and validate its invariant. Program identity, seed identity, and trace identity remain separate.

### Event and trace semantics

Each valid event returns one same-locus integer assignment and one successor. A branch witness is report data:

```text
ResidueBranchWitness = {
    program_id,
    old_value,
    modulus,
    residue,
    row_id,
    exact_result,
}
```

It is rechecked against structural program data. An `h`-event run contains `h+1` scalar states. Fixed points still produce `Advanced(changed=false)` events; cycles repeat states while continuing. Requested horizons, stopping-time queries, resource limits, and externally chosen cycle stops are not native halting.

The scalar state does not contain its history. `A(1)=A(2)=3` is a concrete information-loss witness: the current value cannot recover the prior seed or trace without external provenance. T37's growing prefix is therefore not T35 state.

### Exact examples and invariants

- `A`, seed `1`: `1,3,6,9,15,24,36,54,81,123,186,279,420,630,945,1419,2130,3195,4794`.
- `B`, seed `1`: fixed point with an event at every step.
- `B` cycle through `2`: `2,5,3`.
- `B` cycle through `4`: `4,10,25,13,7`.
- `B` cycle through `40`: `40,100,250,625,313,157,79`.
- `B`, seed `6`, begins `6,15,8,20,50,125,63,32,80,200,500,1250,3125,1563,782,1955,...`; raster continuation and the million-step digit claim remain evidence/observer obligations, not RULE data.

### Complete residue lookup versus ordered fractions

A complete residue table computes one canonical key and performs direct lookup. Its row order is serialization provenance only; there is no overlap or priority.

An ordered fraction system instead selects the first fraction `p/q` for which the reduced denominator `q` divides the old integer. Order is behaviorally material. A finite ordered list can be compiled intensionally to a first-applicable decision over residues modulo the LCM of reduced denominators while retaining the selected-list-index witness, but materializing billions of rows is neither required nor desirable. The lowering is behavior-preserving, not generally injective: shadowed, duplicate, or otherwise redundant source entries can denote the same transition, so the ordered source AST/provenance must remain attached whenever structural program identity is claimed. Any such compilation must commute exactly and preserve the partial no-applicable boundary. The Book's implementation leaves that generic case undefined. The shared runner therefore represents an attempted undefined step with its existing zero-successor `Error(reason=MissingBranch | UndefinedRuleAtState)` envelope, retaining the last complete configuration and committing no event. This evaluator result is not a source-native halt, identity step, or new T35 outcome class.

### Observers and relations

Parity sequences, digit renderings, logarithmic size, digit length, stopping times, cycle detection, growth fits, randomness approximations, primes selected from a Conway trace, and empirical search bounds are observers/analyzers. Base-6 cellular automata, register-machine arithmetic encodings, continuous polynomial emulations, reversible conjugacies, and Turing/number-theory constructions are explicit relations or siblings. They do not replace native T35 execution or justify digit state, hidden registers, or a second executor.

## Semantic Proof Requirements

`42-T35-semantic-oracle.py` must independently compare direct A/B/Collatz steps with a generic residue-indexed unary event over complete typed reports. Required coverage includes:

- exhaustive bounded parity/residue contexts and arbitrary-precision values;
- exact affine-quotient closure and rejection of nonintegral rows;
- Euclidean signed-modulo behavior as an explicit extension;
- exact source prefix, seed-6 prefix, fixed point, and period-3/5/7 cycles;
- `h` events to `h+1` states and changed-false advancement;
- branch-witness reverification and malformed/forged witness rejection;
- no precedence under complete direct residue lookup;
- scalar-history noninjectivity via `A(1)=A(2)`;
- ordered fraction first-applicable behavior and order-sensitive counterexamples;
- exact intensional residue compilation with selected-row witnesses where claimed;
- partial no-applicable evaluation represented through the common zero-successor `Error` envelope and kept distinct from halt/identity;
- observer/analyzer and compiler/relation separation;
- generalized modulus/alphabet/invariant validation; and
- absence of T35-specific state, frontier, neighborhood, UPDATE, or executor fields.

The frozen semantic oracle closes 65,588 Euclidean-remainder checks and 6,150 complete direct/generic A/B/standard-`3n+1` event commutations with 6,150 replayed residue witnesses. It covers 24 arbitrary-precision profiles up to 6,648 bits/2,002 decimal digits; all six row serializations of a three-residue table; the exact A and seed-6 B prefixes; 65 register-relation checks; seven exact source cycles; 200 fixed-point `Advanced` events including five explicit `changed=false` checks; 65 `h+1` trace checks; and three history-merging witnesses including the exact `A(1)=A(2)=3` case.

Every complete report is bound back to exact canonical structural program data, with SHA-256 retained only as derived display/cache metadata: 403 transition-event replays contribute to 14,621 total program-bound event replays; two cross-program events, two missing-branch errors, two stopped traces, and three horizon-zero/cross-program trace cases exercise exact-key rejection and retention. All six row serializations of the three-residue table canonicalize to one exact key, while four ordered-fraction source ASTs remain distinct and 64 behavior-identical shadowed checks retain structural identity. Ordered fractions close 100 branch witnesses, an order discriminator, six generic zero-successor `Error(MissingBranch)` results with the last complete state retained, a two-event-then-error trace, 1,004 lazy Conway residue/value checks, and the exact 8,068-event prime-prefix run. Conway's denominator LCM is 6,469,693,230 while the oracle materializes zero rows. A shadowed-row pair proves bare fraction lowering noninjective; the complete ordered source AST/provenance remains required. The oracle also closes 4,101 exact integer-locus cosine/A relations, separates the modulus-30 reachable invariant from positivity, rejects 370 forged witnesses and 68 hostile constructions, and finds no T35 frontier, neighborhood, UPDATE, or executor fields. Its semantic digest is `7424aae85ed4dc8ee7d2a53d2d93aba32c4b951f8265c6b3a5b9f9846dfc8ba9`; its file SHA is `0c7f7c5875ad54edc504ddc5f9e88b240db8463622ff91080c9aa1dd42e332c1`.

## Architecture Classification

| Responsibility | Classification | Smallest reusable construction | T35 delta |
|---|---:|---|---|
| DOMAIN/configuration | 1/2 | T34 discrete `t+0D` exact scalar | restrict carrier to declared integer subset |
| FRONTIER/NEIGHBORHOOD | 1 | T34 `UniqueScalar` + self read | none |
| Closed expression syntax | 1/3 | T43 closed unary/piecewise AST responsibility | exact integer residue predicates and quotient nodes |
| RULE selection | 2/3 | complete finite key-indexed closed RULE data | residue-key constructor, direct lookup, branch witness |
| RULE result/UPDATE | 1 | T34 same-locus assignment + atomic update | none |
| Trace/outcomes | 1/2 | T34 scalar trace and common `StepResult` outcomes | retain selected-row witness; undefined fraction step uses generic zero-successor `Error` |
| Seeds/invariants | 2 | T08/T34 configuration validation | positive strict profile; natural/signed siblings tagged |
| Ordered fraction sibling | 2/3 | same unary event + first-applicable closed rule schema | order-sensitive selection; no new executor |
| Observers/relations | 1 | existing analyzer/relation boundaries | source-bound presets only |

Every native strict T35 delta is categories 1–3. No concrete counterexample requires a new execution algebra: one old scalar is read, one exact scalar is written, and the T34 atomic unary event advances.

## Current Runtime Fit and Smallest Goal 2 Delta

The checked-in selectors already demonstrate the reusable geometry: `frontiers.time_slice(())` and `neighborhoods.self_at()` each select exactly `[0,0,0,0]`. `UniqueScalar` is therefore a named rank-zero role/preset, not a new FRONTIER or NEIGHBORHOOD type. The checked-in execution path nevertheless remains finite-alphabet, `numpy.int64`, rectangular-array, callback-adjacent, and family-dispatched. Those are implementation gaps in the current realization, not evidence for a T35 family:

1. Generalize the shared exact scalar carrier/serialization to arbitrary-precision integers without `numpy.int64` coercion.
2. Add closed integer AST nodes such as constants, state reference, exact affine quotient, Euclidean modulo/residue equality, and validated total residue lookup. Reuse compatible T43 expression syntax; do not accept host callbacks.
3. Add construction-time totality, unique-residue, exact integer-closure, and separately checked carrier-invariance validation with replayable evidence.
4. Reuse T34 `UniqueScalar`, self access, assignment, atomic UPDATE, event result, and `h+1` trace; attach branch witnesses to events.
5. Add named A/B/Collatz presets, source examples, and conformance fixtures separately from seeds and observers.
6. Represent ordered fraction systems as an order-preserving closed RULE schema or certified intensional compilation on the same event. Route no-applicable evaluation through the existing zero-successor `Error` envelope with no committed event; add no T35-specific outcome.
7. Add no `PiecewiseIntegerState`, T35 executor, rollout branch, callback, hidden digit/register/history state, implicit finite width, or branch-set successor.

## No-Cheating Checks

- No T35 class or executor merely because the source says “system based on numbers.”
- No digit array used as native state; carries/nonlocal digit dependence are reasons not to do so.
- No `numpy.int64`, float division, truncation, sampled closure, or JSON-number identity.
- No callback `If`/predicate evaluator; program syntax is closed structural data.
- No precedence, overlap, fallback, or row order invented for complete residue tables.
- No Conway/FRACTRAN list order erased by unordered residue compilation.
- No no-applicable fraction silently called halt, identity, or invalidity, and no T35-specific outcome class; use the generic partial-evaluation `Error` envelope.
- No fixed point/cycle/stopping threshold promoted to native halt.
- No observer value, digit image, parity trace, stopping-time table, or empirical claim used as RULE semantics.
- No source bit string trusted when it conflicts with formula/prefix chronology without raster alignment.
- No `Table`/`Product`, damaged Blank, or corrupt Turing formula silently repaired.
- No current scalar claimed to contain its seed/history.
- No register/CA/continuous encoding presented as native T35 identity without a complete commuting map.

## Completion Requirements

- [x] Every direct/alias/mechanics search, Notes item, actual Index route, continuation, split witness, image link, and false positive is dispositioned with zero unresolved mechanics.
- [x] A/B/Collatz formulas, seeds, exact prefixes, cycles, event counts, source claims, and empirical qualifications are closed.
- [x] General residue maps and ordered fraction systems have distinct exact selection/partiality semantics.
- [x] Source defects and the raster transcription boundary fail closed.
- [x] The governed asset universe is exact and hash-bound.
- [x] Direct/generic events, arbitrary precision, closure, invariants, traces, witnesses, cycles, order, and hostile cases commute.
- [x] T34/T43 reuse and the smallest Goal 2 delta are implementation-ready without a T35 state/update/executor branch.
- [x] Stage, plan, evidence index, design ledger, and architecture audit are synchronized under D136.
- [x] Root/`/tmp`, optimized fail-closed, silent import, compile, tests, modes, Markdown, diff, scope, and fresh hostile review pass.

## Stage Results

COMPLETE. The 43-query source audit closes 104 lines at `70 pre-Index / 34 actual-Index`, retains 127 at `46 native / 63 relation / 18 control`, excludes seven, reproduces all 34 Index routes at `20 core/observer / 10 arithmetic-emulation / 4 ordered-fraction`, reverse-closes query evidence at `85 exact + 10 image-basename + 9 normalized` and retained evidence at `98 exact + 13 image-basename + 16 normalized`, and leaves zero unresolved. Twenty-six Index-only context targets reverse-close to exact structural split owners; their page-730/page-1114 classes, three route mappings, and exact guard needles are independently frozen. All 26 referenced image files are path/size/SHA-bound. The source-model digest is `6cdc79d6a8e7b149afd4d45843fa8ecb212b8f769c72ffff4928255ce656b2bc`; source oracle SHA is `af06b40b5e35fe97a97b58ad148336c7e9884029d2785a4186f4456e39de6108`.

The asset oracle closes 13 governed assets at `5 native / 5 relation / 3 control` plus 11 exclusions, 26 governed references, 13 hashes, 832,651 bytes, two assemblies/four files, and `13 hash-bound / 0 limited-transcribed / 0 pixel-replayed`; its SHA is `c618c25202a496fc9f3cdac94fe748dbf2183c72932a72e10dd7b9dab249fb23`. The semantic oracle closes 65,588 Euclidean-modulo checks, 6,150 direct/generic commutations, 24 arbitrary-precision profiles up to 6,648 bits, 14,621 exact-program-bound event replays, exact source prefixes/cycles/fixed events, six generic missing-branch results, lazy ordered-fraction evaluation, the exact 8,068-event Conway run, 4,101 integer/cosine relation checks, and 68 hostile rejections. Its SHA is `0c7f7c5875ad54edc504ddc5f9e88b240db8463622ff91080c9aa1dd42e332c1`; digest is `7424aae85ed4dc8ee7d2a53d2d93aba32c4b951f8265c6b3a5b9f9846dfc8ba9`.

D136 classifies every strict T35 delta as categories 1-3: complete Euclidean-residue maps and separately tagged ordered first-applicable fraction lists are closed unary RULE schemas over T34's exact discrete `t+0D` singleton event. Integer closure, carrier invariance, reachable-subset invariance, and exact structural provenance remain distinct. Successful rows emit an ordinary same-locus assignment; missing fraction selection uses the common zero-successor `Error(MissingBranch)` envelope with no committed event. D064-D069/T34/T43 are clarified, no completed stage reopens, and no T35 state, FRONTIER, NEIGHBORHOOD, UPDATE, outcome class, executor, family branch, callback, hidden history, digit packing, or native cycle halt is added.

Canonical, explicit-book, and relocated oracle runs pass; optimized execution and bad usage fail closed; silent imports, in-memory compile, mode 644, Markdown, diff, scope, and all 102 repository tests pass. Independent hostile review is clean after proving that JPEG mutation, context-target reassignment, route-class reassignment, and weakened route needles each fail at the intended gate. Next: T36.
