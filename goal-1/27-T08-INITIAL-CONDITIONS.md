# 27-T08-INITIAL-CONDITIONS

Status: **IN PROGRESS — SOURCE/ASSET/ARCHITECTURE AUDIT ACTIVE**

## Current Facts

- Exact catalog row: T08, CSV line 9, `Initial-Condition Classes`; taxonomy section 8 at `ref/notes/CA-Types.md:177-192` is search vocabulary only, not book evidence.
- The working hypothesis is that T08 classifies seed/run inputs to an existing resolved program, not new transition semantics. The same program can be paired with several initial configurations without changing FRONTIER, NEIGHBORHOOD, RULE, UPDATE, or program identity.
- A deterministic seed description, a probability distribution over seeds, one realized initial configuration, a finite computation realization, and a displayed crop are different objects. Randomness used only to sample event-zero state is not hidden per-step executor state.
- For an infinite fixed lattice, a point seed is naturally a total background field plus a finite override. Rendering that field into a centered finite array is a realization/projection choice, not the seed's native support or boundary policy.
- Seed validity is configuration-schema dependent. A gray value must belong to the declared ALPHABET; composite/tagged control configurations must satisfy structural invariants; a temporal recurrence prefix contains Markov state that cannot be replaced by a spatial point marker.
- T01-T07 already require program, seed, realization/boundary, trace, and view identities to remain distinct. T06/T07 property evidence cannot smuggle a preferred seed into program identity.
- Current `src/ca/seeds.py` contains deterministic, selector-backed, stochastic, compound, geometric, and structured factories plus a finite-shape renderer. Its reusable role and its callback/finite-realization/RNG boundaries require fresh inspection; current behavior is not presumed to define T08.
- DOMAIN means the task/program dimensional support/topology. A seed selects or constructs a valid configuration on that DOMAIN; “seed class” is not a new DOMAIN merely because its support pattern has a different shape.
- Goal 1 changes only `goal-1/`; runtime, root documentation, and tests remain Goal 2 work.

## Updated Assumptions

- Preserve one branch-free SimpleProgram runner:

```text
active = FRONTIER.select(state)
reads  = NEIGHBORHOOD.read(state, active)
writes = RULE(active, reads)
next   = UPDATE.apply(state, active, writes)
```

- Treat a seed as an explicit, typed constructor or sampler for one valid event-zero configuration. Do not add seed-aware RULE or rollout branches.
- Require a lossless distinction among native configuration, compact seed descriptor, realized sample, finite materialization, and observation crop.
- Keep open until book evidence closes: the exact named T08 classes; whether randomness is Bernoulli, fixed-density, uniform over a finite support, or underdetermined; which background/value/centering choices are source-mandated; and whether any seed class carries native symmetry or periodicity invariants beyond event zero.

## Big Picture Objective

Determine exactly which initial-condition classes the source uses, reconstruct their typed configuration semantics and probability/provenance where applicable, and hand Goal 2 the smallest generic seed/profile layer that composes with existing SimplePrograms without changing their execution algebra or conflating infinite support with finite rendering.

## Catalog Identity

- Stable ID: T08.
- Exact CSV name: `Initial-Condition Classes`.
- Taxonomy section: 8, vocabulary seed only.
- Working entry kind: cataloged seed/run-profile classes over existing constructions; not a construction or executor.
- Initial vocabulary: initial condition/configuration/state/pattern/arrangement, simple and random initial conditions, single black/gray/white cell, point/finite/block/row/line seed, all-white/all-black background, periodic/repeating/random configurations, starting configuration, and changes/sensitivity in initial conditions.

## Search Log

`BOOK` means the canonical monolith `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Its body and Notes occupy physical lines `1-20825`; the actual Index begins at `20826`. Twelve frozen regex families produce 1,022 unique candidates: 952 pre-Index lines and 70 actual-Index routes. Exact adjudication retains 482 matched pre-Index lines, rejects 470 pre-Index controls, and treats all 70 Index lines as navigation. Five governed continuations at `BOOK:978,1346,2216,12034,13304` produce the authoritative 487-line retained set.

| Frozen set | Count | SHA-256 of sorted physical line numbers |
|---|---:|---|
| Twelve-query union `U` | 1,022 | `d075e4ebfb5972df0d9047f3c6e8d2271bd8b928b440c666906f0c46b282f362` |
| Matched retained | 482 | `9f7276348fc17b183091f36fa21cc561d4e87f2ff827fd64841648d0e843ed92` |
| Governed continuations | 5 | exact set above |
| Authoritative retained `S` | 487 | `42733f504fa41a98a9f01f88ebeb43b7c8d3e24e0e620229fa9cae3ef62d6ace` |
| Excluded/control pre-Index `X` | 470 | `9914e686142328cece65c6336a5e2797ee2dcbb2090de702139cf826e172840b` |
| Actual-Index routes | 70 | `4e2da3563269b9fa8aa5fc698d2873d6d052a2cb89f2a9d3354d14600582fa13` |

Thus the full declared audit is `1,027 = 487 retained + 470 excluded + 70 Index`, with zero unclassified lines. The 70 Index lines supply navigation only. The split corpus reverse-check finds normalized byte-exact mirrors for 442/487 retained monolith lines; the other 45 are pinned line-join/OCR variants. The normalized exact-mirror set digest is `b85d35a696969b27e517923985d35c4dbfe73eb0213bae774e48d8d81b8a0961`. The monolith remains authoritative rather than pretending those variants are independent evidence.

Known extraction defects are retained as evidence controls, not silently repaired: lost figure glyphs at `BOOK:10647,11277,14341,18764`; a truncated initial condition at `5552`; OCR corruption at `18394,18814`; and damaged `CellularAutomaton` syntax near `11077`. None changes the prose-level seed/configuration distinctions. The executable line-set/query/split oracle below freezes the exact protocol.

| Q | Frozen query family | Total / pre-Index / Index |
|---:|---|---:|
| 01 | exact `initial condition(s)` | 621 / 570 / 51 |
| 02 | `initial` plus state/configuration/pattern/sequence/field/string/word/network/value/data/input/etc. | 54 / 51 / 3 |
| 03 | single/one colored cell, square, element, or point | 79 / 79 / 0 |
| 04 | start/begin/evolve from or with single/random/finite/periodic/uniform/blank | 109 / 109 / 0 |
| 05 | random-initial and start-from-random forms | 112 / 81 / 31 |
| 06 | finite/localized near seed/initial/configuration/pattern/block vocabulary | 61 / 48 / 13 |
| 07 | periodic/repetitive/repeating near initial/configuration/background/block vocabulary | 173 / 158 / 15 |
| 08 | all/only/uniformly black/white/gray or uniform/homogeneous state/background | 29 / 29 / 0 |
| 09 | named color/uniform/periodic/random/regular near background | 32 / 31 / 1 |
| 10 | seed word forms | 19 / 10 / 9 |
| 11 | nested/structured near seed/initial/configuration vocabulary | 136 / 125 / 11 |
| 12 | quantified/described `initial condition(s)` | 128 / 125 / 3 |

The exact regex strings, per-query digests, the complete 487-line `S`, governed set, derived `X`/Index sets, source hash, and the exact 45 split variants are versioned in `goal-1/27-T08-source-oracle.py`. Split equality means complete-line Unicode equality after UTF-8 decoding and `splitlines()` removal of line terminators only; no whitespace, case, punctuation, OCR, Markdown, or Unicode normalization is performed. An identical line may occur anywhere among the 17 split files, so this is occurrence coverage rather than a claimed one-to-one position map.

```bash
python3 goal-1/27-T08-source-oracle.py
```

Recorded result:

```text
source OK
Q01 OK (621, 570, 51)
Q02 OK (54, 51, 3)
Q03 OK (79, 79, 0)
Q04 OK (109, 109, 0)
Q05 OK (112, 81, 31)
Q06 OK (61, 48, 13)
Q07 OK (173, 158, 15)
Q08 OK (29, 29, 0)
Q09 OK (32, 31, 1)
Q10 OK (19, 10, 9)
Q11 OK (136, 125, 11)
Q12 OK (128, 125, 3)
union/pre_index_union/index OK 1022/952/70
matched_retained/retained/excluded OK 482/487/470
structural OK
split_exact_mirror OK 17 442 b85d35a696969b27e517923985d35c4dbfe73eb0213bae774e48d8d81b8a0961
```

## Book Excerpts

Short fragments below are provenance anchors; the construction fact, behavior observation, and implementation/view convention remain separate.

| Source | Section/context | Short source fragment | Construction fact |
|---|---|---|---|
| `BOOK:418-432` | first CA example | “cell in the center is black and all other cells are white” | single distinguished label over an explicit uniform background |
| `BOOK:746` | all 256 ECAs | “starting from a single black cell” | one profile can be reused across many unchanged programs |
| `BOOK:790,846` | three-color totalistic gallery | “initial condition used contains a single gray cell” | gray is a typed source value/role, not a palette guess |
| `BOOK:2706-2710` | Starting from Randomness | “usually started with just a single black cell”; “every cell is chosen ... at random” | simple point and per-cell-random classes are distinct; this passage does **not** specify independence or equal probability |
| `BOOK:3060-3098` | rule 30/22/90 comparisons | random versus single/limited-region starts | the same RULE has different runs/behavior; seed is not program identity |
| `BOOK:3126-3140` | Special Initial Conditions | “fixed block ... repeated forever”; “random sequence of ... blocks” | native periodic field and block-process class are distinct |
| `BOOK:3150-3168` | rule-126/rule-90 block emulation | pairs of black or white cells act as cells | a block-coded seed class is a decoder image and emulation relation |
| `BOOK:3204-3210` | rule 184 nested start | “nested initial conditions ... from substitution systems” | generated start requires an explicit derivation to a frozen target configuration |
| `BOOK:3216,4294` | rule-184 random starts | “exactly equal numbers of black and white cells” | finite exact composition is distinct from iid/density-only randomness |
| `BOOK:3388,3406` | rule-110 structures | “block of length 41 inserted between blocks of the background” | periodic background plus finite defect is native seed data |
| `BOOK:5242` | reversible CA | “equal probability on the two successive first steps” | a program may need multiple temporal slices; equality is explicit here but independence is not |
| `BOOK:7052,7058` | statistical models | “all possible sequences ... equal probability”; “fixed independent probability p” | explicit finite equal-sequence and iid-`p` laws are available, but cannot be retrofitted as the unstated law at `2708` |
| `BOOK:8400` | rule 73 | “no run of an even number of black squares” | constrained initial-condition class differs from unrestricted random starts |
| `BOOK:10899,11077-11150` | `CellularAutomaton` implementation | explicit cyclic list; finite values on constant/repeating background; offset blocks | configuration presentation, finite topology, background, offsets, and multidimensional forms are separately expressible |
| `BOOK:11124-11150` | output specifications | affected region, `Automatic`, explicit offsets | work/output crop is not native initial support or boundary |
| `BOOK:13265` | information content | single black on white versus “infinite sequence of randomly chosen cells” | compact finite and infinite random configurations have different information/scope |
| `BOOK:14031` | differential problems | initial-value versus boundary-value specifications | T45 side data is not automatically a T08 event-zero configuration |
| `BOOK:14213` | randomness each step | random changes during evolution | transition-time draws are not initial-condition sampling |
| `BOOK:14275` | random starts in other systems | random tape colors with definite active cell; finite word/tag limits; random graphs; constraints have no starts | seed/profile schema is support-family-specific and does not force nonstep categories into rollout |
| `BOOK:18674` | rule-110 cyclic-tag emulation | infinite left repetition, finite middle, infinite right repetition | ultimately periodic piecewise field is target-run data in an explicit emulation relation |
| `BOOK:19072` | continuum/cardinality | finite-on-white arrangements versus infinite configurations | finite descriptors/materializations cannot stand in for arbitrary infinite configurations |
| `BOOK:20128,20577` | proof/search boundaries | run-specific occurrence; rule cases unvisited by an initial condition | a seed/run cannot certify a rule property or erase unsampled table rows |

No retained source gives T08 a seed-dependent native transition rule, new firing locus, new write, or new update algebra. `BOOK:12352` and `15766` discuss derived emulation/mapping facts in which changing source input can change a constructed target artifact; they do not make the target rule inspect a seed family during execution.

## Construction Model

### Architecture classification

Let a resolved program `P` expose a configuration schema

```text
C_P = (DomainSchema_P, AlphabetSchema_P, component schema, structural invariants).
```

Each configuration carries one support/topology instance admitted by `DomainSchema_P` plus its labels/components. A fixed lattice has one fixed support form; a word, tree, graph, or finite occurrence bag may have a different support/topology instance at each event. Write `Conf(C_P)` for all complete configurations valid under that schema. T08 does not change `P`; it describes elements, subsets, and probability laws over `Conf(C_P)` and the records by which one such element is supplied at event zero.

| T08-related object | Audit class | Smallest reusable base | Consequence |
|---|---:|---|---|
| One exact initial configuration | 1 — direct reuse | ordinary invariant-valid `Configuration` | accepted unchanged by the shared runner |
| Named deterministic profile | 2 — preset/parameterization | closed `ConfigurationConstructor` targeted at `C_P` | resolves before rollout to one ordinary configuration |
| Initial-condition class | 2 — restriction/set | declarative subset or image of a closed constructor over `Conf(C_P)` | membership capability may be decidable, certified, unknown, or unsupported; never execution |
| Random initial-condition class | 2 — probability-bearing profile | `InitialDistribution` over an explicit configuration class | sampling occurs once before event zero |
| Background-plus-exceptions, periodic, block-coded, or temporal-history form | 3 when lossless — tagged/product representation | ordinary configuration plus validated expansion/projection | no special seed evaluator inside the runner |
| Finite materialization, quotient, crop, raster, dataset split, or behavior label | 2 — realization/relation/observer | existing run and observer records | excluded from seed and program identity |
| New FRONTIER, NEIGHBORHOOD, RULE result, UPDATE, executor, or successor | 4 only with a counterexample | none found | no T08 execution semantic is authorized |

The word *seed* is overloaded in the current documentation and runtime. Goal 2 should keep the following layers distinct even if a convenience facade retains that word:

```text
ConfigurationSchema
    defines admissible support/topology instances, labels, and Conf(C_P)

InitialConditionClass
    denotes K subseteq Conf(C_P)

ConfigurationPresentation
    closed data denoting one exact X_0

ConfigurationConstructor
    closed parameterized map that constructs one exact X_0

InitialDistribution
    optional probability law mu over K

ConstructionRecord
    constructor/profile/arguments -> exact configuration reference

SamplingRealization / SampleRecord
    law plus sampler/key/scope provenance -> exact configuration reference

ValidatedInitialConfiguration
    exact configuration reference plus schema-validation evidence

ComputationRealization / LoweringRecord
    optional native-to-work-state relation for a declared horizon

RunRequest / NativeTrace / ExperimentRecipe / Observer
    separate semantic execution, result, orchestration, and view records
```

A source phrase can identify only a class without determining a probability law. “Random arrangements with exactly equal numbers” denotes a different class/law from independent fair choices; “random” without probabilities, conditioning, finite scope, or a generative rule is underdetermined and cannot silently become Bernoulli `p=1/2`.

### Exact configurations, constructors, and specialized presentations

The public semantic object is a complete configuration, not a mask. It contains an admitted support/topology instance and complete typed labels/components. Literal words, trees, graphs, register banks, geometric bags, scalar states, and fixed fields are all ordinary configurations; no point-evaluation or rectangular materialization API is imposed on all of them.

Fixed-lattice profiles evidenced by T08 can use a capability-gated closed presentation algebra without forcing an infinite field into a tensor:

```text
ExplicitFiniteLattice(domain_instance_ref, assignments)
ConstantField(value)
PeriodicField(period_lattice, phase, finite_tile)
Override(base_presentation, finite_typed_assignments)
PiecewiseField(closed_disjoint_regions, presentations)
```

`Override(ConstantField(white), {origin: black})` is the native point profile on an infinite fixed lattice. `PeriodicField` represents a fixed block repeated forever. `Override(PeriodicField(...), finite assignments)` covers a periodic background with a finite defect. `PiecewiseField` covers evidenced ultimately periodic left and right tails around a finite middle; its region language must be closed, serialized, disjoint, and total. These are lattice codecs/presets, not the universal `Configuration` interface.

A nested initial condition produced by a substitution system is an explicit derivation relation, not a seed-presentation escape hatch:

```text
ConfigurationDerivation(
    exact_source_configuration_ref,
    source_program_and_finite_trace_or_certified_limit_ref,
    closed_typed_transform,
    exact_target_configuration_ref,
    evidence)
```

The target run references the already frozen exact target configuration. It never lazily executes another program or arbitrary constructor while resolving or stepping the target.

Every presentation has:

- one declared target configuration schema and an admitted support/topology instance;
- complete typed labels/components for that instance;
- a canonical structural identity and expansion semantics;
- validation that all values are ALPHABET members and all global invariants hold; and
- an inverse or canonical re-encoding on the representation's declared image when it is claimed lossless.

A constructor is not required to be invertible: two named presets may intentionally construct the same `X_0`. An inverse and one-step commuting law apply when an object claims to be a lossless representation of a native configuration/step. A finite execution lowering additionally owes the horizon-indexed relation below. Neither obligation applies merely because something is a convenient constructor.

Overlapping overrides with unequal values, an uncovered piecewise region, a nonperiodic tile declaration, a dangling derivation, and an assignment outside the DOMAIN are invalid. Last-write-wins order is not invented. A palette rank cannot supply “white”, “gray”, or “black”; each source role resolves to an explicit typed alphabet member.

The finite list used by a practical implementation has no intrinsic boundary meaning. An explicit list on a declared finite cyclic DOMAIN is a complete finite configuration. A window cut from an infinite point or periodic field is instead a lowering/materialization. The source's finite cyclic program and its infinite periodically repeated configuration can be related by a quotient/covering map, but they are not the same configuration object merely because their arrays coincide.

### Configuration classes and stochastic laws

An `InitialConditionClass` is schema-scoped. It denotes a subset through declarative structural data, a constructor image, or a referenced relation. Closed syntax does not imply decidability: exact asymptotic density on an infinite lattice, membership in a generated infinite image, normalization of a general generator, or a global invariant may be undecidable or not finitely checkable. A membership request therefore returns invalid, `UnsupportedMembership`, `Unknown`, certified `DoesNotHold`, or certified `Holds`; only supported finite/structural validators may decide it.

The frozen source evidence distinguishes at least these families:

- constant/uniform configurations;
- finite perturbations of a declared background, including one distinguished cell;
- finite explicit configurations on a declared finite topology;
- periodic configurations and periodic backgrounds with finite or ultimately periodic defects;
- block-coded or macrocell configurations, including images of another alphabet under a fixed block decoder;
- substitution-derived nested configurations represented by frozen targets plus explicit derivation relations;
- unrestricted assignments over a stated scope;
- finite-scope configurations with exact composition constraints, distinct from a random law's density parameter; and
- configurations satisfying a supported closed local-language condition, such as an allowed finite macroblock decoder.

“Simple initial condition” in the prose is not by itself a canonical decidable class. Goal 2 exposes only evidenced concrete profiles or explicitly declared structural classes; it does not turn an informal behavioral adjective into a Boolean field.

An `InitialDistribution` separately declares:

```text
support_class_ref
native sampling scope
finite categorical probabilities or a closed generative law
conditioning/composition constraints
normalization and parameter domain
supported probability/query/sampling capabilities
law semantic version
```

Important nonidentities include:

```text
iid Bernoulli(p)
!= draw p once, then conditionally iid Bernoulli(p)
!= uniform over strings with exactly m black cells
!= independent draws of allowed fixed-width macroblocks
!= a finite-length law over strings accepted by a constraint language.
```

There is no generic “uniform over all strings accepted by a constraint language” without a finite length/scope or a separately specified probability measure on infinite sequences. Normalization and zero-mass conditioning must be proved for the declared scope; closed syntax alone supplies no sampler.

For a finite fixed lattice, sampling may use a canonical coordinate order. A word uses declared sequence order; a graph law must be invariant to vertex renaming or declare a canonicalization with proof; other support instances use law-specific typed sampling requests. Each `SamplingRealization` records sampler algorithm/version, scope/enumeration or structural map, key or input entropy, and draw provenance. The mathematical law identity does not include a particular RNG implementation unless the source construction itself specifies that algorithm. The exact configuration digest likewise excludes provenance: the same `X_0` sampled by two laws has one configuration identity and two `SampleRecord` identities.

Structured laws compose closed component laws, deterministic overlays, and pushforwards while preserving schema invariants. For example, a tape profile may sample tape symbols, choose one explicit head position/state, and then apply the lossless `Plain(symbol) | Head(q,symbol)` constructor. Treating whole composite cells as iid would almost surely violate the exactly-one-head invariant and is not an equivalent law.

An infinite product law is a probability measure characterized by consistent finite-cylinder probabilities, not an array that can be eagerly drawn. Cylinder probability is an optional product-measure capability, not a universal distribution method. A practical finite-window sampler is an explicit realization of a requested cylinder. A coordinate-keyed pseudorandom total field can provide replayable order-independent queries, but with a finite key it is an algorithmic realization related to—not literally an exact draw from—the mathematical infinite independent product measure. Goal 2 must preserve that qualification rather than hide a mutable RNG cursor in execution state.

### Event-zero state and temporal history

The complete Markov state required by `P` must be present at event zero. For a second-order scalar recurrence,

```text
state_t = (x[t-1], x[t])
step(state_t) = (x[t], f(x[t], x[t-1]))
observe(state_t) = x[t].
```

For a three-lag lookup the same construction uses three named lag factors. A ten-lag count rule uses one length-ten shift-register state at every event. A product label at the unique `t+0D` locus, named configuration components, or another transparent tuple codec are lossless representation choices; none is semantically mandatory. Serializing ten seed scalars and then silently changing to a packed integer is a representation boundary only if both encode the same complete state losslessly and the trace records the mapping; it cannot mean that one episode changes configuration schema halfway through.

If the source supplies a temporal prefix before recurrence begins, the prefix is initialization data for the complete Markov state or an explicitly aligned prelude/trace projection. Hidden earlier values that affect the next state cannot be discarded from raw state while only the current scalar is called the configuration. This repair uses ordinary transparent configuration structure and `t+0D` state/update; it adds no seed-aware executor and mandates no particular storage decomposition.

### Realization, boundary, execution, and identity

Construction, sampling, validation, and execution lowering are separate operations:

```text
construct(profile, closed_args) -> ConstructionRecord(X_0_ref)
sample(law, sampling_realization) -> SampleRecord(X_0_ref)
validate(X_0, C_P) -> ValidationEvidence
lower(X_0, computation_realization, horizon) -> LoweringRecord(work_state_ref)
```

A deterministic profile has a construction record, not a fake sample. A sampled configuration has the same denotational configuration identity it would have if constructed literally; its law and RNG belong to `SampleRecord` provenance.

For an infinite fixed-lattice profile, lowering into a finite computational work region is separate from the native configuration. A causal lowering records the support map, requested observation/horizon, and a proof that its work region contains the full dependency cone. It reads native values in that cone and invents no exterior boundary. A `BOUNDARY` belongs to a genuinely finite semantic topology or to an explicitly declared approximation; it must not silently stand in for an unbounded native field. Halo (semantic dependency sufficiency), storage padding, numeric/storage codec, and display crop are separate records.

For a requested horizon `h`, a lowering that claims exactness must satisfy the horizon-indexed commuting obligation

```text
observe(step_native^t(X_0))
    = observe(decode(step_lowered^t(lower(X_0,h))))
for every 0 <= t <= h.
```

One-step agreement is insufficient: a radius-one crop with one halo cell can pass at `t=1` and fail at `t=2`. Approximate/truncated lowerings instead carry an explicit error/scope claim. The event-zero background is not a boundary value that persists through time: a rule may change every background cell after the first step.

After native construction or a validated exact lowering, the runner remains:

```text
active = FRONTIER.select(X_t)
reads  = NEIGHBORHOOD.read(X_t, active)
writes = RULE(active, reads)
X_t1   = UPDATE.apply(X_t, active, writes)
```

No line below event zero inspects a T08 family tag. `P`, its FRONTIER, NEIGHBORHOOD, RULE, UPDATE, successor cardinality, and object identity are unchanged when `X_0` changes.

Keep the identities separate:

```text
Program
ConfigurationSchema
InitialConditionClass
ConfigurationPresentation
ConfigurationConstructor / ConstructionRecord
InitialDistribution
SamplingRealization / SampleRecord
Configuration / ValidationEvidence
ComputationRealization / LoweringRecord / BoundaryOrApproximation
RunRequest / NativeTrace
ExperimentRecipe / Observer / View
```

Translation, reflection, color permutation/complement, block encoding, finite quotienting, and cropping are explicit transforms or relations. Two presentations or constructors may denote the same configuration digest while retaining distinct representation/construction provenance. Two laws can produce the same `X_0` without becoming the same law. A semantic run request references one exact program and one validated native initial configuration (or an explicit exact/approximate lowering); an experiment recipe and observer reference the run without becoming its execution semantics.

### Cross-category scope boundary

T08's catalog row concerns event-zero configurations for stepwise programs. The English phrase *initial condition* also appears in nonstep categories and must not force them into this schema:

- For T31/T32/T33 declarative model sets, a seed or fixed template condition restricts admissible models; it does not create a distinguished successor or event zero.
- For T41 an argument/value condition belongs to a function definition or query; it is not a seed unless an explicit T43 iteration is derived.
- For T45 an initial trace is side data in a differential problem. Only a separately justified IVP-to-flow relation can produce a SimpleProgram state and event-zero configuration.
- A rule-110 initial field that encodes a cyclic tag system is target-run data plus an explicit emulation relation. Its encoded program payload does not become rule-110 program identity.
- A multiway rewrite still has an ordinary initial configuration; branching begins in its successor result, not in a “multiway seed” executor.

Thus equally named source roles reuse seed/profile infrastructure only when their denotation is actually an element or law over `Conf(C_P)`. Otherwise they remain typed constraint, problem-side-data, query, or relation records.

### Dependency-free semantic oracle

```bash
python3 - <<'PY'
from fractions import Fraction
from itertools import permutations, product
from math import comb

def evaluate(presentation, x):
    kind=presentation[0]
    if kind=='constant': return presentation[1]
    if kind=='periodic':
        tile,phase=presentation[1:]
        return tile[(x-phase)%len(tile)]
    if kind=='override':
        base,changes=presentation[1:]
        return changes[x] if x in changes else evaluate(base,x)
    raise ValueError(kind)

point=('override',('constant',0),{0:1})
periodic=('periodic',(1,0,0),0)
defect=('override',periodic,{0:0,4:1})
assert [evaluate(point,x) for x in range(-3,4)]==[0,0,0,1,0,0,0]
assert [evaluate(periodic,x) for x in range(-3,4)]==[1,0,0,1,0,0,1]
assert evaluate(defect,0)==0 and evaluate(defect,4)==1

# An event-zero fill is not a persistent boundary. ECA rule 1 maps 000 to 1.
def eca_step(rule,state):
    n=len(state)
    return tuple((rule >> (4*state[(i-1)%n]+2*state[i]+state[(i+1)%n]))&1
                 for i in range(n))
assert eca_step(1,(0,)*7)==(1,)*7

# Product Bernoulli, a once-per-episode random p mixture, and fixed composition differ.
fair11=Fraction(1,2)**2
mixture11=Fraction(1,3)                 # integral_0^1 p^2 dp
fixed_two11=Fraction(0,1)               # exactly one 1 among two sites
assert fair11==Fraction(1,4) and mixture11!=fair11 and fixed_two11!=fair11
def bernoulli_mass(bits,p):
    return p**sum(bits)*(1-p)**(len(bits)-sum(bits))
assert sum(bernoulli_mass(v,Fraction(1,3)) for v in product((0,1),repeat=4))==1
assert comb(6,3)==20                    # fixed-composition class cardinality

# Block-coded configurations are an image of a closed decoder, not scalar iid cells.
decode={0:(0,0),1:(1,1)}
macro=(1,0,1)
decoded=tuple(y for x in macro for y in decode[x])
assert decoded==(1,1,0,0,1,1)
assert all(decoded[2*i]==decoded[2*i+1] for i in range(3))

# Temporal history is complete Markov state; the visible scalar is a projection.
def ar2_step(state):
    prev,cur=state
    return (cur,(cur+prev)%5)
s=(2,3)
assert ar2_step(s)==(3,0)
assert ar2_step(ar2_step(s))==(0,3)
assert ar2_step((1,3))!=(ar2_step(s))   # same visible current, different full state

# A periodic infinite field and a finite cyclic quotient can agree under a relation
# without sharing native DOMAIN/configuration identity.
tile=(1,0,1)
infinite_window=tuple(tile[x%3] for x in range(12))
finite_cyclic=tuple(tile[x%3] for x in range(12))
assert infinite_window==finite_cyclic
assert ('Z-periodic',tile)!=('cycle-3',tile)

# One DomainSchema can admit variable-support words; fields are not universal.
def valid_word(x): return x[0]=='word' and all(v in (0,1) for v in x[1])
assert valid_word(('word',(1,))) and valid_word(('word',(1,0,1,1)))

# Graph configuration identity is invariant to incidental vertex names/order.
def canon_graph(edges):
    vertices=sorted({v for e in edges for v in e})
    rows=[]
    for perm in permutations(range(len(vertices))):
        ren=dict(zip(vertices,perm))
        rows.append(tuple(sorted((ren[a],ren[b]) for a,b in edges)))
    return min(rows)
assert canon_graph(((0,1),(1,2)))==canon_graph(((2,0),(0,1)))

# Same denotational configuration, different construction/sample provenance.
x0=('word',(1,0,1))
assert x0==tuple(['word',(1,0,1)])
assert ('literal-profile','x0')!=('sample-law-A','key-7','x0')

# Schema membership and structured global invariants are initialization obligations.
def valid_head_config(xs):
    return all(symbol in (0,1) and head in (None,'q0','q1') for symbol,head in xs) \
           and sum(head is not None for _,head in xs)==1
symbols=(0,1,0)
structured=tuple((s,'q0' if i==1 else None) for i,s in enumerate(symbols))
assert structured[1]==(1,'q0') and valid_head_config(structured)
assert not valid_head_config(((0,'q0'),(1,'q1')))
assert not valid_head_config(((2,None),(1,'q0')))

# One-cell halo is exact for t=1 at x=0 but not automatically for t=2.
def rule90(field,lo,hi,exterior=0):
    get=lambda x: field.get(x,exterior)
    return {x:get(x-1)^get(x+1) for x in range(lo,hi+1)}
native={x:0 for x in range(-4,5)}; native[2]=1
work={x:native[x] for x in range(-1,2)}
n1=rule90(native,-4,4); w1=rule90(work,-1,1)
assert n1[0]==w1[0]==0
n2=rule90(n1,-4,4); w2=rule90(w1,-1,1)
assert n2[0]==1 and w2[0]==0

print('T08 semantic oracle: PASS fields, laws, variable domains, history, invariants, halo')
PY
```

## Current API Fit

`simple_programs.md:235-290` already places `SEED` before rollout as support `S_0`, assignment law `mu_seed`, and initial fill `a_init`, while `BOUNDARY` starts separately at `simple_programs.md:292`. That separation is directionally correct and should survive. At the mathematical level the formula can denote a periodic or constrained field by taking `S_0=D` and choosing an appropriate law. Goal 2 still needs a closed typed schema for those laws and compact presentations; the present support/fill prose and runtime cannot serialize or validate periodic tails, piecewise/derived configurations, exact-composition classes, configuration-wide invariants, or product/tagged values losslessly.

The repaired generic API should expose:

```text
ConfigurationSchema.validate(configuration) -> ValidationResult/Evidence
ConfigurationConstructor.construct(closed_args) -> ConstructionRecord
InitialConditionClass.membership(configuration, capability) -> MembershipResult
InitialDistribution.sample(typed_request, SamplingRealization) -> SampleRecord
ComputationLowering.lower(configuration, horizon, observation) -> LoweringRecord
```

Optional capabilities are schema-specific. A fixed field presentation may support `evaluate(point)` and `materialize(window)`; a word supports indexed sequence access; a graph exposes structural loci and alpha-invariant identity. An abstract product measure may support cylinder probabilities but reject total materialization; an undecidable class may return `Unknown` or unsupported membership; a finite explicit configuration may support exhaustive hashing. No universal point/window/canonical-coordinate operation and no callback fallback is inferred from the generic interface.

The smallest change to the conceptual SimpleProgram/run model is to generalize the scalar-fill seed formula into schema-targeted event-zero construction/law records outside program identity. Program construction must not require a preferred seed. A convenience experiment preset may pair a program and an initial profile, but resolving it returns the same program object plus separate construction/sample, validation, realization, and run references.

## Current Runtime Fit

Current runtime reuse is real but narrower than the catalog abstraction:

| Current surface | Reuse/classification | Required Goal 2 correction |
|---|---|---|
| `Seed` fields (`src/ca/seeds.py:39-55`) | partial finite scalar presentation | replace `family: str`, `distribution: Any`, and untyped params with closed tagged schemas; bind to configuration schema and typed values |
| Selector-backed factories | reusable finite support descriptions | preserve loci selection, but do not equate a selected finite mask with native infinite support or a full configuration |
| `render(seed, shape, rng)` (`seeds.py:879-939`) | finite materializer | split validation, law sampling, exact configuration construction, and finite materialization; remove family dispatch from semantic resolution |
| `rng=None` (`seeds.py:58-63`) | convenience only | reject or explicitly record nondeterministic entropy for semantic runs; retain algorithm/version/key/sample provenance |
| Bernoulli renderer (`seeds.py:930-935`) | a different hierarchical law than its name suggests | it draws one global `p` uniformly in `[p_low,p_high]`, then cells conditionally; add an actual fixed-`p` product law, validate bounds, and name the mixture honestly |
| `fractal`/`spiral` predicate params (`seeds.py:733-780`) | opaque callback shim | replace with a supported closed support/expression or a frozen exact configuration plus relation; never execute arbitrary predicates/source programs as seed semantics |
| `compound`/structured factories | useful presentation vocabulary | preserve component values, laws, conflicts, DomainSchema/support instance, invariant proof, and provenance instead of reducing to one scalar mask/union |
| `DatasetSpec`/`EpisodePlan` (`src/ca/datasets.py:57-128`) | downstream experiment recipes | keep shape, split, held-out stream, transforms, boundary, batching, and RNG planning outside program and mathematical law identity |
| Raw episode records (`src/ca/specs.py:58-81`) | trace carrier | add exact initial-configuration/profile/sample references so temporal history and realization provenance are recoverable |
| SplitMix helpers (`src/ca/rng.py:20-70`) | reusable deterministic key derivation | bind algorithm/version/counter and draw mapping to sample provenance; a stable integer key alone does not define the mathematical law |
| Viewer/export (`src/ca/viz/export.py:177-195`) | explicitly lossy dense observer | retain as a declared view, but never use rejection of object/float/symbolic values to narrow semantic configuration types |

All current rendered spatial values are coerced into `np.int64`; one `selected_value` and `fill_value` cannot carry a composite Turing cell, heterogeneous component assignment, exact real, symbolic value, or schema invariant. `support=None` and a finite `shape` silently turn “whole native DOMAIN” into “this tensor.” A point selector with a nonzero time coordinate is also not representable faithfully once rendering drops the time axis. These are representation gaps, not reasons for a seed executor.

Temporal rollout reveals a more serious state boundary. `_rollout_ar2` treats `(x[-1],x[0])` as hidden previous/current values but serializes only `x[0],x[1],...` (`src/ca/rollout.py:334-359`). `_rollout_temporal_lookup` does the same with three lag values (`:362-413`). `_rollout_lagcounts` first serializes ten individual seed values, then evolves one packed ten-bit state (`:417-476`). The rule-generated successor depends on information absent from the serialized scalar “state,” and the apparent configuration schema changes during one episode. Goal 2 must make the complete named-lag/shift-register state visible in the ordinary `t+0D` configuration at every event and move the scalar series into an observer projection; product labels, components, or tuple codecs remain representation choices.

Current tests establish factory shapes, deterministic placement, some RNG reproducibility, and dataset behavior. They do not establish schema membership, typed/composite values, exact law identity, iid versus mixture/fixed composition, native infinite presentations, coordinate-order independence, temporal-state observability, lossless serialization, boundary separation, or unchanged program identity. Existing outputs are migration evidence, not authority where they conflict with the source-faithful model.

Additional current defects must be made explicit in the migration:

- `compound` unions component supports but drops their distinct values and distributions, then paints the union with one outer scalar (`src/ca/seeds.py:514-602`). It is not a lossless product/composition constructor.
- Selector callables are admitted in `src/ca/loci.py:41-50,283-308`; `fractal` and `spiral` expose arbitrary predicate callbacks (`src/ca/seeds.py:733-780`). These fail the closed-data boundary even when their finite masks happen to be reproducible.
- An out-of-window point silently renders as all fill, and a `point(t!=0)` loses its requested time because the spatial renderer/native-index path has no time axis (`src/ca/seeds.py:260-301,925-926`; `src/ca/loci.py:617-635`). Invalid scope cannot be silently reinterpreted as an empty event-zero selection.
- `dedupe` renders candidates using implicit RNG state (`src/ca/seeds.py:942-965`), so stochastic profile “equality” can itself be nondeterministic. Profile, law, realized configuration, denotational equivalence, and transform-orbit dedupe need separate operations.
- `EpisodePlan.id` omits later program/profile/shape/steps/boundary decisions (`src/ca/datasets.py:205-220`). “Held-out seed” currently means a different stream, not proved configuration disjointness (`:193-202,497-505`). Dataset transforms can be recorded as metadata without being applied (`:203,224-244,603-605`). IDs and claims must state exactly which relation they certify.
- Batch rollout's one dense homogeneous shape (`src/ca/rollout.py:88-142,601-640`) is an adapter contract. Ragged words, trees, graphs, composite values, or different native supports require explicit offsets/containers or separate batches, never semantic padding.

## Principles Audit

- Principles 1, 9, and 10 suggest a discoverable catalog preset/profile over the independent seed axis, not a family executor.
- Principles 5, 7, and 8 require every realized seed to be a complete valid configuration on one admitted native support/topology instance; variable-support words/trees/graphs remain first-class, while compact lattice forms need explicit lossless mappings.
- Principle 11 keeps a one-time stochastic seed law distinct from RNG implementation and from stochastic transition rules.
- Principle 12 keeps held-out-seed streams, batching, storage padding, centering, orchestration, and rasterization outside program semantics; a semantic halo/causal lowering separately requires a horizon proof.
- Principles 13-16 require adversaries for variable support, graph renaming, background evolution, translation/centering, finite topology versus approximation, ALPHABET mismatch, structured composite invariants, law capability/identity, replay, temporal resume, and opaque callback/interpreter rejection.

## Detailed Implementation Plan

1. Close a reproducible source universe across direct terminology, concrete seed descriptions, captions, Notes, Index routes, aliases, and cross-references; disposition every candidate.
2. Close the governed visual-asset universe with exact monolith/split references, dimensions, hashes, semantic classifications, and run/caption stop rules.
3. Reconstruct deterministic, stochastic, finite-exception, periodic, and structured seed profiles from evidence; separate seed, realized configuration, realization, boundary, trace, and view.
4. Audit `simple_programs.md`, `src/ca`, tests, datasets, and completed stages; identify exact reuse and mismatches without preserving incidental Phase 1 behavior.
5. Specify Goal 2 schemas, identity/provenance, validation, serialization, transformations, acceptance tests, and no-cheating checks.
6. Run all embedded oracles, independent hostile review, repository tests, Markdown/coverage/decision/diff gates, integrate the ledgers, and advance only after clean closure.

## Goal 2 Implementation Stage

**G2-T08 — typed initial-condition classes, presentations, laws, and realization.** Implement after G2-T01 establishes ordinary configuration schemas and alongside generic run/identity infrastructure. It changes event-zero construction and migration, not the SimpleProgram executor.

| Goal 2 surface | Required work |
|---|---|
| configuration schema | Expose a native DomainSchema, admitted support/topology instances, typed ALPHABET/components, complete-configuration validation, and structural invariants. Validate initial configurations through the same schema used for later states, including variable-support words/trees/graphs. |
| exact configurations and specialized presentations | Accept ordinary structural configurations directly. For fixed lattices, add finite explicit, constant, periodic, finite override, and closed piecewise codecs with capability-specific evaluation/materialization, validation, identity, and round trip on claimed images. Do not impose field APIs on other DOMAIN schemas. |
| configuration-class layer | Add schema-scoped declarative descriptors for evidenced constant, finite perturbation, periodic, block image, finite exact composition, and supported local-language images. Membership returns invalid/unsupported/unknown/certified results; closed syntax does not promise decidability. |
| stochastic-law layer | Add fixed categorical/product laws, explicit parameter-mixture laws, fixed-composition laws, macroblock laws, and supported structured composition/overlay/pushforward laws. Validate scope, probabilities, conditioning, normalization, invariant preservation, and advertised capabilities. |
| sampling realization | Record law, sampler algorithm/version, law-specific scope/enumeration or structural map, key or entropy provenance, and exact configuration reference. Keep configuration digest independent of sample provenance; distinguish infinite measures, finite-cylinder samples, and algorithmic pseudorandom fields. |
| profile/catalog resolver | Resolve source-named convenience profiles to ordinary constructors/classes/laws bound to explicit typed alphabet roles and a configuration schema. Return the exact unchanged program separately. Reject underdetermined “random” profiles instead of inventing parameters. |
| finite realization and boundary | Lower requested work regions with a dependency-cone proof for the full horizon; keep native support, origin/centering, topology/quotient, semantic halo, storage padding, codec, crop, genuine finite boundary, and approximate exterior separate. Do not treat initial fill as persistent exterior. |
| temporal migration | Represent AR2, lag lookup, and lag-count histories as complete named-factor `t+0D` configurations at every event; product labels/components/tuple codecs are representation options. Make scalar series a projection observer and preserve resume/alignment provenance. |
| transforms/relations | Add typed translation, reflection, value permutation, block decode, frozen derived-configuration, quotient/covering, and crop relations. A derivation consumes exact immutable references; it never runs a hidden source interpreter during target resolution. |
| serialization/identity | Version and round-trip schema, class, presentation, constructor/construction record, law, sampling realization/sample record, denotational configuration, validation, lowering, run request/trace, experiment, boundary, and observer independently. Reject stale/tampered digests and opaque payloads. |
| rollout/executor | Accept one validated `X_0` and use the existing branch-free runner. Remove or bypass seed-family and temporal-family dispatch as semantic paths; no T08 flag may reach RULE or UPDATE. |
| tests/source fixtures | Pin the final source/asset evidence and add the acceptance groups below, including variable support, alpha-renaming, probability capability, structured invariants, replay, temporal resume, horizon commutation, identity, and static no-cheating adversaries. |

### Twenty acceptance groups

1. **Program/profile/configuration identity:** pair one exact program object with point, uniform, periodic, and random profiles; assert unchanged program digest/object and identical runner axes. Two constructors and two laws that produce the same `X_0` share its configuration digest but retain distinct construction/sample provenance.
2. **DomainSchema, variable support, and alphabet validation:** accept changing-length words and alpha-renamed graphs as admitted support/topology instances, plus typed ALPHABET/components. Reject palette-derived gray, rank/value collisions, wrong value types, missing components, invalid topology, and support outside the schema; never demand a rectangular point/window API.
3. **Global invariants and structured randomness:** sample tape symbols, overlay one explicit head while retaining its symbol, and validate exactly one tag. Reject zero/two heads and show that iid whole composite cells are not equivalent. Apply the generic invariant mechanism rather than adding a Turing seed class.
4. **Constant and point profiles:** resolve source white-background/single-black and white-background/single-gray forms using explicit member references and origin; evaluate them on native support without requiring a finite tensor.
5. **Finite configuration versus lowering:** distinguish an explicit list on a finite segment, the same list on a finite cycle, and a crop/work state lowered from an infinite field. Array equality cannot merge DOMAIN/topology identities, infer a boundary, or prove horizon sufficiency.
6. **Periodic configurations:** validate nonempty tile, period lattice, phase, and typed values; test negative coordinates and translation. Relate—not identify—an infinite periodic field and its compatible finite cyclic quotient.
7. **Overrides and piecewise tails:** round-trip constant/periodic bases plus finite defects and ultimately periodic left/middle/right forms. Reject conflicting overrides, overlap, gaps, invalid region syntax, and phase ambiguity.
8. **Block and frozen derived images:** encode/decode paired-cell and macroblock classes losslessly; verify a substitution-derived nested target through immutable source/trace-or-certificate/transform/target references. Reject partial decoders, dangling provenance, lazy source execution, and hidden callbacks.
9. **Probability and membership capabilities:** enumerate small finite categorical/Bernoulli supports and assert total mass one, exact event probabilities, validated parameters, and law-specific enumeration. Reject zero-mass conditioning and unnormalized laws; return typed unknown/unsupported for nondecidable global membership or unavailable sampling/probability operations.
10. **Law nonidentity:** distinguish fixed-`p` iid, one-global-`p` mixtures, exact-composition sampling, macroblock sampling, and finite-scope constraint-language sampling with explicit two- and four-site probability witnesses.
11. **Underspecified randomness:** a source/profile that omits probabilities, finite scope, conditioning, or generator yields a typed underdetermined/unsupported result; it never defaults silently to fair Bernoulli or the current `[0,1]` mixture.
12. **Infinite-law capability:** test finite-cylinder consistency for an abstract product measure; reject eager total materialization. Label a finite-key coordinate-hash field as an algorithmic realization, not proof of exact infinite independence.
13. **Replay, structural order, and provenance:** identical sampler version/key/request reproduces the exact configuration digest across scalar/batch execution and row reorder. Coordinate query order cannot alter a coordinate-keyed field; graph vertex serialization cannot alter an alpha-invariant graph law. Missing entropy provenance, changed sampler version, or tampered sample reference fails validation.
14. **Temporal Markov state:** AR2 pairs, three-lag tuples, and ten-bit shift registers remain complete states for every event. Two histories with the same visible scalar produce different successors where expected; pack/unpack and scalar observer projections round-trip without changing state schema mid-run.
15. **Horizon lowering, fill, and boundary:** rule 1 turns an event-zero all-zero field to ones; a zero fill is not permanent exterior. Prove causal-halo commutation for every `t<=h`, including a radius-one one-halo counterexample that fails at `t=2`; distinguish native infinite execution, genuinely finite topology, and explicit boundary approximation.
16. **Centering and translation:** pin the source's finite even/odd centering convention where requested, while proving that native point origin, finite placement, translated profile, materialization window, and display crop have separate identities.
17. **Transforms and relations:** translation/reflection/value permutation preserve class or law only when proved; block decoding, frozen derivation, quotienting, and lowering emit relation records. A symmetric distribution does not imply each sample is symmetric, and graph relabeling is not a new configuration.
18. **Serialization and trust:** canonical round trips preserve typed values, DomainSchema/support instance, class, presentation, constructor/construction, law/sample, denotational configuration, validation, lowering, and provenance separately. Reject stale versions, duplicate/conflicting assignments, NaN/invalid probabilities, and trusted “valid” flags.
19. **Dataset/observer separation:** held-out streams, batch shapes, token budgets, padding, augmentations, palettes, rasters, behavior labels, density estimates, and crops cannot alter program, class, or mathematical-law identity.
20. **No-cheating/static and cross-category scope:** no T08 branch below event-zero resolution, hidden temporal pre-state, `Any`/string family dispatch, opaque predicate/interpreter, implicit RNG, scalar-only coercion, implicit fixed lattice, or callback fallback. PDE side data, constraint seeds, and function arguments remain their native nonstep roles unless an explicit relation derives a SimpleProgram.

## No-Cheating Checks

- No T08/seed-family rollout branch, seed-aware RULE, implicit boundary, forced finite tensor DOMAIN, or preferred seed stored in program identity.
- No opaque predicate/callback or whole-configuration integer accepted as a semantic seed merely because it can render an array.
- No RNG cursor hidden in executor state for a one-time seed draw; no stochastic seed distribution conflated with stochastic transition semantics.
- No centered array, crop, padding, batch shape, held-out split, palette, or raster treated as the native initial configuration.
- No fixed-lattice point/window API imposed on variable-support words, trees, graphs, bags, registers, or scalar configurations; no graph serialization order made semantic.
- No single-black-cell assumption used to prove T06/T07 or a behavior class; no symmetric seed used as rule-symmetry evidence.
- No “gray” value inferred from palette order without an explicit ALPHABET member/valuation.
- No compact representation accepted without an inverse on its invariant-valid image and a one-step commuting law; no finite execution lowering accepted without commuting through the complete requested horizon and observation scope.
- No requirement that every convenience constructor be invertible; stronger round-trip/commutation claims apply only to representations and lowerings that claim equivalence.
- No closed predicate/generator treated as automatically decidable, normalized, or samplable; unsupported/unknown capabilities and zero-mass conditioning remain explicit.
- No derivation descriptor that lazily runs another program/interpreter during target seed resolution; only frozen exact references plus a closed typed transform and evidence.
- No product ALPHABET mandated for temporal history or composite controls; require complete visible Markov/configuration roles and a lossless mapping, not one storage decomposition.
- No iid whole-cell law used when a structured component/overlay law is required to preserve exactly-one or other global invariants.
- No silent off-window drop, ignored time coordinate, sampling-based dedupe, unproved held-out-configuration claim, metadata-only transform claim, or dataset ID that omits identity-bearing decisions.

## Completion Requirements

- [ ] Every declared source candidate and governed asset is dispositioned under reproducible, honestly scoped protocols.
- [ ] Every retained excerpt/asset has exact provenance and its construction fact is separated from behavior, boundary, and view claims.
- [ ] The seed/profile model covers every evidenced deterministic and stochastic class, validation invariant, identity, transform, and realization distinction.
- [ ] Current API/runtime fit and a concrete Goal 2 handoff are implementation-ready with adversarial conformance cases.
- [ ] Global ledgers, independent review, all embedded checks, coverage/diff gates, and repository tests pass.

## Stage Results

IN PROGRESS.
