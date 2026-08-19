# Goal 8: Canonical Family Space Audit

## Objective

Determine the complete evidence-backed `SPACE` envelope for every canonical
family in [`ref/types.csv`](../ref/types.csv), in `book_index` order.

For each family, answer:

1. What is its minimal native Space?
2. What other Spaces does *A New Kind of Science* show or state?
3. What broader range follows from the same mechanics?
4. Where does that generalization stop?
5. Which relevant alternatives are encodings, exclusions, or genuinely
   unresolved?

The work product is the answer for the 60 families, not a process for studying
them.

## Space Semantics

`SPACE` specifies independently addressable coordinates, their relations,
support behavior, and boundary behavior. Attributes stored at one address are
Alphabet values, not additional coordinates.

Time is explicit. Typical Cartesian forms are `[t]`, `[t,x]`, `[t,x,y]`, and
`[t,x,y,z]`, but graph, tree, event, branch, continuous, and one-shot systems
must use the coordinates and relations their mechanics actually require.

For discrete evolution, each step preserves every earlier slice and creates a
complete new slice at `t+1`. Locations outside the Frontier are copied into the
new slice unchanged; nothing at `t` is overwritten.

`INTENSIONAL` is a presentation mode, not a Space. Drawings, embeddings,
serializations, observers, and simulations are not native Space unless the
family's mechanics independently address their coordinates.

## Evidence Standard

- `ref/types.csv` supplies family identity and Book order.
- Prior goals may locate passages; they are not evidence and do not need to be
  re-audited.
- The canonical documents under
  [`ref/A-New-Kind-of-Science/`](../ref/A-New-Kind-of-Science/) are the source
  for `shown` and `stated` claims.
- A `proved` range must identify the invariant mechanics, the generalized
  coordinate or relation, the unchanged update law, and the point where the
  argument fails.
- Lack of a Book example is not proof of exclusion or of a maximum dimension.

## Outputs

During execution, change only:

- `goal-8/spaces.csv` — the authoritative normalized answer;
- `goal-8/findings.md` — shared vocabulary, nontrivial proofs, difficult cases,
  and concise cross-family conclusions.

Use the existing CSV schema:

```text
book_index,family_id,home,slug,space_claim,claim_kind,evidence,time,coordinates,relations,support,boundary,source,reason,limit
```

`claim_kind` is one of `native`, `variant`, `encoding`, `excluded`, or
`unknown`. `evidence` is one of `shown`, `stated`, `proved`, or `unresolved`.
Only `native` and `variant` claims backed by `shown`, `stated`, or `proved`
belong to the supported Space envelope.

Do not create stage files, source ledgers, coverage reports, permanent
validators, or duplicate prose versions of the CSV.

## What Counts as a Completed Family

A family is complete only when its CSV rows directly answer all five objective
questions, including explicit time, support, relations, boundary conditions,
evidence, reasoning, and limits. In particular:

- a row, citation, or family count alone proves nothing;
- a displayed example establishes only what it displays;
- a parameterized closure requires an actual closure argument;
- `unknown` is allowed only after the relevant Book evidence has been pursued
  and the exact missing fact is named; and
- runtime types, names, stubs, and current implementation limits are not
  semantic evidence.

Progress is the set of genuinely completed families in `spaces.csv`. Do not
maintain a second progress system.

## Work

### 1. Audit B001-B060

Proceed in `book_index` order. For each family, read its defining Book material,
derive and bound its complete Space envelope, write the result immediately,
and move on only when the family completion test passes. Revisit earlier rows
only when later evidence exposes a concrete contradiction.

Completion requirement: every one of the 60 families is complete by the
standard above. SPF030 must explicitly settle `[t,x]`, `[t,x,y]`, `[t,x,y,z]`,
higher-rank claims, and relevant non-Cartesian alternatives.

### 2. Adversarial Finish

Review the result for unsupported generalization, category errors, convenient
`unknown`s, and missing Book variants. Pay special attention to graph/tree,
continuous, one-shot, multiway, dynamic-support, product-valued, event-time,
and intensional cases.

Completion requirement:

- the CSV family set exactly matches the 60 rows of `ref/types.csv` and is in
  `book_index` order;
- every supported claim has a valid Book citation or a bounded written proof;
- every remaining unknown is a genuine, precisely stated evidence limit;
- claims use a consistent Space vocabulary without erasing real structural
  differences;
- CSV parsing, identity, allowed values, unique claim keys, source paths, and
  ordering pass a lightweight one-off check;
- `git diff --check` passes; and
- no files outside the two research artifacts changed during execution.

Structural checks catch malformed output; they do not establish semantic
truth. The goal is complete only when the actual 60-family answer survives the
adversarial review.
