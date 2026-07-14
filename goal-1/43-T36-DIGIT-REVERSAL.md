# 43-T36-DIGIT-REVERSAL

Status: **IN PROGRESS — FIRST-PRINCIPLES CONSTRUCTION RECONSTRUCTED; SOURCE/ASSET/SEMANTIC ORACLES PENDING**

## Current Facts

- T36 is CSV physical line 37, `Digit-Reversal Arithmetic Systems`; `ref/notes/CA-Types.md` section 36 is search vocabulary, not primary evidence.
- The strict main rule keeps one positive integer: write its canonical base-2 digits in reverse order, interpret that reversed word as an integer, and add it to the old integer (`BOOK:1543-1553`). Seed 16 yields the page-125 pattern; seed 512 yields the page-126 million-step nonrepeating observation.
- The Notes state the operation as `n -> n + FromDigits[Reverse[IntegerDigits[n,2]],2]`, despite extraction damage that inserts spaces into `FromDigits` and `IntegerDigits` (`BOOK:12635-12643`).
- Strict T36 therefore has a discrete `t+0D` exact-integer configuration. The canonical digit word is a lossless, rule-visible presentation of that integer, not automatically a second native state or a `t+1D` lattice.
- Base choice is semantically required because digit reversal depends on positional representation. The strict source fixes base 2; the History note mentions similar base-10 systems, while arbitrary `b >= 2` remains an explicit validated generalization. Base is program data, not DOMAIN, configuration topology, or hidden executor dispatch.
- Canonical integer digits omit leading zeros. Reversal may place zeros on the left of the reversed word, but decoding erases them without losing strict state because the rule immediately returns to an integer.
- The reversed intermediate is a general finite base-valid word, not a canonical state word: binary `10` reverses to `01`. Canonicalizing before decoding would change the witness and can corrupt width-sensitive profiles.
- The Notes separately describe a fixed-width variant that drops left carries and a growing-width variant that adds one new left digit every event even when it is zero (`BOOK:12643`). These profiles make width/leading zeros semantic and must be separately tagged.
- T34 already owns the arbitrary-precision exact integer carrier, positional codecs, discrete `t+0D` singleton, `UniqueScalar` frontier, self read, same-locus assignment, atomic UPDATE, traces, and common outcomes.
- T35 confirms that a closed rule schema over that scalar event does not justify a construction-named state, assignment, UPDATE, executor, or rollout branch. T36 adds closed positional codec/transform expression nodes and explicit width policies.
- T43's former statement that “digits are the evolving finite word” overstates the strict source. A finite word is a lossless canonical representation of strict state; only profiles whose width or leading zeros affect later events require the word or an equivalent `(value,width)` product in complete configuration.
- Strict positive evolution is strictly increasing, so it has no scalar fixed points or cycles. The Notes' “effective period of 4” describes visible digit-pattern organization, not native configuration equality or halting.

## Updated Assumptions

- **Retained:** strict state is a positive arbitrary-precision integer and strict base is 2. Zero, arbitrary `b >= 2`, and any broader carrier are explicit extensions requiring separate validation and identity.
- **Retained:** strict encoding uses the unique canonical base-2 word with no leading zeros. A generalized codec declares `b >= 2` and an explicit `[0]` convention for an admitted zero extension.
- **Retained:** `ReverseDigits` is a closed structural RULE node composed with exact `EncodeDigits`, `DecodeDigits`, and `Add`, never an unrestricted callback.
- **Retained:** every claimed scalar/word equivalence must preserve the complete old state, exact successor, event count, outcomes, and trace one event at a time.
- **Retained:** fixed width can remain immutable program data when it never changes; growing width must be visible in configuration or in a lossless word representation because equal integers with different widths can have different successors.
- **Retained:** base/profile/width belong to exact structural program identity. Base is not a rendering choice: `F_2(12)=15` while `F_10(12)=33`.
- **Rejected:** a T36 executor, digit-lattice CA branch, implicit machine width, implicit leading-zero preservation, digit observer fed back through hidden state, NumPy overflow, float decoding, host callback transform, or a generic “digit_transform” string with invented rotate/complement/sort semantics.

## Big Picture Objective

Reconstruct T36 from primary evidence as a closed positional-representation unary RULE over the shared scalar SimpleProgram event. Exhaustively close the strict reversal-add system, source trajectories and long-run qualifications, canonical codec, exact base/leading-zero semantics, fixed-width and growing-width Notes variants, observers, assets, Notes/Index/splits/history, arithmetic/FFT/quasi-Monte-Carlo relations, arbitrary-precision runtime fit, representation commutations, and Goal 2 handoff. Add a new semantic component only if a concrete one-step counterexample defeats the smallest reusable base.

## Catalog Identity

- Stable ID: T36.
- Exact CSV name: Digit-Reversal Arithmetic Systems.
- CSV physical line: 37.
- Taxonomy section: 36.
- Canonical main core: `BOOK:1543-1553` plus continuation at `BOOK:1551-1553`.
- Native Notes core: `BOOK:12637-12643`.
- Entry kind: deterministic exact unary integer transition whose closed RULE explicitly factors through a positional digit codec.
- Strict DOMAIN: discrete `t+0D`.

## Initial Construction Model

The reusable generalized profile below declares `b >= 2`; strict T36 instantiates `b=2` and a positive carrier:

```text
CanonicalDigits_b : NonnegativeInteger <-> CanonicalDigitWord_b
reverse_b(n)      = Decode_b(Reverse(CanonicalDigits_b(n)))
F_b(n)            = n + reverse_b(n)

active = UniqueScalar.select(configuration)
n      = Self.read(configuration, active)
writes = Assign(active, F_b(n))
next   = AtomicAssign.apply(configuration, active, writes)
```

The generalized codec is bijective between nonnegative integers and canonical words (`[0]` for zero; otherwise first digit nonzero). `Reverse` need not remain inside the canonical-word image, so decoding accepts a finite base-valid word with leading zeros. The composite still denotes a total exact scalar map; strict conformance exercises its positive base-2 restriction.

On canonical words, `H_b(w) = EncodeCanonical_b(Decode_b(w) + Decode_b(Reverse(w)))` gives the exact one-step commuting square `H_b(EncodeCanonical_b(n)) = EncodeCanonical_b(F_b(n))`. Thus canonical scalar and word configurations are class-3 lossless representations on the invariant-valid image, not different constructions.

The fixed-width Notes sibling declares immutable width `m`, stores `0 <= n < b^m`, encodes exactly `m` digits, and drops left carry after addition:

```text
F_fixed(b,m)(n) = (n + Decode_b(Reverse(Encode_b(n,width=m)))) mod b^m
```

The growing-width sibling must retain width:

```text
configuration = (n,m), 0 <= n < b^m
F_grow(b)(n,m) = (n + Decode_b(Reverse(Encode_b(n,width=m))), m+1)
```

This formulation is a hypothesis to verify against complete Notes mechanics. A width-preserving digit word is an equivalent class-3 representation when the inverse `(word -> value,width)` and one-step commutation are explicit.

Erasing width is not lossless: base-2 words `1` and `01` both decode to numeric value 1, but grow-width reversal-add sends them to `10` (value 2) and `011` (value 3), respectively. Deriving width from hidden event time or seed provenance would make resumed configuration incomplete. Strict and fixed-width profiles also diverge concretely at `b=2,m=1,n=1`: strict yields 2, while fixed-width carry dropping yields 0.

## Architecture Fit Hypothesis

| Responsibility | Provisional class | Smallest reusable construction | T36 delta to test |
|---|---:|---|---|
| DOMAIN/configuration | 1/2/3 | T34 exact discrete `t+0D` singleton | Strict positive carrier/base 2; zero/general-base siblings explicit; optional width product only where width is semantic |
| FRONTIER/read | 1 | T34 `UniqueScalar` plus self read | No T36 selector or neighborhood |
| RULE syntax | 2 | D069 closed unary RULE algebra | Typed positional encode/reverse/decode/add nodes and explicit base/width policy |
| Write/UPDATE | 1 | T34 same-locus assignment and atomic UPDATE | No T36 assignment or UPDATE |
| Canonical digit-word view | 3 | Exact integer/digit codec | Bijection and event/trace commutation, not a new executor |
| Fixed/growing width | 2/3 | Explicit program parameter or product/tagged configuration | Preserve leading zeros and carry policy without hidden time or storage width |
| Outcomes/traces | 1 | Common `StepResult` and scalar trace | Fixed points/cycles advance unless source says otherwise |

No current evidence requires a genuinely different execution algebra. The likely Goal 2 delta is closed positional-expression data and invariants inside the shared unary RULE implementation.

## Evidence and Oracle Work Plan

1. Build a redundant source-query union covering reversal-add, reverse/digit/base/leading-zero/carry terms, main captions, Notes, Index, history, positional codecs, FFT/digit-reversal sequences, and false-positive mathematical digit reversal.
2. Reverse-close every monolith hit and retained continuation to structural split owners; bind every referenced image by exact path/size/SHA and disposition it as native, relation, control, or exclusion.
3. Reproduce source-pinned prefixes for seeds 16 and 512, digit lengths, canonical encoding, and any exact checkpoints recoverable from text or governed rasters without inventing pixel semantics.
4. Exhaustively commute direct scalar events with the generic unary runner across bases, leading/trailing-zero cases, arbitrary-precision values, fixed-width/drop-carry cases, and growing-width product/word representations.
5. Prove the information-loss counterexample for erasing semantic width: two configurations with equal numeric value but different preserved widths can reverse to different decoded values.
6. Reject malformed digits, base below two, negative values without a declared sign codec, overflow/truncation outside the fixed-width profile, forged witnesses, cross-program events, callbacks, implicit host-width behavior, and digest-only identity.
7. Audit `simple_programs.md`, `src/ca`, tests, T34/T35/T43, the design ledger, and Goal 2 handoffs before proposing any new type.

## Goal 2 Handoff Hypothesis

- Extend the shared closed unary expression algebra with versioned positional nodes such as `EncodeDigits(base,width_policy)`, `ReverseWord`, `DecodeDigits(base)`, and exact arithmetic composition.
- Add canonical and fixed-width digit codecs with validation, structural identity, arbitrary-precision serialization, and replayable digit-transform witnesses.
- Add explicit strict, fixed-width/drop-carry, and growing-width presets only after primary evidence closes their semantics.
- Reuse the T34 event, assignment, UPDATE, outcomes, and trace envelope through the branch-free runner.
- Add conformance tests for exact Book prefixes, base/zero/leading-zero cases, arbitrary precision, word/scalar commuting maps, width-loss counterexamples, and no family dispatch.
- Add no `DigitReversalState` for strict scalar execution, T36 executor, digit-CA compiler path, host transform callback, fixed machine width, hidden width/time, observer feedback, or source-unsupported transform menu.

## No-Cheating Checks

- No whole program hidden in a callback or generic formula evaluator.
- No base, width, sign, leading-zero, or carry behavior inferred from host integer/string conventions.
- No digit word called native strict state unless its canonical bijection and step commutation are explicit.
- No scalar-only representation used for a width-sensitive profile when equal values at different widths have different futures.
- No finite-width truncation applied to strict arbitrary-precision evolution.
- No FFT/Halton/van-der-Corput digit permutation sequence presented as native reversal-add feedback without a complete commuting map.
- No raster-derived rule, seed, trace, or numeric checkpoint without an explicit transcription boundary.

## Completion Requirements

- [ ] Every direct/alias/mechanics search, Notes item, actual Index route, continuation, split witness, image link, and false positive is dispositioned with zero unresolved mechanics.
- [ ] Strict formula, carrier, base, canonical digit convention, seeds, exact prefixes, events, and empirical qualifications are closed.
- [ ] Fixed-width/drop-carry and growing-width profiles have exact typed state/program boundaries and no hidden leading-zero semantics.
- [ ] Scalar/word and width-product representations commute losslessly where claimed; information-loss counterexamples block false collapse.
- [ ] Source, asset, semantic, runtime-fit, hostile, portability, fail-closed, tests, mode, Markdown, diff, and scope gates pass.
- [ ] D137, plan, evidence index, design ledger, architecture audit, and Goal 2 handoff are synchronized without a T36 executor.

## Stage Results

In progress. The primary strict construction and the representation boundary are reconstructed; exhaustive source, asset, semantic, runtime, integration, and hostile-review closure remain pending.
