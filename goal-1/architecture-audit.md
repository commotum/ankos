# Goal 1 Representation and Execution Architecture Audit

Status: **IN PROGRESS — HARD PREREQUISITE FOR T06 AND ALL FURTHER TYPE WORK**

## Trigger and Scope

T09/T12 and decisions D009-D014 are reopened because they promoted one state decomposition—separate `SingleControl`/`TransitionControl` records—into a semantic requirement. The audit covers every completed decision and every proposed state, control, frontier, neighborhood, rule result, update law, executor, and runtime API extension. It updates affected stage files, the design ledger, the global plan, and Goal 2 handoffs before T06 or any other type stage resumes.

In this audit, **domain** means only the dimensional task/program space `t+0D`, `t+1D`, `t+2D`, or `t+3D`, whether discrete or continuous. A tape alphabet, head-state set, scalar value set, or parameter set is not called a domain here.

## Classification Vocabulary

1. **DIRECT REUSE** — an existing construction expresses the complete state and transition semantics unchanged.
2. **PARAMETER / RESTRICTION / PRESET / INVARIANT / NAMED ROLE** — no new execution algebra; validation or a closed specialization distinguishes the construction.
3. **LOSSLESS TAGGED / PRODUCT REPRESENTATION** — an explicit structural isomorphism preserves every state component and transition, without hidden data or altered behavior.
4. **GENUINELY DIFFERENT EXECUTION ALGEBRA** — a concrete counterexample proves the smallest existing construction cannot express the state change faithfully.

Different source terminology, semantic role names, or decompositions of equally shaped state do not by themselves justify a new class. Conversely, a collapse is rejected if it requires hidden state, callbacks, family dispatch, lossy encoding, invented behavior, or altered update semantics.

## Reopened Core Finding

For a Turing machine, let

```text
Cell = Plain(TapeSymbol) | Head(HeadState, TapeSymbol)
X : Z -> Cell
invariant: exactly one coordinate contains Head(...)
```

This is losslessly equivalent on valid states to a tape-symbol field plus one `(position,head_state)` record. It keeps both the head state and the symbol beneath it visible. A bare `TapeSymbol union HeadState` is not equivalent because it loses the underlying symbol.

The compact rule remains `delta : Q x Sigma -> Q x Sigma x {L,R}`. From one old snapshot, its structural lowering assigns a plain written symbol at the old head and a head-tagged old destination symbol at the neighbor, then commits both assignments atomically. No zero-head or two-head intermediate configuration is observable. This does not identify the compact Turing program with the enormous set of arbitrary cellular-automaton tables over `Cell`.

The T09 specialization uses `Cell = Plain(bit) | Active(bit)` and the same exactly-one invariant. Its compact eight-row, four-result rule remains native. Because the mobile direction can depend on the old head's radius-one context, a full-slice radius-one target-local CA lowering is not assumed; a closed two-target structural lowering suffices, and any full-slice lowering must prove its required radius.

## Audit Matrix

| Decision / stage | Evidence and former claim | Classification | Smallest reusable base | Required invariants / structural mapping | Reopen action |
|---|---|---|---|---|---|
| D009 / T09 | Mobile event originates at old active cell; former conclusion redefined `FRONTIER` as firing sources | UNDER AUDIT | Existing writable-frontier, old-snapshot parallel assignment schema | Distinguish named activation/source projection from writable target set; prove compact-rule lowering | T09, plan, and Goal 2 handoff reopened |
| D010 / T09 | Active position must be visible; former conclusion required a separate state component | LOSSLESS TAGGED / PRODUCT REPRESENTATION | Finite composite alphabet on the existing field | `Plain(bit) <-> (bit,None)`; `Active(bit) <-> (bit,Unit)`; exactly one active tag | Replace storage mandate with representation-neutral visibility and validation |
| D011 / T09/T12 | Write and move/state change are one atomic event; former conclusion required `TransitionControl` effects | UNDER AUDIT | Existing atomic old-snapshot assignment commit plus a closed structural lowering | Two assignments computed from one valid old state; collision/coverage validation; valid successor | Determine whether a generic finite patch is direct reuse or a parameterization; remove unjustified effect class |
| D012 / T01/T09 | Physical `[left,self,right]` read and codec are shared | DIRECT REUSE, pending placement check | Existing ordered neighborhood/read codec | Preserve ordering before lowering; no mobile permutation | No semantic reopening expected |
| D013 / controlled traces | Raw traces must retain active/head information | PARAMETER / INVARIANT / NAMED ROLE | Existing complete state trace over composite values | Tagged field round-trips exactly; compressed/display traces remain observers | Rewrite representation-neutral wording |
| D014 / T09/T12 | Head payload and position must be visible; former conclusion required `SingleControl` | LOSSLESS TAGGED / PRODUCT REPRESENTATION | Composite finite cell alphabet plus fixed field | `Plain(sigma) | Head(q,sigma)` isomorphic to `(tape,position,q)` on exactly-one states | Replace required class with optional named projection/view |

The matrix is intentionally incomplete while the all-decision review is running. No audited decision is reactivated until its evidence, smallest base, invariants, counterexample (if class 4), dependent stages, and Goal 2 disposition are recorded here.

## Completion Gate

- [ ] D009-D014 have final classifications and revised consequences.
- [ ] Every completed D001-D118 decision appears in the audit matrix, individually or in an explicit lossless grouped row with per-decision disposition.
- [ ] Every completed stage's state/control/frontier/read/result/update/executor/API claims have been checked from first principles.
- [ ] Each class-4 abstraction includes a concrete counterexample against the smallest reusable base.
- [ ] T09/T12 and every affected dependent stage have revised stage results and Goal 2 handoffs.
- [ ] `0-plan.md`, `evidence-index.md`, and `design-ledger.md` agree exactly.
- [ ] Fresh independent review, Markdown-fence checks, `git diff --check`, and scope checks pass.
- [ ] Only after every gate passes may T06 or prior asset repairs resume.
