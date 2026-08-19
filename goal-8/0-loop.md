# Goal 8 Execution Loop

This loop exists only to resume and finish the research. `spaces.csv` is the
progress record; do not create stage records or parallel tracking documents.

## Loop

1. Compare `ref/types.csv` with the current `spaces.csv` and select the first
   incomplete or inadequately supported family in `book_index` order.
2. Read that family's defining Book passages. Use prior goals only to find
   relevant passages or variants.
3. Identify the mechanics that determine its addresses, relations, support,
   boundary behavior, and explicit form of time.
4. Determine the minimal native Space, Book-supported variants, any provable
   closure and its limit, and relevant encodings, exclusions, or genuine
   unknowns.
5. Write the family's final rows to `spaces.csv` immediately. Add to
   `findings.md` only when a proof or conclusion is useful beyond one CSV row.
6. Check the family against the completion test in `0-plan.md`, then continue
   directly to the next family.

Do not pause to update this scaffold, generate status prose, inventory
irrelevant historical leads, or build tooling that does not settle a family.
If evidence is missing, perform a targeted Book search. Use `unknown` only when
that search leaves a precise substantive question unresolved.

## Final Pass

After B001-B060 are complete:

1. Attack the weakest proofs and the pressure cases named in `0-plan.md`.
2. Resolve contradictions and remove claims supported only by intuition,
   illustrations, metadata, or implementation artifacts.
3. Run a lightweight one-off structural and citation check.
4. Inspect `spaces.csv` and `findings.md` as the final answer, run
   `git diff --check`, and confirm the changed-file scope.

Do not declare completion because rows exist or checks are green. Declare it
only when every family has an evidence-backed, bounded Space answer.
