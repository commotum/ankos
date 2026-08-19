# Goal 8 Space Findings

This file records only vocabulary; closure arguments; and difficult boundaries
that do not fit cleanly in `spaces.csv`. The CSV is authoritative.

## Space vocabulary

- **Space** is the admissible address set plus operative relations; support law;
  and boundary law. It is not a semantic class such as “tape” or “image”.
- **Coordinate** is one independently addressable locus. Axis names such as
  `x`; `y`; and `v` are notation; the axis domain and relations carry the
  meaning.
- **Support** is the subset of Space realized at one time. Fixed support can
  retain the same loci at every slice; dynamic support can grow or shrink.
- **Boundary** resolves an operation that would leave or read beyond realized
  support. Infinite support has no outer boundary. Periodic identification;
  omission; halt; and blank extension are different laws and are stated rather
  than hidden in Seed or Rule.
- **Relation** is operative structure such as adjacency; total order;
  parenthood; or incidence. A graph is therefore `[t,v]` plus adjacency; not a
  special semantic Carrier kind.
- **Value** is the state attached to one address. Head state; cell color;
  orientation; activity flags; and a geometric pose can be values when they do
  not independently identify loci.
- **Embedding** is not automatically Space. A tree drawing; a 2D rendering; or
  a geometric pose becomes a Space axis only when the mechanics independently
  address; read; write; or relate locations through it.
- **One-shot transform** uses explicit stages such as `t∈{0,1}`. It is never
  `t-only` merely because feedback is absent.

For every discrete admitted claim; the state is an immutable history over
explicit `t`. An application preserves every coordinate through time `t`;
adds a complete successor slice at `t+1`; copies every realized location
outside the Frontier into that slice unchanged; and never overwrites the old
slice. If support changes; “complete successor slice” means the complete
support produced for `t+1`; all previous slices remain intact.

## B001 closure: synchronous local transforms

The invariant is one output per locus; computed from a bounded neighborhood in
the immutable old slice; followed by one shared commit. For any fixed finite
rank `d`; offsets are finite vectors in `Z^d`; so changing `d` does not change
the read/commit law. This proves `t+dD` for every finite `d>=1`; not an
infinite-rank stencil. The same invariant works on a fixed graph only when
rooted neighborhoods have finitely many rule-understood types. Node or edge
creation is outside the proof.

The Book separately shows 1D; 2D; and 3D cellular automata; discusses 4D and
higher lattices; and explicitly states the fixed-network generalization. A
one-step raster filter remains the same synchronous transform with
`t∈{0,1}`. Continuous or product-valued cell states enlarge the Alphabet; not
Space.

## B002 closure: mobile-head grid rewrite

The native transition is

```text
(control_t; head_t; values_t)
    -> (control_{t+1}; head_t + displacement; values_{t+1})
```

where only the bounded head footprint is rewritten and all other spatial
values copy into the new slice. The 2D Book rule already represents movement
as an integer displacement vector. Replacing that pair with a member of a
finite displacement set in `Z^d` proves the same construction for every finite
`d>=1`. Consequently SPF030 supports `[t,x]`; `[t,x,y]`; `[t,x,y,z]`; and all
higher finite Cartesian ranks. Square and hexagonal adjacency are evidenced.

This proof stops at fixed locally finite lattices. A head on an arbitrary
irregular graph is mechanically plausible but the Book separates sequential
network systems; the available evidence does not yet establish whether the
canonical family absorbs that case. It remains an honest bounded unknown.

Factoring `{control; head position; tape}` into separate registers or tagging
one tape value with the head changes the value encoding and concrete write
footprint; not the Space. In particular; head state or arrow orientation is
not another coordinate axis.

## B003 closure: multiple active loci

For a fixed finite rank; every active locus reads a bounded old-slice
neighborhood and emits finitely many moves; writes; splits; or deletions. A
declared collision law combines all emissions before one shared commit. Vector
offsets prove every finite Cartesian rank. Replacing those offsets by a finite
edge-label set proves fixed bounded-degree labelled graphs. The proof stops if
the topology itself changes; if a move has no declared resolution; or if
conflicts lack a total simultaneous law.

Storing activity as an Alphabet flag can make Frontier derivable; it does not
remove the coordinates on which active loci move or collide.

## B004 closure: independent parallel substitution

There are three genuinely different address forms inside the family:

1. an ordered word `[t,i]` whose current support changes length;
2. an aligned rank-`d` grid `[t,x_1,...,x_d]` whose compatible child blocks
   assemble into the next support; and
3. an occurrence set `[t,o]` whose values may carry a Euclidean pose.

The third distinction matters. Free geometric children can overlap; so their
Euclidean position alone need not uniquely address them. The Book rule acts on
occurrences independently and the Notes state that their affine poses extend
to any number of dimensions. Until another rule reads spatial neighbors; the
embedding is value structure rather than an additional operative axis.

The ranked-grid closure is constructive: for each fixed finite `d`; every old
tile emits a finite rank-`d` block and the declared product-order assembly
forms one successor slice. It stops at incompatible patches; contextual reads;
or topology-changing incidence laws.

## B005 closure: contextual substitution

The Book supplies two boundary witnesses: a 1D rule whose missing right
context omits the last locus; and a 2D grid explicitly wrapped in both
dimensions. For any fixed finite rank `d`; finite context offsets and child
placements can be lifted to `Z^d` without changing immutable old-slice reads or
the atomic generation commit. The boundary must either supply the complete
context or exclude that edge locus; and child patches must have a declared
compatible assembly.

Free geometric substitution is not silently included: the Book explicitly
uses its lack of an obvious stable neighbor relation as the contrast that
motivates grid-based contextual substitution. Likewise a one-match scan is a
different sequential mechanic; adding a 2D drawing to its scan does not make
it a native `t+2D` Space.

## B006 closure: structural pattern rewrite

A finite rooted ordered expression tree has a finite traversal order. That
order determines candidate matches and a nonoverlap set; selected subtrees can
then be replaced while every other node is copied into a complete successor
tree. Without rooted order; a separate match-selection relation is required.
The Book explicitly rejects a native higher-dimensional sequential scan:
imposing one merely linearizes the substrate.

## B007 closure: front deletion and rear append

Prefix deletion and suffix concatenation require only finite total order. The
same construction therefore works on any finite ordered support; while a
multidimensional realization whose adjacency is never read is only a queue
linearization. Cyclic rule phase is determined by time and remains Rule data.

## B008 closure: register machines

For finite named keys `{pc;r1;...;rn}`; an instruction reads the program
counter and its target registers; writes those keys into the new slice; and
copies every untargeted register. This proves arbitrary finite named-register
support. The proof stops at dynamically indexed arrays and pointers; which the
Book explicitly excludes. Packing all registers into prime powers is an
encoding because it hides the independently addressed keys.

## B009 closure: iterated maps

A deterministic self-map `F:A->A` always adds exactly one value at the next
time coordinate. Scalar and fixed-tuple states therefore remain `t`-only;
tuple fields belong to the value schema unless the rule independently
addresses them as loci. Digit rows are renderings of each atomic value; not a
native spatial axis. Branching or addressed fields end this closure.

## B010 closure: indexed recurrence

The recurrence index is explicit time. Whenever every dependency of
`f[t+1]` is a defined earlier coordinate; the rule appends one value without
rewriting history. A separate prefix axis only duplicates time. The proof
stops at future; cyclic; or undefined dependencies.

## B011 closure: iterative erasure

Given old ordered live support `K_t`; compute a deletion set from persistent
labels or current ranks and form `K_(t+1)=K_t-D_t`. This covers numeric lines;
current-rank decimation; and cyclic Josephus support. No Book evidence or
mechanics proof supplies an unordered multidimensional erasure neighborhood.

## B012 closure: digit-emitting transduction

The long-division and square-root procedures transform one fixed finite record
and emit exactly one symbol per step. Because the register fields are fixed
parts of that atomic record and are not dynamically selected as loci; emission
time itself addresses the output sequence. A materialized copied output tape
is therefore an encoding. Random-access storage or multiple independently
addressed outputs would require more Space.

## B013 closure: partial differential relations

Replacing one spatial variable by a vector in `R^d`; and supplying the needed
finite-dimensional partial derivatives; domain; and side data preserves the
PDE relation for every finite `d>=1`. This dimensional proof does not establish
existence; uniqueness; regularity; or infinite-dimensional fields. PDEs have
no built-in evolution time; boundary-value uses therefore need only singleton
outer query time. Finite-difference meshes remain approximating encodings; and
a continuous `t`-only flow is an ordinary differential equation.

## B014 closure and boundary: parallel network rewrite

Represent each port by a relation `E_p(t;v)`. Bounded paths in the old graph
determine every new port and fresh node; allowing one complete graph commit on
any finite or locally finite fixed-port graph. Effective dimension; tree form;
and nesting belong to adjacency. Drawn Euclidean positions do not.

The spring-threshold fracture candidate remains genuinely unresolved. Its
canonical note identifies bonds that break under stretch; but does not specify
a complete time schedule or ambient dimension. Neither can be inferred from a
simulation or illustration.

## B015 closure: multiway rewrite

Branch identity is a genuine coordinate because simultaneous complete states
are independently related to parents and successors. For every enumerable
single match; copy the parent substrate; perform one rewrite; and retain or
deduplicate the complete child. This construction covers strings; arbitrary
finite-dimensional arrays; expression trees; and atomic arithmetic states.
It stops at non-enumerable matches; undecidable state identity; or continuous
successor construction. The merged evolution graph is a derived one-shot
encoding that suppresses generation copies.

## B016 closure: local satisfaction

For fixed support `K` and supplied neighborhood relation `N`; satisfaction is
the one-shot conjunction of the same bounded predicate at every locus. The
argument is independent of Cartesian rank and applies equally to fixed graphs;
while explicit global occurrence obligations remain additional relations.
Embedded cellular-automaton time is a coordinate of the candidate spacetime
diagram; not an update schedule of the criteria family. Any search trajectory
belongs to an external solver such as B018.

## B017 closure: global-score sequential placement

On a candidate locus `K`; compute eligibility and score for all candidates;
choose one winner; and construct the complete successor with one placement and
all induced field changes. This works when `K` is finite; sampleable; or has an
attained maximum. It does not prove simultaneous multiwinner placement. The
Book supports a cyclic score field; a planar frontier lattice; and metric
circle and sphere placement. Unrolled plant diagrams are projections rather
than new native Space.

## B018 closure: stochastic local search

A proposal copies the complete incumbent; changes sampled loci; compares the
whole-state objective; and commits either the candidate or an unchanged new
slice. This proves any finite sampleable addressed support and is independent
of Cartesian rank. A rejected proposal still adds a complete `t+1` slice. The
proof says nothing about convergence; infinite-support sampling; or continuum
search.

## B019 closure and boundary: coupled field plus mobile locus

On any fixed locally finite adjacency relation; first compute the complete new
field from old neighborhoods; then apply the uniquely selected mobile move and
destination-write precedence. Multiple mobile loci; changing topology; or
undefined write conflicts are outside the proof. The mobile locus is one
distinguished address in the field; not another coordinate axis.

The Book passage never textually identifies its Cartesian dimension. A generic
cell-adjacency Space is supported; but `t+1D`; `t+2D`; and `t+3D` remain
unresolved as Book-native claims. In particular; 2D must not be inferred from
the illustration.

## B020 closure: alternating partitions

Let `P_t` partition support into disjoint finite blocks. Apply the block map to
each old block independently; then union all outputs into the complete
successor slice and copy any explicitly uncovered loci. This proves fixed
supports with scheduled graph or hypergraph partitions. Overlapping blocks
need a collision law. Partition phase is derived from `t`; so it is Rule data
rather than an independently addressed axis.
