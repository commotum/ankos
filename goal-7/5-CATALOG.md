# 5-CATALOG

Status: **COMPLETE — EXACT CATALOG, MIGRATION, AND HOSTILE GATES CLOSED**

## Current Facts

- G7-04 began from clean commit
  `cf88affc29e225f64aaeca200c6f6548ecc42512` at
  `413 passed, 13 skipped`.
- The initial preset audit exposed nine missing reusable mechanics. G7-02 and
  G7-03 were reopened in bounded form, reclosed, and left their durable
  evidence in [`3-MECHANICS.md`](3-MECHANICS.md) and
  [`4-CODECS.md`](4-CODECS.md).
- The live catalog now contains exactly 60 canonical constructors, 40 presets,
  4 true aliases, and 1 compatibility adapter.
- Callable-free metadata contains exactly 60 families, 2 close roles,
  45 legacy entries, and 105 public-name relations.
- The callable census is exactly `60 C / 40 P / 4 A / 1 K`. There are
  105 qualified callables, 104 flat catalog callables, and 111
  `ca.catalog.__all__` entries after the seven navigation namespaces are
  included.
- Root `ca` exposes `catalog` as its twelfth name and flattens no catalog
  constructor.
- Every public callable is explicit, keyword-only, annotated, nonvariadic, and
  free of `Any`.
- All thirteen G7-04-owned skips are removed. The focused catalog/conformance
  slice reports `338 passed`; the complete active suite reports
  `975 passed` with no skips.
- Goal 2, Goal 5, and Goal 6 remain frozen. G7-05 has not started.

## Updated Assumptions

- Goal 6's family-level semantic keyword lists are descriptive construction
  metadata. They are not a second executable recipe language.
- Each canonical `C` spelling is a typed navigation wrapper over the explicit
  five components. It does not infer missing fields or certify that arbitrary
  components have a Book-family identity.
- Every `P` spelling is a bounded source-facing compiler or validator over
  closed component mechanics. In particular, T06/T07 validate finite rule
  tables, and T31–T33 compile explicit `ValueNode` relation presentations;
  none accepts an already-expanded program as a pretend refinement.
- True aliases have zero semantic delta. The compatibility spelling has one
  closed, explicitly typed legacy argument domain; that domain is not
  literally a finite set.
- Invocation history is external. Equal source-facing constructions produce
  equal expanded programs and byte-identical canonical payloads without
  catalog/SPF/F/T identity, constructor arguments, or invocation receipts.

## Historical Contract Reconciliation

At stage entry, Goal 6 fixed the name, home, kind, metadata, and semantic
parameter inventory of every family, but it did not define a second general
compiler from those semantic inventories into the five fields. Treating those
lists as literal Python signatures would have required a parallel schema,
matcher, structural-edit, evaluator, stochastic, and differential language.

The resolved boundary is the one already shown in
`ref/notes/ca-scaffold.py`:

```python
def canonical_family(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )
```

All sixty canonical functions have that exact five-component profile. The
catalog's familiar source-facing names are the presets below. Their dependency
audit caused the bounded G7-02/G7-03 reclosures; no preset was exposed by
ignoring an argument, returning a hardcoded witness, accepting an opaque
recipe, or dispatching through family identity.

## Big Picture Objective

Turn the inert catalog shells into the exact ordinary-program construction and
callable-free navigation surface frozen by Goal 6: sixty canonical families,
all authorized presets and aliases, the sole compatibility adapter, the
complete SPF/F/T/name metadata join, explicit collision-free exports, and no
catalog authority over application or serialization.

## Executable Preset and Adapter Freeze

For compactness below:

```python
FIXED0 = loci.Boundary(loci.BoundaryPolicy.FIXED, 0)
PERIODIC = loci.Boundary(loci.BoundaryPolicy.PERIODIC)
RATIONAL0 = loci.Boundary(
    loci.BoundaryPolicy.FIXED,
    Fraction(0),
)
```

These abbreviate the exact immutable version-one defaults. They are not
additional public names.

### Automata presets — 16

```python
eca(*, rule: int = 30, width: int = 79) -> SimpleProgram

multicolor_cellular_automaton(
    *, initial: tuple[int, ...], colors: int, rule: tuple[int, ...],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

totalistic_cellular_automaton(
    *, initial: tuple[int, ...], colors: int, rule: tuple[int, ...],
    radius: int = 1, boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

three_color_totalistic_cellular_automaton(
    *, initial: tuple[int, ...], rule: tuple[int, ...],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

higher_color_totalistic_cellular_automaton(
    *, initial: tuple[int, ...], colors: int, rule: tuple[int, ...],
    radius: int = 1, boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

quiescent_cellular_automaton(
    *, initial: tuple[int, ...], colors: int, rule: tuple[int, ...],
    background: int = 0, boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

symmetric_cellular_automaton(
    *, initial: tuple[int, ...], colors: int, rule: tuple[int, ...],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

generalized_mobile_automaton(
    *, initial: tuple[int, ...], active: tuple[int, ...], colors: int,
    transitions: tuple[
        tuple[tuple[int, int, int], tuple[int, tuple[int, ...]]],
        ...,
    ],
    boundary: loci.Boundary[int] = PERIODIC,
    conflict_policy: rules.ProposalConflictPolicy = (
        rules.ProposalConflictPolicy.REQUIRE_EQUAL
    ),
) -> SimpleProgram

cellular_automaton_2d(
    *, shape: tuple[int, int], initial: tuple[int, ...], colors: int,
    rule: tuple[int, ...], boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

moore_cellular_automaton(
    *, shape: tuple[int, int], initial: tuple[int, ...], colors: int,
    rule: tuple[int, ...], boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

cellular_automaton_3d(
    *, shape: tuple[int, int, int], initial: tuple[int, ...], colors: int,
    offsets: tuple[tuple[int, int, int], ...], rule: tuple[int, ...],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

lattice_cellular_automaton(
    *, shape: tuple[int, ...], initial: tuple[int, ...], colors: int,
    offsets: tuple[tuple[int, ...], ...], rule: tuple[int, ...],
    boundary: loci.Boundary[int] = FIXED0,
    axes: tuple[str, ...] | None = None,
) -> SimpleProgram

arithmetic_iteration(
    *, initial: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    map_expression: rules.RuleExpr,
) -> SimpleProgram

piecewise_integer_map(
    *, initial: int,
    cases: tuple[tuple[int, int, rules.RuleExpr], ...],
    otherwise: rules.RuleExpr,
) -> SimpleProgram

digit_reversal_map(*, initial: int, base: int = 2) -> SimpleProgram

continuous_cellular_automaton(
    *, initial: tuple[Fraction, ...], local_rule: rules.RuleExpr,
    radius: int = 1,
    boundary: loci.Boundary[Fraction] = RATIONAL0,
) -> SimpleProgram
```

`eca` accepts rule numbers `0..255` and positive widths. Finite-palette
constructors require exact integer values, `colors >= 2`, total in-palette
tables, and nonempty or shape-exact initial state. Non-totalistic tables use
declared offset order with the first observation as the most-significant
base-`colors` digit. Totalistic tables have length
`1 + (colors - 1)(2r + 1)`; the three-color specialization fixes
`colors=3, radius=1`, and the higher-color specialization requires
`colors >= 4`. Quiescent and symmetric constructors validate their named table
properties.

Generalized mobile automata require at least three cells, unique in-range
active positions, a total table over every symbol triple, unique destination
offsets in `{-1, 0, 1}`, a recognized conflict policy, and a periodic carrier.
Grid shapes have positive extents and shape-product initial size. Arbitrary
offsets are nonempty, unique, rank-correct, and include the source offset.
Piecewise maps require at least one positive-modulus/in-range-residue branch
and an explicit fallback. Digit reversal accepts a nonnegative integer and
`base >= 2`. Continuous CA values and any fixed exterior are exact
`Fraction` values in `[0,1]`.

### Substitua presets — 15

`SemanticWord`, `WordProduction`, and `ContextProduction` below are the closed
aliases defined by `ca.catalog.substitua`.

```python
neighbor_independent_substitution(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[WordProduction, ...],
) -> SimpleProgram

neighbor_dependent_substitution(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[ContextProduction, ...],
) -> SimpleProgram

creation_destruction_substitution(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[WordProduction, ...],
) -> SimpleProgram

sequential_substitution(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    clauses: tuple[tuple[SemanticWord, SemanticWord], ...],
) -> SimpleProgram

tag_system(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord, n: int,
    appendants: tuple[ContextProduction, ...],
) -> SimpleProgram

cyclic_tag_system(
    *, initial: tuple[bool, ...],
    blocks: tuple[tuple[bool, ...], ...],
    initial_phase: int = 0, trigger: bool = True,
) -> SimpleProgram

symbolic_system(
    *, expression: alphabets.ValueNode,
    rewrites: alphabets.ValueNode,
    scan: rules.RewriteScan = rules.RewriteScan.RULE_PRIORITY_FIRST,
) -> SimpleProgram

substitution_system_2d(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram

geometric_substitution(
    *, seed: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram

context_dependent_substitution_2d(
    *, symbols: tuple[alphabets.SemanticValue, ...],
    initial: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram

recursive_sequence(
    *, prefix: tuple[int | Fraction, ...],
    coefficients: tuple[int | Fraction, ...],
    bias: int | Fraction | None = None,
) -> SimpleProgram

variable_index_recursive_sequence(
    *, prefix: tuple[int, ...],
    recurrence: rules.RuleExpr,
) -> SimpleProgram

number_theoretic_filtering(
    *, upper: int, lower: int = 2, first_divisor: int = 2,
) -> SimpleProgram

constant_digit_sequence(
    *, base: int, prefix: tuple[int, ...],
    next_digit: rules.RuleExpr,
    source_evidence: rules.EvidenceTerm,
) -> SimpleProgram

continued_fraction_substitution(
    *, continued_fraction: tuple[int, ...],
    source_evidence: rules.EvidenceTerm,
) -> SimpleProgram
```

Declared alphabets are nonempty and semantically distinct. Production maps are
immutable, key-unique, total over their declared symbol/context domains, and
closed over declared symbols. Independent substitution forbids empty
offspring; creation/destruction requires both an empty and a length-greater-
than-one production. Neighbor-dependent substitution covers every width-two
context with nonempty offspring. Tag systems require `n > 0`, cover every
width-`n` prefix, and may append an empty word. Cyclic tag systems require a
nonempty block cycle but allow empty initial words and individual blocks.

Sequential clauses are nonempty, ordered, and have nonempty left and right
sides. Symbolic systems require an expression node, a nonempty validated
`rewrite-rules` word, and a recognized scan enum. The 2D presets require
rank-two fields with compatible tile axes and geometry; independent maps cover
all symbols, contextual maps cover all NW/N/W/self contexts, and geometric
maps close both seed and produced cells over their keys.

Fixed recurrences use a nonempty homogeneous exact `int` or `Fraction` domain
and enough prefix terms for every lag. `bias=None` derives that domain's exact
zero; an explicitly supplied bias must have the same exact type. Variable
recurrences require a nonempty positive-integer prefix and closed `RuleExpr`.
Number filtering requires `2 <= lower <= upper` and
`2 <= first_divisor <= upper`. Constant digits require `base >= 2`, a nonempty
in-base prefix, a closed next-digit expression, and closed evidence. Continued
fractions require a nonempty integer tuple with a strictly positive tail and
closed evidence; retaining that evidence does not prove an external
mathematical provenance.

### Machina presets — 4

```python
mobile_automaton(
    *, initial: tuple[int, ...], head: int, colors: int,
    transitions: tuple[
        tuple[tuple[int, int, int], tuple[int, int]],
        ...,
    ],
    boundary: loci.Boundary[int] = PERIODIC,
) -> SimpleProgram

neighbor_updating_mobile_automaton(
    *, initial: tuple[int, ...], head: int, colors: int,
    transitions: tuple[
        tuple[
            tuple[int, int, int],
            tuple[tuple[int, int, int], int],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = PERIODIC,
) -> SimpleProgram

turing_machine(
    *, tape: tuple[int, ...], head: int,
    initial_state: str, states: tuple[str, ...], symbols: int,
    transitions: tuple[
        tuple[tuple[str, int], tuple[str, int, int]],
        ...,
    ],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram

turing_machine_2d(
    *, shape: tuple[int, int], tape: tuple[int, ...],
    head: tuple[int, int], initial_state: str,
    states: tuple[str, ...], symbols: int,
    transitions: tuple[
        tuple[
            tuple[str, int],
            tuple[str, int, tuple[int, int]],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = FIXED0,
) -> SimpleProgram
```

Mobile presets require `colors >= 2`, at least three cells, one in-range head,
a periodic carrier, and a unique total table over all symbol triples.
Movement is exactly `-1` or `1`; the center-updating form changes the source
symbol, while the neighbor-updating form commits the complete three-cell block
atomically.

Turing states are unique nonempty strings, the initial state is declared,
symbol counts are positive, tapes are palette-valid, and heads are in bounds.
Transition tables may be partial: a missing transition produces an explicit
terminal no-successor result. One-dimensional movement is `-1/+1`; 2D movement
is one cardinal unit offset. The 2D shape has two positive extents and
shape-product tape size. Fixed/NONE outward movement terminates; periodic and
reflective movement normalizes to an existing destination, including
same-cell aliases.

### Media presets — 2

```python
constant_digit_register(
    *, register: int,
    register_law: rules.RuleExpr,
    digit_projection: rules.RuleExpr,
    base: int = 10,
) -> SimpleProgram

look_and_say(*, digits: tuple[int, ...]) -> SimpleProgram
```

The register form requires a nonnegative exact integer, `base >= 2`, and two
closed expressions evaluated over the old `{register, digit}` record; both
fields commit atomically. Look-and-say requires a nonempty tuple of
nonnegative exact integers and emits one length/value pair per maximal equal
run.

### Criteria presets — 3

```python
local_constraint_system(
    *, partial_assignment: alphabets.ValueNode,
    predicates: alphabets.ValueNode,
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram

template_constraint_system(
    *, partial_assignment: alphabets.ValueNode,
    allowed_templates: alphabets.ValueNode,
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram

seeded_template_constraint_system(
    *, partial_assignment: alphabets.ValueNode,
    allowed_templates: alphabets.ValueNode,
    required_occurrences: tuple[alphabets.ValueNode, ...],
    relation: rules.RuleExpr,
    cardinality: rules.Cardinality,
) -> SimpleProgram
```

These forms compile explicit `ValueNode` presentations, a closed relation, and
an exact or undetermined cardinality into an intensional relation; they do not
invoke or hide a solver. The seeded form additionally requires a nonempty
immutable tuple of `ValueNode` occurrences.

### True aliases and compatibility adapter

The four `A` callables have signatures identical to their targets and exact
zero-delta expansions:

- `elementary_cellular_automaton` → `eca`
- `network_rewrite` → `parallel_network_rewrite`
- `multiway_system` → `multiway_rewrite`
- `pde` → `partial_differential_relation`

The sole `K` callable has the same closed domain and signature as
`neighbor_updating_mobile_automaton`:

```python
extended_mobile_automaton(
    *, initial: tuple[int, ...], head: int, colors: int,
    transitions: tuple[
        tuple[
            tuple[int, int, int],
            tuple[tuple[int, int, int], int],
        ],
        ...,
    ],
    boundary: loci.Boundary[int] = PERIODIC,
) -> SimpleProgram
```

It emits `DeprecationWarning`, delegates losslessly, serializes byte-identically
to the target, and is available only as
`ca.catalog.machina.extended_mobile_automaton`.

## Implemented Plan

1. `catalog.entries` now owns explicit immutable `FAMILY_ENTRIES`,
   `ROLE_ENTRIES`, `LEGACY_ENTRIES`, and `NAME_ENTRIES`. Lookup returns
   metadata only.
2. The six category modules define every callable once in its primary home
   and do not import `catalog.entries`.
3. `catalog.__init__` is the sole callable/metadata join and lists every
   navigation and flat name explicitly.
4. Root `ca` exposes only the `catalog` namespace, not individual catalog
   callables.
5. `tests/conformance/g7_catalog_manifest.py` is literal test-owned expected
   data and imports no production `ca`.
6. CT11, catalog unit tests, family coverage, and the observer/role boundary
   are active and independently check the frozen metadata and callable
   relations.

## No-Cheating Checks

- [x] Category modules do not import `catalog.entries`; core, `program`, and
  `serialization` do not import catalog.
- [x] Metadata contains no callable, component, program, executor key,
  registry hook, or construction handler.
- [x] There is no `construct(id)`, umbrella `kind=`, registration hook,
  synthesized function, module `__getattr__`, wildcard discovery, or second
  executor.
- [x] Production code does not select behavior by SPF/F/T ID, family, home,
  constructor spelling, Book source, carrier, or locus kind.
- [x] All 105 callables are keyword-only, annotated, nonvariadic, and contain
  no `Any`, callback, ambient RNG, hidden solver, ignored argument, silent
  float fallback, or silent cross-type coercion.
- [x] All returned values are ordinary five-field `SimpleProgram` instances
  using the single generic `apply`.
- [x] Equivalent preset, specialization, alias, and adapter paths compare
  equal and serialize byte-identically.
- [x] Canonical payloads contain no `catalog:` or catalog-source receipt and
  are decoded without importing catalog.
- [x] T08 alone has zero targets; T40 alone has two named targets; T32/T44 are
  presets; F010/F042 remain callable-free roles; the sole K remains qualified.
- [x] Goal 2, Goal 5, and Goal 6 are unchanged.

## Completion Requirements

- [x] SPF IDs are exactly SPF001–SPF060 with unique audit IDs, slugs,
  constructors, and primary homes.
- [x] Home counts are `11 / 15 / 8 / 14 / 9 / 3`; coverage is
  `19 covered / 41 addition`.
- [x] F010/F042 are the two close roles, F039 remains unused, and no role owns
  a constructor.
- [x] Legacy IDs are exactly T01–T45 with disposition counts
  `15 / 21 / 2 / 3 / 2 / 1 / 1` and exact candidate/source/target joins.
- [x] The 49 callable legacy relations are
  `C=5 / P=39 / A=4 / K=1`; the non-T look-and-say preset brings the complete
  public kind census to `60 C / 40 P / 4 A / 1 K`.
- [x] Every constructor, preset, alias, and adapter has a closed explicit
  signature and a codec-covered five-field expansion.
- [x] All 60 canonical wrappers join their exact metadata and representative
  mechanics.
- [x] `ca.catalog` is the twelfth root name; no catalog callable is flattened
  to root `ca`.
- [x] CT11, CT14's role boundary, catalog unit tests, and constructor/metadata
  family coverage pass with no G7-04 skip.
- [x] Focused, full, static, codec, import, lock, compile, whitespace, and
  hostile gates pass.

## Stage Results

- The final catalog inventory is
  `60 canonical / 40 preset / 4 alias / 1 compatibility`,
  `60 family / 2 role / 45 legacy / 105 name`, and
  `105 qualified / 104 flat / 111 catalog __all__ / 12 root`.
- Every alias has the delegate's exact signature. K has the exact
  neighbor-updating signature and expansion.
- Hostile review found and closed four real defects:
  - preset-specific witness/provenance strings leaked invocation identity;
  - rational recurrences silently coerced an explicit integer zero bias;
  - missing Turing transitions returned an unchanged successor rather than a
    typed terminal result; and
  - anchored movement could reject at Frontier before Rule-owned boundary
    semantics ran.
- The repaired source uses mechanics-level evidence, omission-derived exact
  recurrence zero, global finite Turing clause tables with terminal fallback,
  periodic anchored mobile carriers, and explicit normalized Turing
  destinations.
- Exact equality and byte-equality tests cover aliases, K, CA
  specializations, rank-specific versus lattice paths, arithmetic versus
  digit reversal, and 2D substitution versus geometric substitution.
- Focused catalog/conformance verification:

  ```text
  338 passed in 15.77s
  ```

- Complete active verification:

  ```text
  975 passed
  ```

- Static reconciliation proves `60 / 2 / 45 / 105`, all 105 explicit
  signatures, 12 root names, 111 catalog names, 40 codec-clean presets, one
  `apply`, no core/catalog back-edge, and no pending production stub.
- `uv lock --check`, package compilation, `git diff --check`, and the final
  hostile review pass.

## Handoff

G7-04 is complete. G7-05 (`6-CONFORMANCE`) is now the first incomplete stage.
It must run the complete normative matrix together, add only missing
cross-suite/static/wheel evidence, and must not reopen the catalog contract
without a concrete contradiction. No G7-05 stage file or implementation work
has started.
