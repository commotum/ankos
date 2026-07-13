# 11-T29-NETWORK

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T29, CSV line 30, `Network Systems`; taxonomy seed `ref/notes/CA-Types.md:786-813`. The taxonomy supplies vocabulary only.
- The Chapter 5 construction removes fixed geometric support: native state is a finite directed connection pattern, while every drawing position and wire route is visualization only (`BOOK:2368-2384`).
- The section's strict carrier gives every node exactly two outgoing connections. The two ports are distinguished as `above` and `below`, or labels `1` and `2`; each may target any node, including its source (`BOOK:2384-2388`, `2436-2446`).
- Initial enumeration counts inequivalent connection patterns while ignoring labels and excludes unreachable nodes. This creates separate questions about semantic equality, presentation canonicalization, and the distinguished root/component projection (`BOOK:2386-2392`).
- The same connection pattern can be drawn in visibly different ways, and connectivity can encode arrays of any dimension, trees, or nested structure. Layout coordinates and inferred dimension are therefore representations/observers, not Markov state (`BOOK:2394-2422`).
- Basic rules reroute each old node's labeled outgoing connections using labeled paths in the old graph. The page-214 examples establish old-snapshot path composition, simultaneous per-node rewiring, port preservation, and possible disconnection (`BOOK:2424-2446`).
- The remainder of the section tracks only the component containing the first displayed node after rules split a graph. Whether this is native rooted-state semantics or an explicit reference projection must be resolved from Notes/implementation evidence.
- Node-creating rules insert one fresh node into the above connection from every old node. Each fresh node's outgoing targets are derived from the source node's old outgoing connections, with either preserved or swapped port order; newborns must not fire in their birth event (`BOOK:2448-2460`).
- Contextual rules can choose different operations according to local topology: first whether two one-step targets coincide, then the number of distinct nodes reached by labeled paths of length up to two (`BOOK:2460-2482`).
- The strict section remains deterministic and single-successor in time. T30 begins where all possible states are retained; T31 begins where networks/configurations are found by constraints rather than an explicit next-state rule.
- T20 ordered trees cannot represent general cycles/sharing, and T27 occurrence bags have no adjacency. T29 is the first direct challenge requiring mutable first-class graph topology and path-relative reads.

## Updated Assumptions

- Node display indices, line positions, coordinates, edge curvature, above/below page placement, and graph-layout choices are nonsemantic. Port labels `1/2` are semantic even when the Index counts an unlabeled quotient.
- Native nodes require occurrence identity within a snapshot so multiple ports can share a target and cycles/self-loops survive. Whether whole-state equality is literal up to token renaming, rooted isomorphism, or another declared quotient remains under audit.
- Path expressions must traverse the same immutable old graph used by every node's rule. Rerouting in place would make enumeration order semantic and is provisionally rejected.
- Fresh-node allocation must be a typed graph-update effect with collision-free event-scoped identity and explicit lineage, never a hidden global counter exposed to rules.
- Dropping disconnected components must not be silently fused with local rerouting until book implementation proves that the distinguished root/projection is part of the construction rather than figure preparation.
- Fixed out-degree two is the evidenced Chapter 5 profile, not a claim that arbitrary networks universally have two ports.
- Effective dimension, shortest-path growth, connected components, graph drawing, node-count plots, causal networks, network constraints, and isomorphism canonicalization are observers, relations, or algorithms unless direct transition evidence says otherwise.

## Big Picture Objective

Reconstruct Chapter 5 network systems as native deterministic evolution over mutable labeled connectivity. Resolve graph identity, roots/component handling, path-relative old-state reads, rerouting, fresh-node insertion, local topological conditions, synchronous commit, outcomes, seeds, rule encodings/counts, and representations. Determine the smallest honest reuse of the existing source/read/result/update responsibilities while excluding coordinate embedding, adjacency matrices in fixed fake capacity, opaque whole-graph callbacks, hidden allocation, in-place rewiring, and family dispatch.

## Catalog Identity

- Stable ID: T29.
- Exact name: Network Systems.
- CSV provenance: `ref/notes/CA-Types.csv:30`; taxonomy provenance: `ref/notes/CA-Types.md:786-813`.
- Canonical section: Chapter 5, `Network Systems`, beginning at `BOOK:2368` and ending before `Multiway Systems` at `BOOK:2490`.
- Entry kind: deterministic graph-topology evolution construction with fixed-two-labeled-port, rerouting, node-creating, and topology-conditioned profiles.
- Initial search vocabulary: network system(s), network evolution, node(s), connection(s), above/below, labeled connections, reroute/rerouting, insert/new node, disconnected/piece/component/reachable, local structure, distinct nodes, distance two, inequivalent/isomorphic/canonical, adjacency/connectivity, graph, trinet, causal network, space network, network constraint, node count, rule implementation/enumeration.

## Search Log

1. Verified CSV line 30 and read the complete taxonomy section `ref/notes/CA-Types.md:786-813`.
2. Located the complete Chapter 5 core `BOOK:2368-2490`, including every prose definition and page-209 through page-218 caption. Detailed disposition is in progress.
3. Direct `network system(s)` and expanded mechanism/variant searches are in progress across the canonical monolith. Counts will be frozen only after Notes and actual Index duplicates are separated.
4. Core figures, Notes implementation, rule encodings/counts, actual Index routes, split files, history, physics/causal-network relations, constraint-network boundary, runtime fit, and exact oracles are being audited in parallel.

## Book Excerpts

Canonical `BOOK` means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. Excerpt groups and exact dispositions remain open until the full search closes.

### E01 — Connectivity, not drawing geometry, is state

- Provenance: `BOOK:2368-2384`.
- Preliminary fact: a network is nodes plus connections and rules changing connections; layout positions have no fundamental significance.

### E02 — Fixed two labeled outgoing ports and self-loops

- Provenance: `BOOK:2384-2392`, page-209 caption.
- Preliminary fact: the section restricts every node to two outgoing connections; small-network enumeration quotients some labels and omits unreachable nodes.

### E03 — Geometry, arrays, trees, and layouts are derived

- Provenance: `BOOK:2394-2422`, pages 210-212.
- Preliminary fact: one connectivity carrier can realize effective arrays of arbitrary dimension, infinite trees, and nested patterns; identical networks can look different under layout.

### E04 — Labeled-path rerouting and disconnection

- Provenance: `BOOK:2424-2448`, pages 213-214.
- Preliminary fact: rules replace labeled outgoing ports with targets reached by old-graph path words; one rule splits the graph, after which the displayed/reference evolution keeps the piece containing the first node.

### E05 — Fresh-node insertion

- Provenance: `BOOK:2448-2460`, page-215.
- Preliminary fact: one fresh node is inserted into every old node's above connection; its two ports copy or swap targets reached from the old source; the canonical seed has one node.

### E06 — Topology-conditioned cases and longer-range reads

- Provenance: `BOOK:2460-2482`, pages 216-218.
- Preliminary fact: rules branch on one-step target equality or counts of distinct nodes reachable by paths of length at most two; longer-range cases yield nontrivial node-count behavior.

## Construction Model

Open evidence questions to close before committing a model:

1. Exact typed syntax and evaluation order for page-214 path-replacement rules.
2. Whether rules replace port path expressions simultaneously per node and globally from one old snapshot.
3. The authoritative meaning of the first/root node and reachability pruning.
4. Fresh-node target semantics, collision behavior, token allocation, and whether deletion is only projection-induced.
5. Semantic graph equality versus unlabeled/rooted isomorphism and reference enumeration.
6. Complete local-condition key space, result algebra, rule counts/codecs, and Notes generation convention.
7. Base outcomes, empty graph validity, disconnected components, external horizons, and fixed-point treatment.

## Current API Fit

Pending direct audit. The known pressure is a semantic mismatch between fixed rank-0..3 integer coordinate fields and mutable cyclic graph topology; path-relative connection reads and graph rewrites cannot be represented as incidental coordinate neighborhoods.

## Current Runtime Fit

Pending direct audit of `simple_programs.md`, `src/ca`, and tests. No existing runtime module is presumed to implement graph state, isomorphism, path traversal, fresh nodes, or atomic rerouting.

## Principles Audit

Pending evidence closure. Provisional rejections include fixed-capacity adjacency tensors presented as native graphs, layout coordinates as node identity, whole graphs packed into scalar values, arbitrary graph-rewrite callbacks, hidden allocation counters, sequential in-place rewiring, implicit component pruning, and a `network` family rollout.

## Detailed Implementation Plan

1. Close direct-name, alias, mechanism, caption/figure, Notes, actual Index, split, history, implementation, rule-count, creation, component, isomorphism, observer, and cross-reference searches with zero unresolved candidates.
2. Reconstruct strict graph carrier, node/port identity, roots, sources, path reads, local predicates, results, synchronous update, freshness, pruning/projection, outcomes, seeds, variants, and observers.
3. Derive exact canonical trajectories and adversarial conformance oracles independently from prose/Notes/figures.
4. Compare every responsibility with T20/T27, `simple_programs.md`, runtime modules, and tests; decide whether graph mutation establishes a seventh update law.
5. Audit principles, rejected shortcuts, Goal 2 dependencies, serialization/isomorphism, ragged traces, batching, and no-cheating checks.
6. Reintegrate `0-plan.md`, `evidence-index.md`, and `design-ledger.md`; reopen earlier stages only if evidence invalidates them.

## Goal 2 Implementation Stage

Pending evidence closure. It will specify concrete graph carrier/program/result/update APIs, dependencies, exact book presets, migrations, raw traces, canonicalization boundaries, validation, conformance tests, and forbidden fallback audits without a family-specific rollout.

## No-Cheating Checks

- No whole-network scalar, string, expression-tree, fixed-capacity adjacency image, lattice, or drawing-coordinate substitute for native topology.
- No graph/neighbor/rewrite/isomorphism callback containing the construction and no named network rollout branch.
- No hidden node counter, root, component filter, port ordering, path cache, sequential mutation, or newborn firing.
- No silent node deduplication, isomorphism quotient, unreachable-node deletion, edge-label erasure, or display-index semantics.
- No maximum node count, padded adjacency size, layout extent, rendering cutoff, or node-count plot fed back as program state.
- No T20 tree replacement, T27 bag replacement, or fixed-support assignment relabeled as graph rewiring without preserving sharing/cycles/freshness.

## Completion Requirements

- [ ] All names, aliases, figures, Notes, actual Index entries, splits, implementation/history, variants, observers, and relations resolved with zero silent remainder.
- [ ] Native graph/root/port state, sources, reads, rule/results, update, freshness, pruning, seed, successor, and boundary semantics reconstructed.
- [ ] Exact canonical trajectories, rule counts/codecs, isomorphism, rerouting, disconnection, node-creation, local-condition, newborn, and provenance invariants specified.
- [ ] Current API/runtime/principles fit and T20/T27 reuse/divergence explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration complete.

## Stage Results

In progress. Current work has established the strict Chapter 5 section boundary and the central topology-versus-layout distinction; all semantic conclusions remain provisional until core figures, Notes, Index, rule encodings, and independent oracles close.
