# 2-CH08-CLOSE

## Current Facts

- Chapter 8 and its Notes contain nine headings each.
- The compact register contains 24 leads citing the chapter and 51 citing its
  Notes; some leads can cite both documents.
- All inherited lead triggers now come directly from canonical source text.
- Chapter 8 was substantively reviewed earlier but has no Goal 5 closure.

## Updated Assumptions

- Most Chapter 8 material describes applications, properties, models, and
  observations rather than distinct executable constructions.
- Some physical and biological models may nevertheless define mechanics not
  captured by a familiar semantic name.
- Captions and figures need inspection only when the surrounding source leaves
  construction-defining mechanics unresolved.

## Big Picture Objective

Close Chapter 8 and its Notes compactly from canonical source, promote only
plausible executable mechanics or close cases, and carry genuine later-chapter
dependencies forward.

## Detailed Implementation Plan

- Read the chapter and its Notes sequentially.
- Record all 18 headings as covered.
- Review only the 75 document-citing raw leads against their canonical anchors.
- Add a new lead only for construction-bearing or genuinely ambiguous source
  omitted from the compact register.
- Classify obvious non-construction leads cheaply.
- Promote plausible constructions and close mechanical distinctions to
  `SERIOUS` without yet comparing them to T01–T45 or the proposed API.
- Inspect only figures required by a caption, serious lead, or unresolved
  mechanical ambiguity.
- Update `raw-leads.csv`, `coverage.md`, this stage file, and the plan.

## No-Cheating Checks

- Do not read catalog, API, runtime, prior-goal prose, or predecessor audit
  artifacts.
- Do not infer taxonomy from an inherited ID or an old semantic label; use
  canonical Book text.
- Do not create paragraph-level negative dispositions.
- Do not inspect decorative or merely illustrative figures.
- Do not add a full fingerprint to a weak lead.
- Do not ask a second agent to reread the same documents.

## Completion Requirements

- All nine chapter headings and nine Notes headings are covered sequentially.
- Every Chapter 8-citing lead is `WEAK`, `SERIOUS`, `RESOLVED`, or carries an
  explicit later-stage dependency.
- Every serious lead has canonical source anchors and a concise mechanical
  reason.
- Any inspected figure has a recorded taxonomy-bearing reason.
- New source-grounded leads, if any, are appended with unique Goal 5 IDs.
- `coverage.md` records 9/9 for both documents.
- Changes remain confined to Goal 5, `git diff --check` passes, and artifact
  growth remains compact.

## Stage Results

### Coverage

- One clean-context reader read the 770-line chapter and 358-line Notes file
  fully and sequentially. No second reader duplicated that work.
- Covered all nine chapter headings at lines 3, 5, 65, 115, 141, 227, 447,
  663, and 717.
- Covered all nine Notes headings at lines 1, 3, 17, 55, 74, 132, 160, 296,
  and 337.

### Serious or genuinely ambiguous mechanics

The following 28 inherited leads are `SERIOUS` pending mechanics-based
consolidation:

- `L1417`: synchronous displacement-field CA coupled to a mobile crack marker
  that selects a neighbor and destructively writes its destination
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:131-138`).
- `L1418`, `L1458–L1459`: hexagonal lattice-gas/block CA with discrete particle
  motion and collisions, alternating hexagon/dual-triangle blocks, reflective
  boundaries, injected flow, and an energy/temperature extension
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:155-165`;
  `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:107,124-126`).
- `L1421`: a metasystem that mutates a three-color nearest-neighbor CA program
  by adding or modifying rules (`CHAPTERS/08-Implications-for-Everyday-Systems.md:319-329`).
- `L1425`, `L1465–L1467`: phyllotaxis by repeatedly selecting the global field
  maximum, placing an element, applying a translated depletion kernel, and
  updating the cyclic concentration field; simultaneous placement is a
  scheduling variant (`CHAPTERS/08-Implications-for-Everyday-Systems.md:531-547`;
  `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:223-225`).
- `L1427` and part of `L1467`: differential sheet growth with an equal-cell-size
  embedding constraint. It remains open whether the Book defines an iterative
  relaxation or only a relation over acceptable outputs
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:563-569`;
  `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:226`).
- `L1429`, `L1468`: shell generation by progressive addition at a moving
  opening versus a direct parametric surface relation, including outside-only
  handling of self-intersection
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:581-591`;
  `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:234-246`).
- `L1430`, `L1469`: curve generation from intrinsic curvature as a function of
  arc length, integrated into position and heading
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:613-617`;
  `BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:253-271`).
- `L1443–L1447`: one overpacked source group covering ordinary DLA, its
  conserved-mobile-particle CA analogue, and a boiling continuous CA. These
  mechanics must be split during Stage 8 before fingerprinting
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:50-51`).
- `L1448–L1453`: alternative fracture constructions: minimum-total-strength
  paths through random-strength bonds, identical springs that fail past a
  stretch threshold, a three-color CA without a special crack marker, and
  stochastic repeated binary fragmentation
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:59-66`).
- `L1460`: discrete streams choose random directions and coalesce irreversibly
  on meeting, producing a drainage tree
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:130`).
- `L1477–L1478`: a continuous vector concentration field with diffusion and
  nonlinear reaction terms
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:322-328`).

This is a shortlist of leads, not a claim that Chapter 8 contains 28 distinct
types.

### Cheap dispositions

- `RESOLVED`: `L1414–L1416`, `L1419`, `L1422–L1423`, `L1428`,
  `L1432–L1435`, `L1437–L1440`, `L1462`, `L1464`, `L1475–L1476`,
  `L1479–L1484`, and new leads `L1489–L1491`.
  These are ordinary CA/substitution applications, parameters, seeds,
  observers, implementation formulas, or application aliases rather than new
  mechanics.
- `WEAK`: `L1420`, `L1424`, `L1426`, `L1436`, `L1442`, `L1454`, `L1456`,
  `L1463`, and `L1486–L1488`.
  These are narratives, named parameter choices, renderings, observed
  morphologies, measurements, heuristics, examples, statistics, or application
  domains.

### Explicit later-stage dependencies

The following remain `UNREVIEWED`, with their dependency recorded here:

- `L1431`: genetic-program section selection requires comparison with later
  substitution/control constructions.
- `L1441`: historical crystal-growth references require the later
  aggregation/constraint comparison.
- `L1455`, `L1457`: Navier–Stokes and Lorenz material requires the later
  continuum-equation and uniterated-relation inventory.
- `L1461`: natural-selection program mutation depends on the Chapter 11
  universality and Chapter 12 limitation discussions.
- `L1470–L1474`: embryonic substitution, lineage modification, growth,
  aggregation, and self-assembly references require their cross-chapter
  mechanics.
- `L1485`: hierarchical-network/agent market mechanics are deferred to their
  referenced treatment.
- New `L1492`: vorticity-based fluid elements are named but no transition rule
  is supplied here.

### New leads

- `L1489` (`RESOLVED`): discrete large-scale eddies at discrete positions
  interacting through an ordinary CA rule
  (`CHAPTERS/08-Implications-for-Everyday-Systems.md:215`).
- `L1490` (`RESOLVED`): rapid dynamics of a third CA color used to emulate an
  effectively long-range field; an implementation technique
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:45`).
- `L1491` (`RESOLVED`): multiple crystal seeds and optional per-seed
  characteristics yielding Voronoi-like boundaries; a seed recipe plus
  observation
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:46`).
- `L1492` (`UNREVIEWED`, later dependency): discrete-vorticity fluid elements
  with no local transition supplied
  (`BACK-MATTER/NOTES/08-Implications-for-Everyday-Systems-Notes.md:109`).

### Selective figure inspection

- Inspected
  `CHAPTERS/_page_390_Figure_4.jpeg` at original 911×550 resolution because the
  fracture architecture is partly visual. It confirms CA backgrounds for rules
  150, 22, and 122 with an overlaid mobile crack path, but supplies no further
  lookup table; the text remains the mechanics authority for `L1417`.
- Inspected
  `CHAPTERS/_page_393_Figure_2.jpeg` at original 1290×1253 resolution because
  the collision replacements are absent from Markdown prose. It shows the
  local hexagonal/triangular collision cases, particle-scale evolution,
  block-velocity observers, and moving reference frame; only the collision
  cases bear on the construction.
- No other Chapter 8 image requires original-resolution inspection. Captions
  and Notes formulas already specify the relevant mechanics, while remaining
  images show behavior or parameter choices.

### Completion

- All 75 inherited Chapter 8 leads are accounted for exactly once: 28 serious,
  25 resolved, 11 weak, and 11 explicit later-stage dependencies.
- Four source-grounded leads were added: three resolved and one deferred.
  Chapter 8 therefore closes with 79 total leads: 28 serious, 28 resolved, 11
  weak, and 12 deferred.
- `raw-leads.csv` now contains 1,492 rows in approximately 533 KB.
- `coverage.md` records 9/9 headings for both documents.
- No catalog, API, runtime, prior-goal prose, or predecessor audit machinery was
  used.
- Next: Stage 3, `CH09`.
