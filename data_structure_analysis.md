# Goal 8 Space Data-Structure Analysis

This analysis classifies all 230 data entries in `goal-8/spaces.csv` by the
representation their native Space requires.

Entry numbers count data rows and exclude the CSV header.

## Classification

- **A — Array-native:** ordinary n-dimensional arrays, masks, selectors,
  broadcasting, gathering, rolling, scattering, or integer indexing are
  sufficient.
- **R — Relational:** values can remain arrays, but the Space also needs an
  edge list, CSR adjacency, parent table, provenance table, partition
  hierarchy, or another explicit relation. Coordinates alone cannot recover
  the structure.
- **C — Continuous/intensional:** the native Space is not a finite
  enumeration. It needs a function, solver, sampler, measure, or symbolic
  relation. Arrays represent only a discretization or finite sample.
- **M — Mixed:** the row encompasses multiple representations or leaves a
  critical matter unresolved.

| Class | Count | Entries |
|---|---:|---|
| A | 129 | 1–2, 4–5, 7–14, 17–19, 21–24, 27–29, 31–32, 35–49, 51–52, 54–55, 57–59, 64, 77–79, 81–82, 85–94, 96–100, 102–104, 114, 126–130, 134–137, 142–143, 145, 147, 150, 154–158, 163–166, 169–173, 175–178, 180–181, 185, 187–188, 195, 197–198, 200–201, 209–211, 213–216, 218–219, 223–226, 228–230 |
| R | 74 | 3, 6, 15–16, 20, 25–26, 30, 33–34, 50, 66–76, 80, 83–84, 95, 101, 106, 116–125, 131–133, 138–141, 146, 148–149, 159–162, 167–168, 174, 182–184, 186, 189–192, 196, 199, 202–204, 212, 217, 220–222, 227 |
| C | 23 | 53, 60–63, 65, 107–110, 112–113, 115, 144, 152–153, 179, 193–194, 205–208 |
| M | 4 | 56, 105, 111, 151 |

This is a storage and addressing classification. It does not claim that every
Rule can be implemented using selection alone. An array-native system may
still use linear algebra, optimization, convolution, or a numerical solver.

## Relational entries

### Graph, network, incidence, or topology

Entries 3, 6, 15–16, 20, 30, 66–70, 80, 83, 95, 106, 121–125, 146,
148–149, 159, 162, 167–168, 186, 189–192, 196, 202–204, 212, and 220–222
require topology that cannot be inferred from ordinary coordinates.

A typical representation is:

```python
node_values: ndarray[N, ...]
edge_index: ndarray[2, E]
edge_values: ndarray[E, ...] | None
```

For larger sparse systems, the same relation can use CSR-style arrays:

```python
indptr: ndarray[N + 1]
indices: ndarray[E]
```

This remains numerical and vectorizable, but it is not ordinary neighborhood
selection over a coordinate tensor such as `[t,x,y]`. A dense adjacency matrix
can encode the same relation, but costs `O(N^2)` memory even when the graph has
only `O(N)` edges.

This category includes Penrose and irregular tilings, port-labelled graphs,
network rewrites, causal posets, circuits, sorting networks, factor graphs,
weighted networks, and sampled causal-order networks.

### Trees, hierarchies, lineage, and provenance

Entries 25–26, 33–34, 101, 116–120, 131–141, 160, 174, 183–184, 199,
and 217 require parent, child, partition, or provenance relations.

They can use arrays such as:

```python
parent: ndarray[N]
children_indptr: ndarray[N + 1]
children: ndarray[E]
```

or event tables:

```python
event_source: ndarray[E]
event_target: ndarray[E]
```

Selectors can operate over these arrays, but coordinate geometry cannot derive
parenthood or provenance.

### Multiway branching

Entries 71–76 and 84 need both a ragged collection of states and a transition
relation between state identities. Each state can itself be an array, word, or
tree, but the multiway collection is a graph.

### Arbitrary dependency or indirect storage

Entries 50, 161, 182, and 227 require additional indexing:

- Entry 50 has arbitrary well-founded recurrence dependencies.
- Entry 161 has collision chains or probe structure in a hash table.
- Entry 182 has keyed memo storage.
- Entry 227 has countably unbounded random-access memory.

Finite integer-address memory, entry 226, is array-native. Countably unbounded
memory instead needs sparse pages, a dictionary, or a default-backed sparse
array.

## Continuous and intensional entries

### Fields, differential relations, and continuous flows

Entries 60–63, 65, 107–110, 112–113, 115, 144, 179, and 193–194 include
PDE fields, ODE trajectories, continuous material sheets and shells,
continuous functions, continuous operator domains, and billiard flows.

A finite-difference mesh can be an array—entry 64 explicitly records that
encoding—but the mesh is not the original continuous Space. The native object
is closer to:

```python
field(coordinates) -> values
trajectory(time) -> state
```

plus a solver or defining relation.

### Probability spaces and sums over histories

Entries 152–153 and 205–208 require some combination of a sampler, probability
measure, action functional, history generator, and numerical or symbolic
integration. Entry 209 is array-native because it has already discretized and
sampled the underlying continuous construction.

### Countably infinite realized support

Entry 53 describes an actually countably infinite integer support. It cannot
be materialized as a complete NumPy slice and therefore needs a lazy predicate,
symbolic rule, or sparse/default-backed representation.

## Mixed entries

- **56:** Finite enumerated support is array-native; countably infinite support
  requires lazy or sparse representation.
- **105:** The proposed tagged address array is straightforward, but the
  mutation/cell coupling is unresolved.
- **111:** The representation depends on cross-section `C`. Cartesian `C` is
  array-native; graph or mesh `C` is relational; continuous `C` is
  intensional.
- **151:** A randomization wrapper over finite `D` inherits the representation
  of `D`; it adds no independent Space structure.

## Important distinctions

Finite continuous point sets are array-native. Entries 87–88 and 214–215 have
real-valued coordinates but only finitely many objects or points:

```python
points: ndarray[N, D]
distances = np.linalg.norm(points - query, axis=-1)
```

That differs fundamentally from a continuous field assigning a value to every
point of a continuum.

Dynamic words and grids are also array-native. A substitution can produce one
new array per time:

```python
states: tuple[np.ndarray, ...]
```

The arrays need not have identical shapes. Padding may later be useful for ML
batches, but it is not part of the native SimpleProgram.

Packed encodings such as entries 8, 43, 228, and 230 are classified as
array-native only in the vacuous sense that `[t]` indexes one compound value.
They hide all useful internal address structure and should not guide the native
API.

## Architectural conclusion

Ordinary coordinates and NumPy selectors cover 129 of the 230 entries. A
second generic representation—an indexed relation over ordinary integer
identities—covers most of the remaining discrete systems. This does not require
semantic classes for trees, graphs, circuits, or causal networks; it requires
one compact relational representation.

Only genuinely continuous, infinite, or intensional entries require a separate
backend.
