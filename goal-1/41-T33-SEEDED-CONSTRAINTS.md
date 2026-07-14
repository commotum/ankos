# 41-T33-SEEDED-CONSTRAINTS

Status: **IN PROGRESS — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, AND D135 INTEGRATION CLOSED; INDEPENDENT HOSTILE REVIEW PENDING**

## Current Facts

- T33 is CSV physical line 34, `Seeded Template Constraint Systems`; `ref/notes/CA-Types.md` section 33 is search vocabulary, not primary mechanics.
- “Seeded” is a potentially misleading catalog name. The Book does not supply an initial configuration or an evolution. It strengthens T32 by requiring a specified local template to occur at least once somewhere in the complete pattern (`BOOK:2632-2640`).
- The native strict profile remains a static discrete 2D binary square-lattice relation with no native `t` axis. A model is one total field, not a trajectory, and an occurrence witness is not transition state.
- The required occurrence is unanchored. Figures put a witness at the center and the search procedure begins there because translation symmetry permits a convenient representative; the nonperiodic example is unique only up to translations (`BOOK:2640`, `2664`, `2674`, `14086-14095`).
- The local allowed-pattern relation remains unchanged everywhere. T33 adds a global existential conjunct; it does not add a distinguished firing locus, boundary condition, fixed center, seed state, or repair update.
- The strict syntax has `32 * 2^32 = 137,438,953,472` source-counted constraint pairs (`BOOK:2678`). Together with T32's independently fixed 32 templates and `2^32` masks, this forces independent `(allowed mask, required template)` syntax. Thus `required not-in allowed` is well-formed but immediately inconsistent rather than constructor-invalid; “from this set” describes satisfiable examples, not a smaller syntactic family.
- Printed constraint numbers remain the T32 allowed-set numbers “as before,” while the required template is displayed separately at the center (`BOOK:2640`). No source-defined combined 37-bit integer codec exists in the audited source.
- The strict examples can still be repetitive, including periods `98 x 98` and 56 cells on the diagonal (`BOOK:2640`). T33 does not mean nonperiodic, unique, satisfiable, or computationally complex.
- A finite search can extend thousands of cells and still fail globally. Gray partial assignments and a centered witness are solver state/provenance, not model labels or native state (`BOOK:2642-2666`).
- Constraint `18762389` forces a nonrepetitive nested pattern unique up to translation when a stacked-black template must occur; the Notes display a mathematical pattern formula, but its local extraction is syntactically corrupt (`x_{-}` and related forms), so it remains opaque witness/formula evidence rather than executable code or a transition trace (`BOOK:2668-2674`, `14086-14095`).
- Larger complete `3 x 3` profiles and CA-derived rule-60/rule-30 examples retain the same required-occurrence relation with different T32 base supports (`BOOK:2680-2694`).
- The Notes explicitly consider requiring every allowed template to occur somewhere. That is a finite conjunction of existential occurrence relations, not occurrence multiplicity, simultaneous co-location, or a transition schedule (`BOOK:14097`).
- T31/T32 already own the declarative model-set, static scopes, exact local observation, verifier/query/witness/certificate separation, pointwise identity, symmetry observers, and solver boundary. T33 adds one closed global relation node within that category.
- `src/ca` remains the shared SimplePrograms library, not a CA-only package. Its checked-in realization lacks the planned T31/T32 declarative layer; T33 extends that layer and does not justify a rollout family, `seeds.py` branch, executor, or top-level state class.

## Updated Assumptions

- **Retained:** T32 `AllowedLocalPatterns` is the smallest local base; T33 is a declarative conjunction with `RequiredPatternOccurrences`.
- **Retained:** required templates are total maps over exactly the base relation's support/alphabet. Shape or alphabet mismatch is invalid syntax; failure to belong to the allowed set is semantic inconsistency, not malformed data.
- **Retained:** strict T33 requires one template at least once. A principled finite-set closure requires each distinct listed template somewhere; the Notes' “every template” profile is `required = allowed`.
- **Retained:** a witness anchor belongs to a verification/certificate record. It is not part of the denoted model, and translating a model translates its witnesses.
- **Retained:** periodic presentations can decide occurrence by scanning one full fundamental domain while preserving named support-slot aliases. Finite windows can positively witness occurrence with complete support but absence from a bounded window is not global absence.
- **Rejected:** `initial_state`, fixed-center semantics, preferred origin, anchor policy menu, seed-aware rollout, implicit translation quotient, witness marker in the alphabet, search cursor/gray value, occurrence callback, required-count integer, T32 matching flag, or trusted raster solution.

## Big Picture Objective

Reconstruct T33 as a finite closed global-existential relation composed with T32 exact local constraints. Close the strict singleton occurrence profile, source count and numbering, centered-display/search gauge, repetitive and nonrepetitive examples, finite-search boundary, Notes all-required extension, larger supports, assets, Index/splits, scopes, witnesses, solver separation, T32 forgetful map, runtime fit, and Goal 2 handoff. Prove that the catalog word “seeded” does not create initial-condition or execution semantics.

## Catalog Identity

- Stable ID: T33.
- Exact CSV name: Seeded Template Constraint Systems.
- CSV physical line: 34.
- Taxonomy section: 33.
- Canonical main core: `BOOK:2632-2678`.
- Larger-support/CA-derived continuations: `BOOK:2680-2694`.
- Exact Notes core: `BOOK:14086-14097` plus governed continuations.
- Entry kind: static declarative conjunction of one allowed-local-pattern relation and at least one global existential local-pattern occurrence.
- Native strict support: T32's binary oriented five-site cross on static discrete 2D square-lattice support.

## Source Audit

`41-T33-source-oracle.py` is the fail-closed textual evidence record. Its 32 query lanes close 65 unique lines at `56 pre-Index / 9 actual-Index`. It retains 191 lines at `33 native / 49 relation / 109 control`, including 135 governed continuations, with no textual exclusions. Retained split provenance closes at `137 exact + 54 mapped`; the query reverse join closes at `51 exact + 13 mapped`; zero retained lines are monolith-only and zero mechanics are unresolved.

The frozen 24-record source model digest is `c00fee3f69f5d7ec669ec7a4eb1d3b636680f10e42056735b2798708be6aa0b1`. The source-side image interface has 52 candidates, 42 governed at `7 native / 11 relation / 24 control`, and ten exclusions, exactly matching the asset oracle. Source oracle SHA is `f7266058575861d5aa358f4a031ea22a61be8251c0ac8c34027e66d6db5063ec`.

## Book Evidence Map

### E01 — singleton global occurrence, not an initial condition

- Source: `BOOK:2632-2640`.
- Establishes: every local neighborhood must still match the fixed allowed set, and one specified template must occur at least once somewhere. The figure centers the required template for display but does not fix a semantic coordinate.

### E02 — no direct generation and centered solver gauge

- Source: `BOOK:2642-2666`.
- Establishes: constraints do not directly generate patterns; search begins from a chosen centered witness, extends partial assignments, and backtracks. Large finite extension can coexist with global inconsistency.

### E03 — forced nonperiodic pattern up to translation

- Source: `BOOK:2668-2674`, `14086-14095`.
- Establishes: mask `18762389` plus the stacked-black required template forces the stated nested pattern; its only freedom is coordinate origin. The locally corrupt Notes formula is opaque denotation/witness evidence, not repaired executable code or iterative RULE data.

### E04 — strict family cardinality

- Source: `BOOK:2678`.
- Establishes: `137,438,953,472 = 32 * 2^32` strict syntactic constraint pairs. This must be reconciled explicitly with “from this set” and must not be replaced by the smaller sum of allowed-set sizes.

### E05 — larger supports retain occurrence semantics

- Source: `BOOK:2680-2694`.
- Establishes: complete `3 x 3` template systems can require the first template somewhere and can correspond to rule 60/rule 30 patterns. These change T32 base relation data, not the global quantifier or execution category.

### E06 — all-required extension

- Source: `BOOK:14097`.
- Establishes: requiring every allowed template somewhere is an explicit extension. Each existential may have its own witness; this is not one anchor, one simultaneous neighborhood, multiplicity, or a schedule.

### E07 — model/search/initial-condition boundary

- Source: `BOOK:2642-2666`, `14080-14084`, `14275`.
- Establishes: solver choices, gray cells, propagation, periodicity tests, and backtracking are external; bounded failure is not automatically global UNSAT; systems based on constraints do not have initial conditions.

## Asset Audit

`41-T33-asset-oracle.py` binds the exact native/relation/control/excluded raster universe, monolith/split references, physical hashes, bytes, dimensions, paired assemblies, and evidence boundary. The 42 governed assets partition at `7 native / 11 relation / 24 control`, close 84 references, 42 physical hashes, 4,668,695 bytes, and nine assemblies/20 member files. Ten excluded candidates are independently bound by 20 references, ten hashes, 409,462 bytes, and two assemblies. The governed ledger SHA is `4b4fddde132a4fa158d1e00139e3dc597004bf5e6e46badfc3d354a2a8c4d7fd`; the excluded ledger SHA is `93406a8a288d5ee27cfe9e1cc90f86c814da4e0354a2b29e24822d459aea4166`; asset oracle SHA is `47781c12962ede4459c3b8ed63e46ef3af61107fb4970fc81440a155d9deb29e`.

No raster supplies an untranscribed required-template word, allowed mask, witness table, search trace, palette mapping, uniqueness proof, or numeric codec. The boundary remains `42 hash-bound / 0 limited-transcribed / 0 pixel-replayed`. Unrecovered visual facts include the complete required gallery glyphs/fields and allowed sets, gray search decisions/backtracking, raster proofs of existence/uniqueness/periodicity, full 33-/56-row `3 x 3` tables, their first required templates/anchors, palettes, crops, domains, and any solver or UPDATE semantics.

## Construction Model

T33 is a relation over the same static models as T32:

```text
RequiredPatternOccurrences = {
    base: AllowedLocalPatterns,
    required: FiniteNonEmptySet[TotalMap[base.support, base.alphabet]],
    quantifier: EACH_SOMEWHERE,
}

observed(base, X, p) = {
    delta -> X[p + delta]
    | delta in base.support
}

Models(base, required) = {
    X in Models(base)
    | for every template r in required:
        there exists p in Z^base.dimension
        such that observed(base, X, p) = r
}
```

The strict source profile has one required template. The Notes extension uses every template in the allowed set. A generic finite nonempty set is the principled conjunction closure between those profiles; an empty required set canonicalizes to plain T32 rather than naming a T33 program.

Every required template must be total over the base support and alphabet. Duplicate requirements canonicalize because “at least once” is idempotent. `required` is not constrained to be a subset of `base.allowed`: the source's full `32 * 2^32` count admits all independent pairs, and any required template disallowed locally yields an immediate semantic UNSAT certificate.

There is no seed, event-zero configuration, preferred origin, time, FRONTIER, transition NEIGHBORHOOD, RULE result, write, UPDATE, successor, halt, or trace.

### Strict identity and numbering

The strict structural identity is:

```text
StrictT33 = {
    allowed_mask: T32BinaryCrossMask,
    required_template: BinaryCrossTemplate,
}
```

The Book says constraints are numbered “as before” and shows the required template separately. Thus the printed decimal number identifies the T32 mask, not the full T33 pair. The source family count confirms 32 possible requirement choices per mask. Goal 2 may serialize the structural pair or define an explicitly tagged independent codec, but must not claim a source-defined combined integer.

### Occurrence witnesses and translation

For a verified candidate model, a positive occurrence record is closed evidence:

```text
OccurrenceWitness = {
    relation_id,
    model_id,
    required_template_id,
    anchor,
    observed_template,
    scope,
}
```

Reverification checks the declared scope and exact observation. The witness is not part of model identity. If `tau_v` translates fields, then:

```text
X satisfies Required(r)
iff tau_v(X) satisfies Required(r)

witness(X, r, p) -> witness(tau_v(X), r, p + v)
```

Putting one witness at the origin is a solver/display gauge. It is not losslessly identical to the existential relation unless the chosen witness and translation are retained; models with multiple occurrences admit multiple such records. A fixed-anchor relation would denote a different subset of pointwise models.

### T32 forgetful map and proper strengthening

Dropping `required` yields the exact T32 base relation:

```text
forget(base, required) = base
Models(base, required) subseteq Models(base)
```

The inclusion is strict. For an unconstrained full-shift base, an all-zero field can avoid a required template containing a `1`, while another field can contain it. Required-not-allowed gives a second boundary: the T32 base may have models while the T33 conjunction has none.

The global node cannot be replaced by a finite local allowed-pattern flag on the same carrier. In the full shift, fields with a required black occurrence arbitrarily far away agree with the all-white field on every chosen finite observation around the origin, yet only the former satisfy the existential relation. A finite-radius local relation that accepts all translated finite-occurrence models cannot exclude the all-white limit. The smallest justified response is a closed global existential relation node inside the existing declarative algebra, not a new top-level category or executor.

### Scopes, verification, and queries

- **Exact periodic presentation:** verify T32 locality at every residue anchor and scan one full fundamental domain for every required template. A complete witness proves the infinite periodic field satisfies the existential conjunct.
- **Finite window with complete halo:** an observed full-support match positively witnesses an occurrence in the infinite candidate field. Failure to see one is only `NotObservedInScope`, not global violation or UNSAT.
- **Diagnostic open patch:** check only complete local observations. Partial edge neighborhoods do not witness or refute an occurrence unless a declared halo supplies every slot.
- **Solver query:** retain T31/T32 `Satisfiable`, `Unsatisfiable`, `Unknown`, and `ResourceLimit` separation. Reverify witnesses; replay certificates. A large partial pattern or bounded search failure is not a complete result.

For several required templates, each distinct template needs its own occurrence witness, but anchors may differ. The relation asks existence, not exactly one occurrence, earliest occurrence, occurrence count, or one anchor satisfying incompatible templates.

### Symmetry and observers

Translations preserve the unanchored relation and move witnesses. Rotation, reflection, and color exchange must transform both the base relation and every required template. They are explicit relations/observers, not implicit matching modes or equality. Gallery orbit reduction and centered display do not quotient pointwise models unless an explicit observer requests it.

### Search, generation, and CA relations

Starting with a required template at the center, propagating consequences, choosing cells, backtracking, testing periodicity, or compiling CA spacetime constraints are solver/representation relations. None supplies native T33 evolution. Gray is an algorithmic partial-assignment value, not part of the binary model alphabet. The page-219 formula and rule-60/rule-30 correspondences are witnesses or mappings, not replacement RULEs for T33.

## Semantic Proof Requirements

`41-T33-semantic-oracle.py` independently compares direct singleton/all-required occurrence verification with a generic declarative conjunction evaluator over complete reports. It covers:

- exhaustive strict binary periodic carriers and every singleton required template;
- `32 * 2^32` structural counting without enumerating the mask space;
- required-not-allowed well-formed/UNSAT behavior;
- T32 forgetful projection and strict-subset witnesses;
- centered-witness/translation commutation without fixed-anchor collapse;
- period-1/period-2 alias occurrence preservation;
- exact periodic, finite-window, halo, and open-patch scope distinctions;
- multiple requirements as independent existentials and Notes all-required specialization;
- rotation/reflection/color-exchange transforms of base, requirements, models, anchors, and reports;
- pointwise identity versus translation/symmetry orbit observers;
- malformed support/alphabet/template rejection and duplicate canonicalization;
- occurrence-witness reverification, bounded-search `Unknown`, and solver-state exclusion;
- no finite local T32 flag for the global existential; and
- static absence of seed/time/frontier/write/update/successor semantics.

The oracle closes 666 periodic configurations against 256 strict constraints for 170,496 direct/generic complete-report commutations, 1,397,248 anchor checks, and 666 representation round trips. A complete one-site-support relation space adds 208 singleton and 104 all-required checks. Translation closes 320 report commutations and 480 translated occurrence anchors; three explicit D4/color transforms close 960 report commutations and 5,376 checks, with three implicit-match rejections and two explicit orbit witnesses.

It also closes the full count seam; periodic/window/open scopes; projection strictness and noninjectivity; compatible-but-empty and required-outside-allowed emptiness; independent multiple witnesses, duplicate canonicalization, and the empty generic conjunction identity; aliases; occurrence-witness replay independent of base-local consistency; 13 remote-defect radii with 2,925 fixed-origin equalities; a generalized nine-slot/16-color profile; query outcomes and two replayable global-UNSAT certificate forms; 62 hostile validation rejections; and the complete absence of transition fields. Its semantic digest is `54276cd1279b01e75ebe8495c528e5991f0b6c6387ec9744dc65db85539626e7`; semantic oracle SHA is `2d0434a1f75195a6b4147c53b1c5646c4605c0c7406baa449d243bea8d667d3b`.

## Architecture Classification

| Responsibility | Classification | Smallest reusable construction | T33 delta |
|---|---:|---|---|
| Static support/model set | 1 | D058/T31/T32 declarative category | none |
| Base local relation | 1 | T32 `AllowedLocalPatterns` | none |
| Required template data | 2/3 | same total template carrier | finite nonempty requirement set |
| Global quantifier | 3 | generic declarative conjunction/relation algebra | add `RequiredPatternOccurrences(EACH_SOMEWHERE)` |
| Verification reports | 1/2 | T31/T32 scoped reports | add occurrence witnesses and not-observed-in-scope status |
| Solver outcomes/certificates | 1 | T31 query infrastructure | conjunct-aware external analysis only |
| Translation/symmetry | 1/2 | explicit transforms/observers | transform requirements and witness anchors |
| Centered display/search | 2/3 | witness-bearing representation | gauge with provenance; not semantics |
| SEED/FRONTIER/RULE/UPDATE/executor | not applicable | no transition algebra | add nothing |

Relative to SimpleProgram rollout, T33 inherits D058/T31/T32's existing class-4 declarative nonfit because there is no canonical successor. Relative to that already justified category, the incremental T33 delta is classes 1–3 and one genuinely nonlocal relation node; it is not a new semantic category or execution algebra.

## Current Runtime Fit and Smallest Goal 2 Delta

The checked-in runtime lacks the shared declarative relation/query layer already required by T31/T32. T33 should extend that planned layer:

1. Add immutable structural `AllOf(AllowedLocalPatterns(...), RequiredPatternOccurrences(required, quantifier=EACH_SOMEWHERE))` data, or embed the complete base relation in the conjunction. A base ID may be explicit content-addressed provenance, never a hidden registry lookup.
2. Compose the closed nodes with the normalized T32 exact-pattern evaluator and T31 scope/report/query envelopes. Do not dispatch on catalog family. The current static-array adapter must construct `loci.coordinate_space((nx, ny), steps=None)`, validate canonical `t = 0`, and then call `loci.gather`; `steps=None` itself ignores the time column.
3. Add exact occurrence witnesses, per-requirement status, and finite-scope `NotObservedInScope`. Absence in a complete presentation refutes that presented total model's existential conjunct; it does not prove the relation has no other models. Only a replayable global emptiness certificate supports `Unsatisfiable`. Replaying an occurrence witness proves its existential conjunct independently; whole-relation verification separately checks T32 locality.
4. Add translation and other explicit transform conformance for requirements and witnesses. A centered solver representation must retain its chosen witness and translation.
5. Add the strict singleton constructor, the Notes all-required preset, and source-bound example records without inventing raster templates or a combined numeric code.
6. Let solvers consume the closed conjunction and return the existing typed outcomes/certificates; no solver callback or gray/search state enters relation data.
7. Add no `SeededConstraintState`, initial-condition class, `anchor_policy` menu, `seeds.py` branch, rollout branch, FRONTIER, RULE result, UPDATE, family executor, callback, hidden witness marker, or T32 flag.

## No-Cheating Checks

- No use of `SEED` merely because the catalog says “Seeded.”
- No fixed center, preferred origin, distinguished model cell, or initial configuration inferred from centered figures/search.
- No witness anchor stored in the mathematical model or used as pointwise model identity.
- No required template hidden in T32 matching flags, callbacks, or alphabet markers.
- No constructor rejection of `required not-in allowed`; the exact source family count admits that well-formed inconsistent case.
- No occurrence absence inferred from a bounded/open window.
- No partial gray assignment, search cursor, backtracking tree, periodicity heuristic, or SAT state treated as a model or transition trace.
- No multiplicity, exactly-once, first/nearest occurrence, common anchor, or fixed-anchor menu invented from “at least once.”
- No automatic translation/rotation/reflection/color quotient or implicit matching.
- No combined 37-bit NKS codec claimed when the source numbers only the allowed mask and displays the requirement separately.
- No raster-derived allowed set, required word, seed, trace, palette, formula, uniqueness proof, or solver table.
- No formula/CA/substitution/tiling reduction presented as native T33 execution.
- No bounded failure promoted to global UNSAT and no one witness promoted to the whole model set.

## Completion Requirements

- [x] Every direct name, quantifier phrase, strict example, Notes extension, actual Index route, continuation, split witness, image link, and false seed match is dispositioned with zero unresolved mechanics.
- [x] The `32 * 2^32` count, printed numbering, required-template identity, and required-not-allowed boundary are reconciled exactly.
- [x] Centered display/search is proved to be witness-bearing translation gauge, not a semantic fixed anchor or initial condition.
- [x] The governed asset universe and honest transcription boundary are hash-bound.
- [x] Singleton and all-required denotations, scopes, witnesses, translations, symmetries, queries, and solver separation are reconstructed.
- [x] The T32 forgetful map, strict-subset witness, and nonlocal counterexample prove the exact reuse/extension boundary.
- [x] Direct/generic reports commute under adversarial periodic/window/alias/translation/malformed cases.
- [x] Runtime fit and smallest Goal 2 delta are implementation-ready without a seed/executor branch.
- [x] Stage, plan, evidence index, design ledger, and architecture audit are synchronized under the next decision.
- [ ] Root/`/tmp`, optimized fail-closed, silent import, compile, repository tests, modes, Markdown, diff, scope, and fresh hostile review pass.

## Stage Results

Source, asset, and semantic reconstruction are closed. The 32-query source audit closes 65 lines at `56 pre-Index / 9 actual-Index`, retains 191 at `33 native / 49 relation / 109 control`, reverse-closes all retained evidence at `137 exact + 54 mapped`, and leaves zero unresolved. Forty-two governed assets partition `7 native / 11 relation / 24 control`, close 84 references, 42 hashes, 4,668,695 bytes, and nine assemblies/20 files, and remain `42 hash-bound / 0 limited-transcribed / 0 pixel-replayed`.

The semantic oracle closes 666 configurations, 256 strict constraints, 170,496 direct/generic complete-report commutations, 1,397,248 anchor checks, explicit translation/D4/color transforms, singleton/all-required/empty-identity behavior, occurrence-witness/base-conjunct separation, every scope distinction, two replayable global-emptiness certificate forms, the remote-defect nonlocal counterexample, a generalized nine-slot/16-color profile, and 62 hostile rejections. Oracle SHAs are source `f7266058575861d5aa358f4a031ea22a61be8251c0ac8c34027e66d6db5063ec`, asset `47781c12962ede4459c3b8ed63e46ef3af61107fb4970fc81440a155d9deb29e`, and semantic `2d0434a1f75195a6b4147c53b1c5646c4605c0c7406baa449d243bea8d667d3b`; the semantic digest is `54276cd1279b01e75ebe8495c528e5991f0b6c6387ec9744dc65db85539626e7`.

T33 is a static discrete 2D declarative conjunction with no native `t`: T32 supplies the complete local relation, while one closed `RequiredPatternOccurrences(EACH_SOMEWHERE)` node supplies independent unanchored existentials. The `32 * 2^32` source count proves that requirement syntax is independent of membership in the allowed set; membership mismatch is valid empty denotation. Centering is witness/search gauge, every-template occurrence is a conjunction, and neither creates a seed, anchor policy, transition, UPDATE, category, or executor. Runtime-fit findings and global D135 synchronization are integrated; repository-wide gates and fresh hostile review remain before final closure.
