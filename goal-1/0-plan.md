# Goal 1: Book-Grounded Universal Construction Design

Shorthand: `UNIVERSAL-CONSTRUCTIONS`

> **Source location for subsequent work:** use
> [`ref/A-New-Kind-of-Science/Contents.md`](../ref/A-New-Kind-of-Science/Contents.md)
> and the 29 canonical documents it links. This completed goal's embedded
> source-line records are historical evidence for its conclusions, not the
> citation surface for new implementation work.

## Big-Picture Objective

Derive the simplest coherent constructive API capable of representing every catalog entry in `ref/notes/CA-Types.csv` without family-specific rollouts, semantic disguises, fallback paths, or speculative universal abstractions.

For each of the 45 catalog entries, exhaustively collect the relevant textual evidence from the local *A New Kind of Science* Markdown, extract the construction and its variants and parameters, compare it with `simple_programs.md` and the current `src/ca` runtime, determine the smallest honest semantic reuse or extension permitted by `principles.md`, and produce an implementation-ready Goal 2 stage handoff. After every type, fold the finding back into this plan and re-evaluate the cohesion of the whole design.

Goal 1 is research, architecture, and implementation planning. It does not implement the expanded runtime.

## Authoritative Inputs

- `principles.md`: governing design constraints. Its Principle 0 outranks literal adherence to this plan.
- `simple_programs.md`: current proposed generator semantics to test, not presumed truth.
- `src/ca/`: current executable runtime to inspect in full.
- `tests/`: current behavioral evidence and runtime contracts.
- `ref/notes/CA-Types.csv`: authoritative 45-row coverage index.
- `ref/notes/CA-Types.md`: taxonomy and search-vocabulary seed, not a substitute for book evidence.
- `ref/A-New-Kind-of-Science/Contents.md` and its 29 linked documents: canonical local book source for subsequent lookup and citation.
- The completed Goal 1 stage records: historical excerpt inventories and construction-analysis evidence.

## Non-Negotiable Constraints

1. Evidence precedes abstraction. Do not decide how a type fits before collecting and reading its book evidence.
2. Treat catalog types and proposed structural families as hypotheses.
3. Preserve defining semantics. Do not compile a construction into a CA, pack the whole machine into an opaque value, or route it through unrestricted `FORMULAIC` merely to claim coverage.
4. Do not force constraints, derivatives, distributions, observations, and mutations into one result type unless the evidence demonstrates a meaningful shared algebra.
5. Do not add a flag, special case, compatibility shim, fallback conversion, second rollout path, hidden executor state, fake fixed capacity, or weakened test to make a type fit.
6. One reference executor is a desired result only where semantics are genuinely shared. A vacuous executor that delegates the entire system to an arbitrary callback is failure.
7. Keep program semantics, trace representation, ANKoS encoding, batching, and visualization distinct.
8. Goal 1 does not modify `src/ca`, tests, or the root API documents. It records evidence, architecture decisions, rejected alternatives, and Goal 2 plans in `goal-1/`.
9. If a type breaks the current design, reopen affected earlier stages and revise the global plan. Do not protect previous conclusions.
10. Every catalog row must remain traceable even when several rows resolve to one shared construction.

## Current Facts

- `ref/notes/CA-Types.csv` has one header and 45 catalog rows.
- The 45 `ca_type` values are nonempty and unique; the stable `T01` through `T45` mappings in this plan cover each row exactly once.
- `principles.md` contains 17 numbered principles, including Principle 0.
- `simple_programs.md` currently specifies a `t+0D` through `t+3D` trajectory model with selectors, neighborhoods, writable frontiers, and per-target rules.
- `simple_programs.md` currently limits neighborhoods to current-state reads (`Delta t = 0`), writes values at a fixed next-state support in parallel, and copies non-frontier values forward.
- The eleven top-level `src/ca` Python modules are `__init__.py`, `alphabets.py`, `datasets.py`, `frontiers.py`, `loci.py`, `neighborhoods.py`, `rng.py`, `rollout.py`, `rules.py`, `seeds.py`, and `specs.py`; the package also exposes visualization modules.
- The current `src/ca` runtime supports only `t+0d` through `t+3d`, spatial rank zero through three, and a `time_slice` frontier. `specs.py` resolves six named Phase 1 rule/neighborhood families.
- `rollout.py` dispatches through family-name branches for AR2, Dyadlags, Lagcounts, and spatial Dyadrads/Dyadaxes rather than executing one shared selector/rule/update algebra.
- Current temporal families use seed prefixes or packed local history inside family-specific rollout code; ordinary spatial lookup uses selector reads and current-time snapshots.
- The current seed catalog separates selector-backed support from rendering, but `fractal` and `spiral` accept predicate callables and therefore remain current-runtime behavior to audit, not presumed Goal 2 primitives.
- The canonical monolithic book file has numbered content through line 22,498 (`wc -l` reports 22,497 because the final line has no terminating newline) and includes chapter text, captions, notes, index, and colophon material.
- There are no pre-existing `goal-*` folders at scaffold creation time; this is `goal-1`.
- At Foundation start, the `types` worktree was clean and `goal-1/` contained only `0-plan.md`, `0-loop.md`, and `0-prompt.md`; no stage, evidence index, design ledger, or Goal 2 handoff existed.
- Execution status at this sync is Goal 1 complete: Foundation, all 45 type stages, D141 synthesis, and the dependency-aware Goal 2 handoff are closed with no stage reopened or unresolved. `architecture-audit.md` remains authoritative for D000-D118; T06, T07, T08, T10, T11, T14, T15, T18, T21, T22, T23, T24, T25, T26, T28, T32, T33, T35, T36, T38, T40, and T42 are complete under D119-D140, and D141 integrates the catalog-wide result.
- The governing abstraction is a finitely described `SimpleProgram`, not a cellular-automaton library: CONFIGURATION labels or structures support/topology within a dimensional DOMAIN subject to invariants; rule-firing FRONTIER, access-pattern NEIGHBORHOOD, typed RULE writes/replacements, and UPDATE composition/schedule run through one branch-free runner. SEED is a first-class library/run responsibility that supplies one complete valid event-zero configuration, but concrete seed/constructor, realization, horizon, and external stop are RunSpec/preset identity rather than transition-program identity. Cellular automata are one preset of the transition axes.
- DOMAIN names the task/program's dimensional space (`t+0D`, `t+1D`, and so on), with discreteness or continuity explicit. CONFIGURATION declares its native support/topology and invariants. ALPHABET names its value schema, including products/tagged unions. Numeric carriers, head-state sets, address sets, and function definition sets are not separate DOMAINs.
- Representation reuse is accepted only with a lossless map `e` satisfying `map_step_result(e, step_A(s)) = step_B(e(s))` one step for one step, preserving complete state, outcome, successors/branching, events, witnesses, and provenance while requiring no hidden source interpreter. Opaque singleton packing and callbacks remain invalid.
- The three evidenced rollout nonfits remain T31 constraint/model sets, T41 uniterated function definitions, and T45 general PDE relations without a specified evolution problem. T40's exact-denotation/representation-query layer is an arity-zero classes-1–3 specialization of D082/T41 and likewise remains outside rollout; its explicit coefficient algorithms are separately identified work SimplePrograms. Multiway rewriting remains a SimpleProgram whose structured UPDATE result contains a finite successor set plus complete branch witnesses.
- T37 establishes a consecutive exact numeric prefix with an explicit value-carrier profile as state, normalized affine fixed-lag programs, minimal seeds and replay-verified checkpoints, and old-prefix term references. Its bijective `Val* · End(next_index)` encoding turns append into the RULE `End(n) -> Val(n,next) · End(n+1)` and reuses T16 exactly-one ordered splice. Compact seed-plus-event traces reconstruct every nested prefix; a lag window is only a non-injective evaluator quotient. The six page-143 rows, source erratum, factorial/Lucas/Perrin, and AR2/T38/T43 boundaries are exact. T37 left Ulam for T39; the T39 result below now resolves it compositionally.
- T38 keeps that complete prefix, unique endpoint, complete-prefix NEIGHBORHOOD context, endpoint replacement, splice, trace, `StepResult`, and branch-free runner. Its only class-2 responsibility is closed `TermAt(AddressExpr)` syntax and leftmost-innermost demand/failure witnesses inside RULE. Fixed lag is a restriction; resolver-plus-emitter splitting is only a lossless compiled factorization. Undefined demanded addresses and results outside the declared carrier use the common no-commit error protocol; malformed programs remain invalid. D138 adds no T38 selector, NEIGHBORHOOD type, state, FRONTIER, UPDATE, executor, or family branch.
- T40 is an immutable arity-zero exact denotation plus a pure typed positional/simple-continued-fraction representation query. The complete denotation specification and selection form query identity; evaluation context remains separate, while provenance binds both. Coefficient payload, proof-strength outcome, and termination are independent. Terminating positional values retain an infinite zero tail; finite simple continued fractions complete canonically; `a0` is signed and only its tail is positive.
- Long division, strict integer-safe square-root extraction, its proved fixed-program reachable-state quotient, and Gauss residual iteration are optional discrete `t+0D` work SimplePrograms over existing axes, not T40 state or a new executor. Direct nth-coefficient access supplies a concrete counterexample to mandatory prefix rollout. Alternative unary/Gray/negative-radix/non-power/multiplicative/self-delimiting/Fibonacci codecs require closed representation tags and invariants, not family execution.
- D139 closes T40 through classes 1–3 with 447 retained source rows, the complete 897-row actual Index, 63 hash-bound raster candidates, exact/certified/partial/resource/unsupported/unknown/approximate/probable/failure results, replay-verified T42 handoffs, and 72 hostile rejections. No umbrella-native T40 transition CONFIGURATION or DOMAIN, T40 FRONTIER, NEIGHBORHOOD, UPDATE, executor, family branch, hidden callback/CAS object, or float coefficient is added; explicit work programs retain their own visible state and axes.
- T42 is a finite visibly scheduled binary-substitution preset, not an online coefficient stream or new construction family. Its canonical executable carrier is a nonempty uniform word over `PhaseIndex[0..L] x Bit`; a required generic `phase<L` applicability restriction composes with T13 `AllOccurrences`, `Self`, closed nonempty word emission, and D019 ordered concatenation. Phase `L` returns common `ScheduleExhausted` with the final word retained and no D019 commit.
- D140 closes T42 through classes 1–3. A T40 source must be a complete replay-verified result; natural coefficients drop signed `a0` and reverse the positive tail exactly once, so `m` terms yield `m-1` events and longer horizons prepend rather than resume. Explicit schedules use a separate closed tag. Compact/tagged words are lossless interfaces; the uniform product word is the sole plain-`Self` T13 lowering. Strict seed `(0,)` is initial preset/run configuration, not transition-program identity. No T42 state/axis kind, selector class, UPDATE, executor, family branch, callback, raster program, or class-4 algebra is added.
- D141 closes synthesis with one branch-free transition/rewrite algebra for every row that actually supplies canonical evolution and one sibling immutable definition/relation/query/certificate algebra for the six strict-layer non-rollout rows T31-T33, T40-T41, and T45. T40 is an arity-zero reuse of the declarative category, not a fourth nonfit kind. Keyed, ordered/ranked, bag, graph, and finite-successor UPDATE forms are sealed axis implementations, not catalog executors.
- The architecture stage-disposition table and Goal 2 coverage matrix now each contain every T01-T45 exactly once. Goal 2 implements shared substrates once and retains one dependency-aware leaf conformance obligation per catalog row.
- Most catalog deltas are presets, restrictions, invariants, representations, closed rule data, or new axis-policy values. Replacing the current tensor-only carriers and family-branched `src/ca` rollout is nevertheless a substantial one-time substrate refactor; the package is migrated in place with no second library, legacy executor, or second semantic/execution compatibility fork. A lossless deprecated construction façade may map directly to the ordinary program representation without becoming another path.
- T39 evidence splits one actual transition construction from two pure categories: the consecutive-divisor sieve owns survivor-removal events, while structural integer filters/streams and pointwise arithmetic measurements have no update law.
- The strict sieve uses a visible `next_divisor` marker and distinguishes every proper-multiple hit from newly removed candidates. Composite rows advance even when membership does not change. On finite ordered support, a Boolean membership field plus marker is bijective with the ordered-survivor pack; RULE emits ordinary candidate false-writes plus the marker write and generic old-snapshot UPDATE commits them. Infinite membership is intensional. No subset-removal class is required.
- The literal page-147 profile really retains `1`: all 1,200 stage cells match the stated update and the final black set is `{1} union primes<=100`, while bottom labels omit `1`. The mathematical preset therefore starts at 2 explicitly. Finite certification after divisor 10, requested rows through 13, and infinite noncompletion remain distinct.
- Page 148's six prime profiles are observers and page 150's five rows are closed measurements with exact ordering/sign/zero conventions. Their horizons, endpoints, extrema, OCR repairs, `PrimePi` wording, and `LogIntegral` normalization are independently pinned.
- T39 resolves T37's Ulam question through `FirstAcceptedAscendingCandidate` over the complete old prefix followed by the existing append. The source prefix proves unordered pairs of distinct old indices; no fixed-lag extension or hidden pair-sum cache is introduced.
- T41 is a non-transition category: an immutable unary closed-function definition declares exact parameters, a real/complex argument set, a scalar/fixed-vector output schema, a closed ordered expression, primitive version, partiality, and branch/continuation profiles. Point/sample/zero/crossing/extremum requests and their exact/certified/approximate/undefined/failure results are pure scoped records outside UPDATE/rollout.
- Structural identity, certified functional equivalence, and observation equality remain distinct. Exact literals/algebraics/complex values are lossless; viewport, mesh, evaluator, precision, samples, rasters, sounds, histograms, and spectra do not enter function identity.
- The four strict and eight Notes rasters are fully inventoried. Exact page-161 periods/zero families and endpoint conventions, the page-162 tangent/crossing count seam into T42, pole/branch segmentation, finite/infinite series separation, zeta analytic continuation, continuous Riemann-Siegel phase, and declared-precision values/numerical zero counts are pinned.
- Source repairs remain visible: monolith image links are broken, page numbers are offset, the Notes ODE derivative `2` denotes a different curve than claimed, critical-line zeta needs continuation/phase, and the displayed `a=0` infinite lacunary sum cannot converge ordinarily.
- T43 is one ideal real scalar in an explicit state interval under an immutable closed self-map plus a separately identified fixed numerical realization. Its DOMAIN is discrete `t+0D`; certified/tracked evaluator work state and represented feedback state do not masquerade as the exact mathematical point.
- T43 reuses T34's singleton FRONTIER, complete old-value read, generic same-locus write, and atomic UPDATE unchanged. A strict fixed point still advances unchanged, and `h` events always yield `h+1` snapshots.
- Strict map syntax reuses T41 responsibilities with state references, exact predicates, ordered piecewise arms, source-faithful `FractionalPart`, and a distinct modulo-one primitive. Mathematical map ID, realized-transition ID, certified equivalence, conjugacy, profile-specific orbit equality, and finite observation equality remain distinct.
- T43 numerical evidence separates ideal exact, certified enclosure, tracked significance, fixed binary, and fixed decimal feedback. Binary shift profiles collapse at events 50/52; the reconstructed decimal profile has a 12-event preperiod and period 195,312,500.
- Exact rational regeneration matches all 12,960 page-165 cells. A reproducible declared-180-decimal classifier matches all 29,040 page-168 and 38,720 page-170 cells; all eleven strict/Notes asset hashes match. The missing page-166 plate and underdetermined Notes pixel contexts are explicit rather than invented.
- Source repairs include detached/reordered strict formulas, the missing page-166 plate, page-layout sentence interleaving, a false arbitrary-rational-`a` repetition claim, source-faithful negative `FractionalPart`, corrupted logistic/fast-forward formulas, and the integer-torus versus nonintegral-rational closed-box reading of the `{1,1}` vector witness.
- Digit/value/sensitivity/cycle/Lyapunov/attractor/bifurcation/symbolic/fast-forward/rendering records remain analyzers. Sensitivity does not prove intrinsic randomness; a finite orbit/raster does not prove an attractor, asymptotic exponent, or bifurcation boundary.
- T43 preserves T37 prefix, T42 substitution, T44 lattice aggregation, and T45 continuous-time boundaries. Current finite alphabets, callbacks, family rollout, NumPy arrays, and raw exporters remain semantic mismatches.
- T44 is a total real-valued field on fixed ordered one-dimensional support. Every event reads the complete old left/self/right triple, applies a closed affine aggregate and closed scalar map, returns typed same-site writes, and reuses T01's atomic snapshot UPDATE.
- Strict-main integer-line topology is an explicit inference; Notes separately prove a finite periodic list. Segment exterior policy, causal work/halo, raster crop, and support identity remain independent. Exact field state, certified/tracked computation records, and represented finite-arithmetic feedback are distinct.
- Mean, fractional-`3/2`, add-constant, weighted, additive, boiling, coupled-map, noisy, probabilistic, complex-block, and PDE-related profiles retain the exact evidence boundaries established in D096-D102. Backgrounds, differences, parameter/class galleries, bubble/wrap records, and renderings are observers rather than hidden state or halts.
- T44 closes 21 reproducible search queries and 25 evidence groups with zero unresolved candidates. Exact semantic rows, all 17 included asset identities, the page-339 exclusion, and page-172/173/174/175/Notes raster fits reproduce; all 102 repository tests pass.
- T45 is a non-transition category: an immutable closed differential equation plus continuous region, parameterized-locus side data, `Classical` solution concept, and regularity contract denotes a solution set of real-scalar, complex-scalar, or fixed-real-vector fields. It has no native UPDATE unless a separately posed evolution derives one.
- Closed multivariate binders, derivative multi-indices, fixed matrices, reusable candidate/trace bound expressions, and explicit versioned equation-class/locus/admissibility claims preserve the equation/problem/candidate/witness/realization/sample/view distinctions. Only a separately justified IVP derives a continuous flow.
- T45 closes a 27-query exact-manifest oracle and 28 evidence groups with zero unresolved candidates. All 87 excerpts match their provenance; 23 included assets plus the Chapter 5 exclusion, exact semantic/metadata oracles, the heat raster fit, and all 102 repository tests pass. D103-D110 preserve proof strength, Classical-only v1 scope, explicit numerical relations, separate scopes/observers, and T31/T41/T44 reuse.
- T02 is the `k>=3`, radius-one finite-alphabet parameterization of T01. It reuses fixed ordered support, `AllSites`, old left/self/right reads, typed same-site assignment, atomic commit, deterministic continuation, realization, and trace semantics without a new executor or update law.
- A T02 program is primarily an explicit ordered alphabet plus one complete `k^3`-entry table. Its optional Wolfram base-`k` codec uses positional address `k^2*l+k*c+r`, keeps `000` least significant, and requires arbitrary-precision tagged identity; already `k=4` has `2^128` possible tables.
- Alphabet rank, T03 numeric valuation, and palette tone are distinct. T03 is an exact fixed-arity equal-weight sum quotient plus a complete structural sum table; average is an exact label, sum zero is the least-significant code digit, and a noncanonical symbolic valuation defeats rank substitution. Mutation histories, reversibility, purpose searches, behavior labels, and binary emulations remain provenance/property/analyzer/relation records.
- T02 closes an exact 29-query/157-candidate search partition and 21 evidence groups with no remainder. Eleven included, six excluded, and two relation-only assets are hash-pinned; source, semantic, metadata, direct Voronoi priority-table, reversible/inverse-window, and rule-921408 raster oracles pass.
- T02 exposes current runtime defects rather than adding a branch: exhaustive arity is wrong, selector significance is mirrored, general outputs are binary-masked, ordinary lookup is not executable, and batch rule identity is coerced to fixed-width `int64`.
- T03's core aggregate semantics, definition/formula excerpts, official-source repairs, and strict code-777 raster remain valid. Its former 16-query/118-candidate, 17-query/309-candidate, and 18-query/312-candidate closures are superseded by the independently reviewed 18-query/314-candidate partition and 120-asset manifest at `50 included / 61 excluded / 9 relation-only`; the T05 code-`1004600` continuation, T06 direction-linked emulation network, and inherited page-263 slice control are closed.
- T03 reuses T01/T02 fixed support, all-site old-snapshot reads, typed assignment, atomic commit, realization, and trace semantics. D115-D118 add only explicit numeric valuation, the exact reachable-sum case set/table/codec, and typed preset/restriction/sibling boundaries; no executor is added.
- T04's strict `k=3,r=1` preset semantics are unchanged. Its repaired 12-query manifest closes 246 candidates, 75 assets at `35 included / 34 excluded / 6 relation-only`, and 150 exact reverse references; the added page-262/page-263 controls and feature-extraction relation are evidence classifications, not execution machinery.
- T05 closes an exact 11-query/142-lexical-line manifest plus five governed prose continuations and 25 linked assets: 172 candidates with zero remainder. Twelve evidence groups pin 47 provenance lines/47 fragments/40 quote lines; assets close at `5 included / 13 relation-only / 7 excluded` after independent review added four direct page-963 chart relations.
- T05 is exactly the strict finite `k>=4,r=1,A=(0,...,k-1),nu(i)=i` preset over unchanged generic T03, with `M=3k-2`, arbitrary-precision `R=k^M`, and code `1004600` pinned as a structural table. D118 is sharpened; no new primitive, executor, update law, or decision is added. All five embedded checks, independent review, diff/fence gates, and 102 tests pass.
- T06 is a typed property restriction over a strictly eligible resolved homogeneous fixed-support CA-axis program: finite typed alphabet, `AllSites`, complete fixed local reads, a closed deterministic evaluator, exactly one same-site typed label write per firing, and old-snapshot parallel update. Its predicate is `evaluate_P(exact_uniform_read_P(b)) = b`; structural ineligibility is `UnsupportedProperty`, not a false predicate result.
- Program, property claim, replayable evidence, validated selection, and run identities remain separate. The claim binds the property semantic version, structural program reference, and an alphabet-member reference whose alphabet, rank, and canonical typed value agree. Evaluator/schema version and the exact witness belong to evidence. Passing resolves to the identical program and changes no update, successor, or halt semantics.
- The local property excludes seed and realization data. A global all-`b` fixed-point claim on a finite realization additionally requires every exterior read to supply `b`; the finite causal-cone corollary also requires a finite stencil, snapshot-parallel update, finite initial deviation, and globally compatible background.
- T07 is a class-2 validated property over a resolved finite deterministic homogeneous CA-axis program and an explicit left-right action. Reflection of a program is a separate transform; a canonical orbit table is an optional class-3 lossless RULE representation. None changes state, FRONTIER, NEIGHBORHOOD reads, RULE results, UPDATE, execution, or the identity of a passing selected program.
- The authoritative T07 monolith closure has 650 lines: a reproducible 357-line bounded base plus a disjoint 293-line hostile-saturation remainder, partitioned `15 direct / 190 relevant / 25 incidental / 167 sibling-general / 179 excluded / 74 Index`. Its 397 retained pre-Index lines drive the asset audit. All 114 retained saturation additions reverse-join to split material as `103 exact + 11 pinned variants`; the bounded diagnostic separately remains `325 = 313 exact + 12 variants`. This proves reverse split coverage, not an independently exhaustive split-wording search. The final 271-asset/542-reference ledger closes at `4 included / 38 relation-only / 229 excluded`, with 271 unique hashes.
- T07 reconstructs the corrupted general count formula at `BOOK:11897`, corrects the PDE control's intended outer-coefficient relation from `p1=p2` to `p1=p3`, and keeps 64 reflection-fixed ECA rules, 160 reflection-only rule orbits, 88 reflection-plus-color `V4` orbits, and the 32-rule T06/T07 intersection distinct. D120 preserves the branch-free runner and requires one diagonal complete-read action over exact `V_P`, including admissible-space closure for generic value actions. All six embedded blocks, independent hostile review, Markdown/diff gates, and 102 repository tests pass.
- T01 validates a fixed-lattice synchronous assignment protocol only: semantic `AllSites`, ordered old-snapshot reads, an explicit exhaustive table, typed same-site assignment, and atomic parallel update.
- T01 requires semantic support, finite computation realization, and emitted trace extent to be separate. A finite `shape` is not automatically the native integer line.
- T01 found three concrete runtime defects: binary arity-three exhaustive lookup derives 4 rather than 256 rules, the current digit codec mirrors asymmetric Wolfram rules, and generic lookup cannot execute through the family-dispatched rollout.
- T09 correctly rederives the governing simple-program `FRONTIER` as rule-firing loci: it selects the unique tagged active cell. The current schema's writable-coordinate-only frontier is a CA-shaped realization that Goal 2 must broaden; the rule's typed writes may name both source and destination, and one `UPDATE` commits them atomically.
- T09 directly requires visible active-position information, exactly one active marker, atomic old-snapshot update, and full-state traces. It does not establish that these roles require a separate `SingleControl` runtime object: `Plain(bit) | Active(bit)` is a transparent lossless composite field representation.
- The canonical mobile code pair `{35,57}` consumes physical `[left,self,right]`, sharing T01's corrected MSB-first context codec. The Notes finite-list guard is not a boundary or halt policy.
- T12 combines a head-state role with the symbol under the head. Architecture reclosure withdraws the former payload-bearing `SingleControl`/`TransitionControl` requirement: the canonical transparent state may be `Plain(symbol) | Head(head_state,symbol)` (equivalently `TapeSymbol x Option[HeadState]`) with exactly one head, while a factored `(field,position,payload)` form is a lossless view only when explicitly related and validated.
- T10 keeps T09's discrete `t+1D` fixed line, transparent `Plain(bit) | Active(bit)` exactly-one state, unique firing source, and physical left/self/right read. Its exact table returns a three-bit replacement block plus `-1/+1`; a lossless lowering emits three complete labels and reuses D011 atomic finite-write UPDATE. The destination receives its new block bit. There are `16^8=2^32` rules, no source-defined integer codec, no new update law/executor, and no evidence for T11 collisions.
- T11 keeps the same discrete `t+1D` fixed binary line but uses a canonical finite active set. Every old active source reads physical `[left,self,right]` from one snapshot, returns a new source bit plus finite relative activity, and UPDATE replaces activity by the exact union of translated proposals. Owner-unique value assignments plus idempotent set union lower losslessly to complete tagged writes on `A_old union A_next` and D011 atomic commit. The local profile has derived `16^8=2^32`, no source-defined code, and a source-undefined empty-frontier continuation. D123 adds a reusable factor-composition preset, never a T11 executor.
- T12 base machines are total and non-halting, with `(2sk)^(sk)` rules. Special terminal head states, external head/tape stop observations, horizons, and errors are distinct outcomes/protocols.
- T12 requires an inspectable total/default-symbol tape over `Z`; finite read boundaries cannot supply writes or control movement beyond capacity. Numeric rule decoding uses a documented repair of an OCR-lost `k`, guarded by known machine 3024.
- T13 validates source-first generic orchestration but splits update semantics: fixed-locus assignment preserves support, while `ParallelReplaceConcat` consumes every old ordered occurrence and creates children from typed nonempty words.
- T13 state is an explicit discrete ordered sequence with finite canonical and documented infinite-support variants. Snapshot indices, occurrence lineage, finite observation, ragged trace, padding, and rendering are separate.
- T13 uses a total alphabet-closed `Sigma -> Sigma+` table. T17 and T15 independently prove epsilon for private word/edit/emission carriers without weakening T13; other scheduled/probabilistic variants remain separate.
- T14 reuses T13's finite ordered configuration, nonempty word emission, lineage, and ordered-generation concatenation. It parameterizes FRONTIER to old anchors with a right neighbor, NEIGHBORHOOD to immutable overlapping `(self,right)` reads, and the total table to `Sigma^2 -> Sigma+`; it adds no UPDATE algebra, state class, executor, or family branch.
- T14 factors D019 correctly: shared `OrderedGenerationConcat` requires exactly one source-bound emission for every selected anchor and derives the whole successor in source/child order, while T13's `AllOccurrences` preset alone requires every old occurrence to be selected. T15 later proves the private carrier is `Sigma*`; strict T14 still validates `Sigma+`. T14's unmatched rightmost occurrence is read but not copied forward.
- T14's unguarded Notes operator defines `[]->[]` and `[x]->[]` as zero-emission successors, not halts, errors, copy-forward stutters, or epsilon table rows. The page-85 raster fixes both `0110` seeds/tables/traces; page 681 contains four binary and nine three-color pair rows with singleton outputs, not a native eight-row width-three table.
- T15 is the `Sigma^2 -> Sigma*` result-validator parameterization of T14's finite-word, `HasRightNeighbor`, `(self,right)`, and `OrderedGenerationConcat` composition. Seven hash-bound binary/ternary/quaternary tables and exact `t0..t11` traces directly establish epsilon rows under the same schedule; 304,927 bounded cases commute without a new UPDATE or executor.
- T15 retains one source-bound record and a zero-length lineage interval for an explicit epsilon emission. Active `00->[]`, zero-source `[x]->[]`, and post-extinction `[]->[]` have equal successor values but distinct witnesses; T16 `NoMatch` and T17 `InsufficientPrefix` remain zero-successor terminals. Slow/balanced growth, extinction, repetition, and CA-like patches are trace properties/relations.
- T16 reuses finite ordered-word support but not T13 source coverage or commit. An immutable ordered literal program selects the lexicographic first `(clause_index,start_position)` match, returns one typed interval replacement, and commits one atomic splice.
- T16 refines the source-first shell: match applicability is intrinsically coupled to the program's left sides, so `FirstApplicableMatch` and result lookup share one validated program object. This is explicit coupling, not a duplicated matcher callback.
- T16 has zero successors with `NoMatch` when no clause applies. The final state is retained once; an applicable identity rule remains an event/self-loop, and external stop, horizon, invalidity, and error stay distinct.
- T16 supplies no canonical rule numbering and directly evidences only nonempty literal clause sides. T15's contextual epsilon evidence does not broaden T16; its public RHS remains nonempty rather than gaining a flag or inferred deletion feature.
- T17 reuses finite ordered support but requires a distinct queue event: read an exact leading `q`, consume a leading `d`, preserve the old suffix, and append a table-selected word at the remote tail. Wolfram ordinary tags pin `q=d`; Post and Wang variants prove the roles are independently meaningful.
- T17 tables are total `Sigma^q -> Sigma*` maps, so empty appendants are native while missing/duplicate rows are errors. This broadens only private word/edit capability; T13/T16 public nonempty laws remain unchanged.
- T17 has zero successors with a retained `InsufficientPrefix` residue when required spans are unavailable. Wolfram's supplied history maps that residue to `{}` on the next requested sample; this is an explicit reference projection, not a fabricated semantic transition.
- T17 supplies the bounded count `(sum_{j=0}^r k^j)^(k^q)` and the direct `50,625` oracle, but no canonical integer rule codec. Finite words, full ragged traces, queue provenance, and derived length/first-symbol/checkpoint views stay separate.
- T19 adds a finite named register bank over exact arbitrary-precision naturals plus a visible program marker. Code addresses and register keys are typed address spaces, not DOMAIN coordinates or finite alphabet values.
- T19 uses program-coupled active-instruction selection and instruction-owned named operand reads. Closed increment/decrement-jump results return typed register and marker writes through the shared atomic UPDATE; no generalized control class, instruction callback, or family rollout is required.
- T19 reference semantics are event-free absorbing `Quiescent(PastProgramEnd)` with the exact state retained; an explicit `ProgramExitStop` interpretation may instead terminate. The last valid event, reference stutter, optional halt, wrap, horizon, external stop, invalidity, and error remain distinct.
- T19's counted in-program target profile has `(k(n+1))^n` structured programs and no canonical integer codec. A general positive-target profile permits deliberate past-end exits; seeds remain independent and compressed zero-hit/arithmetic views remain event-derived observers.
- T20 adds finite rooted ordered expression trees with typed head/argument paths, closed structural pattern/template programs, whole-subexpression bindings, and functional-left-to-right outermost prefix-free source selection.
- T20 selects greedily, then its bijective balanced/prefix tree-token codec maps selected subtrees to disjoint spans for generic ordered multi-span UPDATE. Bound subtrees may be duplicated, deleted, or rearranged with occurrence-level lineage; this is a schedule/representation preset, not a tree-specific commit.
- T20 exact no-match semantics are event-free absorbing `Quiescent(NoPatternMatch)`; an applicable identity remains `Advanced(changed=false)`. Fixed-point stopping, normalization, cycle detection, confluence, and horizons are separate observers/protocols.
- T20 has structured Catalan expression counts but no rule codec. Functional/tree/Polish/bracket representations, valuations, depths, and size plots are codecs or observers; combinators and deterministic operator evolution are native profiles, while networks and multiway equations remain T29/T30.
- T27 state is a finite multiplicity-preserving bag of immutable prototype occurrences with complete local-to-world affine poses. Every old occurrence reads only itself and emits its total row of parent-local child templates through `P∘C`; a bag-composition UPDATE policy consumes parents and retains ordered child-slot lineage inside the common runner.
- T27 overlap and coincidence are inert: parents do not read neighbors, no footprint is exclusive, and multiplicity/lineage survive. The page-190 orbit proves that two occurrences can share a center and the same square footprint while different 90-degree frames produce different descendants.
- T27 exact page-189/page-190 rules use rational matrices/vectors. Algebraic and explicitly declared finite-precision profiles remain distinct; semantic equality never uses an epsilon. Center lists, polygons, rasters, unions, generation stacks, dimensions, limits, and parameter filters are downstream.
- T27's Möbius and inverse-square-root variant uses a distinct closed extended-complex point-map profile while sharing all-occurrence bag expansion. T13 lineage composes, but its ordered concatenation does not; T28 owns gridded neighbor interaction and T29 owns non-geometric network topology.
- T29 adds finite nonempty root-reachable directed graphs with two semantic ports per vertex, alpha-renamable occurrence identity, exact root/port-preserving isomorphism, and a breadth-first canonical pair codec.
- T29 programs are total closed tables over uniform or exact-length reach-signature reads. Results contain old-snapshot path endpoints or distinct event-local fresh-node occurrences; equal descriptors and equal local topology never merge identities.
- T29 uses a graph UPDATE policy: all old nodes propose from one graph, raw reroutes/births commit atomically, newborns wait, and directed forward closure from the preserved root is projected afterward.
- T29's exact uniform periods/collapse, singleton growth, depth-one `1296` count, five depth-two tables/count anchors, signature witnesses, frozen/projection/freshness/alias cases, and raw-event reconstruction close the parallel handoff.
- The sequential-network table and pruning evidence are preserved, but primary sources do not determine move timing or projection anchor/order. Goal 2 must explicitly defer that FRONTIER/UPDATE schedule profile rather than choose a convention or flag.
- T30's native configuration is one finite word, including epsilon; a finite exact word-set layer is the explicit powerset iteration lift. Its program is an unordered finite relation from nonempty literal left sides to epsilon-capable right sides.
- T30 selects every overlapping match of every clause in one old word. Each match independently creates one single-splice child; layer iteration exact-unions per-parent successor sets, newborns wait, and enumeration order is nonsemantic.
- T30 uses the uniform `StepResult[Configuration]`: its successor component exact-merges equal children across spans, rules, and layer parents, while its event component retains every rewrite witness and dead parent.
- A nonempty all-dead layer advances eventfully to the empty layer; only the empty layer has event-free reference stutter. Identity and recurrent words remain eventful and cannot be suppressed by a global visited/compressed graph.
- Layer lifts, derivation witnesses, simple edges, one-node-per-word compressed spacetime graphs, accumulated languages, counts, confluence/normal forms, proof search, and rendering are distinct from the native word configuration.
- T13 words and T16 literal occurrence/splice kernels compose privately without weakening their public rules/outcomes. Literal semi-Thue/grammar restrictions can reuse T30; tag multiplicity, cyclic/block/pattern/numeric/control variants remain separately typed.
- T31 is the first categorical break from transition execution: an immutable local-count relation denotes a mathematical model set and has no source, rule result, update, successor, seed, time, or halt.
- T31 uses a declared lattice footprint and total center-symbol-to-allowed-neighbor-histogram relation. Exact/at-least conditions compile to finite closed sets; no predicate, solver, boundary, or custom graph belongs in the spec.
- Exact periodic presentations, finite-window queries, and open-patch diagnostics have distinct scopes. Periodic SAT promotes globally; a replayed full-halo finite obstruction may prove global UNSAT; bounded failure remains `Unknown`.
- Constraint verification reports and scoped `Satisfiable/Unsatisfiable/Unknown/ResourceLimit` solver records are distinct from `Advanced/Terminal/Quiescent` outcomes and from solver search traces.
- T31's exact `0011` de Bruijn cycle, permissive run models, `5x5` tile/five-violation perturbation, complete 25-profile gallery, finite obstructions, wrapped-alias, equality, scope, and certificate oracles close the handoff.
- T32 is now closed as one finite exact `AllowedLocalPatterns` node inside the T31 declarative layer: every T31 histogram relation lowers losslessly to it, while exact orientation makes the reverse partial. T33 retains a separately tagged global existential required occurrence. Broader tiling undecidability, CA fixed points, ground states, network constraints, and repair/search algorithms are relations, not T31/T32 mechanics.

## Synthesis Conclusions and Goal 2 Boundaries

- The 45-row CSV and one-to-one T-ID mapping are complete for this goal; `CA-Types.md` remained search vocabulary rather than evidence.
- The shared `FRONTIER -> NEIGHBORHOOD -> RULE -> UPDATE` algebra is substantive for every evidenced canonical step/rewrite construction. The literal claim that all 45 rows execute is false because six strict-layer rows are declarative.
- Every transition state can be Markovian with semantically required history/control exposed as tags, products, markers, prefixes, or structural fields. No completed type requires hidden executor state.
- Raw semantic traces require typed loci, events, witnesses, lineage, and structural configurations; canonical `[t,x,y,z]` coordinates remain only one fixed-dimensional view.
- Current `src/ca` tensor/family boundaries are not genuine semantic boundaries and must be replaced in place during Goal 2.
- Shared implementation stages plus one leaf conformance obligation per T01-T45 are cleaner than one implementation stage or runtime class per type.
- Probability-bearing transitions, first-class continuous-time flow, T28 adaptive subdivision, T29 sequential timing/projection, and unsupported exact-real profiles remain explicit future evidence/backend boundaries rather than invented behavior.

## Required Goal 1 Artifacts

Execution of this plan will create:

- One stage file for foundation work.
- One evidence-and-design stage file for each of the 45 catalog types.
- `goal-1/evidence-index.md`: coverage ledger linking every CSV row to searches, excerpts, stage status, and unresolved candidates.
- `goal-1/design-ledger.md`: evolving inventory of proposed state models, selectors, read models, result types, update algebras, invariants, and rejected abstractions.
- `goal-1/goal-2-handoff.md`: dependency-aware implementation plan with a traceable conformance stage for every type.
- One synthesis stage and one Goal 2 handoff stage.

Do not create empty type stage files in advance. Create each from `0-loop.md` when its work begins so it reflects current facts.

## Evidence Completeness Standard

A type's evidence pass is complete only when all of the following are recorded:

1. The CSV name, taxonomy index, aliases, singular/plural forms, historical names, named variants, rule examples, and parameter vocabulary used for searching.
2. Searches across the canonical monolithic book for direct names, aliases, variant names, parameter terms, relevant section headings, captions, Notes references, and Index references.
3. Context inspection around every candidate match. Search hits alone are not excerpts.
4. Follow-up of relevant cross-references such as "see page" or references to earlier/later constructions.
5. Every unique relevant passage copied into the stage file with exact source path, line provenance, surrounding section, and a short statement of what construction fact it establishes.
6. Relevant captions included even when nearby prose appears duplicative, because captions often state rule mechanics or initial conditions more precisely.
7. False positives and excluded candidates logged with reasons, so completeness can be audited.
8. Duplicate text appearing in monolithic and split files recorded once, with the monolithic path as canonical provenance.
9. No unresolved candidate matches or unsearched aliases remain. Genuine ambiguity is recorded as an open evidence question rather than silently resolved.

"Every excerpt" means every unique passage found in the repository's local Markdown that materially describes the type's construction, core variants, parameters, initial conditions, update semantics, state organization, or relation to another catalog type. It does not mean every passing mention with no constructive content.

## Common Type-Stage Protocol

Each type stage must perform this loop:

1. **Identify:** establish the exact catalog entry, aliases, whether it is an engine, specialization, filter, seed class, observable, solver-defined system, or another kind of entry.
2. **Collect:** execute and log the exhaustive evidence search, then record all unique relevant excerpts.
3. **Reconstruct:** derive the construction from the excerpts: state, support/topology, values, control, active loci, reads, rule inputs and outputs, update/commit semantics, successor structure, halting, boundaries, seed, parameters, and observables.
4. **Compare:** map each construction element to `simple_programs.md` and concrete `src/ca` modules and tests. Label each element `direct`, `parameterization`, `principled extension`, `semantic mismatch`, or `not applicable`.
5. **Minimize:** propose the smallest semantic classes or protocol changes not already present. Search prior stage results before inventing anything.
6. **Challenge:** test the proposal against `principles.md`, identify abstraction pressure, and document rejected shortcuts and why they are forbidden.
7. **Plan Goal 2:** write a self-contained implementation stage with files, API changes, migrations, tests, canonical examples, validation, dependencies, and completion requirements. Shared primitives are referenced, not re-planned as duplicate implementations.
8. **Re-integrate:** update `0-plan.md`, `evidence-index.md`, and `design-ledger.md`. Re-evaluate every global abstraction touched by the new evidence and reopen earlier stages when necessary.

## Success Metrics

- All 45 CSV rows have complete, auditable evidence stages.
- Every relevant unique local-book excerpt is captured with provenance.
- Every type has a construction model grounded in those excerpts rather than inferred from its name.
- Every type has an explicit current API/runtime fit analysis.
- Proposed semantic additions are deduplicated across types and justified by at least one real construction.
- No proposal relies on prohibited fallbacks, opaque packing, family-specific rollout, or vacuous callback interfaces.
- The final design ledger names the genuinely shared execution algebra or algebras and explains any irreducible split.
- `goal-2-handoff.md` contains a dependency-aware implementation and verification path covering all 45 entries.
- Each type remains separately traceable in Goal 2 even when implementation is organized around shared primitives.
- The final `0-plan.md` is internally cohesive and contains no stale decision contradicted by later evidence.

## Verification Requirements

- Confirm CSV row count, uniqueness, and one-to-one stage coverage mechanically.
- Confirm every type stage contains its search log, excerpts, construction model, comparison, principles audit, Goal 2 handoff, and integration result.
- Confirm all excerpt paths and line references resolve against current repository files.
- Confirm every proposed new primitive is used by a documented construction and is not equivalent to an existing primitive.
- Confirm all 45 types appear in `evidence-index.md` and `goal-2-handoff.md` exactly once as coverage obligations.
- Review the final design for hidden family branches, `Any` escape hatches, padding-as-semantics, global formula bypasses, and duplicated execution logic.
- Run `git diff --check` and verify Goal 1 has not modified runtime, tests, or root API documents.

## Stages

Stages are ordered to expose difficult semantic differences early. `TNN` records the stable CSV taxonomy index even though execution order is adversarial rather than numeric.

### 1-FOUNDATION

Status: **COMPLETE** in `goal-1/1-FOUNDATION.md`.

#### Big Picture Objective

Establish an auditable baseline of the taxonomy, evidence source, current API, current runtime, and evolving design vocabulary before judging any type.

#### Detailed Implementation Plan

- Read `principles.md`, `simple_programs.md`, every top-level `src/ca` module, and the corresponding tests in full.
- Validate the 45 CSV rows against `CA-Types.md` headings and establish stable `T01` through `T45` identifiers.
- Create `evidence-index.md` and `design-ledger.md` with no premature family conclusions.
- Define reproducible search logging, excerpt provenance, deduplication, fit labels, and Goal 2 handoff format.

#### Completion Requirements

- All 45 types are indexed exactly once with pending status and stable stage mapping.
- Current runtime and API responsibilities are documented with file references.
- Search and evidence standards are executable and leave no undefined meaning of "complete."
- Initial assumptions and suspected abstractions are explicitly marked as hypotheses.

#### Stage Result

Foundation mechanically joined all 45 CSV rows to taxonomy sections, stable T IDs, unique execution stages, and pending evidence-index records. It read and inventoried the complete governing API/runtime/test baseline, created `evidence-index.md` and `design-ledger.md`, and recorded current family-dispatched rollout, hidden temporal history, fixed-support assignment, and unrestricted callable pressure as liabilities rather than design commitments. The current suite passed with 102 tests; Goal 1 changes were confined to `goal-1/`. No type conclusion was made and no stage was reopened. Next: T01.

### 2-T01-ELEMENTARY

Status: **COMPLETE** in `goal-1/2-T01-ELEMENTARY.md`.

#### Big Picture Objective

Establish elementary cellular automata as the fixed-lattice, synchronous, ordered-local-rule baseline.

#### Detailed Implementation Plan

Apply the common type-stage protocol, emphasizing binary alphabets, radius-one ordered neighborhoods, rule numbering, full parallel update, boundaries, and single-cell seeds.

#### Completion Requirements

All T01 evidence and search candidates are resolved; current runtime behavior is mapped precisely; its Goal 2 conformance stage is complete; global ledgers are updated.

#### Stage Result

The exhaustive direct-name, alias, named-rule, caption, Notes, Index, boundary, seed, equivalence, and restriction searches closed with zero unresolved candidates and 23 canonical excerpt groups. T01 reconstructs an arbitrary Boolean table over ordered `(left,self,right)` reads with Wolfram oracle `(n >> (4*left + 2*self + right)) & 1`, one same-site write per fixed lattice site, and old-snapshot parallel commit. The usual centered cell, random fields, finite cycles, and display crops are separate seed/realization choices; reflection and black/white conjugation yield 88 analysis orbits while all 256 rules remain executable. Architecture reclosure identifies this as the CA preset of the common SimpleProgram runner, not the boundary of the abstraction. Goal 2 must fix generic exhaustive cardinality and ordering, retain explicit support/realization/trace boundaries, and use a strict elementary preset with independent asymmetric rule-30 tests. Next: T09.

### 3-T09-MOBILE

Status: **COMPLETE** in `goal-1/3-T09-MOBILE.md`; evidence and architecture are reclosed.

#### Big Picture Objective

Stress the baseline with one active locus whose rule both changes state and moves control.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing active-cell state, local reads, write scope, movement, compressed observations, and whether frontier loci are sources or targets.

#### Completion Requirements

All T09 evidence is captured; control and movement semantics are explicit; no CA compilation is used as the proposed fit; Goal 2 and global integration are updated.

#### Stage Result

The exhaustive direct/control/function search produced 135 candidates, with targeted rule-count, compression, schedule, boundary, split-file, Notes, and Index remainders all dispositioned and zero unresolved. T09 reconstructs a fixed binary line labeled by `Plain(bit) | Active(bit)` with exactly one active tag, physical `[left,self,right]` reads, and an arbitrary eight-row compact rule returning typed source assignment plus `{-1,+1}` tag movement. The common atomic UPDATE preserves the old destination bit while moving the tag. Its 65,536 compact rules remain inspectable pairs of byte tables. The canonical `{35,57}` order, asymmetric guards, sparse trajectory, pack/unpack bijection, and one-step commuting map close conformance. Transparent composite labels are accepted; opaque packing, arbitrary composite-CA tables, display compression as state, finite-edge invention, and family dispatch are rejected. Next: T12.

### 4-T12-TURING

Status: **COMPLETE** in `goal-1/4-T12-TURING.md`; evidence and architecture are reclosed.

#### Big Picture Objective

Test tape values, head control state, symbol writes, state transitions, movement, blank support, and halting in one construction.

#### Detailed Implementation Plan

Apply the common protocol, distinguishing the tape alphabet from head state and testing whether complete Markov state remains visible to the shared executor.

#### Completion Requirements

All T12 variants and parameters are evidenced; write/move/control effects are modeled without hidden executor state; Goal 2 and global integration are updated.

#### Stage Result

All 278 direct-name lines, 74 halt lines, exact rule/count/codec candidates, captions, Notes, Index routes, split duplicates, named variants, and cross-system emulations were dispositioned with zero unresolved. T12 reconstructs a total compact `Q x Sigma -> Q x Sigma x {L,R}` table over an integer tape labeled by `Plain(symbol) | Head(q,symbol)` with exactly one head. `NEIGHBORHOOD` exposes only `(q,symbol)` at the tagged source. RULE returns `AssignSource(symbol_next)` plus typed `MoveHead(q_next,direction)` intent; UPDATE resolves the destination through the visible topology, preserves its old symbol from the same snapshot, and applies both effects atomically. A concrete two-label assignment batch is only a verified lossless lowering. This representation is bijective with the factored tape/head view on valid states. The base family never halts; a special terminal tag is an intrinsic variant, while external observations, horizons, and errors remain distinct. The `(2sk)^(sk)` count, repaired codec, code 3024, Notes table, sparse trajectory, pack/unpack, and commuting-square oracles close conformance. A bare lossy union, arbitrary composite-CA table, hidden head state, finite-edge invention, and family dispatch are rejected. Next: T13.

### 5-T13-PARALLEL-SUBSTITUTION

Status: **COMPLETE** in `goal-1/5-T13-PARALLEL-SUBSTITUTION.md`.

#### Big Picture Objective

Test variable support and source elements that emit ordered replacement blocks in parallel.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing neighbor independence, source identity, replacement concatenation, growth, ancestry, and the distinction between semantic support and rendering scale.

#### Completion Requirements

All T13 evidence is captured; no fixed-capacity padding or target-local inversion is accepted as core semantics; Goal 2 and global integration are updated.

#### Stage Result

All 288 direct-name lines and the complete definition/replacement/alias/Notes/Index/split/rendering/growth/infinite/stochastic/emulation search families were dispositioned with zero unresolved candidates and 26 canonical excerpt groups. T13 reconstructs a total finite-alphabet morphism `Sigma -> Sigma+` over an explicit discrete ordered sequence. Every old occurrence fires once from the same snapshot, returns a typed nonempty word, and an ordered block-replacement UPDATE consumes the parent generation and creates children in source/block order. The counterexample `a -> aa` requires this UPDATE-axis implementation because same-site scalar writes cannot preserve support growth or child lineage; it does not require a substitution executor or a different top-level algebra. The exact `1->10, 0->01` trajectory, growth fixtures, ordering adversaries, and lineage intervals form independent tests. Finite/infinite support, cuts, ragged traces, ancestry, and renderings remain separate. Next: T16.

### 6-T16-SEQUENTIAL-SUBSTITUTION

Status: **COMPLETE** in `goal-1/6-T16-SEQUENTIAL-SUBSTITUTION.md`.

#### Big Picture Objective

Test ordered matching, first-applicable replacement, one-event steps, and scan semantics.

#### Detailed Implementation Plan

Apply the common protocol, identifying which choices belong to frontier selection, rule ordering, and update semantics without introducing a family switch.

#### Completion Requirements

All T16 scan and match variants are evidenced; ordering is modeled as defining semantics; Goal 2 and global integration are updated.

#### Stage Result

All 51 direct-name lines and the complete rule/position-order, caption, Notes, Index/split, alias/history, stopping, overlap/confluence, finite-input, causal-trace, generalized/multiway, and emulation searches were dispositioned with zero unresolved candidates and 21 canonical excerpt groups. T16 reconstructs a finite ordered word plus an immutable ordered list of nonempty literal clauses. Selection is rule-major then leftmost position, exactly one old-snapshot interval is replaced, scanning restarts on the next step, and absence of a match is a typed terminal outcome. Principle 0 refines source selection to consume one program-owned applicability view; `ReplaceInterval` and `SingleSpliceUpdate` form a sibling structural update while T13 ordered state/provenance can be reused unchanged. Exact canonical, sorting, priority, overlap, newborn, identity/no-match, and lineage oracles guard the handoff. Host regex/replace-all, hidden cursors, family dispatch, fixed capacity, CA compilation, and multiway branching are rejected. Empty RHS remains an evidence boundary for T15. No prior stage was reopened. Next: T17.

### 7-T17-TAG

Status: **COMPLETE** in `goal-1/7-T17-TAG.md`.

#### Big Picture Objective

Test queue-like state changes that consume a prefix, inspect it, append a block remotely, and halt on insufficient input.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing deletion number, append lookup, positional reindexing, halting, and whether effects can remain structurally typed.

#### Completion Requirements

All T17 variants are evidenced; consume/append/halting semantics are direct rather than simulated; Goal 2 and global integration are updated.

#### Stage Result

All 175 direct occurrences on 111 unique lines and the complete mechanism, caption/figure, Notes, Index/split, history, Post/Wang, cyclic/multiway boundary, halt/extinction, bounded-count, finite-input, randomness-observer, PCP, and emulation searches were dispositioned with zero unresolved candidates and 21 canonical excerpt groups. T17 reconstructs an immutable complete prefix-word program over a finite ordered word: Wolfram ordinary tags read and delete the same leading `n`, then atomically preserve the old suffix and append a possibly empty word; Post and Wang prove read width and deletion number are distinct generic roles. Principle 0 rejects T16 front replacement and adds `ConsumePrefixAppend` plus `QueueSpliceUpdate`, while reusing ordered support, provenance, outcomes, and an epsilon-capable private edit carrier without changing T13/T16 public contracts. Operationally a short word is terminal with its residue retained; the supplied short-to-empty history is a labeled projection, guarded by figure case (c)'s residue `0` at step 287 and `{}` at 288. Case (a), one-deletion/T13 checkpoints, tail-order, empty/missing-table, Post/Wang, count, and provenance oracles close the Goal 2 handoff. No prior stage was reopened. Next: T19.

### 8-T19-REGISTER

Status: **COMPLETE** in `goal-1/8-T19-REGISTER.md`.

#### Big Picture Objective

Test finite control over unbounded numeric values with instruction-pointer-dependent branching.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing register identity, instruction definitions, increment, decrement-jump, zero behavior, and complete control state.

#### Completion Requirements

All T19 evidence is captured; instruction execution is not hidden in an opaque formula callback; Goal 2 and global integration are updated.

#### Stage Result

All 129 direct occurrences on 94 lines, 135 direct/alias occurrences on 95 lines, and the complete mechanism, image/caption, Notes, actual Index/split, history, count, program-control/end/halting, seed, observer, variant, universality, compiler, and reduction searches were dispositioned with zero unresolved native-mechanics candidates and 25 canonical excerpt groups. T19 reconstructs a finite named bank over exact naturals plus a visible program marker/product factor. The marked instruction is the firing locus, named operands are its access pattern, and closed increment/decrement-jump results return typed register and marker writes for the shared atomic UPDATE. No generalized control class or register executor is required. Program exhaustion is event-free quiescence; special exit is an explicit interpretation and implicit wrap is forbidden. The exact count, trajectories, repaired witness, square-root exit, and arbitrary-precision tests close the handoff. Next: T20.

### 9-T20-SYMBOLIC

Status: **COMPLETE** in `goal-1/9-T20-SYMBOLIC.md`.

#### Big Picture Objective

Test hierarchical expression state, pattern bindings, subtree replacement, scan order, overlap, duplication, and deletion.

#### Detailed Implementation Plan

Apply the common protocol, comparing tree topology and graph encodings without treating display positions as semantics.

#### Completion Requirements

All T20 evidence is captured; pattern and rewrite semantics are explicit; no string-only workaround is accepted without proof of fidelity; Goal 2 and global integration are updated.

#### Stage Result

All 73 exact-name occurrences on 60 lines and the conservative 272-occurrence/166-line direct-and-alias search were dispositioned, together with every caption/figure, Notes, actual Index/split, history, representation, combinator/operator variant, fixed-point, observer, and compiler route. Twenty-four canonical excerpt groups remain after deduplication and zero native-mechanics candidates are unresolved. T20 reconstructs a discrete recursive-tree topology, typed paths, closed patterns/templates, subtree bindings, ordered outermost prefix-free firing selection, and inert instantiation. A bijective balanced/prefix tree-token codec maps selected subtrees to disjoint spans for generic ordered multi-span UPDATE. Structural duplication/deletion and occurrence lineage are retained without a tree UPDATE, symbolic executor, or opaque whole-tree callback. Exact trajectory, overlap/newborn, count, S/K, priority, identity, no-match, codec, and provenance oracles close the handoff. T13 lineage and T16 program coupling compose at their typed axes. Next: T27.

### 10-T27-GEOMETRIC

Status: **COMPLETE** in `goal-1/10-T27-GEOMETRIC.md`.

#### Big Picture Objective

Test replacement of geometric objects by transformed descendants outside a rigid lattice.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing primitive geometry, scale, translation, rotation, reflection, overlap, orientation, and the boundary between program state and rendering.

#### Completion Requirements

All T27 evidence is captured; geometric semantics are not reduced to visualization metadata; Goal 2 and global integration are updated.

#### Stage Result

The conservative core search dispositioned 46 occurrences on 37 lines and the expanded alias/observer audit dispositioned 129 on 88, leaving 18 canonical excerpt groups and zero unresolved native-mechanics candidates. All main figures, Notes, actual Index/splits, exact and approximate affine rules, overlap/orientation, complex/IFS variants, dimensions, history, limits, observers, and relations were resolved; the official figure source recovered image-only page-191(d) without fabricating exact coefficients.

T27 reconstructs finite bags of fully posed prototype occurrences, exact or explicitly declared affine scalar carriers, parent-local `P∘C` composition, permutation-invariant all-occurrence frontiers, self-only reads, and multiplicity-preserving bag replacement through the UPDATE axis. Exact centers/counts, overlap, same-center/same-footprint/different-frame, composition order, equivariance, duplicate slots, permutation, newborn timing, validation, and provenance close the handoff. Center/raster/union/limit observers remain downstream, while nonlinear complex branches use a distinct closed point-map RULE form. T13 lineage composes but ordered concatenation does not. Next: T29.

### 11-T29-NETWORK

Status: **COMPLETE** in `goal-1/11-T29-NETWORK.md`.

#### Big Picture Objective

Test dynamic topology whose connectivity, not drawing coordinates, defines state and neighborhoods.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing node identity, labeled connections, path-relative reads, rerouting, insertion, deletion, components, and isomorphism.

#### Completion Requirements

All T29 evidence is captured; topology is first-class; graph updates do not rely on incidental coordinates; Goal 2 and global integration are updated.

#### Stage Result

The direct-name search dispositioned 44 occurrences on 40 lines; conservative family, expanded graph/network, and executable-symbol audits dispositioned 290/217, 1,278/654, and 27/19 respectively. Twenty-seven canonical groups cover all main figures, Notes/programs, actual Index/splits, exact rule tables/counts/periods, isomorphism, projection, observers, variants, and relations. Parallel semantics have zero unresolved candidates; the sequential source limitation is explicit.

T29 reconstructs a discrete rooted two-port graph topology, old-snapshot paths and exact-length reach signatures, total direct/fresh result rows, collision-free event births, atomic raw rerouting, and post-commit directed root projection. Exact BFS canonicalization handles root/port isomorphism without merging nodes. Fresh graph identity and incidence cannot be expressed by value-only fixed-support writes, so a typed graph UPDATE policy extends the common runner; no network executor is added. Uniform, creation, snapshot, projection, freshness, alias, identity, and provenance oracles close the parallel handoff. Only the unresolved sequential source/schedule profile is deferred pending decisive primary evidence. Next: T30.

### 12-T30-MULTIWAY

Status: **COMPLETE** in `goal-1/12-T30-MULTIWAY.md`.

#### Big Picture Objective

Test all possible rewrites, multiple states per step, deduplication, repeated states, and causal/state graph construction.

#### Detailed Implementation Plan

Apply the common protocol, deciding from evidence whether the next state is a collection, a graph increment, multiple outcomes, or another explicit structure.

#### Completion Requirements

All T30 evidence is captured; branch identity and deduplication are explicit; no accidental single-path collapse occurs; Goal 2 and global integration are updated.

#### Stage Result

Exact and broader direct audits dispositioned 267/182 and 277/186 occurrences/lines; the expanded alias/confluence search dispositioned 388/224 and implementation symbols 18/16. Twenty-five canonical groups cover every main figure, executable Notes/program, page-952 observer, actual Index/split, history, group/grammar/numeric/tag variant, compressed/causal graph, confluence/completion, proof-search, and relation passage. Base literal mechanics have zero unresolved candidates.

T30's smallest configuration is one finite word. Its unordered epsilon-capable literal relation selects every overlapping match and produces one child per match; the uniform `StepResult[Word]` contains an exact successor set and separate derivation witnesses. A finite word-set layer is the explicit powerset iteration lift, not a different state class or executor. Dead parents drop; epsilon differs from the empty successor set; recurrent words fire despite compressed-graph reuse. Page-219/page-220, page-206, cross-parent layer merge, page-224, overlap/diamond/identity/extinction/reconstruction oracles close the handoff. Next: T31.

### 13-T31-CONSTRAINTS

Status: **COMPLETE** in `goal-1/13-T31-CONSTRAINTS.md`.

#### Big Picture Objective

Determine whether declarative local constraints share an executor with transition systems or require a distinct, honest semantic algebra.

#### Detailed Implementation Plan

Apply the common protocol, separating the constraint-defined solution set from search, propagation, enumeration, and visualization algorithms.

#### Completion Requirements

All T31 evidence is captured; the constraint/solver boundary is explicit; any executor split is justified rather than hidden; Goal 2 and global integration are updated.

#### Stage Result

The direct-name union dispositioned 29 occurrences on 27 lines, conservative family search 162/134, expanded audit 815/415, and bare constraint search 467/312. Twenty-eight canonical groups cover every strict figure, Notes/Index/split, de Bruijn/periodic proof, search/repair/complexity passage, CA/tiling/ground-state/network/equation relation, and T32/T33 boundary. All 27 direct lines are classified; strict mechanics have zero unresolved candidates.

T31 reconstructs a total-field model set defined by a closed center-conditioned neighbor-histogram relation. It adds exact periodic/open/window scopes, pure verification, pointwise periodic equivalence, replayable finite obstructions, and separate scoped solver results outside rollout. The `0011` cycle, permissive rows, `5x5` tile, full 25-profile classification, perturbation/obstruction/scope/alias/equality/certificate tests close the handoff. Generic alphabet/dimension/footprint support is labeled principled closure, and broader template complexity is not misattributed. Next: T34.

### 14-T34-ARITHMETIC

Status: **COMPLETE** in `goal-1/14-T34-ARITHMETIC.md`.

#### Big Picture Objective

Test scalar arithmetic iteration without assuming spatial locality or finite alphabets.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing number type, exactness, operation, initial value, representation base, and the difference between state and observable digits.

#### Completion Requirements

All T34 evidence is captured; arithmetic state is not confused with its rendering; Goal 2 and global integration are updated.

#### Stage Result

The direct-name union dispositioned 65 occurrences on 55 lines, the conservative mechanics query 27/26, the focused native query 13/12, and exact code/observer forms 6/6. Thirty canonical groups cover the scoped main core, all seven main figures and Notes figures, Notes/programs/actual Index/splits/history, exact value carriers, addition/multiplication presets, nonlocal carries, digit/fraction/size observers, finite suffix quotients, CA/substitution relations, reversibility, precision, and fast-forward evaluation. Strict mechanics have zero unresolved candidates.

T34 is a discrete `t+0D` SimpleProgram over an exact numeric carrier with closed `AddConstant | MultiplyConstant` RULE nodes, self read, and ordinary same-locus UPDATE. Arbitrary-precision integers/reduced rationals, decimal-string codecs, exact traces, structural program identity, eventful identity steps, explicit run outcomes, and base/radix/crop/repetend observers are implementation-ready. Page-117..122 row counts/endpoints, `3^499`, exact `(3/2)^t`, the 201-dot fractional plot, suffix period, overflow, carry, normalization, and cross-base tests close the handoff. `MultiplyMod`, compilers, and direct powers remain explicit presets/relations/observers; T43 shares the unary runner.

### 15-T37-RECURSIVE

Status: **COMPLETE** in `goal-1/15-T37-RECURSIVE.md`.

#### Big Picture Objective

Test growing historical state and fixed dependency references used to append new sequence terms.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing seeds, index origin, dependency support, append semantics, and whether history is state or trace.

#### Completion Requirements

All T37 evidence is captured; recurrence dependencies and invalid indices are explicit; Goal 2 and global integration are updated.

#### Stage Result

The direct-name union dispositioned 48 occurrences on 42 lines, fixed-lag tokens 23/13, focused mechanics 32/20, literal recurrence programs 20/20, aliases 10/10, and named saturation 160/118. Nineteen excerpt groups cover the strict main range and raster, Notes, actual Index/splits, programs/history, Fibonacci/Lucas/Perrin/factorial, logistic/Ackermann/Ulam/modular relations, analyzers/observers, and every construction boundary. Strict mechanics have zero unresolved candidates.

T37 uses `NumericPrefix(carrier,origin,terms)`, exact minimal fresh seeds and replay-verified checkpoints, normalized `AffineFixedLag` programs, and a closed factorial-capable expression extension. The prefix codec `Val(o,v_0) · ... · End(n)` is bijective; unique-`End` FRONTIER selection, old-prefix dependency reads, and RULE replacement `End(n) -> Val(n,next) · End(n+1)` reuse T16 exactly-one ordered splice. Every valid event preserves all old terms and appends exactly one indexed term; repeated values still advance and fixed-reference invalidity is static. Compact seed-plus-event traces reconstruct `h+1` prefixes from `h` appends, while a lag window is only a future-sufficient non-injective quotient.

Exact oracles pin the six page-143 horizons `38/48/22/26/44/27`, every displayed term and endpoint, the source's (e)/(f) characteristic-equation mislabel, Fibonacci beyond signed 64-bit, Lucas/Perrin/factorial, trace cardinality, checkpoint replay, and window loss. Closed forms, plots, sounds, and memoization remain downstream; current modular hidden-history AR2 is not the reference implementation. T38 computed indices and T43 scalar maps stay separate; at T37 closure Ulam remained an explicit T37/T39 composition question, resolved by the following stage. No prior stage was reopened. Next: T39.

### 16-T39-FILTERS

Status: **COMPLETE** in `goal-1/16-T39-FILTERS.md`.

#### Big Picture Objective

Test constructive filtering, sieving, and derived numeric sequences that may not be ordinary state transitions.

#### Detailed Implementation Plan

Apply the common protocol, distinguishing candidate support/set, stage policy, predicates, survivors, removed values, and derived measurements.

#### Completion Requirements

All T39 evidence is captured; finite field writes and the survivor-list representation commute losslessly, infinite membership remains intensional, and Goal 2/global integration are updated.

#### Stage Result

The exact heading, prime/sieve/direct-function, divisibility/divisor, factorization, survivor/candidate/filter/removal, perfect/Goldbach/number-theory, representation, history, actual-Index, and relation searches are fully dispositioned. The direct prime search found 221 occurrences on 134 lines; the high-signal union found 144/84, including 121/66 before the Index; nineteen evidence groups cover the strict main, seven raster files/twelve plotted profiles, native Notes, split, actual Index, algorithms, variants, history, emulation, source repairs, Ulam, and T40 boundary. Zero source candidate remains unresolved.

T39 separates pure filter/measurement definitions from the stepwise consecutive-divisor sieve. Strict configuration has ordered finite/intensional candidate support and a visible next-divisor marker; the immutable stage program remains separate. Finite membership is a Boolean field with a lossless ordered-survivor pack. The current stage is the FRONTIER; proper-multiple hits are read witnesses/write targets, and ordinary candidate false-writes plus the marker write commit through generic old-snapshot UPDATE. Infinite membership is derived intensionally from support/program/marker. Every valid row advances, including composite zero-removal rows. Mathematical-set/stream/direct-query/measurement results stay outside transition execution.

All 1,200 page-147 cells match the literal `1..100`, divisors `2..13` trace. The source genuinely retains `1`, so exact display and corrected prime profiles are separate. Independent oracles pin all six page-148 formulas/horizons—including 1,000 forward gaps ending at 8—and all five page-150 measurements—including ordered Goldbach and signed ordered square tuples. Finite certification, infinite intensional queries, equality, serialization, trace, outcomes, numerical contexts, and no-cheating cases are explicit.

Ulam is now an honest T37/T39 composition: closed first-accepted ascending candidate selection counts one unordered pair of distinct old indices in the complete old prefix, then the existing T37 append fires. The source's `1,2,3,4,...` prefix itself rejects ordered/self-pair alternatives. Current finite coordinate/callback selectors are semantic mismatches, while their universe/predicate/order responsibility split can be generalized structurally. Exact semantic assertions, seven raster hashes, Markdown fences, `git diff --check`, and all 102 repository tests pass. No prior stage is reopened. Next: T41.

### 17-T41-FUNCTIONS

Status: **COMPLETE** in `goal-1/17-T41-FUNCTIONS.md`.

#### Big Picture Objective

Test symbolic continuous functions and sampled or event-derived observables without inventing false dynamics.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing closed function definitions, continuous argument sets, sampling, exact event detection, parameters, and derived outputs.

#### Completion Requirements

All T41 evidence is captured; function definition and observation method remain distinct; Goal 2 and global integration are updated.

#### Stage Result

The direct-name union found 59 occurrences on 51 lines; the formula-literal union 176/83; crossing/rule mechanics 19/9. Eighteen evidence groups cover the strict main, native Notes, clean split, actual Index, function/series/zero/evaluation history and relations, every alias/false positive, four strict rasters, eight Notes-only rasters, and source repairs. Zero candidate remains unresolved.

T41 establishes a closed immutable unary function definition outside transition execution. `MathematicalFunctionSpec` carries one argument, exact/declared parameters, a real/complex definition set, a scalar/fixed-vector output schema, an ordered AST, versioned primitive semantics, partiality, and branches. Point/sample/real-zero/complex-zero/crossing/extremum queries declare their own scope and numerical context. Exact/certified/approximate/undefined/failure values, multiplicity-aware zero events, completeness, certificates, diagnostics, and renderings remain separate records.

All page-160/161/162/163 and supplementary profiles are pinned to exact formulas or explicit uncertainty. Independent checks verify two-sine periods/counts, the page-162 factorization/continued fractions, special-function anchors, and 60-decimal Riemann-Siegel values plus numerical zero totals. Pole segmentation, endpoint inclusion, the page-162 double tangent, zeta continuation/phase, the divergent `a=0` profile, and the inconsistent ODE initial derivative are explicit adversaries/source repairs.

T20 tree/codecs, T27 compatible numeric expressions, T31 query/certificate discipline, and T34 exact numbers are reused only at their established responsibilities. T41 supplies only source definition/query data; T40 owns the exact continued-fraction query/result; T42 consumes only a complete replay-verified D139/T40 result or separately tagged closed schedule and contributes the finite schedule/preset semantics over shared T13/D019/D024 state/trace machinery. T43/T44/T45 remain distinct. Exact/declared-precision assertions, all twelve hashes, search controls, Markdown fences, `git diff --check`, and all 102 repository tests pass. No prior stage reopened. Next: T43.

### 18-T43-ITERATED-MAPS

Status: **COMPLETE** in `goal-1/18-T43-ITERATED-MAPS.md`.

#### Big Picture Objective

Test continuous scalar state, repeated maps, piecewise behavior, precision, and optional digit representations.

#### Detailed Implementation Plan

Apply the common protocol, determining what can reuse scalar iteration while preserving interval and precision semantics.

#### Completion Requirements

All T43 evidence is captured; map and representation policies are explicit; Goal 2 and global integration are updated.

#### Stage Result

The direct map/mapping search found 106 occurrences on 89 lines, the controlled iteration union 214/155, and the high-signal map/chaos/precision/analysis union 332/210. Nineteen evidence groups cover strict main, native Notes, clean and line-oriented splits, actual Index, history, aliases, programs, precision profiles, analyzers, relations, all eight strict/three Notes assets, and every false positive. Zero candidate remains unresolved.

T43 establishes one ideal exact scalar map state, distinct certified/tracked computation work records, and separately identified fixed represented recurrences. The immutable map owns its value interval, exact parameters, ordered expression, primitive version, and normalized self-map/partial contract; a realized program additionally owns full radix/format/rounding/comparison semantics and represented closure. The `t+0D` singleton FRONTIER, complete self read, generic same-locus write, and atomic UPDATE directly reuse T34. Strict maps always advance, including unchanged fixed points; `h` events produce `h+1` states.

Exact rational reconstruction matches all 12,960 page-165 cells. The declared 180-decimal classifier matches page 168 at 29,040/29,040 and page 170 at 38,720/38,720 with recorded crop coordinates, thresholds, precision, and `Pi` literal. All eleven hashes match. Binary finite-storage collapse, decimal preperiod/period, logistic cycles, vector old-tuple update, discontinuity/cusp/endpoint semantics, and source repairs are pinned without overclaiming the missing page-166 plate or underdetermined Notes rasters.

T34 assignment and T41 syntax compose without reinterpretation. T37 prefixes, T42 substitutions, T44 aggregate fields, T45 flows, fixed-realization identity, cycles, sensitivity, Lyapunov, attractor/bifurcation, symbolic views, and fast-forward evaluators remain explicit categories. Semantic/raster oracles, source references, Markdown fences, eleven hashes, `git diff --check`, and all 102 repository tests pass. No prior stage reopened. Next: T44.

### 19-T44-CONTINUOUS-CA

Status: **COMPLETE** in `goal-1/19-T44-CONTINUOUS-CA.md`.

#### Big Picture Objective

Test the existing lattice algebra with continuous value spaces, local aggregation, numeric maps, and precision policy.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing gray-level range, averaging, map composition, exactness, and the boundary between mathematical values and finite numerical execution.

#### Completion Requirements

All T44 evidence is captured; reusable CA components and genuinely new numeric semantics are separated; Goal 2 and global integration are updated.

#### Stage Result

The literal 21-query search oracle reproduces every pre-Index/actual-Index count, and 25 evidence groups disposition all strict, Notes, split, Index, history, alias, implementation, parameter, application, stochastic, complex-block, and PDE candidates with zero unresolved remainder. T44 reconstructs one total `[0,1]` field on fixed ordered 1D support, synchronous old left/self/right reads, an exact affine aggregate plus closed scalar map, typed same-site assignments, and T01 atomic fixed-effects commit. Integer-line strict support remains a labeled inference; Notes ring, segment exterior, causal work, and render crop are distinct. Exact ideal fields, certified/tracked computation records, represented feedback, and stochastic draws have separate identities.

The exact semantic oracle covers mean/coefficient/mass, fractional-`3/2`, add-quarter/background, additive residues, weighted range, boiling equality, and noisy closure. Metadata reproduce all 17 included assets plus the excluded discrete page-339 plate; the runnable raster oracle passes pages 172-175 and both Notes panels, including the absolute-right observer discriminator. D096-D102 record direct snapshot-UPDATE reuse, field/numeric/support/observer semantics, and additive/coupled/boiling/noisy/probabilistic/block/PDE boundaries. Search, source, fence, hash, raster, semantic, diff, and all 102 repository-test gates pass. Next: T45.

### 20-T45-PDE

Status: **COMPLETE** in `goal-1/20-T45-PDE.md`.

#### Big Picture Objective

Test continuous space and time, derivative-defined evolution, initial/boundary conditions, and numerical approximation as an explicitly separate concern.

#### Detailed Implementation Plan

Apply the common protocol, distinguishing the equation from discretization, integrator, stability, resolution, and finite trace encoding.

#### Completion Requirements

All T45 evidence is captured; no discretized CA is presented as the PDE itself; any separate execution algebra is justified; Goal 2 and global integration are updated.

#### Stage Result

The exact 27-query oracle emits and verifies every pre-Index/actual-Index candidate manifest, and 28 evidence groups close strict, Notes, split, Index, equation-family, condition, method, solution, continuum-relation, history, application, and observer evidence with zero unresolved remainder. T45 reconstructs immutable scalar/complex/fixed-vector differential equations and `Classical` continuous-region/side-data problems whose denotation is a solution set, with no native source, UPDATE, successor, or halt unless a posed evolution derives one. Closed multivariate expressions, differential operators, fixed matrices, reduced-locus trace binders, versioned class/locus/admissibility claims, and proof-strength-preserving queries keep equation, problem, candidate, witness, realization, sample, and view identities distinct.

The semantic oracle passes exact heat/wave identities, the incompatible diffusion caption datum, nonlinear potential endpoint counterexample, background amplitude/periods, and the finite-difference kernel/grid. Metadata pin 23 included assets plus one material exclusion, and the analytic heat raster oracle passes. D103-D110 record the declarative ontology, syntax, IVP, proof, discretization, scope, and observer boundaries. All 87 quotes, 44 source bounds, Markdown fences, `git diff --check`, independent review, and all 102 repository tests pass. No prior stage reopened. Next: T02.

### 21-T02-MULTICOLOR-CA

Status: **COMPLETE** in `goal-1/21-T02-MULTICOLOR-CA.md`.

#### Big Picture Objective

Determine whether multi-color nearest-neighbor CA is purely alphabet/rule parameterization of the baseline.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing color count, ordered neighborhood table size, coding, seeds, and validation limits.

#### Completion Requirements

All T02 evidence is captured; reuse versus extension is proven; Goal 2 and global integration are updated.

#### Stage Result

The exact 29-query oracle partitions all 157 candidate lines, and 21 evidence groups close every strict, Notes, actual-Index, split, implementation, variant, property, application, search, and emulation route with no unresolved remainder. T02 is exactly the `k>=3`, radius-one finite-alphabet/table parameterization of T01: fixed ordered support, `AllSites`, ordered old left/self/right reads, one complete `k^3` table, typed same-site assignment, atomic commit, and deterministic continuation. The Wolfram codec uses `k^2*l+k*c+r`, preserves leading-zero rows, and requires arbitrary-precision tagged identity; no executor or update law is added.

All seven embedded oracles pass. They cover the `3^27` count, every binary specialization, asymmetric codes and exact source traces, evolving-background and fixed-width adversaries, 11 included/six excluded/two relation-only assets, the direct Voronoi priority-table expansion, ten reversible labels and inverse windows `3,4,5,6`, and the direct rule-921408 JPEG regression. All 48 quotes match the monolith. D111-D114 preserve alphabet/table/codec identity, rank/aggregate/palette separation, and mutation/reversibility/search/emulation boundaries. Independent re-review, fences, `git diff --check`, and all 102 repository tests pass; no prior stage reopened. Next: T03.

### 22-T03-TOTALISTIC-CA

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED** in `goal-1/22-T03-TOTALISTIC-CA.md`. T04's bounded repair proved that inherited page-263 raster `BOOK:2928` belongs to the already-retained two-dimensional totalistic gallery; the one-control repair is complete and the semantic result is unchanged.

#### Big Picture Objective

Model totalistic rule reduction as an explicit aggregation construction rather than a separate rollout.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing sums/averages, rule coding, state count, neighborhood arity, and symmetry consequences.

#### Completion Requirements

Completed: widened the named-code source/asset closure, preserved the valid aggregation/evaluation result, reran every embedded/global gate, and obtained fresh independent review before resuming T05 completion.

#### Stage Result

COMPLETE after bounded T05/T06/T04 repairs: the T04-era repair partitioned 309 candidates and 116 rasters at `48 included / 60 excluded / 8 relation-only`; the code-`1004600` Notes continuation and two linked plots widened that to 312/118, the direction-linked `BOOK:18770 -> 18772` emulation network widened it to 313/119, and the inherited page-263 slice control closes the final audit at 314 candidates and 120 rasters at `50 included / 61 excluded / 9 relation-only`. Exact radius-two code `10/20/52`, aggregate semantics, and all prior repairs remain valid.

The former `16-query / 118-candidate / 26-34-25-23-10` partition and associated split/evidence-group totals are retained only as historical audit output, not current exhaustion evidence. The valid semantic result is an explicit numeric valuation `nu:A->{0,...,k-1}` followed by the exact sum of `2r+1` old reads and a complete `M=1+(k-1)(2r+1)`-row structural table. The optional Wolfram code uses sum zero as the least-significant base-`k` digit. T01/T02 fixed-lattice assignment and atomic update are reused unchanged.

The six embedded blocks pass: source/evidence closure at 215 cited lines/89 fragments/86 quote lines, exact semantics, `50/61/9` metadata, 72 audited links, a 106-link mechanical reverse join with 22 control-only siblings outside, binary radius-two codes `10/20/52`, code-20 survival counts, code-357/code-1329 labels, code-420 additivity, exact code-777/code-867 trajectories, code-`1004600` and its long-run observers, and the 946-cell strict code-777 raster. D115-D118 preserve T04/T05 presets, T06/T07 restrictions/properties, and additive/outer/weighted/histogram/higher-dimensional/continuous/emulation/observer boundaries. Fresh independent review, fences, `git diff --check`, and all 102 repository tests pass; every reopening is resolved. T04's bounded repair is independently reclosed; next: T06.

### 23-T04-THREECOLOR-TOTALISTIC

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED** in `goal-1/23-T04-THREECOLOR-TOTALISTIC.md`. T06 found omitted direct raster links at `BOOK:17431 -> 17433` and `BOOK:2922 -> 2924`; the bounded audit also inherited the page-263 slice control. The asset/reverse-join repair is complete and preset semantics are unchanged.

#### Big Picture Objective

Validate the emphasized three-color totalistic catalog entry as a preset, restriction, or distinct construction.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing seven sum cases, rule numbering, seeds, and background filtering.

#### Completion Requirements

Completed: repaired all three inherited raster omissions, reran every embedded/global gate, obtained fresh independent review, and preserved the already-proved preset semantics.

#### Stage Result

COMPLETE after bounded T06 repair: 12 queries plus governed follows close 246 candidates in the exact partition `34/53/11/20/54/30/27/17`; 15 evidence groups close 260 cited lines, 92 fragments, and 90 quote lines. The repaired ledger closes 75 assets at `35 included / 34 excluded / 6 relation-only` and 150 exact reverse references, including `BOOK:2924` and `BOOK:2928` as controls and `BOOK:17433` as a relation. All six embedded checks, asset identities, independent review, fences, `git diff --check`, and all 102 repository tests pass. The exact `k=3,r=1,A=(0,1,2),nu(i)=i` preset, seven cases, 2,187 codes, D115-D118, and shared executor/update result remain unchanged. Next: T06.

### 24-T05-HIGHERCOLOR-TOTALISTIC

Status: **COMPLETE** in `goal-1/24-T05-HIGHERCOLOR-TOTALISTIC.md`.

#### Big Picture Objective

Validate higher-color totalistic systems and parameter scalability against the shared aggregation model.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing general `k`, reachable-sum sets, rule counts, and finite-table validation.

#### Completion Requirements

All T05 evidence is captured; parameter bounds and reuse are explicit; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE: 11 controlled query families close 142 lexical lines, five governed follows and 25 assets expand the exact partition to 172 candidates, and 12 evidence groups close `47/47/40` provenance/fragment/quote-line counts. The asset audit closes `5 included / 13 relation-only / 7 excluded`; exact page-122/page-256 label corpora, code `1004600`, cardinality, bigint, snapshot, and boundary oracles pass. The result is the strict finite `k>=4,r=1` canonical preset over generic T03. T03's discovered source omissions were repaired and reclosed; T04 was later reopened only for its own T06-discovered asset gap. D118 is sharpened without D119, an executor, or an update law. Independent review, five embedded blocks, fences, diff checks, and all 102 tests pass. Next: T06.

### 25-T06-QUIESCENT

Status: **COMPLETE** in `goal-1/25-T06-QUIESCENT.md`; T06 is a generic typed property/restriction over an unchanged eligible CA-axis program, not a construction or execution branch.

#### Big Picture Objective

Determine whether quiescent-background preservation is a rule invariant, family filter, boundary condition, or seed property.

#### Detailed Implementation Plan

Apply the common protocol, grounding blank-state preservation and finite-seed behavior in book evidence.

#### Completion Requirements

All T06 evidence is captured; the invariant is placed once in the generic property layer; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE: the exact evidence union reconciles the retained nine-family diagnostic, the 19-family/280-line core, and five governed continuations into 329 unique canonical lines with the disjoint partition `4 direct / 30 CA property relations / 129 CA seed-background-profile controls / 76 sibling SimpleProgram controls / 21 general controls / 69 actual-Index routes`. The physical-asset ledger closes 47 files at `5 included / 29 relation-only / 13 excluded`, with 94 monolith/split references, exact metadata, and zero unresolved remainder.

T06 resolves to the class-2 restriction `evaluate_P(exact_uniform_read_P(b)) = b` over a strictly eligible resolved CA program. Exact elementary/totalistic counts, a nonzero-blank codec adversary, the page-262 `64 total / 32 preserving / 30 displayed` source repair, hostile-boundary separation, finite-cone qualification, and identity preservation pass. D119 adds only generic claim/evidence/selection records; the 15-group Goal 2 handoff covers membership collisions, unsupported shapes, stale/tampered evidence, serialization, and no-cheating checks. No construction, runner branch, update law, outcome, halt, alphabet role, or sparse-background optimization is added, and no prior stage reopens. All six embedded checks, independent review, Markdown/diff gates, and 102 repository tests pass. T07, T08, T10, T11, T14, T15, and T18 subsequently complete under D120-D126; next: T21.

### 26-T07-SYMMETRIC

Status: **COMPLETE** in `goal-1/26-T07-SYMMETRIC.md`. T07 is a class-2 property over an eligible resolved program and explicit action; reflection is a separate transform and a canonical orbit table is an optional class-3 lossless RULE representation. D120 is active.

#### Big Picture Objective

Determine how left-right symmetry constrains rule construction and relates to isotropic and totalistic reductions.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing reflection orbits, validation, rule counts, and interactions with quiescence.

#### Completion Requirements

All T07 evidence is captured; symmetry is not duplicated as family behavior; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE after hostile reclosure. The original 357-line/22-asset manifest remains an explicitly superseded bounded diagnostic. The authoritative protocol closes 650 monolith lines at `15/190/25/167/179/74`; its manually adjudicated 162-line supplement is pinned rather than presented as mechanically regenerated. All 114 retained saturation additions have split reverse coverage at `103 exact + 11 variants`. The fixed-point asset universe closes 271 JPEGs/542 references at `4/38/229` with 271 unique hashes.

T07 adds no construction or execution branch: local displacement reflection is a class-2 property over one exact admissible typed read space and a single diagonal action; reflected programs are separate transforms; orbit tables are optional class-3 RULE representations. The repair separates typed positions, component/value/output actions, admissible-space closure `rho_alpha(V_P)=V_P`, and support-point from displacement reflection. D120 is active. All six embedded blocks, independent hostile review, Markdown/diff gates, and 102 repository tests pass. T08, T10, T11, T14, T15, and T18 subsequently complete under D121-D126; next: T21.

### 27-T08-INITIAL-CONDITIONS

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED** in `goal-1/27-T08-INITIAL-CONDITIONS.md`. T08 is an event-zero configuration/class/law axis over an unchanged resolved program; D121 is active.

#### Big Picture Objective

Separate initial-condition experiment classes from program types while preserving catalog traceability.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing exact configurations, deterministic constructors, configuration classes, stochastic laws, complete/cylinder/algorithmic realizations, native support, invariants, finite lowering, boundary, trace, and view distinctions.

#### Completion Requirements

All T08 evidence is captured; seeds remain independent where semantics permit; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE after hostile source, asset, and architecture reclosure. The 16-query source protocol closes 1,205 query-union lines plus five governed continuations, with 701 retained construction lines, 439 duplicate/control lines, and 70 actual-Index routes in a 1,210-entry declared audit. All 701 retained lines have split reverse coverage at `634 exact + 67 non-exact variants`. The frozen asset universe closes 577 JPEGs at `363 direct / 198 relation / 16 control`, with 1,152 references (`577 monolith + 575 split`), two explicit split omissions, and 577 unique hashes.

T08 adds no construction-specific DOMAIN, state family, FRONTIER, NEIGHBORHOOD, RULE result, UPDATE policy, successor algebra, executor, outcome, halt, or transition-time RNG. It supplies typed complete configurations, constructors, classes, probability laws, capability-scoped realizations, validation, finite lowering relations, and observers over the unchanged program. Finite cylinders are not complete infinite states; algorithmic fields are not silently equated with ideal product-measure draws; complete native traces remain distinct from proved horizon-scoped decoded lowering observations. D121 is active. The source, asset, semantic, Markdown, diff, independent-review, and 102-test gates pass. T10, T11, T14, T15, and T18 subsequently complete under D122-D126; next: T21.

### 28-T10-EXTENDED-MOBILE

Status: **COMPLETE — EVIDENCE, ASSETS, AND ARCHITECTURE RECLOSED** in `goal-1/28-T10-EXTENDED-MOBILE.md`; D122 is active.

#### Big Picture Objective

Test wider local write scopes while retaining a single active locus and movement.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing source-relative multi-target writes, atomicity, compact rule identity, active-marker preservation, boundary scope, and the distinction between T09 parameterization and any genuinely new execution algebra.

#### Completion Requirements

All T10 evidence is captured; wider writes reuse principled effects rather than a special rollout; Goal 2 and global integration are updated.

#### Stage Result

The exact 18-query oracle closes a 183-line union at `161 pre-Index / 22 actual-Index`, partitions the pre-Index set as `66 retained / 95 excluded`, and adds 22 governed continuations for 88 retained lines. All 17 physical split documents reverse-close at `171 exact + 12 mapped query variants` and `83 exact + 5 mapped retained variants`; the Atlas and catalog are pinned, the catalog name is absent from the book, malformed Notes extraction is explicit, and zero source candidate remains unresolved. The governed asset fixed point separately records the strict 14-file subledger and every wider source-neighborhood relation/control candidate with exact physical identities, reverse references, and hashes.

T10 is exactly the T09 one-active binary line with a wider native table `Bit^3 -> Bit^3 x {-1,+1}`. The result lowers to three distinct complete tagged labels; the unique destination carries its new block bit, and generic D011 atomic finite-write UPDATE commits all three from one snapshot. The Notes row `000 -> 111,+1` proves strict T09's center-only result is insufficient while the exhaustive 2,048-case factored/tagged oracle proves no new execution algebra is needed. The rule count is `16^8=2^32`; the structural table is primary and optional planes `(115,37,103,196)` are explicitly inferred rather than source identity.

Exact `t0..t12`, outside-preservation, exactly-one-tag, fail-closed source/asset/semantic, target-radius-two CA-compiler, Markdown, diff, scope, independent-review, and all 102 repository-test gates pass. D122 adds no state class, control payload, UPDATE law, executor, family branch, boundary, halt, or collision policy. T11, T14, T15, and T18 subsequently complete under D123-D126; no prior stage reopens. Next: T21.

### 29-T11-GENERALIZED-MOBILE

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, AND ARCHITECTURE CLOSED** in `goal-1/29-T11-GENERALIZED-MOBILE.md`; D123 is active.

#### Big Picture Objective

Test multiple active loci, activity creation/deletion, simultaneous effects, and collisions.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing active-set state, split/disappear rules, update grouping, and evidence for conflict semantics.

#### Completion Requirements

All T11 evidence is captured; unspecified conflicts remain explicit obligations rather than invented behavior; Goal 2 and global integration are updated.

#### Stage Result

The exact 16-query oracle closes a 130-line union at `108 pre-Index / 22 actual-Index`, retains 20 query hits plus six governed continuations, excludes 88 false positives, and leaves zero source candidate unresolved. All 17 split documents reverse-close at `123 exact + 7 extraction variants`. The source-bound asset fixed point contains 16 unique JPEGs at `C/O/R/X=2/1/10/3`, 32 monolith/split references, and 16 hashes; the direct BOOK:922/926/932 plates pin the rule/result glyphs and evolution without turning crops into boundaries.

T11 is the T09 binary fixed integer line with a canonical finite active set rather than exactly one tag. Every old active source reads physical `[left,self,right]` bits from one snapshot and returns `(new_source_bit,finite_relative_activity_set)`. UPDATE applies owner-unique source-bit assignments and replaces activity by the associative, commutative, idempotent union of translated proposals. After normalization, complete tagged writes on `A_old union A_next` reuse D011 atomic commit. Activity collisions coalesce; there is no value-write conflict or arbitrary policy.

The local page-76 profile is `Bit^3 -> Bit x P({-1,0,+1})` with a derived `16^8=2^32` rule space, while the wider Notes carrier permits finite relative integer sets and has no source-defined code. The corrected BOOK:922 row is `000 -> (1,{-1,+1})`; inferred planes `(63,15,16,245)`, exact `t0..t12`, and 157,184 exhaustive composition/representation cases pass. Empty-frontier continuation remains `SourceUndefined(NoActiveSources)`, not an invented halt or stutter.

D123 adds only generic `ParallelFactorCompose` with `DistinctAssign` and `ReplaceWithUnion` inside the same runner. Independent hostile review is clean; source/asset/semantic root, `/tmp`, optimized-mode, Markdown, diff, scope, coverage, and 102-test gates pass. No prior stage reopens. T14, T15, and T18 subsequently complete under D124-D126; next: T21.

### 30-T14-CONTEXTUAL-SUBSTITUTION

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/30-T14-CONTEXTUAL-SUBSTITUTION.md`; D124 is active.

#### Big Picture Objective

Add neighbor-dependent replacement choice to variable-length parallel substitution.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing context windows, right-edge behavior, replacement alignment, and interaction between reads and source emissions.

#### Completion Requirements

All T14 evidence is captured; boundary and context semantics are explicit; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 308-line source audit, 22-asset fixed point, direct page-85 rules/seeds/traces, open-right boundary, empty/singleton behavior, 164,592-case generic commuting proof, 4,080 singleton-output relation proof, opaque exact-snapshot handle adversary, architecture audit, Goal 2 handoff, and global integration are closed. T14 parameterizes the shared ordered-generation construction with `HasRightNeighbor`, `(Self,Right)`, and `Sigma^2 -> Sigma+`; it adds no UPDATE algebra or executor. Independent hostile review is clean after its status, handle-scope, and raster-wording findings were repaired; T15's later same-generation collision adversary further strengthens the shared handle proof without reopening T14. All root/`/tmp`/optimized-mode, Markdown, diff, scope, coverage, and 102-test gates pass. No prior stage reopens. T15 and T18 subsequently close under D125-D126; next: T21.

### 31-T15-CREATION-DESTRUCTION

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/31-T15-CREATION-DESTRUCTION.md`.

#### Big Picture Objective

Test empty and multi-element replacements, extinction, and balanced growth as native support changes.

#### Detailed Implementation Plan

The source, asset, semantic, architecture, hostile-review, and final global gates are complete. Preserve the D125 result; T18 subsequently closes under D126 and T21 is next.

#### Completion Requirements

All T15 evidence is captured; dynamic support handles creation/destruction without sentinels; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The repaired 22-query/351-line source closure, 23-asset fixed point, seven exact tables/seeds/`t0..t11` traces, 304,927-case commuting proof, explicit epsilon/zero-source/extinction witnesses, opaque exact-snapshot handle adversaries, D125 integration, and clean independent hostile review close T15. It widens only the private ordered-emission carrier to `Sigma*`; strict T13/T14/T16 validators remain nonempty. All root/`/tmp`/optimized-mode, Markdown, diff, scope, coverage, and 102-test gates pass. No new state class, UPDATE algebra, executor, family branch, sentinel, or growth policy is justified; no prior stage reopens. T18 subsequently closes under D126; next: T21.

### 32-T18-CYCLIC-TAG

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/32-T18-CYCLIC-TAG.md`.

#### Big Picture Objective

Add cyclic program control and conditional append behavior to tag-system semantics.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing visible cyclic focus, trigger semantics, deletion, append schedule, and complete state.

The 19-query source audit closes 305 candidates with 160 retained and zero unresolved; the source-bound closure has 43 assets and five full page-96 `t0..t99` fixtures. The 71,442-case semantic oracle closes the occurrence-addressed tagged representation `Phase(slot) · Data(word)` and the explicit equal-rotation Notes quotient: one old-snapshot ordered multi-span commit replaces the phase/head prefix and conditionally inserts the scheduled block at the old endpoint. Empty activity still traverses all four axes. D126 reuses T17/D024/D032/D039 without a cyclic executor or new UPDATE algebra.

#### Completion Requirements

All T18 evidence is captured; cyclic control is state rather than executor memory; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. Exact source/split/Index and 43-asset fixed points, the page-95 `t0..t24` and five page-96 `t0..t99` fixtures, 71,442 direct/tagged commuting cases, 1,806 shared T17 span cases, 255 natural-multiplicity cases, branch-free empty-axis flow, the named-slot/Notes-value quotient distinction, strict exact-type and snapshot/provenance adversaries, D126 integration, and clean hostile review close T18. Root/`/tmp`/optimized-mode fail-closed, Markdown, diff, scope, coverage, and all 102 repository-test gates pass. No prior stage reopens. Next: T21.

### 33-T21-2D-CA

Status: **COMPLETE** in `goal-1/33-T21-2D-CA.md`.

#### Big Picture Objective

Validate dimensional and lattice generalization of CA with two-dimensional neighborhoods and seeds.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing square-grid geometry, orthogonal neighbors, totalistic variants, boundaries, and spatial initial patterns.

#### Completion Requirements

All T21 evidence is captured; dimension is parameterized without PE-specific semantics; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The repaired source fixed point closes 338 evidence lines at `130 native / 75 relation / 133 control`, with 42 exclusions, zero unresolved, and retained split closure `270 exact + 68 nonexact`. The asset candidate fixed point closes 113 files as `53 governed + 60 adjacency-only`, 226 references, 113 hashes, and an honest 14-record hash-bound/not-pixel-replayed transcript ledger. The semantic oracle closes 17,728 independent native/generic events plus 160 Book-to-ENU basis-permutation cases, explicit Self access, exact 32/10/6 rule schemas, nonaliasing direction tests, and support/background/boundary separation. D127 reuses T01/T02/T03/T08 without a 2D state, new UPDATE, executor, family branch, or hidden center/boundary. Clean hostile review, root/`/tmp`/optimized-mode, import/compile/fence/diff/scope gates, and all 102 tests pass. No prior stage reopens. Next: T22.

### 34-T22-MOORE-CA

Status: **COMPLETE** in `goal-1/34-T22-MOORE-CA.md`.

#### Big Picture Objective

Validate Moore adjacency and center inclusion as neighborhood/rule parameters.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing eight neighbors, center handling, neighbor counts, and square-grid symmetry.

#### Completion Requirements

All T22 evidence is captured; no duplicate executor or rule family is introduced; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 17-query source union closes 164 lines at `117 pre-Index / 47 actual-Index`, with 270 retained (`96 native / 102 relation / 72 control`), 24 exclusions, and retained split closure `192 exact + 78 variants`. The asset fixed point closes 95 candidates as `68 governed + 27 adjacency-only`, 190 references, 95 hashes, and `95 hash-bound / 28 transcribed / 0 pixel-replayed`. The semantic oracle closes 1,419 native/generic events, complete positional/outer/totalistic/growth schemas, C4/D4 orbit restrictions at 140/102, printed `3702` to canonical `630`, 262,144 WireWorld predicate-count contexts, and a concrete Dyadaxes-loss witness. D128 reuses T01/T02/T03/T08/T21 through audit categories 1–3 without a state/control class, UPDATE, executor, family branch, hidden center/boundary, Life/symmetry engine, or raster rule. Clean hostile review, all portability/format/scope gates, and 102 tests pass. No prior stage reopens. T23 subsequently closes under D129. Next: T24.

### 35-T23-3D-CA

Status: **COMPLETE** in `goal-1/35-T23-3D-CA.md`.

#### Big Picture Objective

Validate cubic-lattice state, six- and twenty-six-neighbor variants, and 3D seeds.

#### Detailed Implementation Plan

Apply the common protocol, separating construction semantics from visualization requirements.

#### Completion Requirements

All T23 evidence is captured; 3D neighborhoods reuse general geometry where justified; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The nineteen-query source oracle closes 151 lines at `104 pre-Index / 47 actual-Index`; 138 retained evidence lines partition as `76 native / 16 relation / 46 control`, with 32 exclusions, zero unresolved candidates, and retained split closure `123 exact + 15 variants`. The declared one-hop radius-four asset universe closes 42 plates at `10 governed + 32 adjacency-only`, 84 references, 42 hashes, and `42 hash-bound / 9 transcribed / 0 pixel-replayed`. The semantic oracle closes 5,139 native/generic events, explicitly fires all 14/7 face and 54/27 full product/shell indices, proves positional/frame maps and quotient multiplicity, uses nonvacuous named and sum-sensitive ternary fixtures, and gives two Dyadaxes-loss witnesses. D129 reuses T01/T02/T03/T08/T21/T22 through categories 1–3 without a state/control class, UPDATE, executor, family branch, hidden Self/boundary, callback, or raster rule. Clean hostile review, all portability/format/scope gates, and 102 tests pass. No prior stage reopens. Next: T24.

### 36-T24-HIGHERDIM-CA

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/36-T24-HIGHERDIM-CA.md`; D130 is active.

#### Big Picture Objective

Test arbitrary dimension, lattice geometry, and symmetry beyond the current `t+3D` API envelope.

#### Detailed Implementation Plan

Apply the common protocol, evaluating native rank, flattening, graph adjacency, metadata, and what distinctions ANKoS must preserve.

#### Completion Requirements

All T24 evidence is captured; any coordinate limitation or schema change is stated honestly; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The repaired 30-query source oracle closes 218 lines at `168 pre-Index / 50 actual-Index`; 166 retained evidence lines partition as `80 native / 21 relation / 65 control`, with 77 exclusions, retained split closure `150 exact + 16 variants`, entry-specific guards for every dense Index line, and zero unresolved candidates. The dependent radius-four asset universe closes 36 plates at `11 governed + 25 adjacency-only`, 72 references, 36 hashes, and `36 hash-bound / 6 transcribed / 0 pixel-replayed`. The strengthened semantic oracle closes 1,791 non-vacuous native/generic events plus 46 hostile rejections, with exact basis inverses/physical commutations, physically derived hex actions and 1,024 codec/event commutations, inclusive-total and canonical-slot network views, sampled visible rule-bank reuse, concrete typed-offset divergence, read provenance, occurrence multiplicity, and snapshot parallelism. D130 uses categories 1–3 and adds no T24 UPDATE or executor. The independent hostile review is clean; all oracle portability/fail-closed/import/compile/Markdown/diff/scope/mode gates and 102 tests pass. No prior stage reopens. Next: T25.

### 37-T25-2D-TURING

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/37-T25-2D-TURING.md`; D131 is active.

#### Big Picture Objective

Validate Turing-machine reuse when tape support and movement become two-dimensional.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing movement set, position, revisitation, blank support, and dimensional parameterization.

#### Completion Requirements

All T25 evidence is captured; dimensional reuse is proven without a separate rollout; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The Q00-Q29 source oracle closes 71 lines at `50 pre-Index / 21 actual-Index`, retains 63 at `30 native / 29 relation / 4 control`, excludes 13, reverse-joins all retained lines to the split corpus, and leaves zero unresolved. The dependent 12-image universe closes 24 references, 12 hashes, 562,275 bytes, and `12 hash-bound / 0 transcribed / 0 pixel-replayed`. The semantic oracle proves 3,118 native/generic events and 38 hostile rejections: tagged/factored one-step equivalence, self-only RULE visibility, destination-preserving UPDATE, all strict local outcomes, exact Langton C4, relative-turn nonimages, six-port topology, declared coordinate-frame mapping, quotient aliases, unbounded travel, immutable setup provenance, and observer separation. Primary text fixes four square-grid movement choices but not their exact coordinate-vector binding; the oracle's cardinal map is an explicit conventional realization, while Langton's formula independently fixes its unit-complex moves. D131 composes T12, D011, D127, and D130 in audit categories 1–3. `src/ca` remains the shared SimpleProgram substrate; T25 adds no state/control class, UPDATE algebra, executor, branch, callback, hidden control, arbitrary-CA identity, destination-label RULE read, implicit boundary, raster program, or invented worm codec. All gates and 102 repository tests pass. No prior stage reopens. T26 subsequently closes under D132; next: T28.

### 38-T26-2D-SUBSTITUTION

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/38-T26-2D-SUBSTITUTION.md`; D132 is active.

#### Big Picture Objective

Test parallel replacement of rectangular-grid tile labels by compatible rectangular block mosaics while keeping geometric role decoding, off-grid geometry, and contextual patch choice separate.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing finite tile labels, total closed patch tables, generic `RankedBlockMosaicAssemble`, exact old-snapshot `Flatten2D` product order, typed no-commit incompatibility, parent consumption, newborn deferral, rendering separation, and the boundary to unproved geometric decoding, free geometry, and contextual choice. The named uniform wrapper requires positive old/block extents. Treat `BOOK:13744` as a native opaque-label compatible preset only after the guarded deletion of its one surplus closing brace.

#### Completion Requirements

All T26 evidence is captured; shared replacement semantics and geometry-specific requirements are separated; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The frozen Q00-Q29 source audit closes a 94-line query union at `67 pre-Index / 27 actual-Index`; 56 matched retained lines plus 59 governed continuations yield 115 retained lines at `23 native / 67 relation / 25 control`, with 11 exclusions, retained split closure `77 exact + 38 mapped`, and zero unresolved. The 26 governed JPEGs partition `3 native / 16 relation / 7 control`, close 52 monolith/split references, 26 unique hashes, 1,838,481 bytes, and five assemblies covering 14 files, and remain `26 hash-bound / 0 transcribed / 0 pixel-replayed`. The semantic oracle proves 6,667 distinct native/generic events, 6,658 prototype-keyed full-`StepResult` T27 bag commutations, and 16,709 selected-frontier rank-one mosaic commutations for 30,034 total; canonical fixture overlaps are recorded but not added twice. It also closes 81 hostile rejections and two typed invalid/no-commit outcomes. The rank-one partition is 1,519 all-selected plus 15,190 with unselected sources; the original 1,470 positive all-selected cases, 49 empty inputs, 98 singleton/no-selected cases, 1,390 selected-epsilon cases, 1,519 right-neighbor cases, and 600 fixed-positive cases are explicit overlapping subsets. T26 is discrete `t+2D` over a finite nonempty rectangular tile grid: `AllOldTiles` reads Self only, a total closed `TileLabel -> nonempty rectangular patch` table emits typed blocks, and generic `RankedBlockMosaicAssemble(rank=2)` validates equal patch heights within each source row and equal total slab widths across source rows before exact old-snapshot `Flatten2D` assembly, parent consumption, and newborn deferral. Patch widths need not agree down source columns; the crossed-width witness advances with two width-three slabs. Incompatibility returns `PatchStepResult(Invalid(IncompatibleMosaic(...)), successors=(), step=None)` before commit. D019 selected-source `OrderedGenerationConcat` is the rank-one member: unselected parents are consumed, selected epsilon remains explicit, and empty/no-selected events produce the empty successor. The named uniform wrapper requires positive extents. This ranked-mosaic policy is a justified implementation on the existing UPDATE axis, not a new execution algebra. `BOOK:13744` supplies native opaque-label rule/seed data only after deleting its single guarded surplus closing brace; no geometric role codec is invented and image `BOOK:13742` remains relation evidence. Independently, only the uniform aligned subset has the proved category-3 D041-D043 T27 map. Encoding maps the source token; grid and bag derive successor tokens independently; a reversible bijection over the two source/successor pairs preserves `Advanced.changed`, singleton successor cardinality, step presence, the successor carrier, rectangles/patches, every parent-local target/prototype/pose, and complete lineage. Mixed-mosaic one-step pose commutation is not claimed. Arbitrary free geometry remains T27; neighbor-dependent choice remains T28; white is ordinary; raster, scale, coordinate formulae, and fractal limits remain observers or relations. No T26 state class, execution algebra, executor, family branch, callback, hidden control, padding/cropping, implicit-white behavior, raster rule, invented geometric codec, or mixed-mosaic T27 step claim is added. Oracle SHAs are source `124b2be2c5ac1121946f7fe952d83ca93403782998992ffcd5974d9c8339b5f2`, asset `e36e7ec66460c81cd5d78f0dbe39188c431961c135b7c76a87be68e369ffd438`, and semantic `10395a02c1bd44514e610c98e1efc861513541a0b8b7046fedd557629e43a0f4`; the frozen semantic digest is `e380704a0626ad7a578e0937007cfa6ea8cc0dd6cee1b8c2d24a7eab18b7c57c`. All oracle root/relocated/import/compile/optimized-mode/format/scope gates, 102 repository tests, and independent hostile review pass. No prior stage reopens; 37 of 45 type stages remain complete. Next: T28.

### 39-T28-CONTEXTUAL-2D-SUBSTITUTION

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/39-T28-CONTEXTUAL-2D-SUBSTITUTION.md`; D133 is active.

#### Big Picture Objective

Combine 2D patch replacement with neighbor-dependent rule choice and boundary semantics.

#### Detailed Implementation Plan

Apply the common protocol, stressing the source's finite periodic two-dimensional grid, all-old-tile firing, immutable overlapping `2 x 2` contextual windows, closed pattern-to-patch choice, exact old-snapshot `Flatten2D` assembly, parent consumption, newborn deferral, and compositional reuse of T14's contextual-read result with T26's rank-two mosaic UPDATE. Audit the exact `Partition[list,{2,2},1,-1]` alignment and cyclic boundary rather than importing a menu of boundary policies. Keep raster-only rule rows, free geometry, sequential scanning, constraints, and arbitrary callbacks outside the strict construction unless primary evidence proves them.

#### Completion Requirements

All T28 evidence is captured; no duplicated contextual-replacement engine is proposed; Goal 2 and global integration are updated.

#### Stage Results

COMPLETE. The frozen 25-query source audit closes 67 lines at `52 pre-Index / 15 actual-Index`, retains 72 at `6 native / 13 relation / 53 control`, excludes 11, reverse-closes retained split evidence at `49 exact + 23 mapped`, and leaves zero monolith-only/unresolved evidence. The official `_` row is frozen offline under snapshot SHA `ba1aff54973afd0cd42cb7afc41220dd11835a0cb5b3d8d9ce8f5e9fe3d1b866`, which records fetched-document SHA `f28a332211082048417abce950a75756a4bdae7c7d48f3f12ab87ffdab02328c`; the source oracle derives the repaired Book row from it. Official Wolfram Language `Partition`, `Part`, `Blank`, and `ReplaceAll` semantics are frozen under snapshot SHA `89dc720f5f905d41821c4284457cf75d08de2cae66af501789f26746682c6589`, binding lower-right cyclic alignment, `_`, priority, and schema-qualified unchanged nonmatch. Ten governed assets partition `1 native / 2 relation / 7 control`, close 20 references, ten hashes, 1,112,143 bytes and two assemblies/four files, and remain `10 hash-bound / 1 limited-transcribed / 0 pixel-replayed`; the complete raster rule table, seed, trace, and palette mapping remain unavailable. The semantic oracle closes 682 periodic configurations/5,506 ordered reads, the repaired Blank row at two of sixteen contexts, 65,536 independently typed complete-result commutations/1,048,576 firings/4,194,304 child witnesses, 57 hostile rejections, one compatible crossed-width aligned mixed mosaic, two typed invalid/no-commit commutations, and one lower-right/upper-left divergence. D133 composes D127 periodic configuration/access, T14 contextual-read responsibility, T26 source-bound patches, and D132 rank-two mosaic UPDATE. Ordered closed `Literal | AnonymousAny` product rows use official first-match semantics and construction-time totality; exact host nonmatch is materialized by the declared product-pattern importer, exhaustive compilation retains source AST/provenance, and context cells are not parents. The unequal-subdivision warning remains an open adaptive carrier/topology profile. Oracle SHAs are source `28fa3d71612a3d3ae109f6e245c1155ea9d4e74967c6a3c32394e77778a6aee3`, asset `95fe4b6dbda261a9068d6c7a6b8aa1765bcb0ef19e444abebe47895569731c77`, and semantic `1faca62a3261a4b328cb70d6daebd00b916788c63e4e4f77109754ccee8715ef`; the semantic digest is `82b03edcc186e9ceccdffb33f1e90fb671a64e4dd008eec057a11f6339f44209`. No T28 state, UPDATE, executor, branch, callback, implicit fallback, raster program, padding/reflection menu, hidden scan, or flat assembly is added. All gates pass; no prior stage reopens. T32 and T33 are subsequently complete under D134-D135; next: T35.

### 40-T32-TEMPLATE-CONSTRAINTS

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/40-T32-TEMPLATE-CONSTRAINTS.md`; D134 is active.

#### Big Picture Objective

Model exact allowed local templates and overlap consistency as a specialization of constraint semantics.

#### Detailed Implementation Plan

Apply the declarative non-rollout protocol, emphasizing finite total offset-to-label templates, exact orientation, one-field overlap, static support, explicit periodic/open/window scopes, verifier/query/solver separation, source-derived codecs, and T31 lowering. Keep source codec order distinct from unordered semantic support; make rotation/reflection/color exchange explicit transforms; keep T33 occurrence separate.

#### Completion Requirements

All T32 evidence is captured; template constraints reuse the correct declarative layer; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 39-query source audit closes 92 lines at `77 pre-Index / 15 actual-Index`, retains 169 at `18 native / 67 relation / 84 control`, excludes two, reverse-closes retained split evidence at `119 exact + 50 mapped`, and leaves zero unresolved. Official checking-note and three-argument `Partition` snapshots close the Blank/`Alternatives` repair and complete-window/drop-incomplete behavior under SHAs `15e06813de186756952e5ec1d465ed4cec7931fc388b68e08437af1cd0c6678f` and `716958949c69e2c6ade2e196a412c7baa8391c31eaa20119a97712275617edf9`; the unchanged inherited T28 language-semantics snapshot SHA `89dc720f5f905d41821c4284457cf75d08de2cae66af501789f26746682c6589` independently supplies `_ = Blank[]`. Forty-two governed assets partition `4 native / 12 relation / 26 control`, close 84 references, 42 hashes, 3,571,461 bytes, and eight assemblies/23 files, and remain `42 hash-bound / 0 limited-transcribed / 0 pixel-replayed`; the raster 171-family matching/analyzer table remains unrecovered. The semantic oracle closes 666 configurations/5,328 native-generic full reports/43,664 checks; all 1,024 strict binary degree-four center-conditioned T31 histogram relations with 21,712 lowering commutations/109,200 checks; explicit C4, determinant-negative reflection, binary color-exchange, and generic support-order transforms; strict source-derived numeric codecs; overlap/alias/scope/query/T33 boundaries; and 68 hostile rejections. T32 is a static discrete 2D declarative model set with no native `t`: one closed exact-pattern node extends D058/T31, T31 normalizes losslessly into it, and the north/east same-histogram witness prevents false reverse collapse. Codec slot order, Book coordinates, compass adapters, symmetry transforms, pointwise identity, and orbit observers remain explicit and separate. D134 adds no state/category, transition axis, UPDATE, executor, callback, implicit matching, repair dynamics, hidden solver, finite boundary, raster program, or T33 flag. Oracle SHAs are source `7ac7b234fe272bd2992f5e83594f4333f05b433d96abfac7f4f3b1f68e5f5881`, asset `1ba29a655bde67ac853e3160bbb92c901f79ae784adcd6c7c2cfc381998ba18f`, and semantic `055e54f4bf2bac09fe0b2ed2290cdb950472ef04f467b277b32537d655c768db`; the semantic digest is `72b671c04ac5e5a27ab1c2c2e86612b4ac1e493ab5722e89dc187b4d0939cbd5`. All gates pass; no prior stage reopens. T33 is subsequently complete under D135; next: T35.

### 41-T33-SEEDED-CONSTRAINTS

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/41-T33-SEEDED-CONSTRAINTS.md`; D135 is active.

#### Big Picture Objective

Add required template occurrence without conflating an unanchored global existential with initial state or a fixed semantic anchor.

#### Detailed Implementation Plan

Apply the declarative non-rollout protocol. Compose T32 `AllowedLocalPatterns` with a closed `RequiredPatternOccurrences(EACH_SOMEWHERE)` node; treat the centered figure/search witness only as a translation gauge with provenance. Close the `32 * 2^32` source count, strict singleton and Notes all-required profiles, required-not-allowed inconsistency, exact periodic/window scopes, witnesses, translation/symmetry transforms, solver separation, and the nonlocal counterexample. Add no seed, fixed-anchor menu, FRONTIER, RULE, UPDATE, or executor.

#### Completion Requirements

All T33 evidence is captured; seed requirements are placed in the correct semantic layer; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 32-query source audit closes 65 lines at `56 pre-Index / 9 actual-Index`, retains 191 at `33 native / 49 relation / 109 control`, reverse-closes retained evidence at `137 exact + 54 mapped`, and leaves zero unresolved. Forty-two governed assets partition `7 native / 11 relation / 24 control`, close 84 references, 42 hashes, 4,668,695 bytes, and nine assemblies/20 files, and remain `42 hash-bound / 0 limited-transcribed / 0 pixel-replayed`. The semantic oracle closes 666 configurations, 256 strict constraints, 170,496 direct/generic complete-report commutations, 1,397,248 anchor checks, explicit translation/D4/color transforms, singleton/all-required/empty-identity behavior, conjunct-local occurrence witnesses, all scope distinctions, replayable emptiness certificates, the remote-defect nonlocal counterexample, separate binary nine-slot and 16-color four-slot fixtures, and 62 hostile rejections.

D135 reconstructs T33 as structural `AllOf(AllowedLocalPatterns, RequiredPatternOccurrences(EACH_SOMEWHERE))` inside D058/T31/T32. The source count `32 * 2^32` proves independent requirement syntax; required-not-allowed is valid empty denotation. Centering is witness/search gauge, and every-template mode is a conjunction of independent existentials. IDs are provenance rather than hidden lookups; static `loci.gather` adapters must validate `t=0`; occurrence-witness replay proves only its conjunct, while whole verification independently checks T32 locality. No seed, fixed anchor, state/category, transition axis, UPDATE, executor, callback, implicit symmetry, repair/search dynamics, combined source codec, or raster program is added.

Oracle SHAs are source `f7266058575861d5aa358f4a031ea22a61be8251c0ac8c34027e66d6db5063ec`, asset `d3d506796c43881e6da8dd2ac0dcd514a5def4ecd9531d868c4b897d15ea6cc6`, and semantic `9ccf511f4d4a1192c6b62ff9863e0630b5811240bdfaf5b3b9651d03a29485ba`; semantic digest is `54276cd1279b01e75ebe8495c528e5991f0b6c6387ec9744dc65db85539626e7`. Root/relocated oracle runs, optimized fail-closed behavior, silent imports, compile, modes, Markdown, diff, and scope gates pass; all 102 repository tests pass; fresh hostile re-review is clean. No prior stage reopens. T35 is now complete under D136; next: T36.

### 42-T35-PIECEWISE-INTEGER

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, D136 ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/42-T35-PIECEWISE-INTEGER.md`.

#### Big Picture Objective

Test predicate-selected arithmetic branches and exact integer closure.

#### Detailed Implementation Plan

Apply the common protocol. Reuse T34's `t+0D` unary scalar event and T43's closed-expression responsibility; represent strict programs as complete direct residue lookup with exact integer-closure validation and branch witnesses. Keep Conway ordered first-applicable fractions separately tagged, preserve their partial no-applicable boundary, and distinguish observer/analysis/compiler relations from native execution. Add no T35 state, UPDATE, executor, callback, hidden history, or branch-set successor.

#### Completion Requirements

All T35 evidence is captured; branching reuses explicit rule choice without hiding arithmetic; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 43-query source audit closes 104 lines at `70 pre-Index / 34 actual-Index`, retains 127 at `46 native / 63 relation / 18 control`, excludes seven, reverse-closes query evidence at `85 exact + 10 image-basename + 9 normalized` and retained evidence at `98 exact + 13 image-basename + 16 normalized`, and leaves zero unresolved. Twenty-six Index-only context targets have exact split owners plus frozen semantic-class, route, and guard records; all 26 referenced image files are path/size/SHA-bound. Thirteen governed assets at `5/5/3` plus 11 exclusions close the raster boundary. The semantic oracle closes 65,588 modulo checks, 6,150 direct/generic commutations, 24 arbitrary-precision profiles, 14,621 exact-program-bound event replays, ordered-fraction partiality, the 8,068-event Conway run, and 68 hostile rejections.

D136 keeps complete residue maps and separately tagged ordered fraction lists as closed unary RULE schemas over T34's discrete `t+0D` exact scalar event. Complete residue rows have no precedence; fraction order, duplicates, and shadowed rows remain structural identity; exact keys rather than digests govern replay; and missing selection uses the common zero-successor `Error(MissingBranch)` result with no event. No T35 state, frontier, neighborhood, UPDATE, outcome class, executor, family branch, callback, hidden history, digit packing, or native cycle halt is added; no prior stage reopens.

Oracle SHAs are source `af06b40b5e35fe97a97b58ad148336c7e9884029d2785a4186f4456e39de6108`, asset `c618c25202a496fc9f3cdac94fe748dbf2183c72932a72e10dd7b9dab249fb23`, and semantic `0c7f7c5875ad54edc504ddc5f9e88b240db8463622ff91080c9aa1dd42e332c1`; semantic digest is `7424aae85ed4dc8ee7d2a53d2d93aba32c4b951f8265c6b3a5b9f9846dfc8ba9`. Root/relocated/explicit-book runs, optimized and bad-usage rejection, silent imports, compile, modes, Markdown, diff, scope, 102 tests, and independent hostile mutation review pass. Next: T36.

### 43-T36-DIGIT-REVERSAL

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/43-T36-DIGIT-REVERSAL.md`; D137 is active.

#### Big Picture Objective

Test rules whose semantics explicitly depend on positional number representation.

#### Detailed Implementation Plan

Apply the common protocol. Reuse T34's exact discrete `t+0D` singleton event and extend the closed unary RULE algebra with typed positional encode/reverse/decode/add nodes. Strict source conformance is nonnegative integers in base 2: zero is the native fixed point `0 -> 0`, while every positive state is strictly increasing. Arbitrary bases and signed carriers are explicit extensions. Prove the canonical scalar/word commuting square, keep fixed width as program data, retain growing width in a transparent `(value,width)` product or lossless word, and close leading-zero/carry policies without callbacks or host-width behavior. Add no T36 state class, FRONTIER, NEIGHBORHOOD, UPDATE, executor, transform menu, or digit-CA fallback.

#### Completion Requirements

All T36 evidence is captured; semantic digit representation is distinguished from optional visualization; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. The 18-query source audit closes 125 rows at `99 pre-Index / 26 actual-Index`, retains 70 at `19 native / 19 relation / 32 control`, excludes 48, reverse-closes the complete retained/routed/guarded-Index crosswalk to 96 unique split owners at `71 exact / 16 image-basename / 4 normalized / 5 structural repair`, binds 34 Book-semantic guards plus four auxiliary guards, and leaves zero unresolved. Seven governed assets at `4/3/0` plus nine exclusions close 32 references, 16 hashes, 1,232,875 bytes, and five semantic manifests/41 exact records; all seven governed assets are hash-bound and none supplies pixel-derived semantics. The semantic oracle closes 1,180 source events and independent word replays, 22,036 scalar/word commutations, 1,881 fixed-reversal entries, five arbitrary-precision profiles, 260 horizons/8,320 event replays, an executable width-erasure counterexample, seven structural program keys, three cross-program rejections, and 68 hostile rejections.

D137 keeps strict T36 as T34's exact discrete `t+0D` nonnegative scalar event and extends D069 only with closed positional encode/reverse/decode/add nodes plus canonical/fixed/grow profiles. Zero is a continuing fixed-point event; canonical words commute losslessly; growing width remains visible because equal scalar projections can have different successors. No T36 state, frontier, neighborhood, assignment, UPDATE, executor, family branch, callback, machine-width behavior, hidden width/time, digit-CA fallback, raster rule, or observer-controlled evolution is added.

Oracle SHAs are source `7a4cf99382aab7a6a6867798a06f3f0ce5d07887fce3217d1e6a6ae0a5326733`, asset `972450eb675396bb352c2cac0bf4a7a4dc878c17b3f364e466ca2a0577bfd33a`, and semantic `cbbe63f4f4ad8f517df7532719c423e9ff796bbf3b1cfeae3e150540554e4791`; semantic digest is `30539868a2202ffdae0e4574e0ceefb68e5715d6d3a7a543efd63bd730a5ccc8`. Root/relocated/import/compile/optimized/bad-usage, mode, Markdown, diff, scope, 102-test, and independent hostile-review gates pass. No prior stage reopens. Next: T38.

### 44-T38-VARIABLE-RECURRENCE

Status: **COMPLETE — EVIDENCE, ASSETS, SEMANTICS, ARCHITECTURE, AND HOSTILE REVIEW CLOSED** in `goal-1/44-T38-VARIABLE-RECURRENCE.md`; D138 is active.

#### Big Picture Objective

Test data-dependent historical addresses and invalid-index semantics in growing recursive sequences.

#### Detailed Implementation Plan

Apply the common protocol. Reuse T37's complete `NumericPrefix`, unique `End` FRONTIER, complete explicit old-prefix NEIGHBORHOOD read, endpoint write, compact trace, and D072/T16 one-splice lowering. Extend only the closed RULE expression algebra with ordered nested `TermAt(AddressExpr)` reads over exact integer syntax. Preserve complete old-prefix state, leftmost-innermost demand occurrences, exact structural provenance, common no-commit errors, and observer separation. Add no T38 selector/access class, state, FRONTIER, NEIGHBORHOOD type, UPDATE, executor, callback, family branch, hidden memo state, or invalid-index policy menu.

#### Completion Requirements

All T38 evidence is captured; dynamic reads are direct and validated; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. Seventeen frozen query lanes close 102 unique source hits at `83 pre-Index / 19 actual-Index`; the pre query partition is `14 native / 13 relation / 24 control / 32 exclusion`, complete governed evidence is `20 / 36 / 44` plus 49 continuations, Index closes at `3 / 9 / 6 / 1`, and 124 unique split owners close at `98 exact / 15 image-basename / 11 normalized`. Twenty-five Book semantic guards, five auxiliary guards, seven source-defect records, 22 source-model records, and all 15 image dispositions are frozen with zero unresolved.

Four governed rasters at `3/1/0` plus eleven exclusions bind 30 references, 15 hashes, 653,438 bytes, and five semantic manifests/51 records. All four are hash-bound, two are additionally limited-transcribed, and none is pixel-replayed. The asset/semantic integration gate equates all eight formulas, seeds, horizons, and 340 visible values; the cropped lower page-144 plots remain explicitly unavailable.

The semantic oracle closes 325 displayed events/1,122 demands, 2,033 longer events/7,114 demands, 325 prefix/tag/splice commutations, 97 fixed-lag restrictions, 64 bounded-window loss counterexamples, 14 dependent-access cases with ten errors, 4,096 page-131 observer checks, 64 arbitrary-precision events up to 4,103 bits, ten compact lossless trace reconstructions, and 47 hostile rejections. A separate 2,533-case full-result gate proves that independently implemented merged closed-RULE evaluation and optional resolver-plus-emitter compilation are identical across visible, long, partial, fixed-lag, and bigint profiles. D138 reuses complete-prefix NEIGHBORHOOD access and adds only closed dependent lookup syntax/witnesses to RULE; UPDATE remains T37/T16. No prior stage reopens.

Oracle SHAs are source `df9cd5d4d52ce2e552d884c8ea12c932c3f9536c8cf35f4528fefe9f3768a410`, asset `95a45d1d079309a0b56fff8411be3cae66aaf31fdd38d49411a62c50f5b887e2`, and semantic `29795148a77eb0b26cb679b482879659d5ec4355268954285bcd0419c2db1249`; semantic digest is `416670f63d52cdb84982dfc4f135c4fa51e3d64a8c9a6579b0d1533c8d693b06`. Root/relocated/import/compile/optimized/bad-usage, cross-interface, mutation, mode, Markdown, diff, scope, 102-test, and independent hostile-review gates pass. Next: T40.

### 45-T40-CONSTANT-DIGITS

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, ARCHITECTURE, AND HOSTILE-REVIEW CLOSED UNDER D139** in `goal-1/45-T40-CONSTANT-DIGITS.md`.

#### Big Picture Objective

Test exact constants as sources for indexed digit and continued-fraction sequences without inventing mutable dynamics.

#### Detailed Implementation Plan

Apply the common protocol, emphasizing immutable exact denotation, pure representation query/result, base and canonicalization, coefficient exactness, evaluator realizations, and term limits. Do not fabricate a mutable constant or mandatory prefix evolution: explicit long-division, square-root, positional-residual, and continued-fraction procedures are separately identified work SimplePrograms over existing axes.

#### Completion Requirements

All T40 evidence is captured; source definition and generated observable remain distinct; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. Twenty discovery lanes close a 213-row union, while an independent Book-wide lane closes 309 direct matches at `242 pre-Index / 67 Index`; the pre-Index rows split into 110 retained and 132 line-hash-bound sibling exclusions. Total retained evidence is 447 at `169 native / 238 relation / 40 control`. Independent fixed universes route all 117 strict-main rows, all 126 native-Notes rows, and the complete 897-row actual Index at `30 / 102 / 4 / 16 / 745`; the split crosswalk closes 1,359 rows with zero unresolved.

Fifty-three governed rasters at `11 native / 40 relation / 2 control` plus ten exclusions bind 124 references, 63 unique hashes, and 2,167,477 bytes. All 63 are hash-bound; none is pixel-transcribed or replayed. The semantic oracle closes exact positional and simple-continued-fraction canonicalization, certified pi coefficients, exact surd/`e` families, optional work commutations, finite-prefix loss, 159 exact plus 36 certified random-access agreements, the complete result/outcome/termination taxonomy, three replay-verified T42 handoffs, and 72 hostile rejections.

D139 reuses D082/T41 declarative definitions and T34/T36/T43 work/value responsibilities through classes 1–3. The umbrella T40 query layer has no native transition DOMAIN; explicit coefficient algorithms are ordinary discrete `t+0D` work SimplePrograms. Source audit digest is `5eeb98409dc44e07284e142355054d9dde66e7566fde4c9f36e35c0642840623`; source/asset/semantic SHAs are `9209966474b1da250949cf74dbd2d4f844fb4b87f994be0806d4b8b79c87859c`, `7eb5afb0f072557603d1ce7a08aa9f1a6b4c872e51d8b7d7cbf66b056388cced`, and `a3b8b01d32db2a5198c564ee453beb23a1e3acd1f23b7e639bd9ec30b2671cc7`; semantic digest is `f5bd58e930032f69aae6fd2a613a267d9ca8a3c9742e41de1d193cdcdfe97716`. All oracle/interface, relocation, governed/excluded mutation, fail-closed, Markdown, diff, scope, independent hostile-review, and 119-test gates pass. Next: T42.

### 46-T42-CF-SUBSTITUTION

Status: **COMPLETE — SOURCE, ASSET, SEMANTIC, RUNTIME-FIT, D140 ARCHITECTURE, AND INDEPENDENT HOSTILE REVIEW CLOSED** in `goal-1/46-T42-CF-SUBSTITUTION.md`.

#### Big Picture Objective

Reconstruct T42 as a finite visibly scheduled binary-substitution preset whose immutable execution-order schedule comes from a complete replay-verified T40 result or a separately tagged explicit schedule.

#### Detailed Implementation Plan

Normalize natural simple-CF coefficients by retaining signed `a0` as provenance/observer data, dropping it from execution, and reversing the positive tail exactly once. Use the canonical nonempty uniform `PhaseIndex[0..L] x Bit` word, generic `phase<L` applicability restriction, T13 all-occurrence/self-read/nonempty emissions, D019 ordered old-generation concatenation, and the common terminal envelope. Keep the strict `(0,)` seed in preset/run configuration; preserve full source result, schedule horizon/orientation, lineage, and terminal word. Keep compact/tagged encodings, quadratic macros, mechanical words, plots, digital slopes, crossings, and billiards in their correct interface/relation roles. Add no T42 axis, state class, UPDATE, executor, callback, or family branch.

#### Completion Requirements

All T42 evidence is captured; rule scheduling is explicit state or input rather than hidden control; Goal 2 and global integration are updated.

#### Stage Result

COMPLETE. Fourteen search lanes close a 48-row union, the independent Book-wide lane closes 39 candidates, and 54 retained rows partition as `10 native / 21 relation / 23 control`; fixed closure covers the five-row strict main, five-row executable Notes, all 897 Index rows, and 951 split rows with zero unresolved. Twelve governed rasters at `1/11/0` bind 24 references, twelve hashes, and 285,055 bytes; all are hash-bound, page 162 is additionally limited-transcribed, and none is pixel-replayed.

The semantic oracle closes three full replay-verified T40 handoffs, the `m-1` source defect, 630 live and 390 completion cases over thirteen programs, 630 exact canonical product-T13 commutations/5,145 children, exact terminal retention across six views, four page-162 fixtures/25 events/301 firings/599 children, coefficient/rational/horizon/macro boundaries, and 98 hostile rejections. Terminal carriers retain and replay the full program and reject live-phase exhaustion. D140 classifies T42 as classes 1–3 T13/D019/D024 reuse with a closed schedule constructor and provenance validation only.

Source audit digest is `2726957389d256722469424e41ea2e92188ba5e30d7ab52c4df2598dd7250aa6`; source/asset/semantic SHAs are `27dfafe8798ce65af8d282440c85f02ae7d8d591f0fec30350ad52e41a25270d`, `a13a0fb85bae143a2ec53f2e4f77458777c980739e13ed522e85d3a42f21d4c6`, and `f283f02069b6a2cc46d49d3d4f34c61532bb5684167cf69db9562f1ba273bae5`; semantic digest is `c7e02485cb444cfeff14680d214a164f48e2f9bdf12e8021f5f28205ca9a789d`. All oracle/interface, relocation, mutation, fail-closed, architecture, and independent hostile-review gates pass. No runtime code changed and no prior stage reopened. Next: synthesis.

### 47-SYNTHESIS

Status: **COMPLETE** in `goal-1/47-SYNTHESIS.md` under D141.

#### Big Picture Objective

Re-derive the complete architecture from all 45 evidence records and determine the smallest genuine construction algebra or set of algebras.

#### Detailed Implementation Plan

- Audit every proposed primitive against all type stages and merge only semantically identical concepts.
- Re-test the candidate executor boundaries, state model, result types, update semantics, family index, and trace/encoding boundary.
- Identify contradictions, reopen affected stages, and remove abstractions supported only by convenience.
- Produce a cohesive proposed revision strategy for `simple_programs.md` and `src/ca` without implementing it.

#### Completion Requirements

- All 45 stages are complete and internally consistent.
- Every primitive has evidence-backed users and explicit invariants.
- Irreducible execution algebras are named and justified; apparent unity is not purchased through callbacks or `Any`.
- No unresolved contradiction remains in `0-plan.md` or `design-ledger.md`.

#### Stage Result

COMPLETE. D141 reduces every catalog construction with canonical evolution to one branch-free `FRONTIER.select -> NEIGHBORHOOD.read -> RULE.apply -> UPDATE.apply` algebra with closed typed axis values and a uniform `StepResult`. T31-T33, T40-T41, and T45 use one sibling immutable definition/relation/query/certificate algebra where the catalog object supplies no canonical next state; separately evidenced work evolutions still use the common runner. The architecture matrix contains T01-T45 exactly once, preserves seed/run identity separately from transition identity, and records the honest stochastic, continuous-time, adaptive-subdivision, sequential-network, and exact-real boundaries. Independent hostile review and all final global gates pass.

### 48-GOAL2-HANDOFF

Status: **COMPLETE** in `goal-1/goal-2-handoff.md`.

#### Big Picture Objective

Turn the evidence-grounded architecture into a complete, dependency-aware Goal 2 implementation plan.

#### Detailed Implementation Plan

- Consolidate each type's Goal 2 handoff into `goal-1/goal-2-handoff.md`.
- Order shared semantic primitives before the type conformance stages that depend on them.
- Preserve a distinct traceable implementation/conformance obligation for every CSV row without duplicating shared implementation.
- Define migrations, canonical examples, tests, coverage matrix, no-cheating checks, and final ANKoS universality verification.
- Specify how a later `goal-2` scaffold should be generated, but do not implement Goal 2 in this goal.

#### Completion Requirements

- Every type appears exactly once as a Goal 2 coverage obligation.
- Every implementation stage has dependencies, files, tests, completion evidence, and rollback/re-derivation triggers.
- Shared work is planned once; no family-specific rollout or second semantic/execution compatibility path is proposed.
- The handoff is sufficient to scaffold and execute Goal 2 without repeating Goal 1 research.

#### Stage Result

COMPLETE. G2-00 through G2-12 form an acyclic in-place migration plan with explicit files, dependencies, tests, completion criteria, and re-derivation triggers. The exact CSV coverage matrix maps all 45 catalog names once; the normative `Cnn = Tnn` matrix supplies 45 direct leaf-dependency records and every authority file exists. The plan implements shared substrates once, keeps the new runner private until one atomic public cutover, permits only a lossless executor-free construction façade, and authorizes neither family rollout nor a second semantic execution path. The future Goal 2 implementation gates remain deliberately open.
