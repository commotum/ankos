# 7-INDEX-CHECK

## Current Facts

- The Index has 5,484 top-level entries and approximately 83,000 words.
- Goal 5 does not treat those entries as independent source units.
- Sequential discovery is complete through Chapter 12.
- The compact register contains 1,563 leads, of which 81 are currently serious;
  these remain leads rather than type counts.

## Updated Assumptions

- The Index will mainly expose aliases, historical names, and additional source
  references for already discovered mechanics.
- Generic entries such as “cellular automata” or “computation” are too broad to
  inspect exhaustively.
- A bounded checklist built from discovered mechanism names and close aliases
  is sufficient when followed by the later whole-book saturation pass.

## Big Picture Objective

Use the Index as a targeted omission and alias challenge without reading or
dispositioning all 5,484 entries.

## Detailed Implementation Plan

- Build a compact checklist from the mechanics named in Goal 5 stage results
  and surface labels mechanically extractable from the raw-lead register.
- Group synonyms under cellular, rewriting, network, numeric, continuous,
  stochastic/growth, relation/constraint, analysis, memory, and computation
  families.
- Search only the Index for those terms and their explicit `see`/`see also`
  aliases.
- Follow a referenced Book location only when it is absent from the register or
  raises a genuine mechanical ambiguity.
- Add a raw lead only for a source-grounded omitted mechanism.
- Record checked terms and outcomes compactly in this stage file; do not retain
  a raw hit dump.

## No-Cheating Checks

- Do not read the Index sequentially or create one row per Index entry.
- Do not search the catalog, API, runtime, or prior-goal material.
- Do not treat a new name, person, application, theorem, property, or page
  reference as a new construction without source mechanics.
- Do not repeat the whole-book saturation pass reserved for Stage 9.
- Do not build a generalized Index parser or permanent search tool.

## Completion Requirements

- The checklist covers all discovered mechanism families and close aliases.
- Every explicit Index alias reached by the checklist is checked.
- Every genuinely new source location is inspected in canonical source.
- Any omitted mechanism is added to `raw-leads.csv` with a canonical anchor.
- The checked-term/result summary is compact and no line-by-line Index ledger
  exists.
- `coverage.md` marks the Index checklist complete.
- Changes remain confined to Goal 5, `git diff --check` passes, and artifact
  growth remains compact.

## Stage Results

### Checked families

The bounded checklist covered:

- cellular, block, continuous, probabilistic, reversible, sequential/
  asynchronous, second-order, totalistic, mobile, fluid, and lattice-gas
  automata;
- substitution, sequential substitution, string rewriting, multiway, tag,
  cyclic-tag, multiway-tag, symbolic, grammar, classifier, Markov, and normal
  algorithms;
- network evolution/substitution, graph rewriting, network constraints, causal,
  random, trivalent, directed, sequential, and mobile-network systems;
- arithmetic and iterated-map systems, register/program machines, ordered
  fraction systems/Fractran, recursive/partial functions, minimization,
  Diophantine relations, and continued fractions;
- continuous systems/computation, coupled-map lattices, ODE/PDE/continuum
  equations, Navier–Stokes, Lorenz, reaction–diffusion, Einstein equations,
  path integrals, and variational principles;
- random/self-avoiding walks, aggregation/DLA, Eden growth, percolation,
  deposition, branching, crystal growth, phyllotaxis, fracture, drainage,
  shells, and curvature;
- constraints, tilings, PCP/correspondence systems, sequence equations,
  satisfiability/CNF, axiom/operator systems, word problems, sorting networks,
  self-assembly, and shortest paths;
- compression codecs, dithering, linear prediction, hashing, signal/image
  processing, randomness tests, backtracking, sideways CA evolution,
  cryptanalysis, and Boolean minimization;
- matrix/associative memory, neural networks, nearest-neighbor retrieval,
  Voronoi diagrams, Hamming/error-correcting codes, and memory encodings; and
- computation interfaces, stored-program machines, Turing/nondeterministic/
  quantum machines, combinators, lambda calculus, compilers, emulation,
  halting, and partial functions.

### Alias outcomes

- Asynchronous CA resolves through the Index's sequential-CA terminology.
- Second-order CA resolves through reversible CA.
- Graph rewriting resolves through `Networks` → evolution/substitution.
- Coordinate evaluation resolves through finite automata, formulas for nesting,
  and substitution systems.
- Intrinsic synchronization resolves through CA synchronization and dataflow.
- Inverse CA procedures resolve through backtracking, cryptanalysis, and
  sideways evolution.
- Associative retrieval resolves through matrix memories and nearest-neighbor
  algorithms.
- Unbounded minimization resolves through general recursive and partial
  functions.
- Error diffusion resolves through dithering/halftoning, distinct from ordered
  threshold dithering.

### Completion

- Every mechanics family retained in Stages 2–6 has an Index entry or explicit
  broader/alias route.
- No Index entry established a source-grounded omitted mechanism.
- No lead or status change was required.
- Six minor wording choices—coordinate automaton, error diffusion, graph
  rewriting, intrinsic synchronization, unbounded minimization, and associative
  memory—remain discoverability aliases for the final handoff, not taxonomy
  questions.
- The Index was not read or dispositioned line by line, no hit dump was
  retained, and the whole-book saturation pass remains reserved for Stage 9.
- `coverage.md` marks the Index checklist complete.
- Next: Stage 8, `CONSOLIDATE`.
