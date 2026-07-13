# 4-T12-TURING

Status: **REOPENED — REPRESENTATION ARCHITECTURE AUDIT**

## Current Facts

- Reopening finding: distinct tape-symbol and head-state roles do not require distinct top-level storage classes. A transparent canonical cell alphabet is `Plain(TapeSymbol) | Head(HeadState,TapeSymbol)`, equivalently `TapeSymbol x Option[HeadState]`, with exactly one `Head` cell.
- The head-bearing value must retain both the head state and the tape symbol beneath it. A bare `TapeSymbol union HeadState` is lossy and remains invalid.
- Old-snapshot parallel assignment can atomically write the old head cell and tag the destination; it exposes no intermediate zero-head or two-head state. The compact `Q x Sigma -> Q x Sigma x {L,R}` table remains native program identity rather than an arbitrary composite-alphabet CA table.

- Exact catalog row: T12, CSV line 13, `Turing Machines`; taxonomy seed `ref/notes/CA-Types.md:294-330`.
- Canonical source is `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md` (`BOOK`).
- Native state is a fixed ordered tape-symbol field plus one visible head control record `(position, finite head state)`.
- A base rule is a deterministic total map `Q x Sigma -> Q x Sigma x {-1,+1}`. It reads only head state and the symbol under the head, writes at the old head site, then changes head state and position atomically.
- For `s=|Q|` and `k=|Sigma|`, there are `(2sk)^(sk)` base rules: 4,096 for `(2,2)`, 2,985,984 for `(3,2)` or `(2,3)`, and `2^32` for `(4,2)`.
- The ordinary Chapter 3 family is non-halting. A special terminal head state, an externally observed head/tape condition, and an example-specific stationary transition convention are three distinct later notions of completion.
- Blank tape, initial head state/position, arbitrary/random tape, one-sided computational input, finite observation, and stop policy are separate from the total transition table.
- T12 refines T09's position-only control to payload-bearing `SingleControl` and `TransitionControl`; T09 uses a unit payload and remains semantically unchanged.

## Updated Assumptions

- Tape symbols and head states are distinct finite domains even when their cardinalities happen to match. Equal raw rule counts for `(3,2)` and `(2,3)` do not make their roles interchangeable.
- Head state is carried by the active source passed to the rule, not disguised as a tape symbol or neighborhood value.
- A single payload-bearing control transition atomically changes position and head state. A separate hidden state assignment would permit invalid intermediate control.
- The finite-list `TMStep` guard is an implementation-domain guard, not tape capacity, boundary, or halt semantics. The sparse Notes implementation `a[_]=0` is the clean unbounded blank realization.
- The base table is complete. A missing row is invalid, never an implicit halt or fallback.
- Intrinsic terminal control, episode stop criteria, horizon exhaustion, realization failure, and a fixed point have distinct outcomes/reasons.
- Nondeterministic, two-dimensional, quantum, CA/tag/register emulations, and multicolor-to-binary compilers are variants or relations, not switches inside base T12.

## Big Picture Objective

Exhaustively reconstruct Turing machines and their construction-relevant variants, then extend the T01/T09 source-read-effect-update protocol with finite control payloads, total tape fields, and explicit termination while preserving independent alphabets and rejecting head packing, fixed capacity, callbacks, and family rollouts.

## Catalog Identity

- Stable ID: T12.
- Exact name: Turing Machines; Index abbreviation `TMs` redirects here. No local `a-machine` or `automatic machine` alias occurs.
- Entry kind: fixed-support, single-control deterministic transition construction, with explicitly separated terminal and branching variants.
- Search vocabulary: Turing machine(s), TM/TMs, tape, head/active cell, head state/internal state, symbol/color/cell under head, blank tape/all cells white, read/write, new state/symbol, displacement/move left/right, 2-state/2-color, 4096, 2,985,984/three million, `TMStep`, `TMEvolveList`, rule numbering, head/tape boundary, halt/stop/Busy Beaver, universal/nondeterministic/2D/quantum Turing machines, worms/vants/turmites/turning machines, and CA/tag/register/recursive-function emulations.

## Search Log

### Coverage and method

The taxonomy was read before searching. Case-insensitive fixed/regex searches covered every vocabulary family in the canonical monolith, then every match was inspected in context and relevant Index/cross-references followed.

| Query | Canonical count |
|---|---:|
| `Turing machine` | 416 occurrences on 278 lines: 107 main text, 108 Notes, 63 Index |
| `TM` / `TMs` | 30 occurrences on 24 lines, all Index/navigation |
| `tape` | 23 occurrences on 19 lines |
| `head` | 82 occurrences on 56 lines |
| `state of the head` / `cell under the head` | 8 / 6 |
| `blank tape` / `all cells white` | 9 / 5 |
| `4096` / `2,985,984` / `three million` | 16 / 7 / 1 |
| `halt*` | 139 occurrences on 74 lines; every Turing-colocated or Index-reached hit classified |
| `non-deterministic Turing` / `universal Turing` | 19 / 25 |

Literal `read-write`/`read/write` does not occur; exact read/write behavior is instead explicit in the transition table and `TMStep`. Representative command form was `rg -n -i -e '<variant>' BOOK`, with fixed strings used for exact phrases.

### Candidate disposition

| Region/candidates | Disposition |
|---|---|
| `936-982` | Base construction, parameters, blank seed, and fixed support included; behavior/history prose excluded |
| `2264-2306`, `13660-13678` | 2D Turing machines and aliases redirected to T25 |
| `7938-8174`, `18363-18590`, `18814-18848`, `18916-18938` | CA/TM, multicolor/binary, tag, register, integer, rule-60/110 emulations classified as relations; packing explicitly rejected |
| `8486-8690` | Stationary halt convention, state/color variants, and exact named machines retained; universality behavior otherwise excluded |
| `9166-9368`, `19395` | External completion protocol and nondeterministic branch semantics retained; complexity results excluded |
| `12012-12081` | Entire base Notes implementation, codec/count, blank run, and Busy Beaver halt-state variant audited and included |
| `14275` | Random tape symbols plus definite head start included |
| `14702-15233` | Attractor/entropy/undecidability behavior only |
| `18850-18862` | Symmetry/equivalence, state-vs-color distinction, and initial-condition-sensitive table retained |
| `19231-20115` | Halt distinctions, one-sided experiment, nondeterministic implementation retained; remaining computability discussion excluded |
| Index `20890-22498` | `Tape` at `22154`, `TMs` redirect, and complete Turing entry `22362-22378` followed; no primary evidence |

Targeted variants were fully dispositioned: nondeterministic right-hand-side lists introduce multiway successors (`9320-9324`, `19530-19534`); 2D adds a grid/four moves; `vants`, `turmites`, `turning machines`, and worms name only 2D variants; quantum analogs are quantum-gate networks; reachable-case-only emulation tables do not legalize partial base tables.

### Split/image/source-defect audit

- Matching split Chapters 3/5/9/11/12, Atlas, and malformed BACK-MATTER Notes/Index/Colophon files add no unique passage. Chapter 12's split duplicates the 1D Notes around its lines 3393-3462; the canonical monolith remains authority.
- The page-94 rule image `_page_94_Figure_1.jpeg` was inspected and corroborates the numeric decoder/input ordering for machine 3024.
- `BOOK:12047-12049` is OCR-damaged: the quotient divisor vector displays `{2,2,1}`. That cannot bijectively decode `2sk` outputs for general `k`. Rule count, output roles, known diagrams, and mixed-radix arithmetic uniquely require `{2k,2,1}`. The repaired codec is recorded explicitly rather than executing corrupt text.
- The taxonomy lists output concepts as write/move/next state, while Notes positional triples are next state/write/move. The API uses named fields, so no positional ambiguity remains.

**Search closure:** all 278 direct-name lines, 74 halt lines, parameter/seed/codec candidates, captions, Notes, Index targets, split hits, aliases, named codes, and emulation routes are included, marked duplicate/behavior, or assigned to another construction. Zero T12 evidence candidates remain unresolved.

## Book Excerpts

All excerpts are verbatim from `BOOK`; OCR defects are preserved and explicitly resolved.

### E01 — tape, head, head state, and self-only read

`BOOK:940-948`, Chapter 3, “Turing Machines”:

> Turing machines are similar to mobile automata in that they consist of a line of cells, known as the "tape", together with a single active cell, known as the "head". But unlike in a mobile automaton, the head in a Turing machine can have several possible states
>
> the rule for a Turing machine can depend on the state of the head, and on the color of the cell at the position of the head, but not on the colors of any neighboring cells.

### E02 — state/color counts and blank experimental seed

`BOOK:952-978`, same section:

> there are non-trivial Turing machines that have just two possible states and two possible colors for each cell. ... some of the 4096 machines of this kind.
>
> With three states for the head, there are about three million possible Turing machines.
>
> starting with the head in the first state ... and all cells white.
>
> The Turing machine has four possible states for its head, and two possible colors for each cell on its tape. It starts with all cells white, corresponding to a blank tape.

### E03 — fixed tape organization

`BOOK:982`, adjacent “Substitution Systems” contrast:

> cellular automata, mobile automata and Turing machines ... consist of a fixed array of cells. ... the colors of these cells can be updated ... [but] the underlying number and organization of cells always stays the same.

### E04 — head state is not movement direction

`BOOK:2266-2270`, 2D contrast:

> a Turing machine has a head that at each step moves from one cell to another, updating the color of the cell it leaves according to a definite rule.
>
> the three possible orientations of the arrow on this dot correspond to the three possible states of the head. ... the orientation ... has no direct relationship to directions on the grid—or to which way the head will move at the next step.

### E05 — example-specific stationary halt convention

`BOOK:8494`, universality section:

> one element of the rule can be considered as specifying that the Turing machine should "halt" with the head staying in the same location and same state.

This is a declared convention for that example, not a new base direction or automatic self-loop rule.

### E06 — external head-position completion

`BOOK:9216-9222` and `9248-9252`, computation experiments:

> The head of the machine starts at the right-hand end of this sequence, and the machine runs until its head first goes further to the right—at which point the machine stops
>
> A computation is taken to be complete when the head of the Turing machine goes further to the right than it was at the beginning.
>
> there is no guarantee that a particular Turing machine will ever even complete a computation in a finite number of steps.

Completion here is an episode observation on a one-sided input experiment, not an intrinsic rule output.

### E07 — nondeterministic branching is a different successor algebra

`BOOK:9320-9324`, NP-completeness section:

> a non-deterministic Turing machine has rules that allow multiple choices to be made at each step, leading to multiple possible paths of evolution.

### E08 — exact visible state, transition table, and atomic step

`BOOK:12014-12026`, Notes:

> The state of a Turing machine at a particular step can be represented by the triple  $\{s, list, n\}$ , where s gives the state of the head, list gives the values of the cells, and n specifies the position of the head

```text
{1,0}->{3,1,-1}  {1,1}->{2,0,+1}
{2,0}->{1,1,+1}  {2,1}->{3,1,+1}
{3,0}->{2,1,+1}  {3,1}->{1,0,-1}
```

> the left-hand side in each case gives the state of the head and the value of the cell under the head, and the righthand side consists of a triple giving the new state of the head, the new value of the cell under the head and the displacement of the head.

```text
TMStep[rule_List, {s_, a_List, n_}] /; 1 <= n <= Length[a] :=
  Apply[{#1, ReplacePart[a, #2, n], n + #3}&,
        Replace[{s, a[[n]]}, rule]]
```

The code proves read-old-self, write-old-position, then move/change-control as one returned state. The finite guard supplies no edge behavior.

### E09 — sparse unbounded blank execution

`BOOK:12034-12040`, same Notes:

> The result of t steps of evolution from a blank tape can also be obtained from

```text
s = 1; a[_] = 0; n = 0;
Do[{s, a[n], d} = {s, a[n]} /. rule; n += d, {t}]
```

The default-valued integer field can be written outside any prior finite window.

### E10 — cardinality and numeric codec

`BOOK:12042-12052`, Notes:

> With k possible colors for each cell and s possible states, there are a total of  $(2sk)^{sk}$  possible Turing machine rules.
>
> One can number Turing machines and get their rules using
>
> The examples on page 79 have numbers 3024, 982, 925, 1971, 2506 and 1953.

The evidence-repaired codec is:

```text
B = 2*s*k
digits = padded big-endian base-B digits, length s*k
input order: state 1..s; within state, symbol k-1..0
d -> (1 + floor(d/(2*k)), floor(d/2) mod k, 2*(d mod 2)-1)
```

For `(s,k)=(2,2)`, code `3024` has digits `[5,7,2,0]`, providing a clean known-number conformance fixture.

### E11 — explicit special halt-state variant

`BOOK:12081`, Busy Beaver Notes:

> to find a Turing machine with a specified number of states that "keeps busy" for as many steps as possible before finally reaching a particular "halt state" (numbered 0 below).

### E12 — arbitrary/random tape values retain a definite head

`BOOK:14275`, random-initial-condition Notes:

> In systems like mobile automata and Turing machines the colors of initial cells can be random, but the active cell must start at a definite location, and depending on the behavior only a limited region of initial cells near this location may ever be sampled.

### E13 — head packing is a CA emulation

`BOOK:7938` and `18363-18372`:

> lighter colors in the cellular automaton represent ordinary cells in the Turing machine, while darker colors represent the cell under the head, with a specific darker color corresponding to each possible state of the head.
>
> Given any Turing machine ... a cellular automaton which emulates it can be constructed
>
> If the Turing machine has s states for its head, then the cellular automaton has k(s+1) colors for each cell.

This explicitly identifies extra-color head markers as an encoding, not native T12 state.

### E14 — base machines do not typically halt; emulation tables can be partial only on a trajectory

`BOOK:18812` and `18814-18831`:

> these results concern Turing machines which can halt ...; the Turing machines that I consider do not typically have this feature.
>
> this Turing machine requires only 8 out of the 12 possible cases in its rules to be specified.

The second statement describes a specific rule-110 emulation/reachable trajectory. It does not weaken the base total-table invariant.

### E15 — states and colors remain different roles

`BOOK:18850-18854`, enumeration Notes:

> Of the 4096 s = 2, k = 2 Turing machines ... 560 are distinct after taking account of obvious symmetries and equivalences.
>
> For s = 2, k = 3 machines, the first two numbers are the same, but the final number of distinct cases is 48,505.
>
> The total number of possible Turing machines depends on the product sk. The number of distinct machines that need to be considered increases as k increases for given sk

Equal raw cardinality does not authorize merging tape and control alphabets.

### E16 — halt state versus external criteria

`BOOK:19240`, halting Notes:

> Halting is usually defined by the head of the Turing machine reaching a special halt state. But other criteria can equally well be used-say the head reaching a particular position ... or a certain pattern of colors being formed on the tape.

These become intrinsic terminal control versus episode stop policies with distinct reasons.

## Construction Model

### Base deterministic machine

```text
state = (Line(Z), Tape(default_symbol, overrides),
         SingleControl(key="head", position, payload=head_state))

source = head.position
symbol = tape[source]
(next_state, write, move) = table[(head.payload, symbol)]

next = atomic_apply(state,
  Assign(at=source, value=write),
  TransitionControl(key="head",
                    expected_from=source,
                    to=source+move,
                    next_payload=next_state))
```

| Dimension | T12 semantics |
|---|---|
| Support/state | Fixed ordered integer line + total tape field + exactly one payload-bearing head control. |
| Alphabets | Independent finite `Sigma` for tape and `Q` for running head states. Blank is a distinguished seed/default symbol, not a rule output role. |
| Source/read | `ControlLocus("head")`; rule gets the source control payload and `self_at(0)` symbol only. Neighbor tape changes cannot affect the step. |
| Rule | Complete unique table over `Q x Sigma`; named output fields `(next_state,write,move)`; `move in {-1,+1}` for base family. |
| Result/update | Assign old head site plus payload-bearing control transition, applied atomically; all other symbols preserved. |
| Successor | Exactly one successor for a running base state. No missing-row fallback or branch. |
| Seed | Tape default/overrides, initial head state, and initial head position are episode inputs. Canonical blank is `(default=0,state=1,position=0)`. |
| Boundary | None on `Z`. Finite list guard is a realization error boundary only; read boundaries cannot make writes/head motion unbounded. |
| Trace | Structured tape + head position + head state + terminal status, then explicit observation/ANKoS lowering. |

### Rule/cardinality invariants

- Input rows: `s*k`; legal base outputs per row: `s*k*2`; rule count `(2sk)^(sk)`.
- `(2,2)`: `8^4=4096`; `(3,2)` and `(2,3)`: `12^6=2,985,984`; `(4,2)`: `16^8=2^32`.
- Numeric codec inputs are state ascending and symbol descending; digits are padded big-endian base `2sk`; direction bit 0 is left and 1 is right.
- Constructor validates distinct complete input keys, legal next state/write/move, and the correct domain/codomain. Named fields prevent tuple-order mistakes.

### Exact table and trajectory oracle

Using the E08 table from blank tape with head state 1 at position 0:

```text
t0  q=1 h= 0 ones={}
t1  q=3 h=-1 ones={0}
t2  q=2 h= 0 ones={-1,0}
t3  q=3 h= 1 ones={-1,0}
t4  q=2 h= 2 ones={-1,0,1}
t5  q=1 h= 3 ones={-1,0,1,2}
t6  q=3 h= 2 ones={-1,0,1,2,3}
t7  q=1 h= 1 ones={-1,0,1,3}
t8  q=2 h= 2 ones={-1,0,3}
t9  q=1 h= 3 ones={-1,0,2,3}
t10 q=2 h= 4 ones={-1,0,2}
t11 q=1 h= 5 ones={-1,0,2,4}
t12 q=3 h= 4 ones={-1,0,2,4,5}
```

### Termination model

| Kind | Semantics |
|---|---|
| Base | `Termination.Never`; total table always continues. Horizon returns `HorizonReached`, never `Halted`. |
| Intrinsic terminal variant | Extend visible control payload with terminal set `H` (e.g. state 0); entering it produces a final terminal snapshot with zero successors. Validate its actual codomain/count separately from base. |
| External episode stop | Typed `HeadAt(position)` or `TapeMatches(pattern)` observation; stops the run with a distinct reason without changing rule/state semantics. |
| Stationary example convention | Explicitly declared fixed-point stop predicate for that machine only; never infer halt from any self-loop. |
| Errors | Missing rule, illegal symbol/state/move, and finite-realization edge are errors, not halt. |

### Variant disposition

| Variant | Relation |
|---|---|
| Blank/nonblank/random tape, initial head state/position | Seed/control initialization only |
| One-sided computation/input boundary | Experiment realization plus external stop policy |
| Special halt state | Intrinsic terminal-control variant |
| Nondeterministic TM | Same state/read/effects but multiple outcomes; defer to multiway successor algebra |
| 2D TM | T25 topology/movement construction |
| Multicolor-to-binary, CA/tag/register/integer conversions | Emulations, not primitive reuse |
| Rule-60/110 machines | Named ordinary table/seed fixtures; reachable partial listings are not general partial rules |

## Current API Fit

| Element | Fit | Finding |
|---|---|---|
| Fixed ordered 1D topology | DIRECT conceptually / PRINCIPLED EXTENSION for `Z` | Current rank-1 finite shape (`simple_programs.md:115-198`) remains a realization only |
| Tape alphabet | DIRECT/PARAMETERIZATION | Explicit finite values fit (`:200-230`) |
| Independent head-state domain | PRINCIPLED EXTENSION | Field schema has one alphabet and no control role |
| Visible head `(position,state)` | PRINCIPLED EXTENSION/refinement of T09 | Current state is only `X:D->A` (`:87-113`) |
| Firing source | DIRECT from T09 design | `ControlLocus("head")`; current write-target frontier (`:1412-1510`) remains a documented mismatch |
| Self-only read | DIRECT/PARAMETERIZATION | Current-self selector fits (`:1303` and general relative reads `:360-394`) |
| Product rule input | PRINCIPLED EXTENSION | Explicit product of source payload and self symbol; not a wider neighborhood |
| Exhaustive table | DIRECT conceptually | Table semantics fit (`:1795-1829`) after finite typed product codomain support |
| Atomic result/update | PRINCIPLED refinement | `Assign + TransitionControl(next_payload)` generalizes T09's relocation |
| Seed/field | PARTIAL | Fill/selected values exist (`:235-290`); head start and total sparse field do not |
| Boundary | NOT APPLICABLE natively | Fixed/periodic/reflective finite reads (`:292-358`) are not unbounded head/tape semantics |
| Trace | PRINCIPLED EXTENSION | Must preserve values, position, payload, and termination before lowering |
| Halting/stop reason | PRINCIPLED EXTENSION | No current terminal policy or outcome distinction |

## Current Runtime Fit

- `alphabets.boolean()`/`symbolic()` can represent tape symbols (`src/ca/alphabets.py:129-177`), but `Dynamics` has no alphabet/structured state (`specs.py:23-68`). The module correctly says topology/role are not alphabet semantics (`alphabets.py:25-29`).
- `neighborhoods.self_at(0)` is the correct tape read (`neighborhoods.py:110-137`). T12 must not reuse T09's radius-one read.
- `CoordinateSpace` is finite and gather boundaries only remap/fill reads (`loci.py:31-94,531-614`); they cannot preserve writes/head motion beyond capacity.
- Only `time_slice` is executable and non-full frontiers are rejected (`frontiers.py:54-80`, `rollout.py:825-831`, `tests/test_rollout.py:529-544`).
- `Rule`/`UpdateFn` use `Any` and scalar-return assumptions (`rules.py:30,64-78`); lookup expects alphabet-valued output (`:262-295`), and exhaustive input count ignores product control (`:173-195`).
- Family switches drive rollout/rule application and spatial execution updates a dense full field (`rollout.py:145-212,292-331,576-660`).
- Seeds render only value arrays (`seeds.py:39-55,879-939`). Raw results store one ndarray/dense coords (`specs.py:58-68`, `rollout.py:215-235`), collapsing head position/state/terminal status.
- No current test covers a Turing table, control payload, self-only controlled source, atomic write/move/state change, unbounded sparse tape, or halting distinction.

## Principles Audit

| Principles | T12 result |
|---|---|
| 0-2 | Refine T09 control to payload-bearing form; do not add a Turing executor. |
| 3-4 | Frontier=head source; neighborhood=self tape read; rule=typed table result; update=assignment plus atomic control transition; termination remains explicit. |
| 5 | Head state/position and tape default/overrides are visible Markov state. |
| 6-8,12 | Integer topology, sparse total field, work window, structured trace, and canonical encoding stay separate. |
| 9 | `Q`, `Sigma`, moves, table domain/codomain/count are coupled; machine rule and initial tape/head remain independent. |
| 10 | A Turing preset returns the ordinary shared spec. |
| 11 | Total/non-halting schedule or terminal policy is defining; numeric codec, emulation, compression, batching, external stop observation are separate. |
| 13-15 | Neighbor independence, different head payloads, beyond-window moves, exact trajectory, and halt/error/stop distinctions are mandatory adversarial tests. |
| 16 | Payload control/termination are architecture; extra-color packing, callbacks, family switches, partial fallbacks, and implicit edge halts are shims. |

## Detailed Implementation Plan

1. Refine `SingleActive/RelocateControl` to payload-bearing `SingleControl/TransitionControl`; migrate T09 to unit payload without behavior change.
2. Add an inspectable total/default tape field over `Line(Z)`; keep work/observation extents separate.
3. Compose a rule input from active-source payload and `self_at(0)`, and validate a complete unique product table.
4. Apply source assignment and payload/position transition atomically; preserve untouched tape values.
5. Add explicit `Never`/terminal-control termination and typed episode stop reasons; never infer halt from errors/horizon/self-loop.
6. Preserve structured tape/control/terminal snapshots before trace encoding and observations.
7. Expose strict table/numeric presets over the generic executor and add independent oracles.

## Goal 2 Implementation Stage

### G2-T12 — Payload control, total tapes, termination, and Turing conformance

**Dependencies:** G2-T01 generic fixed-line assignment/support/realization; G2-T09 source frontiers, structured control, compound atomic effects, structured traces. T12 refines position-only control, so implement the payload-bearing form once and use unit payload for T09.

**Implementation areas:**

- Synthesis-selected state/support module: `Line(Z)`, inspectable `Tape(default_symbol,overrides)`, and `SingleControl(key,position,payload,domain)`.
- Typed effects/update: `TransitionControl(key,expected_from,to,next_payload)` plus `Assign`; atomic validation/application. Replace provisional position-only relocation.
- `frontiers.py`: reuse `ControlLocus("head")`; `neighborhoods.py`: reuse `self_at(0)`.
- `rules.py`: product-key exhaustive tables and finite typed result codecs; strict complete coverage and `(2sk)^(sk)` base cardinality; evidence-repaired numeric codec guarded by known IDs/images.
- Generic executor: pass source control record plus gathered self value to the table and apply effects without a family branch.
- `specs.py`/preset index: `turing(states,symbols,table|number)` returns the ordinary spec. Rule/machine signature stays separate from initial tape/head.
- Explicit termination layer: `Never`, terminal-control-state predicate, and distinct episode stop policies/reasons. Retain one final terminal snapshot; do not pad it as repeated execution.
- Structured raw trace/encoding for tape, head position/state, terminal flag; value coordinates remain a downstream view.
- New `tests/test_t12_turing.py` plus shared control/effect/termination/tape tests.

**Canonical tests:**

1. Assert all six E08 rows and the exact `t0..t12` sparse trajectory.
2. Exhaust all 4,096 `(2,2)` numeric tables: uniqueness, four input pairs, eight legal results, round-trip; check code 3024 digits `[5,7,2,0]`.
3. Assert `(2sk)^(sk)` at `(2,2)`, `(3,2)`, `(2,3)`, `(4,2)`; reject partial/duplicate/illegal tables and out-of-range numbers.
4. Neighbor independence: change `head±1` only and require identical transition. Head-state dependence: same tape/position, different payload selects different rows and remains distinct.
5. Assert old head cell write, one position move, payload transition, unchanged destination/other tape, and atomicity.
6. Move/write beyond every initial window on blank `Z` with no wrap/reflect/truncate/pad/implicit halt.
7. Reuse one machine spec with blank/nonblank tapes and different initial head states/positions.
8. Round-trip structured snapshots differing only in position, head payload, or terminal state.
9. Base horizon returns `HorizonReached`, never `Halted`.
10. Halt-state variant enters visible terminal 0, keeps the final snapshot once, has zero successors, and reports intrinsic halt; validate its non-base cardinality separately.
11. `HeadAt`/tape-pattern/fixed-point stop reports a distinct external reason and does not alter dynamics; missing row/edge errors never halt.
12. Run T01/T09/T12 through the same executor and statically reject family switches, head packing, hidden state, and callbacks.

**Completion evidence:** all canonical/independent tests and existing suite pass; no Turing branch/packing/hidden control; base numeric/table count round-trips; terminal and external-stop reasons remain distinct; unbounded tape and structured trace are inspectable.

## No-Cheating Checks

- No head position/state packed into tape color, executor locals, closure, metadata, or visualization.
- No Turing family branch/dedicated rollout/callback.
- No radius-one T09 read; T12 reads self only plus explicit control payload.
- No partial-table/missing-row fallback or nondeterministic branch inside deterministic result.
- No finite capacity or read boundary presented as tape semantics; no implicit edge halt.
- No conflation of blank default with fixed read boundary.
- No implicit halt from horizon, self-loop, fixed point, missing rule, stay move, display exit, or error.
- No terminal padding, value-only trace, self-parity-only oracle, or weakened tests.

## Completion Requirements

- [x] All aliases, captions, Notes, Index entries, parameters, cross-references, duplicates, and false positives are resolved.
- [x] All unique construction-relevant excerpts have exact canonical provenance.
- [x] Tape, symbol/head alphabets, visible control, read/result/update, support/boundary, seed, successor, and halting are reconstructed.
- [x] Rule cardinalities, numeric codec, and canonical examples have independent conformance oracles.
- [ ] Current API/runtime/test fit and T09 refinement are reclassified without presuming `SingleControl`/`TransitionControl` storage.
- [ ] Goal 2 handoff and global reintegration are revised around the lossless composite representation and invariant.

## Stage Results

**Reopened:** the Turing evidence, compact transition table, counts, tape semantics, and halt distinctions remain valid, but the required `SingleControl`/`TransitionControl` architecture and prohibition on transparent head packing are withdrawn pending `architecture-audit.md`.

T12 is complete with zero unresolved evidence candidates. Its base family is a total non-halting `Q x Sigma -> Q x Sigma x {L,R}` transition on an unbounded default-symbol tape. It refines T09's control to `SingleControl(position,payload)` and `TransitionControl(...,next_payload)`, with T09 represented by a unit payload and no behavior change. Special terminal head states are an explicit variant; external head/tape/fixed-point criteria remain episode stop policies, and horizon/errors are neither. The OCR-damaged numeric codec is repaired transparently and guarded by known rule 3024. Nondeterministic, 2D, and emulation variants remain distinct. No prior completed stage is reopened. Next: T13 Neighbor-Independent Substitution Systems.
