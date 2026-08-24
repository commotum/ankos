# Goal 9 Continuation Prompt

```text
Work through /home/jake/Developer/ankos/goal-9/0-plan.md using
/home/jake/Developer/ankos/goal-9/0-loop.md.

Objective: replace the current type-heavy ANKoS runtime with a minimal,
coordinate-first kernel based on ordinary Python values:

SPACE + ALPHABET + NEIGHBORHOOD + RULE -> SIMPLEPROGRAM
SIMPLEPROGRAM + SEED -> TRAJECTORY
rollout(TRAJECTORY, limit/resources) -> EPISODE

Build the refactor itself, not any presets. The completed goal must be ready
for a later goal to implement canonical presets one at a time.

Non-negotiable constraints:
- Replace loci.py with a new selector.py built from ordinary coordinates and
  small selector functions; do not carry the Locus/Region hierarchy forward.
- Remove semantic Frontier and all required write-capability machinery.
- Use no inheritance, generics, semantic family classes, Preset class,
  compatibility proof framework, certificates, evidence trees, or denotation
  DSL unless a concrete requirement in this goal proves one unavoidable.
- Shape/support is realized by Seed; boundary and coordinate law belong to
  Space; Neighborhood reads; one exact callable Rule constructs successor
  values.
- Every step appends a complete immutable state at explicit t+1 addresses.
- Do not wrap or fall back to the old runtime to make tests pass.
- Canonical catalog names may remain only as honest unimplemented progress
  stubs. Stub presence is not implementation.
- Do not create ECA, Turing-machine, family, or dataset presets in this goal.

For each stage: inspect current files and tests, update 0-plan.md with facts,
create the stage file from the template, implement only that stage, run focused
and full relevant verification, record exact results, fold discoveries back
into the plan, and continue to the first incomplete stage.

Completion means the live ca package uses the primitive execution path,
loci.py and frontiers.py are gone, Cartesian and relational anonymous fixtures
prove immutable explicit-time execution, obsolete ceremony tests are removed,
and the public API is genuinely ready for the first later preset. Carry every
remaining issue forward explicitly rather than weakening this finish line.
```
