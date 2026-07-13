# 11-T29-NETWORK

Status: **COMPLETE**

## Current Facts

- Exact catalog row: T29, CSV line 30, `Network Systems`; taxonomy seed `ref/notes/CA-Types.md:786-813`. The taxonomy supplied search vocabulary only.
- The Chapter 5 construction removes fixed geometric support. Native state is a finite nonempty directed graph with one distinguished root and exactly two distinguished outgoing ports per node, conventionally `above/below` or `1/2`. Drawing coordinates, wire routes, and node display numbers are not state.
- Self-loops, cycles, two ports sharing one target, distinct nodes with identical local structure, and arbitrarily many incoming edges are all native. Every retained node is forward-reachable from the root.
- Port labels and the root are semantic. The page-209 count of label-ignored reachable networks is a static enumeration observer, not the runtime equality law.
- Semantic equality is root- and port-preserving vertex isomorphism. It never merges automorphic, bisimilar, or locally indistinguishable nodes.
- An exact canonical serialization is available: breadth-first discovery from the root, visiting port `above` before `below`, and assigning integers on first discovery. For finite root-reachable deterministic two-port graphs this codec is an exact isomorphism canonicalizer, not a heuristic graph layout.
- A path read is a finite word over ports, including epsilon. It folds left-to-right through one immutable old graph; epsilon returns the source node.
- The local signature used by the contextual rules is a tuple of cardinalities of exact-length endpoint sets, not cumulative metric balls. For depth two the complete evidenced key domain is `(1,1),(1,2),(2,1),(2,2),(2,3),(2,4)`.
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
- Fixed-topology cellular automata and Boolean networks, undirected trivalent space networks, cluster substitution, network mobile automata, causal networks, multiway evolution, and constraint-defined networks are related constructions, not switches on the T29 parallel executor.
- T29 is the first catalog row whose Markov state contains mutable cyclic topology. T20 ordered trees cannot preserve arbitrary sharing/cycles, and T27 occurrence bags have no adjacency.
- The current runtime contains no graph carrier, graph selector, port-path read, fresh-node effect, graph commit, isomorphism codec, or ragged graph trace. A seventh update law is required.

## Updated Assumptions

- `RootedPortGraph` is finite, nonempty, and internally closed. Every node has exactly one target for each of the two ports, and every node is directed-forward-reachable from the root.
- Semantic vertex tokens are occurrence identities local to a snapshot. They support aliasing and cycles but are alpha-renamable. Integers emitted by the reference codec are not rule-visible identities.
- Ports are ordered as `Above=1` then `Below=2` for path syntax and canonical traversal. Erasing or swapping the port order changes a graph unless an explicitly separate relation proves an isomorphism.
- A path word is closed structural data, never a traversal callback. Its endpoint is evaluated only in the old graph and remains valid during proposal construction.
- For depth `d`, `R_k(v)` is the set of endpoints of all port words of exactly length `k` from `v`. The contextual read is `(|R_1|,...,|R_d|)`. The necessary bound `|R_(k+1)| <= 2|R_k|` does not define a complete generic key domain.
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

