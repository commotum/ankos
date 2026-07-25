# 7-INDEX-CHECK

## Current Facts

- The Index has 5,484 top-level entries and approximately 83,000 words.
- Goal 5 does not treat those entries as independent source units.
- Sequential discovery is complete through Chapter 12.
- The compact register contains 1,563 leads, of which 81 are currently serious;
  these remain leads rather than type counts.

## Updated Assumptions

- The Index will mainly expose aliases, historical names, and additional source
  references for already discovered mechanics.
- Generic entries such as “cellular automata” or “computation” are too broad to
  inspect exhaustively.
- A bounded checklist built from discovered mechanism names and close aliases
  is sufficient when followed by the later whole-book saturation pass.

## Big Picture Objective

Use the Index as a targeted omission and alias challenge without reading or
dispositioning all 5,484 entries.

## Detailed Implementation Plan

- Build a compact checklist from the mechanics named in Goal 5 stage results
  and surface labels mechanically extractable from the raw-lead register.
- Group synonyms under cellular, rewriting, network, numeric, continuous,
  stochastic/growth, relation/constraint, analysis, memory, and computation
  families.
- Search only the Index for those terms and their explicit `see`/`see also`
  aliases.
- Follow a referenced Book location only when it is absent from the register or
  raises a genuine mechanical ambiguity.
- Add a raw lead only for a source-grounded omitted mechanism.
- Record checked terms and outcomes compactly in this stage file; do not retain
  a raw hit dump.

## No-Cheating Checks

- Do not read the Index sequentially or create one row per Index entry.
- Do not search the catalog, API, runtime, or prior-goal material.
- Do not treat a new name, person, application, theorem, property, or page
  reference as a new construction without source mechanics.
- Do not repeat the whole-book saturation pass reserved for Stage 9.
- Do not build a generalized Index parser or permanent search tool.

## Completion Requirements

- The checklist covers all discovered mechanism families and close aliases.
- Every explicit Index alias reached by the checklist is checked.
- Every genuinely new source location is inspected in canonical source.
- Any omitted mechanism is added to `raw-leads.csv` with a canonical anchor.
- The checked-term/result summary is compact and no line-by-line Index ledger
  exists.
- `coverage.md` marks the Index checklist complete.
- Changes remain confined to Goal 5, `git diff --check` passes, and artifact
  growth remains compact.

## Stage Results

- Pending.

