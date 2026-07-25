# 14-CENSUS

## Final Result

- 1,564 raw leads resolve to 190 serious source leads, 867 resolved leads, and
  507 weak leads.
- The serious evidence resolves to 102 full candidates: 60 executable roots,
  35 presets/variants, and 7 close candidates.
- The final inventory contains 60 executable semantic families and two
  close-only groups.
- T01–T45 cover 19 executable families. Forty-one executable families are
  source-grounded catalog additions.
- All 60 executable families fit
  `SimpleProgram(seed, alphabet, frontier, neighborhood, rule)`.
- No sixth top-level API field and no configurable `UpdatePolicy` is justified.
- No serious discovery, family, catalog, hostile-review, or API question
  remains unresolved.

The implementation-facing results are:

- `taxonomy-census.md`
- `api-pressure.md`
- `integration-handoff.md`

## Final Verification

- `raw-leads.csv` and `source-decision-matrix.csv` contain the exact ordered
  range L0001–L1564 with identical terminal statuses.
- Status counts are exactly 190 `SERIOUS`, 867 `RESOLVED`, and 507 `WEAK`.
- `candidates.md` contains exactly C001–C102, and every candidate has at least
  one serious source row.
- Every serious matrix row maps to exactly one candidate and that candidate's
  one final family.
- `11-FAMILIES.md` contains 62 rows: 60 executable and two close-only. The
  catalog relation is exactly 19 covered, 41 proposed additions, and two
  non-family roles.
- Candidate roles across those rows are exactly 60 executable roots, 35
  presets/variants, and seven close exclusions, with no duplicate or missing
  candidate.
- `api-pressure.md` contains exactly one mapping for every retained family:
  60 `fits-five` and two `close-role`.
- The census lists every retained family exactly once with the same stable ID
  and slug as the family and API reports.
- T01–T45 appear exactly once. Row dispositions are 15 `retain-family`, 21
  `retain-preset`, two `merge`, three `repair`, two `alias`, one `retire-role`,
  and one `split`.
- All 4,309 matrix source anchors resolve within 25 canonical Markdown
  documents and their line ranges exist.
- Chapters 8–12 and their Notes remain heading-complete; the two additional
  mechanics-bearing figures have explicit selective-inspection reasons.
- The frozen 40-query saturation pass was not rerun; its one bad Q037
  disposition is explicitly corrected.
- The single independent hostile review's six material findings are all
  incorporated.
- `git diff --check` passes.
- Repository changes are confined to `goal-5`.
- `goal-5` is approximately 1.4 MiB. Its only large files are the required
  1,564-row raw register and compact source-decision matrix, followed by the
  human-readable candidate and API reports; it contains no copied Book corpus,
  raw search dump, transaction history, replay system, or generated validator.

## Handoff

Goal 5 is closed. The recommended next authorized goal is Goal 6: remaster the
frozen Goal 2 architecture and implementation plan around the five-field API
and this 60-family coverage inventory. Goal 7 can then implement that remaster.
No whole-Book rediscovery is required.

