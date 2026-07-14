# 11-T29-NETWORK

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: the T29 row and runner contract in `architecture-audit.md` supersede any prohibition on transparent graph schemas or network-executor framing below.

The evidence/search closure and conformance fixtures remain valid. A rooted graph, graph occurrences/views, and typed create/rewire/project replacements are transparent DOMAIN/NEIGHBORHOOD/RULE/UPDATE choices inside the shared runner, not a network executor.

## Current Facts

- Exact catalog row: T29, CSV line 30, `Network Systems`; taxonomy seed `ref/notes/CA-Types.md:786-813`. The taxonomy supplied search vocabulary only.
- The Chapter 5 construction removes fixed geometric support. Native state is a finite nonempty directed graph with one distinguished root and exactly two distinguished outgoing ports per node, conventionally `above/below` or `1/2`. Drawing coordinates, wire routes, and node display numbers are not state.
- Self-loops, cycles, two ports sharing one target, distinct nodes with identical local structure, and arbitrarily many incoming edges are all native. Every retained node is forward-reachable from the root.
- Port labels and the root are semantic. The page-209 count of label-ignored reachable networks is a static enumeration observer, not the runtime equality law.
- Semantic equality is root- and port-preserving vertex isomorphism. It never merges automorphic, bisimilar, or locally indistinguishable nodes.
- An exact canonical serialization is available: breadth-first discovery from the root, visiting port `above` before `below`, and assigning integers on first discovery. For finite root-reachable deterministic two-port graphs this codec is an exact isomorphism canonicalizer, not a heuristic graph layout.
- A path read is a finite word over ports, including epsilon. It folds left-to-right through one immutable old graph; epsilon returns the source node.
- The local signature used by the contextual rules is a tuple of cardinalities of exact-length endpoint sets, not cumulative metric balls. For depth two the complete evidenced key set is `(1,1),(1,2),(2,1),(2,2),(2,3),(2,4)`.
- Programs are finite closed data. A row returns two typed port-target expressions: either an old-snapshot path endpoint or one newly inserted node whose own two ports target old-snapshot path endpoints.
- Every syntactic insertion occurrence allocates a distinct fresh node, even when two descriptors are equal or both parent ports request identical insertions. Fresh nodes cannot target one another in the evidenced grammar and never fire in their birth event.
- All old nodes fire exactly once against the same old snapshot. Commit retains every old node, installs both rewritten old-node ports, installs all fresh-node ports, and only then projects to the directed forward closure of the preserved old root.
- The projection is native to the reference parallel evolution. It is not weak connectivity, not undirected connectivity, not deletion before rewriting, and not a layout cleanup. Direct deletion is absent; nodes disappear only through root-reachability projection.
- Projection is also a correct factor of future parallel behavior: the rule grammar cannot reconnect a dropped old reachability class because all direct and fresh targets follow paths inside the firing source's old forward-reachable class.
- A successful update has exactly one successor. An isomorphic or literal identity update is still `Advanced(changed=false)`; there is no intrinsic halt, boundary, node cap, or fixed-point stop.
- The four page-214 uniform rerouting rules on the canonical five-node seed have periods 5 and 4, a fixed point after one event, and a one-node collapse after two events, respectively.
- The two page-215 creating rules grow from the singleton seed as `1,2,4,8,...`. Their first two reference-ordered snapshots distinguish preserved from swapped fresh-node ports.
- The page-216 restricted one-step grammar has 6 possible expressions per parent port, 36 per-node actions, and `36^2=1296` complete depth-one tables. No analogous finite depth-two alphabet or rule count is supplied.
- Pages 217-218 and the Notes provide five exact depth-two tables and their node-count series through event 15; long-run anchors and one exact repeated-state period independently guard the implementation.
- The parallel construction has zero unresolved native mechanics. A related sequential-network note supplies a six-row `{rewrite,move_port}` table and its figure evidences reachability pruning, but neither prose, figure, nor official program data determines old-edge versus committed-edge movement, projection anchor, or projection/movement order. That variant is explicitly deferred behind a source-acquisition gate rather than guessed.
- Fixed-topology cellular automata and Boolean networks, undirected trivalent space networks, cluster substitution, network mobile automata, causal networks, multiway evolution, and constraint-defined networks are related constructions, not switches on the T29 graph-axis preset.
- T29 is the first catalog row whose Markov state contains mutable cyclic topology. T20 ordered trees cannot preserve arbitrary sharing/cycles, and T27 occurrence bags have no adjacency.
- The current runtime contains no graph carrier, graph selector, port-path read, fresh-node write, graph UPDATE policy, isomorphism codec, or ragged graph trace. These are typed additions to the common axes, not grounds for a network executor.

## Updated Assumptions

- `RootedPortGraph` is finite, nonempty, and internally closed. Every node has exactly one target for each of the two ports, and every node is directed-forward-reachable from the root.
- Semantic vertex tokens are occurrence identities local to a snapshot. They support aliasing and cycles but are alpha-renamable. Integers emitted by the reference codec are not rule-visible identities.
- Ports are ordered as `Above=1` then `Below=2` for path syntax and canonical traversal. Erasing or swapping the port order changes a graph unless an explicitly separate relation proves an isomorphism.
- A path word is closed structural data, never a traversal callback. Its endpoint is evaluated only in the old graph and remains valid during proposal construction.
- For depth `d`, `R_k(v)` is the set of endpoints of all port words of exactly length `k` from `v`. The contextual read is `(|R_1|,...,|R_d|)`. The necessary bound `|R_(k+1)| <= 2|R_k|` does not define a complete generic key set.
- A complete program declares one read profile and contains exactly one unique row for every declared key. Missing rows, duplicate rows, undeclared keys, invalid words, or implicit host-language fallthrough are invalid program data.
- `InsertFresh(a,b)` is a generative value in the result algebra, not a side-effecting allocator. Commit assigns event-scoped fresh tokens injectively and records the mapping.
- Identical fresh descriptors do not imply node identity. Node identity also never collapses merely because two nodes have equal outgoing pairs.
- All proposals are validated against one old snapshot before any mutation. In-place source-order rewiring is a different construction and is rejected.
- Every old node remains present in the raw successor. Projection occurs after the complete raw graph exists. A node may therefore fire and create raw descendants that are all subsequently dropped.
- Directed forward closure from the preserved root is the strict reference profile. A `KeepAll` graph evolution, if later evidenced, must be another explicit update construction rather than a boolean pruning flag.
- Breadth-first canonicalization belongs to equality/serialization and trace lowering. Execution may use opaque event-local tokens but must remain equivariant under alpha-renaming.
- Native graph traces are ragged sequences of typed graph snapshots and graph events. Dense adjacency padding, layout coordinates, node-count plots, and image frames are downstream.
- Random-network seeds require an explicit generation algorithm and random source. The book's frequency comments do not specify a canonical distribution and cannot define one.
- Effective dimension, layout, component counts, node counts, cycles, fixed points, periods, causal dependencies, and multiway branch diagrams are observers or relations. They never feed back unless another construction explicitly reads them.
- Parallel T29 always returns one `Advanced` result. Horizon, cancellation, resource limits, fixed/cycle observers, and errors remain separate.

## Big Picture Objective

Reconstruct Chapter 5 network systems as native deterministic evolution over mutable labeled connectivity. Pin down graph identity, root/component handling, port paths, exact-length topology signatures, closed reroute/create programs, simultaneous proposal evaluation, collision-free freshness, raw commit, directed projection, outcomes, canonical representations, seeds, variants, and exact conformance oracles. Determine the smallest honest extension of the shared source/read/result/update responsibilities while excluding coordinate embedding, fixed adjacency capacity, opaque whole-graph callbacks, hidden allocation, in-place rewiring, family dispatch, and guessed sequential semantics.

## Catalog Identity

- Stable ID: T29.
- Exact name: Network Systems.
- CSV provenance: `ref/notes/CA-Types.csv:30`; taxonomy provenance: `ref/notes/CA-Types.md:786-813`.
- Canonical section: Chapter 5, `Network Systems`, `BOOK:2368-2492`. T30 begins at `BOOK:2494` and T31 at `BOOK:2568`.
- Entry kind: deterministic graph-topology evolution construction with fixed two labeled outgoing ports, path rerouting, fresh-node creation, topology-conditioned rules, and root projection.
- Strict profiles: uniform path rerouting; one-step topology-conditioned reroute/create rules; depth-two exact-reach-signature rules.
- Related but distinct profile with unresolved source order: sequential network systems.
- Search vocabulary: network system(s), graph-based system(s), sequential network system(s), network evolution/substitution, node/connection/link, above/below, port, follow/path, reroute, insert/new node, connected/reachable/component/piece, first node/root, local structure, distinct node counts, graph isomorphism/layout/dimensionality, causal/Boolean/constraint/multiway/cluster/mobile networks, directed/undirected, random network, and the implementation symbols listed below.

## Search Log

1. Verified CSV line 30, read `ref/notes/CA-Types.md:786-813` in full, and treated it only as a vocabulary seed.
2. Read the complete Chapter 5 core `BOOK:2368-2492` and the clean split duplicate `CHAPTERS/5-Two-Dimensions-and-Beyond/Two-Dimensions-and-Beyond.md:219-323`. The split repairs local OCR/layout only; canonical provenance remains the monolith.
3. Exact `network system(s)` search found 44 occurrences on 40 monolith lines: 33/29 before the actual Index and 11/11 in the actual Index. The T29 main section contributes 19 occurrences on 18 lines; T29 Notes contribute 8 occurrences on 5 lines.
4. A conservative named-family vocabulary search found 290 occurrences on 217 lines: 216/160 before the Index and 74/57 in it. It covered graph-based and sequential network systems, network CA/Boolean/constraint/causal/substitution/space variants, directed/undirected networks, graph grammar/isomorphism/layout, and dimensionality.
5. The expanded boundary search for `network(s)` or `graph(s)` found 1,278 occurrences on 654 lines: 959/510 before the Index and 319/144 in it. Every candidate was classified as native evidence, a followed relation, a duplicate, or a false positive.
6. Searched executable symbols `CyclicNet`, `Follow[`, `NeighborNumbers`, `NetEvolveStep`/`NetEvolveStep1`, `ConnectedNodes`, `RenumberNodes`, `NetEvolveList`, and `NetCAStep`. There are 27 occurrences on 19 lines; 25/17 are native Notes evidence and the two later `NetCAStep` hits are non-native cross-references.
7. Inspected all local page-209 through page-218 rasters. They establish label-ignored static counts, layout nonuniqueness, path arrows, projection, new-node timing, the depth-one rule grammar, the five depth-two programs, and node-count series.
8. Checked the official Chapter 5 primary PDF, `https://files.wolframcdn.com/pub/www.wolframscience.com/nks/nks-ch5-sec5.pdf`, against the rasters and checked the official programs CDF, `https://www.wolframscience.com/nks/programs/NKSPrograms-05.cdf`, for complete rule tables and reference routines.
9. Read the complete native Notes neighborhood `BOOK:13814-13919`: graph representation, path following, projection, node creation, signature cases, exact rules/count sequences, sequential network systems, dimensionality, and fixed-topology network automata.
10. Followed supporting implementation/history/observer material at `BOOK:13642-13658`, `14275`, `14754`, `5658-6180`, `16312-16658`, and the Index routes listed in E27.
11. `BACK-MATTER/Index/Index.md:1715-1820` is actually a Notes duplicate and `BACK-MATTER/Notes/Notes.md` is unusable. The actual monolith Index begins near `BOOK:20826`; its split copy is interleaved under `BACK-MATTER/Colophon/Colophon.md:3383`. Actual routes were resolved against their destination passages.
12. Reconstructed all four page-214 uniform rules, both page-215 creating rules, the complete depth-one grammar/count, all five page-217/218 depth-two tables, short and long node-count anchors, and the six sequential table rows.
13. Independently generated all six depth-two key witnesses, the frozen-snapshot and directed-projection adversaries, freshness/alias adversaries, alpha-renaming checks, and the canonical five-node and singleton-seed trajectories.
14. Audited `simple_programs.md`, every top-level `src/ca` module relevant to support/read/rule/update/trace, and the tests. No current graph semantics were found.
15. All names, aliases, core figures, Notes, actual Index routes, splits, history, programs, rule counts, seeds, identity questions, observers, and relations are dispositioned. Parallel mechanics have zero unresolved candidates. The sequential source limitation is explicit and does not get silently resolved.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These 27 groups cover every unique construction-relevant passage; split duplicates are logged above.

### E01 — Connectivity replaces fixed geometry

- Provenance: `BOOK:2362-2384`, Chapter 5 transition and `Network Systems` opening.
- Fact: unlike arrays or free plane geometry, a network is specified by nodes and their connections; changing the drawing does not change the network.

### E02 — Two outgoing connections and reachable small-network counts

- Provenance: `BOOK:2386-2394`, page-209 caption.
- Fact: the section restricts each node to two outgoing connections and enumerates 1, 3, and 14 reachable connection patterns for one, two, and three nodes after ignoring labels. This is an enumeration quotient, not a runtime port-erasure rule.

### E03 — Arrays and trees encoded by connectivity

- Provenance: `BOOK:2396-2422`, pages 210-212.
- Fact: identical connectivity can be drawn differently, while regular arrays of arbitrary dimension, trees, and nested structures can all be encoded by connections. Dimension/layout are derived.

### E04 — Labeled path rerouting

- Provenance: `BOOK:2424-2446`, pages 213-214.
- Fact: a rule replaces the above and below connections of each node with endpoints reached by specified sequences of old labeled connections; the illustrations use a five-node cyclic seed.

### E05 — Simultaneous disconnection and first-piece projection

- Provenance: `BOOK:2440-2450`, page-214 caption.
- Fact: rerouting can split the graph. Subsequent displayed evolution keeps only the part connected in the directed reference sense to the first node.

### E06 — Fresh-node insertion

- Provenance: `BOOK:2452-2464`, page-215.
- Fact: each old node can insert a new node into an outgoing connection; the new node's two outgoing links are derived from the source's previous links, with preserved or swapped order.

### E07 — Local topology conditions

- Provenance: `BOOK:2464-2484`, pages 216-217.
- Fact: rule choice can depend first on whether the two immediate targets coincide and then on the number of distinct endpoints accessible at successive path lengths. This creates finite local case tables.

### E08 — Complex depth-two behavior

- Provenance: `BOOK:2484-2492`, page-218.
- Fact: simple closed local network rules produce complex node-count histories and repeated structures; these remain deterministic single-successor systems.

### E09 — Multiway boundary

- Provenance: `BOOK:2494-2562`, `Multiway Systems`.
- Fact: retaining every possible result from replacements creates a branching evolution graph. That successor algebra is T30, not a mode of T29.

### E10 — Notes graph representation and cyclic seed

- Provenance: `BOOK:13814-13846`.
- Fact: a finite network is represented by one ordered pair of target indices per node; `CyclicNet[n]` supplies the five-node reference seed and `Follow` folds a connection word from a node.

### E11 — Parallel evolution, projection, and renumbering

- Provenance: `BOOK:13848-13872`.
- Fact: `NetEvolveStep` computes all node results from the old list, then `ConnectedNodes` retains nodes reachable from node 1 and `RenumberNodes` produces a compact reference list. Node-creation rules allocate distinct appended nodes.

### E12 — Exact topology signatures and rule tables

- Provenance: `BOOK:13873-13887`.
- Fact: `NeighborNumbers` forms cardinalities of exact-length reachable endpoint sets. The Notes give the complete depth-two case set, five exact programs, node-count sequences, a binary-digit recurrence relation for one program, and long-time anchors.

### E13 — Sequential-network variant

- Provenance: `BOOK:13889-13903` and the official page-936 figure/program table.
- Fact: one active node is rewritten and may move along port 1 or 2; six table rows are given. The node-count plot evidences pruning, but the source does not fix movement against old versus rewritten links, projection anchor, or operation order.

### E14 — Network dimensionality

- Provenance: `BOOK:13905-13907`.
- Fact: growth in nodes reached at increasing distance can be used to estimate effective dimension. It is an observer.

### E15 — Cellular automata and Boolean systems on fixed networks

- Provenance: `BOOK:13909-13919`.
- Fact: values can evolve on an otherwise fixed connection graph, including Boolean-network profiles. This changes node values rather than T29 topology.

### E16 — Arbitrary fixed-graph cellular automata

- Provenance: `BOOK:13642-13658`.
- Fact: ordinary CA rules can be transported to fixed graphs with declared neighborhoods. This is a relation/compilation boundary, not evidence that T29 carries cell colors.

### E17 — Random-network seeds and statistical observations

- Provenance: `BOOK:14275` and `14754`.
- Fact: random initial networks and frequency statements are discussed, but no canonical seed distribution/algorithm sufficient for conformance is specified.

### E18 — Space as a network and derived layout/dimension

- Provenance: `BOOK:5658-5754`.
- Fact: networks can model space without embedding coordinates; apparent locality and dimensionality emerge from connectivity. Layout is representational.

### E19 — Constraint-defined networks

- Provenance: `BOOK:5756-5812`.
- Fact: networks can be selected by satisfying local/global constraints rather than advanced by a unique explicit reroute rule. This is T31.

### E20 — Causal networks

- Provenance: `BOOK:5814-5922`.
- Fact: event-dependency graphs can be derived from an evolution. They are trace observers unless a construction makes the causal graph itself state.

### E21 — Scheduling and multiway evolution

- Provenance: `BOOK:5924-6076`.
- Fact: different update orders can generate alternative histories and multiway graphs. T29 parallel timing is fixed and does not contain a scheduler.

### E22 — Cluster replacement on networks

- Provenance: `BOOK:6078-6180`.
- Fact: rules can replace whole local clusters and reconnect boundaries. This graph-grammar construction is broader than the per-node path/fresh grammar here.

### E23 — Notes on layout and dimensionality

- Provenance: `BOOK:16312-16353`.
- Fact: spring/electrical embeddings and distance-growth estimates visualize/analyze networks but do not determine their transition.

### E24 — Notes on constraints and causal graphs

- Provenance: `BOOK:16365-16400`.
- Fact: constraint solving and causal-network construction have distinct semantics and cannot be hidden inside a graph update callback.

### E25 — Multiway relation

- Provenance: `BOOK:16511-16519`.
- Fact: retaining alternative applications produces a graph of states/events; equality and merging of states are explicit multiway concerns.

### E26 — Cluster, grammar, mobile, and directed-network variants

- Provenance: `BOOK:16558-16658`.
- Fact: network grammars, substitution of clusters, network mobile automata, and directed/undirected profiles have different active objects and reconnection laws. They remain separate constructions.

### E27 — Actual Index routes

- Provenance: actual Index entries at `BOOK:20918`, `21092`, `21213`, `21229-21231`, `21654`, `21683`, `21899`, `22096`, and `22144`.
- Fact: routes for graph isomorphism/layout, network systems, causal and constraint networks, dimensionality, substitution/grammar, multiway evolution, and Boolean/CA-on-network variants all lead to passages dispositioned above.

## Construction Model

### Rooted two-port graph carrier

The strict state contract is:

```text
Port = Above | Below
PortWord = finite tuple[Port]              # epsilon is valid

RootedPortGraph = {
    vertices: FiniteNonEmptySet[VertexToken],
    root: VertexToken,
    next: TotalMap[(VertexToken, Port), VertexToken]
}

invariant:
    root in vertices
    every next target is in vertices
    every vertex is reachable from root by a finite PortWord
```

`VertexToken` distinguishes occurrences within a snapshot. It carries no arithmetic, spatial, or persistent user-visible meaning. Both ports may target the same vertex; either may self-loop; cycles, sharing, and arbitrary finite incoming degree are ordinary.

For graph `G`:

```text
follow(G, v, epsilon) = v
follow(G, v, p :: rest) = follow(G, next(v,p), rest)

R_k(G,v) = { follow(G,v,w) | w in Port^k }
signature_d(G,v) = (|R_1|, ..., |R_d|)
```

Words fold in written order. For example `21` means follow `Below` and then `Above`. The read layer exposes the declared path endpoint map and, when requested, the exact-length signature. It does not expose the entire graph through a callback.

The evidenced read profiles are:

```text
UniformNetworkRead:
    key(v) = Unit

ExactLengthReachCounts(depth=1):
    key set = {(1), (2)}

ExactLengthReachCounts(depth=2):
    key set = {
        (1,1), (1,2),
        (2,1), (2,2), (2,3), (2,4)
    }
```

Every depth-two key is realizable. More generally, `|R_(k+1)| <= 2|R_k|` is necessary but does not prove that an arbitrary tuple is realizable, and the book supplies no generic-depth table enumerator. The public program therefore carries an exact declared finite key set rather than synthesizing one from this inequality.

### Equality and exact canonical representation

Two states are semantically equal exactly when a bijection maps root to root and preserves both port targets. Node list order and raw tokens are ignored; distinct vertices are never merged.

For this carrier, canonicalization needs no general graph-isomorphism search:

1. enqueue the root and assign it canonical index 0;
2. dequeue in breadth-first order;
3. inspect `Above` then `Below`;
4. assign the next unused index at first encounter;
5. emit each canonical node's ordered pair of canonical targets.

Every node is reachable, so the process emits all nodes. A root/port-preserving isomorphism necessarily preserves discovery order, and equal canonical pair arrays construct such an isomorphism. The codec is therefore exact. An event retains both the raw-token-to-canonical map and any author/reference ordering; execution does not depend on either.

The static page-209 values `1,3,14` use a coarser label-ignored enumeration relation for `n=1,2,3`. It may be implemented as an observer but cannot replace strict equality.

### Closed program and typed results

The result grammar is finite data:

```text
OldEndpoint =
    DirectOld(path: PortWord)

FreshEndpoint =
    InsertFresh(
        above_old_path: PortWord,
        below_old_path: PortWord
    )

PortTargetExpr = DirectOld | InsertFresh

NodePortRewrite = {
    above: PortTargetExpr,
    below: PortTargetExpr
}

NetworkProbe =
    UniformNetworkRead
  | ExactLengthReachCounts(depth, exact_key_set)

PortRewriteProgram = {
    probe: NetworkProbe,
    referenced_paths: FiniteSet[PortWord],
    rows: TotalMap[probe.key, NodePortRewrite]
}
```

Each path in a direct or fresh descriptor is interpreted relative to the firing old vertex in the old graph. Each syntactic `InsertFresh` occurrence creates one distinct vertex. Thus a row with fresh expressions in both parent ports creates two vertices, even if the descriptors are textually equal. A fresh vertex's two ports can only target old endpoints under the evidenced grammar; nested fresh expressions, fresh-to-fresh references, supplied global node IDs, arbitrary subgraph values, and callbacks are invalid.

Program validation establishes:

- the probe and exact key set are well formed;
- every key has exactly one row and no undeclared row exists;
- every referenced path is a finite port word in the declared two-port alphabet;
- both outputs exist;
- every fresh descriptor supplies exactly two old path endpoints;
- row order is serialization only;
- no missing-row fallback, first-match behavior, or Mathematica unmatched-expression behavior leaks into semantics.

### All-node FRONTIER and graph UPDATE policy

`AllNetworkNodes` selects every old vertex exactly once. The selector may expose snapshot-scoped source handles in any order because commit is equivariant; a reference order may use the current Notes list. `PortPathRead` evaluates all declared endpoints and the probe key against the immutable old graph. The result lookup returns the one closed row for that key.

`ParallelRerouteCreateProject` commits in this order:

1. verify that there is exactly one proposal for every and only old vertex, and that its source, read, and result all belong to the same snapshot;
2. allocate one collision-free event-local token for every `InsertFresh` occurrence, injectively across the whole event;
3. retain every old vertex in a raw vertex set;
4. replace both ports of every old vertex from its proposal, resolving direct endpoints to old vertices and inserted endpoints to their allocated fresh vertices;
5. add each fresh vertex with both of its ports resolved to the firing source's old-snapshot path endpoints;
6. construct the complete raw graph; no newborn is selected or rewritten in this event;
7. compute directed forward closure from the preserved old root using the raw graph;
8. discard raw vertices outside that closure and retain the old root as successor root;
9. emit a graph event sufficient to reconstruct proposals, births, raw edges, retained/dropped sets, edge changes, and canonical renaming.

```text
ParallelPortGraphRewrite =
    SOURCE: AllNetworkNodes
    READ: PortPathRead
    RULE: PortRewriteProgram
    RESULT: NodePortRewrite
    UPDATE: ParallelRerouteCreateProject
```

This typed graph UPDATE policy is not fixed-support assignment: edges and support both change. It is not T13 concatenation or T27 bag expansion: old nodes survive, their topology mutates, and only some result occurrences create children. It is not T20 tree replacement: sharing and cycles are native. Those differences justify the graph policy and its validators inside the common runner, not a seventh executor or top-level semantic class. Proposal validation, lineage, token allocation, and immutable-snapshot utilities may be shared.

### Why post-commit root projection is exact

Let `C` be the old forward-reachable class of a firing source. Every `DirectOld(path)` ends in `C`. Every fresh node created by that source targets only vertices in `C`, and its only incoming reference is installed by a source in `C`. No row can refer to a vertex outside the source's old class or to a dropped token by name.

Consequently, after a raw successor disconnects vertices from the root, no future application of this parallel grammar to the retained class can reconnect those discarded vertices. Projecting after each event produces the same retained future as evolving the raw graph and observing only the root class. This justifies the Notes projection for this strict grammar without turning garbage collection into a general graph-runtime default.

### Outcome and trace semantics

Every valid strict graph/program pair returns:

```text
StepResult(
    successors = {retained_rooted_port_graph},
    outcome = Advanced(changed = not Isomorphic(old, retained)),
    event = NetworkRewriteEvent(...),
)
```

An applicable identity or isomorphic successor remains an event with `changed=false`. There is no base `NoMatch`, halt, boundary, or capacity outcome because the table is total and every nonempty state has sources. A vertex can fire and create raw descendants and then be dropped in the same event. The root always survives, so the strict state never becomes empty.

`NetworkRewriteEvent` records at least:

```text
snapshot_id
old_root
per_old_node {
    source_token
    probe_key
    path_endpoint_map
    selected_row_key
    result
}
fresh_births {
    token
    source_token
    parent_port
    insertion_ordinal
    above_old_target
    below_old_target
}
raw_vertex_set
raw_port_pairs
retained_vertex_set
dropped_vertex_set
old_edge_changes
raw_to_canonical_vertex_map
```

The event plus old snapshot must reconstruct the raw graph exactly; the retained set and canonical map must reconstruct the successor. Optional policies may stop on a literal/isomorphic fixed point, a repeated canonical state, a node-count predicate, a horizon, resource exhaustion, or cancellation. They report their own reason without rewriting the transition. Layouts, adjacency matrices, node counts, dimensions, causal graphs, images, and padded batches are downstream projections of the raw typed trace.

## Exact Book Presets and Oracles

### Uniform path-rerouting rules

The Notes reference seed is:

```text
G0 = {{5,2}, {1,3}, {2,4}, {3,5}, {4,1}}
root = 1
```

Using port words `1=Above`, `2=Below` and result order `[Above,Below]`, the four page-214 rows are:

```text
a: [DirectOld(21),      DirectOld(2)]
b: [DirectOld(11),      DirectOld(2)]
c: [DirectOld(epsilon), DirectOld(2)]
d: [DirectOld(epsilon), DirectOld(1)]
```

With root/port-preserving canonical equality:

- (a) returns to `G0` after 5 events and has no earlier repeat;
- (b) returns after 4 events and has no earlier repeat;
- (c) reaches the directed five-cycle `{{1,2},{2,3},{3,4},{4,5},{5,1}}` after one event and is then fixed;
- (d) has node counts `5,5,1`; at event 2 its retained state is `{{1,1}}` and remains fixed.

These distinguish written path order, port order, old-snapshot reads, directed projection, and exact isomorphism equality.

### Node-creating singleton rules

Both page-215 presets start from `{{1,1}}` and rewrite the parent above port to a fresh node while leaving its below port direct:

```text
a: [InsertFresh(1,2), DirectOld(2)]
b: [InsertFresh(2,1), DirectOld(2)]
```

Both have node counts `1,2,4,8,...`. In the Notes append-reference order:

```text
case a:
  G1 = {{2,1}, {1,1}}
  G2 = {{3,1}, {4,1}, {2,1}, {1,1}}

case b:
  G1 = {{2,1}, {1,1}}
  G2 = {{3,1}, {4,1}, {1,2}, {1,1}}
```

The picture lays nodes out next to their parents, so picture order differs from append order. Only lineage and graph isomorphism may reconcile them.

### Restricted depth-one grammar and exact count

For the page-216 profile, every path endpoint is one old step (`1` or `2`). A parent-port expression is one of:

```text
DirectOld(1)
DirectOld(2)
InsertFresh(1,1)
InsertFresh(1,2)
InsertFresh(2,1)
InsertFresh(2,2)
```

There are 6 expressions for each of two parent ports, hence 36 node actions. The probe has two keys, `(1)` and `(2)`, so a complete rule table count is `36^2 = 1296`.

This count must not be extrapolated to `36^6` for depth two. Pages 217-218 use epsilon and length-two paths; the book supplies neither a finite sampling alphabet/distribution nor a complete depth-two enumeration/count. With arbitrary finite paths, the grammar is countably infinite.

### Five exact depth-two programs

Notation `N(a,b)` means `InsertFresh(a,b)`; an unwrapped word means `DirectOld(word)`. Keys are exact-length signatures.

```text
program a
  11 -> [1, N(21,21)]
  12 -> [N(epsilon,11), N(11,epsilon)]
  21 -> [N(epsilon,epsilon), N(1,21)]
  22 -> [N(11,21), N(2,21)]
  23 -> [N(epsilon,epsilon), 2]
  24 -> [N(22,epsilon), epsilon]

program b
  11 -> [N(epsilon,11), 2]
  12 -> [2, N(epsilon,epsilon)]
  21 -> [21, N(epsilon,1)]
  22 -> [N(2,1), epsilon]
  23 -> [12, 2]
  24 -> [N(1,1), 21]

program c
  11 -> [N(11,1), 2]
  12 -> [N(12,2), N(22,epsilon)]
  21 -> [N(22,2), N(1,epsilon)]
  22 -> [N(1,1), N(21,11)]
  23 -> [21, 2]
  24 -> [N(1,12), N(12,epsilon)]

program d
  11 -> [N(12,12), epsilon]
  12 -> [22, N(1,1)]
  21 -> [1, N(epsilon,2)]
  22 -> [12, 21]
  23 -> [N(21,2), 1]
  24 -> [1, 11]

program e
  11 -> [epsilon, N(11,12)]
  12 -> [N(epsilon,1), N(11,12)]
  21 -> [2, epsilon]
  22 -> [N(21,1), N(11,2)]
  23 -> [22, 2]
  24 -> [21, 2]
```

Starting from the one-node graph, node counts for events 0 through 15 are:

```text
a: 1,2,6,10,6,4,8,13,9,12,6,10,15,11,14,8
b: 1,2,4,4,6,8,11,16,17,16,16,13,12,11,8,8
c: 1,2,6,18,28,8,14,18,21,22,28,29,25,26,35,36
d: 1,2,3,3,6,9,4,8,10,17,22,29,30,38,56,46
e: 1,2,6,12,12,11,12,12,11,15,12,12,11,11,19,18
```

Long-run guards are:

```text
d: n100=205, n500=262, n1000=190, n2500=292,
   n10000=163, n50000=214
e: n100=55, n500=145, n1000=262, n2500=538, n5000=1101
```

For program (b), represented state `G49 = G768`, giving period 719 after the prefix. Program (c)'s node-count relation to binary digits supplies an independent observer oracle but does not replace graph-state comparison.

### Minimal signature witnesses

Using zero-based pair arrays and root 0, these graphs realize every depth-two key:

```text
(1,1): ((0,0),)
(1,2): ((1,1),(0,1))
(2,1): ((1,2),(0,0),(0,0))
(2,2): ((0,1),(0,0))
(2,3): ((0,1),(0,2),(0,0))
(2,4): ((0,1),(2,3),(0,0),(0,0))
```

They guard exact-length rather than cumulative reach counts, sharing, and alias preservation.

### Adversarial semantic oracles

1. **Written path order.** Choose a graph whose root has `A=1,B=2` with `A(1)=3` and `A(2)=2`. `BA` ends at 2 while `AA` ends at 3; reversed-word evaluation fails.
2. **Frozen snapshot.** Under uniform rule (a), `t0=((1,1),(0,0))` must become `t1=((0,1),(1,0))`. In-place source order incorrectly produces `((0,1),(0,0))`.
3. **Directed projection.** Under rule (d), `t0=((0,1),(0,0))` has raw successor `((0,0),(1,0))`. Node 1 fired, but only the root singleton is retained even though the raw graph is weakly connected.
4. **Fresh occurrence identity.** A singleton row with both parent ports equal to `InsertFresh(epsilon,epsilon)` produces raw graph `((1,2),(0,0),(0,0))` with 3 nodes, not 2. Reapplying produces 9 raw nodes before projection.
5. **No structural deduplication.** Two nonroot nodes may have equal outgoing pairs or be automorphic. The root can still have signature `(2)`; merging them changes future rules.
6. **Newborn deferral.** Raw count equals old count plus the number of syntactic insertion occurrences across old-node proposals; it does not recursively expand newborns.
7. **Alpha equivariance.** Arbitrarily rename all old tokens and root consistently. The successor must be isomorphic, and event lineage must transform equivariantly.
8. **Root and port preservation.** Moving the root or swapping only one port pair generally changes state, even if an unlabeled drawing looks identical.
9. **Identity event.** `[epsilon,epsilon]` on the singleton returns `Advanced(changed=false)`, not terminal/quiescent/no-event.
10. **Provenance reconstruction.** Applying the recorded proposals and birth mapping to the recorded old graph must reconstruct the raw graph exactly; projecting the recorded retained set must reconstruct the successor.
11. **Validation.** Reject a dangling target, missing root, empty graph, unreachable seed node, incomplete/duplicate table, undeclared key, invalid port symbol, malformed path, read from another snapshot, missing/extra old-node proposal, reused fresh token, fresh-to-fresh target, and mismatched root projection.

## Sequential Network Variant: Evidence Boundary

The Notes give this exact table, where each row returns `(rewrite, move_port)`:

```text
11 -> ([N(epsilon,11), 2], 2)
12 -> ([22, N(epsilon,22)], 2)
21 -> ([epsilon, 22], 2)
22 -> ([12, N(1,2)], 1)
23 -> ([N(12,1), N(2,21)], 2)
24 -> ([N(22,epsilon), 1], 1)
```

The prose says one active node is operated on and can then move along its above or below connection. The official CDF contains the six rows but no evaluator. The official node-count plot repeatedly drops sharply; because these rows only reroute/insert, it independently evidences some reachability garbage collection.

The primary sources do **not** determine:

- whether movement follows the old active node's selected port or its committed rewritten port;
- whether movement occurs before or after graph projection;
- whether projection is rooted at a persistent original root, the pre-move active node, the post-move active node, or another anchor;
- whether pruning precedes or follows active-token relocation.

The ambiguity changes behavior immediately. In the `(1,2)` row, the below port becomes a fresh node and the move is `Below`: old-edge timing moves to the old below target, while committed-edge timing moves to the newborn. Figures lack IDs and stepwise data needed to decide.

Goal 2 must therefore expose no guessed sequential executor and no convenience timing flag. It may define the inert evidence schema:

```text
SequentialPortGraphState = {
    graph: RootedPortGraph,
    active: VertexToken,
    projection_anchor: UnresolvedBySource
}
```

and mark `sequential_network_system` unavailable with a precise source-gap assertion until a primary evaluator or decisive trajectory is acquired. If a convention is ever added for research, it must be named as a convention and cannot claim book conformance.

## Variants, Relations, and Boundaries

- **Strict parallel uniform/depth-one/depth-two profiles:** native T29 programs sharing the same graph update.
- **Sequential network systems:** evidenced rule family, but transition order/anchor is underdetermined as above.
- **Keep-all raw evolution:** useful diagnostic/reference relation, not the canonical retained state and not an update flag.
- **Infinite arrays and trees represented as networks:** static/generative examples; the strict evolving carrier here is finite after each event.
- **Random networks:** seed family requiring an explicit distribution/algorithm absent from the direct evidence.
- **Network layout and effective dimension:** codecs/observers.
- **Cellular automata and Boolean networks on a fixed graph:** node-value evolution on immutable topology, distinct from T29 edge evolution.
- **Undirected trivalent Chapter 9 space networks:** different carrier/degree/rewrite rules.
- **Local constraint systems:** T31 chooses satisfying configurations rather than applying one total local next-state map.
- **Causal networks:** derived event-dependency graphs.
- **Multiway systems:** T30 returns a set of alternative successor states and explicitly merges equality classes.
- **Cluster/network substitution grammars:** replace subgraphs and reconnect boundaries; the per-node path/fresh result algebra cannot express them.
- **Network mobile automata:** add visible active-node control and sequential locality under separately evidenced timing.
- **Pointers, linked lists, LISP, and circuits:** analogies/representations, not alternate T29 state encodings.
- **Random-complexity frequency claims:** the main text's roughly one in 10,000 and the Notes' few in 1,000 use unspecified samples/criteria; neither is a conformance distribution.

## Corrected Architecture and Goal 2 Handoff

T29 is a discrete `t+0D` SimpleProgram whose configuration has rooted two-port graph support/topology. FRONTIER selects old vertices, NEIGHBORHOOD evaluates declared port paths/reach views on the frozen graph, RULE returns direct/fresh reroute replacements, and a graph-capable UPDATE allocates vertices, rewires ports, and applies directed-root projection atomically. Fresh support proves fixed-label assignment alone is insufficient, but it justifies an UPDATE-axis implementation—not a network executor.

Revised G2-T29 adds graph configuration/codec schemas, vertex loci, port-path access, typed direct/fresh replacements, and graph create/rewire/project UPDATE inside the branch-free runner. It removes seventh-law/executor and whole-graph-value prohibition framing while retaining root/port identity, cycles/sharing, freshness, projection order, alpha-equivalence, provenance, and the explicit sequential evidence boundary.

The historical API/handoff below remains evidence provenance; this section governs its executor/class classification.

## Historical Current API Fit (Superseded by Architecture Audit)

| T29 responsibility | Current proposal fit | Required conclusion |
|---|---|---|
| State/support | Dense `D -> A` over fixed rank-0..3 coordinates | SEMANTIC MISMATCH; add finite rooted labeled topology |
| Vertex identity | Coordinate tuple | SEMANTIC MISMATCH; use alpha-renamable snapshot tokens |
| Root/control anchor | No graph root; single-position control exists only in prior design | PRINCIPLED EXTENSION; graph root is state, not mobile control |
| Source | Writable coordinate frontier | SEMANTIC MISMATCH; every old vertex fires exactly once |
| Read | Fixed coordinate offsets | SEMANTIC MISMATCH; old-snapshot labeled path endpoints and exact-reach signatures |
| Rule | Scalar table/formula result | SEMANTIC MISMATCH; closed total port-rewrite/create table |
| Result | Same-site scalar assignment | SEMANTIC MISMATCH; two port expressions with typed fresh-node occurrences |
| Update | Fixed-support copy/parallel write | SEMANTIC MISMATCH; raw graph rewrite, allocation, and root projection |
| Boundary | Fixed/periodic/reflective coordinate edges | NOT APPLICABLE; graph is internally closed |
| Equality | Dense array equality | SEMANTIC MISMATCH; exact root/port-preserving isomorphism |
| Trace | Fixed dense frame | SEMANTIC MISMATCH; ragged graph snapshots plus raw/projection events |
| Orchestration | Old-source/read/result/update responsibilities | DIRECT at the responsibility level |
| Program/seed/horizon separation | Separate configuration responsibilities | DIRECT; keep graph seed and external stop independent |

The current proposal's `FORMULAIC` escape would merely hide graph traversal, mutation, and allocation in a callback. T20 trees preserve hierarchy but not graph sharing/cycles; T27 bags preserve identity/multiplicity but not adjacency; neither is a native substitute.

## Historical Current Runtime Fit (Superseded by Architecture Audit)

| Runtime area | Finding | T29 disposition |
|---|---|---|
| `alphabets.py` | Finite scalar integer/float/symbol values | Cannot represent graph topology or vertex references |
| `loci.py:31-94` | Rank-0..3 integer coordinates and predicate loci | Cannot address alpha-renamable graph vertices |
| `frontiers.py:38-80` | Only dense time-slice firing | Wrong support/source contract |
| `neighborhoods.py:46-80` | Coordinate offset gathers/callables | No port-word traversal or topology signatures |
| `rules.py:30-78` | Scalar results, named families, callable rule | Reject callback escape; add closed graph row data |
| `specs.py:23-82` | Fixed shape and raw family/rule payloads | Cannot validate rooted graphs or graph programs |
| `rollout.py:40-175,580-660` | Dense preallocation, copy-forward, and family branches | No graph execution; do not add a network branch |
| `datasets.py:321-330` | Stacks equal-shaped arrays | Graph episodes require explicit ragged collation |
| visualization | Coordinate/raster assumptions | Layout is an optional downstream graph renderer |
| tests | No graph carrier/update/isomorphism coverage | Add structural goldens before image tests |

`simple_programs.md:31-73` and `64-77` define coordinate loci and callback-like rules; `37-80` defines coordinate frontiers; `23-81` and the later rollout sections assume fixed dense shapes. These are semantic mismatches, not missing adapters.

## Historical Principles Audit (Superseded by Architecture Audit)

- **Principle 0:** connectivity, root, port order, aliasing, and freshness must survive. A drawing, adjacency image, or encoded scalar fails native advancement.
- **Principles 1-4:** graph state, all-node sources, path/signature reads, closed results, simultaneous raw commit, projection, and event provenance are explicit.
- **Principle 5:** the strict state is Markovian. Fresh allocation is event-local; list IDs and lineage do not become hidden rule state.
- **Principles 6-8:** vertex tokens, graph ports, display numbers, layouts, canonical indices, ANKoS addresses, and batch slots are separate domains. No capacity enters semantics.
- **Principles 9-10:** page rules are strict presets over typed paths/tables rather than named executors.
- **Principle 11:** frozen proposals, distinct insertion occurrences, newborn deferral, and post-commit directed projection are defining semantics; traversal caches and token choices are incidental.
- **Principle 12:** raw ragged graph traces precede canonical pair arrays, adjacency matrices, layouts, node-count series, causal graphs, and batching.
- **Principles 13-15:** written path order, in-place rewiring, weak versus directed projection, aliasing, duplicate fresh descriptors, and alpha-renaming are adversarial tests.
- **Principles 16-17:** `ParallelRerouteCreateProject` is a real seventh update sibling. Reusing tree/bag/assignment names without topology semantics would be a shim.

Rejected shortcuts:

- coordinate layout, fixed lattice, adjacency raster/tensor, padded maximum-node matrix, or whole graph packed into one value;
- arbitrary graph/rewrite/traversal/isomorphism callback, NetworkX as the semantic engine, or named network rollout branch;
- persistent global node counter, rule-visible list index, hidden root, hidden component filter, or hidden path cache;
- in-place/source-order rewiring, newborn firing, deletion before raw commit, weak/undirected projection, or silent keep-all behavior;
- structural node deduplication, automorphism quotient of vertices, bisimulation collapse, edge-label erasure, or root erasure;
- path reversal, unordered ports, cumulative-ball signature substituted for exact-length sets, missing-row fallback, or invented generic-depth count;
- random graph sampler/distribution inferred from frequency prose;
- guessed sequential move/projection timing or an `old/new` convention flag;
- T20 tree replacement, T27 bag expansion, or fixed-support assignment relabeled as graph evolution.

## Historical Detailed Implementation Plan (Superseded by Architecture Audit)

1. Closed exact-name, family/alias, broad graph, mechanism, caption/raster, Notes, executable-symbol, actual Index, split, history, layout/dimension, fixed-network, constraint, causal, multiway, grammar, mobile, random-seed, and relation searches.
2. Reconstructed the finite rooted two-port graph, exact isomorphism, BFS canonical codec, old-snapshot path reads, exact-length signatures, complete programs, fresh-node result grammar, all-node source, raw commit, and directed projection.
3. Proved projection is a correct factor for the strict grammar and separated it from a hypothetical keep-all update.
4. Recovered the four uniform rules, two creating rules, depth-one `1296` count, five complete depth-two tables, short/long count anchors, and exact repeated-state witness.
5. Derived all six depth-two key witnesses and adversarial path-order, frozen-update, directed-GC, freshness, alias, alpha, identity, provenance, and validation tests.
6. Audited the sequential variant independently and recorded the source gap without contaminating the complete parallel construction.
7. Compared every responsibility with prior stages, `simple_programs.md`, the runtime, and tests; established a seventh update law without reopening earlier conclusions.
8. Reintegrated the global plan/evidence/design ledgers and prepared an implementation-ready Goal 2 stage for the closed parallel profile.

## Historical Goal 2 Implementation Stage (Superseded by Corrected Handoff)

### G2-T29 — Rooted two-port graphs and parallel reroute/create/project

Dependencies: shared typed outcomes/errors and source/read/result/update orchestration; T13/T27 parent-child provenance concepts; an immutable snapshot/proposal validator. Do not depend on coordinate loci, T20 expression trees, T27 geometric bags, NetworkX semantics, or a graph callback.

1. Add `src/ca/graphs.py` or the synthesis-selected graph-owned module with `Port`, normalized `PortWord`, immutable `RootedPortGraph`, validation, `follow`, directed closure, exact-length reach signatures, exact BFS canonicalization, serialization, hashing, and alpha-renaming helpers.
2. Add `UniformNetworkRead` and `ExactLengthReachCounts` with explicit evidenced key domains. Reads return closed path endpoint maps/signatures and retain snapshot identity.
3. Add `DirectOld`, `InsertFresh`, `NodePortRewrite`, and `PortRewriteProgram`. Validate total rows, key/path closure, port order, result shape, and the restriction to old-snapshot fresh targets.
4. Add `AllNetworkNodes` and `PortPathRead` through the shared executor shell. No graph object or traversal function is passed to user code.
5. Add `ParallelRerouteCreateProject` with exact old coverage, event-scoped fresh allocation, frozen proposal resolution, raw graph construction, newborn deferral, directed root closure, and complete graph provenance. Add no family dispatch.
6. Add `Advanced(changed=...)` graph outcomes and raw ragged graph traces. Keep canonical pair-array, Notes list order, node-count series, layout, adjacency, dimension, cycle/fixed observers, and batching downstream.
7. Add strict constructors for the five-node cyclic seed, singleton seed, four uniform rules, two creation rules, depth-one profile, and five depth-two tables. Preserve program/seed/horizon separation.
8. Add a diagnostic keep-all raw graph projection only as event inspection, not a semantic successor option. Do not expose a pruning flag.
9. Represent the sequential six-row table as evidence data if useful, but make its executor unavailable with a precise source-gap diagnostic. Add no guessed convention or timing switch.
10. Audit exports, specs, serialization, dataset collation, rendering, and production code for callbacks, coordinate packing, padding/caps, hidden IDs/root/GC, in-place mutation, deduplication, port erasure, missing-row fallback, and family branches.

Completion requires:

- graph validation, alpha-renaming, port/root-preserving equality, BFS canonical round-trip, alias/cycle/self-loop, and malformed graph tests;
- `Follow` epsilon/written-order tests and all six depth-two signature witnesses;
- page-214 period 5/4, fixed-after-one, and `5,5,1` collapse goldens;
- page-215 `1,2,4,8` and exact first-two reference snapshots;
- page-216 grammar cardinality `1296` without invented depth-two count;
- all five depth-two tables, counts through event 15, long anchors, and `G49=G768`;
- frozen-snapshot, directed-projection, duplicate-fresh, newborn, alias, identity, exact raw-count, event-reconstruction, and validation adversaries;
- raw ragged trace followed by explicit pair-array/layout/count lowering;
- an explicit sequential-unavailable test documenting the unresolved source order;
- unchanged prior construction semantics, one shared executor shell, no network rollout branch, and all repository tests passing.

## Historical No-Cheating Checks (Superseded where they prohibit transparent graph schemas)

- No network family rollout, whole-graph successor/rewrite/traversal/isomorphism callback, host graph engine, or `Any` graph/result payload.
- No coordinate, drawing, lattice, tree, bag, adjacency image, padded tensor, scalar code, string, or fixed-capacity substitute for native graph topology.
- No hidden root, port order, source order, list index, node counter, allocation cursor, path cache, projection, or persistent lineage.
- No in-place rewiring, partial commit, newborn firing, descriptor coalescing, weak-component pruning, pre-rewrite pruning, or direct deletion.
- No node dedupe by equal edges, automorphism, bisimulation, layout, or hash collision.
- No missing/duplicate rule fallback, implicit identity row, reversed path, cumulative reach count, or invented generic rule enumeration.
- No graph size, degree padding, path-depth cap beyond the declared program, layout extent, observation window, or render limit as semantics.
- No random seed/distribution inferred from qualitative frequency claims.
- No sequential convention, keep-all switch, fixed-point stop, cycle cache, dimension estimator, causal graph, or node-count observer feeding execution.
- No T20 tree update, T27 occurrence-bag update, T13 concatenation, or dense assignment relabeled as graph rewrite.

## Completion Requirements

- [x] All names, aliases, figures, Notes, executable programs, actual Index entries, splits, history, variants, observers, and relations are resolved with zero silent remainder.
- [x] Native rooted graph/port state, equality, paths, signatures, source/read/result/update, freshness, raw commit, projection, seed, successor, and trace semantics are reconstructed.
- [x] Exact uniform/creation/depth-one/depth-two tables, counts, trajectories, signature witnesses, and adversarial invariants are specified.
- [x] Parallel mechanics are closed; the sequential source ambiguity is explicitly isolated rather than guessed.
- [x] Current API/runtime/principles fit and T20/T27 reuse/divergence are explicit.
- [x] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Architecture-Reclosed Stage Result

**COMPLETE.** T29 uses a discrete `t+0D` DOMAIN with rooted graph configuration support/topology, vertex firing loci, port-path/reach access, typed fresh/direct graph writes, and graph UPDATE in the common runner. Fresh identity and incidence justify the UPDATE policy, not a network executor; only the unresolved sequential schedule/profile remains deferred.

## Historical Stage Results (Evidence Retained; Architecture Superseded)

T29 is complete. The direct name audit dispositioned 44 occurrences on 40 lines; the conservative family audit dispositioned 290/217, the expanded graph/network audit 1,278/654, and the executable-symbol audit 27/19. Twenty-seven canonical excerpt groups cover the main mechanics, every page-209 through page-218 figure, Notes and programs, actual Index/splits, identity/layout/dimension, fixed-network systems, constraints, causal/multiway/grammar/mobile relations, random seeds, and history. Zero parallel-mechanics candidates remain.

The construction is a finite nonempty root-reachable directed graph with two semantic outgoing ports per vertex. Every old vertex follows closed paths and chooses a total topology-signature row against one old snapshot. One atomic update retains old vertices, reroutes both ports, allocates a distinct node per fresh expression, installs newborn ports to old endpoints, forms the raw graph, and projects directed forward closure from the preserved root. Exact root/port isomorphism has a simple BFS canonical codec. This establishes `ParallelRerouteCreateProject` as the seventh update sibling.

Uniform periods/collapse, singleton creation, the `1296` restricted count, five exact depth-two tables, short and long count anchors, `G49=G768`, all signature witnesses, and adversarial snapshot/projection/freshness/alias/provenance cases close the parallel handoff. The sequential table is preserved, and its pruning is evidenced, but move timing and projection anchor/order remain a transparent primary-source limitation. Goal 2 must not guess them.

## Historical Integration Results (Superseded by Architecture Audit)

- Added finite rooted labeled graph state, alpha-renamable vertex identity, exact root/port isomorphism, and BFS canonical serialization to the semantic inventory.
- Added all-vertex sources, port-word reads, exact-length topology signatures, closed reroute/create results, collision-free event freshness, and raw graph provenance.
- Added `ParallelRerouteCreateProject` as the seventh public update law with post-commit directed root projection.
- Separated semantic state from Notes/display indices, layouts, adjacency encodings, node counts, dimensions, causal graphs, and compressed traces.
- Isolated the sequential variant behind a source-acquisition gate and preserved its exact six-row table without a convention flag.
- Preserved T01/T09/T12/T13/T16/T17/T19/T20/T27 conclusions; no prior stage is reopened.
- Next stage: T30, Multiway Systems.
