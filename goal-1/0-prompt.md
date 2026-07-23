# Goal 1 Continuation Prompt

```text
Work through /home/jake/Developer/ankos/goal-1/0-plan.md using /home/jake/Developer/ankos/goal-1/0-loop.md.

Objective: derive the simplest coherent constructive API for every one of the 45 entries in ref/notes/CA-Types.csv. For each type, exhaustively collect every unique construction-relevant excerpt from the local A New Kind of Science Markdown, reconstruct the type and its variants from that evidence, compare it with principles.md, simple_programs.md, and the current src/ca runtime, propose only the smallest evidence-backed semantic reuse or extension, write an implementation-ready Goal 2 stage handoff, and re-integrate the finding into the global design before continuing.

Principle 0 governs the work: my directions and the current plan are hypotheses, not constraints to patch around. If a type does not compose naturally, stop, identify the failed assumption, re-derive the design from first principles, reopen affected stages, and record the necessary divergence. Never use family-specific rollouts, flags, compatibility shims, fallback conversions, opaque whole-state packing, fake fixed capacity, unrestricted formula/callback escape hatches, hidden executor state, weakened tests, or cosmetic interfaces that conceal different semantics.

Goal 1 is evidence, architecture, and Goal 2 planning only. Do not implement the expanded runtime or edit src/ca, tests, principles.md, or simple_programs.md. Keep all Goal 1 artifacts under goal-1/.

For every stage: sync against actual files; update 0-plan.md with current facts; select the first incomplete or newly reopened stage; create its stage file from the loop template; perform only that stage; record searches, complete excerpts with provenance, construction semantics, API/runtime fit, principles audit, rejected shortcuts, verification, and Goal 2 handoff; update evidence-index.md and design-ledger.md; fold the result back into 0-plan.md; then continue.

Do not mark a type complete until all aliases, variants, captions, Notes, Index references, cross-references, candidate matches, and false positives are accounted for. Search hits are not evidence until their context is read. CA-Types.md is a search guide, not a substitute for the book.

Completion means all 45 types have auditable evidence and design stages, every excerpt and semantic proposal is traceable, contradictions have been resolved rather than patched, the final construction algebra or algebras remain substantive and cohesive, and goal-2/goal-2-handoff.md provides a dependency-aware implementation and conformance plan covering every catalog row. Open issues must remain explicit next work; do not declare success around an easier subset.
```
