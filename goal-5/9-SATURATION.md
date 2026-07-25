# 9-SATURATION

## Current Facts

- Sequential reading, the Index challenge, and mechanics consolidation are
  complete.
- The source-decision matrix contains 1,563 terminal lead decisions and 94
  serious mechanics candidates.
- Blind discovery remains in force until this single saturation pass is closed.

## Big Picture Objective

Challenge the consolidated inventory once across the entire canonical Book,
using discovered vocabulary and omission-oriented aliases, without creating
another audit system.

## Detailed Implementation Plan

- Use one fixed set of 40 non-overlapping query families covering local
  evolution, rewriting, maps and machines, relations, finite procedures, and
  construction-bearing application aliases.
- Scan every canonical Markdown file once.
- Compare matching lines mechanically with existing canonical lead anchors.
- Inspect only unrepresented hits, grouped by query family and source context.
- Add a lead only for actual new construction evidence; otherwise record the
  compact omission result here.
- Delete temporary hit material after decisions are complete.

## No-Cheating Checks

- Do not open the current catalog, API, Goal 1, Goal 2, or predecessor audit
  materials.
- Do not change the query set after seeing results.
- Do not rerun equivalent searches by chapter or by reviewer.
- Do not retain a raw hit archive in Goal 5.

## Completion Requirements

- All 40 query families have hit counts and a terminal omission decision.
- Every unrepresented hit is inspected in source context.
- Any new serious mechanic receives a lead, matrix row, and fingerprint.
- No unresolved saturation hit remains.
- Temporary raw hit material is deleted and `git diff --check` passes.

## Stage Results

- Froze 40 query families before searching and scanned all 31 canonical
  Markdown files exactly once.
- The pass found 2,297 query-line matches. Existing source anchors directly
  covered 571; the other 1,726 were grouped by nearby source context and
  inspected against the canonical Book.
- Every unmatched context was already represented mechanics, an alias, or
  exposition/property material. No new construction, lead, candidate, or
  unresolved question resulted.
- No query was tuned or rerun after results were visible. The temporary raw hit
  file was deleted after all 40 terminal decisions were validated.

| Query | Family | Hits | Anchored | Reviewed | Outcome |
|---|---|---:|---:|---:|---|
| Q001 | deterministic-cellular-automata | 106 | 40 | 66 | represented |
| Q002 | block-and-lattice-gas-automata | 19 | 9 | 10 | represented |
| Q003 | mobile-head-and-active-cell | 79 | 18 | 61 | represented |
| Q004 | asynchronous-and-synchronized-schedules | 11 | 6 | 5 | alias |
| Q005 | probabilistic-cellular-automata | 7 | 6 | 1 | represented |
| Q006 | continuous-local-automata | 27 | 14 | 13 | alias |
| Q007 | parallel-independent-substitution | 58 | 31 | 27 | alias |
| Q008 | contextual-and-sequential-substitution | 65 | 21 | 44 | alias |
| Q009 | tag-and-erasing-rewrite | 118 | 26 | 92 | represented |
| Q010 | symbolic-and-term-rewrite | 101 | 5 | 96 | alias |
| Q011 | multiway-rewrite | 209 | 52 | 157 | represented |
| Q012 | local-graph-rewrite | 4 | 2 | 2 | exposition |
| Q013 | dynamic-network-systems | 40 | 20 | 20 | represented |
| Q014 | causal-network-construction | 148 | 17 | 131 | represented |
| Q015 | derived-state-graph-boundary | 38 | 4 | 34 | represented / alias / exposition |
| Q016 | iterated-number-and-vector-maps | 154 | 34 | 120 | represented / alias / exposition |
| Q017 | recurrence-and-recursive-functions | 62 | 18 | 44 | represented / alias / exposition |
| Q018 | digit-emitting-register-procedures | 2 | 1 | 1 | represented / alias / exposition |
| Q019 | iterated-erasure | 13 | 3 | 10 | represented / alias / exposition |
| Q020 | global-and-append-only-sequence-growth | 29 | 9 | 20 | represented / alias / exposition |
| Q021 | register-and-stored-program-machines | 102 | 22 | 80 | represented / alias / exposition |
| Q022 | turing-partial-and-branching | 14 | 10 | 4 | represented / alias / exposition |
| Q023 | encoder-evolution-decoder-interface | 35 | 2 | 33 | represented / alias / exposition |
| Q024 | quantum-and-unitary-evolution | 30 | 6 | 24 | represented / alias / exposition |
| Q025 | continuous-equation-evolution | 128 | 40 | 88 | represented / alias / exposition |
| Q026 | field-and-action-relations | 74 | 17 | 57 | represented / alias / exposition |
| Q027 | local-satisfaction-constraints | 18 | 8 | 10 | represented / alias / exposition |
| Q028 | global-and-objective-constraints | 12 | 4 | 8 | exposition |
| Q029 | equation-and-word-relations | 269 | 36 | 233 | represented |
| Q030 | boolean-relations-and-finite-networks | 24 | 6 | 18 | alias |
| Q031 | compression-transformations | 18 | 9 | 9 | alias |
| Q032 | signal-image-and-error-processing | 23 | 8 | 15 | alias |
| Q033 | probabilistic-model-and-test-procedures | 20 | 4 | 16 | exposition |
| Q034 | cryptographic-and-inverse-procedures | 77 | 21 | 56 | represented |
| Q035 | direct-and-jump-ahead-evaluation | 6 | 2 | 4 | alias |
| Q036 | memory-retrieval-and-learning | 31 | 5 | 26 | alias |
| Q037 | interactive-multi-program-systems | 1 | 0 | 1 | alias |
| Q038 | aggregation-and-random-growth | 67 | 27 | 40 | alias |
| Q039 | fracture-flow-and-morphogenesis | 56 | 8 | 48 | alias |
| Q040 | program-and-rule-mutation | 2 | 0 | 2 | exposition |
