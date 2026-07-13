# 6-T16-SEQUENTIAL-SUBSTITUTION

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T16, CSV line 17, `Sequential Substitution Systems`; taxonomy seed `ref/notes/CA-Types.md:424-460`.
- T13 established ordered sequence state and structural replacement, but T16 replaces only one matched block per step rather than every old occurrence.
- Canonical evidence must resolve two independent priorities: which ordered rule is tried first and which occurrence of its left-hand side is chosen in the left-to-right scan.
- No-match behavior, overlap, empty sides, seed, trace events, and the relation to generalized/multiway substitution remain under evidence audit.

## Updated Assumptions

- A match is a source interval/path in the old ordered sequence, not a next-slice writable coordinate and not merely a symbol occurrence.
- Rule-list order and scan direction are defining semantics whenever they change the selected event.
- One structural splice is expected per step; T13's all-source `ParallelReplaceConcat` cannot be reused without an honest update distinction.
- Stopping because no ordered replacement applies must remain distinct from horizon, invalid rules, fixed points, and external stop policies.

## Big Picture Objective

Exhaustively recover sequential substitution semantics, then determine the smallest honest reuse of ordered sequence support, typed word replacement, structural trace, and termination without hiding priority/scan inside a callback or adding a sequential-family rollout.

## Catalog Identity

- Stable ID: T16.
- Exact name: Sequential Substitution Systems.
- Entry kind: deterministic ordered first-match string-rewrite construction.
- Search vocabulary: sequential substitution/replacement, string rewriting, production system, Markov/normal algorithm, text editor/search-and-replace, scan left/right, first occurrence/match/replacement, rule order/priority, overlap, `Flat`, `SSSEvolveList`, `StringReplace`, no replacement/stops/termination, confluence, multiway/generalized substitution, causal network, universality, initial string/word.

## Search Log

In progress. Main text, captions, Notes implementation/order/halting, history aliases, Index/splits, generalized/multiway boundaries, and emulations are under independent audit.

## Book Excerpts

In progress.

## Construction Model

Pending evidence closure. Working hypothesis:

```text
state = finite ordered word
for rule in ordered_rules:
    locate leftmost match of rule.lhs in old word
    if found:
        result = SpliceMatch(match, rule.rhs)
        next = SingleSplice(old, result)
        stop search
if no rule matches:
    terminal NoMatch
```

Exact Mathematica ordering/overlap and empty-side validation remain to be proved.

## Current API Fit

Pending reconstruction. Expected reuse is T13 ordered state/word typing and structural trace; expected mismatches are active-source discovery over patterns, priority, single-splice commit, and no-match termination.

## Current Runtime Fit

Pending reconstruction. Current fixed dense frontier, scalar lookup, fixed-shape NumPy trace, and family dispatch cannot express prioritized structural matching natively.

## Principles Audit

Pending evidence closure. Priority and scan order are defining semantics under Principles 3/11; no callback, regex engine smuggling, T16 branch, or all-match shortcut is accepted.

## Detailed Implementation Plan

1. Close direct/alias/caption/Notes/Index/split/variant/emulation searches.
2. Reconstruct ordered rule selection, match enumeration, overlap, one-splice commit, seed, successor, no-match termination, and trace provenance.
3. Compare against T13 structural update and rederive selector/result/update responsibilities wherever composition fails.
4. Specify Goal 2 files, migrations, exact trajectories, adversarial priority/order tests, and shared-executor conformance.
5. Reintegrate, reopen contradicted stages only, verify, and advance.

## Goal 2 Implementation Stage

Pending evidence closure and fit audit.

## No-Cheating Checks

- No sequential-family rollout or unrestricted whole-word callback/regex replacement engine.
- No all-occurrences or all-rules replacement presented as the one-event construction.
- No hidden rule sorting, unordered map, scan-direction default, or overlap fallback.
- No fixed-capacity padding/shift buffer as variable sequence semantics.
- No no-op, missing rule, invalid match, horizon, or error conflated with `NoMatch` termination.
- No multiway branching collapsed to a deterministic path or deterministic priority mislabeled as confluence.

## Completion Requirements

- [ ] All aliases, captions, Notes, Index entries, splits, variants, duplicates, and false positives are resolved.
- [ ] Ordered word, rule priority, scan/match policy, result, splice update, seed, successor, termination, and observables are reconstructed.
- [ ] Exact trajectories and adversarial priority/overlap/no-match invariants have independent tests.
- [ ] Current API/runtime/principles fit and T13 reuse/divergence are explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

In progress. No T16 architectural conclusion is complete yet.
