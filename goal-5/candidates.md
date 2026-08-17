# Serious mechanics candidates

This is the compact Stage 8 shortlist. Candidate identity is mechanical, not a claim that every row becomes a public type. Catalog and API material remained closed while this inventory was formed.

- Serious candidate clusters: 102
- Serious source leads represented: 190

## C001 — `active-node-network-rewrite`

- Leads: L0918
- Carrier/domain: mutable directed graph plus one active-node marker
- Initialization: seed graph and designated active node
- Acting loci and read: only the active node reads its bounded local connection structure
- Effect, schedule, commit: rewrite nearby edges or nodes then move activity; one atomic sequential commit
- Termination/output: stops if activity is trapped or no rule applies; outputs graph and active-node path
- Defining variants: connection-following choices; local topology tests; node insertion
- Representative sources: BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L453-457
- Distinguishing test: only one node acts per step, unlike a parallel network rewrite

## C002 — `alternating-block-cellular-automaton`

- Leads: L1390, L1418, L1458, L1459, L1494, L1507
- Carrier/domain: lattice partitioned into finite blocks / a 2D binary spin array plus a checkerboard phase mask
- Initialization: discrete particles or complex amplitudes plus partition phase / a spin configuration and one active checkerboard parity
- Acting loci and read: current disjoint block under active alignment / only active-parity cells read their current spin, four-neighbor sum, and mask
- Effect, schedule, commit: apply block collision permutation or unitary then shift alignment for next step / flip eligible active cells in parallel, then toggle parity; two half-step commits conserve energy
- Termination/output: fixed-step lattice particle trace or amplitudes / fixed steps or indefinite; outputs spin history, energy, or magnetization
- Defining variants: hex lattice gas; temperature state; reversible conserved; unitary / initial spin density and energy; checkerboard phase
- Representative sources: CH08:L155-165;N08:L107,L124-126;CH09:L303-321;N09:L923-927 / BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L458-468
- Distinguishing test: the partition alignment alternates and a whole block is transformed as one unit / adjacent sites never update in the same half-step and total nearest-neighbor energy remains invariant

## C003 — `append-only-sequence-generator`

- Leads: L0504, L0572, L0575
- Carrier/domain: growing finite symbol sequence with a counter or aggregate register
- Initialization: empty or short seed sequence and initial counter
- Acting loci and read: the append frontier reads the next counter value or an aggregate of the whole prefix
- Effect, schedule, commit: append encoded symbols sequentially; the existing prefix is never rewritten
- Termination/output: normally unbounded; output is the limiting or finite generated sequence
- Defining variants: successive-integer concatenation; append digits of current symbol sum
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L203-210;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L569-599
- Distinguishing test: after every step the previous state must remain an exact prefix of the next

## C004 — `arithmetic-equation-constraint`

- Leads: L0963, L1561
- Carrier/domain: nonnegative integer variables and polynomial or exponential expressions / integer tuples over a finite-dimensional arithmetic domain
- Initialization: equations and candidate assignment / equation plus fixed coefficients or parameters; no evolving seed
- Acting loci and read: all terms under the assignment / the relation reads all variables in a candidate tuple
- Effect, schedule, commit: uniterated evaluate both sides and accept equality / no transition schedule; accept tuples satisfying the equation
- Termination/output: Boolean result witnesses or existential solution set / external enumeration may not terminate; output is the full or queried solution set
- Defining variants: polynomial; exponential; auxiliary compilation variables / linear equations; Pell equations; general Diophantine equations
- Representative sources: CH12:L885-905;N12:L901-966 / BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L721-747
- Distinguishing test: unknowns are nonnegative integers constrained by exact arithmetic equations / membership is decided by one global arithmetic relation, not overlapping local templates

## C005 — `associative-evolution-by-squaring`

- Leads: L1532
- Carrier/domain: associative transformations or algebra elements
- Initialization: initial element rule composition and target exponent
- Acting loci and read: binary digits of requested step count
- Effect, schedule, commit: repeatedly square and conditionally compose according to exponent bits
- Termination/output: state at target time
- Defining variants: logarithmic fast-forward; symbolic composition
- Representative sources: CH10:L743-757;N10:L790-810
- Distinguishing test: work grows with the bit length of time rather than by simulating every prior step

## C006 — `asynchronous-cellular-automaton`

- Leads: L1499, L1500
- Carrier/domain: finite-color lattice plus readiness or update schedule
- Initialization: CA state rule and scan random or arrow-control policy
- Acting loci and read: one selected cell or a ready local neighborhood
- Effect, schedule, commit: expose each write immediately; choose next locus by schedule or readiness
- Termination/output: fixed update count or asynchronous trace
- Defining variants: fixed scan; random permutation; random choice; arrow-gated synchronization
- Representative sources: N09:L407-443
- Distinguishing test: writes become visible before all cells have completed a global generation

## C007 — `bidirectional-axiom-rewriting`

- Leads: L1560
- Carrier/domain: expression or formula trees with equations
- Initialization: initial expression axioms and fresh-term enumeration policy
- Acting loci and read: all matching subtrees in both equation directions
- Effect, schedule, commit: generate every forward and reverse replacement as multiway successors
- Termination/output: cutoff proof graph reachability or derived formulas
- Defining variants: RHS-only variables; subtree or whole-formula rewrites
- Representative sources: CH12:L749-775;N12:L605-611,L751-797
- Distinguishing test: each equation is usable in both directions and all applicable rewrites may branch

## C008 — `boolean-satisfaction-relation`

- Leads: L1558
- Carrier/domain: Boolean variables clauses and assignments
- Initialization: CNF formula and candidate assignment
- Acting loci and read: each clause literals
- Effect, schedule, commit: uniterated accept iff every clause has at least one true literal
- Termination/output: Boolean result or satisfying assignments
- Defining variants: CNF; bounded-machine-trace compiler
- Representative sources: CH12:L681-691;N12:L521-543
- Distinguishing test: validity is clause satisfaction not execution of the compiled machine history

## C009 — `branching-annihilating-particle-system`

- Leads: L1326
- Carrier/domain: moving branches or particles embedded in space and time
- Initialization: a finite initial branch configuration
- Acting loci and read: each live branch reads the branching clock and collision occupancy
- Effect, schedule, commit: spawn two or three branches at fixed intervals; colliding pairs annihilate at the event
- Termination/output: no live branches or indefinite growth; outputs particle worldlines and nested pattern
- Defining variants: two-branch and three-branch spawning rules
- Representative sources: CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L813-820
- Distinguishing test: two colliding branches disappear; independent substitution descendants would both remain

## C010 — `causal-network-extraction`

- Leads: L1497
- Carrier/domain: event dependency graph derived from an evolution
- Initialization: update history with input provenance
- Acting loci and read: each event and the last events producing its inputs
- Effect, schedule, commit: create an event node and dependency edges while carrying unchanged provenance
- Termination/output: derived causal graph
- Defining variants: event granularity; unchanged-cell carry rules
- Representative sources: CH09:L655-707;N09:L347-355,L378-384
- Distinguishing test: nodes denote update events rather than system states

## C011 — `context-dependent-substitution`

- Leads: L0169
- Carrier/domain: finite-symbol word
- Initialization: seed word
- Acting loci and read: each symbol plus specified neighboring symbols
- Effect, schedule, commit: replace symbols from contextual rules with generation commit
- Termination/output: fixed-generation word or trace
- Defining variants: left-context; right-context; boundary deletion
- Representative sources: CH03:L333-337
- Distinguishing test: two equal symbols can receive different replacements because their contexts differ

## C012 — `context-free-derivation-and-parsing`

- Leads: L1542
- Carrier/domain: grammar symbols parse trees and strings
- Initialization: start symbol or target string plus productions
- Acting loci and read: one nonterminal or parser span
- Effect, schedule, commit: rewrite a nonterminal forward or combine reverse parses retaining alternatives
- Termination/output: derived strings parse forest or recognition
- Defining variants: context-free generation; reverse parsing; ambiguous derivations
- Representative sources: N10:L1039-1065
- Distinguishing test: productions build or parse nested grammatical structure and may retain multiple derivations

## C013 — `continuous-billiard-dynamics`

- Leads: L1346
- Carrier/domain: a point ball with continuous position and velocity inside a bounded table
- Initialization: initial position and slope or velocity
- Acting loci and read: free motion reads no environment until the next boundary collision
- Effect, schedule, commit: continuous flight followed by event-driven boundary reflection and immediate velocity commit
- Termination/output: normally unbounded; outputs trajectory or ordered boundary-hit sequence
- Defining variants: table geometry and starting slope
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L60-61
- Distinguishing test: update times are collision events determined by geometry rather than fixed discrete timesteps

## C014 — `coordinate-automaton-evaluator`

- Leads: L1530
- Carrier/domain: integer coordinate digits and finite automaton
- Initialization: start state coordinate base and transition table
- Acting loci and read: successive digits of one requested coordinate
- Effect, schedule, commit: fold automaton state over coordinate digits once
- Termination/output: single cell value without full pattern generation
- Defining variants: uniform cuboidal substitutions; multiple dimensions
- Representative sources: CH10:L647-673;N10:L672-681
- Distinguishing test: one cell is queried directly from its coordinates without evolving intermediate arrays

## C015 — `differential-sheet-growth-relation`

- Leads: L1427
- Carrier/domain: embedded sheet mesh with target equal cell sizes
- Initialization: initial mesh topology growth profile and boundary conditions
- Acting loci and read: global geometry and adjacent cell metrics
- Effect, schedule, commit: add material then solve or relax embedding to satisfy equal-size constraints
- Termination/output: acceptable embedded sheet or iteration trace if a solver is supplied
- Defining variants: relation-only; iterative relaxation ambiguity
- Representative sources: CH08:L563-569;N08:L226
- Distinguishing test: the defining condition is an embedding-wide equal-cell-size constraint

## C016 — `diffusion-limited-aggregation`

- Leads: L1376, L1445
- Carrier/domain: lattice or continuous space with an aggregate seed / a fixed occupied cluster plus one mobile random walker on a lattice
- Initialization: seed cluster walker source and sticking contact rule / a seed cluster and a walker released far from it for each growth cycle
- Acting loci and read: one mobile walker position and aggregate boundary / the walker reads local moves and whether its position is adjacent to the whole cluster
- Effect, schedule, commit: random-walk until contact then irreversibly attach; repeat / random-walk sequentially; at first cluster contact commit the walker as one new occupied cell
- Termination/output: target particle count or cluster / target cluster size; outputs the accumulated cluster
- Defining variants: random-walker DLA; Laplace-field sampling equivalent / lattice; dimension; walker release and escape boundary policies
- Representative sources: N08:L50 / BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L359-360
- Distinguishing test: a new particle performs a random walk before first-contact attachment / frontier-site probability is induced by first-hit random-walk paths, not direct uniform frontier sampling

## C017 — `digit-emitting-register-transducer`

- Leads: L0396, L0398, L0569
- Carrier/domain: finite integer registers plus a growing digit-output stream
- Initialization: dividend and divisor or radicand with algorithm-specific register values
- Acting loci and read: the whole register tuple acts and reads comparisons or bounded remainder state
- Effect, schedule, commit: atomically update registers and emit exactly one base digit per sequential step
- Termination/output: division may enter a remainder cycle; root extraction continues to requested precision
- Defining variants: binary long division; paired-register square-root extraction
- Representative sources: CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L303-308;CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L343-350
- Distinguishing test: the emitted symbol is construction-defining and cannot be recovered as only a final state

## C018 — `driven-sandpile-relaxation`

- Leads: L1411
- Carrier/domain: integer sand-height values on a regular lattice
- Initialization: a stable height array, often empty
- Acting loci and read: sites at or above the dimension-dependent threshold read local neighbor heights
- Effect, schedule, commit: add load at a center or random site, then apply conservative local topplings until a fixed point
- Termination/output: each avalanche ends when all sites are subthreshold; outer drive cycles output stable states and durations
- Defining variants: center or random drive; dimension d; threshold 2d; one-dimensional and two-dimensional rules
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L665-676
- Distinguishing test: one drive event can trigger zero or many internal toppling steps before the next load is admitted

## C019 — `einstein-spacetime-relation`

- Leads: L1506
- Carrier/domain: continuous spacetime metric and stress-energy fields
- Initialization: boundary or initial data and candidate fields
- Acting loci and read: curvature and stress-energy at all spacetime points
- Effect, schedule, commit: enforce field equations or extremize action as a global relation
- Termination/output: admissible metric fields or evolved solution
- Defining variants: initial-value form; action-extremum form
- Representative sources: N09:L820-840
- Distinguishing test: outputs are metrics satisfying curvature and stress-energy constraints

## C020 — `encode-evolve-decode-interface`

- Leads: L1545, L1549
- Carrier/domain: source states target mechanism and decoding relation
- Initialization: source input encoder target initial-state map stop or observation rule and decoder
- Acting loci and read: selected encoded target features before and after evolution
- Effect, schedule, commit: encode once evolve unchanged target then decode at a time or stopping predicate
- Termination/output: decoded result or emulation relation
- Defining variants: fixed; multiple; angled-block; terminating encoders
- Representative sources: CH11:L15-37;N11:L674-690
- Distinguishing test: the underlying target dynamics stay unchanged while encoder time and decoder define the computation

## C021 — `energy-minimization-constraint`

- Leads: L0955, L1448
- Carrier/domain: random-weight bond graph / fixed lattice or graph of discrete spins with local energy terms
- Initialization: graph geometry bond strengths and endpoints / domain, spin alphabet, couplings, and boundary data; no evolutionary seed required
- Acting loci and read: global candidate paths or a shortest-path frontier / each local term reads a bounded neighboring spin configuration
- Effect, schedule, commit: minimize summed broken-bond strength and commit the selected path / no intrinsic step rule; sum local energies and select global minimizers
- Termination/output: minimum path and total strength / external minimization may be difficult; output is the ground-state set
- Defining variants: random bond distributions / Ising-like energies; generalized local couplings; spin-glass couplings
- Representative sources: N08:L59 / BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L704
- Distinguishing test: the crack is selected by a global minimum-total-strength objective / two locally admissible configurations can both pass hard tests yet have different energy

## C022 — `enumerative-semidecision`

- Leads: L1544, L1551
- Carrier/domain: ordered candidate domain and decidable predicate
- Initialization: query candidate generator and predicate
- Acting loci and read: next candidate in enumeration
- Effect, schedule, commit: test candidates in order and halt on first match
- Termination/output: first or least witness; may diverge when none exists
- Defining variants: description enumeration; unbounded minimization
- Representative sources: CH10:L975-989;N10:L5-15;N11:L829-855
- Distinguishing test: absence of a witness causes nontermination rather than a negative result

## C023 — `error-diffusion-dither`

- Leads: L1518
- Carrier/domain: grayscale raster
- Initialization: input intensities scan order quantizer and diffusion weights
- Acting loci and read: current pixel plus accumulated incoming error
- Effect, schedule, commit: quantize sequentially then distribute error only to future neighbors
- Termination/output: reduced-palette raster
- Defining variants: Floyd-Steinberg weights; alternate scans
- Representative sources: N10:L348-360
- Distinguishing test: later pixel decisions depend on quantization error from earlier pixels

## C024 — `exact-sequence-hash-table`

- Leads: L1535
- Carrier/domain: symbol keys bounded integers and table buckets
- Initialization: keys hash fold table size and collision policy
- Acting loci and read: next input symbol during hash fold then selected bucket
- Effect, schedule, commit: fold key to hash and insert or query using chaining or probing
- Termination/output: bucket index stored value or miss
- Defining variants: chaining; linear or structured probing
- Representative sources: CH10:L829-839;N10:L976-980
- Distinguishing test: exact equality is checked after bounded hashing resolves candidate locations

## C025 — `field-gated-local-evolution`

- Leads: L1431
- Carrier/domain: discrete local states coupled to continuous concentration fields
- Initialization: local states fields diffusion constants thresholds and rule banks
- Acting loci and read: local neighborhood and local field concentrations
- Effect, schedule, commit: diffuse fields then select and execute a local rule bank by thresholds
- Termination/output: fixed-time state and field history
- Defining variants: gene-bank selection; multiple diffusing signals
- Representative sources: CH08:L623-632
- Distinguishing test: a diffusing field threshold chooses which local transition program runs

## C026 — `maximal-run-record-transduction`

- Leads: L1510
- Carrier/domain: an ordered finite symbol carrier with a configured scan and homogeneous-extent grammar
- Initialization: input symbols, scan origin, record convention, and empty encoded carrier; inverse mode starts from records
- Acting loci and read: the current scan locus and the maximal homogeneous extent beginning there
- Effect, schedule, commit: emit the extent's symbol/length or another self-delimiting extent record, then advance beyond it; inverse mode expands the record
- Termination/output: end of input; record stream or reconstructed symbols
- Defining variants: binary run lengths; explicit symbol-length pairs; self-delimiting integer grammars; row, space-filling, or rectangular scans
- Representative sources: CH10:L163-187;N10:L83-85,L171-175
- Distinguishing test: the next record boundary is determined by maximal equality from the current scan locus, not by a fixed block, prior match, recursive parent split, or probability interval

## C027 — `finite-operator-table-model`

- Leads: L1562
- Carrier/domain: finite domain operator tables expressions and axioms
- Initialization: domain size operator tables variable assignment and equations
- Acting loci and read: expression tree under each variable assignment
- Effect, schedule, commit: evaluate bottom-up; accept a table only if every assignment satisfies every axiom
- Termination/output: value table Boolean model test or satisfying operator tables
- Defining variants: single or multiple operators; finite axiom systems
- Representative sources: CH12:L1073-1095;N12:L1189-1203,L1245-1257
- Distinguishing test: operators are unknown finite tables universally tested over all assignments

## C028 — `finite-topology-sequence-model-fitting`

- Leads: L1522
- Carrier/domain: symbol sequences and finite probabilistic graph
- Initialization: training sequence model topology and smoothing rule
- Acting loci and read: counted symbols blocks or transitions
- Effect, schedule, commit: estimate outgoing probabilities then sample a path sequentially
- Termination/output: fitted model likelihoods or generated sequence
- Defining variants: IID; fixed blocks; Markov order
- Representative sources: CH10:L441-459;N10:L495-501
- Distinguishing test: the topology is fixed and only probabilities are learned from observed frequencies

## C029 — `finite-unitary-circuit`

- Leads: L1559
- Carrier/domain: finite qubit amplitude vector
- Initialization: normalized input amplitudes ordered gates and measurement policy
- Acting loci and read: one or two qubits selected by each gate
- Effect, schedule, commit: apply unitary gates in order then sample basis outcomes by squared magnitude
- Termination/output: final amplitudes or sampled bitstring
- Defining variants: one-qubit; two-qubit; finite precision; tolerance
- Representative sources: N12:L560-574
- Distinguishing test: a finite gate list transforms amplitudes and measurement samples squared magnitudes

## C030 — `generalized-mobile-automaton`

- Leads: L0149
- Carrier/domain: 1D cells plus a finite active-site set
- Initialization: cell colors and one or more active sites
- Acting loci and read: each active site and its neighborhood
- Effect, schedule, commit: move split or delete active sites with simultaneous commit
- Termination/output: fixed-step trace or final cells and active set
- Defining variants: multiple-active; split; annihilation
- Representative sources: CH03:L231-247
- Distinguishing test: the active-site count can change during evolution

## C031 — `global-maximum-depletion-placement`

- Leads: L1425, L1465, L1466, L1467
- Carrier/domain: cyclic scalar field with placed-point set
- Initialization: initial concentration field depletion kernel and placement count
- Acting loci and read: all field positions for a global maximum
- Effect, schedule, commit: select maximum place point translate depletion kernel then update field
- Termination/output: requested placements or point pattern
- Defining variants: sequential; simultaneous tied maxima; cyclic field
- Representative sources: CH08:L531-547;N08:L223-225
- Distinguishing test: each new point is chosen by a global field maximum rather than a local frontier

## C032 — `history-dependent-growth-rewrite`

- Leads: L0868
- Carrier/domain: growing lattice site set retaining birth or parent relations
- Initialization: small occupied-site seed with stored ancestry data
- Acting loci and read: candidate growth sites read current occupancy and retained historical parent relations
- Effect, schedule, commit: add all eligible sites and their provenance per growth round; prior sites persist
- Termination/output: normally unbounded; output is occupied support together with retained ancestry
- Defining variants: Ulam growth rules and partial-rule variants
- Representative sources: BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L130-151
- Distinguishing test: two equal current occupancy patterns with different ancestry can evolve differently

## C033 — `intrinsic-curvature-curve-integration`

- Leads: L1430, L1469
- Carrier/domain: planar or spatial curve parameterized by arc length
- Initialization: start position heading and curvature function
- Acting loci and read: current arc position heading and curvature
- Effect, schedule, commit: integrate heading from curvature then position from heading
- Termination/output: end arc length or sampled curve
- Defining variants: continuous integration; discrete sampling
- Representative sources: CH08:L613-617;N08:L253-271
- Distinguishing test: input specifies intrinsic curvature rather than Cartesian coordinates

## C034 — `inverse-local-rule-reconstruction`

- Leads: L1526, L1527
- Carrier/domain: observed CA or LFSR outputs and unknown predecessor variables
- Initialization: target trace or column rule boundary assumptions and width
- Acting loci and read: sideways neighborhoods or partial light-cone assignments
- Effect, schedule, commit: solve modular equations or depth-first assign variables and prune contradictions
- Termination/output: predecessor set key candidates or failure
- Defining variants: sideways evolution; linear solve; DFS backtracking
- Representative sources: CH10:L575-633;N10:L531-544,L608-624
- Distinguishing test: the procedure reconstructs hidden predecessor states from constrained outputs

## C035 — `iterated-erasure-process`

- Leads: L0376, L0535
- Carrier/domain: ordered surviving set of cells or numbers
- Initialization: finite or conceptually infinite ordered population
- Acting loci and read: survivors are tested by divisibility or rank in the current survivor ordering
- Effect, schedule, commit: delete the selected subset and commit the reduced support once per round
- Termination/output: finite domains exhaust or stabilize; output survivors, primes, or survival times
- Defining variants: Eratosthenes sieve; every-kth decimation; circular Josephus variant
- Representative sources: CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L211-214;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L418-430
- Distinguishing test: support only shrinks and current survivor rank can affect the next deletion

## C036 — `iterated-history-dependent-game`

- Leads: L1543
- Carrier/domain: two program agents action histories and payoff matrix
- Initialization: programs initial histories rounds and payoff table
- Acting loci and read: each program reads both prior output histories
- Effect, schedule, commit: simultaneously emit moves append histories and award matrix payoff
- Termination/output: round trace and cumulative payoffs
- Defining variants: deterministic or randomized programs
- Representative sources: N10:L1081-1085
- Distinguishing test: each agent move is generated by a program over both players past moves

## C037 — `iterated-map`

- Leads: L0331, L0332, L0333, L0341, L0342, L0345, L0347, L0353, L0419, L0500, L0590, L0623, L1395, L1547, L1548
- Carrier/domain: nonnegative integer state / one finite tuple of integer or real values, optionally viewed through a digit encoding / a continuous scalar or vector state and differentiable objective f
- Initialization: initial integer ordered dispatch rules and arithmetic maps / one starting scalar or vector / initial point x0 and step size a
- Acting loci and read: current integer residue or divisibility tests / the sole current tuple acts; the rule may read all values, guards, or encoded digits / the current point reads the local derivative or gradient of f
- Effect, schedule, commit: select one arithmetic transform by residue or first applicable multiplier then repeat / replace the entire tuple by one deterministic image in one atomic discrete step / commit x := x - a grad(f(x)) once per iteration
- Termination/output: halt condition or integer trajectory / usually an unbounded orbit; optional halt, cycle, or target test; output is the orbit / gradient tolerance, fixed point, or step budget; outputs the final point and objective value
- Defining variants: residue-indexed functions; ordered fraction multipliers / add or multiply; parity maps; reverse-add; Euclid pairs; shift, logistic, Newton, and matrix maps / scalar or vector state; fixed or varying step size; Newton iteration is a related variant
- Representative sources: CH11:L377-393;N11:L525-570 / CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L53-54;CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L111-118;CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L472-491;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L678-683 / BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L542-549
- Distinguishing test: exact arithmetic predicates choose one of several integer transformations at each step / the next state is one selected image computable from only the current finite tuple / a zero-gradient local minimum halts even when another point has a lower global objective

## C038 — `least-unique-sum-sequence`

- Leads: L0533
- Carrier/domain: growing ordered sequence of integers
- Initialization: finite integer prefix such as one and two
- Acting loci and read: the append operation reads all earlier values and all pair-sum multiplicities
- Effect, schedule, commit: globally search upward and append the least uniquely representable sum
- Termination/output: continues while a qualifying integer exists; output is the generated sequence
- Defining variants: Ulam-sequence seeds and related uniqueness predicates
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L404-409
- Distinguishing test: choosing the next term requires a global least search over all prior pairs

## C039 — `lightcone-boolean-compiler`

- Leads: L1533
- Carrier/domain: finite CA light cone and Boolean expressions
- Initialization: rule target cell time depth and input variables
- Acting loci and read: all assignments or recursively composed local formulas
- Effect, schedule, commit: enumerate finite dependencies compose formulas then minimize
- Termination/output: Boolean formula truth table or decision artifact
- Defining variants: formula minimization; BDD-like representations
- Representative sources: CH10:L759-801;N10:L816-903
- Distinguishing test: output is a Boolean formula exactly representing a bounded local evolution

## C040 — `local-factor-probability-relation`

- Leads: L1521
- Carrier/domain: finite symbol sequence
- Initialization: candidate sequence and nonnegative local block factors
- Acting loci and read: all overlapping blocks
- Effect, schedule, commit: multiply local factors and normalize if a probability distribution is required
- Termination/output: sequence weight or normalized probability
- Defining variants: block widths; boundary factors
- Representative sources: N10:L493-494
- Distinguishing test: sequence weight factorizes over overlapping local neighborhoods

## C041 — `local-graph-rewrite-system`

- Leads: L1503, L1504
- Carrier/domain: labeled graph with preserved external interfaces
- Initialization: initial graph rewrite rules schedule and optional active node
- Acting loci and read: matched connected subgraph and its dangling interface
- Effect, schedule, commit: replace a match preserving external links; choose global matches or one active-node match
- Termination/output: fixed steps graph trace and optional active location
- Defining variants: least-recent; arbitrary single; maximal nonoverlap; mobile active node
- Representative sources: CH09:L901-965;N09:L495-528,L552-556,L594-600
- Distinguishing test: rules replace connected subnetworks while retaining their outside attachments

## C042 — `local-plus-global-constraint`

- Leads: L0703
- Carrier/domain: complete discrete configuration on a lattice or fixed graph
- Initialization: allowed local templates plus one or more globally required occurrences
- Acting loci and read: local checks read overlapping neighborhoods and the global check scans the whole domain
- Effect, schedule, commit: no evolution; accept only configurations satisfying local rules and existential obligations
- Termination/output: external solver may fail or diverge; output is the satisfying-configuration set
- Defining variants: one required template; all-template occurrence; CA-encoded nested examples
- Representative sources: CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L491-497
- Distinguishing test: a locally valid configuration is rejected if the required template never occurs

## C043 — `local-satisfaction-constraint`

- Leads: L0694, L0699, L0950, L0953, L1496
- Carrier/domain: complete finite or infinite labeled network / complete symbolic array, tiling, or spacetime diagram on a fixed domain
- Initialization: candidate network and allowed rooted-neighborhood templates / allowed overlapping templates, tile compatibility data, and optional boundaries
- Acting loci and read: each node neighborhood as a static pattern / every location reads its bounded overlapping neighborhood
- Effect, schedule, commit: uniterated accept iff every local neighborhood matches an allowed template / no intrinsic iteration; a valid output satisfies every local predicate simultaneously
- Termination/output: Boolean acceptance or zero-one-many satisfying networks / solver is external and may not terminate; output is any or all satisfying configurations
- Defining variants: template radius; label sets / one- and two-dimensional templates; polyomino tilings; CA histories as spacetime constraints
- Representative sources: CH09:L595-615;N09:L324-330 / CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L433-479;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L677-696
- Distinguishing test: no update occurs; validity is a universal local constraint on a complete network / validity is unchanged by solver order and requires no distinguished time direction

## C044 — `local-template-feature-extractor`

- Leads: L1516
- Carrier/domain: raster or finite field
- Initialization: input image kernels weights and threshold
- Acting loci and read: each sliding local window
- Effect, schedule, commit: correlate or threshold every window to emit response cells
- Termination/output: feature map
- Defining variants: template matching; weighted convolution; threshold units
- Representative sources: CH10:L323-357;N10:L298-334
- Distinguishing test: output cells report local feature responses rather than evolving the input field

## C045 — `matrix-associative-memory`

- Leads: L1539
- Carrier/domain: numeric vectors and weight matrix
- Initialization: stored patterns matrix-construction rule and query vector
- Acting loci and read: all query components through matrix projection
- Effect, schedule, commit: multiply by memory matrix then threshold or normalize once
- Termination/output: recalled vector or convergence after optional iteration
- Defining variants: projection memory; threshold variants
- Representative sources: N10:L1019-1020
- Distinguishing test: memory recall is a global matrix projection followed by componentwise decision

## C046 — `merged-state-multiway-evolution-graph`

- Leads: L1502
- Carrier/domain: distinct rewrite states and directed transition edges
- Initialization: initial string and rewrite rules
- Acting loci and read: all one-step matches from each frontier state
- Effect, schedule, commit: generate all results merge equal states and add edges by breadth or depth layers
- Termination/output: finite cutoff graph or reachable-state graph
- Defining variants: deduplicated states; multiplicity-preserving edges
- Representative sources: N09:L457-463
- Distinguishing test: equal results from different histories share one state node

## C047 — `mobile-automaton`

- Leads: L0141
- Carrier/domain: 1D finite-color cells plus one active index
- Initialization: cell colors and active position
- Acting loci and read: active cell and nearest neighbors
- Effect, schedule, commit: update active color then move index left or right; commit each step
- Termination/output: fixed-step trace or final tape and active position
- Defining variants: binary colors; rule presets
- Representative sources: CH03:L169-185
- Distinguishing test: exactly one lattice site is active and moves after every local write

## C048 — `mobile-crack-displacement-ca`

- Leads: L1417
- Carrier/domain: discrete displacement field plus one crack marker
- Initialization: initial displacement cells crack location and lookup rule
- Acting loci and read: crack marker neighborhood and local displacement values
- Effect, schedule, commit: synchronous field update plus one destructive crack move and destination write
- Termination/output: fixed-step crack path and displacement field
- Defining variants: neighbor-choice policies; CA background rules
- Representative sources: CH08:L131-138
- Distinguishing test: a unique crack marker selects and destroys one destination cell while a field CA also evolves

## C049 — `mobile-head-grid-rewrite`

- Leads: L0668, L0895
- Carrier/domain: fixed lattice of cell symbols plus one head position, state, and optional orientation
- Initialization: initial grid or tape contents and designated head state and position
- Acting loci and read: only the head locus acts, reading its state and the symbol under it
- Effect, schedule, commit: write one cell, update head state or orientation, then move one edge; sequential commit
- Termination/output: halts on a missing or halting rule or runs forever; outputs grid and head trajectory
- Defining variants: absolute-direction 2D Turing rules; relative-turn turmites; higher-dimensional grids
- Representative sources: CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L127-131;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L190-216
- Distinguishing test: exactly one local cell can be rewritten per step and the acting locus moves

## C050 — `moving-opening-shell-accretion`

- Leads: L1429, L1468
- Carrier/domain: parametric surface with a moving open rim
- Initialization: initial opening curve growth rates and orientation
- Acting loci and read: current rim geometry and accumulated surface
- Effect, schedule, commit: append a new strip at the moving opening and advance rim
- Termination/output: fixed growth amount or generated shell surface
- Defining variants: progressive accretion; direct parameterization; outside-only clipping
- Representative sources: CH08:L581-591;N08:L234-246
- Distinguishing test: new surface is added only along a moving opening

## C051 — `multiway-rewrite`

- Leads: L0689, L0930, L1065
- Carrier/domain: deduplicated set of whole string or array states
- Initialization: one or more seed states and a finite replacement-rule set
- Acting loci and read: every current state is searched for every rule and every matching position
- Effect, schedule, commit: form one successor per possible single replacement, then union and deduplicate by generation
- Termination/output: halts when no successor exists or branches indefinitely; outputs state sets or evolution graph
- Defining variants: strings; multidimensional arrays; grammars; group and semigroup presentations
- Representative sources: CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L355-369;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L549-574
- Distinguishing test: two applicable matches create alternative global states rather than one state with both edits

## C052 — `multiway-tag-evolution`

- Leads: L1554
- Carrier/domain: sequence states with tag rules
- Initialization: initial sequence prefix rules and branch policy
- Acting loci and read: all matching prefix rules on every frontier sequence
- Effect, schedule, commit: apply every match create branches and optionally deduplicate equal results
- Termination/output: cutoff evolution tree or merged state graph
- Defining variants: multiplicity-preserving; order-preserving; state-deduplicated
- Representative sources: N12:L269-304
- Distinguishing test: more than one matching tag rule advances simultaneously as separate branches

## C053 — `mutable-rule-cellular-metasystem`

- Leads: L1421
- Carrier/domain: CA configuration plus mutable finite rule program
- Initialization: three-color seed rule set and mutation policy
- Acting loci and read: local CA neighborhood plus selected program entry
- Effect, schedule, commit: evolve CA while events add or modify rules in the program
- Termination/output: fixed generations or configuration-and-program history
- Defining variants: rule addition; rule modification
- Representative sources: CH08:L319-329
- Distinguishing test: the transition table itself is part of the evolving state

## C054 — `nearest-memory-retrieval`

- Leads: L1537
- Carrier/domain: points in a metric space
- Initialization: stored points metric index and query
- Acting loci and read: query distances or nodes along a search index
- Effect, schedule, commit: search Voronoi spatial tree or descent basin until nearest candidate
- Termination/output: retrieved stored item and distance
- Defining variants: Voronoi cells; kd-like trees; stored minima descent
- Representative sources: N10:L988-996
- Distinguishing test: the selected memory minimizes distance to the query

## C055 — `neighbor-dependent-block-substitution`

- Leads: L0674
- Carrier/domain: fixed-dimensional symbolic array, usually with periodic boundaries
- Initialization: finite seed array and context-sensitive block rules
- Acting loci and read: each replacement locus reads an overlapping local block containing neighbors
- Effect, schedule, commit: compute context-selected replacement blocks in parallel and commit the assembled array
- Termination/output: normally run for a requested depth; output is the sequence of expanded arrays
- Defining variants: neighborhood shape; boundary mode; replacement-block dimensions
- Representative sources: CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L225-227;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L360
- Distinguishing test: identical center symbols in different neighborhoods can receive different replacements

## C056 — `neighbor-updating-mobile-automaton`

- Leads: L0145
- Carrier/domain: 1D finite-color cells plus one active index
- Initialization: cell colors and active position
- Acting loci and read: active neighborhood including adjacent cells
- Effect, schedule, commit: write active cell and neighbors then move active index
- Termination/output: fixed-step trace or final tape and active position
- Defining variants: write footprint and move rule
- Representative sources: CH03:L197-207
- Distinguishing test: a step may overwrite neighbors as well as the active cell

## C057 — `neural-network-state-and-learning`

- Leads: L1540
- Carrier/domain: directed weighted units
- Initialization: unit states topology weights activation and learning data
- Acting loci and read: incoming weighted values at selected or layered units
- Effect, schedule, commit: update feedforward or recurrent activations and optionally adjust weights
- Termination/output: output vector state trajectory or learned weights
- Defining variants: feedforward; recurrent; synchronous or asynchronous; learning rules
- Representative sources: N10:L1021-1023
- Distinguishing test: the transition is weighted aggregation through a network and may modify weights from examples

## C058 — `nondeterministic-turing-machine`

- Leads: L1557
- Carrier/domain: Turing tapes heads controls and branch set
- Initialization: input tape transition relation and acceptance states
- Acting loci and read: each branch state and scanned symbol
- Effect, schedule, commit: apply every permitted write-state-move outcome and optionally merge equal configurations
- Termination/output: existential accept reject if all halt or cutoff branch graph
- Defining variants: deduplicated branches; breadth or depth schedule
- Representative sources: CH12:L647-677;N12:L495-503
- Distinguishing test: a state-symbol pair can have several simultaneous successor configurations

## C059 — `ordered-dither`

- Leads: L1517
- Carrier/domain: grayscale raster
- Initialization: input intensities recursively built threshold matrix and palette
- Acting loci and read: each pixel value and its periodic threshold
- Effect, schedule, commit: quantize pixels independently against ordered thresholds
- Termination/output: binary or reduced-palette raster
- Defining variants: recursive matrices; periodic tiling
- Representative sources: N10:L339-347
- Distinguishing test: pixel decisions use a fixed precomputed threshold matrix and no propagated error

## C060 — `ordinary-differential-equation`

- Leads: L0632
- Carrier/domain: finite-dimensional vector of continuous variables over continuous time
- Initialization: variable values at an initial time and equation parameters
- Acting loci and read: each derivative reads the current vector and optionally explicit time
- Effect, schedule, commit: all variables follow one simultaneous continuous flow
- Termination/output: runs to a horizon, fixed point, cycle, singularity, or blow-up; output is a trajectory
- Defining variants: autonomous and driven equations; Lorenz, van der Pol, and field-background reductions
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L901-902;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L953-980
- Distinguishing test: the rule specifies derivatives at every time rather than a discrete next-state map

## C061 — `parallel-independent-substitution`

- Leads: L0161, L0172, L0411, L0412, L0413, L0605, L0669, L0671, L0910, L0911, L1453
- Carrier/domain: ordered words or independently branching objects / finite-symbol word / sequence, array, oriented geometry, or point set whose elements carry finite types
- Initialization: seed word or initial object collection / seed word / finite seed element or pattern and fixed or scheduled replacement rules
- Acting loci and read: each symbol or object without neighbor context / each symbol and optional context / every element acts and reads only its own type or orientation plus the global step schedule
- Effect, schedule, commit: replace all eligible items per generation; deterministic or sampled offspring / replacement blocks may be empty; commit a generation together / replace all elements by finite children in parallel, then concatenate or union atomically
- Termination/output: generation trace or final word tree or fragments / fixed point extinction or fixed-generation word / usually a requested depth; output is the nested symbolic or geometric state
- Defining variants: ordered block substitution; stochastic binary fragmentation / creation-deletion balance; multicolor / 1D scheduled rules; 2D or 3D blocks; geometric, affine, and nonlinear point branches
- Representative sources: CH03:L299-307;N08:L66 / CH03:L343-363 / CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L454-461;CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L175-205;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L333-335
- Distinguishing test: each item chooses offspring without reading adjacent items / a valid rule can replace a symbol by the empty word / equal elements at the same step always produce equal children regardless of neighbors

## C062 — `parallel-network-rewrite`

- Leads: L0675, L0683, L0685
- Carrier/domain: mutable directed graph with finite connection labels and optional node types
- Initialization: seed graph, often one looped node
- Acting loci and read: every node reads bounded paths or a local topology signature around itself
- Effect, schedule, commit: reroute edges or insert nodes at all loci in parallel, then commit one new graph
- Termination/output: normally unbounded or reaches a fixed topology; output is the graph sequence
- Defining variants: fixed outdegree; rerouting; node insertion; topology-conditioned and depth-two rules
- Representative sources: CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L241;CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L287-331
- Distinguishing test: the support topology itself changes while all old nodes act in the same step

## C063 — `partial-differential-equation`

- Leads: L0459, L0638, L0639, L0640, L0653, L1455, L1477, L1478
- Carrier/domain: continuous fields or finite real-valued state / continuous field over continuous space and time
- Initialization: initial field or vector plus boundary data and coefficients / equation plus initial or boundary functions on a spatial domain
- Acting loci and read: local derivatives and coupled field values / each spacetime point is related through local spatial and temporal derivatives
- Effect, schedule, commit: integrate simultaneous differential equations through continuous time / continuous field must satisfy the relation; evolution is unique only when data make it well posed
- Termination/output: target time trajectory or boundary-value solution / ends at a horizon or singularity, or has no or many solutions; output is a solution field
- Defining variants: Navier-Stokes PDE; vector reaction-diffusion / hyperbolic, parabolic, and scalar-field equations; negative diffusion; Burgers and nonlinear waves
- Representative sources: N08:L84-105,L322-328 / CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L625-674;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L925-1035;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L591-595
- Distinguishing test: state change is defined by continuous derivatives and requires numerical or analytic integration / with insufficient or inconsistent boundary data the same equation can have many or no solutions

## C064 — `population-evolutionary-search`

- Leads: L1398
- Carrier/domain: a population of candidate genomes with a fitness or constraint objective
- Initialization: multiple initial candidate individuals
- Acting loci and read: selection reads population fitness; recombination reads two or more parent genomes
- Effect, schedule, commit: select and sexually recombine candidates, committing a new population by generations
- Termination/output: fitness threshold or generation budget; outputs the population or best candidate
- Defining variants: population size; selection policy; crossover or mixing strategy; mutation policy
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L556-560
- Distinguishing test: the system must retain multiple candidates and create offspring using information from distinct parents

## C065 — `post-correspondence-relation`

- Leads: L1553
- Carrier/domain: finite list of ordered word pairs
- Initialization: candidate index sequence and tile pairs
- Acting loci and read: all chosen upper and lower words in shared order
- Effect, schedule, commit: concatenate both sides with the same indices then test equality
- Termination/output: Boolean acceptance or witness index sequence
- Defining variants: nonempty witness; bounded search wrapper
- Representative sources: CH12:L541-555;N12:L241-291
- Distinguishing test: the same tile-index sequence must make upper and lower concatenations equal

## C066 — `probabilistic-cellular-automaton`

- Leads: L0631, L1136
- Carrier/domain: fixed lattice or graph of discrete cell states / binary cells on a regular lattice
- Initialization: initial configuration plus local outcome probabilities / simple configuration such as all white plus a deterministic CA rule
- Acting loci and read: all cells read bounded neighborhoods / ordinary CA neighborhoods plus an externally chosen center-cell random event
- Effect, schedule, commit: sample a local rule outcome per cell and synchronously commit the random next configuration / synchronous CA evolution with one random center recoloring each step; relative ordering unstated
- Termination/output: normally unbounded; output is a sample path or distribution over configurations / normally unbounded; state or spacetime history
- Defining variants: mixtures of two or more local rules and probability parameters / random injection versus randomness confined to the initial condition
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L897-898 / BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes/06-Starting-from-Randomness-Notes.md:L15-17
- Distinguishing test: the same state and parameters can yield different next configurations / same initial state and rule can diverge across runs because fresh randomness enters after time zero

## C067 — `probabilistic-cellular-automaton-fitting`

- Leads: L1523
- Carrier/domain: spacetime lattice histories
- Initialization: training histories neighborhood shape and random sampler
- Acting loci and read: each observed spacetime neighborhood and successor
- Effect, schedule, commit: count conditional outputs then sample every new cell from its learned distribution
- Termination/output: generated history or fitted local distributions
- Defining variants: neighborhoods; synchronous sampling
- Representative sources: CH10:L461-477
- Distinguishing test: probabilities are conditioned on local spacetime neighborhoods and used to generate a new CA history

## C068 — `program-based-statistical-test`

- Leads: L1524
- Carrier/domain: dataset and randomized surrogate datasets
- Initialization: observed input randomization law program and comparison statistic
- Acting loci and read: whole observed and randomized inputs
- Effect, schedule, commit: run the same program on observed and surrogate inputs then compare outputs
- Termination/output: significance score rank or decision
- Defining variants: program choices; randomization ensembles
- Representative sources: CH10:L515-533
- Distinguishing test: an arbitrary executable program supplies the statistic being calibrated

## C069 — `random-functional-graph`

- Leads: L1226
- Carrier/domain: n labeled nodes with one directed successor slot each
- Initialization: a fixed node count n and no pre-existing arcs
- Acting loci and read: each node independently reads the complete set of possible successor labels
- Effect, schedule, commit: choose one successor uniformly for every node; one-shot graph construction
- Termination/output: ends after n choices; outputs a functional digraph with cycles and in-trees
- Defining variants: node count n; independently sampled successor assignments
- Representative sources: BACK-MATTER/NOTES/06-Starting-from-Randomness-Notes/06-Starting-from-Randomness-Notes.md:L589-590
- Distinguishing test: every node has outdegree exactly one and the graph is sampled once rather than evolved by rewrites

## C070 — `random-lattice-percolation`

- Leads: L1391
- Carrier/domain: a finite or infinite lattice with independently occupied sites and an adjacency relation
- Initialization: occupy each site randomly at density p
- Acting loci and read: a global connectivity observer reads occupied connected components
- Effect, schedule, commit: one-shot random configuration followed by a spanning-cluster test; no temporal transition
- Termination/output: ends after sampling and connectivity analysis; outputs clusters or a percolation boolean
- Defining variants: square or triangular lattice; undirected or directed connectivity; density p
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L497-498
- Distinguishing test: classification changes with global spanning connectivity even though occupation is sampled independently

## C071 — `random-stream-coalescence`

- Leads: L1460
- Carrier/domain: discrete directed streams on a lattice
- Initialization: stream sources and random direction law
- Acting loci and read: active stream tips and occupancy at proposed destinations
- Effect, schedule, commit: advance tips randomly and irreversibly merge tips that meet
- Termination/output: fixed steps or drainage tree
- Defining variants: direction distributions; source layouts
- Representative sources: N08:L130
- Distinguishing test: two streams that meet permanently share one downstream continuation

## C072 — `recursive-function-evaluator`

- Leads: L0513, L0516, L0520, L0523, L0524
- Carrier/domain: integer arguments, recursive definitions, and a dynamic call or reduction tree
- Initialization: requested function call with base cases and combinator definitions
- Acting loci and read: a reducible call reads argument tests and may demand nested self-calls
- Effect, schedule, commit: expand and reduce calls according to evaluation order; cache or unwind where specified
- Termination/output: returns an integer or diverges or is undefined; output is the evaluated value
- Defining variants: Ackermann nesting; bounded primitive recursion; composition; unbounded minimization; eager or lazy order
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L237-268;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L316-364
- Distinguishing test: changing call-evaluation order can change definedness even when the written recurrence is unchanged

## C073 — `register-machine`

- Leads: L0193, L0202
- Carrier/domain: nonnegative integer registers plus program counter / integer registers plus program counter
- Initialization: zero or supplied registers and instruction list / register values and extended instruction list
- Acting loci and read: current instruction and addressed register / current instruction and one or more addressed registers
- Effect, schedule, commit: increment or conditional decrement-jump then update counter / perform arithmetic or comparison then branch or advance
- Termination/output: halt policy or fixed-step register and counter trace / halt policy or fixed-step machine state
- Defining variants: two registers; program presets / multiple registers; add; subtract; compare
- Representative sources: CH03:L473-509 / CH03:L519-525
- Distinguishing test: control flow is driven by zero-tested decrement-jump instructions / a single instruction may read or combine two registers

## C074 — `reversible-boolean-circuit-embedding`

- Leads: L1534
- Carrier/domain: Boolean bits with ancillas
- Initialization: input function reversible gate set and initialized ancillas
- Acting loci and read: gate-selected bit tuple
- Effect, schedule, commit: apply a finite permutation-gate sequence preserving enough outputs to invert
- Termination/output: final bits including function and garbage outputs
- Defining variants: ancilla layouts; reversible gate decompositions
- Representative sources: N10:L904
- Distinguishing test: the circuit is a permutation on full bit states even when the target function is not invertible

## C075 — `run-length-list-rewrite`

- Leads: L0502
- Carrier/domain: finite symbol list whose maximal runs are dynamically regrouped
- Initialization: short seed list such as one
- Acting loci and read: the whole list acts; each maximal equal-symbol run is read as one unit
- Effect, schedule, commit: replace every run by its length-symbol pair and concatenate for the next sequential step
- Termination/output: normally unbounded; output is the sequence of rewritten lists
- Defining variants: look-and-say seeds and equivalent large-alphabet substitution encodings
- Representative sources: BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L193-202
- Distinguishing test: a symbol replacement cannot be chosen until maximal run boundaries are known

## C076 — `self-avoiding-random-walk`

- Leads: L1370
- Carrier/domain: current lattice position together with the complete visited-site set
- Initialization: a one-site path or another simple path
- Acting loci and read: the current endpoint reads candidate neighbors and global visited-set membership
- Effect, schedule, commit: choose an unvisited neighbor randomly, append it, and permanently mark it visited
- Termination/output: target length or trapped endpoint; outputs a non-self-intersecting path
- Defining variants: direct growth; pivot or short-walk-combination samplers; dimension
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L312-313
- Distinguishing test: a move onto any earlier site is forbidden even when that site is not locally recent

## C077 — `sequence-equation-relation`

- Leads: L1555
- Carrier/domain: finite words assigned to variables
- Initialization: word equations alphabet and candidate variable assignment
- Acting loci and read: all variable occurrences within concatenations
- Effect, schedule, commit: substitute words flatten both sides and test equality
- Termination/output: Boolean acceptance or satisfying assignments
- Defining variants: multiple equations; bounded alphabets
- Representative sources: N12:L314-316
- Distinguishing test: unknowns range over finite words rather than individual symbols or numbers

## C078 — `sequence-recurrence`

- Leads: L0356, L0363, L0510
- Carrier/domain: growing indexed sequence of numeric terms
- Initialization: finite prefix supplying all initially referenced indices
- Acting loci and read: the next index acts and reads fixed offsets or value-selected earlier indices
- Effect, schedule, commit: compute and append one term, committing it before the next index is evaluated
- Termination/output: continues indefinitely or becomes undefined on an invalid dependency; output is the sequence
- Defining variants: linear fixed-lag rules; Fibonacci-like rules; value-dependent backward references
- Representative sources: CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L169-186;BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes/04-Systems-Based-on-Numbers-Notes.md:L219-268
- Distinguishing test: the written rule addresses retained terms by index, potentially reaching arbitrarily far back

## C079 — `sequential-geometric-packing`

- Leads: L1299, L1399
- Carrier/domain: nonoverlapping circles or spheres embedded in Euclidean 2D or 3D
- Initialization: one initial object plus a radius sequence
- Acting loci and read: a new object reads the geometry and contacts of the complete existing packing
- Effect, schedule, commit: place one object at a time at the nearest feasible central position; each placement is permanent
- Termination/output: target object count or no feasible placement; outputs packing and contact graph
- Defining variants: equal or unequal radii; 2D circles; analogous 3D spheres touching two existing objects
- Representative sources: CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L637-648;BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L561-562
- Distinguishing test: each committed object is chosen greedily from current geometry, not by solving the final packing globally

## C080 — `sequential-substitution-system`

- Leads: L0175
- Carrier/domain: finite-symbol string
- Initialization: seed string and ordered rewrite rules
- Acting loci and read: candidate substrings scanned left to right
- Effect, schedule, commit: replace the first selected match once per step then rescan
- Termination/output: fixed point step limit or final string
- Defining variants: first-match; text-editor replacement
- Representative sources: CH03:L369-379
- Distinguishing test: only one selected occurrence is rewritten at a step

## C081 — `similarity-preserving-template-hash`

- Leads: L1536
- Carrier/domain: structured input and layered sparse template responses
- Initialization: input templates thresholds layers and bucket map
- Acting loci and read: selected sparse features at each layer
- Effect, schedule, commit: apply layered local detectors then fold sparse responses into an address
- Termination/output: memory address or candidate bucket
- Defining variants: visual templates; multilayer sparse codes
- Representative sources: CH10:L851-879
- Distinguishing test: nearby inputs are intended to map to nearby or shared addresses rather than only exact hashes

## C082 — `spin-configuration-ensemble`

- Leads: L1387, L1389
- Carrier/domain: a finite periodic 2D array of spins in {-1,+1} with nearest-neighbor energy
- Initialization: the complete configuration space plus either target energy E or inverse temperature beta
- Acting loci and read: selection reads each configuration globally through its summed nearest-neighbor energy
- Effect, schedule, commit: no intrinsic evolution: retain an E shell or assign weight exp(-beta E) in one ensemble construction
- Termination/output: one-shot distribution; outputs weighted configurations or magnetization statistics
- Defining variants: microcanonical fixed-energy shell; canonical Boltzmann weighting; Monte Carlo is auxiliary sampling
- Representative sources: BACK-MATTER/NOTES/07-Mechanisms-in-Programs-and-Nature-Notes/07-Mechanisms-in-Programs-and-Nature-Notes.md:L422-459
- Distinguishing test: within one energy shell weights are equal; across energies the canonical weight ratio is exp(-beta deltaE)

## C083 — `spring-threshold-fracture`

- Leads: L1449
- Carrier/domain: spring-bond particle lattice
- Initialization: particle positions identical springs loads and break threshold
- Acting loci and read: incident spring lengths and forces
- Effect, schedule, commit: integrate deformation and irreversibly delete springs beyond stretch threshold
- Termination/output: break event or fixed-time fracture state
- Defining variants: force laws; loading schedules
- Representative sources: N08:L59
- Distinguishing test: bonds fail from dynamic stretch rather than preassigned random strength

## C084 — `stochastic-frontier-aggregation`

- Leads: L1274
- Carrier/domain: an occupied-cell cluster on a discrete lattice
- Initialization: normally one occupied seed cell
- Acting loci and read: an eligible empty frontier site and its local occupied-neighbor pattern
- Effect, schedule, commit: sample one eligible frontier site and add it irreversibly; one-cell sequential commit
- Termination/output: fixed cluster size or no eligible site; outputs the occupied cluster
- Defining variants: Eden A or B sampling; neighbor templates; lattice and dimension
- Representative sources: CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L417-428
- Distinguishing test: the next cell is sampled directly from the frontier rather than selected by a probing random walk

## C085 — `stochastic-local-search`

- Leads: L1286, L1290, L1292
- Carrier/domain: a finite binary array or cyclic string plus a constraint-violation cost
- Initialization: a randomly chosen configuration
- Acting loci and read: one randomly chosen cell and the global cost before and after its proposed flip
- Effect, schedule, commit: sequential proposal; accept on cost decrease or, in the nonworsening variant, equal cost
- Termination/output: exact satisfaction, step budget, or a stalled local minimum; outputs incumbent pattern and cost
- Defining variants: strict-improvement; nonworsening plateau moves; one- or two-dimensional constraint sets
- Representative sources: CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L553-596
- Distinguishing test: on a neutral flip the strict variant rejects while the plateau-crossing variant accepts

## C086 — `stochastic-random-walk`

- Leads: L1269
- Carrier/domain: one particle position on a discrete lattice
- Initialization: a starting site
- Acting loci and read: the current position and the locally allowed displacement set
- Effect, schedule, commit: choose one displacement randomly and commit one sequential move per step
- Termination/output: fixed step budget or indefinite; outputs current position or the full path
- Defining variants: step lengths; dimensions; square or hexagonal lattices; sources and boundaries
- Representative sources: CHAPTERS/07-Mechanisms-in-Programs-and-Nature/07-Mechanisms-in-Programs-and-Nature.md:L393-410
- Distinguishing test: a proposed return to a visited site is allowed, unlike a self-avoiding walk

## C087 — `stochastic-spacetime-causal-network`

- Leads: L1505
- Carrier/domain: points in continuous spacetime
- Initialization: sampling region density metric and causal-order rule
- Acting loci and read: sampled event pairs and intervening events
- Effect, schedule, commit: sample events connect future-cone pairs then remove transitive shortcuts
- Termination/output: finite causal graph
- Defining variants: region shape; density; dimension
- Representative sources: N09:L816-818
- Distinguishing test: edges are the transitive reduction of causal order among randomly sampled spacetime events

## C088 — `stored-program-random-access-machine`

- Leads: L1546
- Carrier/domain: addressed bit memory program counter and instruction register
- Initialization: memory image program and entry address
- Acting loci and read: address named by current instruction
- Effect, schedule, commit: fetch decode execute write memory then increment or branch counter
- Termination/output: halt state or machine trace
- Defining variants: stored data and opcodes; compiled or interpreted front ends
- Representative sources: N11:L15-23
- Distinguishing test: instructions and data occupy addressed memory accessed by a program counter

## C089 — `symbolic-expression-rewriting`

- Leads: L0203, L0316, L1541
- Carrier/domain: expression trees and pattern rules
- Initialization: initial expression and ordered rules
- Acting loci and read: matching subtrees under a structural scan
- Effect, schedule, commit: apply nonoverlapping matches in a defined scan order and commit a new tree
- Termination/output: fixed point step limit or expression trace
- Defining variants: left-to-right; apply-once; arbitrary patterns
- Representative sources: CH03:L531-537;N03:L823-835;CH10:L909-915
- Distinguishing test: matches are structural expression subtrees rather than flat string positions

## C090 — `synchronous-local-state-automaton`

- Leads: L0231, L0244, L0245, L0429, L0430, L0431, L0657, L0876, L0891, L0920, L1447
- Carrier/domain: staggered or hexagonally drawn 1D cells / 1D finite-color CA configuration / finite algebra-valued lattice / continuous-valued temperature lattice / fixed lattice, tiling, or graph whose nodes carry discrete or real local states
- Initialization: initial finite-color row with boundary policy / seed and ordered component rules / seed values and finite binary operation table / initial temperatures heating rate and neighborhood / complete initial node-state assignment, fixed adjacency, and optional node-rule labels
- Acting loci and read: two predecessor cells / component neighborhood for each component pass / left neighbor and current cell / all local temperatures in averaging neighborhood / every node acts and reads a bounded neighborhood in the fixed domain
- Effect, schedule, commit: update all cells synchronously from a two-input rule / apply two or more CA rules sequentially inside each macro-step / apply the algebra operation synchronously at every cell / average synchronously add heat and keep fractional part above threshold / compute all node values from the old state and synchronously commit one new state
- Termination/output: fixed-step spacetime or final row / fixed macro-step trace or final configuration / fixed-step lattice or trace / fixed-step temperature and bubble-event trace / normally unbounded or reaches a cycle or fixed point; output is the configuration orbit
- Defining variants: multicolor; base-k rule encoding / noncommuting order; effective larger radius / semigroup; group; non-Abelian; table-defined / heating rates; neighborhoods / one to three dimensions; irregular tilings; real-valued cells; homogeneous or node-specific rules
- Representative sources: N03:L135-150 / N03:L190 / N03:L192-225 / N08:L51 / CHAPTERS/04-Systems-Based-on-Numbers/04-Systems-Based-on-Numbers.md:L546-551;CHAPTERS/05-Two-Dimensions-and-Beyond/05-Two-Dimensions-and-Beyond.md:L27-34;BACK-MATTER/NOTES/05-Two-Dimensions-and-Beyond-Notes/05-Two-Dimensions-and-Beyond-Notes.md:L474-482
- Distinguishing test: each output has exactly two predecessor inputs instead of an odd centered neighborhood / one reported step contains multiple ordered CA rule applications / the local rule is the multiplication table of a finite algebra / threshold crossing wraps temperature by its fractional part to model latent heat / topology stays fixed and every node has exactly one committed next value per step

## C091 — `tag-system`

- Leads: L0181, L0186
- Carrier/domain: finite-symbol queue-like sequence / finite-symbol queue plus cyclic block pointer
- Initialization: initial sequence deletion number and append table / initial sequence ordered block cycle and phase
- Acting loci and read: fixed prefix removed from the front / first symbol and current scheduled block
- Effect, schedule, commit: delete prefix then append a block chosen from removed symbols / remove one symbol advance phase and conditionally append scheduled block
- Termination/output: empty or unmatched halt; otherwise trace and sequence / empty halt or fixed-step sequence and phase
- Defining variants: one-deletion; two-deletion; append tables / two-block alternation; longer cycles
- Representative sources: CH03:L423-445 / CH03:L447-471
- Distinguishing test: the rule always consumes a fixed front prefix and appends at the rear / append choice is fixed by a cyclic phase rather than by a lookup on the full prefix

## C092 — `turing-machine-partial-function`

- Leads: L1552
- Carrier/domain: Turing tape head and finite control
- Initialization: encoded input tape transition table and halt-readout policy
- Acting loci and read: current state scanned symbol and tape boundary
- Effect, schedule, commit: write symbol change state move head until halt predicate
- Termination/output: value on halting inputs; undefined otherwise
- Defining variants: halt state; boundary escape; fixed point; tape-pattern readout
- Representative sources: CH12:L571-607;N12:L207-209,L235-237,L365-369
- Distinguishing test: nonhalting evolution denotes no function value rather than an infinite output trace

## C093 — `weighted-history-sum-relation`

- Leads: L1508
- Carrier/domain: admissible histories or field configurations
- Initialization: boundaries action functional and complex weighting convention
- Acting loci and read: each complete history or configuration
- Effect, schedule, commit: compute action weight and sum or integrate contributions
- Termination/output: complex amplitude or correlation with cutoff or measure
- Defining variants: history paths; continuous fields; discretized cutoff
- Representative sources: N09:L880,L955-957
- Distinguishing test: output combines all admissible histories rather than selecting or evolving one

## C094 — `xor-stream-cipher`

- Leads: L1525
- Carrier/domain: bit plaintext key state and keystream
- Initialization: plaintext key or generator seed and sampling policy
- Acting loci and read: next plaintext bit and next keystream bit
- Effect, schedule, commit: XOR aligned streams sequentially; same operation decrypts
- Termination/output: ciphertext or recovered plaintext
- Defining variants: repeating key; LFSR or additive CA; sparse rule-30 samples
- Representative sources: CH10:L539-565,L599-605
- Distinguishing test: encryption is bitwise XOR with a separately generated aligned stream

## C095 — `fixed-comparison-sorting-network`

- Leads: L1556
- Carrier/domain: finite ordered values on a fixed set of indexed wires
- Initialization: input list plus a fixed ordered or layered sequence of index pairs
- Acting loci and read: each comparator reads exactly its two addressed wires; disjoint comparators in one layer may act in parallel
- Effect, schedule, commit: replace the pair by its ordered minimum/maximum values and advance to the next comparator or layer
- Termination/output: after the fixed schedule ends, output the resulting list; a valid sorting network sorts every input ordering
- Defining variants: transposition, insertion, Batcher, Green, repetitive, nested, and irregular comparator schedules
- Representative sources: N12:L331-347,L461-476; `BACK-MATTER/NOTES/_page_1157_Figure_7.jpeg`
- Distinguishing test: comparator locations are fixed independently of input values, and a compare-exchange gate is generally non-injective, unlike a reversible Boolean or unitary gate

## C096 — `priority-dovetailed-oracle-construction`

- Leads: L1564
- Carrier/domain: two monotonically growing Boolean oracle approximations, an enumeration of suspended register-machine work states and outputs, and priority/scheduler state
- Initialization: all-white bottom rows, enumerated register programs, initial simulations and requirements, and an optional queried row/address
- Acting loci and read: a fair finite subset of simulations reads private machine state and the complete current shared approximation; the controller reads displayed agreements and requirement state
- Effect, schedule, commit: dovetail selected simulations, expose outputs, enumerate diagonalizing black cells, and update or invalidate affected lower-priority work in one coupled stage
- Termination/output: a query halts exactly when its selected bottom cell becomes black; the global construction yields two growing incomparable approximations and their finite-stage trace
- Defining variants: equivalent universal embedded machines; fair schedules; one-table diagonal variants; priority and injury encodings
- Representative sources: N12:L80-92; `BACK-MATTER/NOTES/_page_1146_Figure_2.jpeg`
- Distinguishing test: one shared approximation write can invalidate another suspended computation's displayed agreement, requiring fair later attention and priority injury that no single register-machine state supplies

## C097 — `weighted-prefix-block-transduction`

- Leads: L1511
- Carrier/domain: a finite sequence partitioned into configured fixed blocks plus a binary prefix tree
- Initialization: input blocks and empirical or supplied weights, with either an existing code tree or tree-building state
- Acting loci and read: tree construction reads current node weights; encoding reads one fixed block and its codeword
- Effect, schedule, commit: repeatedly combine least-weight nodes, then map blocks independently to prefix-free leaf codewords; decoding consumes bits to a leaf
- Termination/output: tree/preamble plus concatenated codewords, or decoded blocks
- Defining variants: one- or two-dimensional block shape; supplied or empirical weights; fixed or dynamically updated Huffman tree
- Representative sources: CH10:L189-205,L235-249;N10:L87-106
- Distinguishing test: every block contributes a separately decodable prefix-tree leaf word rather than refining one interval for the complete message

## C098 — `nested-interval-symbol-transduction`

- Leads: L1512
- Carrier/domain: a finite symbol sequence, cumulative probability partition, and numeric interval
- Initialization: input, probabilities, interval `[0,1]`, cursor, and exact or finite-precision convention
- Acting loci and read: the next symbol, current interval, and probability partition
- Effect, schedule, commit: replace the current interval by the symbol-selected subinterval and finally emit a shortest tag; decoding reverses refinements
- Termination/output: final interval tag or decoded sequence
- Defining variants: fixed or adaptive probabilities; renormalization; block alphabets
- Representative sources: N10:L108-121
- Distinguishing test: every symbol refines one interval shared by the entire message, so there are no per-symbol codeword boundaries

## C099 — `history-reference-record-transduction`

- Leads: L1513
- Carrier/domain: an ordered sequence or scanned region, consumed prefix, dictionary/window state, and literal/reference records
- Initialization: input, cursor, minimum match, search or dictionary policy, and empty output
- Acting loci and read: current unconsumed input plus eligible earlier substrings or regions and dictionary state
- Effect, schedule, commit: append a configured best-match pointer or literal, advance, and update the dictionary; decoding copies from reconstructed history
- Termination/output: literal/reference stream or reconstructed carrier
- Defining variants: backward search, sliding window, bounded Lempel–Ziv dictionary, and one- or two-dimensional match geometry
- Representative sources: CH10:L209-267;N10:L123-153
- Distinguishing test: equal current symbols can produce different records because the decision depends on already consumed history

## C100 — `recursive-uniform-region-decomposition`

- Leads: L1514
- Carrier/domain: a finite array and rooted hierarchy of spatial regions
- Initialization: root region, sample values, split geometry, uniformity tolerance, and optional minimum scale
- Acting loci and read: one pending region and all samples it contains
- Effect, schedule, commit: emit a uniform leaf or replace the region by configured children and recurse; inverse mode fills leaves into an output array
- Termination/output: region tree or reconstructed array
- Defining variants: dimension, quadtree geometry, equality or lossy tolerance, and minimum feature size
- Representative sources: CH10:L233-239,L269-279;N10:L154-168
- Distinguishing test: every decision belongs to a nested containment tree rather than a flat maximal-run scan or global basis projection

## C101 — `orthogonal-basis-coefficient-transform`

- Leads: L1515
- Carrier/domain: a finite numeric signal or image block, basis operator, coefficient vector, and reconstruction block
- Initialization: samples, invertible basis, coefficient ordering, retention or quantization policy, and inverse convention
- Acting loci and read: the complete transform block and basis; selection reads the complete coefficient vector
- Effect, schedule, commit: project onto basis coefficients, discard or quantize selected coefficients, and optionally invert
- Termination/output: coefficient representation or reconstructed approximation
- Defining variants: Walsh, Fourier/cosine, wavelet, basis ordering, coefficient budget, and quantization
- Representative sources: CH10:L281-305;N10:L181-288
- Distinguishing test: each coefficient algebraically mixes many samples, and discarding one can change the global reconstruction

## C102 — `predictive-residual-transduction`

- Leads: L1520
- Carrier/domain: a numeric sample stream, fitted predictor state, and residual/code stream
- Initialization: samples, predictor order, fitting window/objective, residual quantizer or codebook, and initial history
- Acting loci and read: the current sample, retained preceding samples, and current or fitted coefficients
- Effect, schedule, commit: fit or update a predictor, emit the next residual or code index, reconstruct if requested, and advance
- Termination/output: model parameters plus residual records, or reconstructed samples
- Defining variants: first differences; window and predictor order; fitted or supplied coefficients; residual vector codebooks
- Representative sources: N10:L424
- Distinguishing test: output is error relative to a causal history model, not a fixed global projection or prior-substring pointer
