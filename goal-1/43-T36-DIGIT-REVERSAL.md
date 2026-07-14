# 43-T36-DIGIT-REVERSAL

Status: **IN PROGRESS — FIRST-PRINCIPLES CONSTRUCTION RECONSTRUCTED; SOURCE/ASSET/SEMANTIC ORACLES PENDING**

## Current Facts

- T36 is CSV physical line 37, `Digit-Reversal Arithmetic Systems`; `ref/notes/CA-Types.md` section 36 is search vocabulary, not primary evidence.
- The strict main rule keeps one nonnegative integer: write its canonical base-2 digits in reverse order, interpret that reversed word as an integer, and add it to the old integer (`BOOK:1497`, `BOOK:12503`, `BOOK:1543-1553`, `BOOK:12635-12643`). Seed 16 yields the page-125 pattern; seed 512 yields the page-126 million-step nonrepeating observation. The showcased positive seeds do not impose a positive-only carrier.
- The Notes state the operation as `n -> n + FromDigits[Reverse[IntegerDigits[n,2]],2]`, despite extraction damage that inserts spaces into `FromDigits` and `IntegerDigits` (`BOOK:12635-12643`).
- Strict T36 therefore has a discrete `t+0D` exact-integer configuration. The canonical digit word is a lossless, rule-visible presentation of that integer, not automatically a second native state or a `t+1D` lattice.
- Base choice is semantically required because digit reversal depends on positional representation. The strict source fixes base 2; the History note mentions similar base-10 systems, while arbitrary `b >= 2` remains an explicit validated generalization. Base is program data, not DOMAIN, configuration topology, or hidden executor dispatch.
- Canonical integer digits omit leading zeros. Reversal may place zeros on the left of the reversed word, but decoding erases them without losing strict state because the rule immediately returns to an integer.
- The reversed intermediate is a general finite base-valid word, not a canonical state word: binary `10` reverses to `01`. Canonicalizing before decoding would change the witness and can corrupt width-sensitive profiles.
- The Notes separately describe a fixed-width variant that drops left carries and a growing-width variant that adds one new left digit every event even when it is zero (`BOOK:12643`). These profiles make width/leading zeros semantic and must be separately tagged.
- T34 already owns the arbitrary-precision exact integer carrier, positional codecs, discrete `t+0D` singleton, `UniqueScalar` frontier, self read, same-locus assignment, atomic UPDATE, traces, and common outcomes.
- T35 confirms that a closed rule schema over that scalar event does not justify a construction-named state, assignment, UPDATE, executor, or rollout branch. T36 adds closed positional codec/transform expression nodes and explicit width policies.
- T43's former statement that “digits are the evolving finite word” overstates the strict source. A finite word is a lossless canonical representation of strict state; only profiles whose width or leading zeros affect later events require the word or an equivalent `(value,width)` product in complete configuration.
- Zero is the native canonical word `[0]` and performs the ordinary event `0 -> 0`; it is a fixed point, not a halt. Every positive strict state is strictly increasing, so the positive subset has no fixed points or cycles. The Notes' “effective period of 4” describes visible digit-pattern organization, not native configuration equality or halting.

## Updated Assumptions

- **Retained:** strict state is a nonnegative arbitrary-precision integer and strict base is 2. Arbitrary `b >= 2`, signed values, and any broader carrier are explicit extensions requiring separate validation and identity.
- **Retained:** strict encoding uses the unique canonical base-2 word: `[0]` for zero and otherwise no leading zeros. A generalized codec declares `b >= 2` and retains the same explicit zero convention.
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

## Primary-Source and Asset Closure

The fail-closed source oracle uses 18 independent query lanes. Their union contains 124 monolith rows: 98 before the physical Index and 26 actual-Index candidates. The Index boundary is exact: 12 rows are routed T36 aliases/relations and 14 are guarded flattened-column or recursive-sequence collisions. The complete governed partition is 19 native, 19 relation, and 30 control rows (68 retained), with 48 explicit exclusions and zero unresolved rows.

The retained evidence reverse-joins to 94 unique split-corpus owners:

| Join class | Rows | Boundary |
|---|---:|---|
| Exact text | 71 | Byte-normalized text agrees exactly |
| Image basename | 15 | Monolith and split rows name the same opaque asset |
| Normalized text | 4 | Minimum score `0.996587`; no low-score fuzzy acceptance |
| Structural OCR repair | 4 | Exact owner plus frozen damaged and repaired needles |

The four structural repairs cover the extracted `FromDigits`/`IntegerDigits` spacing damage and the `dyadic`/`Paley`/`BitReverseOrder` corruption. Actual-Index routes, neighboring-column sentinels, exclusions, query contracts, and repair witnesses have separately frozen records; clearing or weakening them fails the oracle.

The evidence roles are:

| Role | Primary evidence | Semantic boundary |
|---|---|---|
| Native scalar rule and observations | `BOOK:1497`, `1543-1553`, `12503`, `12635-12645` | Nonnegative exact scalar, base-2 canonical codec, seeds 16/512, empirical growth/periodicity qualifications, fixed/growing-width variants |
| Positional relations | `BOOK:8838`, `12646-12658`, `17313-17356`, `17611`, `20738` | Fixed-width digit-reversal permutation, FFT/Walsh reorderings, van-der-Corput/quasi-Monte-Carlo relations; not reversal-add state evolution |
| Controls | T35/T37 neighbors, digit codecs, Turing-counter displays, recursive/bitwise/run-length sequences, and `BOOK:12974` | Establish boundaries and confirm that the Book's “whole number” usage includes zero; do not add T36 mechanics |

The asset boundary contains exactly seven governed files at `4 native / 3 relation / 0 control` and nine excluded neighbor files. The governed set has 14 monolith/split references, seven distinct hashes, 1,062,053 bytes, and two assemblies across five grouped files. The exclusions have 18 references, nine hashes, 170,822 bytes, and one assembly across five grouped files. All seven governed assets are hash-bound; none is pixel-transcribed or pixel-replayed. Consequently the numeric prefixes below are independently computed from the source-pinned formula and seeds, not claimed as raster transcriptions.

## Initial Construction Model

The reusable generalized profile below declares `b >= 2`; strict T36 instantiates `b=2` and the nonnegative carrier:

```text
CanonicalDigits_b : NonnegativeInteger <-> CanonicalDigitWord_b
reverse_b(n)      = Decode_b(Reverse(CanonicalDigits_b(n)))
F_b(n)            = n + reverse_b(n)

active = UniqueScalar.select(configuration)
n      = Self.read(configuration, active)
writes = Assign(active, F_b(n))
next   = AtomicAssign.apply(configuration, active, writes)
```

The generalized codec is bijective between nonnegative integers and canonical words (`[0]` for zero; otherwise first digit nonzero). `Reverse` need not remain inside the canonical-word image, so decoding accepts a finite base-valid word with leading zeros. The composite still denotes a total exact scalar map; strict conformance exercises its nonnegative base-2 restriction.

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
| DOMAIN/configuration | 1/2/3 | T34 exact discrete `t+0D` singleton | Strict nonnegative carrier/base 2; general-base and signed siblings explicit; optional width product only where width is semantic |
| FRONTIER/read | 1 | T34 `UniqueScalar` plus self read | No T36 selector or neighborhood |
| RULE syntax | 2 | D069 closed unary RULE algebra | Typed positional encode/reverse/decode/add nodes and explicit base/width policy |
| Write/UPDATE | 1 | T34 same-locus assignment and atomic UPDATE | No T36 assignment or UPDATE |
| Canonical digit-word view | 3 | Exact integer/digit codec | Bijection and event/trace commutation, not a new executor |
| Fixed/growing width | 2/3 | Explicit program parameter or product/tagged configuration | Preserve leading zeros and carry policy without hidden time or storage width |
| Outcomes/traces | 1 | Common `StepResult` and scalar trace | Fixed points/cycles advance unless source says otherwise |

No current evidence requires a genuinely different execution algebra. The likely Goal 2 delta is closed positional-expression data and invariants inside the shared unary RULE implementation.

## Current Runtime Fit

The current modules already expose the right SimpleProgram responsibilities, but not yet the exact T36 value/rule schemas. T36 therefore needs small shared-axis additions, not a catalog executor.

| Responsibility | Current `src/ca` mechanism | T36 disposition |
|---|---|---|
| DOMAIN/locus | Rank-zero `t+0d` shape plus the time-slice frontier | Reuse the one-locus responsibility as `UniqueScalar`; base and digit width are not DOMAIN axes |
| ALPHABET/value | `alphabets.py:40-85` admits finite enumerated `int/float/str` ranges | Reuse T34's planned arbitrary-precision nonnegative integer value; add a transparent product/tagged value only for growing width. Do not enumerate an unbounded alphabet or use object-array packing |
| FRONTIER | Current time-slice selection | Restrict to the unique scalar locus; no T36 frontier type |
| NEIGHBORHOOD | `neighborhoods.py:110-137` provides current self access | Direct responsibility-level reuse; no digit stencil or temporal history |
| RULE | `rules.py:65-78,316-328` stores family strings and an unrestricted callable | Add closed positional nodes to D069's shared unary RULE algebra; never use `formulaic`, a transform callback, or an operation-name switch |
| UPDATE | One rule result becomes the next value | Reuse generic same-locus atomic assignment. Fixed carry dropping and growing-width construction are RULE-result semantics, not UPDATE laws |
| Runner | `rollout.py:145-212,292-331` dispatches on named families | Replace with the shared structural runner in Goal 2; adding `if family == "digit_reversal"` would be a regression |
| Seeds/traces | Pair/history seeds and fixed NumPy `RawEpisode.states` (`seeds.py:136-178`, `specs.py:58-81`) | Use one exact scalar seed and `h` events/`h+1` exact states; fixed dtypes cannot preserve the million-step or arbitrary-precision construction |
| Visualization | Viewer export encodes finite integer code arrays | Keep digit rows, widths, crops, localized structures, and regular-region plots downstream as observers with explicit codecs |

The seed-512 value already exceeds signed 64-bit range after 82 events. That is a concrete runtime counterexample to retaining the current fixed-width episode representation, but it does not justify a T36 runner: it just exercises T34's exact scalar carrier and the closed positional RULE delta.

## Semantic Closure

The semantic oracle evaluates every governed profile through both an integer encode/reverse/decode/add path and an independent grade-school digit-word addition path. Its exact results are:

- 1,180 source-seed events (`180 + 1000`), with all 1,180 replayed through the independent word evaluator and exact program provenance;
- 22,036 scalar/word commutations: 11,275 canonical, 5,022 fixed-width, and 5,739 growing-width;
- 1,881 exhaustive fixed digit-reversal entries over `(base,width) = (2,7), (2,10), (3,6)`, each a proved involutive permutation;
- five arbitrary-precision profiles reaching 6,644 bits and 2,001 decimal digits;
- 260 trace horizons, 8,320 committed events and replays, and 2,080 `changed=false` events that still advance normally;
- seven exact structural program keys, three cross-program replay rejections, 68 hostile rejections, and 14 exact dataclass-role records;
- zero new FRONTIER, NEIGHBORHOOD, UPDATE, or executor symbols.

Representative exact boundaries are:

| Profile | Old configuration | Successor | Point proved |
|---|---|---|---|
| Strict canonical base 2 | `0` | `0` | Native fixed point; event exists with `changed=false` |
| Strict canonical base 2 | `16` | `17` | Binary reversal, not decimal string reversal |
| Strict canonical base 2 | `2` (`10`) | `3` | Reversed intermediate `01` is valid but noncanonical |
| Fixed base 2, width 4 | `2` (`0010`) | `6` (`0110`) | Width is immutable program data |
| Fixed base 2, width 4 | `15` | `14` | Untruncated sum 30 drops one left carry |
| Growing base 2 | `(2,4)` | `(6,5)` | Width is visible successor state |
| Growing base 2 | `(6,5)` | `(18,6)` | One position is added at every event |

The width-erasure counterexample is executable, not rhetorical: `(value,width)=(1,1)` and `(1,2)` have the same numeric projection, but one step produces `(2,2)`/`10` and `(3,3)`/`011`. Therefore the scalar projection is not a lossless configuration map for the growing profile. By contrast, strict canonical words and integers commute one event at a time because the canonical codec is bijective on nonnegative integers.

For the source-pinned positive seeds, the independently computed seed-16 trace ends after 180 events at `3987197239207620088799663177286543360` (122 bits), while the seed-512 value after 1,000 events has 627 bits. These are deterministic formula checks, not recovered raster values; the source's one-million-event observation remains an empirical qualification rather than a reproduced million-event fixture.

The oracle binds complete source claims, architecture classifications, Goal 2 deltas, structural program keys, role manifests, witnesses, events, outcomes, and traces. Hostile mutations prove that removing event replay, removing trace continuity, adding a `DigitReversalExecutor`, or changing any architecture/source/handoff claim makes the oracle fail.

## Final Architecture Classification

| Responsibility | Class | Smallest reusable base | Required T36 invariant/delta |
|---|---:|---|---|
| Strict configuration/DOMAIN | 1/2 | T34 discrete `t+0D` exact singleton | Nonnegative carrier and base-2 canonical profile; zero is native |
| Base/profile identity | 2 | Closed unary-program parameters | Exact base and canonical/fixed/grow tag; fixed width in program identity |
| FRONTIER/NEIGHBORHOOD | 1 | `UniqueScalar` plus `Self` | No new selector or access pattern |
| RULE | 2 | D069 shared closed unary algebra | Typed encode/reverse/decode/add and explicit width/carry profile |
| Assignment/UPDATE/outcome/trace | 1 | T34 generic same-locus atomic assignment and `StepResult` | Fixed points continue; complete state equality controls `changed` |
| Canonical word representation | 3 | Exact canonical integer codec | Bijection and one-event commuting square |
| Growing-width representation | 3 | Tagged `(value,width)` or width-preserving word | Preserve semantic width; scalar erasure is prohibited by the counterexample |
| New execution algebra | Not justified | Shared branch-free SimpleProgram runner | No T36 state class, executor, family branch, or UPDATE law |

D137 therefore classifies every T36 delta as direct reuse, parameterization/restriction, or lossless tagged/product representation. There is no class-4 execution-algebra delta.

## Evidence and Oracle Work Plan

1. Build a redundant source-query union covering reversal-add, reverse/digit/base/leading-zero/carry terms, main captions, Notes, Index, history, positional codecs, FFT/digit-reversal sequences, and false-positive mathematical digit reversal.
2. Reverse-close every monolith hit and retained continuation to structural split owners; bind every referenced image by exact path/size/SHA and disposition it as native, relation, control, or exclusion.
3. Independently compute frozen prefixes for the source-pinned seeds 16 and 512, verify the stated digit-length and growth claims, and admit no raster-derived numeric checkpoint without an explicit transcription boundary.
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
