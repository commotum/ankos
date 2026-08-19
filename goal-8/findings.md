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
- **Outer stage versus embedded time** must stay distinct. A one-shot query or
  construction stage may be written `q`; `tau`; or `stage` when its input is
  itself a history with physical or simulated time `t`. Renaming an axis does
  not change its status; collapsing two independent orders does.
- **Administrative coordinates** such as branch; replicate; program; input;
  agent; or rule-entry IDs are genuine Space only when the mechanics
  independently address or relate them. They are not Cartesian dimensions;
  and an intensional description of possible items does not by itself create
  an axis.
- **Ambient geometry** is Space when metric; topology; or boundary selects an
  operation—as in billiard collision or nearest-point retrieval. A drawn pose
  remains a value when no mechanic addresses the ambient locations—as in an
  ODE curve rendering or a freely embedded substitution occurrence.
- **Structural depth is not execution time.** Tree depth; network layer; and
  target-system time may coincide with an evaluation schedule in a concrete
  construction; otherwise an explicit outer work or query stage is kept
  separate.

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

The Book separately shows 1D; square-grid 2D; and 3D cellular automata;
discusses 4D and higher lattices; and explicitly states the fixed-network
generalization. Triangular; pentagonal; and Penrose examples require a
separate `[t,v]` tile-incidence claim: their 2D pose does not turn irregular
tile addresses into Cartesian `[t,x,y]`. A one-step raster filter remains the
same synchronous transform with `t∈{0,1}`. Continuous or product-valued cell
states enlarge the Alphabet; not Space.

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

The same transition is proved on a fixed finite-port edge-labelled graph:
replace a displacement symbol by a port label; follow its one selected edge;
and copy every other node. The proof requires finitely many rule-understood
ports and a total missing-port result. What remains unresolved is narrower:
arbitrary unlabelled irregular incidence supplies no canonical deterministic
destination selector when several neighbors are indistinguishable.

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

A total scan over an array is only a 1D encoding when matching never reads the
array's multidimensional incidence. But if finite patterns actually match and
replace rank-`d` blocks; those coordinates remain operative. Enumerating the
finite matches; applying a total tie/nonoverlap order; replacing the selected
blocks; and copying all other loci proves every fixed finite `d`. The proof
stops at infinite match sets; missing overlap policy; or undefined reshaping at
the array edge.

## B007 closure: front deletion and rear append

Prefix deletion and suffix concatenation require only finite total order. The
same construction therefore works on any finite ordered support; while a
multidimensional realization whose adjacency is never read is only a queue
linearization. Cyclic rule phase is determined by time and remains Rule data.
Front and rear are order roles; not boundary policies. The actual boundary is
underflow: after complete erasure or when the queue is shorter than the delete
width; the application must halt; be undefined; or use a declared short-queue
law.

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
labels or current ranks and form `K_(t+1)=K_t-D_t`. The Book shows a finite
interval and states the unbounded positive-integer process. Rank-based
decimation extends to finite orders and discrete well-orders of type `N`; an
arbitrary countable total order need not have a first or kth surviving element.
A key-predicate deletion can use a broader keyed set; but then keys; not order;
do the work. No evidence supplies an unordered multidimensional erasure
neighborhood.

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
a finite or countable rooted fixed-port graph when fresh identities are
canonical. Effective dimension; tree form; and nesting belong to adjacency.
Drawn Euclidean positions do not. A component-retention or drop decision must
also be total; local finiteness alone neither supplies that policy nor makes an
uncountable graph constructible.

The spring-threshold fracture candidate remains genuinely unresolved. Its
canonical note identifies bonds that break under stretch; but does not specify
a complete time schedule or ambient dimension. Neither can be inferred from a
simulation or illustration.

## B015 closure: multiway rewrite

A generation-state identity is a genuine coordinate because distinct complete
states at one generation are independently related to parents and successors.
It is not a persistent causal-path ID: two derivations can merge into one
equal child with multiple parents. For every finite match set; copy the parent
substrate; perform one rewrite; and retain or deduplicate each complete child.
This construction covers strings; arbitrary finite-dimensional arrays;
expression trees; and atomic arithmetic states. Countably infinite branching
requires an explicitly admitted relational semantics; it cannot be completed
by one ordinary executable application. The merged evolution graph is a
derived one-shot encoding that suppresses generation copies.

## B016 closure: local satisfaction

For fixed support `K` and supplied neighborhood relation `N`; satisfaction is
the one-shot conjunction of the same bounded predicate at every locus. The
argument is independent of Cartesian rank and applies equally to fixed graphs.
A separately evidenced existential occurrence requirement may be conjoined;
but locality does not prove arbitrary global obligations.
Embedded cellular-automaton time is a coordinate of the candidate spacetime
diagram; not an update schedule of the criteria family. Any search trajectory
belongs to an external solver such as B018.

## B017 closure: global-score sequential placement

On a candidate locus `K`; compute eligibility; select one winner; and construct
the complete successor with one placement and all induced field changes. A
global-score selector requires an attained maximum and total tie law. A
stochastic frontier selector instead requires a normalized probability kernel
and sampleability; sampleability alone does not make an argmax exist. Neither
form proves simultaneous multiwinner placement. The Book supports a cyclic
score field; a stochastic planar frontier lattice; and metric circle and
sphere placement. Unrolled plant diagrams are projections rather than new
native Space.

## B018 closure: stochastic local search

A proposal copies the complete incumbent; changes sampled loci; compares the
whole-state objective; and commits either the candidate or an unchanged new
slice. This proves any finite sampleable addressed support and is independent
of Cartesian rank. A rejected proposal still adds a complete `t+1` slice. The
proof says nothing about convergence; infinite-support sampling; or continuum
search.

## B019 closure and boundary: coupled field plus mobile locus

On any fixed finite or countable locally finite adjacency relation with a
total labelled or tie-resolved destination selector; first compute the
complete new field from old neighborhoods; then apply the uniquely selected
mobile move and destination-write precedence. Multiple mobile loci; changing
topology; or undefined write conflicts are outside the proof. The mobile locus
is one distinguished address in the field; not another coordinate axis.

The Book figure is a 1D cellular-automaton spacetime diagram: horizontal
position is `x`; successive rows are `t`; and the black crack marker occupies
one `x` at each step. Thus `[t,x]` is shown—not `[t,x,y]`. The viewport does not
prove whether the modeled line is finite or unbounded; that extent and its
boundary remain unstated. Replacing scalar offsets by finite vectors proves
every finite Cartesian rank; replacing them by a fixed labelled adjacency
relation proves the graph form. The proof does not admit dynamic topology or
multiple independently moving loci.

## B020 closure: alternating partitions

Let `P_t` partition support into disjoint finite blocks. Apply the block map to
each old block independently; then union all outputs into the complete
successor slice and copy any explicitly uncovered loci. This proves fixed
supports with scheduled graph or hypergraph partitions. Overlapping blocks
need a collision law. Partition phase is derived from `t`; so it is Rule data
rather than an independently addressed axis.

## Adversarial closure corrections: B021-B043

Several initial `unknown` rows merely recorded that the Book did not draw
another example. That is not the limit of a mechanics-based closure proof.

- B021 separates outer mutation `m` from rollout time `tau`. A finite Alphabet
  and finite neighborhood give a finite rule table on any fixed
  finite-neighborhood Space; mutating a table entry and separately evaluating
  the result therefore covers finite-rank lattices and fixed locally finite
  graphs. It does not prove rule mutation during one rollout.
- B023 is product accretion: support at stage `T` is `[0,T] x C`; the Frontier
  is `{T} x C`; and one new copy of fixed cross-section `C` is appended. This
  proves every fixed finite intrinsic rank but stops at branching; merging; or
  topology-changing rims.
- B027 and B029 lift rectangles to finite-dimensional hyperrectangles. Their
  closures require a total scan; deterministic overlap and tie laws; and
  respectively maximal-uniform-region or prior-equal-region predicates.
  Merely saying “higher-dimensional” without these laws would not be a proof.
- B030 depends on a rooted partition relation—not on rectangles as such. Any
  finite; well-founded; exact partition hierarchy with decidable uniformity
  supports the same accept-or-split recursion.
- B033 extends to finite; countable; or continuous datum Spaces only when a
  probability law and sampler are supplied. Without them a randomization test
  is undefined; this is an exclusion rather than an unresolved geometry.
- B043 depends on finite candidate adjacency and retained provenance. Those
  operations lift from the shown 2D grid to any fixed locally finite relation;
  they stop at dynamic topology; unbounded fanout; or missing provenance
  identity.

## Representation and time boundaries: B025-B054

Several families required separating operative coordinates from convenient
tables; drawings; or work schedules.

- B025's native time is causal precedence itself: `[e]` plus producer edges
  and their reachability order. A scalar update number or page row is an
  encoding; not the event-time coordinate.
- B026 and B050 use `[t,v]`. Edges are adjacency relations; not another axis.
  Directional local laws require typed or ordered ports; an unlabelled graph
  suffices only for permutation-invariant laws.
- B030's tree addresses are partition paths. Breadthwise recursion depth is an
  evaluation schedule; and rectangular page coordinates are an encoding of
  the hierarchy.
- B031 distinguishes a basis/sample/coefficient index from the geometric
  coordinates at which a transformed field may be materialized. A continuous
  basis parameter can still be a discrete address set of basis members.
- B035 and B036 keep outer reconstruction or application stages separate from
  target-system time and structural layer depth. B051 likewise separates
  one-shot construction `tau` from continuous physical event time `t_phys`.
- B032 closes over any fixed finite-neighborhood model Space. Learning or
  changing its topology remains unresolved because the Book supplies no
  topology hypothesis class; edit law; selection rule; or stopping law.
- B046's event mechanic lifts from a rectangle to every finite-dimensional
  hyperrectangle by taking the first positive face-hit time and reflecting the
  corresponding velocity components. Tied hits and Zeno accumulation require
  explicit resolution.
- B047's Laplace or harmonic-measure construction reproduces the attachment
  law without walker microtime. It is therefore a field-based encoding of
  first-passage aggregation; not evidence that the walker occupies field
  coordinates at every microstep.
- B048 has a finite contemporaneous population `P_t`; the Book does not fix
  persistent slots; survivor copying; cardinality; or identity allocation.
- B052 uses one-shot aggregation `tau`; alternative history `h`; and whatever
  coordinates belong to the measured base Space. A Monte Carlo sample index
  is an alternative axis; not sampler evolution time unless an update kernel
  is actually supplied.
- B053 needs a half-open-bin or tie convention. Without it; interval endpoints
  do not determine a total transduction even though the output remains a
  finite variable-length ordered stream.

## B055-B060 cross-family findings

B055 makes sample time itself explicit Space. Predictor coefficients and
residuals can remain product values at `[t]`; the finite lag relation reaches
earlier time coordinates and does not create a second spatial axis.

B056 has two bounded closures. Exact Euclidean nearest retrieval is unchanged
for every fixed finite dimension because it still computes the same distances
and selects an argmin; this stops at finite-dimensional, finite stored support.
Exhaustive retrieval also works on any fixed finite metric set because only the
metric and minimizer relation are used; this does not generalize spatial trees
or Newton descent to arbitrary metrics. The Book's d-dimensional tree is
operative auxiliary index Space in that variant, while the Newton example is
an explicitly timed, approximate two-dimensional basin search.

B057 exposes three different meanings of time without making time implicit:
layer index for feedforward evaluation, recurrence or individual-write index
for fixed recurrent networks, and optimization index when weights evolve.
Mutable weights justify independently addressed edge loci; fixed weights may
remain attributes of a fixed weighted relation.

The B058 finite-agent closure preserves one invariant: every agent reads the
same immutable joint history, all actions are emitted together, and one payoff
function commits the resulting payoff vector. It stops at fixed finite agent
sets with total strategies and payoff functions. The 256-by-256 rule
tournament is an observer over many games, not the Space of one game.

B059's numeric memory address is native because fetch; branch; indirect reads;
and writes resolve through it. Packing the whole machine into one value is
only an encoding. Countably unbounded memory is nevertheless proved by
declaring addresses `N` and one blank word from the outset. Every fixed-arity
instruction still fetches and writes only finitely many words; a first write
does not allocate a new coordinate but changes the value at an already
declared address. The proof stops at non-total address arithmetic; unbounded
per-step writes; or negative; transfinite; uncountable; or continuous address
sets.

B060's row and input axes are administrative rather than geometric, but they
are native because the construction enumerates machine rows, independently
addresses integer inputs and oracle cells, and compares or changes those
entries over explicit construction stages. Merely describing all possible
programs intensionally would not create these axes; their explicit enumeration
and addressed dependencies do.
