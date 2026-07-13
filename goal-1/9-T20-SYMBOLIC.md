# 9-T20-SYMBOLIC

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T20, CSV line 21, `Symbolic Systems`; taxonomy seed `ref/notes/CA-Types.md:524-551`.
- The taxonomy hypothesis is an evolving hierarchical expression transformed by pattern rules. The Chapter 3 example appears to use curried `e[...]` trees, named pattern variables, a left-to-right scan, and simultaneous application at non-overlapping matches, but canonical evidence must settle exact expression grammar, match eligibility, traversal, binding, overlap, replacement timing, seed, and halting.
- T13 supplies explicit tree/lineage observations for parallel symbol replacement, while T16 supplies program-coupled literal matching, ordered priority, and one interval splice. Neither has yet established a native expression tree, structural pattern variables, subexpression bindings, duplication/deletion of bound subtrees, or a maximal non-overlapping match set.
- A host symbolic engine may be useful as an independent oracle, but routing execution through unrestricted host patterns or replacement callbacks would conceal the construction and fail Principle 0.
- Tree identity, child order, head/application representation, expression occurrences, pattern-variable scope, binding consistency, traversal order, overlap selection, result templates, atomic replacement, fixed points, seeds, variants, observers, universality, and encodings remain under audit.

## Updated Assumptions

- The expression tree and every piece of control needed to choose a deterministic match set must be explicit semantic data. Display layout, textual parentheses, object identity, and host evaluator state are not native unless the book requires them.
- Pattern variables bind complete subexpressions, not string fragments or scalar cell values. Repeated occurrences of one variable, variable capture, substitution into a result template, and whether unmatched symbols are literals require evidence-backed rules.
- Traversal and overlap policy are defining semantics whenever changing them changes the next expression. They cannot be treated as an incidental matcher implementation.
- A rewrite event must expose source occurrence(s), environment/bindings, instantiated output tree, consumed/persisted/duplicated structure, and old-snapshot provenance before any update algebra is chosen.
- T16's `FirstApplicableMatch`/`SingleSpliceUpdate` may be insufficient if a symbolic step applies one rule at every non-overlapping match during one scan. T13's full parallel replacement may also be insufficient if eligibility depends on subtree patterns and overlapping candidates.
- Fixed points, no-match termination, an explicitly requested horizon, invalid patterns, evaluation errors, and applicable identity rewrites must remain distinct.

## Big Picture Objective

Exhaustively reconstruct the canonical symbolic-system expression model, pattern language, deterministic matching/traversal/overlap policy, binding/template instantiation, update timing, successor/halting behavior, seeds, variants, and relations. Determine the smallest honest tree-rewrite source/read/result/update model without string flattening, unrestricted host evaluation, opaque callbacks, family dispatch, fixed-capacity tensors, or conflation with T13/T16.

## Catalog Identity

- Stable ID: T20.
- Exact name: Symbolic Systems.
- Entry kind: unresolved pending evidence; expected deterministic hierarchical term-rewrite construction.
- Search vocabulary: symbolic system/expression; symbolic transformation/rewrite/replacement; combinator; application/head/argument/tree/subexpression; `e`, `e[x_][y_]`, blank/pattern/named pattern/variable/binding; match/matching; scan/left/right/order; replace/apply/overlap/non-overlap/simultaneous/parallel; fixed point/repeat/halt/stop; initial expression/seed; nested expression/growth/size; Mathematica/ReplaceAll/ReplaceRepeated; lambda calculus/combinatory logic/operator systems; universality/emulation; exact Notes implementation symbols; Index aliases and page routes.

## Search Log

In progress. Independent canonical core/figure, Notes/Index/split/history/variant, and Principle-0/API/runtime-fit audits are running.

## Book Excerpts

In progress.

## Construction Model

Pending evidence closure. Working questions, not conclusions:

```text
state = ordered rooted expression tree
program = ordered pattern -> template rule data

candidates = match(pattern, every expression occurrence)
selected = deterministic traversal/overlap policy(candidates)
results = instantiate(template, each selected binding environment)
next = atomic tree replacement from the old snapshot
```

Canonical evidence must determine whether there is one rule or an ordered program, which occurrences count as a scan position, whether the head is itself an expression occurrence, how nested/adjacent matches are ordered, whether newborn expressions can match in the same step, and whether absence of a match terminates or yields a fixed successor.

## Current API Fit

Pending evidence reconstruction. Expected direct responsibility reuse is immutable program data, visible structured state, source-first orchestration, typed outcomes, and provenance. Expected mismatches are dense rank-0..3 support, scalar alphabets, coordinate neighborhoods, writable-target frontiers, scalar rule returns, fixed-shape traces, and formula callbacks.

## Current Runtime Fit

Pending full audit. Current `src/ca` has no inspectable ordered expression tree, pattern AST, binding environment, occurrence path, deterministic overlap selector, instantiated tree result, tree-replacement commit, or structural trace.

## Principles Audit

Pending evidence closure. Principle 0 must decide whether T13 occurrence replacement, T16 program-coupled matching, and a private ordered/tree edit kernel compose, or whether T20 proves a new overlap-aware tree-update law. No host `ReplaceAll` delegation, regex/string encoding, arbitrary predicate/template callback, flattened-cell packing, hidden evaluator, family rollout, or fixed-depth/capacity tree is accepted.

## Detailed Implementation Plan

1. Close direct, alias, caption/figure, Notes, actual Index, split, history, implementation, traversal, pattern, overlap, fixed-point, seed, growth, universality, and emulation searches.
2. Reconstruct expression grammar/topology, values, occurrence identity/paths, pattern AST, binding environments, active match selection, reads, result instantiation, update/commit, successor, halting, seeds, parameters, variants, and observers.
3. Compare T20 with T13/T16 and rederive source/read/result/update responsibilities wherever literal intervals, all-occurrence coverage, or existing splice semantics do not compose.
4. Specify exact canonical trajectories and adversarial binding/repetition/nesting/overlap/traversal/newborn/identity/no-match/provenance invariants with an independent matcher oracle.
5. Write the implementation-ready Goal 2 stage, reintegrate all ledgers, verify, and advance.

## Goal 2 Implementation Stage

Pending evidence closure and fit audit.

## No-Cheating Checks

- No symbolic-family rollout, whole-expression callback, host evaluator delegation, unrestricted matcher/predicate/template function, or `Any` term/rule/result.
- No flattening the expression into a string, tape, token array, CA row, scalar code, or fixed-depth padded tensor as native state.
- No hidden traversal cursor, replacement queue, binding environment, evaluation attribute, simplifier, memoization, or host-language rewrite ordering.
- No regex substitution, textual parenthesis matching, object-identity-dependent semantics, or display-tree coordinates standing in for ordered tree paths.
- No overlap resolution, newborn timing, rule priority, or fixed-point behavior inferred from a convenient library default without canonical evidence.
- No applicable identity rewrite collapsed into no-match/fixed-point termination; no horizon/error/invalid pattern mislabeled as semantic halt.
- No reuse of T13/T16 update algebras until tree source coverage, bindings, and overlap invariants are proven equivalent.

## Completion Requirements

- [ ] All aliases, captions/figures, Notes, actual Index entries, splits, variants, duplicates, and false positives are resolved.
- [ ] Expression state/topology, pattern/binding semantics, traversal/overlap selection, result instantiation, update timing, seed, successor, and halting are reconstructed.
- [ ] Exact trajectories and adversarial binding/nesting/overlap/newborn/identity/no-match/provenance invariants have independent tests.
- [ ] Current API/runtime/principles fit and T13/T16 reuse/divergence are explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

In progress. No T20 architectural conclusion is complete.
