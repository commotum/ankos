# 42-T35-PIECEWISE-INTEGER

Status: **IN PROGRESS — FIRST-PRINCIPLES ARCHITECTURE RECONSTRUCTED; EVIDENCE ORACLES PENDING**

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

`42-T35-source-oracle.py` will be the fail-closed textual evidence record. It must close the whole-number/parity construction, exact A/B formulas, seeds, prefixes, cycles, event-count convention, standard `3n+1`, negative/signed variants, empirical-versus-proved claims, stopping-time rules, CA compiler, parity reconstruction, reversible system, general modulus tables, register encoding, ordered Conway fractions, current-family boundaries, assets, actual Index, split reverse provenance, and extraction defects.

Known source hazards requiring guarded disposition include the page-122 extracted parity bit string, missing punctuation in the reconstruction code, damaged pattern underscores in `ASEvolveList`, the apparent `Table`/`Product` register-encoding conflict, and badly corrupt Turing/number-theory text near `BOOK:19460`. None may be silently repaired into executable semantics.

Final query counts, retained N/R/C partition, exclusions, reverse provenance, source-model digest, image interface, oracle SHA, and unresolved total are pending the independent source audit.

## Asset Audit

`42-T35-asset-oracle.py` will bind the exact native/relation/control/excluded raster universe, monolith/split references, hashes, bytes, dimensions, assemblies, and evidence boundary. Expected native candidates include the page-122 digit evolution, page-123 multi-seed profiles, page-124 seed-6 trajectory, and Notes stopping-time/reversible plates. Register-machine, general arithmetic, Conway, T34, and T36 plates require explicit relation/control/exclusion disposition.

No raster may supply an untranscribed formula, rule row, seed, trace, palette, cycle, stopping-time result, branch order, or numeric codec. Final governed counts, ledger/oracle SHAs, transcription boundary, assemblies, and unrecovered visual facts are pending the independent asset audit.

## Construction Model

The source-faithful strict normal form is closed data:

```text
ResidueIntegerMap = {
    modulus: PositiveInteger,
    rows: TotalMap[{0,...,modulus-1}, ClosedIntegerExpr],
    state_invariant: IntegerSubset,
    closure_evidence: ReplayableValidation,
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

For an affine quotient row `(a*n+b)/d` declared on `n = r mod m`, exact closure over the full residue class follows from `d | a*m` and `d | a*r+b`. More general closed expressions require their own complete validator/certificate; a host callback is not a substitute.

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

An ordered fraction system instead selects the first fraction `p/q` for which `q` divides the old integer. Order is behaviorally material. A finite ordered list can be compiled intensionally to a first-applicable decision over residues modulo the LCM of reduced denominators while retaining the selected-fraction witness, but materializing billions of rows is neither required nor desirable. Any such compilation must commute exactly and preserve the partial no-applicable outcome. The Book's implementation does not define that generic outcome, so Goal 2 must not invent halt, identity, or error as native source semantics.

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
- partial no-applicable outcome kept distinct from halt/identity;
- observer/analyzer and compiler/relation separation;
- generalized modulus/alphabet/invariant validation; and
- absence of T35-specific state, frontier, neighborhood, UPDATE, or executor fields.

Final commutation counts, trace/check totals, semantic digest, hostile controls, and oracle SHA are pending the independent semantic audit.

## Architecture Classification

| Responsibility | Classification | Smallest reusable construction | T35 delta |
|---|---:|---|---|
| DOMAIN/configuration | 1/2 | T34 discrete `t+0D` exact scalar | restrict carrier to declared integer subset |
| FRONTIER/NEIGHBORHOOD | 1 | T34 `UniqueScalar` + self read | none |
| Closed expression syntax | 1/3 | T43 closed unary/piecewise AST responsibility | exact integer residue predicates and quotient nodes |
| RULE selection | 2/3 | complete finite key-indexed closed RULE data | residue-key constructor, direct lookup, branch witness |
| RULE result/UPDATE | 1 | T34 same-locus assignment + atomic update | none |
| Trace/outcomes | 1/2 | T34 scalar trace and generic outcomes | retain selected-row witness; partial fraction sibling explicit |
| Seeds/invariants | 2 | T08/T34 configuration validation | positive strict profile; natural/signed siblings tagged |
| Ordered fraction sibling | 2/3 | same unary event + first-applicable closed rule schema | order-sensitive selection; no new executor |
| Observers/relations | 1 | existing analyzer/relation boundaries | source-bound presets only |

Every native strict T35 delta is categories 1–3. No concrete counterexample requires a new execution algebra: one old scalar is read, one exact scalar is written, and the T34 atomic unary event advances.

## Current Runtime Fit and Smallest Goal 2 Delta

The checked-in runtime recognizes `t+0d` mechanically but remains finite-alphabet, `numpy.int64`, rectangular-array, callback-adjacent, and family-dispatched. Those are implementation gaps in the current realization, not evidence for a T35 family:

1. Generalize the shared exact scalar carrier/serialization to arbitrary-precision integers without `numpy.int64` coercion.
2. Add closed integer AST nodes such as constants, state reference, exact affine quotient, Euclidean modulo/residue equality, and validated total residue lookup. Reuse compatible T43 expression syntax; do not accept host callbacks.
3. Add construction-time totality, unique-residue, invariant, and integer-closure validation with replayable evidence.
4. Reuse T34 `UniqueScalar`, self access, assignment, atomic UPDATE, event result, and `h+1` trace; attach branch witnesses to events.
5. Add named A/B/Collatz presets, source examples, and conformance fixtures separately from seeds and observers.
6. Represent ordered fraction systems as an order-preserving closed RULE schema or certified intensional compilation on the same event. Keep no-applicable behavior explicitly partial until evidence resolves it.
7. Add no `PiecewiseIntegerState`, T35 executor, rollout branch, callback, hidden digit/register/history state, implicit finite width, or branch-set successor.

## No-Cheating Checks

- No T35 class or executor merely because the source says “system based on numbers.”
- No digit array used as native state; carries/nonlocal digit dependence are reasons not to do so.
- No `numpy.int64`, float division, truncation, sampled closure, or JSON-number identity.
- No callback `If`/predicate evaluator; program syntax is closed structural data.
- No precedence, overlap, fallback, or row order invented for complete residue tables.
- No Conway/FRACTRAN list order erased by unordered residue compilation.
- No no-applicable fraction silently called halt, identity, or invalidity without source evidence.
- No fixed point/cycle/stopping threshold promoted to native halt.
- No observer value, digit image, parity trace, stopping-time table, or empirical claim used as RULE semantics.
- No source bit string trusted when it conflicts with formula/prefix chronology without raster alignment.
- No `Table`/`Product`, damaged Blank, or corrupt Turing formula silently repaired.
- No current scalar claimed to contain its seed/history.
- No register/CA/continuous encoding presented as native T35 identity without a complete commuting map.

## Completion Requirements

- [ ] Every direct/alias/mechanics search, Notes item, actual Index route, continuation, split witness, image link, and false positive is dispositioned with zero unresolved mechanics.
- [ ] A/B/Collatz formulas, seeds, exact prefixes, cycles, event counts, source claims, and empirical qualifications are closed.
- [ ] General residue maps and ordered fraction systems have distinct exact selection/partiality semantics.
- [ ] Source defects and the raster transcription boundary fail closed.
- [ ] The governed asset universe is exact and hash-bound.
- [ ] Direct/generic events, arbitrary precision, closure, invariants, traces, witnesses, cycles, order, and hostile cases commute.
- [ ] T34/T43 reuse and the smallest Goal 2 delta are implementation-ready without a T35 state/update/executor branch.
- [ ] Stage, plan, evidence index, design ledger, and architecture audit are synchronized under the next decision.
- [ ] Root/`/tmp`, optimized fail-closed, silent import, compile, tests, modes, Markdown, diff, scope, and fresh hostile review pass.

## Stage Results

Pending source, asset, semantic, runtime-fit, integration, and independent hostile-review closure.
