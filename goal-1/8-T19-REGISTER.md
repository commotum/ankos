# 8-T19-REGISTER

Status: **REOPENED — ARCHITECTURE AUDIT; EVIDENCE CLOSED**

The evidence/search closure and conformance fixtures remain valid. Register state is being re-derived as the transparent `FiniteRegisterBank × ProgramCounter` product on `t+0D`; `SingleControl`/`TransitionControl` are not required classes.

## Current Facts

- Exact catalog row: T19, CSV line 20, `Register Machines`; taxonomy seed `ref/notes/CA-Types.md:495-522`.
- The native state is a finite bank of named registers containing arbitrary-precision non-negative integers plus one visible program counter. The immutable program is a nonempty ordered instruction sequence, not evolving state.
- The Chapter 3 base presentation uses two instruction forms. `Increment(r)` adds one to register `r` and falls through. `DecrementJump(r,target)` subtracts one and jumps when the old value is positive; at zero it leaves the register unchanged and falls through. The zero result is the conditional branch, not a clamp after negative arithmetic.
- Each successful instruction is one atomic event over an old snapshot: its numeric effect and program-counter transition cannot be observed or committed separately.
- The canonical examples loop only through explicit decrement-jumps. There is no implicit wrap at the end of the program.
- The exact reference `RMStep` returns an unchanged state whenever `pc > program length`. Program exhaustion is therefore an absorbing quiescent condition with no instruction event. The Notes separately say it is sometimes convenient to interpret the same condition as a special halt; that is an explicit episode/analysis policy, not another base instruction or hidden executor behavior.
- A last increment or zero-fallthrough is still a valid event and produces `pc = length + 1`. A successful jump may also deliberately target beyond the program, as the canonical square-root example does. Only the next requested step observes program exhaustion.
- The usual enumerated profile restricts decrement-jump targets to the `n` in-program addresses. With `k` registers and exact program length `n`, it has `(k(n+1))^n` structured programs. The source gives this cardinality but no digit significance or canonical integer program code.
- The program and seed are independent. The canonical figures use `pc=1` and zero registers, while arbitrary natural-valued register vectors are native. Prepending increments can compile an arbitrary seed into a zero-seed program, but changes the program and event timeline and is not semantic identity.
- Compressed zero-hit diagrams, logarithmic register plots, executed-instruction subsequences, binary digit views, and the derived `3n+1` arithmetic recurrence are observers over full instruction events. They are not alternative machine state or a reduced executor.
- More registers and the exact `eq`, `add`, and register-indirect `jmp` instructions are documented variants. Continuous real registers, universal fixed machines, and CA/Turing/arithmetic/Diophantine representations are separate variants, compilers, or reductions, never the native T19 carrier.
- T09/T12's visible `SingleControl`, typed control transition, atomic compound effects, structured event traces, and outcome distinctions compose. Their spatial/tape supports, finite alphabets, and geometric reads do not. T19 adds an infinite `Naturals` value domain, finite named register bank, program-address source, instruction-owned operand access, typed arithmetic results, and a quiescent outcome; it does not require a new update algebra.

## Updated Assumptions

- `SingleControl` must be generic over a typed address domain. A program counter can point into immutable code without implying that instructions or registers are spatial cells.
- A finite register bank is named value support with no adjacency or boundary. Tuple order supplies stable serialization and keys, not a lattice topology or neighborhood geometry.
- `Natural` is an exact infinite value domain. It cannot be implemented as a large finite alphabet, NumPy `int64`, float, modular value, saturating counter, unary tape, or fixed-capacity field.
- Source selection and reads are program-coupled in the same substantive sense as T16 match selection: the active instruction determines its operand-access plan. One immutable validated program owns instruction identity, register references, and jump targets; there is no duplicate selector configuration or instruction callback.
- Base instruction evaluation is a closed tagged algebra. Adding a whole-machine function, `Any` payload, formula rule, opcode-family rollout, or host exception branch would erase the construction rather than generalize it.
- `AtomicEffectsUpdate` can commit typed effects aimed at different state components. T19 reuses it for register assignment plus control transition after validating both against the same snapshot.
- `Quiescent(PastProgramEnd)` is neither an executed identity instruction nor necessarily a zero-successor terminal. The exact reference sampler may repeat it indefinitely; a `ProgramExitStop` policy may instead emit one retained terminal state and stop.
- A successful instruction always changes state: increment changes a register, a positive decrement changes a register even when it jumps to the same address, and a zero branch advances the counter. State equality can therefore distinguish a reference stutter here, but trace semantics must still use the typed event/outcome rather than infer meaning from equality.
- The finite enumeration profile and the general executable profile must remain distinct structured validators. The former restricts jump targets to `1..n`; the latter permits a positive target beyond `n` as an explicit exit. Neither permits zero/negative program counters or register references.
- Register-swap equivalence is an analysis symmetry, not a quotient of program identity. Repeated instructions and behaviorally equivalent programs remain separate syntactic programs.

## Big Picture Objective

Reconstruct the complete register-machine instruction cycle, numeric state, conditional control, program boundary, seed, enumeration, observers, native variants, and emulation relations. Determine whether the source/read/result/update protocol remains construction-bearing when control selects immutable code and the program directs named unbounded-value reads, while rejecting spatial packing, fixed-width arithmetic, implicit wrap, opaque evaluation, family dispatch, and observer-defined state.

## Catalog Identity

- Stable ID: T19.
- Exact name: Register Machines.
- CSV provenance: `ref/notes/CA-Types.csv:20`; taxonomy provenance: `ref/notes/CA-Types.md:495-522`.
- Entry kind: deterministic finite-program numeric state machine; the base reference relation is total over valid positive-counter states because exhausted programs stutter.
- Direct body aliases: `counter machines` and `program machines` (`BOOK:12402`). The alphabetic Index also routes `Abacus machines` to register machines (`BOOK:20836`) but supplies no body construction under that name.
- `URM` means **universal register machine**, a fixed interpreter variant (`BOOK:18894-18908`, `22390-22392`), not “unlimited register machine.” The corpus contains no `Minsky machine` or `unlimited register machine` phrase. Minsky is a historical attribution, not a local alias.
- Search vocabulary: register/counter/program/abacus machine; register bank/value/key; instruction/program counter/opcode/address; increment; decrement-jump; zero/nonzero/fallthrough/jump; beginning/end/wrap/exit/halt/stutter; program length/count/numbering; initial condition; compressed evolution/zero hit/`3n+1`; many/three/two registers; add/subtract/compare/equal/indirect jump; universal/URM; `RMStep`, `RMExecute`, `RMEvolveList`, `RMToCA`, `TMToRM`, `RMEncode`, `RMToRM2`, `RMToAS`, and `R2ToURM`.

## Search Log

1. Verified CSV/taxonomy identity and read the entire local taxonomy section. The taxonomy is a search seed only; every construction statement below was checked against canonical book evidence.
2. Searched the monolithic book for singular/plural `register machine`; this produced 129 occurrences on 94 direct-name lines. Expanding through counter/program/abacus aliases produced 135 occurrences on 95 lines: 57 relevant body/Notes lines, 35 Index routes, two passing generic mentions, and one false binary-counter hit. Universal/URM routes, exact implementation/compiler symbols, instruction/control terms, counts, seeds, observers, halting, histories, and emulation vocabulary were searched separately.
3. Inspected every direct candidate in context, not just the match line. The native core is `BOOK:1160-1218`; implementation/history is `BOOK:12366-12403`; later constructive relations and variants are dispositioned below.
4. Inspected all three Chapter 3 figures directly: `_page_113_Figure_1.jpeg`, `_page_114_Picture_5.jpeg`, and `_page_115_Figure_1.jpeg`. Image-only program transcriptions were independently executed against the visible trajectories or stated arithmetic observer.
5. Followed the complete alphabetic Index hub at `BOOK:21923-21925`: core pages 97-102; square root; continuous version; arithmetic and CA emulation; Turing-machine emulation; Diophantine encoding; halting and halting problem; history/implementation; intermediate degrees; attempted Life proof; many registers; random initial conditions; small universal machines; and tiling undecidability.
6. Followed corroborating Index routes for decrement-jump, increment, program counter, branching programs, opcodes, `3n+1`, arithmetic recurrence, Busy Beaver, halting, randomness, assemblers/languages/compilers/linker, primes, multiregister machines, and relevant historical names. These added no undispositioned base mechanics.
7. Checked split files. `CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:477-535` is a clean duplicate of the core. The misleading `BACK-MATTER/Index/Index.md:269-306` is a duplicate of Notes page 896, not the alphabetic Index. `BACK-MATTER/Colophon/Colophon.md` duplicates the later Notes/emulation passages and the actual Index hub. Canonical provenance is recorded once against the monolith.
8. Found two material OCR failures in both local Notes copies: `RMStep` stops mid-definition at `BOOK:12377`, and the halt-maxima list is corrupted at `BOOK:12382`. Narrowly repaired only those facts from the official primary [implementation note](https://www.wolframscience.com/nks/notes-3-9--implementation-of-register-machines/) and [halting note](https://www.wolframscience.com/nks/notes-3-9--halting-of-register-machines/), then cross-checked mechanics against `BOOK:1166-1172`, counts, figures, and independent execution.
9. Searched for a halt instruction, separate zero-test instruction, implicit wrap, self-modifying program, numeric rule/program codec, state-transition-graph definition, `Minsky machine`, and `unlimited register machine`; none is evidenced for T19.
10. Excluded false positives: shift registers; a Turing machine used as a binary counter (`BOOK:12054`); Minsky's universal Turing machine; cross-column OCR fragments; the derived arithmetic recurrence; random low-level-language crash commentary; and CA/TM/arithmetic/Diophantine/tiling encodings. Zero unresolved native-mechanics candidates remain.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These 25 groups capture every unique local passage that materially determines T19 or a boundary with another construction. Split duplicates are logged above rather than copied.

### E01 — Practical-computer idealization and exact base instruction set

- Provenance: `BOOK:1160-1172`, Chapter 3, “Register Machines.”
- Fact: practical registers store numbers and programs are instruction sequences. The simple construction has two registers whose numbers may be any size and two instructions. Increment adds one. Decrement-jump subtracts and transfers control only when possible; at zero the value is unchanged and execution falls through. The zero case supplies conditional control.

### E02 — Visible program counter, canonical seed, and explicit looping

- Provenance: `BOOK:1174-1184`, `_page_113_Figure_1.jpeg`.
- Fact: successive rows expose both register values and a dot marking the instruction being executed. All shown machines start at instruction one with both registers zero. The caption twice qualifies that the **particular programs** jump back to the beginning; direct image inspection shows an explicit final decrement-jump, so the figure is not evidence of end wrap.

### E03 — Short-program enumeration and syntactic identity

- Provenance: `BOOK:1186-1198`, `_page_114_Picture_5.jpeg`, `_page_115_Figure_1.jpeg`.
- Fact: there are 10,552 programs of lengths at most four; exactly 248,832 of length five, with two register-swapped nonrepetitive examples; 276,224,376 through length seven; and exactly 11,019,960,576 of length eight, with 126 complex cases. Register swap is reported as a relation between two programs, so it is not quotienting the count.

### E04 — Event-derived observers and arithmetic recurrence

- Provenance: `BOOK:1198-1206`, with the related arithmetic discussion at `BOOK:1497-1507`.
- Fact: the complex eight-instruction example is compressed by retaining events where either register has just decreased to zero; further panels show executed instructions and second-register values at first-register zero hits. The latter sequence starts at one and follows `3n/2` for even `n` and `(3n+1)/2` for odd `n`. “Has just decreased” makes this an event predicate, not a snapshot filter for `register == 0`.

### E05 — More registers, extended operations, and language analogy

- Provenance: `BOOK:1208-1218`.
- Fact: three registers allow similar complex behavior with seven instructions. Extended sets may add/subtract/compare two registers. Such machines resemble low-level programs with variables corresponding to registers and no arrays or pointers. The analogy does not license arbitrary host-language callbacks.

### E06 — Exact state, canonical five-instruction program, seed, and count

- Provenance: `BOOK:12366-12380`.
- Fact: state is `{n,list}`, with `n` the current instruction and `list` the register values. The page-99 program is `{i[1],d[2,1],i[2],d[1,3],d[2,1]}` and a typical seed is `{1,{0,0}}`. Exact-length cardinality is `(k(1+n))^n`. Prepending increments can simulate arbitrary initial register values, which evidences a compiler relation without eliminating independent seeds.

### E07 — Repaired reference stepper and absorbing exhaustion

- Provenance: locally truncated `BOOK:12374-12377`; narrow repair from the official implementation note linked in the Search Log.
- Fact: `RMStep` first tests `n > Length[prog]` and returns `{n,list}` unchanged. Otherwise it fetches `prog[[n]]`. Increment returns counter `n+1` with one register incremented. Positive decrement returns its fixed target with one register decremented; zero returns `n+1` unchanged. `RMEvolveList` is `NestList`, so a requested horizon can show repeated exhausted snapshots even though no instructions execute.

### E08 — Optional halt interpretation and repaired maxima

- Provenance: `BOOK:12382-12385`; narrow numeric repair from the official halting note.
- Fact: the Notes say it is *sometimes convenient* to enter a special halt state when execution is attempted beyond the program. From zero seed the exact maximum executed-instruction counts for lengths one through eight are `{1,3,5,10,16,37,215,1280}`. The listed length-eight witness exits at `pc=9` with registers `[81,0]` after 1,280 instruction events.

### E09 — Exact extended instructions and history aliases

- Provenance: `BOOK:12388-12403`.
- Fact: `eq[r1,r2,m]` jumps to `m` iff the old values are equal and otherwise falls through; `add[r1,r2]` replaces the first operand by the old sum and falls through; `jmp[r1]` loads the counter from the old register value. Only prose mentions subtraction, so no exact subtraction semantics is inferred. The history passage supplies `counter machine` and `program machine` aliases and Shepherdson/Sturgis/Minsky attributions.

### E10 — Finite integer initial conditions have no canonical randomness

- Provenance: `BOOK:14275`.
- Fact: systems based on integers, explicitly including register machines, use finite digit sequences and have no unique definition of random initial conditions. T19 therefore supports explicit arbitrary natural tuples but no privileged infinite random bank or seed distribution.

### E11 — Cellular-automaton emulation is a compiler

- Provenance: `BOOK:7962-7972`.
- Fact: a CA can use expanding/contracting unary side patterns for register magnitudes and a center cell color for the program point. This visibly changes representation and timing; it is evidence of emulation, not native register topology.

### E12 — Register-machine universality and arithmetic packing

- Provenance: `BOOK:8082-8102`.
- Fact: a shown three-register, 72-instruction program emulates a two-state Turing machine, with a compressed checkpoint every other time register three increments from zero. An arithmetic system can encode program position and two registers using a residue and prime exponents. Both are explicitly compiled/stroboscopic relations.

### E13 — Exact RM-to-CA compiler and seed encoding

- Provenance: `BOOK:18416-18422`.
- Fact: `RMToCA` produces an `m+7`-color CA for an `m`-instruction two-register program; register values become unary regions and the program point becomes a distinguished cell state. The compiled initial row depends on register values. This route must never be used to satisfy T19 natively.

### E14 — Exact TM-to-RM compiler and checkpoints

- Provenance: `BOOK:18576-18592`.
- Fact: `TMToRM` creates and links instruction segments. A blank tape maps to `{1,{0,0,0}}`; two registers encode left/right tape digits and a third coordinates the simulation. A machine with `s` states generates 34s-36s instructions. The compiler proves expressiveness, not shared native state.

### E15 — Many-register to two-register compilation

- Provenance: `BOOK:18594-18617`.
- Fact: a finite register vector is encoded into prime exponents of one natural and the program is compiled to two registers. Correct multiregister checkpoints occur when the second compiled register increments from zero. Native register identity must therefore remain unpacked even though two-register computational sufficiency is proved.

### E16 — Concrete computation and deliberate past-end target

- Provenance: `BOOK:18619-18624`.
- Fact: a 14-instruction, three-register program computes rounded square root. It includes target 15, directly showing a positive beyond-end target used as program exit; for input ten it independently reaches `pc=15,[3,0,0]` after 43 executed instructions.

### E17 — Arithmetic-system compiler and decoder

- Provenance: `BOOK:18626-18646`, corroborated by the clean main caption at `BOOK:8102`.
- Fact: `RMToAS` packs a counter and prime-power register values into one integer and reconstructs them by modular arithmetic/factorization. A local OCR defect in one formula is resolved by the caption and decoder. This is a relation only, never a reason to make native T19 state one integer.

### E18 — Fixed universal register machines

- Provenance: `BOOK:18894-18908`.
- Fact: the evidence only suggests no universal two-register machine among programs through length eight. Documented universal constructions include three registers/175 instructions, two registers/4,694 instructions, and Korec's fixed eight-register/41-instruction machine. `R2ToURM` places a compiled program and input into the fixed machine's initial condition, with enormous slowdown.

### E19 — Continuous-register variant boundary

- Provenance: `BOOK:19080-19086`, especially `19082-19084`.
- Fact: continuous models generalize registers to arbitrary reals and usually add arithmetic primitives while retaining discrete programs/choices/steps. Arbitrary real initial digits or equation-solving primitives can smuggle oracle power. This is a separate construction, not a broadened base `Natural` domain.

### E20 — Register machines as meta-program enumeration

- Provenance: `BOOK:19113-19125`.
- Fact: the intermediate-degree construction uses register machines to enumerate programs and their possible outputs inside a diagonal argument. It adds oracle/halting meta-structure, not a new ordinary instruction or state component.

### E21 — General halting context

- Provenance: `BOOK:19240-19246`.
- Fact: practical programs are often regarded as halting after finishing instructions, while other long-running programs may become unchanged. This supports the explicit `ProgramExitStop` interpretation but does not override the exact base `RMStep` stutter.

### E22 — Incomplete Life route

- Provenance: `BOOK:18749-18751`.
- Fact: the historical register-machine route to Life universality is explicitly described as incomplete. It is not cited as a proof or used as native conformance evidence.

### E23 — Tiling reduction

- Provenance: `BOOK:19274`.
- Fact: Berger's tiling-undecidability construction can be understood through an elaborate register-machine emulation. This is a reduction, not a native topology, state, or transition rule.

### E24 — Diophantine reduction

- Provenance: `BOOK:19931-19935`.
- Fact: Diophantine equations can emulate register or arithmetic systems. The equation variables and solution relation are not T19 state or execution.

### E25 — Exhaustive Index hub

- Provenance: `BOOK:21923-21925`, with aliases at `20836`, `21054`, `21819`, and `22390-22392`.
- Fact: the hub routes every core, implementation, history, halt, variant, initial-condition, universality, and emulation topic above. All routes are dispositioned; no additional native instruction, state component, boundary rule, or integer code appears.

## Construction Model

### State, program, and domains

The base value domain is exact:

```text
Natural = arbitrary-precision integer n with n >= 0
RegisterKey(k) = one of 1..k
PositiveProgramCounter = integer pc >= 1
```

The immutable dynamics object is structured data:

```text
Instruction(k) =
    Increment(register: RegisterKey(k))
  | DecrementJump(register: RegisterKey(k), target: PositiveProgramCounter)

RegisterProgram = (
    register_count: positive integer k,
    instructions: NonEmptySequence[Instruction(k)],
    target_profile: EnumeratedInProgram | PositiveExitTargets,
)
```

`EnumeratedInProgram` requires every target in `1..length` and is the profile counted by the book. `PositiveExitTargets` admits a target greater than `length`, which becomes exhausted control, and is required by E16. Zero/negative targets, invalid register keys, booleans masquerading as integers, missing/opaque instructions, and program mutation are invalid. They do not wrap, clamp, halt, or fall through.

The visible Markov state is:

```text
RegisterMachineState(
    bank = FiniteRegisterBank[RegisterKey(k), Natural],
    control = SingleControl(
        key="program_counter",
        position=PositiveProgramCounter,
        payload=Unit,
    ),
)
```

The bank contains exactly `k` values. It is not a line: register 1 has no spatial neighbor relationship to register 2, and there is no boundary outside the bank. The counter addresses program text, not bank support. Program, seed, horizon, stop policy, and observers remain independent validated objects.

### Source, operand reads, and closed instruction results

Program-coupled source selection is explicit:

```text
ActiveInstruction.select(state.control, program) ->
    ExecutableInstructionSource(
        program_identity,
        snapshot_id,
        pc,
        instruction,
        operand_access_plan,
    )
  | PastProgramEnd(pc, program_length)
```

For `1 <= pc <= length`, the exact instruction determines the typed register read. Even increment reads the old operand so arithmetic and expected-old validation are inspectable. Base instructions read exactly one register; extended `eq`/`add` read two; register-indirect `jmp` reads the addressed register. There is no geometric neighborhood, arbitrary address callback, whole-bank formula, or executor-local instruction fetch.

Base evaluation returns a closed result sum carrying typed effects:

```text
IncrementResult(
    source,
    operand=(r, old),
    effects=(Assign(RegisterSlot(r), old + 1),
             TransitionControl(pc, pc + 1)),
)

DecrementJumpTaken(
    source,
    operand=(r, old > 0),
    effects=(Assign(RegisterSlot(r), old - 1),
             TransitionControl(pc, target)),
)

ZeroFallthrough(
    source,
    operand=(r, old == 0),
    effects=(TransitionControl(pc, pc + 1),),
)
```

The result records its branch explicitly; zero need not fabricate an assignment from zero to zero. `AtomicEffectsUpdate` validates program identity, snapshot ownership, expected counter, expected old operand, register key/domain, effect uniqueness, and next counter, then commits all effects together. Any stale source, overflow/coercion, negative result, missing effect, extra write, contradictory target, or partial failure is an error with no state mutation.

This is substantive reuse of T09/T12. `Assign` targets a named value location and `TransitionControl` targets visible control; atomic update never required those targets to share a lattice. T19 adds instruction/result members but not a fifth update algebra.

### Exact instruction cycle

For an executable counter:

```text
old = state
source = ActiveInstruction.select(old.control, program)
read = InstructionOperandRead(old.bank, source.access_plan)
result = ExecuteInstruction(source.instruction, read)
next = AtomicEffectsUpdate.apply(old, result.effects)
return Advanced(next, RegisterInstructionEvent(old, source, read, result, next))
```

The counter in snapshot `t` identifies the instruction executed between snapshots `t` and `t+1`. The event preserves `pc_before`, instruction identity, operand key/value(s), branch, typed effects, `pc_after`, and full before/after bank values. An increment and its fallthrough are one event. A decrement and its conditional jump are one event. New values cannot influence the branch that produced them.

### Program end, quiescence, and halting

When `pc > length`, base reference execution returns:

```text
Quiescent(
    reason=PastProgramEnd(pc, length),
    state=old,                 # exact pc and bank retained
    instruction_event=None,
)
```

A reference-history sampler may append the unchanged state for every further requested sample, matching `NestList`. Those samples must be labeled quiescent; they are not identity instructions, zero fallthroughs, or advanced events.

An explicit episode policy can instead map the same first exhaustion observation to:

```text
Terminal(reason=ProgramExit, final_state=old)
```

and retain the final state once with zero further successors. This policy is appropriate for the Notes' optional halt analysis and practical-program view. It is not a boolean inside `RegisterProgram`, an implicit wrap policy, or a second executor.

Distinguish all of:

- `Advanced` into `pc=length+1` after the last valid instruction;
- `Quiescent(PastProgramEnd)` with reference stutter and no instruction event;
- `Terminal(ProgramExit)` under an explicit stop interpretation;
- an external predicate stop;
- horizon exhaustion;
- invalid state/program/reference;
- execution/storage error.

An explicit last decrement-jump to one loops because the instruction says so. No host array index or default boundary supplies wrap. A jump to any positive value beyond the end exits. A counter below one is invalid rather than a Python/Mathematica indexing convention.

### Enumeration and program identity

For exact length `n` and `k` registers under `EnumeratedInProgram`, each instruction slot has:

```text
k increment choices + k*n decrement-jump choices = k(n+1)
```

so the total is:

```text
(k(n+1))^n
```

For `k=2`, exact lengths one through eight are:

```text
4, 36, 512, 10,000, 248,832, 7,529,536,
268,435,456, 11,019,960,576
```

The sums through four and seven are respectively `10,552` and `276,224,376`, matching E03. These are syntactic counts. Program equality and serialization use the declared register count plus ordered tagged instructions and operands. No integer `rule_id`, digit order, behavior quotient, register-symmetry quotient, or exhaustive infinite-value table is inferred.

### Seed and observation model

The canonical preset is:

```text
pc = 1
registers = (0, ..., 0)
```

but native seeds may specify any positive counter and any exact natural vector of length `k`. A past-end seed is valid and immediately quiescent/terminal according to observation policy. An invalid counter below one or negative/wrong-arity register value is rejected.

Prepending increments to compile a seed into a zero vector is an explicit transformation that changes program length, addresses, and elapsed instruction count. Its correctness can be tested as a relation after its setup prefix, never used to canonicalize program/seed identity.

Observers consume snapshots and `RegisterInstructionEvent`s:

- raw counter/register trajectory;
- successful-decrement-to-zero events for either selected register;
- executed-instruction subsequence at those events;
- logarithmic or binary rendering of selected values;
- arithmetic checkpoint sequence for the page-100 program;
- program-exit time and final bank;
- register-swap symmetry and behavior classification.

The zero-hit predicate is `old_value > 0 and new_value == 0` on a `DecrementJumpTaken` event. It must not select an initially zero register or repeated zero-fallthrough/quiescent snapshots.

### Exact trajectory and relation oracles

The first simple figure program is visually decoded as `[i1,d1->1]`. From `(pc,r1,r2)=(1,0,0)`:

```text
t0 (1,0,0)
t1 (2,1,0)
t2 (1,0,0)
```

The return is caused by the explicit `d1->1`, not wrap.

For the exact E06 five-instruction program and zero seed:

```text
t0  (1,0,0)
t1  (2,1,0)
t2  (3,1,0)
t3  (4,1,1)
t4  (3,0,1)
t5  (4,0,2)
t6  (5,0,2)
t7  (1,0,1)
t8  (2,1,1)
t9  (1,1,0)
t10 (2,2,0)
t11 (3,2,0)
t12 (4,2,1)
t13 (3,1,1)
t14 (4,1,2)
t15 (3,0,2)
t16 (4,0,3)
t17 (5,0,3)
t18 (1,0,2)
```

This one fixture crosses positive decrement-jumps and zero fallthroughs on both registers, fixed and backward targets, and counter/register timing.

The page-100 figure program is visually decoded and independently validated as:

```text
[i1,i1,i1,d2->1,d1->6,i2,d1->5,d2->3]
```

At successful register-1 decrements to zero, `(executed step,r2,next pc)` begins:

```text
(8,1,6), (23,2,5), (47,3,6), (79,5,5),
(129,8,5), (204,12,6), (312,18,6), (471,27,6),
(707,41,5), (1063,62,5), (1597,93,6), (2394,140,5)
```

The values `1,2,3,5,8,12,18,27,41,62,93,140,...` exactly satisfy E04. This guards image transcription, event filtering, and observer separation.

Boundary discriminators are intentionally tiny:

```text
[i1], seed (pc=1,[0])
    -> Advanced(pc=2,[1])
    -> Quiescent(pc=2,[1]) forever in reference sampling

[d1->1], seed (pc=1,[0])
    -> Advanced ZeroFallthrough(pc=2,[0])
    -> Quiescent(pc=2,[0])

[d1->1], seed (pc=1,[1])
    -> Advanced DecrementJumpTaken(pc=1,[0])
    -> Advanced ZeroFallthrough(pc=2,[0])
```

The repaired eight-instruction halt witness must execute exactly 1,280 events and end at `(pc=9,[81,0])`. The square-root program with input ten must execute 43 events and end at `(pc=15,[3,0,0])`. Exact arithmetic tests additionally start above `2^63` and verify increment/decrement without dtype coercion.

### Variant disposition

| Candidate | Disposition |
|---|---|
| Two-register, `i`/`d` program | Strict canonical preset over the generic finite-register protocol. |
| Any finite `k` | Native parameterization; three-register examples are direct. |
| In-program jump targets | Enumerated profile counted by `(k(n+1))^n`. |
| Positive beyond-end target | General executable profile; direct square-root exit evidence. |
| Raw past-end behavior | Native reference `Quiescent` stutter, preserving counter and bank. |
| Special halt at program exit | Explicit stop/analysis interpretation, not base instruction or wrap. |
| `eq`, `add`, register-indirect `jmp` | Closed extended instruction members with exact Notes semantics; separate preset/profile. |
| Subtract two registers | Mentioned in prose only; exact result/underflow semantics unresolved, so no implementation inferred. |
| Many-register to two-register | Compiler using prime-power packing and stroboscopic checkpoints. |
| Continuous real registers | Separate continuous-computation construction; never base domain widening. |
| Fixed URM | Universal interpreter program plus encoded input; separate variant/compiler. |
| CA, Turing, arithmetic, Diophantine, tiling encodings | Relations/reductions; never native T19 state, update, or trace. |
| Life route | Historical incomplete proof, excluded as conformance evidence. |
| Compressed/zero-hit/`3n+1` views | Derived observers over full events. |
| Random initial register vector | No canonical distribution evidenced; accept explicit seed only. |
| Integer program code | Not evidenced; retain structured program identity and exact count only. |

## Current API Fit

| Concern | Fit | Finding |
|---|---|---|
| Canonical dense domain/address | SEMANTIC MISMATCH | `simple_programs.md:1-24,87-113` fixes dense `[t,x,y,z]` fields. A finite named bank plus a counter into immutable code has no spatial rank, adjacency, or shared coordinate support. |
| Value/alphabet | PRINCIPLED EXTENSION | The value-set responsibility (`:200-233`) is reusable, but current alphabets are finite. T19 needs exact infinite `Naturals`; program instructions and counter addresses are separate domains. |
| State/control | PRINCIPLED EXTENSION | The documented field has no visible payload/control component. Reuse the T09/T12 `SingleControl` architecture, generalized to program addresses, plus a named register bank. |
| Seed | PRINCIPLED EXTENSION | Selector/fill/distribution seeds (`:235-290`) create dense slices. T19 needs an explicit counter and finite natural tuple, independent of program and horizon. |
| Boundary | NOT APPLICABLE | Fixed/periodic/reflective policies (`:292-358`) concern spatial reads. Program exhaustion is a typed quiescent/exit condition; invalid register keys are validation errors. |
| Neighborhood/read | SEMANTIC MISMATCH | Relative coordinate selectors (`:360-731`) cannot express instruction-owned named-register access or distinguish code fetch from operand read. |
| Frontier/source | SEMANTIC MISMATCH | A writable next-slice frontier (`:1412-1510`) is not the visible counter-selected current instruction. |
| Rule | SEMANTIC MISMATCH | Scalar target-value rules (`:1767-1793`) cannot represent a closed instruction union, conditional branch, arithmetic effect, and counter transition. |
| Formulaic rule | SEMANTIC MISMATCH | A whole-state formula (`:2036-2073`) could simulate the machine but would hide instruction validation, reads, typed effects, and shared orchestration. |
| Update | PRINCIPLED EXTENSION | Current copy/parallel scalar write (`:1767-1793,2156-2199`) is insufficient, but T09/T12's planned `AtomicEffectsUpdate` directly fits register assignment plus control transition. No T19-only commit is needed. |
| Successor/termination | PRINCIPLED EXTENSION | Fixed-horizon generation lacks reference quiescence, optional program-exit terminal interpretation, event-free repeated samples, and structured stop reasons. |
| Trace/encoding | SEMANTIC MISMATCH | A dense scalar tensor cannot preserve arbitrary-precision values, code-address control, instruction events, branches, and quiescent-vs-terminal metadata. |
| Program ID/count | PARAMETERIZATION | Structured instruction serialization and finite-profile counts are supported conceptually; requiring one integer ID would add unsupported semantics. |
| Observers | PARAMETERIZATION | Zero-hit, instruction, logarithmic, binary, arithmetic, and halt-time views are derivable if full event provenance is retained. |

## Current Runtime Fit

- `src/ca/alphabets.py:43-85` represents finite alphabets. It has no infinite exact natural domain. A huge finite range would create a fake maximum and make program behavior depend on storage capacity.
- `Dynamics` requires a fixed shape and carries `Any`-like rule data (`src/ca/specs.py:23-55`); `RawEpisode`/`RawBatch` use a NumPy array plus scalar integer `rule_id` (`:58-81`). A fixed number of registers does not make an `int64` tensor faithful: values are unbounded, the counter has a different semantic role, and events/programs are structured.
- `frontiers.py:54-80` exposes only full time slices. It cannot select one current instruction from immutable code or return `PastProgramEnd`.
- `rules.py:30,64-78,316-334` permits family strings, `Any` parameters, and callables. A `formulaic` register step would be precisely the prohibited whole-machine escape hatch.
- `_rollout_states` and `_rollout_batch_states` dispatch through family names (`src/ca/rollout.py:145-212`). Adding a `register_machine` branch would duplicate execution and fail Principle 0.
- Rollout and seed/batch paths allocate/coerce NumPy integer arrays (`src/ca/rollout.py:342-354,583-598,610-629`). Values above `2^63-1` overflow or coerce, violating E01. Object-dtype arrays are not a principled replacement for a typed state/event boundary.
- The spatial path performs scalar per-coordinate writes and requires `time_slice` (`src/ca/rollout.py:576-660,825-831`). It has no named-bank assignment, expected-old arithmetic, program-address control, atomic compound commit, or quiescent outcome.
- Dense `canonical_coords` can lower a snapshot for downstream export, but treating `[t,x,0,0]` as native state would falsely make register-number proximity topological. A lowering must attach roles and preserve the structured program/control/event tables.
- Existing tests cover current fixed-family/fixed-array behavior only. They contain no arbitrary-precision value, visible-counter discriminator, zero/nonzero branch pair, atomic rollback, program-end stutter/exit split, structured program count, or event-derived zero-hit observer.

## Principles Audit

| Principles | T19 result |
|---|---|
| 0-3 | The source/read/result/update shell survives only after program-address control, a finite named bank, exact naturals, and instruction-owned access are derived. Spatial coordinates and finite alphabets are not protected abstractions. |
| 4 | Closed `IncrementResult`, `DecrementJumpTaken`, and `ZeroFallthrough` expose arithmetic/control effects. Quiescence and exit are typed outcomes, not booleans or executor branches. |
| 5 | Counter and every register value are visible Markov state. No loop index, pending jump, overflow bit, prior zero event, or encoded program is hidden. |
| 6-8,12 | Program semantics, full structured trace, compressed views, arithmetic relation, ANKoS lowering, batching, and rendering remain separate. |
| 9 | Program length, instruction addresses, register keys, operand plan, and results are intrinsically coupled through one immutable program. Seeds, horizon, stop interpretation, and observers remain independent. |
| 10 | The two-register base and enumerated target profile are strict constructors over the generic protocol. Extended instructions and URMs are closed data variants, not mode strings or family rollout. |
| 11 | Old-value branching, atomic value/control timing, exact past-end stutter, and event-derived zero hits are defining. Host lists, dicts, integer objects, and serialization formats are incidental only if exact. |
| 13-15 | Zero/nonzero, self-target, visible-counter, last-instruction, explicit-exit, stutter/halt/horizon, count, overflow, stale-effect, observer, and compiler-separation adversaries are mandatory. |
| 16 | Typed domains/program/source/read/result/effects/outcomes are architecture. Formula callbacks, unary/prime packing, fake capacity, implicit wrap, and instruction-family dispatch are shims. |

The shared orchestration remains substantive:

```text
source  = SOURCE.select(old_state.control, immutable_program)
reads   = READ.read(old_state, source.access_plan)
result  = RULE.evaluate(source.instruction, reads)
outcome = UPDATE.apply(old_state, result.effects)
```

It is not a vacuous executor because every boundary enforces T19 construction facts. `ActiveInstruction` validates counter/program identity; `InstructionOperandRead` exposes the exact named values; a closed evaluator returns inspectable branch-specific effects; `AtomicEffectsUpdate` validates and commits them. `PastProgramEnd` bypasses no callback—it returns a typed quiescent outcome from source selection. T09/T12 keep their own spatial/tape sources and finite table evaluators while sharing control/effect/update/outcome responsibilities.

No earlier stage is reopened. T09's unit-payload active position and T12's payload-bearing head already required generic visible control; T19 clarifies that control addresses need not belong to the mutable value support. Their public state, rules, and outcomes do not change. The general outcome inventory expands with quiescence, and the value inventory expands with exact infinite domains.

## Detailed Implementation Plan

1. Record the closed core/figure/Notes/Index/split/history/variant/emulation audit and the two narrow official OCR repairs.
2. Add exact `Naturals`, `FiniteRegisterBank`, typed register keys, and program-address control without using finite alphabets, spatial coordinates, or NumPy scalar state.
3. Generalize `SingleControl` over typed address domains and add program-coupled `ActiveInstruction` plus closed instruction-specific operand access plans.
4. Add immutable structured `RegisterProgram` profiles and closed base instruction/result members; reuse `Assign`, `TransitionControl`, and `AtomicEffectsUpdate` with expected-old validation.
5. Add `Quiescent(PastProgramEnd)` to structured outcomes and an explicit `ProgramExitStop` interpretation, preserving valid last events, repeated reference samples, terminal traces, horizons, and errors distinctly.
6. Add event-rich register traces and observers for successful zero hits, executed instruction subsequences, numeric renderings, arithmetic checkpoints, and exit statistics.
7. Verify canonical trajectories, exact counts, repaired halt witness, square-root exit, branch/control discriminators, arbitrary precision, atomic rollback, immutability, observer provenance, and shared-executor operation.
8. Reintegrate the plan, evidence index, and design ledger; re-audit T09/T12 reuse and reopen them only if public behavior changes.

## Goal 2 Implementation Stage

### G2-T19 — Exact register banks, program-address control, closed instructions, and quiescent program exit

**Dependencies:** G2-T09/G2-T12 `SingleControl`, `Assign`, `TransitionControl`, atomic compound effects, structured events, and advanced/terminal/horizon/error outcomes; synthesis-selected generic source/read/rule/update orchestration. T19 does not depend on any CA, tape, substitution, arithmetic packing, or compiler implementation.

**Implementation areas:**

- Value-domain module: add `Naturals` with exact arbitrary-precision membership/coercion rules that reject bools, negatives, floats, overflow, and silent narrowing. Keep infinite domains distinct from exhaustively enumerable finite alphabets.
- State module: add immutable `FiniteRegisterBank` with positive stable register keys, exact natural values, structural equality/serialization, and no adjacency. Generalize `SingleControl` positions through typed address-domain validation and add `ProgramAddressSpace`.
- Program module: add tagged `Increment` and `DecrementJump`; immutable nonempty `RegisterProgram`; `EnumeratedInProgram` and `PositiveExitTargets` validators; canonical structured serialization; no required integer ID.
- Source/read module: add `ActiveInstruction`, `ExecutableInstructionSource`, `PastProgramEnd`, and instruction-authored operand plans/reads. Validate state/program register counts, counter positivity, snapshot/program identity, exact register accesses, and old values.
- Result module: add `IncrementResult`, `DecrementJumpTaken`, and `ZeroFallthrough` with explicit branches and typed `Assign`/`TransitionControl` effects. Extended `eq`, `add`, and `jmp` belong in a closed follow-on instruction-set preset after base conformance, never an arbitrary callable registry.
- Update module: reuse `AtomicEffectsUpdate`; broaden its typed target registry to named bank slots and program control if required. Require all expected-old checks before committing and guarantee rollback on every validation failure. Do not add a register-specific update loop.
- Outcome module: add `Quiescent(PastProgramEnd,state)` with no instruction event and a reference-sampling projector; add explicit `ProgramExitStop` mapping to retained `Terminal(ProgramExit)`. Keep external stops, horizons, invalidity, and errors unchanged.
- Trace module: store structured register snapshots and `RegisterInstructionEvent` records with before/after counter/bank, instruction, operand values, branch, and effects. Repeated reference stutters are labeled non-events. Dense exports are downstream role-aware views.
- Observer module: derive zero-hit checkpoints from positive decrement events, instruction subsequences, logarithmic/binary values, arithmetic recurrence, register-swap transforms, and halt-time statistics without changing execution.
- Migration boundary: leave current Phase-1 dense CA APIs/tests working behind their existing adapter while moving generic execution to typed state/program/outcome protocols. Do not add a register family string, formula function, `Any` payload, `object` ndarray state, or second rollout path.

**Required conformance tests:**

1. Execute the exact five-instruction E06 trajectory through `t18`, checking counter, both values, branch tags, reads, effects, and event timing.
2. Execute the visually decoded simple program and prove its return is an explicit jump; `[i1]` must exit rather than wrap.
3. From the same decrement instruction, old values zero and one must yield respectively unchanged-value fallthrough and decrement+jump. A self-target decrements until zero, then falls through.
4. Check exact `k=2,n=1..8` counts, cumulative counts, exhaustive uniqueness for tiny programs, repeated instructions, and register-swap symmetry without quotienting identity.
5. Execute with operands above `2^63` and `2^100`; assert exact `+1/-1`, no dtype/float conversion, no saturation, and no maximum.
6. Hold register values fixed while changing the counter and prove state/evolution differ; counter must survive snapshot, serialization, trace, batch, and resume boundaries.
7. Reuse one immutable program across multiple arbitrary seeds; separately verify the prepend-increments compiler relation after its setup prefix without equating program identities.
8. Distinguish last valid `Advanced` event, repeated `Quiescent` reference samples, `Terminal(ProgramExit)`, external stop, horizon, invalid program/state, and execution error. Preserve the exact beyond-end counter.
9. Execute the repaired length-eight witness for 1,280 events to `(pc=9,[81,0])` and the 14-instruction square-root program for input ten to `(pc=15,[3,0,0])` after 43 events.
10. Reject negative/non-integral values, wrong bank arity, invalid keys, counter below one, invalid target profile, missing/opaque instructions, stale snapshots, effect mismatches, and partial commits.
11. Reproduce the page-100 zero-hit values and arithmetic recurrence strictly as projections of full events; prove a naive `register == 0` snapshot filter disagrees.
12. Run T09, T12, and T19 through the same generic orchestration/update/outcome entry point with different typed sources/readers/evaluators and no family dispatch or callback delegation.
13. Prove CA unary, two-register prime packing, arithmetic integer packing, and URM encoded initial conditions enter only compiler/relation tests and are rejected by native T19 constructors.
14. Verify no numeric program code is required or synthesized; structured serialization round-trips exactly and program counts remain metadata.

**Completion conditions:**

- Exact naturals, bank, program, counter, source/read, result/effects, update, quiescence, terminal interpretation, trace, and observer contracts are public and fully typed.
- Every successful base instruction uses one generic atomic transition; exhaustion never executes an instruction, wraps, or hides a halt branch.
- Canonical trajectories, counts, halt/square-root witnesses, arbitrary-precision values, and observer projections pass independently.
- Current tests remain passing through an explicit compatibility boundary; no family branch, callback, fixed capacity, object-array substitute, packing, hidden counter, or weakened assertion is introduced.
- Documentation links T19 evidence, both official OCR repairs, structured program identity, target profiles, and every rejection directly to tests.

## No-Cheating Checks

- No `register_machine` rollout family, opcode switch in rollout, whole-program callback, formula rule, `Any` instruction/result, or delegated arbitrary `step(state)`.
- No packing `(pc,registers)` into a scalar, prime exponents, alphabet symbol, CA row, Turing tape, unary region, or URM seed as native representation.
- No NumPy `int64`, float, modulo, saturation, maximum register, padded digits, fixed unary capacity, overflow flag, object-dtype workaround, or truncation.
- No hidden program counter, executor-local loop index, pending branch, prior zero event, mutable program text, or observer-controlled transition.
- No implicit wrap, modulo counter, last-instruction restart, host negative/zero indexing, or exception-as-halt behavior.
- No zero decrement converted to negative arithmetic, unconditional jump, no-op without a counter event, halt, error, or silent clamp.
- No program-end stutter mislabeled as an identity instruction; no optional exit halt conflated with base reference semantics, horizon, external stop, or error.
- No compressed zero-hit history treated as state; no initial/repeated zero snapshot mistaken for “just decreased to zero.”
- No register-swap quotient, invented integer rule code, behavior hash as identity, or seed compiled into the program without explicit provenance.
- No CA/TM/arithmetic/Diophantine/tiling/URM compiler used to claim native conformance; no incomplete Life route cited as proof.

## Completion Requirements

- [x] All direct names, aliases, captions/images, Notes, Index routes, splits, history, variants, duplicates, emulations, and false positives are resolved.
- [x] Register state/domain, instruction pointer, exact instruction forms, reads, effects, branching, seed, successor, program end, and optional halt are reconstructed.
- [x] Counts, program identity, target profiles, canonical trajectories, zero/nonzero/control/overflow/boundary/observer invariants, and independent witnesses are specified.
- [x] Current API/runtime/principles fit and T09/T12 reuse/divergence are explicit.
- [x] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

All 129 direct occurrences on 94 lines, 135 direct/alias occurrences on 95 lines, the complete mechanism, figures, Notes, actual Index and split-file duplicates, instruction/count/seed/end/halting searches, observers, history, native variants, universality routes, compilers, and reductions were dispositioned with zero unresolved native-mechanics candidates and 25 canonical excerpt groups. Two local Notes truncations were repaired narrowly from official primary pages and guarded by main prose, exact counts, and independent execution.

T19 reconstructs a finite named bank over exact naturals plus visible unit-payload program-address control. An immutable ordered program selects one closed instruction and its named operand read; branch-specific results return register assignment and control transition effects for one shared atomic commit. The reference base is total: a counter beyond the program yields an unchanged, event-free `Quiescent(PastProgramEnd)` outcome. A special program-exit halt is an explicit terminal interpretation, never implicit wrap or a hidden instruction. The enumerated profile has `(k(n+1))^n` programs and structured identity but no canonical integer code.

Principle 0 preserves T09/T12 visible control, typed effects, atomic update, structured traces, and outcome distinctions while rejecting their spatial/tape support and finite alphabets. T19 adds exact infinite values, a register bank, code-address source/read responsibilities, closed instruction results, and quiescence without adding another update algebra. Canonical five- and eight-instruction trajectories, page-100 arithmetic checkpoints, exact counts, explicit program-boundary cases, the 1,280-step halt witness, the square-root exit, and values beyond `2^63` close the Goal 2 handoff. CA/TM/arithmetic/URM encodings and compressed observers remain relations only. No prior stage is reopened. Next: T20 Symbolic Systems.

## Integration Results

- Added T19 to the completed construction inventory with finite named numeric state, program-address control, instruction-owned reads, typed arithmetic/control effects, atomic commit, and quiescent/exit outcomes.
- Generalized the control inventory from spatial/tape positions to typed address domains; control need not point into mutable value support.
- Added exact infinite value domains and finite register banks while preserving finite alphabets as a separate member.
- Added program-coupled active-instruction selection and operand access without broadening rule choice to callbacks or arbitrary address functions.
- Reused `Assign`, `TransitionControl`, and `AtomicEffectsUpdate`; no new commit sibling was justified.
- Added `Quiescent` beside advanced/terminal/stop/horizon/error and kept reference sampling separate from semantic instruction events.
- Recorded structured program identity, finite enumeration profiles, general positive exit targets, seed independence, and event-derived observer boundaries.
- Rejected implicit wrap, fixed-width arithmetic, scalar/unary/prime packing, family dispatch, formula evaluation, object-array substitution, hidden counters, observer-defined state, and compiler-as-native implementation.
- T01/T09/T12/T13/T16/T17 remain complete; no public contract changed and no earlier stage reopened.
