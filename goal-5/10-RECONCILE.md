# 10-RECONCILE

## Discovery Freeze

Blind whole-book discovery is frozen before catalog or design comparison.

- Frozen raw leads: 1,563
- Frozen terminal statuses: 188 serious, 867 resolved, 508 weak
- Frozen mechanics candidates: 94
- Saturation result: zero new or unresolved construction leads

From this point forward, T01–T45 and design materials may affect catalog
dispositions and family naming, but they may not retroactively manufacture Book
evidence or candidates.

## Big Picture Objective

Reconcile every current catalog identifier against the frozen source-grounded
mechanics inventory, without treating catalog names as evidence of separate
families.

## Detailed Implementation Plan

- Locate and read the 45-row catalog and only the design evidence needed to
  interpret its rows.
- Review T01–T45 in three disjoint ranges.
- Give every identifier exactly one retain, alias, merge, split, retire, or
  repair disposition.
- Route every unmatched frozen candidate as a proposed addition, a semantic
  role, or a close exclusion.
- Record source-grounded integration obligations without modifying the catalog.

## Completion Requirements

- T01–T45 each appear exactly once.
- Every frozen candidate has an explicit catalog relationship.
- Additions and repairs have mechanical arguments and canonical sources.
- No discovery count changes after the freeze.

## Stage Results

- Reconciled all 45 rows exactly once against the frozen 94-candidate
  inventory. The existing rows yield 20 retained families, 16 retained
  presets, two aliases, two merges, two repairs, two retired semantic roles,
  and one split.
- Current catalog rows directly cover 23 candidates. Of the other 71, 49 are
  source-grounded candidate additions, 14 are mechanically covered by an
  existing family, and eight are close observer/interface/seed/compiler roles.
  Candidate additions remain candidates until family consolidation; this is
  not a proposal for 49 new public classes.
- Updated every serious row in `source-decision-matrix.csv` with its catalog
  action. Non-serious leads are explicitly outside catalog reconciliation.
- Discovery remained frozen: no lead, status, candidate, or source count
  changed.

| ID | Catalog row | Disposition | Candidates |
|---|---|---|---|
| T01 | Elementary Cellular Automata | retain-family | C090 |
| T02 | Multi-Color Nearest-Neighbor Cellular Automata | retain-preset | C090 |
| T03 | Totalistic Cellular Automata | retain-preset | C090 |
| T04 | Three-Color Totalistic Cellular Automata | retain-preset | C090 |
| T05 | Higher-Color Totalistic Cellular Automata | merge | C090 |
| T06 | Quiescent-Background-Preserving Cellular Automata | retain-preset | C090 |
| T07 | Left-Right Symmetric Cellular Automata | retain-preset | C090 |
| T08 | Initial-Condition Classes | retire-role | - |
| T09 | Mobile Automata | retain-family | C047 |
| T10 | Extended Mobile Automata | repair | C056 |
| T11 | Generalized Mobile Automata | retain-family | C030 |
| T12 | Turing Machines | retain-family | C049 |
| T13 | Neighbor-Independent Substitution Systems | retain-family | C061 |
| T14 | Neighbor-Dependent Substitution Systems | retain-family | C011,C055 |
| T15 | Creation-Destruction Substitution Systems | merge | C061 |
| T16 | Sequential Substitution Systems | retain-family | C080 |
| T17 | Tag Systems | retain-family | C091 |
| T18 | Cyclic Tag Systems | retain-preset | C091 |
| T19 | Register Machines | retain-family | C073 |
| T20 | Symbolic Systems | retain-family | C089 |
| T21 | Two-Dimensional Cellular Automata | retain-preset | C090 |
| T22 | Moore-Neighborhood Cellular Automata | retain-preset | C090 |
| T23 | Three-Dimensional Cellular Automata | retain-preset | C090 |
| T24 | Higher-Dimensional Lattice Cellular Automata | retain-preset | C090 |
| T25 | Two-Dimensional Turing Machines | retain-family | C049 |
| T26 | Two-Dimensional Substitution Systems | retain-preset | C061 |
| T27 | Geometric Replacement And Fractal Systems | repair | C061 |
| T28 | Neighbor-Dependent Two-Dimensional Substitution Systems | retain-family | C055 |
| T29 | Network Systems | retain-family | C062 |
| T30 | Multiway Systems | retain-family | C051 |
| T31 | Local Constraint Systems | retain-family | C043 |
| T32 | Template Constraint Systems | alias | C043 |
| T33 | Seeded Template Constraint Systems | retain-preset | C042,C043 |
| T34 | Arithmetic Iteration Systems | retain-family | C037 |
| T35 | Piecewise Integer Maps | retain-preset | C037 |
| T36 | Digit-Reversal Arithmetic Systems | retain-preset | C037 |
| T37 | Recursive Sequences | retain-family | C078 |
| T38 | Variable-Index Recursive Sequences | retain-preset | C078 |
| T39 | Number-Theoretic Filtering Systems | retain-family | C035 |
| T40 | Mathematical-Constant Digit Systems | split | C003,C017 |
| T41 | Function-Combination Systems | retire-role | C072 |
| T42 | Continued-Fraction-Driven Substitution Systems | retain-preset | C061 |
| T43 | Iterated Maps | retain-family | C037 |
| T44 | Continuous Cellular Automata | alias | C090 |
| T45 | Partial Differential Equation Systems | retain-family | C063 |
