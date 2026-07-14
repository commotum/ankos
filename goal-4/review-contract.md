# Goal 4 Review Contract

Contract ID: `ANKOS-REVIEW-1`

Status: Frozen by Stage 1.

## Principals and sessions

Every review record uses a stable principal ID, reviewer type, and session ID. Reviewer types are `HUMAN`, `AGENT`, and `AUTOMATED`. A claim of `HUMAN` is allowed only when a person actually performed the recorded decision.

Roles are:

- `CREATOR`: proposes the candidate or repair;
- `SOURCE_REVIEWER`: independently reads the authoritative witness;
- `SPECIALIST_REVIEWER`: reviews formulas/code/data, Index, figures, captions, or another declared specialty;
- `ADJUDICATOR`: resolves a disagreement and is distinct from every disagreeing principal.

Changing a role label, session ID, or display name does not create independence. The stable principal IDs must differ.

## Required coverage

- Every author-text or source-significant layout change receives one independent `SOURCE_REVIEWER` decision from the authoritative witness.
- Formula, code, rule/data, structural hierarchy, Index order/entry, caption association, visual replacement/insertion, and witness-only text insertion receive a blind source/specialist decision before the reviewer sees the proposed repair.
- High risk is the union of repair-class tags and operation/AST-impact tags. `STRUCTURE_BOUNDARY`, `MARKDOWN_STRUCTURE`, `HEADING_OR_FURNITURE`, `FORMULA_OR_SYMBOL`, `WOLFRAM_CODE`, `RULE_TABLE_OR_DATA`, `FIGURE_OR_CAPTION`, and `INDEX_ENTRY` are always high risk. Every witness-only author-text insertion and every authorial structure/hierarchy change is high risk regardless of its primary class.
- Every changed technical token, Index entry/column decision, and figure/caption association receives specialist coverage even when a source reviewer also reviewed it.
- Every disagreement receives third-principal adjudication; no disagreeing principal may self-adjudicate.
- Every unchanged ordinary block participates in total sequential review, with the pre-frozen quality sample receiving blind independent adjudication.
- All technical spans, printed Index regions, and printed figure groups receive their owning specialist-stage review whether changed or unchanged.

## Record fields

Each enumerated review row records:

- block, repair, witness-region, and evidence-view IDs/hashes;
- reviewer role, type, stable principal ID, and session ID;
- exact page/region or viewport/crop coordinates viewed;
- whether raw OCR, candidate output, or proposed repair was visible;
- independent transcription, structure, token, or association decision;
- agreement/disagreement, follow-up, adjudicator, and closure;
- review timestamp as audit metadata only, excluded from deterministic build output.

A blanket document-level `reviewed: true` flag is never sufficient.

## Independence gates

Validation fails when:

- creator and required reviewer principal IDs are equal;
- a high-risk decision lacks a sealed blind pre-proposal record;
- the evidence-view hash differs from the repair evidence hash or is absent;
- a required specialist role is missing;
- an adjudicator is one of the disagreeing principals;
- a disagreement remains open while workflow state is `CLOSED`;
- a reviewer is claimed as human without a human review record.

Agent review is recorded honestly as agent review. This contract does not silently substitute automation for a source reviewer.
