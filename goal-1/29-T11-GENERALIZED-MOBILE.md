# 29-T11-GENERALIZED-MOBILE

Status: **IN PROGRESS — HOSTILE REVIEW AND FINAL GATES PENDING**

## Current Facts

- T11 is CSV row 12, Generalized Mobile Automata, taxonomy section 11. The taxonomy supplies search vocabulary only.
- The frozen 16-query source audit closes 130 unique query lines at 108 pre-Index and 22 actual-Index. It retains 20 search hits plus six governed continuations, excludes 88 false positives, reverse-closes all 17 split documents, and leaves zero unresolved source candidate.
- BOOK:916-934 defines more than one active cell, one rule firing for every old active cell, split, disappearance, proliferation, and an almost-all-active cellular-automaton limit.
- The damaged Notes continuation at BOOK:12008-12010 exposes the complete operational core: a value list and active-position list, old-snapshot radius-one reads, one new value at each old source, and exact Union composition of translated next-active positions.
- The direct plates at BOOK:922,926,932 show the local binary profile. Their result dots include offset 0 and empty, singleton, pair, and triple subsets of {-1,0,+1}; prose shorthand about left/right movement and splitting in two is not an exhaustive result schema.
- T11 value writes cannot conflict: each distinct old active source writes only its own position. Proposed activity destinations can collide, and the source defines their composition as idempotent set union.
- DOMAIN is discrete t+1D. The fixed integer line is configuration support/topology, not the meaning of DOMAIN.
- A complete state can be a line labeled by Bit × ActiveFlag, equivalently Plain(Bit) | Active(Bit), with a finite set of active tags. The Notes factorization (bit field, active set) is a checked lossless view, not a required top-level state class.
- Post-extinction behavior is source-underdetermined. GMAStep does not successfully define a step from an empty active list, so strict Goal 2 must expose NoActiveSources without inventing terminal-versus-absorbing behavior.
- Goal 1 changes only goal-1/. Runtime implementation, public API revisions, and runtime tests belong to Goal 2.

## Updated Assumptions

- The binary fixed line, physical left/self/right bit read, and source-site value write are inherited directly from ordinary mobile automata.
- Exactly-one activity is not inherited. A valid T11 configuration has a canonical finite active set, possibly empty after a transition.
- Every old active source fires exactly once against the same old value field. Newborn destinations cannot fire until a later event.
- One row result is a new source bit plus a finite literal set of relative next-active offsets. The main-text local profile restricts those offsets to subsets of {-1,0,+1}; the executable Notes schema accepts finite relative-position lists more generally.
- UPDATE first validates all source results, applies distinct source-bit assignments, and replaces the activity factor by the union of translated proposals. It does not union proposals with the old activity set.
- A tagged lowering emits one complete next-cell label at each position in old_active union next_active. This lowering reuses atomic finite writes after global result normalization.
- T11 therefore needs a reusable closed component-composition preset on the UPDATE axis, not a family executor, special state class, hidden activity cache, or arbitrary conflict callback.
- The page-91 example table, its trajectory, the local 16-result row space, 16^8 = 2^32, and optional bit planes are derived from hash-bound visual evidence. The book states no T11 rule count, number, or codec.

## Big Picture Objective

Reconstruct generalized mobile automata from complete primary evidence and identify the smallest branch-free SimpleProgram fit for multiple simultaneous firing sources, source-local value assignment, activity creation/deletion, and idempotent destination composition. Preserve the full state and native step semantics without treating the present CA-shaped realization of src/ca as the abstraction.

## Catalog Identity

- Stable ID: T11.
- CSV line: 12.
- Catalog name: Generalized Mobile Automata.
- Taxonomy section: 11.
- Construction kind: deterministic transition construction over a fixed labeled line with a finite active-source set.
- Search vocabulary: generalized mobile automata, mobile automata, active cells, GMAStep, nlist, multiple activity, split, disappear, proliferate, relative positions, every active cell, CA interpolation, historical aliases, Notes syntax, and actual Index routes.
- Index route: BOOK:21213 contains Generalized mobile automata, 76. There is no literal page 76 route in prose or Notes.

## Search Log

### Exact query protocol

goal-1/29-T11-source-oracle.py freezes 16 case-insensitive line queries:

1. direct generalized-mobile names;
2. the wider mobile-automaton family;
3. active-cell wording;
4. GMAStep and nlist;
5. quantified multiple-active wording;
6. create, split, disappear, and proliferate wording;
7. active-position and relative-position wording;
8. application to every active cell;
9. ordinary-mobile/CA interpolation;
10. a literal page-76 control;
11. historical and multiple-active aliases;
12. collision/conflict/activity-layer API jargon;
13. CA-limit wording;
14. exact executable composition syntax;
15. one-active predecessor boundaries;
16. split/disappear/proliferate near active-cell wording.

The per-query counts are:

| Query | total | pre-Index | actual-Index |
|---|---:|---:|---:|
| Q00 | 6 | 5 | 1 |
| Q01 | 119 | 98 | 21 |
| Q02 | 47 | 44 | 3 |
| Q03 | 1 | 1 | 0 |
| Q04 | 4 | 4 | 0 |
| Q05 | 4 | 4 | 0 |
| Q06 | 1 | 1 | 0 |
| Q07 | 1 | 1 | 0 |
| Q08 | 1 | 1 | 0 |
| Q09 | 0 | 0 | 0 |
| Q10 | 1 | 0 | 1 |
| Q11 | 0 | 0 | 0 |
| Q12 | 2 | 2 | 0 |
| Q13 | 1 | 1 | 0 |
| Q14 | 8 | 7 | 1 |
| Q15 | 3 | 3 | 0 |

After union and deduplication:

- query union: 130, digest 796e7dc0f8d55ee6ef7627939c87ee942d147ac44538d91afd9f8c1ab7aae514;
- pre-Index union: 108, digest e420645cbf4c0ddaa39511d780394208dcf213b9a6cce30c17cac8ef1182ed4c;
- actual Index: 22, digest 7e730c202bc5917d39e6577bcac44d8adfd6e6157446e801aa61312ea2da84e4;
- matched retained: 20, digest 04d299273ce081cadd3b14cc9e070a09aaf5cfc50a5e93ee66dd2b2fb62d0ec7;
- governed continuations: 6 at BOOK:850,858,860,922,926,932;
- final retained: 26, digest 15ec07596824fc5034feaba4735d329e74826b2849fa260b7053bbf07fe1ce8c;
- excluded pre-Index candidates: 88, digest cf7b3013909633e3d4a5be2f61e816bed83b65089e42d72eb0e83240ebae7905.

### Split, Atlas, and catalog closure

- All 17 split Markdown documents are manifest-bound.
- The split query universe has 130 reverse records: 123 exact and seven explicit extraction variants.
- Retained material has 19 exact mirrors and seven explicit non-exact mirrors at BOOK:854,858,860,862,922,926,932.
- The seven wider query variants are mapped explicitly, including the Chapter 11 emulation extraction and Chapter 7 observer extraction.
- Direct-name text occurs only in the Chapter 3 split and the Colophon stream.
- ANKoS-Atlas.md has three generic mobile/active hits at lines 7,81,83 and no generalized-mobile, GMAStep, page-76, or collision hit.
- CA-Types.csv, CA-Types.md, the monolith, all split files, and the Atlas are hash-bound.
- The malformed lead-in at BOOK:12008 is identically truncated in monolith and split material. It is quoted only as a continuation; no heading is fabricated.

### Candidate disposition

| Candidate class | Disposition |
|---|---|
| BOOK:848-864,914-934,982,11955-11965,12008-12010 | retained native baseline, generalized construction, fixed-support contrast, and executable semantics |
| BOOK:868-912,11982-12006 outside governed T11 lines | ordinary/extended one-active behavior, motion, or Notes controls |
| BOOK:940-958,1042 | Turing/sibling systems |
| BOOK:1256,1352-1360,4136,4196 | historical or behavior comparisons |
| BOOK:5818-5942,6008-6012,16388-16398 | causal, path, substitution, or observer relations |
| BOOK:7924-8014,16442,18352-18463 | CA/substitution emulations or reverse relations |
| BOOK:13679,16066,16400,16648-16654 | 2D, reversible, motion, or network siblings |
| BOOK:14275 | ordinary mobile random-seed note |
| 22 Index hits | all followed; Sequential automata redirects only to ordinary Mobile automata |

No excluded candidate adds a T11 boundary, halt, conflict policy, seed law, rule codec, or alternative native update.

## Book Excerpts

### E01 — inherited binary line and local read

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:850-864.
- Establishes: ordinary mobile automata use a binary line, one active source, an immediate-neighbor read, a new source color, and left/right movement. T11 explicitly generalizes the source cardinality.

> The rule applies only to this active cell. It looks at the color of the active cell and its immediate neighbors, then specifies what the new color of the active cell should be, and whether the active cell should move left or right.

### E02 — defining multiple-active construction

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:916-924.
- Establishes: the named family, more than one active cell, split, disappearance, creation, any active count, and one application to every cell active at that step.

> The basic idea of such generalized mobile automata is to allow more than one cell to be active at a time. And the underlying rule is then typically set up so that under certain circumstances an active cell can split in two, or can disappear entirely.
>
> The rule given above is applied to every cell that is active at a particular step.

The words typically, many cases, and some cases are descriptive, not a closed output enumeration.

### E03 — proliferation and CA limiting behavior

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:928-934.
- Establishes: finite-time active proliferation in the examples and CA-like behavior when almost all displayed cells are active.

> In case (a), only a limited number of cells ever become active. But in all the other cases shown active cells proliferate forever. In case (d), almost all cells are active, and the system operates essentially like a cellular automaton.

This is a behavior/relation claim, not identity with an arbitrary CA table.

### E04 — fixed support

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:982.
- Establishes: cellular automata, mobile automata, and Turing machines share a fixed array whose organization does not change.

> at the lowest level they consist of a fixed array of cells

The fixed array is configuration support. It does not redefine DOMAIN, which remains t+1D.

### E05 — factored state and typed row result

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12008.
- Context: extraction-truncated continuation immediately before GMAStep.
- Establishes: value list, list of active positions, and a result consisting of a new source value plus relative new-active positions.

> specified by {list, nlist}, where list gives the values of the cells, and nlist is a list of the positions of active cells. The rule can be given by specifying a list of cases such as {0, 0, 0} -> {1, {1, -1}}, where in each case the second sublist specifies the new relative positions of active cells.

### E06 — old-snapshot evaluation and exact composition

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:12010.
- Establishes: Map evaluates all old active reads before Fold writes old sources; Union after translation flattens, sorts, and deduplicates the complete next activity.

~~~text
GMAStep[rules_, {list_, nlist_}] :=
  Module[{a, na},
    {a, na} =
      Transpose[
        Map[Replace[Take[list, {# - 1, # + 1}], rules] &, nlist]];
    {Fold[ReplacePart[#1, Last[#2], First[#2]] &,
          list, Transpose[{nlist, a}]],
     Union[Flatten[nlist + na]]}]
~~~

For a canonical set of old positions, source value targets are distinct. Activity collisions are not value-write conflicts; they coalesce idempotently.

### E07 — actual Index route

- Source: ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md:21213.
- Establishes: the actual Index points Generalized mobile automata to page 76 and separately mentions paths of particles on page 531.
- Limitation: the extracted Index line is highly interleaved, so it is navigation only.

## Source-Underdetermined Boundaries

| Question | Evidence-closed answer |
|---|---|
| post-extinction step | unspecified: disappearance is native, but GMAStep has no successful empty-nlist branch |
| native finite boundary | none stated; finite host list syntax does not define wrap, reflection, fixed exterior, truncation, or halt |
| duplicate active inputs | not validated by host code; semantic state uses a canonical finite set |
| incomplete or duplicate table rows | not validated by Replace; strict typed construction requires one total row per reachable Bit^3 context |
| exhaustive output offsets | text allows finite relative-position lists; direct plates establish the local {-1,0,+1} profile but not a universal radius bound |
| rule count/number/codec | no source statement |
| seed class | no general rule; the direct plates supply an all-white, one-active fixture |
| random frequency and behavior class | observations only |

## Asset Ledger

goal-1/29-T11-asset-oracle.py binds the retained source digest and closes a zero-remainder physical universe.

- Mechanical radius-four source neighborhood: 10 assets.
- Explicit predecessor/successor companions: 6 assets.
- Total: 16 unique physical JPEGs, 16 monolith references, 16 split references, 16 unique hashes.
- Universe digest: 48158fc4a89e8dcfdc2611799b0152309478a5c7d5f3aea439597f946b12fc8b.
- Ledger digest: bc00a4fac328069714ba8cd20713a6bb47774c1d0f2e8d06b491526f5a127c89.
- Strict direct subset digest: daa4b34781edb487e6dc388cbe60f94a261c27d2fcc9c00a23a0d5bca2d2d7f1.
- Strict ledger digest: 0c713a3c4775fac478c8b75907cd35fc0ec9518131c4790b116e92dac8ccd346.

| Class | BOOK image lines | Disposition |
|---|---|---|
| C construction | 922,932 | direct rule plates; 932 also contains evolution panels |
| O observer | 926 | direct page-91 evolution |
| R relation | 858,860,866,900,902,906,908,910,944,946 | ordinary/extended mobile predecessor and Turing successor plates |
| X control | 844,12004,12006 | preceding CA and page-75 motion-note adjacency controls |

Counts are C/O/R/X = 2/1/10/3. Direct visual hashes pin:

- BOOK:922: one exact example rule strip and its activity dots;
- BOOK:926: simultaneous multiple-active evolution;
- BOOK:932: eight rule/evolution examples whose result glyphs visibly include {}, {0}, {0,+1}, and {-1,0,+1}.

The plate frames, widths, gray palette, dots, crops, and raster dimensions are observers/encodings. They are not finite boundaries or runtime state schemas. The Notes opening text is missing, but no native raster is missing.

## Construction Model

### Native state and transition

Let Bit = {0,1}. A factored state is:

~~~text
configuration = (values : Z -> Bit,
                 active : FiniteSet[Z])
~~~

For a valid nonempty old active set A:

~~~text
sources = FRONTIER.select(configuration) = sorted(A)

for each p in A, from the same old values:
    reads[p] = (values[p-1], values[p], values[p+1])
    (new_bit[p], offsets[p]) = table[reads[p]]

next_values[p] = new_bit[p]  for p in A
next_values[x] = values[x]   for x not in A

next_active =
    union over p in A of {p + d | d in offsets[p]}
~~~

All row evaluation precedes all mutation. Newborn loci are next-event sources only. Different sources may have overlapping read neighborhoods; this is harmless because reads share one immutable snapshot. Distinct old sources own distinct bit assignments.

### Rule schema and local profile

The evidence-wide structural row type is:

~~~text
Bit^3 -> Bit x FiniteSet[Z]
~~~

Each row stores a finite literal offset set. The direct page-76 local profile is:

~~~text
Bit^3 -> Bit x P({-1,0,+1})
~~~

It has eight contexts and 2 × 2^3 = 16 possible row results. Therefore the local-profile rule space is derived as:

~~~text
16^8 = 2^32 = 4,294,967,296
~~~

This is not a source-stated count and has no source-defined integer codec. For arbitrary finite integer offset lists the Notes schema is wider, so 2^32 must never be presented as the whole generalized family.

### Exact derived page-91 fixture

Reading gray as 1, white as 0, physical context order left/self/right, and dots as relative activity, the hash-bound BOOK:922 strip transcribes:

~~~text
111 -> (0,{+1})
110 -> (0,{+1})
101 -> (1,{+1})
100 -> (1,{0,+1})
011 -> (1,{-1})
010 -> (1,{-1,+1})
001 -> (1,{-1})
000 -> (1,{-1,+1})
~~~

The 000 result does not contain offset 0; the gray output square has no central dot. Under the optional inferred index i = 4L + 2C + R, the four low-significance-first result planes are (new_bit,left,center,right) = (63,15,16,245). These planes are a derived fixture only.

From values(x)=0 and A={0}, the exact derived trace is:

~~~text
t0  ones=()                                           active=(0,)
t1  ones=(0,)                                         active=(-1,1)
t2  ones=(-1,0,1)                                     active=(-2,1,2)
t3  ones=(-2,-1,0,2)                                  active=(-3,2,3)
t4  ones=(-3,-2,-1,0,2,3)                             active=(-4,1,3,4)
t5  ones=(-4,-3,-2,-1,0,1,2,4)                       active=(-5,2,4,5)
t6  ones=(-5,-4,-3,-2,-1,0,1,4,5)                    active=(-6,3,5,6)
t7  ones=(-6,-5,-4,-3,-2,-1,0,1,3,4,6)               active=(-7,2,6,7)
t8  ones=(-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,6,7)        active=(-8,3,5,7,8)
t9  ones=(-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,4,5,6,8)     active=(-9,4,6,8,9)
t10 ones=(-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,4,5,8,9)  active=(-10,3,7,9,10)
t11 ones=(-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,7,8,10)
    active=(-11,4,6,10,11)
t12 ones=(-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,5,6,7,8,10,11)
    active=(-12,5,7,9,11,12)
~~~

The semantic oracle derives this transition-by-transition; it does not compare raster pixels as runtime state.

### Lossless tagged/factored representation

A transparent cell form is:

~~~text
Cell = Plain(Bit) | Active(Bit)
encode(values,A)[x] =
    Active(values[x]) if x in A
    Plain(values[x])  otherwise
~~~

The inverse strips the tags to recover values and returns exactly the finite set of tagged positions. Unlike a bare Bit union Marker, the active label retains the underlying bit. Unlike T09/T10/T12, there is no exactly-one invariant.

goal-1/29-T11-semantic-oracle.py exhaustively proves factored/tagged commutation for every binary assignment on five relevant positions, every nonempty subset of three neighboring sources, and every combination of all 16 local row results. That is 157,184 composition cases. It also checks inverse round trips, outside preservation, split, disappearance, offset-0 survival, collision, source/destination overlap, source-order invariance, and old-snapshot scheduling.

### UPDATE composition and complete-write lowering

The native factor composition is:

~~~text
Bit factor:
    DistinctAssign({p -> new_bit[p] | p in old_active})

Activity factor:
    ReplaceWithUnion(
        {{p+d | d in offsets[p]} | p in old_active}
    )
~~~

ReplaceWithUnion unions the proposals with one another and replaces the old activity factor. It does not preserve an old tag unless offset 0 or another source proposes that location.

After aggregation, an equivalent atomic tagged lowering uses targets old_active union next_active:

~~~text
for x in old_active union next_active:
    bit_x =
        new_bit[x] if x in old_active
        old_bit[x] otherwise
    tag_x = Active if x in next_active else Plain
    write complete Cell(tag_x,bit_x) at x
~~~

Targets are distinct by construction, so generic AtomicFiniteWrites commits the normalized map from one old snapshot. This is a reusable UPDATE-axis component-reducer preset plus a lossless lowering, not a T11 executor or arbitrary collision policy.

Three adversaries distinguish the responsibilities:

1. Two sources can propose the same destination. The activity factor contains it once.
2. One source can activate a position that is also another old source. That position receives the latter source's new bit and the union-derived active tag.
3. A source with no outgoing offset is untagged even though its bit assignment still commits.

### Empty activity and outcomes

A transition may produce next_active = empty. That resulting configuration is complete and valid. A further strict step is not source-defined:

- it cannot fire a rule because FRONTIER selects no source;
- GMAStep's Transpose assignment does not define the empty case successfully;
- the book does not say terminal, absorbing, or error.

Goal 2 should return a typed Quiescent(NoActiveSources) or equivalent non-advancing outcome while keeping terminal-versus-stutter projection outside the native construction. It must not synthesize an observer-visible duplicate state as though the book specified an absorbing transition.

### DOMAIN, support, realization, and trace

- DOMAIN: discrete t+1D.
- Native support/topology: fixed ordered integer line.
- ALPHABET: binary value plus active flag/tag.
- Invariant: active positions form a canonical finite set; duplicates and hidden caches are invalid.
- FRONTIER: all old active tags.
- NEIGHBORHOOD: physical offsets [-1,0,+1], projected to underlying bits.
- RULE result: one new source bit plus finite relative activity offsets.
- UPDATE: distinct source assignments plus replacement by proposal union, committed atomically.
- Successor: one deterministic successor when the old active set is nonempty and the table is total.
- Seed fixture: all-zero field with active set {0}; broader seed choice is independent T08 data.
- Boundary: none natively. Any finite list edge is a computation realization obligation.
- Trace: complete tagged configurations and per-source event witnesses before rasterization or compression.

### Variants, relations, and identity

- Ordinary mobile T09 is the exactly-one, one-destination {-1,+1} restriction with a different continuation invariant.
- Extended mobile T10 widens source value writes to three cells but retains one source. Its block writes must not be imported into T11.
- The page-76 local profile restricts output offsets to {-1,0,+1}; arbitrary finite Notes offsets are a wider parameterization.
- An almost-all-active run can behave like a CA, but behavior similarity is not arbitrary-CA program identity.
- A constrained tagged CA can emulate one step. For the local profile a target-local all-sites compiler generally needs radius two: target activity can depend on a neighboring source's far-side bit.
- 2D mobile and network mobile change dimensional DOMAIN or support/topology/access schemas and remain siblings.
- Activity plots, active counts, width, behavior class, paths, causal networks, rule glyphs, and raster frames are observers.
- Native identity is the structural table plus typed result schema and support/configuration schema. Codec, seed, run, finite realization, compiler, trace, and view identities remain separate.

## Current API Fit

The intended SimpleProgram algebra fits T11. The current simple_programs.md is a CA-shaped realization that must broaden at its own axes.

| T11 responsibility | Current document evidence | Classification | Smallest Goal 2 correction |
|---|---|---|---|
| discrete t+1D | simple_programs.md:115-198 | direct dimensional responsibility | keep DOMAIN separate from integer support and finite SHAPE |
| tagged binary labels | :200-234 admits finite scalar values only | shared principled extension | generic products/tagged unions plus configuration invariants |
| all active firing sources | :1412-1510 defines writable next coordinates | semantic mismatch in wording | FRONTIER.select returns firing loci; add AllTags(active) |
| physical old radius-one read | :360-420 supplies ordered relative snapshot reads | parameterization | reuse offsets and add UnderlyingBit projection |
| typed table result | :1767-1797 returns one scalar at one writable coordinate | principled extension | closed OrderedTable[Read,Result] with structural results |
| multi-source evaluation | :1510,1791 requires same-snapshot parallelism | direct scheduling responsibility | evaluate every selected source before UPDATE |
| union/replace activity composition | no component reducer is exposed | new generic UPDATE-axis preset | DistinctAssign × ReplaceWithUnion, statically typed |
| complete-write commit | :1785-1787,2191-2197 supplies copy-forward and parallel write | direct after lowering | reuse AtomicFiniteWrites on the normalized distinct map |
| empty source outcome | current all-sites frontier hides the case | shared outcome obligation under D024 | typed NoActiveSources without invented successor |
| complete structured trace | scalar trajectory schema at :87-113 | shared principled extension | serialize full configurations and event witnesses before views |

The branch-free operational form is unchanged:

~~~text
active  = AllTags(active).select(state)
reads   = OrderedRelativeRead([-1,0,+1], UnderlyingBit).read(state, active)
results = OrderedTable.evaluate(active, reads)
next    = ParallelFactorCompose(
              bit=DistinctAssign,
              activity=ReplaceWithUnion
          ).apply(state, active, results)
~~~

The catalog name does not appear below preset resolution.

## Current Runtime Fit

| Current surface | Evidence from current files | Classification | Goal 2 migration |
|---|---|---|---|
| src/ca/alphabets.py | Value and Alphabet are flat scalar data at lines 40-56 | mismatch for visible tags | add generic product/tagged schemas, structural codecs, and invariant validation |
| src/ca/frontiers.py | lines 1-60 define update-site masks; only time_slice is executable | semantic mismatch | make frontiers typed firing-source selectors and add tag-derived selection |
| src/ca/loci.py | finite tensor universes/selectors only | reusable finite selector mechanics plus support extension | retain coordinate selection, add typed structural/source loci without callbacks |
| src/ca/neighborhoods.py | literal_offsets at lines 140-174 expresses geometry | parameterization | reuse ordered offsets with an explicit value-factor projection |
| src/ca/rules.py | Rule stores family strings and Any callback at lines 30,64-78; lookup returns scalar at 262-295 | mismatch | closed generic ordered tables and structural result schemas; no formulaic escape |
| src/ca/specs.py | Dynamics uses Any/dense shape and family decoders at lines 23-55,117-198 | mismatch | typed axis specs/registry; catalog presets compile before execution |
| src/ca/rollout.py | lines 145-212 branch on family; 825-831 rejects non-time_slice frontiers | mismatch | one runner invoking selected axis objects |
| spatial rollout | lines 643-660 computes a dense scalar all-sites next array | mismatch for source-relative factor results | collect result objects, normalize UPDATE effects, then commit |
| episode state | src/ca/specs.py:58-81 requires ndarray states | mismatch | structured complete configurations first; dense encodings are adapters |
| current tests | tests/test_rollout.py:529-544 proves other frontiers are rejected; no mobile/active tests exist | current behavior evidence only | add cross-family runner, commutation, composition, outcome, serialization, and edge tests |

The current 102 tests are regression evidence only. No family string, formulaic callback, dense four-color CA disguise, or metadata cache can execute T11 as its native construction.

## First-Principles Classification Matrix

| Responsibility | Evidence | Classification | Smallest reusable base | Required invariant | Reopen? |
|---|---|---|---|---|---|
| DOMAIN | fixed line and time evolution | 1 direct reuse | T09 discrete t+1D | dimensional tag matches support | no |
| support/topology | BOOK:982 | 1 direct reuse | fixed integer line | organization unchanged | no |
| ALPHABET | values plus activity positions | 2 parameterization | tagged/product finite labels | tag retains underlying bit | no |
| configuration representation | tagged versus factored | 3 lossless representation | generic product/tag mapping | finite canonical active set; inverse round trip | no |
| FRONTIER | every old active cell fires | 2 parameterization | generic state-derived selector | exactly the old active set, once each | D009 strengthened |
| NEIGHBORHOOD | immediate neighbors | 1 direct reuse | T09 ordered radius-one read | physical L/C/R, old snapshot | no |
| RULE input/table | Bit^3 total table | 1/2 direct table parameterization | generic OrderedTable | eight unique rows for strict binary profile | no |
| RULE result | new source bit plus relative positions | 2 typed result parameterization | generic product result | finite normalized offset set | D011 strengthened |
| UPDATE composition | source assignments plus proposal union | 2 reusable named preset | generic component reducers + atomic commit | distinct source targets; activity set replaced by proposal union | add D123 |
| tagged lowering | complete writes at A union A-prime | 3 lossless representation | D011 AtomicFiniteWrites | one complete write per distinct target | no |
| executor/runner | one deterministic successor | 1 direct reuse | common SimpleProgram runner | no family dispatch | no |
| empty outcome | GMAStep gap | explicit evidence boundary | D024 typed outcome | no invented successor | no |
| local CA compiler | target-radius-two relation | 3 relation, not identity | generic compiler record | one-step commute on valid image | no |
| new execution algebra | no counterexample remains after factor composition | 4 not justified | none | branch-free pipeline | no |

This is the requested distinction: typed roles and one new reusable UPDATE-axis combiner are sufficient. There is no T11 semantic state class or executor.

## Principles Audit

- Principles 0-3 require re-deriving the construction rather than treating time_slice, scalar lookup, or dense ndarray state as the SimpleProgram boundary.
- Principle 4 places source selection, reads, result production, and effect composition at separate typed axes. AllTags is FRONTIER; translated activity destinations are RULE-result data.
- Principle 5 requires the complete activity set in state. Tagged labels and the factored Notes form are equivalent; neither may become hidden executor state.
- Principles 6-8 keep t+1D, fixed integer support, active/value factors, sparse realization, and raster marks distinct.
- Principles 9-10 allow the local page-76 profile and broader finite-offset Notes form as validated presets over the same structural schema.
- Principle 11 makes old-snapshot evaluation and exact Union composition defining semantics. Source order, last-writer policy, sequential mutation, and newborn firing are forbidden.
- Principle 12 keeps behavior frequencies, activity density, particle paths, causal networks, and images downstream of the trace.
- Principles 13-15 are exercised by 157,184 commuting cases, exact page-91 replay, collision, overlap, disappearance, old-snapshot, order, empty-frontier, and compiler-radius adversaries.
- Principle 16 treats factor composition and tagged lowering as explicit mappings, not fallback dispatch. One runner remains.

## Dependent Decision Audit

| Decision/stage | T11 result |
|---|---|
| D009 | decisive confirmation: FRONTIER is the set of old firing sources, not source sites union next-active destinations |
| D010 | activity is a visible role in complete configuration; multiple tags invalidate only the T09/T10 exactly-one preset, not the representation |
| D011 | typed results may carry source assignments and structural proposals; complete tagged writes remain an atomic lowering |
| D012 | physical left/self/right bit order remains shared |
| D013 | raw traces preserve every active tag and per-source witness before activity plots or compression |
| D014/T12 | same lossless-tag principle, but no head-state payload; T12 remains closed |
| D024 | empty-frontier handling remains construction-specific and source-underdetermined |
| D043 | multiplicity-preserving occurrence-bag composition is not T11 activity semantics |
| D054 | finite successor-set union is a different layer from union of destinations inside one deterministic successor |
| D122/T10 | T10 remains one-source, three-value-write; T11 remains multi-source, center-value-write |
| T01/T09/T13 | all-sites assignment, exactly-one mobile, and ordered substitution remain strict presets/siblings; none reopens |

### D123 candidate — generalized mobile uses typed factor composition, not a family executor

- Status: proposed for activation after hostile review and final gates.
- Basis: BOOK:918-924 supplies a finite set of simultaneous firing sources; BOOK:12008 gives one source value plus relative activity positions; BOOK:12010 evaluates all old reads, writes distinct old sources, and replaces next activity by exact Union.
- Configuration: discrete t+1D fixed line labeled by Plain(Bit) | Active(Bit), with a canonical finite active set, losslessly equivalent to (bit field, active set).
- Execution: AllTags selects all old sources; physical old [L,C,R] bits are read; a total table returns (new_source_bit,finite_offsets); UPDATE applies distinct bit assignments and ReplaceWithUnion activity composition atomically.
- Lowering: after union normalization, emit distinct complete labels on old_active union next_active and reuse D011 AtomicFiniteWrites.
- Identity: the structural table/result schema is primary. The page-76 local profile has a derived 16^8 rule space; no T11 number or codec is invented.
- Boundary: no family branch, hidden state, arbitrary conflict policy, multiplicity, boundary, or post-extinction continuation is added.
- Consequence: Goal 2 adds one generic closed component-reducer preset and conformance fixtures inside the shared runner. It adds no GeneralizedMobileState, update executor, or catalog dispatch.

## Detailed Implementation Plan

1. **COMPLETE:** freeze and disposition every direct, alias, active-cell, split/disappear, Notes, implementation, page, relation, and actual-Index query.
2. **COMPLETE:** reverse-close all split documents, Atlas, catalog, taxonomy, extraction variants, and governed source continuations.
3. **COMPLETE:** close the source-bound physical fixed point with hashes, reverse references, semantic classes, visual facts, and zero unresolved asset.
4. **COMPLETE:** reconstruct state, frontier, read, result, schedule, union composition, lowering, outcomes, support, seed, variants, relations, and observers.
5. **COMPLETE:** implement exhaustive representation/composition, page-91, old-snapshot, collision, overlap, disappearance, order, empty-outcome, and compiler-radius oracles.
6. **COMPLETE:** audit simple_programs.md, src/ca, tests, principles, D009-D014/D024/D043/D054/D122, and dependent stages from current files.
7. **IN PROGRESS:** hostile-review D123, the Goal 2 handoff, exact fixture, source/asset closure, and no-cheating claims.
8. **PENDING:** run all root/tmp/-O/oracle/test/Markdown/diff/scope/coverage gates, activate D123, and reintegrate the plan/evidence/ledger.

## Goal 2 Implementation Stage

### G2-T11 — finite active-source composition over the shared runner

Implement after generic configuration/tag/source-frontier/finite-write work from G2-T08/G2-T09 and the structural-result work from G2-T10. This stage adds a generic component reducer and one strict preset, not a runner.

| Goal 2 surface | Required work |
|---|---|
| dependencies | G2-T01 runner/configuration shell; G2-T02 ordered tables; G2-T08 complete seeds and finite lowerings; G2-T09 tagged activity/source selection; G2-T10 structural results and atomic finite writes; shared D024 outcomes |
| ALPHABET/configuration | construct Plain(Bit) | Active(Bit) generically; validate a canonical finite active set and preserve the bit under each tag; support a checked factored view with no duplicate authority |
| FRONTIER | add/use AllTags(active), returning stable canonical source handles; reject duplicate/invalid tags and distinguish empty selection |
| NEIGHBORHOOD | reuse ordered relative [-1,0,+1] plus UnderlyingBit projection and old-snapshot scope |
| RULE schema | closed total OrderedTable[Bit^3, Bit × FiniteOffsetSet]; strict local constructor validates offsets subset {-1,0,+1}; wider constructor stores finite literal integer offsets |
| result evaluation | evaluate all sources before mutation; retain a typed event per source with source, read, native row result, and translated proposal set |
| UPDATE composition | add/use ParallelFactorCompose with DistinctAssign for source bits and ReplaceWithUnion for activity; validate all events before commit |
| lowering | normalize to one complete Cell write for every position in old_active union next_active; preserve destination bits unless that position was also an old source; prove equivalence to factor composition |
| outcome | when old activity is empty, return NoActiveSources without silently choosing terminal, absorbing, or error projection |
| StepResult/trace | record canonical source events, union witness, normalized writes, validation evidence, before/after references, and ordinary one-successor Advanced outcome |
| strict preset | generalized_mobile_binary(table, offset_profile=local_radius_one) resolves to ordinary axes. No family value reaches the runner |
| identity/serialization | structural table/result schema first; round-trip arbitrary signed offsets, tags, sparse fields, event witnesses, and optional versioned derived codecs |
| finite realization | prevalidate the complete read/proposal/write horizon or use a separately identified topology/boundary approximation; no edge behavior becomes native |
| optional compiler | record a constrained tagged-CA relation, invariant-valid image, and sufficient target radius; do not replace native identity |
| migration | remove dependence on time_slice, scalar lookup, ndarray-only state, family branches, formulaic callbacks, hidden active metadata, or arbitrary four-color CA encodings |

### Acceptance groups

1. **Exact source fixture:** implement the eight BOOK:922 rows and independently replay the exact t0..t12 checkpoint.
2. **Local result space:** prove eight contexts, eight activity subsets, sixteen row results, and derived 16^8; keep this distinct from the wider finite-offset Notes schema.
3. **Schema validation:** reject missing, duplicate, extra, malformed, nonbinary, non-finite, non-integer, or profile-exceeding rows/offsets before execution.
4. **Multiple sources:** every old active position fires once; overlapping reads are legal and use one old snapshot.
5. **Old-snapshot adversary:** adjacent sources both reading 000 must not observe an earlier source's new bit.
6. **Union collision:** two sources proposing the same destination yield one active tag and no value-write conflict or multiplicity.
7. **Source/destination overlap:** a destination that is another old source combines that source's new bit with union-derived activity.
8. **Split/disappear/survive:** cover empty, singleton, pair, triple, offset-0, and all-sources-disappear results.
9. **Newborn schedule:** new destinations retain old underlying bits unless also old sources and cannot fire in the producing event.
10. **Exhaustive representation commutation:** preserve the 157,184-case factored/tagged composition proof and inverse round trips.
11. **Ordering:** permuting source enumeration cannot change next state; event serialization uses canonical order.
12. **Empty frontier:** preserve the complete empty-active configuration but emit NoActiveSources on another requested step; test external terminal/stutter projections separately.
13. **Atomic failure:** any invalid event/result/target fails before commit and exposes no partial bit/tag state.
14. **Identity:** distinguish equal bit fields with different active sets; distinguish local/wider schemas, tables, seeds, outcomes, realizations, compilers, traces, and views.
15. **Boundary:** separate native integer support, genuine finite topology, explicit boundary approximation, exact horizon lowering, and storage crop.
16. **Same runner:** representative T01, T09, T10, T11, T12, and T13 programs execute through one runner with no catalog/family condition below preset resolution.
17. **Compiler radius:** retain the target-radius-one counterexample and require radius two or an independently proved sufficient mapping for the local profile.
18. **Serialization/tamper:** round-trip complete tagged configurations, signed offset sets, source events, union witness, normalized writes, and outcomes; reject altered witnesses.
19. **Static no-cheating:** scan for T11 switches/classes/executors, Any/callbacks, hidden activity, sequential mutation, last-writer policies, fake capacity, and observer feedback.

Completion requires public typed schemas, exact fixtures, cross-family runner tests, fail-closed validation, serialization/tamper tests, static scans, finite-lowering adversaries, and no regression in existing programs.

## No-Cheating Checks

- No GeneralizedMobileState, GeneralizedMobileUpdate, T11 executor, family flag, rollout branch, callback, or opaque packed machine.
- No claim that the CA-shaped current API is the SimpleProgram abstraction.
- No taxonomy conflict-policy prose promoted over GMAStep's exact source semantics.
- No writable destination set called FRONTIER; only old active cells are firing sources.
- No T10 three-cell value writes imported into T11; strict T11 writes each old source value only.
- No sequential source application, newborn same-event firing, observer-visible intermediate configuration, or source-order dependence.
- No last-writer, first-writer, arbitrary callback, error-on-activity-collision, or multiplicity semantics. Destination activity is a set union.
- No old activity copied forward unless proposed by offset 0 or another source.
- No bare Bit union Marker that loses the bit, and no hidden or unsynchronized factored cache.
- No exactly-one or nonempty invariant inherited from T09 after the step.
- No universal {-1,0,+1} claim for the wider Notes schema and no arbitrary-offset claim for the local page-76 profile.
- No native 2^32 rule-count or numeric-code claim; those are derived only for the local profile.
- No finite tensor edge, crop, padding, wrap, reflection, truncation, or exception promoted to native line semantics.
- No absorbing or terminal post-extinction semantics invented from a failed host-language empty case.
- No arbitrary four-color CA table presented as compact T11 identity; any compiler is lossless, invariant-restricted, and one-step commuting.
- No activity raster, density, path, causal graph, behavior class, or random frequency fed into execution.
- No weakening or reopening of T09/T10/T12; T11 changes source cardinality and typed result composition only.

## Completion Requirements

- [x] Every declared query, candidate, continuation, split/Atlas/Index route, extraction defect, and source limitation is frozen with zero unresolved remainder.
- [x] Every governed physical asset is pinned or explicitly classified; direct construction/evolution evidence is separate from relations and controls.
- [x] State, DOMAIN/support, ALPHABET/activity, frontier, read, result, schedule, composition, successor, seed, boundary, variants, relations, observers, rule space, and identity are resolved or explicitly underdetermined.
- [x] Factored and tagged representations have an explicit inverse and exhaustive one-step composition proof.
- [x] Exact page-91, split, disappear, offset-0, collision, source-overlap, old-snapshot, ordering, empty-frontier, and compiler-radius adversaries are executable.
- [x] Current API/runtime/tests and all dependent decisions are audited from actual files.
- [x] The Goal 2 handoff identifies generic shared surfaces, public types, migration, serialization, outcomes, and adversarial acceptance without a T11 executor.
- [ ] Independent hostile review is clean and every oracle/test/Markdown/diff/scope/coverage gate passes after final integration.

## Re-Integration Audit

1. **Prior assumption invalidated?** Yes: the taxonomy's speculative need for an arbitrary conflict policy is contradicted by GMAStep. No active corrected design decision fails.
2. **Existing primitive reuse?** DOMAIN, support, tagged labels, physical read, ordered table, atomic commit, outcomes, traces, and the runner are reused. Only a reusable factor reducer/preset is added.
3. **Exception/flag/hidden state/callback?** None. The strict constructor resolves to ordinary typed axes.
4. **Complete Markov state/trace?** Yes. Every bit and active tag is in configuration; canonical event witnesses reproduce the factored transition.
5. **DOMAIN/support/value/activity/representation separation?** Yes. Discrete t+1D, integer support, bit/activity roles, sparse storage, and rasters/compilers are distinct.
6. **Defining versus incidental algorithm?** Snapshot evaluation, source assignments, and proposal union are defining. Map/Fold syntax, list bounds, sorting implementation, and drawing are incidental.
7. **Encoding fidelity?** Tagged and factored forms commute. Any tensor encoding must preserve both factors and finite-support/realization evidence.
8. **Reopened stages?** None expected. T09/T10/T12 retain stricter source/result invariants; T13 retains a different support-replacement composition.
9. **Goal 2 dependency change?** G2-T11 consumes G2-T08/T09/T10 and contributes ParallelFactorCompose/ReplaceWithUnion plus multi-source fixtures for later contextual/graph/rewrite stages.
10. **API coherence?** One closed component reducer and one preset replace the need for a state class, family runner, hidden active list, or conflict callback.

## Stage Results

IN PROGRESS pending independent hostile review and final integration gates.

The evidence result is otherwise closed. The 16-query source oracle yields a 130-line union at 108 pre-Index and 22 actual-Index, retains 26 lines including six governed continuations, excludes 88 false positives, reverse-closes all 17 split documents at 123 exact plus seven extraction-variant query records, and leaves zero unresolved source candidate. The 16-asset physical fixed point closes at C/O/R/X = 2/1/10/3 with 32 monolith/split references, 16 unique hashes, and no missing native raster.

T11 is a binary fixed line with a finite active-source set. Every old source reads physical [L,C,R] bits from one snapshot and returns a new source bit plus finite relative activity. UPDATE applies distinct source-bit assignments and replaces activity by exact union of translated proposals. Activity collisions deduplicate; there is no value-write collision or arbitrary policy. A tagged Cell = Plain(Bit) | Active(Bit) representation is losslessly equivalent to the Notes' factored state and lowers after union to D011 atomic complete writes.

The page-76 local profile has result type Bit × P({-1,0,+1}) and a derived 16^8 = 2^32 rule space, but no source-defined number. The corrected BOOK:922 table has 000 -> (1,{-1,+1}), optional inferred planes (63,15,16,245), and an exact t0..t12 replay. The semantic oracle covers 157,184 exhaustive composition/representation cases plus schedule, collision, overlap, disappearance, ordering, empty-outcome, and radius-two compiler adversaries.

The smallest architecture change is a generic ParallelFactorCompose preset with DistinctAssign and ReplaceWithUnion, followed by ordinary atomic commit in the same branch-free runner. D123 remains to be activated after review. Post-extinction continuation, a native finite boundary, a general seed law, a universal offset bound, and a T11 codec remain explicitly source-underdetermined.
