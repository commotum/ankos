# 8-T19-REGISTER

Status: **IN PROGRESS**

## Current Facts

- Exact catalog row: T19, CSV line 20, `Register Machines`; taxonomy seed `ref/notes/CA-Types.md:495-522`.
- The taxonomy hypothesis is a finite ordered instruction program over a finite tuple of unbounded non-negative registers plus a visible instruction pointer. The canonical book evidence must settle exact instruction forms, instruction-pointer timing, fallthrough/wrap behavior, zero-decrement behavior, seed, program enumeration, and any intrinsic halt.
- T09/T12 already establish visible payload-bearing control and atomic value/control transitions, but their support is a lattice/tape and their control selects a spatial source. T19 may reuse typed control/effects/outcomes only if a program address plus named register access composes without pretending registers are cells.
- Register identity, numeric domain, active instruction, exact read set, increment/decrement-jump result, zero branch, program-end behavior, initial conditions, trace observers, extended instructions, universal variants, and halting extensions remain under audit.

## Updated Assumptions

- The instruction pointer is semantically visible Markov state, never an executor loop counter or a color packed into a register.
- A register is a named slot containing an unbounded non-negative integer. Fixed-width overflow, saturation, wraparound, tensor capacity, and unary cell encodings are not native unless canonical evidence says otherwise.
- Program text is immutable episode-independent data unless a documented variant explicitly mutates it.
- Increment and decrement-jump must return typed numeric/control effects atomically; a whole-machine callback or formula rule would erase the construction.
- Program end, explicit halt instructions, unreachable/invalid instruction pointers, external horizons, and repeated states must remain distinct until evidence resolves them.

## Big Picture Objective

Exhaustively reconstruct the canonical register-machine instruction cycle, numeric state, conditional control flow, enumeration, seeds, observers, and variants. Determine whether T09/T12's visible single-control and atomic typed-effect protocol extends cleanly to program-address control plus named unbounded registers, without family dispatch, opaque instruction callbacks, fixed-width arithmetic, or Turing/CA compilation.

## Catalog Identity

- Stable ID: T19.
- Exact name: Register Machines.
- Entry kind: unresolved pending evidence; expected deterministic finite-program numeric state machine.
- Search vocabulary: register machine, register, counter machine, Minsky machine, unlimited/universal register machine/URM, increment, decrement, decrement-jump, jump, instruction pointer/program counter, program/instruction number, zero/negative/fall through/next instruction, first/end/beginning/wrap, halt/stop, two/three/many registers, instruction count/program count/enumeration, initial condition, compressed evolution, zero event, 3n+1/Collatz relation, emulation/universality, state-transition graph, low-level language, and exact Notes implementation symbols.

## Search Log

In progress. Independent canonical core, Notes/Index/split/history/variant, and Principle-0/runtime-fit audits are running.

## Book Excerpts

In progress.

## Construction Model

Pending evidence closure. Working hypothesis, not a conclusion:

```text
state = (nonnegative register tuple, instruction pointer)
instruction = program[instruction_pointer]

increment(r):
    register[r] += 1
    instruction_pointer = next instruction

decrement_jump(r,target):
    if register[r] > 0:
        register[r] -= 1
        instruction_pointer = target
    else:
        register[r] remains 0
        instruction_pointer = next instruction
```

Canonical wrap, halting, exact instruction encoding/count, and whether the read of a decrement instruction is a rule input or update precondition remain to be established.

## Current API Fit

Pending evidence reconstruction. Expected direct responsibility reuse is finite numeric value/control program separation; expected mismatches are dense spatial support, coordinate neighborhoods, writable-target frontiers, scalar same-site rules, and fixed-shape trace assumptions.

## Current Runtime Fit

Pending full audit. Current `src/ca` has no typed named-register bank, instruction-address source, instruction algebra, unbounded-natural effect, conditional decrement result, or structured program/control trace.

## Principles Audit

Pending evidence closure. Principle 0 must determine whether T12 `SingleControl` can address a program rather than a spatial field, and whether atomic effects need an explicit conditional numeric sibling rather than hidden rule branching. No family rollout, instruction callback, packed machine integer, fixed-width overflow, unary CA/TM compiler, or hidden instruction pointer is accepted.

## Detailed Implementation Plan

1. Close direct, alias, caption, Notes, Index, split, history, instruction, numbering/count, seed, halt, observer, extended-variant, and emulation searches.
2. Reconstruct registers/identity/domain, program/control, active source, reads, instruction inputs/results, atomic commit, successor, program-end/halting behavior, seed, parameters, variants, and observables.
3. Compare T19 with T09/T12 and rederive control/source/effect responsibilities wherever spatial position, tape reads, or movement do not compose.
4. Specify exact canonical trajectories, program-count/codec guards, zero/nonzero branch, wrap/end/halt, overflow, provenance, and shared-executor tests.
5. Write the implementation-ready Goal 2 stage, reintegrate all ledgers, verify, and advance.

## Goal 2 Implementation Stage

Pending evidence closure and fit audit.

## No-Cheating Checks

- No register-family rollout, whole-program callback, formula escape hatch, or `Any` instruction/effect.
- No packing registers and instruction pointer into one integer, alphabet symbol, tape, CA row, or Turing-machine encoding.
- No fixed integer width, overflow, saturation, modulo, maximum register value, unary capacity, padding, or truncation as native arithmetic.
- No hidden instruction pointer, implicit mutable program, host-language exception control flow, or observer-dependent branching.
- No zero decrement turned into negative arithmetic, unconditional jump, halt, error, or silent clamp without evidence.
- No program-end wrap or halt inferred from host array behavior; canonical semantics must decide it.

## Completion Requirements

- [ ] All aliases, captions, Notes, Index entries, splits, variants, duplicates, and false positives are resolved.
- [ ] Register state, instruction pointer, exact instruction forms, reads, effects, branching, seed, successor, program-end, and halting semantics are reconstructed.
- [ ] Exact trajectories and adversarial zero/nonzero/control/overflow/program-boundary invariants have independent tests.
- [ ] Current API/runtime/principles fit and T09/T12 reuse/divergence are explicit.
- [ ] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Stage Results

In progress. No T19 architectural conclusion is complete.
