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
