# `ca` 0.2.0 Target Public API

Status: **accepted architectural direction; runtime migration pending**

This document defines the target semantic API for the ANKoS refactor. The
five-field runtime currently present in the repository still contains
`frontier` and patch/disposition machinery; that implementation does **not**
yet satisfy this contract.

The ownership decisions in this document are authoritative for the refactor.
Older Goal 6 documents remain useful historical records, but their
`Seed + Alphabet + Frontier + Neighborhood + Rule` architecture and mutable
patch vocabulary are superseded here.

## One Definite Program Value

Every executable `SimpleProgram` is one immutable value with exactly five
definite fields, in this order:

```python
@dataclass(frozen=True)
class SimpleProgram:
    space: Space
    alphabet: Alphabet
    seed: Seed
    neighborhood: Neighborhood
    rule: Rule
```

Conceptually:

```text
SimpleProgram =
    SPACE
  + ALPHABET
  + SEED
  + NEIGHBORHOOD
  + RULE
```

| Field | Public meaning |
|---|---|
| `space` | The exact coordinate set or coordinate law, operative relations, support law, finite extent where applicable, and boundary/access behavior |
| `alphabet` | The exact set or schema of values that may occur at Space coordinates |
| `seed` | The exact complete initial slice at `t=0`, including its initial realized support |
| `neighborhood` | The exact read/dependency relation used to observe earlier coordinates when constructing a new slice |
| `rule` | The exact deterministic, relational, or stochastic law that constructs complete successor slices from admitted prior state |

“Definite” does not mean finite or exhaustively materialized. A field may
denote an infinite lattice, continuous region, symbolic relation, closed
probability kernel, or intensionally represented state. It means that the
field contains no unresolved choice, range, missing parameter, or unrecorded
ambient decision.

Choices and ranges belong to presets. Resolving a preset produces definite
component values and ultimately definite `SimpleProgram` values.

There is no top-level `FRONTIER`, `DOMAIN`, `SHAPE`, `BOUNDARY`, scheduler, or
parameter bag:

- Space owns coordinate, shape, support, and boundary semantics.
- Activity is represented in state values or derived from state and Space.
- Shape and Boundary are not separate fields; they are applicable parts of a
  concrete Space.
- Component parameters belong to component presets before resolution.
- Execution horizon, replay selection, projection, batching, and resources are
  run or dataset concerns rather than program fields.

## Space, Slices, and Explicit Time

Time is never implicit. For an ordinary discrete spatial system, a coordinate
has the form:

```text
(t, x)
(t, x, y)
(t, x, y, z)
(t, v)             # relational/graph address
```

The Space defines the exact time coordinate as well as the non-temporal
coordinates and relations. This document specifies the discrete contract,
with `t in N` and explicit transitions from `t` to `t+1`. Non-discrete
families will specialize that contract when they are implemented; they do not
need speculative machinery in this core API.

Let `K_t` be the realized non-temporal support at time `t`. A complete state
slice is:

\[
X_t:K_t\rightarrow A.
\]

One discrete application constructs a completely new slice:

\[
X_t\longmapsto X_{t+1}.
\]

The complete history through `T` is the immutable union of those disjoint
time-addressed slices:

\[
H_T=\bigcup_{0\le t\le T}\{(t,c,X_t(c)):c\in K_t\}.
\]

Nothing at time `t` is updated, replaced, deleted, or overwritten. Even when a
logical value is unchanged, its next occurrence is written at a new address:

\[
X_{t+1}(c)=X_t(c),
\]

where `(t,c)` and `(t+1,c)` are different coordinates.

For dynamic-support systems, `K_{t+1}` may differ from `K_t`. A locus absent
from the new slice has not been deleted from history; its earlier occurrence
remains at time `t`. A newly appearing locus exists only in the new slice.

A complete slice may use a lossless intensional or default-compressed
representation. “Complete” means that its value and presence are determined
for every admitted coordinate, not that an infinite support must be enumerated.

## What Space Owns

Space answers: **where can state exist, how are those coordinates related, and
what happens at the limits of the coordinate set?**

| Concern | Owner |
|---|---|
| Time coordinate or time relation | Space |
| Rank, axes, coordinate domains, and topology | Space |
| Fixed extent such as length `7` or shape `(11, 11)` | Space |
| Periodic, reflective, fixed-exterior, or rejecting access | Space |
| Whether per-slice support is fixed, sparse, growing, shrinking, or otherwise constrained | Space |
| Initial realized support and initial values | Seed |
| Complete support and values of the next slice | Rule, constrained by Space |
| Allowed values at every realized coordinate | Alphabet |

For example, these are different Spaces:

```python
FiniteLine(length=7, boundary=Periodic())
FiniteLine(length=7, boundary=FixedExterior(0))
FiniteLine(length=11, boundary=Periodic())
InfiniteLine(default=0)
```

A finite extent is not a Seed property. The same dense seven-value input can
mean either a complete finite world or a finite input window embedded in a
default-completed infinite world:

```python
# A genuinely finite world.
space = FiniteLine(length=7, boundary=Periodic())
seed = LiteralSeed((0, 0, 0, 1, 0, 0, 0))
```

```python
# An infinite world represented intensionally, with one non-default locus.
space = InfiniteLine(default=0)
seed = DefaultCompletedSeed(default=0, overrides={0: 1})
```

The second Seed denotes a complete infinite slice intensionally; its
non-default footprint contains one coordinate. A dense input window can
desugar to that representation, but the input array alone cannot determine
whether the world is finite, periodic, reflective, fixed-exterior, or
infinite.

Dense-Seed shape inference may exist as convenience syntax, but it must
desugar into an explicit Space plus an exact Seed. Seed never becomes the
semantic owner of geometry or boundary behavior.

Some access laws contain values, such as `FixedExterior(0)` or an infinite
Space's default value. Compatibility validation must ensure that those values
belong to the resolved Alphabet.

## Alphabet and Activity

Alphabet defines semantic values, including tagged unions and product values.
Persistent or mobile activity is ordinary state, not a separate Frontier.

For a Turing-style machine with tape symbols `Gamma` and controller states
`Q`, the per-coordinate Alphabet is:

\[
A=\operatorname{Inactive}(\Gamma)
  \;\cup\;
  \operatorname{Active}(Q\times\Gamma).
\]

For a binary tape and two controller states, the six values are:

```text
Inactive(0)
Inactive(1)
Active(0, 0)
Active(0, 1)
Active(1, 0)
Active(1, 1)
```

Equivalently:

```text
BLACK
WHITE
UP_BLACK
UP_WHITE
DOWN_BLACK
DOWN_WHITE
```

The size of this tagged Alphabet is:

\[
|A|=|\Gamma|+|Q||\Gamma|=(|Q|+1)|\Gamma|.
\]

This is a tagged union rather than the full product
`is_active x head_state x symbol`, because an inactive cell has no controller
state. The latter would introduce meaningless inactive-with-head-state values.

For a single-head machine, Seed places exactly one `Active(q, symbol)` value,
and Rule preserves one active value by construction. Alphabet only defines
which tagged values are legal; it does not acquire a separate global-invariant
language.

The general activity rule is:

- Persistent mobile identity, such as a head, cursor, walker, crack, or active
  graph node, is encoded in Alphabet values.
- Activity derived from values, such as an unstable numeric cell, is computed
  from those values.
- Activity derived from coordinates or support, such as an append position or
  current rim, is computed from Space and the current slice.
- A compiler may derive an `active_sites` execution plan for efficiency, but
  it is not a semantic field and is never serialized as the program's meaning.

## Seed

Seed is one exact complete `t=0` slice admitted by Space and Alphabet. It does
not denote a collection, unresolved generator, or ambient random draw.

Seed validation checks at least:

- every realized initial coordinate is admitted by Space;
- every initial value belongs to Alphabet;
- the initial support obeys Space's support law; and
- the Seed satisfies Rule and Neighborhood preconditions, such as containing
  exactly one active head when that program requires one.

Structured and random seed *presets* may enumerate or sample many Seeds. Each
result of that process is an exact Seed before it enters a `SimpleProgram`.
Replay information needed to reproduce a sampled Seed belongs to preset or
dataset provenance; the resolved Seed itself contains the exact realized
state.

## Neighborhood

Neighborhood defines the exact observation/dependency interface used while
constructing new coordinates. It may be:

- a fixed finite offset stencil;
- a compound set of independently summarized regions;
- a graph-relative or port-labelled neighborhood;
- an indirect lookup whose address is stored in state;
- a read over earlier time coordinates;
- a global finite observation; or
- a closed intensional relation.

Neighborhood does not grant write permission and does not select a mutable
region. Space resolves coordinate and boundary access; Neighborhood specifies
which resolved values and identities become Rule input.

For ECA, Neighborhood is the ordered triple `(left, self, right)` from slice
`t`. For the tagged-head machine, it must expose enough adjacent tagged values
for Rule to move the unique `Active` tag while retaining tape symbols.

## Rule

Rule is the exact law relating resolved Neighborhood observations to complete
successor outcomes. A Rule may be deterministic, branching, stochastic,
algebraic, structural, differential, or intensional, but its law is fully
bound in a `SimpleProgram`.

For a deterministic discrete program:

\[
O_t=N(H_t),\qquad R(O_t)=X_{t+1}.
\]

For a relational discrete program:

\[
R(N(H_t))\subseteq\{\text{complete admitted slices at }t+1\}.
\]

Rule cannot inspect history outside the interface declared by Neighborhood.
A law that needs historical or global information declares a correspondingly
historical or global Neighborhood rather than receiving hidden ambient state.

Every successor alternative is a complete slice. Rule does not return a CRUD
patch, a set of replacements, or `KEEP`/`Preserve`/`Delete` dispositions.

This does **not** mean that Rule secretly contains a Frontier. Where activity
is dynamic, the current slice already records it through Alphabet values or
makes it derivable from values, coordinates, and support. Rule propagates that
explicit state while constructing the next complete slice.

For a right-moving tagged head, the complete new slice contains:

- `Inactive(written_symbol)` at the former head's logical coordinate;
- `Active(next_control, old_destination_symbol)` at the destination's new
  time coordinate; and
- the corresponding copied value at every other admitted coordinate in the
  new slice.

No earlier coordinate is replaced. A local implementation may share unchanged
persistent structure, but physical sharing is not part of semantic identity.

## Constructing One Exact Program

The target direct-construction spelling is:

```python
import ca

program = ca.SimpleProgram(
    space=ca.spaces.finite_line(
        time=ca.spaces.discrete_time(start=0),
        length=11,
        boundary=ca.spaces.periodic(),
    ),
    alphabet=ca.alphabets.boolean(),
    seed=ca.seeds.literal(
        (False, False, False, False, False, True,
         False, False, False, False, False),
    ),
    neighborhood=ca.neighborhoods.offsets(-1, 0, 1),
    rule=ca.rules.elementary(30),
)
```

This value contains no open width, boundary, rule-number, or Seed choice.
Different widths, boundaries, exact Seeds, or rule tables produce different
concrete `SimpleProgram` values, even when all belong to the same ECA preset
and taxonomy family.

Constructor spellings in this section describe the target namespace and may
be introduced incrementally during migration. The five-field ownership and
complete-slice semantics are not provisional.

## Presets

A preset is a declarative generator, enumerator, sampler, or constrained
factory for **definite values**. A preset is not a sixth program field and is
not itself executable as a `SimpleProgram`.

Conceptually:

```text
Preset[T] -> one or more definite T values
```

Presets may exist independently for every field:

```text
SpacePreset
AlphabetPreset
SeedPreset
NeighborhoodPreset
RulePreset
```

They may also be composed into a whole-program `ProgramPreset`:

```text
field presets
    ↓ compatibility-constrained composition
ProgramPreset
    ↓ resolve / enumerate / sample
definite SimpleProgram values
```

For example:

```python
eca_programs = ca.presets.ProgramPreset(
    spaces=ca.presets.spaces.finite_lines(
        lengths=range(5, 101),
        boundaries=(
            ca.spaces.periodic(),
            ca.spaces.fixed_exterior(False),
        ),
    ),
    alphabets=ca.presets.exact(ca.alphabets.boolean()),
    seeds=ca.presets.seeds.binary(
        ca.presets.seeds.single_active(),
        ca.presets.seeds.alternating(),
        ca.presets.seeds.bernoulli(probabilities=(0.1, 0.5, 0.9)),
    ),
    neighborhoods=ca.presets.exact(
        ca.neighborhoods.offsets(-1, 0, 1),
    ),
    rules=ca.presets.rules.elementary(rule_ids=range(256)),
)
```

The Seed preset receives the resolved Space and Alphabet and produces exact
Seeds of the correct extent and value schema. A Bernoulli preset may use
replayable sampling during expansion, but no unresolved Bernoulli law remains
in the resulting `SimpleProgram.seed`.

Alphabet presets work the same way. A machine-Alphabet preset may range over:

```text
n_head in {1, 2, 3, 4, 5}
n_cell in {1, 2, 3, 4, 5}
```

and generate 25 exact ordered `(n_head, n_cell)` combinations. Each resolved
Alphabet contains:

\[
n_A=(n_\text{head}+1)n_\text{cell}
\]

tagged active/inactive values.

### Compatibility, not a blind Cartesian product

Program-preset resolution follows semantic dependencies:

```text
SPACE
├── constrains Seed coordinates and support
├── constrains Neighborhood relations and access
└── constrains Rule's admitted successor support

ALPHABET
├── constrains Space exterior/default values
├── constrains Seed values
├── constrains Neighborhood observations
└── constrains Rule inputs and outputs

NEIGHBORHOOD
└── constrains Rule's observation schema
```

Examples of incompatible combinations include:

- a 2D offset Neighborhood with a 1D line Space;
- an ECA Rule with a non-binary Alphabet;
- a tagged-head Rule without exactly one active value in Seed;
- a fixed exterior value absent from Alphabet; and
- a Seed whose realized support violates the selected Space.

The resolver rejects incompatible tuples with focused errors; it does not ask
the user to repeat cross-field facts or write a global constraint expression.

### Relationship to PE configs

This resembles the config machinery in `/home/jake/Developer/pe` because one
declarative Python file can expand into many concrete objects. The semantic
level is different:

```text
PE ExperimentConfig
    -> model alternatives, dataset mixtures, repetitions, evaluations

ANKoS ProgramPreset
    -> compatible, definite SimpleProgram values
```

A downstream `DatasetPlan` may then play the broader PE-like orchestration
role by selecting programs, rollout horizons, repetitions, splits, mixtures,
and projections.

User preset files are ordinary Python modules built from public constructors
and preset combinators. Their source spelling is provenance, not part of the
resolved program's semantic identity.

## Applying and Rolling Out Programs

The family-blind semantic operation consumes a definite program and an
admitted immutable history:

```python
result = ca.apply(program, history)
```

Conceptually it performs:

```text
1. Validate the complete current history against Space and Alphabet.
2. Resolve Neighborhood observations through Space relations and access laws.
3. Ask Rule for its complete successor-slice relation.
4. Validate every complete candidate slice against the five resolved program
   fields.
5. Append each valid candidate as a new immutable branch at the next time
   coordinate while preserving every earlier slice.
```

An application result distinguishes:

```text
ApplicationComplete(complete_successor_slices_and_evidence)
ApplicationNoSuccessor(reason_and_evidence)
ApplicationRejected(validation_fault)
```

Deterministic programs normally return one complete successor slice.
Branching, stochastic, constraint, and intensional programs may denote many
or a measured/intensional set of complete successor slices. Validation is
atomic at the whole-slice level: no partial candidate becomes authoritative.

Rollout starts from the exact Seed and repeatedly applies the same program:

```python
trajectory = ca.rollout(
    program,
    steps=100,
    replay_key=1234,
)
```

Its target signature is:

```text
rollout(program, *, steps, replay_key=None) -> RolloutResult
```

There is no `initial=` override. Supplying another initial state means
constructing another definite Seed and therefore another `SimpleProgram`.

`steps` selects a finite application prefix; it is not Space shape, Seed data,
or necessarily physical time duration. Each discrete application still adds
the explicitly addressed successor slice at `t+1`. Replay keys realize
already-declared stochastic Rule laws; they do not repair an unresolved Seed
or program preset.

Non-discrete execution is deliberately deferred until those families are
implemented. Its design must retain the two settled principles: time remains
explicit, and earlier coordinates are never mutated.

## Catalog and Taxonomy

The 60 canonical SPF families remain descriptive taxonomy and development
obligations. They are not runtime subclasses, executor branches, or
automatically implemented program constructors.

The six catalog homes remain navigation groupings:

```text
automata
substitua
machina
media
criteria
dynamica
```

A catalog family can own reusable presets without determining semantic
identity. For example:

```text
SPF050 synchronous-local-state-transform    broad mechanics family
ECA ProgramPreset                           constrained program suite
Rule 30, width 11, one exact Seed            definite SimpleProgram
```

Rule 30 and Rule 90 are distinct concrete program values but remain members
of the same ECA preset and taxonomy family. Likewise, changing exact shape or
Seed produces another concrete value without creating a new taxonomy family.

Catalog IDs, names, aliases, sources, and Book order are metadata. They never
select an executor or appear as a sixth field.

## Serialization

Canonical program serialization contains the expanded, validated fields:

```text
space
alphabet
seed
neighborhood
rule
```

It preserves:

- explicit time and non-temporal coordinates;
- Space relations, support law, shape, and boundary/access behavior;
- the exact complete `t=0` Seed slice;
- Alphabet value identities;
- Neighborhood dependency structure; and
- Rule's complete-successor relation, including exact stochastic laws where
  present.

It does not serialize a preset alias in place of the resolved structure.
Applications that need the preset filename, arguments, sampling key, dataset
split, or human invocation history keep a separate provenance manifest.

The current five-field wire schema containing `frontier` is incompatible with
this contract and must receive a new schema version during implementation.
Patch dispositions and writable capabilities are not migrated into the new
canonical format.

## Migration From the Current Runtime

The architectural migration is:

| Current runtime concept | Target concept |
|---|---|
| `CarrierContract` plus concrete Carrier boundary | Definite `Space` |
| Seed-produced Configuration carrying geometry | Exact Seed slice validated against Space |
| `WritableRegion` / `Frontier` | Removed from semantic API |
| Active selector | Alphabet/state tag or predicate derived from state and Space |
| `Preserve`, `Replace`, `Delete`, `Absent`, `Create` | Complete successor-slice construction |
| Sparse write patch | Lossless representation of a complete slice |
| `rollout(..., initial=...)` | Construct another program with another exact Seed |
| Parameterized catalog convenience call | Preset resolving to definite program values |

Removing Frontier does not require discarding every internal optimization. A
compiler may derive active sites, affected neighborhoods, persistent-structure
sharing, or a finite execution plan. Such artifacts must be observationally
equivalent to complete-slice semantics and must not become serialized program
meaning.

No destructive in-place migration of old configurations is meaningful. A
migrator must reconstruct explicit Space, Alphabet, exact `t=0` Seed,
Neighborhood, and complete-slice Rule semantics, or reject the old recipe as
ambiguous.

## Target Package Ownership

The target public organization is:

```text
src/ca/
├── __init__.py
├── program.py
├── spaces.py
├── loci.py
├── alphabets.py
├── seeds.py
├── neighborhoods.py
├── rules.py
├── serialization.py
├── py.typed
├── presets/
│   ├── __init__.py
│   ├── spaces.py
│   ├── alphabets.py
│   ├── seeds.py
│   ├── neighborhoods.py
│   └── rules.py
└── catalog/
    ├── __init__.py
    ├── entries.py
    ├── automata.py
    ├── substitua.py
    ├── machina.py
    ├── media.py
    ├── criteria.py
    └── dynamica.py
```

| Namespace | Responsibility |
|---|---|
| `ca.program` | `SimpleProgram`, complete-slice application, rollout, histories, and result records |
| `ca.spaces` | Time and coordinate Spaces, relations, support laws, shapes/extents, and boundary/access behavior |
| `ca.loci` | Shared coordinate, identity, and relation vocabulary used by Spaces |
| `ca.alphabets` | Exact value schemas, tagged unions, and products |
| `ca.seeds` | Exact complete initial slices and Seed validation |
| `ca.neighborhoods` | Exact read/dependency relations |
| `ca.rules` | Exact complete-successor laws and typed no-successor relations |
| `ca.presets` | Preset protocols, choices, ranges, compatibility resolution, and whole-program composition |
| `ca.serialization` | Versioned canonical codecs and typed decode results |
| `ca.catalog.entries` | Descriptive family, name, source, and provenance metadata |
| six catalog modules | Family-owned presets and unfinished canonical development surfaces |

`frontiers.py` is removed from the target public component surface. If a
compiled active-site plan remains useful internally, it belongs to private
execution machinery and carries no independent semantics.

## Downstream Dataset and PE Integration

Dataset construction remains downstream of the semantic API:

```text
field presets
    ↓
ProgramPreset
    ↓ resolve compatible choices
definite SimplePrograms
    ↓ rollout with horizons/replay choices
semantic Trajectories
    ↓ split/mix/project/tokenize
PE-facing datasets and batches
```

`DatasetPlan` may own:

- enumeration or sampling policies;
- preset-resolution provenance;
- rollout horizons and repetitions;
- train, evaluation, and out-of-distribution splits;
- trajectory mixtures and weights;
- coordinate and value serialization for ML;
- padding, masking, and batch layout; and
- replay keys and dataset-level reproducibility.

It may not redefine Space, Alphabet, Seed, Neighborhood, or Rule semantics
after a definite program has been constructed.

This recovers the useful separation from the old PE integration while making
the ownership more explicit:

```text
ProgramPreset     chooses a space of compatible programs
SimpleProgram     is one exact program and exact initial state
rollout           produces one semantic trajectory prefix
DatasetPlan       generates and organizes many trajectories
projection        converts them into ML representations
```

## Short Form

The complete direction is:

```text
SimpleProgram = SPACE + ALPHABET + SEED + NEIGHBORHOOD + RULE

Preset[T]
    generates definite T values

ProgramPreset
    combines field presets subject to compatibility
    and resolves to definite SimplePrograms

Rule
    constructs complete new time slices

Trajectory
    preserves every earlier slice immutably

DatasetPlan
    selects, runs, mixes, and projects many programs
```

Shape belongs to Space when it limits which coordinates exist. Initial
footprint belongs to Seed. Boundary behavior belongs to Space. Dynamic
activity belongs to Alphabet/state or is derived from state and Space. There
is no semantic Frontier and no CRUD transition model.
