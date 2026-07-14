# 31-T15-CREATION-DESTRUCTION

Status: **IN PROGRESS — EXHAUSTIVE SOURCE, ASSET, SEMANTIC, AND ARCHITECTURE AUDITS OPEN**

## Current Facts

- T15 is CSV line 16, Creation-Destruction Substitution Systems. The catalog and `CA-Types.md` supply search vocabulary only; neither is primary construction evidence.
- The direct Chapter 3 discussion begins at `BOOK:1028` immediately after the strict nonempty neighbor-dependent examples. It says elements may disappear, distinguishes excessive disappearance from rapid growth, and studies rules whose creation and destruction are nearly balanced (`BOOK:1028-1040`).
- The direct figures use variable-cardinality ordered words. Equal-total-width and fixed-box rows are alternate views, and only sequence order remains semantic as insertions/deletions shift later displayed positions (`BOOK:1032-1048`).
- The facing-page three- and four-color examples retain the same creation/destruction theme; one has a CA-like regular region away from the right edge and the others create and destroy elements throughout (`BOOK:1044-1052`). Exact table arity, empty rows, seeds, and boundary behavior must be decoded and independently bound before this becomes a construction claim.
- T14 established `OrderedGenerationConcat`: selected old anchors emit ordered words and UPDATE consumes the old generation, concatenating writes in source/child order. T13 and strict T14 currently validate `Sigma+`; T15 must determine whether the reusable base is actually `Sigma*` with nonempty output only a preset invariant.
- An empty RULE emission, zero selected sources, an empty successor, extinction, halt, and zero successors are distinct. T14's `[]->[]`/singleton-to-empty behavior comes from zero eligible pairs and cannot serve as evidence for a native epsilon-valued T15 row.
- DOMAIN is expected to remain discrete `t+1D`; the finite ordered word and its occurrence topology belong to CONFIGURATION. This remains a hypothesis until the direct rule plates and Notes/Index routes close.
- Goal 1 changes only `goal-1/`. Runtime implementation and tests remain Goal 2 work.

## Updated Assumptions

- Leading reuse hypothesis: T15 keeps the T14 finite-word/frontier/read schedule and widens the pair-table output from `Sigma+` to `Sigma*`; the shared UPDATE then needs no new algebra. This is not accepted until a direct empty-output row and one-step commuting reconstruction are proved.
- If the source instead mixes self-only and contextual profiles, they should be named presets over the same ordered-generation base, not one family switch or a table that accepts ambiguous key shapes.
- Empty emissions must remain explicit typed writes/events bound to their old sources even though they create no children. Lineage must not invent epsilon symbols, zero-width child objects, or sentinels.
- Extinction to the valid empty word is a successor. Whether the empty word subsequently stutters, terminates, or has another source-defined outcome must follow the exact native operator rather than a global empty-frontier rule.
- Balanced/slow growth is initially an observer or rule/trajectory property, not a `growth_policy`, update mode, or hidden selection criterion.

## Big Picture Objective

Reconstruct creation-destruction substitution directly from exhaustive primary evidence and decide whether native empty emissions are a typed-result parameterization of the existing ordered-generation construction. Preserve the distinctions among deletion, zero-source events, extinction, terminal outcomes, and rendering while requiring a concrete counterexample before introducing any new UPDATE algebra or executor.

## Catalog Identity

- Stable ID: T15.
- CSV line: 16.
- Catalog name: Creation-Destruction Substitution Systems.
- Taxonomy section: 15.
- Provisional construction kind: deterministic parallel transition system over a dynamically sized ordered symbol configuration.
- Search vocabulary: creation/destruction, disappear/disappearance, die out/extinction, slow/balanced/fixed growth, empty replacement, page 86/page 87, substitution rule plates, Notes/Index routes, multicolor variants, and adjacent contextual relations.

## Search Log

The exhaustive frozen source oracle is in progress. Direct anchors already requiring disposition include `BOOK:1028-1052`, their linked plates and captions, relevant Notes and actual Index routes, split-document counterparts, growth/property continuations, and T13/T14/T16/T17 relations. No search count or closure claim is made until every candidate is frozen and classified.

## Book Excerpts

### Excerpt 1: disappearance, extinction pressure, and balance

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1028-1030`
- Context: Chapter 3, continuation of neighbor-dependent substitution systems.
- Establishes: native disappearance is permitted and balance/extinction are trajectory-level phenomena to reconstruct.

> It is, however, also possible to consider substitution systems in which elements can simply disappear. If the rate of such disappearances is too large, then almost any pattern will quickly die out. And if there are too few disappearances, then most patterns will grow very rapidly.
>
> But there is always a small fraction of rules in which the creation and destruction of elements is almost perfectly balanced.

### Excerpt 2: two renderings of one dynamic ordered evolution

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1032-1038`
- Context: caption and discussion for the page-86 example.
- Establishes: equal-total-width and fixed-box views are observers; fixed-amount growth describes the example, not an update policy.

> Two views of a substitution system whose rules allow both creation and destruction of elements. In the view on the left, the boxes representing each element are scaled to keep the total width the same, whereas on the right each box has a fixed size, as in our original pictures of substitution systems on page 82. The right-hand view shows that the rates of creation and destruction of elements are balanced closely enough that the total number of elements grows by only a fixed amount at each step.

### Excerpt 3: order survives addition and subtraction

- Source: `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:1046`
- Context: caption for three- and four-color examples.
- Establishes: occurrence order is semantic while row-local displayed positions are not persistent addresses.

> Note that on each line in each picture, only the order of elements is ever significant: as the insets show, a particular element may change its position as a result of the addition or subtraction of elements to its left.

## Construction Model

Open evidence questions:

- Does the strict direct profile use ordered pair contexts exactly as T14, and which old anchors are eligible?
- Which exact rows emit zero, one, or multiple symbols, over which alphabets?
- Does the rightmost old occurrence remain source-ineligible, and what happens after the word becomes empty?
- Are the displayed seeds/tables/textual rules recoverable from Notes, raster, or both?
- Does one shared `OrderedGenerationConcat[Word]` commute with the native operator when `Word` permits epsilon?
- How should an empty source-bound emission be represented in event/lineage data without creating a child or alphabet symbol?

The provisional candidate, subject to those answers, is:

```text
active = FRONTIER.select(configuration)
reads  = NEIGHBORHOOD.read(configuration, active)
writes = RULE(active, reads)                  # source-bound words in Sigma*
next   = UPDATE.apply(configuration, active, writes)
```

## Current API Fit

Pending exact reconstruction. The reuse target is the generic finite ordered configuration, occurrence frontier predicates, occurrence-relative reads, total structured lookup, source-bound word writes, and `OrderedGenerationConcat`. Any new semantic class or UPDATE requires a direct counterexample to that composition.

## Current Runtime Fit

`src/ca` is the runtime namespace for the broader SimplePrograms library, not a cellular-automata library. Its currently implemented fixed-shape components and family-dispatched rollout do not yet realize the full intended axes. T15 is expected to stress ragged empty/nonempty word frames and epsilon-capable typed writes; Goal 2 must complete those generic axes rather than add a T15 rollout branch, sentinel, fixed capacity, callback, or family dispatch.

## Principles Audit

- DOMAIN/configuration/topology must remain separated: dynamic ordered support is not a new dimensional DOMAIN.
- Empty output is a value of a typed word-result schema, not an empty alphabet symbol or hidden delete callback.
- If T15 commutes with the same ordered-generation commit, nonempty output belongs to T13/T14 preset validation rather than the reusable UPDATE base.
- Extinction and subsequent evolution must remain source-defined outcomes; the runner has no universal empty-frontier behavior.
- Slow growth, balance, eventual repetition, CA-like patches, and display scaling remain claims/observers/relations unless evidence makes one transition-defining.

## Detailed Implementation Plan

1. Freeze the exhaustive monolith/split/Notes/Index source union and every disposition in `31-T15-source-oracle.py`.
2. Close the source-bound asset universe, hashes, rule/seed/trajectory decoding, and observer classifications in `31-T15-asset-oracle.py`.
3. Build an independent native/generic semantic oracle covering epsilon rows, deletion, creation, source order, snapshot/newborn behavior, extinction, and malformed writes.
4. Audit D019, D020, D024, and D124 from first principles; factor only the smallest reusable base and reopen any contradicted preset wording.
5. Complete the API/runtime comparison, Goal 2 handoff, no-cheating checks, hostile review, global integration, and all root/`/tmp`/optimized-mode/Markdown/diff/scope/coverage/test gates.

## Goal 2 Implementation Stage

Pending evidence closure. The provisional obligation is to make the ordered-generation result carrier honestly epsilon-capable while keeping strict T13/T14 constructors nonempty, preserving explicit source-bound empty-emission witnesses, and executing through the same branch-free runner.

## No-Cheating Checks

- Reject treating T14's zero eligible pairs as proof of a T15 epsilon rule row.
- Reject an empty string/sentinel/padding cell standing for deletion.
- Reject removing old sources in place before all reads are taken from the old snapshot.
- Reject copying unmatched or non-emitting old sources forward unless the source explicitly does so.
- Reject treating extinction as halt, error, no successor, or automatic episode termination without evidence.
- Reject a `growth_policy` that changes execution or filters native successors.
- Reject T15-specific state, UPDATE, rollout, callback, family switch, CA compiler, fixed capacity, or rendering-fed execution.
- Require source/asset/semantic oracles to pass from the repository and `/tmp` and fail closed under `python -O`.

## Completion Requirements

- [ ] Exhaustive source/split/Notes/Index/alias audit closes with zero unresolved candidates.
- [ ] Source-bound asset fixed point closes with all rule/seed/trajectory and observer facts independently decoded.
- [ ] Native empty outputs, zero-source cases, extinction, and subsequent evolution are distinguished exactly.
- [ ] Semantic oracle proves or refutes reuse of the shared ordered-generation UPDATE with adversarial cases.
- [ ] API/runtime/principles audits identify the smallest reusable base and any narrowly reopened decisions.
- [ ] Goal 2 handoff is implementation-ready and contains canonical conformance/no-cheating tests.
- [ ] Independent hostile review is clean and every oracle/test/Markdown/diff/scope/coverage gate passes.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` are integrated consistently.

## Stage Results

In progress. Direct prose establishes native disappearance pressure, balanced-growth observations, dynamic ordered support, and multiple renderings, but the exact rule/seed/operator semantics remain open pending exhaustive source and asset closure. No runtime code has changed and no new UPDATE algebra has been accepted.
