# Goal 5: Lean Whole-Book Construction Taxonomy

Shorthand: **Lean Taxonomy**

## Big-Picture Objective

Finish the whole-book *A New Kind of Science* construction taxonomy with enough
rigor to guide the catalog, the minimal `SimpleProgram` API, and the later
implementation plan—without building or extending a forensic audit system.

Goal 5 is the sole active completion contract for the unfinished whole-book
taxonomy investigation. Earlier audit artifacts remain preserved and inert;
their plans, prose, tools, histories, search archives, validators, and
transaction machinery are not operating context for this goal.

The work must:

- cleanly close Chapter 8 from the canonical Book source;
- read Chapters 9–12 and their Notes sequentially;
- retain only construction-bearing and genuinely ambiguous evidence;
- distinguish cheap raw leads from serious taxonomy candidates;
- inspect only figures that can materially affect the taxonomy;
- use the Index as an omission checklist rather than a line-by-line corpus;
- consolidate all inherited and newly discovered leads by mechanics;
- perform one whole-book search saturation pass;
- reconcile the resulting shortlist against T01–T45 only after discovery is
  frozen;
- identify semantic families and pressure-test `simple_programs.md` and
  `api.md`;
- perform one independent hostile review; and
- produce a compact source-to-decision matrix and an actionable integration
  handoff.

This goal plans and completes research and architecture analysis. It does not
modify the current catalog, API, runtime, tests, Goal 1, or Goal 2 unless the
user separately authorizes integration after the final handoff.

## Clean Context Boundary

Goal 5 must be understandable from:

- `goal-5/0-plan.md`;
- `goal-5/0-loop.md`;
- the canonical Book Markdown and relevant original-resolution figures under
  `ref/A-New-Kind-of-Science/`; and
- after blind discovery is frozen, `ref/notes/CA-Types.csv`,
  `ref/notes/CA-Types.md`, `simple_programs.md`, `api.md`, Goal 1's completed
  conclusions, and Goal 2's frozen handoff.

Do not open, summarize, import, execute, or rely on any predecessor plan, loop,
prompt, stage report, history ledger, search archive, route ledger, validator,
test harness, helper program, generated accepted-output payload, or transaction
record.

There is one narrow exception needed to preserve prior discovery work:

- Stage 1 may mechanically stream the existing raw-candidate data store once
  and project only a legacy lead identifier, canonical source anchor, and short
  surface trigger into a compact Goal 5 register.
- Because the raw store uses opaque source-unit IDs, Stage 1 may also
  mechanically read the existing data-only source-unit map solely to translate
  each ID to a canonical document and line range. The surface trigger must be
  derived directly from the canonical Markdown.
- The projection must not copy prior conclusions, semantic fingerprints,
  dispositions, confidence scores, search metadata, verification metadata, or
  surrounding prose.
- The source store must not be loaded wholesale into model context.
- After the projection is verified by count and sampled source anchors, Goal 5
  uses only its compact register and the canonical Book.

This exception is a data bridge, not an inherited methodology.

## Non-Negotiable Constraints

1. **Preserve earlier work.** Do not delete or modify predecessor artifacts.
   Preservation does not make them governing context.
2. **Canonical-source authority.** Taxonomy claims must ultimately be supported
   by the repaired canonical Book Markdown and, when needed, its corresponding
   original-resolution figure.
3. **Blind discovery first.** Do not use T01–T45, the proposed API, Goal 1
   conclusions, Goal 2, or current runtime capabilities to decide what exists
   in Chapters 8–12, the Index, or saturation searches.
4. **Sequential chapter reading.** Read each assigned chapter and its Notes in
   source order. Record section-level coverage, not a disposition for every
   paragraph.
5. **Evidence selectivity.** Retain only passages that describe a construction,
   may describe a construction, distinguish close mechanisms, or create a
   material ambiguity. Ordinary exposition requires no negative record.
6. **Cheap leads, expensive candidates.** A raw lead receives only an ID,
   source anchor, surface trigger, and status. Full semantic analysis is
   reserved for serious candidates, existing catalog obligations, proposed
   additions, and genuinely close exclusions.
7. **Mechanics before names.** Consolidate by what the system does, not by the
   Book's changing names, chapter topic, visual appearance, or existing catalog
   labels.
8. **Selective image inspection.** Inspect an image only when its caption,
   surrounding text, raw lead, or unresolved ambiguity indicates that the image
   may define or distinguish a construction. Decorative and merely
   illustrative images need no individual disposition.
9. **Index as checklist.** Use names, aliases, page references, and mechanism
   terms in the Index to challenge omissions. Do not review every Index line as
   an independent source unit.
10. **One saturation pass.** Run one whole-book search sweep after sequential
    reading and consolidation. Inspect new or unresolved hits. Do not perform
    identical verification reruns.
11. **One hostile review.** Use one independent final challenge focused on
    plausible additions, close collapses, exclusions, source omissions, and API
    counterexamples. Do not create nested per-stage hostile-review systems.
12. **No infrastructure project.** Do not create append-only histories,
    transaction replay, accepted-output programs, generalized validators,
    duplicate execution bundles, mutation suites, relocation suites, or
    chapter-specific generated software.
13. **Human-readable artifacts.** Prefer compact Markdown and CSV. Do not embed
    full Book chapters, complete search output, giant JSON snapshots, or
    duplicated source text.
14. **Token discipline.** Project large inputs to needed fields, inspect them in
    bounded batches, summarize once, and avoid redundant agents rereading the
    same material. Parallel work is allowed only for distinct, non-overlapping
    tasks.
15. **No implementation drift.** Goal 5 produces decisions and a handoff. It
    does not silently edit the catalog, API, runtime, tests, or prior goals.
16. **No false completeness.** An unresolved serious candidate, missing source
    anchor, unexplained T01–T45 mismatch, or unanswered API counterexample keeps
    the relevant stage open.

## Working Definitions

### Raw lead

A cheap pointer to a passage, caption, figure, Notes entry, or Index alias that
might bear on a construction. Required fields:

- stable Goal 5 lead ID;
- inherited identifier when applicable;
- canonical source anchor;
- short surface trigger;
- status: `UNREVIEWED`, `WEAK`, `SERIOUS`, or `RESOLVED`.

A raw lead is not a type and carries no full semantic fingerprint.

### Serious candidate

A source-grounded possibility that may be:

- a distinct executable construction;
- a material variant of a known construction;
- a close exclusion whose equivalence is not obvious; or
- a catalog obligation whose mechanics need an explicit home.

Serious candidates receive full analysis.

### Non-construction role

Something relevant to examples or explanations but not itself a distinct
executable construction, such as:

- a seed or initial-condition recipe;
- a preset or named parameter choice;
- an observer, renderer, measurement, or projection;
- a property, behavior, theorem, or empirical class;
- an implementation technique;
- an application domain or metaphor; or
- a duplicate name for already captured mechanics.

### Semantic family

A group of constructions that share the same essential state-transition
mechanics and differ only through explicit data, parameters, schedules, domains,
or aliases that the common abstraction can honestly represent.

Visual resemblance or a shared Book label is not sufficient. Conversely,
different Book names do not require different implementation classes.

### Full semantic fingerprint

For a serious candidate, record only the dimensions needed to decide identity,
family membership, and API fit:

- state carrier and alphabet;
- support or domain;
- initialization semantics;
- loci eligible to act or change;
- information read;
- transformation and effects produced;
- scheduling and commit semantics;
- termination or non-result behavior;
- observer/output semantics when construction-defining;
- defining parameters and variants;
- source anchors;
- smallest distinguishing example or counterexample.

## Current Facts

- The repaired canonical Book contains Chapters 1–12, their Notes, front
  matter, back matter, the Index, and extracted figures.
- Goal 1 completed an investigation of the current 45-row seed catalog and
  produced a frozen implementation handoff.
- That 45-row catalog is not yet proven exhaustive relative to the whole Book.
- Earlier blind work covered the bookends and Chapters 1–7 and substantively
  reviewed Chapter 8.
- The inherited raw-candidate store contains 1,488 provisional leads. They are
  coverage pointers, not 1,488 types.
- Each inherited lead has at least one source-unit ID. The raw store does not
  itself contain canonical file and line anchors, so Stage 1 must translate
  those IDs through the data-only source-unit map and derive the corresponding
  source text from canonical Markdown.
- Chapter 8 still needs a compact, source-grounded Goal 5 closure.
- Chapters 9–12, their Notes, and the Index still require the lean protocol.
- The final consolidation, reconciliation, family inventory, API-pressure
  analysis, hostile review, and census have not been completed.
- Goal 2 is frozen for comparison and must not be remastered until Goal 5
  produces its final handoff.

## Assumptions To Challenge

- Most inherited raw leads will collapse into examples, presets, properties,
  observers, aliases, or duplicate descriptions.
- Chapters 9–12 may introduce fewer new executable mechanics than Chapters 3–5,
  but their conceptual vocabulary may conceal constructions under non-program
  language.
- The Index will mostly expose aliases and missed references rather than define
  new constructions.
- The minimal `SimpleProgram` components may cover all retained families, but
  only family-by-family counterexamples can establish this.
- Semantic names can usually remain aliases or presets rather than public API
  classes.
- A single strong saturation pass and a single independent hostile review can
  provide adequate omission resistance without exhaustive negative evidence.

## Required Goal 5 Artifacts

Create artifacts only when their stage begins:

- `goal-5/coverage.md`: section-level reading and selective-image coverage.
- `goal-5/raw-leads.csv`: compact inherited and newly discovered lead register.
- `goal-5/candidates.md`: serious candidates and their semantic fingerprints.
- `goal-5/source-decision-matrix.csv`: one compact source-to-final-decision map.
- `goal-5/taxonomy-census.md`: final catalog and semantic-family conclusions.
- `goal-5/api-pressure.md`: family-by-family fit against the minimal API.
- `goal-5/integration-handoff.md`: exact proposed catalog, planning, and API
  changes for a later authorized goal.

Do not create empty placeholders in advance.

## Success Metrics

Goal 5 succeeds only when:

- Chapter 8 has a compact closure grounded in its chapter, Notes, and relevant
  figures.
- Chapters 9–12 and their Notes have been read sequentially with complete
  section-level coverage.
- Every figure with a credible chance of defining or distinguishing a
  construction has been inspected at sufficient resolution.
- The Index has challenged all discovered names, aliases, and mechanism terms.
- Every inherited and new raw lead maps to a serious candidate, a mechanics
  cluster, or a concise non-construction disposition.
- One whole-book search pass produces no unresolved serious lead.
- Every serious candidate has a complete semantic fingerprint and source
  anchors.
- Every T01–T45 entry maps to exactly one final disposition and one semantic
  family or receives an explicit split/merge/retirement proposal.
- Every proposed addition and every close exclusion has a distinguishing
  example, equivalence argument, or counterexample.
- The semantic-family inventory distinguishes executable mechanics from
  aliases, presets, seeds, observers, properties, and renderings.
- Every retained family has a clear fit, extension, or counterexample against
  `SimpleProgram(seed, alphabet, frontier, neighborhood, rule)`.
- One independent hostile review has been resolved.
- The final census states the number of serious constructions, semantic
  families, proposed catalog additions, and unresolved questions.
- The integration handoff is concrete enough to scaffold the later Goal 2/API
  remaster without reopening Book discovery.

## Verification Requirements

- Confirm canonical source anchors exist and sampled excerpts match their
  source.
- Confirm sequential coverage includes every heading in Chapters 8–12 and their
  Notes.
- Confirm selective-image decisions are traceable from a caption, passage,
  lead, or ambiguity.
- Confirm inherited lead projection preserves the discovered record count while
  excluding prior judgments and verification metadata.
- Confirm every raw lead has exactly one terminal mapping by finalization.
- Confirm every serious candidate appears exactly once in the final candidate
  inventory.
- Confirm every T01–T45 identifier appears exactly once in reconciliation.
- Confirm every proposed catalog addition is source-grounded and mechanically
  non-equivalent to retained entries.
- Confirm every family is tested against the minimal API with at least one
  canonical example and every claimed API gap with a concrete counterexample.
- Confirm the saturation query set covers discovered names, aliases, and
  mechanism vocabulary and that all new hits are dispositioned.
- Confirm hostile-review findings are either incorporated or rebutted with
  source evidence.
- Run lightweight structural checks appropriate to the artifacts, plus
  `git diff --check`.
- Confirm Goal 5 did not modify the Book, current catalog, API, runtime, tests,
  or prior goals.
- Inspect `du -sh goal-5` and the largest Goal 5 files. Unexpected bulk,
  embedded source corpora, or machine histories is a verification failure.

## Stages

### 1-CUTOVER

Status: **IN PROGRESS**.

#### Big Picture Objective

Establish the clean Goal 5 operating boundary and preserve prior discovery
through a compact, conclusion-free raw-lead projection.

#### Detailed Implementation Plan

- Verify the canonical Book and Goal 5 scaffold are present.
- Record section-level baseline coverage in `coverage.md`.
- Mechanically locate and stream the inherited raw-candidate store without
  opening adjacent predecessor materials.
- Create `raw-leads.csv` with only Goal 5 ID, inherited ID, canonical source
  anchor, short surface trigger, and `UNREVIEWED` status.
- Verify the projected record count and sample anchors against the canonical
  Book.
- Record that this plan supersedes every earlier unfinished taxonomy-audit
  completion contract while preserving earlier files unchanged.
- Measure Goal 5 artifact sizes and confirm the new working set is compact.

#### Completion Requirements

- The clean-context boundary is recorded in the Stage 1 result.
- All inherited raw leads are represented exactly once in the compact register.
- No predecessor judgment, prose report, verification metadata, history, search
  archive, or code has been imported.
- Sampled source anchors resolve in the canonical Book.
- Earlier artifacts and all non-Goal-5 files remain unchanged.

### 2-CH08-CLOSE

#### Big Picture Objective

Close Chapter 8 and its Notes in a compact, source-grounded form without
repairing or reviving prior audit machinery.

#### Detailed Implementation Plan

- Read Chapter 8 and its Notes sequentially from the canonical Markdown.
- Record heading-level coverage.
- Review inherited Chapter 8 leads against their source passages.
- Inspect only figures implicated by relevant captions, passages, leads, or
  unresolved mechanical ambiguity.
- Add any newly discovered raw leads.
- Mark obvious weak leads concisely and promote plausible constructions or
  close cases to `SERIOUS`.
- Carry genuine cross-chapter questions forward explicitly rather than resolving
  them by assumption.
- Record the compact Chapter 8 findings in the stage file and shared registers.

#### Completion Requirements

- Every Chapter 8 and Chapter 8 Notes heading is covered.
- Every Chapter 8 raw lead is mapped to a status or an explicit later-stage
  dependency.
- Every inspected figure has a concrete taxonomy reason.
- All serious Chapter 8 candidates have source anchors.
- No per-paragraph negative ledger or predecessor transaction repair exists.

### 3-CH09

#### Big Picture Objective

Discover construction-bearing mechanics in Chapter 9 and its Notes.

#### Detailed Implementation Plan

- Read the chapter and Notes sequentially.
- Record heading-level coverage.
- Capture only construction-bearing or genuinely ambiguous passages.
- Add cheap raw leads before performing semantic analysis.
- Inspect only candidate-bearing, text-bearing, or ambiguity-resolving figures.
- Promote only plausible distinct mechanics or close cases to serious
  candidates.
- Preserve unresolved forward references for later routing.

#### Completion Requirements

- Every Chapter 9 and Chapter 9 Notes heading is covered.
- All retained evidence has canonical source anchors.
- Selective figure inspection is justified and recorded.
- No ordinary exposition receives a gratuitous negative disposition.
- All serious candidates and unresolved questions are explicit.

### 4-CH10

#### Big Picture Objective

Discover construction-bearing mechanics in Chapter 10 and its Notes.

#### Detailed Implementation Plan

- Apply the same sequential, evidence-selective protocol as Stage 3.
- Pay particular attention to whether perception and analysis procedures are
  executable constructions, observers, measurements, or properties.
- Use distinguishing examples when a procedure might define a separate
  transition system.

#### Completion Requirements

- Every Chapter 10 and Chapter 10 Notes heading is covered.
- Retained leads and serious candidates are source-grounded.
- Observer/measurement claims are not promoted to constructions without
  mechanical evidence.
- Relevant figures and unresolved questions are accounted for.

### 5-CH11

#### Big Picture Objective

Discover construction-bearing mechanics in Chapter 11 and its Notes.

#### Detailed Implementation Plan

- Apply the same sequential, evidence-selective protocol as Stage 3.
- Distinguish executable computation models from universality claims,
  encodings, simulations, proofs, and historical commentary.
- Record concrete mechanics and defining variants without using T01–T45 as a
  checklist.

#### Completion Requirements

- Every Chapter 11 and Chapter 11 Notes heading is covered.
- Executable constructions are separated from properties and encodings.
- All retained evidence and relevant figures are source-grounded.
- Serious candidates and unresolved equivalence questions are explicit.

### 6-CH12

#### Big Picture Objective

Discover construction-bearing mechanics in Chapter 12 and its Notes.

#### Detailed Implementation Plan

- Apply the same sequential, evidence-selective protocol as Stage 3.
- Separate principles and claims about computational behavior from actual
  constructions used to instantiate or demonstrate them.
- Capture any late aliases, variants, or counterexamples relevant to earlier
  candidates.

#### Completion Requirements

- Every Chapter 12 and Chapter 12 Notes heading is covered.
- Principles and behavioral claims are not mistaken for executable families.
- All retained evidence and relevant figures are source-grounded.
- Cross-chapter questions needed for consolidation are explicit.

### 7-INDEX-CHECK

#### Big Picture Objective

Use the Index as a compact omission and alias challenge.

#### Detailed Implementation Plan

- Build a checklist from discovered construction names, aliases, historical
  names, and mechanism vocabulary.
- Inspect relevant Index entries and their referenced Book locations.
- Add a raw lead only when an entry exposes an unreviewed source location,
  plausible alias, or genuinely new mechanism.
- Record checked terms and outcomes compactly in the stage file.
- Do not disposition unrelated Index lines.

#### Completion Requirements

- Every discovered name and alias has been challenged through the Index.
- Every relevant new page reference is checked against canonical source.
- All new leads are registered.
- No line-by-line Index ledger is created.

### 8-CONSOLIDATE

#### Big Picture Objective

Reduce the raw leads to mechanics-based clusters and a defensible shortlist of
serious candidates.

#### Detailed Implementation Plan

- Work through `raw-leads.csv` in bounded batches without loading it wholesale.
- Group leads by state carrier, domain, initialization, acting loci, readable
  information, transformation/effects, scheduling/commit, termination, and
  defining output semantics.
- Merge aliases and duplicate descriptions.
- Disposition weak leads concisely as preset, seed, observer, property,
  rendering, example, implementation technique, domain metaphor, duplicate, or
  insufficient evidence.
- Promote plausible distinct mechanics and close cases to `candidates.md`.
- Write full semantic fingerprints only for serious candidates.
- Retain raw-lead-to-candidate or raw-lead-to-disposition mappings in the compact
  source-decision matrix.

#### Completion Requirements

- Every raw lead has a mechanics cluster or concise disposition.
- Duplicate names do not create duplicate candidates.
- Every serious candidate has a complete semantic fingerprint and source
  anchors.
- Close merges include a distinguishing test or equivalence argument.
- The shortlist is small enough to review directly and no candidate exists only
  because of a Book label.

### 9-SATURATION

#### Big Picture Objective

Run one whole-book search sweep to find omissions after sequential discovery and
initial consolidation.

#### Detailed Implementation Plan

- Derive one query set from discovered names, aliases, mechanism nouns, mechanism
  verbs, and unresolved distinctions.
- Search the canonical Book, Notes, front matter, back matter, and Index once.
- Inspect only hits not already represented by a source decision.
- Register and classify new leads.
- Reopen consolidation only for actual new evidence.
- Record queries, hit counts, and new decisions compactly; do not retain giant
  raw search dumps.

#### Completion Requirements

- The query set covers all discovered vocabulary and known alias families.
- Every novel or unresolved hit is dispositioned.
- Any new serious candidate receives a semantic fingerprint.
- No unresolved serious search hit remains.
- No identical verification rerun or per-chapter search archive is created.

### 10-RECONCILE

#### Big Picture Objective

Freeze blind discovery and reconcile the serious shortlist against T01–T45.

#### Detailed Implementation Plan

- Record the discovery freeze before opening catalog or prior design materials.
- Read `CA-Types.csv` and only the catalog/design evidence required for each
  comparison.
- Map every T01–T45 entry to one serious candidate or an explicit
  merge/split/retirement outcome.
- Identify source-grounded additions without renumbering the existing catalog.
- Distinguish catalog aliases and semantic roles from executable families.
- Record exact mismatches and later integration obligations.

#### Completion Requirements

- Discovery was frozen before catalog comparison.
- Every T01–T45 identifier appears exactly once in reconciliation.
- Every unmatched serious candidate has an explicit proposed disposition.
- Every addition, split, merge, or retirement has source evidence and a
  mechanical argument.
- No catalog name is treated as proof of a separate family.

### 11-FAMILIES

#### Big Picture Objective

Produce the final semantic-family inventory independently of public API class
names.

#### Detailed Implementation Plan

- Cluster reconciled candidates by essential transition mechanics.
- Identify which distinctions are parameters, presets, aliases, seeds,
  schedules, observers, or genuinely different primitives.
- Use smallest distinguishing examples and counterexamples to test close
  collapses.
- Finalize the catalog-action and family-action dimensions in
  `source-decision-matrix.csv`.
- Record counts of raw leads, serious candidates, executable constructions,
  semantic families, catalog aliases, and proposed additions.

#### Completion Requirements

- Every serious candidate has exactly one family disposition.
- Each family has a concise defining mechanism and representative sources.
- Close family boundaries have explicit equivalence or counterexample evidence.
- Non-construction roles are kept outside the executable-family count.
- The family inventory is complete enough for API analysis.

### 12-API-PRESSURE

#### Big Picture Objective

Test whether every retained family fits the elegant minimal API and identify the
smallest honest changes where it does not.

#### Detailed Implementation Plan

- Read `simple_programs.md`, `api.md`, the relevant completed design conclusions,
  and the frozen Goal 2 handoff.
- Map each semantic family to:
  `seed`, `alphabet`, `frontier`, `neighborhood`, and `rule`.
- Treat semantic construction names as aliases or presets unless a concrete
  counterexample requires a new primitive.
- Test state generation, nonlocal readable regions, multi-target atomic writes,
  constraints, uniterated relations, termination, stochasticity, and
  observer/output boundaries where relevant.
- For every claimed API gap, provide a minimal construction that cannot be
  represented honestly.
- Write `api-pressure.md` with retained primitives, aliases/presets, genuine
  extensions, rejected extensions, and Goal 2 consequences.

#### Completion Requirements

- Every retained family has a documented API mapping.
- Every proposed API addition has a concrete counterexample to the unextended
  API.
- No semantic Book name becomes a public class merely for convenience.
- Seeds, observers, renderers, and properties remain separate unless source
  mechanics prove they are construction-defining.
- Goal 2 repair obligations are explicit but not implemented.

### 13-HOSTILE-REVIEW

#### Big Picture Objective

Perform one strong independent challenge of the nearly final taxonomy and API
conclusions.

#### Detailed Implementation Plan

- Give the reviewer the canonical sources, compact Goal 5 artifacts, and final
  questions—not predecessor audit machinery.
- Challenge proposed additions, close merges, exclusions, omitted aliases,
  selective-image choices, saturation coverage, and API-fit claims.
- Sample source locations across every chapter and Notes range.
- Require concrete source evidence or counterexamples for objections.
- Resolve each material finding in the compact artifacts.

#### Completion Requirements

- One independent hostile review is complete.
- Every material finding is incorporated or rebutted with evidence.
- New evidence is routed back through consolidation, reconciliation, family, and
  API decisions as needed.
- No second nested review framework is created.
- No serious objection remains unresolved.

### 14-CENSUS

#### Big Picture Objective

Publish the final whole-book taxonomy answer and a dependency-aware handoff for
later authorized integration.

#### Detailed Implementation Plan

- Finalize `source-decision-matrix.csv`.
- Write `taxonomy-census.md` with exact counts, family definitions, catalog
  dispositions, additions, aliases, exclusions, and remaining uncertainties.
- Finalize `api-pressure.md`.
- Write `integration-handoff.md` with exact proposed changes to the catalog,
  Goal 1 conclusions if necessary, Goal 2/API planning, and the later
  implementation scaffold.
- Verify all success metrics and repository-scope constraints.
- Run lightweight structural checks, `git diff --check`, and artifact-size
  inspection.

#### Completion Requirements

- The final census directly answers what constructions the whole Book contains,
  how many serious constructions and semantic families remain, and what the
  current catalog misses or misclassifies.
- Every final decision traces to canonical source.
- The API report states whether the minimal API survives and lists only
  evidence-required changes.
- The handoff is implementation-ready without reopening Book discovery.
- All verification requirements pass.
- Goal 5 remains compact, human-readable, and free of inherited audit
  infrastructure.
