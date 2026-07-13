# 7-T17-TAG

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T17, CSV line 18, `Tag Systems`; taxonomy seed `ref/notes/CA-Types.md:441-466`.
- The taxonomy proposes a finite variable-length queue-like word, fixed front deletion, an appended word selected from removed input, and terminal behavior when too few symbols remain. Canonical evidence must determine the exact selector: the first symbol, the entire deleted prefix, or a documented variant.
- T13 provides ordered occurrence support/full-generation replacement; T16 adds a single interval splice and typed no-applicable-rule termination. T17 may reuse their ordered edit kernel, but prefix consumption plus suffix append and short-word halting require their own evidence and update law.
- Deletion number, appendant table domain/codomain, seed, one- versus two-symbol variants, empty appendants, exact event order, rule numbering, support boundary, and relations to cyclic tag/Turing/CA systems remain under audit.

## Updated Assumptions

- The word front is semantic. Reversal, a hidden queue object, or an arbitrary chosen interval would change the construction.
- Consumption and append occur in one logical transition from the old word. Appended symbols are not read or deleted until a later step unless evidence says otherwise.
- A short input must produce an explicit construction-specific terminal outcome rather than an index error, padded read, fabricated blank, or generic no-match result.
- If rule choice reads only the leading symbol while the update deletes `v` symbols, those roles must remain distinct; no neighborhood is widened merely to justify deletion.
- Queue state remains an explicit ordered word, not an opaque scalar, bounded ring buffer, or Turing/CA compilation.

## Big Picture Objective

Exhaustively reconstruct ordinary tag-system consume/read/append/halting semantics, then determine the smallest honest reuse of ordered support, typed structural results, span editing, and terminal outcomes without hiding a queue machine in a callback or adding a tag-family rollout.

## Catalog Identity

- Stable ID: T17.
- Exact name: Tag Systems.
- Entry kind: unresolved pending evidence; expected deterministic finite-word queue rewrite construction.
- Search vocabulary: tag system/machine, Post tag, deletion number, delete/remove/drop/take first/beginning/left, append/add/join/end/right, appendant, production, first/deleted symbol/block/prefix, one-tag/1-tag/two-tag/2-tag, halt/stop/extinction/too short/length, initial word/condition, `TSEvolveList`/`TSStep`, rule number/count/enumeration, cyclic tag, universal tag, substitution/Turing/CA emulation, random initial conditions, and history/Index aliases.

## Search Log

In progress. Direct main-text mechanics/captions/examples and independent Notes/Index/split/history/variant/emulation audits are running.

## Book Excerpts

In progress.

## Construction Model

Pending evidence closure. Working question, not a conclusion:

```text
if len(word) < deletion_number:
    terminal TooShort
else:
    read leading selector required by the rule
    consume fixed prefix
    append selected word at the suffix
```

The exact read domain, order of operations, empty outputs, and terminal threshold must be established from the book.

## Current API Fit

Pending evidence reconstruction. Expected direct responsibility reuse is finite alphabet/program-seed separation; expected mismatches are fixed dense support, writable-target frontier, local stencil reads, scalar rule results, same-site commit, and fixed-shape trace.

## Current Runtime Fit

Pending full audit. Current `src/ca` has no explicit queue-front source, prefix read, consume-and-append effect, short-word terminal outcome, or ragged trace.

## Principles Audit

Pending evidence closure. Principle 0 must decide whether T17 is one ordered multi-span edit, a new queue update algebra, or pressure that redraws the source/read/update boundary. No callback, family branch, hidden cursor, fixed capacity, padding, or compiler is accepted.

## Detailed Implementation Plan

1. Close direct, alias, caption, Notes, Index, split, history, variant, initial-condition, halting, numbering, and emulation searches.
2. Reconstruct state/front, active source, exact read, rule table, consume/append result, atomic update, successor, terminal threshold, seed, trace provenance, parameters, and variants.
3. Compare T17 with T13/T16 and rederive responsibilities wherever prefix read, deletion, and suffix append do not compose.
4. Specify exact canonical trajectories, length laws, terminal boundaries, read/delete discriminators, ordering/provenance adversaries, and shared-executor tests.
5. Write the implementation-ready Goal 2 stage, reintegrate all ledgers, verify, and advance.

## Goal 2 Implementation Stage

Pending evidence closure and fit audit.

## No-Cheating Checks

- No tag-family rollout or whole-queue callback.
- No bounded deque/ring buffer, fake blank symbol, padding, mask, wraparound, truncation, or capacity failure as word semantics.
- No opaque encoding as a CA/Turing machine or scalar alphabet value.
- No treating the deleted prefix, selected rule input, or appended word as interchangeable without evidence.
- No appending before the old-front read or consuming appended newborns in the same event.
- No short input turned into a boundary read, default rule, no-op, error, horizon, or T16 `NoMatch` without proof.
- No cyclic program counter smuggled into ordinary T17; T18 remains separate.

## Completion Requirements

- [ ] All aliases, captions, Notes, Index entries, splits, variants, duplicates, and false positives are resolved.
- [ ] State/front, rule input/output, deletion number, atomic consume/append, seed, successor, terminal behavior, and observables are reconstructed.
- [ ] Exact trajectories and adversarial read/delete/order/short-word/provenance invariants have independent tests.
- [ ] Current API/runtime/principles fit and T13/T16 reuse/divergence are explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

In progress. No T17 architectural conclusion is complete.
