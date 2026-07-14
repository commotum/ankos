› I don't think that's true:   My only disagreement is with this phrase:

    > Frontier describes those areas that may change.

    I would instead say:

    > Frontier describes the components to which the rule is applied this step.

    Those are not always the same set.

    For a mobile automaton:

    - Frontier: the single active cell.
    - Neighborhood: its readable [left, self, right] view.
    - Rule result: writes to the source and to the selected destination.
    - Update: commits both writes atomically.

    The destination may change without itself being a frontier member. Conversely, a frontier member can fire but remain
    unchanged.

  For example, in that case, the frontier is BOTH the SOURCE AND THE DESTINATION. In fact, it's the source and all possible
  destinations. These are differentiated by the values their position holds, ie one is active, the other is not, that is
  determined by the alphabet. Then the RULE takes everything into consideration, looks at the FRONTIER (which is any
  position/cell that may change) all the inactive cells result in no evaluation, and then the active cell gets run through
  the rule, and the rule determines the output to all of the cells. Right?


• Yes—you’re right. I was conflating the rule-firing subset with the frontier itself.

  Under your model, for a mobile automaton with active position a:

  FRONTIER = {a - 1, a, a + 1}

  That is the complete region that could change during the next step:

  - a is the source.
  - a - 1 and a + 1 are the possible destinations.
  - The alphabet identifies which member contains Active(bit).
  - The rule is applicable only at that active member.
  - Its result supplies a coupled update for the frontier.
  - The unselected destination retains its old value.

  Formally:

  frontier = PossibleWrites(
      around=FindValue(Active),
      offsets=(-1, 0, +1),
  )

  for locus in frontier:
      proposal = rule.apply(
          locus=locus,
          value=configuration[locus],
          neighborhood=neighborhood.read(configuration, locus),
      )

      # Plain(...) produces no proposal.
      # Active(...) produces the coupled source/destination update.

  Or more directly, the rule can operate once on the frontier as a structured patch:

  proposal = rule.apply(configuration.view(frontier))
  result = update.commit(configuration, proposal)

  For direction +1, it might return:

  Patch(
      write(a,     Plain(new_bit)),
      write(a + 1, Active(old_right_bit)),
      preserve(a - 1),
  )

  So the concepts are:

  - Frontier: every existing or potential locus that this step is permitted to change.
  - Alphabet: includes semantic roles such as Plain and Active.
  - Neighborhood: everything readable when deciding the frontier’s next contents.
  - Rule: determines applicability and returns the coupled frontier update.
  - Update: commits all returned changes atomically and resolves any conflicts.

  That is cleaner because it avoids inventing a separate source-selection axis. “Which cell causes the change?” is already
  represented transparently by the active tag in the configuration.

  The corresponding generic step can remain:

  def step(program, configuration):
      frontier = program.frontier(configuration)
      proposals = []

      for component in frontier:
          view = program.neighborhood.read(configuration, component)
          proposal = program.rule.evaluate(component, view)

          if proposal is not None:
              proposals.append(proposal)

      return program.update.commit(configuration, proposals)

  The only necessary generalizations are:

  - A rule may return a multi-locus patch, not merely one next value.
  - A frontier may contain potential destinations, including dynamically created loci.
  - Rule applicability may depend on the value at a frontier component.
  - UPDATE must define atomicity and collision behavior when multiple frontier components propose overlapping writes.

  For multiple mobile heads, for example:

  FRONTIER = dilation(active_positions, allowed_write_offsets)

  Each active-tagged component proposes its patch; inactive members propose nothing; UPDATE handles overlapping proposals.

  So yes: the mobile automaton does not force frontier to mean “rule-firing loci.” It demonstrates that the frontier can
  remain the possible-write region, while activity and applicability live visibly in the alphabet and rule. The plan’s
  conclusion that T09 “rederives” frontier as firing loci is therefore not uniquely necessary; your interpretation is a
  coherent—and arguably simpler—countermodel.


› Is it just arguably simpler? Or is it actually more elegant?


• Given the architecture you’re aiming for, I think it is actually more elegant, not merely arguably simpler.

  It gives every component one clean responsibility:

  - Alphabet: what information and roles exist at each position.
  - Frontier: where this step is permitted to make changes.
  - Neighborhood: what information may be read.
  - Rule: how readable state maps to proposed changes.
  - Update: how simultaneous proposals compose and commit.

  That is a very crisp read/write separation:

  NEIGHBORHOOD = read capability
  FRONTIER     = write capability
  RULE         = transformation
  UPDATE       = transaction semantics

  My source-oriented interpretation introduced another concept—“firing loci”—that is often already encoded in the state. For
  a mobile automaton, Active(bit) tells us exactly which component drives the rule. Adding a separate active-source selector
  duplicates that fact in the orchestration layer.

  Your formulation keeps control where it belongs: visibly in the configuration.

  Configuration:
      Plain(0), Plain(1), Active(0), Active(1)

  Frontier:
      source and every possible destination

  Rule:
      Plain(...)  → no proposal
      Active(...) → coupled source/destination proposal

  That generalizes naturally:

  - A Turing head is an alphabet role.
  - An instruction marker is an alphabet role.
  - An end marker in a growing sequence is an alphabet role.
  - A pending query or unresolved solver obligation can be a configuration role.
  - A matched interval can be a structured frontier component.

  The runtime doesn’t need to understand any of those roles. It merely evaluates the rule over the writable frontier.

  ### The precise contract

  I’d define frontier as:

  > The complete, possibly intensional region containing every locus that a step is authorized to create, remove, replace, or
  > relabel.

  It is a possible-write envelope, not the exact changed set. Therefore:

  actual_write_targets ⊆ frontier

  The runtime validates that invariant.

  For the mobile automaton:

  frontier(configuration) = {
      active_position - 1,
      active_position,
      active_position + 1,
  }

  The rule may write only two members, but all three must be present because either neighbor could be selected.

  ### Why this is stronger

  It enables useful validation before committing anything:

  for effect in proposals:
      require(effect.target in frontier)

  That means the rule is not an unrestricted mutation callback. Even if it computes destinations dynamically, its effects
  remain confined to a declared capability.

  The frontier can also be represented intensionally:

  RelativeRegion(anchor=Tagged("Active"), offsets=Range(-1, +1))
  NamedRegion(instruction.operands | {program_counter})
  MatchedIntervals(program.clauses)
  FreshChildrenOf(old_graph_nodes)

  It need not always materialize as a flat list of existing coordinates. This handles dynamic support, insertions, graph
  births, and remote named registers without weakening the abstraction.

  ### The resulting core API

  class SimpleProgram:
      configuration: ConfigurationSchema
      alphabet: Alphabet
      frontier: WritableRegion
      neighborhood: ReadableRegion
      rule: Rule
      update: UpdatePolicy

  And the generic runner remains straightforward:

  def step(program, state):
      frontier = program.frontier.resolve(state)
      proposals = []

      for component in frontier.components(state):
          view = program.neighborhood.read(state, component)
          proposals.extend(
              program.rule.evaluate(
                  component=component,
                  value=state.value_at(component),
                  view=view,
              )
          )

      frontier.validate(proposals)
      return program.update.commit(state, proposals)

  An implementation may optimize this by indexing only values for which the rule is applicable—such as Active—but that is an
  execution optimization, not a separate semantic axis.

  So yes: frontier as writable capability is the more elegant abstraction. It is more orthogonal, preserves visible state,
  avoids duplicating activation semantics, supports static validation, and retains the original intuitive relationship:

  Frontier says where writes may go.
  Neighborhood says where reads may come from.
  Rule connects the two.
  Update makes the connection atomic.


› Even that I think is too much overkill. We're probably fine with:

      class SimpleProgram:
          seed: Seed
          alphabet: Alphabet
          frontier: WritableRegion
          neighborhood: ReadableRegion
          rule: Rule

  Now maybe that's not ultra clear yet, but there is no extra "UpdatePolicy." The update policy is the rule. The only part
  might budge on is if the seed is not just the initial state, but a generator for initial states, either constructively or
  through random bernoulli sampling or something. Right?


• Yes. I was over-factoring implementation mechanics into the public ontology.

  This is probably the right top-level API:

  class SimpleProgram:
      seed: Seed
      alphabet: Alphabet
      frontier: WritableRegion
      neighborhood: ReadableRegion
      rule: Rule

  There is no configurable update policy because SimpleProgram has one universal step convention:

  1. Start from the old configuration.
  2. Resolve its writable frontier.
  3. Read the neighborhood from the old configuration.
  4. Apply the rule.
  5. Atomically replace the frontier with the rule’s result.
  6. Preserve everything outside the frontier.

  Conceptually:

  def step(program, old):
      writable = program.frontier.resolve(old)
      readable = program.neighborhood.read(old, writable)
      replacement = program.rule.apply(
          old=old,
          frontier=writable,
          neighborhood=readable,
      )
      return old.replace(writable, replacement)

  Variable-length substitution, graph changes, and multiway behavior don’t require an UpdatePolicy; they require
  appropriately typed frontiers and rule results:

  word frontier  → replacement word
  graph frontier → replacement subgraph
  field frontier → replacement field values
  multiway rule  → zero, one, or several possible replacements

  Atomic snapshot replacement is simply what “applying a rule” means.

  The rule can have internal structured forms—lookup tables, arithmetic expressions, substitutions, graph transformations—but
  those are variants of Rule, not additional top-level axes.

  On Seed: yes, it should probably mean an initial-configuration source, not necessarily one already-materialized state.

  Seed =
      ExactConfiguration(...)
      | Constructive(...)
      | RandomLaw(...)

  Examples:

  ExactConfiguration({...})

  Constructive(
      SingleActiveCell(position=0, background=Plain(0))
  )

  RandomLaw(
      Bernoulli(p=0.5)
  )

  There is one important distinction around randomness:

  Bernoulli(p=0.5)

  denotes a distribution over initial configurations, whereas:

  Bernoulli(p=0.5, key=1234)

  denotes a reproducible realization procedure. An actual run may therefore look like:

  trajectory = run(
      program,
      random_key=1234,
      realization=FiniteWindow(-500, 500),
  )

  An exact or deterministic constructive seed would not need random_key.

  So Seed owns:

  - Native support or board construction.
  - Initial values.
  - Deterministic construction, if any.
  - A probability law, if stochastic.

  The run request owns:

  - A particular random key.
  - Finite realization bounds when the native seed is infinite or intensional.
  - The requested trajectory horizon.

  That leaves a remarkably compact semantic core:

  SEED          initial configuration(s)
  ALPHABET      possible values and roles
  FRONTIER      possible writes
  NEIGHBORHOOD  permitted reads
  RULE          next contents of the frontier

  Everything else—atomicity, simultaneous old-state reads, and preservation outside the frontier—can be fixed semantics of
  SimpleProgram, not additional user-facing objects.

› Does this align with simple_programs.md spec? And what about the various types as outlined in goal-1 folder? I think it's
  getting thrown off by the fact that in the book (A New Kind of Science), Wolfram uses different semantic classes to
  describe different constructions of the same underlying objects. For example, can you verify that the mobile automata and
  turing machines both fit under this minimal API?


• I’ll verify this against the actual simple_programs.md contract and the completed Goal 1 evidence, with special attention
  to T09 mobile automata and T12 Turing machines. I’ll separate “fits the five-field public API” from “requires hidden
  semantics,” because that is the decisive test.

• Started `/root/simple_spec`

• Started `/root/mobile_verify`

• Started `/root/turing_verify`

• Explored
  └ List goal-1
    Search ^Status: in *.md
    Read 0-plan.md

• Ran wc -l simple_programs.md goal-1/design-ledger.md goal-1/architecture-audit.md goal-1/3-T09-MOBILE.md
  │ goal-1/4-T12-TURING.md goal-1/29-T11-GENERALIZED-MOBILE.md
  └   2199 simple_programs.md
      1103 goal-1/design-ledger.md
    … +3 lines (ctrl + t to view transcript)
       633 goal-1/29-T11-GENERALIZED-MOBILE.md
      5289 total

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• The folder has advanced beyond the earlier snapshot: 33 type stages are now complete, T23 is in progress, and 11 remain.
  I’m using the current files, not the earlier 27/18 count, and I’m checking whether the five fields are sufficient as public
  semantics—not merely whether each type can be encoded by hiding machinery inside Rule.

• Explored
  └ Read architecture-audit.md
    Search ^#{1,4}  in simple_programs.md
    Read simple_programs.md
    Search ^#{1,4}  in 3-T09-MOBILE.md
    Read 3-T09-MOBILE.md, 4-T12-TURING.md
    Search ^## Construction in ^### .*transition

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Yes—with one precise adjustment. Your five-field API matches the core semantics of simple_programs.md better than the
  current Goal 1 architecture does.

  simple_programs.md already defines:

  - FRONTIER as writable next-state coordinates.
  - NEIGHBORHOOD as readable current-state coordinates.
  - RULE as the next value for frontier coordinates.
  - One fixed execution law: old-snapshot reads, parallel replacement, and copy-through outside the frontier.

  It has no configurable UpdatePolicy. (simple_programs.md:1412, simple_programs.md:1767)

  ## One necessary adjustment

  The current document also has separate DOMAIN, SHAPE, and BOUNDARY fields. Your minimal API can eliminate those only if
  Seed becomes a source of complete configurations:

  class Seed[Configuration]:
      # Produces configurations carrying their own
      # support, topology, extent/defaults, and invariants.
      ...

  Then:

  class SimpleProgram:
      seed: Seed
      alphabet: Alphabet
      frontier: WritableRegion
      neighborhood: ReadableRegion
      rule: Rule

  is sufficient.

  The existing SEED already includes a probability distribution over initial assignments, so Bernoulli sampling is explicitly
  aligned with the spec. However, the current document allocates the domain before applying the seed; that responsibility
  would need to move into the generated configuration. (simple_programs.md:235, simple_programs.md:2156)

  I’d express the fixed semantics as:

  X₀ ~ SEED

  Fₜ = FRONTIER(Xₜ)
  Nₜ = NEIGHBORHOOD(Xₜ, Fₜ)
  Yₜ ∈ RULE(Xₜ restricted to Fₜ, Nₜ)

  Xₜ₊₁ = Xₜ with Fₜ atomically replaced by Yₜ

  Everything outside Fₜ is preserved. Yₜ may be one replacement or several alternative replacements for a multiway rule.

  ## Mobile automata fit exactly

  Let the configuration alphabet be:

  Cell = Plain(Bit) | Active(Bit)
  invariant: exactly one Active

  If the active cell is at h:

  FRONTIER = {h-1, h, h+1}
  NEIGHBORHOOD = old values at {h-1, h, h+1}

  The native mobile rule is:

  μ : Bit³ → Bit × {-1,+1}
  μ(L,C,R) = (new_bit, direction)

  Its complete frontier replacement is:

  direction = -1:
      [Active(L), Plain(new_bit), Plain(R)]

  direction = +1:
      [Plain(L), Plain(new_bit), Active(R)]

  Everything outside those three positions is unchanged.

  That precisely preserves Wolfram’s native {list, active_position} step. The apparent discrepancy comes from representation:

  - In {list,n}, the rule changes list[n] and separately changes n.
  - In the tagged field, changing n necessarily changes the labels at both the source and destination.

  The stage already proves the representations are bijective and commute one step at a time. (goal-1/3-T09-MOBILE.md:259,
  goal-1/3-T09-MOBILE.md:347)

  So the book’s statement that “only the active cell is updated” describes its factored representation. It does not imply
  that the losslessly equivalent tagged board has only one writable position.

  The extended mobile automaton T10 is even more direct: its native rule already returns a replacement three-cell block plus
  a movement direction.

  ## Turing machines fit the same way

  Use:

  Cell = Plain(TapeSymbol) | Head(HeadState, TapeSymbol)
  invariant: exactly one Head

  Suppose:

  X[h] = Head(q, a)
  δ(q, a) = (q′, b, d)
  d ∈ {-1,+1}

  Then:

  FRONTIER = {h-1, h, h+1}
  NEIGHBORHOOD = old labels at {h-1, h, h+1}

  And the rule’s frontier replacement is:

  X′[h]   = Plain(b)
  X′[h+d] = Head(q′, underlying_symbol(X[h+d]))
  X′[h-d] = X[h-d]

  Everything outside the frontier is preserved.

  The neighboring symbols do not affect the native Turing decision: δ still reads only (q,a). The destination symbol is
  inspected only so that moving the head preserves the symbol already underneath it.

  Again, the Goal 1 stage proves this tagged representation is bijective with Wolfram’s {head_state,tape,head_position}
  representation and commutes exactly one step at a time. (goal-1/4-T12-TURING.md:264, goal-1/4-T12-TURING.md:344)

  So both constructions share the same five-field form:

   Field           Mobile automaton                                    Turing machine
  ━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   seed            Bit field plus one active position                  Total/default tape plus one head position/state
  ──────────────  ──────────────────────────────────────────────────  ───────────────────────────────────────────────────────
   alphabet        Plain(bit) | Active(bit)                            Plain(symbol) | Head(q,symbol)
  ──────────────  ──────────────────────────────────────────────────  ───────────────────────────────────────────────────────
   frontier        Source plus both possible destinations              Source plus both possible destinations
  ──────────────  ──────────────────────────────────────────────────  ───────────────────────────────────────────────────────
   neighborhood    Source’s left/self/right values                     Head data plus possible destination labels
  ──────────────  ──────────────────────────────────────────────────  ───────────────────────────────────────────────────────
   rule            New bit, movement, complete frontier replacement    New state, symbol, movement, complete frontier
                                                                       replacement

  No extra update axis is semantically required.

  ## How this bears on the other Goal 1 types

  The 33 completed stages do not currently provide a counterexample to the minimal API. Their supposed update-policy
  differences can generally be understood as different Rule result shapes:

   Goal 1 constructions                    Frontier/replacement interpretation
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Fixed CA, totalistic CA, scalar maps    Replace selected values
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Mobile/Turing/register machines         Replace a tagged writable region
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Parallel substitution                   Replace the old word/occurrences with emitted words
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Sequential substitution                 Replace the selected matched interval
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Tag/cyclic-tag systems                  Replace prefix and tail-related structural region
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Symbolic rewriting                      Replace selected subtrees
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Recursive sequences                     Replace the end marker with value plus new end marker
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Geometric systems                       Replace parent occurrences with child occurrences
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Networks                                Replace affected graph structure
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Multiway rewriting                      Return several alternative frontier replacements
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Initial-condition types                 Different Seed constructors or probability laws
  ──────────────────────────────────────  ───────────────────────────────────────────────────────
   Quiescence/symmetry                     Restrictions or properties of Rule, not new programs

  The Rule must therefore be allowed to return a typed structural replacement—not merely one scalar. But that is still one
  Rule field, not a separate update dimension.

  The hardest current entries are constraints, uniterated functions, and general PDE relations. Goal 1 calls them nonfits
  because they do not independently specify a canonical next step. That does not prove they require another runtime ontology.
  It means they are incomplete SimpleProgram specifications until one supplies:

  - a seed or candidate generator,
  - a writable frontier,
  - readable information,
  - and a rule describing evaluation, refinement, iteration, or solution generation.

  For example, f(x)=x² by itself does not say whether to sample f, iterate it, or solve f(x)=0. Those become different
  SimplePrograms by supplying different seed/frontier/neighborhood wiring around the same underlying rule object.

  That supports your diagnosis: Goal 1 appears to be treating Wolfram’s different descriptions and application conventions as
  evidence for different semantic machinery. Some distinctions are real—branching, variable support, graph identity—but they
  can live in the types of Seed, WritableRegion, ReadableRegion, and Rule rather than becoming top-level execution axes.

  The current Goal 1 conclusion that FRONTIER means firing sources and UPDATE must be a separate axis is therefore not forced
  by the evidence. It is one factorization. Your writable-frontier interpretation:

  SEED → configuration
  FRONTIER → possible writes
  NEIGHBORHOOD → permitted reads
  RULE → complete next frontier

  is consistent with simple_programs.md, gives exact mobile/Turing semantics, and looks like the cleaner architecture to test
  against the remaining 11 types.

─ Worked for 5m 14s ─────────────────────────────────────────────────────────────────────────────────────────────────────────


› Tell me more about constraints, uniterated functions, and general PDE relations?


• I’ll unpack the three cases from their completed Goal 1 stages, then distinguish two questions: whether the mathematical
  object itself defines a trajectory, and whether it can participate in your five-field generator once an evaluation or
  construction procedure is supplied.

• Started `/root/constraints_deep`

• Started `/root/functions_deep`

• Started `/root/pde_deep`

• Explored
  └ Search ^#{1,4}  in 13-T31-CONSTRAINTS.md
    Read 13-T31-CONSTRAINTS.md, 17-T41-FUNCTIONS.md, 20-T45-PDE.md

• Waiting for agents

• Finished waiting
  └ No agents completed yet

• Waiting for agents

• Finished waiting
  └ No agents completed yet

• Waiting for agents

• Finished waiting
  └ No agents completed yet

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• The core distinction is emerging clearly: all three can be inputs to a process with a trajectory, but the bare object often
  specifies a relation or denotation rather than a successor. The important architectural question is whether SimpleProgram
  represents the bare mathematical object or an executable use of it.

• Waiting for agents

• Finished waiting
  └ No agents completed yet

─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• These three expose one real design question, but it is not whether you need an UpdatePolicy.

  The question is:

  > Is Rule necessarily a temporal function producing one next state, or can it be a closed relation describing the allowed
  > contents of the frontier?

  If Rule is relational, the minimal API can encompass all three.

  A useful general signature is:

  RULE:
      readable neighborhood
          → allowed replacement(s) of writable frontier

  Or mathematically:

  Rule : NeighborhoodState → Set[FrontierState]

  Then:

  - Deterministic evolution returns one replacement.
  - Multiway evolution returns several replacements.
  - An impossible/terminal case returns none.
  - A stochastic rule returns a probability measure over replacements.
  - A constraint returns every replacement satisfying a relation.
  - A function returns the output corresponding to its input.
  - A PDE returns fields satisfying its differential relation.

  The distinction is no longer “different execution classes.” It is how the rule’s inputs and outputs are wired and whether
  the result is fed back.

  ## Constraints

  A T31 constraint is finite data defining a set of allowed complete configurations:

  Constraint:
      alphabet
      neighborhood footprint
      allowed neighbor histograms for each center value

  Its denotation is:

  Models(C) = {
      X : Zᵈ → Alphabet
      | every location satisfies C’s local relation
  }

  For example, the 1D condition “every cell has one black and one white neighbor” permits precisely translations of:

  ...001100110011...

  Nothing says that one such configuration evolves into another. Nothing says which cell should be filled first or repaired.
  The book explicitly says constraints describe allowed complete configurations, provide no direct construction procedure,
  and have no initial conditions. (goal-1/13-T31-CONSTRAINTS.md:223, goal-1/13-T31-CONSTRAINTS.md:83)

  Under a strictly temporal interpretation, it lacks:

  - An initial state.
  - A writable frontier.
  - A repair order.
  - A successor configuration.

  But under a relational interpretation, it can fit:

  SimpleProgram(
      seed=BoundaryDataOrCandidateGenerator(...),
      alphabet=Binary,
      frontier=UnknownRegion(...),
      neighborhood=Offsets(-1, +1),
      rule=AllowedLocalConfigurations(...),
  )

  Here Rule does not say “change this cell.” It says:

  > These are the frontier assignments globally compatible with the readable assignments and the constraint.

  There may be zero, one, or many replacements.

  The major caveat is that this must be a joint relation over the frontier. Independently selecting a locally permitted value
  at each cell does not necessarily produce a globally consistent configuration.

  A concrete solver is then a separate SimpleProgram operating on the constraint:

  seed          = partial assignment
  frontier      = unresolved variables
  neighborhood  = related assignments and constraints
  rule          = branch, propagate, or backtrack

  Different solvers have different trajectories but share the same underlying constraint rule. That supports keeping the
  constraint as reusable rule data rather than inventing a separate execution ontology.

  ## Uniterated functions

  An uniterated function is:

  f : X → Y

  It says how to obtain an output from an argument, but it does not say to feed the output back into the input.

  For f(x)=x², these are different constructions:

  ### One evaluation

  Input(x) → Output(x²)

  SimpleProgram(
      seed=Arguments(...),
      alphabet=InputOrOutputValue,
      frontier=OutputSlots(),
      neighborhood=InputSlots(),
      rule=Square(),
  )

  Each argument produces a one-step trajectory:

  Input(3) → Output(9)

  ### Iteration

  xₜ₊₁ = xₜ²

  SimpleProgram(
      seed=ExactValue(3),
      alphabet=Number,
      frontier=CurrentValue(),
      neighborhood=CurrentValue(),
      rule=Square(),
  )

  Now the trajectory is:

  3 → 9 → 81 → 6561 → ...

  The mathematical expression Square() is identical. What changes is the wiring:

  - Does the output occupy a separate result slot?
  - Or does it replace the value that will be read on the next step?

  This is perhaps the clearest confirmation of your diagnosis. T41 “mathematical functions” and T43 “iterated maps” need not
  be different rule classes. They are different uses of the same underlying rule.

  The T41 stage calls functions nonfits because the bare definition supplies no argument, feedback convention, sampling mesh,
  root-finding algorithm, or stopping condition. (goal-1/17-T41-FUNCTIONS.md:296, goal-1/17-T41-FUNCTIONS.md:345)

  That means the function alone is not a complete SimpleProgram. It can still be the Rule inside many SimplePrograms:

  - Point evaluation.
  - Sampling.
  - Iteration.
  - Root isolation.
  - Crossing detection.
  - Optimization.

  Those programs have different seeds, frontiers, and neighborhoods around the same function.

  ## PDE relations

  A general PDE such as:

  uₓₓ + uᵧᵧ = 0

  is closer to a constraint than to an evolution rule. It describes which complete functions u(x,y) are permitted.

  It does not specify:

  - Which variable is time.
  - What an instantaneous state contains.
  - Which direction evolution proceeds.
  - Initial data.
  - Boundary data.
  - Whether a solution exists.
  - Whether it is unique.

  So a boundary-value problem can be represented relationally:

  SimpleProgram(
      seed=BoundaryData(...),
      alphabet=Real,
      frontier=InteriorField(region),
      neighborhood=DifferentialGerm(...),
      rule=Satisfies(Laplacian(u) == 0),
  )

  The rule returns the set of interior fields compatible with the boundary values and equation. That set can contain zero,
  one, or many fields.

  A PDE becomes genuinely evolutionary when a time variable and sufficient Cauchy data are supplied.

  For diffusion:

  uₜ = ¼uₓₓ
  seed: u(0,x)

  For the wave equation:

  uₜₜ = uₓₓ
  seed: u(0,x), uₜ(0,x)

  These can become continuous-time SimplePrograms:

  SimpleProgram(
      seed=CauchyData(...),
      alphabet=FieldValue,
      frontier=WholeSpatialSlice(),
      neighborhood=DifferentialGerm(order=2),
      rule=ContinuousEvolution(...),
  )

  The PDE stage explicitly says that a suitably posed and justified initial-value problem can derive a continuous flow.
  (goal-1/20-T45-PDE.md:724)

  The numerical version is another derived SimpleProgram:

  seed          = sampled initial field
  frontier      = next grid slice
  neighborhood  = finite stencil
  rule          = finite-difference/integrator formula

  But that grid program is not identical to the PDE. Mesh spacing, stencil, boundary lowering, time integrator, precision,
  and tolerances are added semantics. (goal-1/20-T45-PDE.md:753)

  ## The common structure

  These three can all be viewed as relations:

  Constraint:  C(X)                    allowed configurations
  Function:    y = f(x)                allowed input/output pairs
  PDE:         P[u] = 0                allowed fields
  Transition:  X′ = F(X)               allowed current/next pairs

  A transition is simply a relation with a privileged input/output orientation and an instruction to feed each output into
  the next step.

  That suggests this interpretation of the five fields:

  SEED          supplies known/input configuration data
  ALPHABET      defines possible values
  FRONTIER      identifies values to be determined or replaced
  NEIGHBORHOOD  identifies values available to the relation
  RULE          relates readable values to allowed frontier values

  Then iteration is not an intrinsic property of every Rule. It emerges when the program wiring makes the new frontier part
  of the next readable configuration.

  So I would revise Goal 1’s conclusion slightly:

  - Bare constraints, functions, and PDEs often do not define their own canonical trajectories.
  - They are nevertheless expressible as closed relational Rule objects.
  - Concrete evaluation, solution, or evolution requests can produce trajectories through the same five-field API.
  - Solver work should remain distinct from the mathematical relation it operates on.
  - None of this requires an UpdatePolicy.

  The unresolved question is primarily whether Seed means only “complete initial state” or more generally “generator/source
  of the known side of a relational construction.” If you choose the latter, the five-field API becomes substantially more
  universal without adding another top-level concept.

─ Worked for 4m 30s ─────────────────────────────────────────────────────────────────────────────────────────────────────────


› So constraints are like any other, but more like a one to many? or like any answer works as long as it meets the
  constraints? and ten functions are simply just one to the next step or the answer? but maybe not multi-step?


• Exactly.

  A constraint is best understood as a relation from known information to every valid completion:

  known/boundary values
      → {all assignments satisfying the constraints}

  That result may contain:

  - Zero answers: inconsistent constraints.
  - One answer: uniquely determined.
  - Many or infinitely many answers: every satisfying configuration is valid.

  So it is “one-to-many,” but only after choosing what counts as the known input. With no boundary data, it simply denotes a
  set:

  {X | X satisfies C}

  The rule does not choose one preferred answer. A solver may return one witness, enumerate several, or prove there are none,
  but that solver behavior is separate from the constraint.

  For example:

  x + y = 10
  x,y ∈ NaturalNumbers

  denotes:

  {(0,10), (1,9), ..., (10,0)}

  Any of those is a correct answer.

  A function is more specifically one-to-one-step:

  x → f(x)

  For example:

  3 → 9       where f(x)=x²

  That is one mathematical evaluation. It becomes multi-step only when the program feeds the answer back into the input:

  3 → 9 → 81 → 6561 → ...

  Those use the same underlying function but different program wiring:

  Evaluation:
      input slot → separate answer slot
      stop after producing the answer

  Iteration:
      current-state slot → same slot in next state
      repeat

  There is also a third possibility: the algorithm used to calculate f(x) may take many internal steps. For example,
  numerically finding Sin(1) or a zeta zero may involve iterative computation. That is the evaluator’s trajectory, not the
  mathematical function’s trajectory.

  So the clean cardinality picture is:

  Deterministic function:
      one input → one answer

  Partial function:
      one input → one answer or undefined

  Constraint/relation:
      known information → zero, one, or many valid answers

  Iterated function:
      repeatedly feed each answer back as the next input

  Multiway rule:
      current state → multiple next states, each of which may continue

  The difference between a constraint and a multiway evolution is what happens after branching:

  Constraint:
      problem → valid answers

  Multiway evolution:
      state → possible next states → further possible states → ...

  You can represent constraint answers as one-step trajectory branches, but they are normally endpoints unless another rule
  explicitly continues from them.


› I feel like all of that can fit in the minimal set, right?


• Yes. I think they all fit once the minimal API adopts one general rule contract:

  RULE:
      readable neighborhood
          → zero or more possible replacements of the frontier

  The universal semantics become:

  class SimpleProgram:
      seed: Seed
      alphabet: Alphabet
      frontier: WritableRegion
      neighborhood: ReadableRegion
      rule: Rule

  1. SEED produces initial configuration(s).
  2. FRONTIER identifies what may be filled or replaced.
  3. NEIGHBORHOOD identifies what the rule can read.
  4. RULE returns zero, one, or many frontier replacements.
  5. Each replacement produces a successor, preserving everything outside the frontier.

  Then cardinality handles the different cases:

  0 replacements     impossible, terminal, undefined, or unsatisfied
  1 replacement      deterministic answer/next state
  many replacements  multiple valid answers or multiway evolution
  distribution       stochastic answer/next state

  ### Function evaluation

  seed          = Input(3)
  frontier      = output slot
  neighborhood  = input slot
  rule          = y = x²

  Result:

  Input(3) → Answer(9)

  Answer(9) can have no further applicable replacement, so the trajectory ends.

  ### Iterated function

  seed          = 3
  frontier      = current value
  neighborhood  = current value
  rule          = x′ = x²

  Result:

  3 → 9 → 81 → 6561 → ...

  Same mathematical rule; different frontier/neighborhood wiring.

  ### Constraint

  seed          = known values or boundary data
  frontier      = unknown region
  neighborhood  = known values and constraint dependencies
  rule          = every frontier assignment satisfying the constraint

  Result:

  Problem → {Solution₁, Solution₂, ..., Solutionₙ}

  There may be zero, one, many, or infinitely many valid replacements. The Rule denotes all valid answers; a concrete solver
  is how an implementation tries to produce them.

  ### Multiway evolution

  seed          = initial word
  frontier      = every matching region
  neighborhood  = match context
  rule          = every permitted rewrite

  Result:

  State₀ → {State₁, State₂}
  State₁ → {...}
  State₂ → {...}

  Unlike constraint answers, those successors remain eligible for repeated rule application.

  ### PDE

  For a boundary-value problem:

  seed          = region and boundary data
  frontier      = unknown interior field
  neighborhood  = differential dependencies
  rule          = every field satisfying the PDE and side data

  For an evolutionary PDE:

  seed          = Cauchy data
  frontier      = evolving spatial field
  neighborhood  = differential germ of the current field
  rule          = next field or continuous flow relation

  Again, the same five concepts work.

  The only real requirements are:

  - Seed may describe one configuration, a family, a probability law, or partial known data.
  - Frontier may be a structured or continuous region, including presently unfilled support.
  - Neighborhood need not be spatially local.
  - Rule is a relation returning zero-to-many replacements, not necessarily a scalar function.
  - Replacement is atomic and preservation outside the frontier is fixed framework semantics.

  Under that contract, constraints, functions, PDEs, deterministic transitions, stochastic systems, and multiway systems do
  not require different top-level APIs. They are different cardinalities and wirings of the same five pieces.

  So yes: the Goal 1 “nonfit” conclusion appears to follow from assuming Rule means “one temporal successor.” Once Rule means
  a general relation between readable state and writable state, those nonfits largely disappear.
