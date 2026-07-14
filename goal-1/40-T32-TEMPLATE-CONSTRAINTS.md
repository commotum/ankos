# 40-T32-TEMPLATE-CONSTRAINTS

Status: **IN PROGRESS — ARCHITECTURE RECONSTRUCTED; EVIDENCE ORACLES AND HOSTILE REVIEW PENDING**

## Current Facts

- T32 is CSV physical line 33, `Template Constraint Systems`; `ref/notes/CA-Types.md` section 32 is search vocabulary, not primary mechanics.
- This is a static declarative construction, not a transition system. A finite relation denotes the set of complete labeled planes whose local pattern at every anchor belongs to an allowed set.
- The strict main-text profile is binary on the square lattice. Its local support is the oriented five-site cross, so there are `2^5 = 32` possible local templates and `2^32 = 4,294,967,296` allowed-template sets. The Book fixes raw sorted `(row,column)` offsets `((-1,0),(0,-1),(0,0),(0,1),(1,0))`; compass names arise only through the explicit T21 Book-frame-to-ENU adapter `(row,column) -> (x=column,y=-row)`.
- Templates apply at every cell and neighboring anchored occurrences overlap. Overlap is pointwise equality in one candidate field, not a write collision or UPDATE policy (`BOOK:2614-2620`).
- The strict family is unusually completely classified in the source: `766,979,044` allowed sets have no model and the remaining `3,527,988,252` have a periodic model represented by one of 171 displayed pattern families (`BOOK:2620-2630`). This source theorem does not by itself supply a machine-readable 171-pattern solver table.
- The Notes define the 32-bit numbering scheme and check finite arrays with alternatives of `3 x 3` Mathematica patterns whose four corners are Blank. The general-rule Notes independently fix the raw sorted five-offset order and descending binary neighborhood catalog used by the page-941 plate (`BOOK:13513-13520`), so the numeric codec need not be inferred from pixels. Its first offset is locally malformed as `(-1, 0)` while the remaining entries use Mathematica braces; a guarded one-tuple delimiter repair, consistent with T21's raw-tuple interpretation, is disambiguated by five-neighbor arity, `Sort` order, the other four tuples, and the page-941 cross-reference. The Blank corners are outside the five-site cross support; they are not wildcard-valued semantic slots (`BOOK:14048-14060`).
- The local extraction corrupts two executable tokens: it renders the four Blank corners `_` as `-` and Mathematica `Alternatives` bars `t1 | t2 | t3` as slashes `t1/t2/t3`. The official Wolfram Science note supplies both forms; both repairs must be frozen and fail-closed before the adapter is executable.
- Allowed sets are exact and oriented. Overall rotation, reflection, and black/white exchange omit equivalent gallery representatives; they are relations between constraints/models, not implicit matching modes (`BOOK:14048`).
- T31 already owns the generic declarative model-set, exact periodic/open/window scopes, verifier reports, solver-query outcomes, witnesses, certificates, `Unknown`, pointwise model identity, and no-evolution boundary.
- T32 adds a closed allowed-local-pattern relation node inside that same declarative algebra. It does not add a state class, solver class, executor, frontier, rule result, UPDATE law, seed, or trajectory.
- T31 count relations lower losslessly to allowed oriented templates by enumerating every assignment with an allowed center-conditioned histogram. T32 is strictly more expressive than histograms because it can distinguish two patterns with the same center and neighbor counts but different orientations.
- T33 begins when one allowed template is also required to occur at least somewhere (`BOOK:2632-2640`). That existential global conjunct is not a T32 flag, seed, initial condition, or distinguished firing locus.
- Enlarged `3 x 3`, `2 x 2` multicolor, CA-fixed-point/spacetime, subshift, and tiling constructions are variants or explicit relations. They do not retroactively change the strict five-site profile or add evolution.
- `src/ca` remains the intended shared SimplePrograms library, not a CA-only package. Its checked-in realization currently lacks the declarative relation/model-set layer that T31 and T32 require; existing alphabet, loci, and coordinate-access machinery remains reusable, while rollout is simply inapplicable because the source supplies no native step. Static 2D reuse must pass an explicit `CoordinateSpace(shape=(nx,ny), steps=None)` to `loci.gather`; otherwise its fallback interprets the leading array axis as time.

## Updated Assumptions

- **Retained:** T31's generic declarative category is the smallest semantic base. T32 is a tagged closed local-relation schema, not a second top-level constraint system.
- **Retained:** native models are total fields on a static discrete plane. Exact periodic tiles and finite windows are representations/query scopes, not finite native grids or initial states.
- **Retained:** every template is a total label map on one declared finite anchored support containing the zero offset; the allowed set may be empty and still denotes a valid, inconsistent relation.
- **Retained:** support offsets are geometrically named only inside a declared coordinate frame. Generic serialization order is representational; the NKS-numbered strict preset uses the independently source-fixed raw sorted `(row,column)` order and descending binary catalog, with compass names supplied by an explicit frame adapter.
- **Retained:** exact orientation is semantic. Rotation/reflection/color exchange must transform explicit data or be enumerated in the allowed set.
- **Retained:** distinct support offsets remain distinct occurrences even when a tiny periodic presentation maps them to the same residue cell.
- **Retained:** model verification and solving remain separate. Pairwise template compatibility, propagation, square-spiral extension, backtracking, memoization, symmetry pruning, and a recovered 171-pattern decision table are solver/analyzer concerns.
- **Rejected:** a predicate callback, `matching_policy` flag, custom graph callback, implicit symmetry closure, padding/boundary menu, violation-repair dynamics, CA fixed-point rollout, one witness as the model set, bounded failure as global UNSAT, or T33 occurrence data inside T32.

## Big Picture Objective

Reconstruct T32 as exact finite allowed-pattern relation data over static labeled support; close the strict binary cross profile, numbering and Blank adapter, overlap law, periodic witnesses, 171-family theorem, T31 lowering, T33 boundary, scopes, solvers, variants, assets, Index/splits, and runtime fit. Prove that it reuses the T31 declarative algebra while requiring only a more expressive closed relation node, with no invented evolution or family-specific semantic class.

## Catalog Identity

- Stable ID: T32.
- Exact CSV name: Template Constraint Systems.
- CSV physical line: 33.
- Taxonomy section: 32.
- Canonical main core: `BOOK:2614-2630`.
- T33 boundary: `BOOK:2632-2640`.
- Exact Notes core: `BOOK:14048-14084`.
- Later template variants/relations: `BOOK:2666-2698`, `14113-14155`, and their governed continuations.
- Entry kind: static translation-invariant allowed-local-pattern relation defining a possibly empty set of complete models.
- Native strict support: binary five-site cross on static discrete 2D square-lattice support.

## Source Audit

`40-T32-source-oracle.py` will be the fail-closed textual evidence record. It must close direct names, allowed/fixed templates, overlap, exact counts, the 171-pattern result, the source-derived sorted-offset/template order and constraint numbering, Notes implementation, Blank-and-Alternatives repair, finite/open checking, solver/search boundaries, T31/T33 boundaries, later template sizes/colors, CA/tiling/subshift relations, actual Index routes, governed image links, split reverse provenance, and false positives such as unrelated CA rule counts.

Final frozen counts, digests, snapshot hashes, source-oracle SHA, and unresolved total are pending the independent source audit.

## Book Evidence Map

### E01 — exact oriented templates and overlap

- Source: `BOOK:2614-2618`.
- Establishes: every anchored local arrangement must be one member of a fixed allowed set; neighboring anchored templates overlap.

### E02 — strict rule space and complete periodic-witness theorem

- Source: `BOOK:2620-2630`.
- Establishes: `2^32` allowed sets; exact satisfiable/unsatisfiable totals; 171 periodic pattern families suffice for the strict profile; gallery symmetries are display reductions.

### E03 — existential occurrence begins T33

- Source: `BOOK:2632-2640`.
- Establishes: requiring one allowed template to occur somewhere is an additional global relation and not part of plain T32.

### E04 — relation data versus external search

- Source: `BOOK:2642-2664`.
- Establishes: constraints do not directly generate a pattern; enumeration, propagation, choices, backtracking, gray cells, and finite obstructions belong to solving and proof.

### E05 — nonperiodic/complex examples use stronger profiles

- Source: `BOOK:2666-2698`.
- Establishes: required occurrences and larger complete `3 x 3` templates can force nested or CA-derived patterns; these are T33 or broader-template relations, not evidence for a T32 update process.

### E06 — strict numbering and template catalog

- Source: `BOOK:13513-13520`, `14048-14052`.
- Establishes: after the single guarded delimiter repair, the raw Book offsets are sorted as `((-1,0),(0,-1),(0,0),(0,1),(1,0))`; `Reverse[Table[IntegerDigits[...]]]` fixes the 32 descending binary templates displayed on page 941; and the 32-bit integer selects catalog positions. This makes the numeric codec textually derivable and independently checkable without raster transcription. Compass labels require the explicit T21 frame adapter.

### E07 — exact finite-array adapter

- Source: `BOOK:14055-14060` plus the hash-bound official repair.
- Establishes: the official `t1 | t2 | t3` is Mathematica `Alternatives`, and alternatives of cross-shaped `3 x 3` patterns are matched on every complete finite-array window. Blank corners project away; this finite checker does not create a global boundary policy.

### E08 — 171-pattern identification is solver work

- Source: `BOOK:14054`.
- Establishes: symmetry pruning, satisfiable-superset pruning, local compatibility filters, and constructive search identify witnesses; none is relation validity or native execution.

### E09 — periodic representation and search complexity

- Source: `BOOK:14063-14084`.
- Establishes: repetitive models have finite exact presentations; square-spiral search is external; broader infinite existence is undecidable and finite-region existence NP-complete. Those generic complexity statements must not erase the strict family's complete 171-witness classification.

### E10 — larger supports/colors and occurrence variants

- Source: `BOOK:14097-14111`.
- Establishes: support size, alphabet size, and occurrence requirements can be extended; a fixed finite anchored support remains relation data, while existential occurrence remains a separate node.

### E11 — CA relations preserve the static category

- Source: `BOOK:14113-14123` and `4072-4084`.
- Establishes: CA fixed points and spacetime diagrams can map to allowed-template models. The mapping is a relation/encoding, not native CA evolution or a hidden time axis in T32.

### E12 — tilings and other declarative relatives

- Source: `BOOK:14124-14155` and actual Index routes.
- Establishes: tilings, polyominoes, ground states, correspondence systems, sequence equations, and pattern avoidance require explicit carrier/relation mappings rather than a callback or name-based collapse.

## Asset Audit

`40-T32-asset-oracle.py` will bind the exact native/relation/control raster universe, monolith and split references, physical paths, byte sizes, dimensions, SHA-256 values, paired assemblies, and evidence boundaries. The printed-page-213 example plate, pages 214–215 171-family catalog, and page-941 32-template catalog are expected native candidates; T31 and T33 plates are relations/controls. The asset oracle does not pixel-transcribe the catalog, even though its ordering is independently recovered from `BOOK:13513-13520`.

Final governed counts, manifest SHA, limited-transcription boundary, and unresolved visual facts are pending the independent asset audit.

## Construction Model

T32 is a relation over a static domain, not a transition program:

```text
AllowedLocalPatternRelation = {
    dimension: PositiveInt,
    alphabet: FiniteNonEmptyOrderedSet[Label],
    support: FiniteNonEmptySet[Offset[Z^dimension]],
    require: zero_offset in support,
    allowed: FiniteSet[TotalMap[support, alphabet]],
}

Models(C) = {
    X: Z^dimension -> alphabet
    | for every anchor p in Z^dimension:
        {delta -> X[p + delta] | delta in C.support} in C.allowed
}
```

The native strict preset is:

```text
dimension = 2                         # static 2D; no native t axis
alphabet  = {0,1}
support   = {Self, North, East, South, West}
allowed   = any subset of alphabet^support
```

Semantically, strict support is the unordered set of five raw Book `(row,column)` offsets and every template is an offset-to-label map. The ordered raw tuple belongs only to the NKS codec/source AST and decodes catalog words into those maps. A declared adapter may expose equivalent ENU names; neither storage array axes, compass labels, nor codec order enters relation satisfaction or extensional equality.

The empty allowed set is valid syntax with no models. Duplicate offsets, a missing zero anchor, mixed-dimensional offsets, undeclared labels, partial templates, duplicate templates, and callbacks are invalid syntax. Whether a valid relation has a model is a semantic/query question, not constructor validation.

For candidate model `X` and anchor `p`:

```text
observed(C,X,p) = {delta -> X[p+delta] | delta in C.support}
satisfied_at(C,X,p) = observed(C,X,p) in C.allowed
violation_at(C,X,p) =
    None if satisfied_at(...)
    else LocalPatternViolation(p, observed(C,X,p), relation_id=C.id)
```

`p` is a verification anchor, not a FRONTIER locus. `observed` is a pure structural read, not a transition NEIGHBORHOOD event. The violation is not a RULE result, and there is no write, UPDATE, successor, schedule, seed, halt, or trace.

### Strict Notes adapter

The Notes' semantic support is the five-site cross. The repaired outer expression is an explicit `Alternatives` tree, and each repaired `3 x 3` alternative has `_` at all four corners and literal `0/1` on the cross. A closed importer must:

1. verify the repaired `Alternatives` syntax and exactly that fixed shape and Blank-corner schema;
2. project the four corners away;
3. map the five named positions to an `Offset -> Label` template;
4. collect alternatives as an unordered allowed set; and
5. retain source spelling/provenance separately from normalized relation data.

It must not install a host `MatchQ` callback, preserve Blank as an alphabet value, add wildcard slots to the semantic footprint, or infer rotations/reflections.

The Notes' finite `Partition[list,{3,3},{1,1}]` checker visits only complete array windows. An array smaller than `3 x 3` therefore reports `checked_anchors=0` and at most vacuous local consistency, never global `Satisfiable`. This is an open-patch verifier fixture, not evidence that native infinite support has dropped boundaries. Exact periodic presentations reuse T31's modulo point query and check one complete fundamental domain.

### T31 lowering and the orientation counterexample

For a T31 center-conditioned histogram relation with footprint `F`, define support `S={0} union F` and enumerate:

```text
allowed_templates = {
    a: S -> alphabet
    | histogram(a(delta) for delta in F) in allowed_histograms[a(0)]
}
```

For every total field `X`, T31 satisfaction at every anchor is equivalent to satisfaction of this expanded T32-shaped relation. The map is lossless for well-formed T31 rows because each valid histogram has at least one oriented realization and can be recovered by regrouping the exhaustive templates; compact T31 AST/provenance remains authoritative program identity.

The reverse does not hold for arbitrary T32 data. With a binary cross, two templates can share center `0` and histogram `three 0 / one 1` while placing the `1` North versus East. A T32 allowed set may contain one but not the other; a histogram relation cannot. This is the concrete counterexample justifying a generic oriented-pattern relation node without justifying a new semantic category.

### Overlap and periodic aliasing

Every anchor observes the same candidate field. If two anchored occurrences overlap, both read the one label already assigned to that physical coordinate; no patch merge occurs. In a small periodic presentation, distinct support offsets may reduce to the same residue coordinate, but the observed template retains every named offset occurrence. This can impose equal-label conditions and must not be coordinate-deduplicated.

### Symmetry, numbering, and identity

Allowed templates are exact oriented data. Rotation/reflection/color exchange acts by an explicit bijection on support and labels, inducing a mapped relation and mapped models. It is not semantic equality, automatic closure, or matching policy. Gallery orbit reduction is observer metadata.

The NKS integer is a codec over an ordered catalog of 32 templates. `BOOK:13513-13520` fixes the raw sorted `(row,column)` offsets and the catalog as descending five-bit words; `BOOK:14050` selects positions whose 32-bit mask digit is `1`. Generic relation execution still uses explicit templates, while the strict numeric constructor is a guarded source-derived codec with exhaustive singleton-bit and representative round-trip conformance. Direction names are adapter metadata, not part of the raw codec.

### Scope, verification, and queries

T32 directly reuses T31's:

- total infinite-field denotation;
- exact axis-aligned periodic presentation and LCM-box pointwise equivalence;
- finite-window-with-halo and diagnostic open-patch scopes;
- pure local verification reports;
- `Satisfiable`, `Unsatisfiable`, `Unknown`, and `ResourceLimit` query outcomes;
- witness reverification and certificate replay; and
- pointwise model identity with separate symmetry/orbit observers.

The strict 171-family theorem permits a specialized complete analyzer only if the exact 171 witness families and their matching table are recovered; the 32-template catalog codec alone is insufficient. Generic bounded periodic search remains incomplete, and broader undecidability prevents a total solver API. Neither fact changes relation semantics.

## Semantic Proof Requirements

`40-T32-semantic-oracle.py` must independently compare direct allowed-pattern verification with the generic declarative relation evaluator over complete typed reports. Required witnesses include:

- exhaustive strict binary cross constraints/models on bounded periodic carriers;
- an orientation-sensitive north/east counterexample against histogram collapse;
- T31 count-to-template lowering commutation;
- every-anchor overlap consistency;
- period-1/period-2 alias-occurrence preservation;
- periodic, finite-window, and open-patch scope distinctions;
- malformed support/template rejection, including missing anchor and partial maps;
- empty allowed-set valid syntax with no passing nonempty model;
- exact orientation versus explicit symmetry transforms;
- pointwise model identity versus orbit grouping;
- verifier/query/result separation and bounded-failure `Unknown`;
- T33 existential occurrence excluded from T32; and
- static absence of frontier/write/update/seed/time semantics.

Final event counts, hostile controls, semantic digest, oracle SHA, and guarded numeric-codec results are pending the independent semantic audit.

## Architecture Classification

| Responsibility | Classification | Smallest reusable construction | T32 delta |
|---|---:|---|---|
| Static discrete support/model set | 1 | T31 generic declarative category | none |
| Alphabet and exact periodic/open/window presentations | 1 | T31 finite alphabet and scoped model representations | none |
| Local coordinate access | 1/2 | generic finite named offset access | include zero anchor and preserve orientation/alias occurrences |
| Relation data | 3 | tagged closed local-relation algebra | add `AllowedLocalPatterns(support, allowed)` |
| T31 histogram form | 3 | compact tagged source form | lossless exhaustive lowering with source AST retained |
| Verification/violations | 1/2 | T31 pure verifier/report envelope | observe exact offset-label map instead of histogram |
| Solver outcomes/witnesses/certificates | 1 | T31 query infrastructure | optional strict analyzer remains separate |
| Symmetry/views | 1 | explicit relations/observers | transform exact templates; never implicit matching |
| T33 required occurrence | separate relation node | generic declarative conjunction | deferred to T33; no T32 flag |
| FRONTIER/RULE result/UPDATE/executor | not applicable | no transition algebra | add nothing |

Relative to D058's already justified declarative category, every T32 delta is categories 1–3. Relative to SimpleProgram rollout, T32 remains the same existing class-4 nonfit because it has no canonical successor; it does not justify another semantic category, an execution algebra, or reopening any transition stage.

## Current Runtime Fit and Smallest Goal 2 Delta

The checked-in `src/ca` realization has no declarative constraint modules, scoped model/query records, or exact local-relation verifier yet. T31 already requires those shared pieces inside the broader SimplePrograms library. T32 should extend that planned implementation rather than create a parallel family API:

1. Add generic immutable `AllowedLocalPatterns` as one tagged relation node with finite named support, total templates, canonical serialization, and no callback.
2. Normalize T31's compact histogram AST losslessly into `AllowedLocalPatterns` and use one exact-pattern evaluator and report envelope. Retain compact T31 AST/provenance for program identity; any direct histogram evaluator is only a certified commuting optimization, not relation-tag family dispatch.
3. Add pure exact-template observation and violation construction atop the shared coordinate/presentation layer. For a static array, construct `CoordinateSpace(shape=(nx,ny), steps=None)` explicitly and pass it to `loci.gather`; canonical zero `t` coordinates are an encoding column, not native time.
4. Add the T31 count-to-template inverse/image check and conformance proofs so arbitrary oriented relations cannot masquerade as histograms.
5. Add the strict binary-cross constructor, guarded Notes adapter, and source-derived NKS numeric constructor using the exact sorted-offset/descending-binary catalog, with exhaustive positional conformance.
6. Keep search/analyzer algorithms in the solver layer. A future recovered 171-witness table is data for a strict analyzer, not core semantics.
7. Add explicit symmetry transforms/orbit observers; require enumeration for symmetry-invariant matching.
8. Add no rollout branch, T32 state class, template predicate, matching flag, relation-family verifier dispatch, repair update, hidden boundary, T33 requirement, or trusted raster table.

## No-Cheating Checks

- No `TemplateConstraintSystem` top-level semantic class when a tagged local relation node suffices.
- No seed, initial state, time axis, FRONTIER, writes, UPDATE, successor, halt, or trajectory.
- No violation-repair dynamics or CA fixed-point rollout used as native semantics.
- No host predicate/`MatchQ` callback; allowed patterns are closed finite data.
- No corner Blank stored as a label or semantic slot.
- No implicit rotation/reflection/color-swap matching or symmetry quotient equality.
- No coordinate deduplication after periodic aliasing.
- No pairwise compatibility or minimality imposed as constructor validity.
- No finite/open checker promoted to a global witness without explicit scope.
- No one periodic witness substituted for the complete model set.
- No bounded search exhaustion promoted to global UNSAT.
- No 171-pattern table, native example rows, seed, or trace invented from raster layout; the numeric template order is admitted only because separate textual Notes derive it exactly.
- No T33 existential required occurrence packed into T32.
- No generic undecidability claim used to contradict the strict source family's finite complete classification.

## Completion Requirements

- [ ] Every direct name, alias, strict line, variant, Notes item, actual Index route, continuation, split witness, image link, and false positive is dispositioned with zero unresolved strict mechanics.
- [ ] The official Blank-and-Alternatives repair and finite Notes adapter are frozen fail-closed.
- [ ] The governed asset universe and transcription boundary are exact and hash-bound.
- [ ] Static support, alphabet, templates, overlap, denotation, scopes, verification, query outcomes, symmetries, numbering, and T31/T33 boundaries are reconstructed.
- [ ] T31 lowering and the orientation counterexample prove the exact reuse boundary.
- [ ] Direct/generic semantic reports commute under adversarial periodic/open/scope/orientation/malformed cases.
- [ ] Current runtime/tests are inspected and the smallest Goal 2 delta is implementation-ready.
- [ ] Stage, plan, evidence index, design ledger, and architecture matrix are synchronized.
- [ ] Root/`/tmp`, optimized fail-closed, silent import, in-memory compile, repository tests, modes, Markdown, diff, scope, and independent hostile review pass.

## Stage Results

Pending source, asset, semantic, integration, and hostile-review closure.
