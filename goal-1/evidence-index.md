# Goal 1 Evidence Index

This ledger is the authoritative coverage join between `ref/notes/CA-Types.csv`, the numbered taxonomy sections in `ref/notes/CA-Types.md`, Goal 1 evidence stages, and the eventual Goal 2 conformance obligations. `CA-Types.md` supplies search vocabulary only; book evidence must come from the canonical monolith.

## Status Vocabulary

- `PENDING`: the type stage has not begun.
- `IN PROGRESS`: the stage file exists but at least one completion requirement remains unproved.
- `REOPENED`: later evidence invalidated a completed conclusion and the stage must be re-derived.
- `COMPLETE`: every candidate match is resolved, all unique construction-relevant excerpts are recorded, the construction and variants are reconstructed, API/runtime/principles fits are audited, the Goal 2 handoff is implementation-ready, and global integration is current.

Only `COMPLETE` counts toward the 45-type coverage total. A search hit, a taxonomy summary, or a plausible API fit never changes status by itself.

## Evidence Record Contract

Each type stage must make the following auditable:

1. Exact CSV identity, taxonomy section, aliases, variants, examples, parameters, and cross-referenced systems.
2. Reproducible searches of `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`, including direct terms, captions, Notes, Index entries, and vocabulary discovered from cross-references.
3. Disposition of every candidate as included evidence, duplicate, followed cross-reference, or false positive, with no silent remainder.
4. Every unique construction-relevant excerpt verbatim with canonical path, exact line range, section context, and the fact it establishes.
5. Evidence-first construction reconstruction, current API/runtime comparison, principles audit, rejected shortcuts, no-cheating checks, and Goal 2 implementation/conformance handoff.
6. Re-integration into this ledger, `design-ledger.md`, and `0-plan.md`, including any reopened stage.

## Catalog Coverage

| ID | CSV line | Catalog type | Taxonomy section | Execution stage and file | Status | Searches / excerpts / unresolved candidates |
|---|---:|---|---:|---|---|---|
| T01 | 2 | Elementary Cellular Automata | 1 | `2-T01-ELEMENTARY.md` | COMPLETE | 8 search families; 23 excerpt groups; all split/Notes/Index/cross-reference candidates dispositioned; 0 unresolved |
| T02 | 3 | Multi-Color Nearest-Neighbor Cellular Automata | 2 | `21-T02-MULTICOLOR-CA.md` | PENDING | Not started |
| T03 | 4 | Totalistic Cellular Automata | 3 | `22-T03-TOTALISTIC-CA.md` | PENDING | Not started |
| T04 | 5 | Three-Color Totalistic Cellular Automata | 4 | `23-T04-THREECOLOR-TOTALISTIC.md` | PENDING | Not started |
| T05 | 6 | Higher-Color Totalistic Cellular Automata | 5 | `24-T05-HIGHERCOLOR-TOTALISTIC.md` | PENDING | Not started |
| T06 | 7 | Quiescent-Background-Preserving Cellular Automata | 6 | `25-T06-QUIESCENT.md` | PENDING | Not started |
| T07 | 8 | Left-Right Symmetric Cellular Automata | 7 | `26-T07-SYMMETRIC.md` | PENDING | Not started |
| T08 | 9 | Initial-Condition Classes | 8 | `27-T08-INITIAL-CONDITIONS.md` | PENDING | Not started |
| T09 | 10 | Mobile Automata | 9 | `3-T09-MOBILE.md` | COMPLETE | 19 direct query terms/families; 14 excerpt groups; 135 combined candidates plus targeted remainders/splits dispositioned; 0 unresolved |
| T10 | 11 | Extended Mobile Automata | 10 | `28-T10-EXTENDED-MOBILE.md` | PENDING | Not started |
| T11 | 12 | Generalized Mobile Automata | 11 | `29-T11-GENERALIZED-MOBILE.md` | PENDING | Not started |
| T12 | 13 | Turing Machines | 12 | `4-T12-TURING.md` | COMPLETE | 278 direct-name lines plus all 74 halt lines/parameter/Notes/Index/split/emulation candidates dispositioned; 16 excerpt groups; 0 unresolved |
| T13 | 14 | Neighbor-Independent Substitution Systems | 13 | `5-T13-PARALLEL-SUBSTITUTION.md` | COMPLETE | 288 direct-name lines plus definition/replacement/alias/Notes/Index/split/rendering/growth/infinite/stochastic/emulation candidates dispositioned; 26 excerpt groups; 0 unresolved |
| T14 | 15 | Neighbor-Dependent Substitution Systems | 14 | `30-T14-CONTEXTUAL-SUBSTITUTION.md` | PENDING | Not started |
| T15 | 16 | Creation-Destruction Substitution Systems | 15 | `31-T15-CREATION-DESTRUCTION.md` | PENDING | Not started |
| T16 | 17 | Sequential Substitution Systems | 16 | `6-T16-SEQUENTIAL-SUBSTITUTION.md` | COMPLETE | 51 direct-name lines plus rule/position order, captions, Notes, aliases/history, Index/splits, stopping, overlap/confluence, finite-input, causal, generalized/multiway, and emulation routes dispositioned; 21 excerpt groups; 0 unresolved |
| T17 | 18 | Tag Systems | 17 | `7-T17-TAG.md` | IN PROGRESS | Direct mechanics/examples, Notes/Index/splits/history, deletion/append/halting variants, numbering, initial conditions, and emulations under audit |
| T18 | 19 | Cyclic Tag Systems | 18 | `32-T18-CYCLIC-TAG.md` | PENDING | Not started |
| T19 | 20 | Register Machines | 19 | `8-T19-REGISTER.md` | PENDING | Not started |
| T20 | 21 | Symbolic Systems | 20 | `9-T20-SYMBOLIC.md` | PENDING | Not started |
| T21 | 22 | Two-Dimensional Cellular Automata | 21 | `33-T21-2D-CA.md` | PENDING | Not started |
| T22 | 23 | Moore-Neighborhood Cellular Automata | 22 | `34-T22-MOORE-CA.md` | PENDING | Not started |
| T23 | 24 | Three-Dimensional Cellular Automata | 23 | `35-T23-3D-CA.md` | PENDING | Not started |
| T24 | 25 | Higher-Dimensional Lattice Cellular Automata | 24 | `36-T24-HIGHERDIM-CA.md` | PENDING | Not started |
| T25 | 26 | Two-Dimensional Turing Machines | 25 | `37-T25-2D-TURING.md` | PENDING | Not started |
| T26 | 27 | Two-Dimensional Substitution Systems | 26 | `38-T26-2D-SUBSTITUTION.md` | PENDING | Not started |
| T27 | 28 | Geometric Replacement And Fractal Systems | 27 | `10-T27-GEOMETRIC.md` | PENDING | Not started |
| T28 | 29 | Neighbor-Dependent Two-Dimensional Substitution Systems | 28 | `39-T28-CONTEXTUAL-2D-SUBSTITUTION.md` | PENDING | Not started |
| T29 | 30 | Network Systems | 29 | `11-T29-NETWORK.md` | PENDING | Not started |
| T30 | 31 | Multiway Systems | 30 | `12-T30-MULTIWAY.md` | PENDING | Not started |
| T31 | 32 | Local Constraint Systems | 31 | `13-T31-CONSTRAINTS.md` | PENDING | Not started |
| T32 | 33 | Template Constraint Systems | 32 | `40-T32-TEMPLATE-CONSTRAINTS.md` | PENDING | Not started |
| T33 | 34 | Seeded Template Constraint Systems | 33 | `41-T33-SEEDED-CONSTRAINTS.md` | PENDING | Not started |
| T34 | 35 | Arithmetic Iteration Systems | 34 | `14-T34-ARITHMETIC.md` | PENDING | Not started |
| T35 | 36 | Piecewise Integer Maps | 35 | `42-T35-PIECEWISE-INTEGER.md` | PENDING | Not started |
| T36 | 37 | Digit-Reversal Arithmetic Systems | 36 | `43-T36-DIGIT-REVERSAL.md` | PENDING | Not started |
| T37 | 38 | Recursive Sequences | 37 | `15-T37-RECURSIVE.md` | PENDING | Not started |
| T38 | 39 | Variable-Index Recursive Sequences | 38 | `44-T38-VARIABLE-RECURRENCE.md` | PENDING | Not started |
| T39 | 40 | Number-Theoretic Filtering Systems | 39 | `16-T39-FILTERS.md` | PENDING | Not started |
| T40 | 41 | Mathematical-Constant Digit Systems | 40 | `45-T40-CONSTANT-DIGITS.md` | PENDING | Not started |
| T41 | 42 | Function-Combination Systems | 41 | `17-T41-FUNCTIONS.md` | PENDING | Not started |
| T42 | 43 | Continued-Fraction-Driven Substitution Systems | 42 | `46-T42-CF-SUBSTITUTION.md` | PENDING | Not started |
| T43 | 44 | Iterated Maps | 43 | `18-T43-ITERATED-MAPS.md` | PENDING | Not started |
| T44 | 45 | Continuous Cellular Automata | 44 | `19-T44-CONTINUOUS-CA.md` | PENDING | Not started |
| T45 | 46 | Partial Differential Equation Systems | 45 | `20-T45-PDE.md` | PENDING | Not started |

## Coverage Summary

- Foundation: complete in `1-FOUNDATION.md`.
- Type stages complete: 5 / 45.
- Type stages reopened: 0.
- Type stages unresolved: 39 pending, 1 in progress.
- Synthesis: pending.
- Goal 2 handoff: pending.

## Reopened-Stage Log

None at Foundation start. Add an entry here whenever later evidence invalidates a completed stage; do not erase the prior conclusion or silently downgrade it.
