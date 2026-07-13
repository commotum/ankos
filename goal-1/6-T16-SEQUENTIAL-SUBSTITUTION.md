# 6-T16-SEQUENTIAL-SUBSTITUTION

Status: **COMPLETE**

## Current Facts

- Exact catalog row: T16, CSV line 17, `Sequential Substitution Systems`; taxonomy seed `ref/notes/CA-Types.md:413-439`.
- The native state is a finite ordered word over a declared finite alphabet. The construction depends on scanning a limited string, so an infinite random initial condition is not a native base case.
- A program is an ordered list of literal block replacements. At every step it tries clause 0 over the whole word from left to right, then clause 1 from the left only if clause 0 has no match, and so on. Selection order is therefore lexicographic `(clause_index, start_position)`, not global leftmost position across clauses.
- Exactly one matched interval is replaced per logical step. Search restarts from the first clause and the left edge on the next step; no persistent cursor is part of state.
- If no clause applies, evolution intrinsically terminates. This is distinct from an applicable identity rewrite, a repeated snapshot, an external stop condition, a horizon, an invalid clause, or an execution error.
- The match interval is an old-snapshot source. Prefix and suffix occurrences persist; matched occurrences are consumed; replacement occurrences are created in right-hand-side order. This is a single structural splice, not T13's all-occurrence replacement and not fixed-support assignment.
- The direct T16 corpus establishes nonempty literal left sides but gives no deletion example and does not explicitly settle an empty right side. This stage keeps the evidence-strict T16 conformance surface at nonempty right sides and records deletion for T15 re-audit rather than silently broadening the family.
- There is no canonical integer rule code or finite rule count. Arbitrary finite block lengths and ordered clause-list lengths make the unbounded program space countably infinite.

## Updated Assumptions

- T13's ordered sequence state, snapshot-scoped occurrence identities, ragged trace, and structural provenance are reusable without changing their meanings.
- T13's `AllOccurrences -> SelfSymbol -> ReplaceOccurrence -> ParallelReplaceConcat` is not reusable as T16 execution. T16 requires program-dependent match discovery, rule-major priority, one interval result, a single-splice commit, and no-match termination.
- `FRONTIER` remains meaningful as source selection only after its independence hypothesis is weakened honestly: for literal rewriting, applicability depends intrinsically on the same authoritative ordered program that owns the clauses. A selector cannot discover a match without the left sides, and left sides must not be duplicated in a callback or second table.
- A typed `FirstApplicableMatch` source policy can expose this coupling: it consumes an `OrderedLiteralRewriteProgram` and returns zero or one `RewriteMatch`. The generic executor need not know T16, but the specification must validate that source discovery and result lookup refer to the same program object.
- The chosen match includes clause index, half-open interval, and consumed occurrence handles. A variable-length matched-word read validates the source; the rule returns `ReplaceInterval(match,replacement_word)`; `SingleSpliceUpdate` owns persistence, consumption, creation, and order.
- Zero selected sources has no universal meaning. T13's empty word has a vacuous successor, while T16's `NoApplicableClause` is terminal. The program/update contract must produce a typed step outcome rather than treating every empty frontier as halt or continuation.
- Rule order, left-to-right scan, one-event granularity, and restart behavior are defining semantics under Principle 11. A regex engine, host replacement default, or unordered map is not an incidental implementation choice.

## Big Picture Objective

Recover the exact deterministic first-match string-rewrite construction, then add only the smallest honest pressure to the shared transition model: program-coupled match-source discovery, a typed interval replacement, one-splice structural update, and no-match termination. Preserve T13 ordered support and provenance while rejecting a sequential-family rollout, hidden cursor, host-regex callback, or all-match/multiway substitution.

## Catalog Identity

- Stable ID: T16.
- Exact name: Sequential Substitution Systems.
- Canonical aliases and relations: sequential substitution/replacement systems, classifier systems, production systems, string rewriting systems, Markov systems, Markov normal algorithms, search-and-replace systems, and text-editor rules.
- `semi-Thue system` is not treated as a T16 alias in this corpus: its direct occurrences name multiway systems.
- Entry kind: deterministic ordered first-applicable literal string-rewrite construction.
- Defining parameters: finite alphabet, finite initial word, ordered nonempty clause list, literal nonempty left side per clause, replacement word, rule-major priority, left-to-right occurrence order, and one replacement per step.
- Search vocabulary: sequential substitution/system/replacement, classifier system, string rewriting, production system, Markov system, normal algorithm, text editor, search-and-replace, scan string/sequence, left-to-right/right-to-left, first sequence/match/replacement, successive replacements/scans, one/single/all possible replacement, replacement order, overlap, stops/no replacement, `Flat`, `SSSEvolveList`, `StringReplace`, confluence, causal network, generalized substitution, multiway, finite/random initial string, emulation, and operator evolution.

## Search Log

### Coverage and method

The taxonomy section was read first. Case-insensitive fixed and regex searches covered the direct name, mechanical phrases, aliases, implementation symbols, rule/position order, overlap, termination, seed extent, causal events, generalized and multiway variants, emulations, and historical names. Broad `replacement`, `halt`, and `stop` hits were inspected only where section context, a T16 cross-reference, or an Index route made them candidates.

| Query family | Canonical hit count or disposition |
|---|---:|
| `sequential substitution system` / `sequential substitution` | 42 / 51 lines, all classified |
| `string rewriting` / `production system` / `normal algorithm` | 6 / 6 / 2 lines, all classified |
| `search-and-replace` / `scan the string` / `left-to-right scan` | 2 / 3 / 4 lines, all classified |
| `right-to-left` | 1 line, unrelated arithmetic digit scan |
| `first replacement` / `first sequence` / `successive replacement` | 5 / 4 / 1 lines, all classified |
| `one replacement` / `single replacement` / `all possible replacements` | 4 / 2 / 2 lines, all classified |
| `order of replacements` / `none of the replacements` / `effectively stops` | 2 / 1 / 1 lines, all classified |
| `StringReplace` / `SSSEvolve` / `Flat` | all implementation and false-positive contexts inspected |
| `replacement` / `overlap` / `confluence` | 90 / 51 / 22 lines, targeted T16/generalized/multiway contexts classified |
| `initial string` and random-initial-condition routes | 6 direct lines plus Notes/Index references, all classified |
| `halt` / `stop` | 74 / 32 lines; non-T16 occurrences excluded by context |

Representative commands were `rg -n -i -e '<term>' BOOK`, followed by exact context inspection. Search counts are an audit trail, not evidence by themselves.

### Candidate disposition

| Region/candidates | Disposition |
|---|---|
| `1054-1078` | Core finite string state, text-editor analogy, left-to-right first occurrence, exact single rule/seed, ordered multi-rule priority, and restart semantics included. |
| `1084-1106` | Three-clause complexity, seed `BAB`, event dots, and record-length-only observer included; figure-only rule glyphs were not guessed from OCR. |
| `2358-2366` | One-block-per-step corroboration and lack of a natural direct 2D scan included. |
| `2508-2510`, `6016-6022` | Same block rules but all possible successors redirected to multiway systems; retained as the deterministic/branching boundary. |
| `5928-5954` | Generic block replacement, first-applicable T16 selection, causal event traces, and all-fitting generalized replacement contrast included. |
| `5954-6002`, `16429-16444`, `16521-16544` | Replacement-schedule dependence, causal invariance, overlaps, convergence, and Church-Rosser/confluence classified as generalized/multiway properties, not base T16 selection. |
| `7938-7960`, `8030-8040` | T16-to-CA and CA-to-T16 emulations included as relations; neither compiler defines native execution. |
| `12263-12292` | Complete Notes implementation, associativity, single replacement, explicit position tracking, sorting, no-match stop, order, aliases, and adaptive-rule extension included. |
| `13265`, `14275` | Finite/integer-like initial-condition limitation included. |
| `15766` | Runtime rule addition classified as an adaptive-program extension, not hidden mutable base state. |
| `16404-16426` | One-replacement implementation, all-fit contrast, element provenance, and depth-first sequential limit included. |
| `16446-16448` | Sequential cellular automata excluded: fixed cells are updated in-place and may read newly updated neighbors. |
| `18396-18414` | Published T16-to-CA compiler classified as an OCR-damaged emulation, not an implementation source. |
| `18478-18486` | Clean CA-to-T16 compiler and initial encoding retained only as a relation/conformance stress case. |
| `19164`, `20184` | Variable block sizes and operator-evolution analogy included. |
| `13989`, `19339`, Index `22096` | Semi-Thue references explicitly describe multiway systems and are excluded as T16 aliases. |

### Split, Index, image, and source-defect audit

- Chapter 3 split lines 371-423 duplicate canonical `BOOK:1054-1106`; Chapter 5 split lines 211-217/329-339, Chapter 9 lines 759-901, and Chapter 11 lines 247-259/323-339 duplicate the 2D, multiway, scheduling/causal, and emulation passages. No unique passage was added.
- Mispartitioned `BACK-MATTER/Index/Index.md:168-197` duplicates canonical Notes `BOOK:12263-12292`; `BACK-MATTER/Notes/Notes.md` is a one-line unrelated truncation.
- `BACK-MATTER/Colophon/Colophon.md` contains duplicated later Notes and the flattened actual Index. Atlas lines 93-96 are high-level summaries only.
- The actual Index exists in the monolith. Its OCR-flattened T16 entry at `BOOK:22096` routes to pages 88-92, implementation/history 893-894, causal networks 499, computational reducibility 1134, random initial conditions 949, CA emulations 660/667/1111/1113, multiway contrast 204/938/1172, 2D generalization 192, genetic programs 1002, and sequential-CA contrast 1034; all construction-bearing routes were followed. Classifier, Markov, normal-algorithm, and search-and-replace redirects at `BOOK:20972`, `21497`, `21701-21703`, and `22080` add names but no mechanics.
- The same flattened line interleaves adjacent Semigroup entries. `enumeration 805`, `history 1153`, `number 945`, `universality 1159`, Krohn-Rhodes, equivalence undecidability, and word-problem undecidability are not T16 routes. The separate computational-universality Index entry at `BOOK:22390` correctly routes T16 to page 667.
- `_page_104_Picture_3.jpeg` was inspected to verify the selected `BA` event dots and rule glyph. Figure-only three-clause rules were not transcribed because clean Markdown does not preserve their labels reliably.
- Notes page labels `82` and `85` at `BOOK:12269-12274` are extraction errors for the main-text pages 88/89; their literal 0/1 rules correspond to the A/B examples after symbol renaming.
- `SSSEvolveList` declares `init_s` but the extracted body uses `init` (`BOOK:12282-12283`); `init_s` is the evident intended argument. This OCR/name defect does not determine semantics.
- The explicit prefix/suffix patterns at `BOOK:12286` are OCR-damaged, but the prose and `Length[s[x]]` independently establish that the chosen substitution position can be recorded.
- Mathematica `/.` returns the same expression when no rule applies. Notes call that situation effectively stopped; the semantic reconstruction records terminal `NoMatch` rather than treating host-language stuttering as infinite evolution.

### Ambiguities resolved

1. The algorithm is rule-major, then leftmost-position. `BOOK:1070-1078` says to scan the whole word for the first clause and rescan from the left for the second only if necessary. It is not one global left-to-right scan that chooses whichever clause starts earliest.
2. One host `ReplaceAll` application does not license repeated rewriting within a step. Main text and captions say exactly one block/event per step; replacement output is considered only after the next step restarts.
3. `Flat` supplies associative contiguous-subsequence matching, not commutativity. Word order is preserved; clauses and positions are ordered.
4. A no-match expression and an identity rewrite can have equal values but different event/termination semantics. Only absence of an applicable clause is terminal.
5. Every evidenced left side is nonempty, and an empty left side would have unsupported ubiquitous match positions. T16 rejects it.
6. No direct T16 passage or example settles an empty right side. General multiway examples do delete, but they do not prove the T16 variant. The base T16 handoff therefore validates nonempty replacement words and requires T15 to re-audit deletion rather than inferring it from host syntax or external terminology.
7. Index column interleaving makes `enumeration of, 805` visually adjacent to T16, but page 805 concerns operator/string-concatenation material. No T16 rule-number convention or finite count was found.

**Search closure:** independent canonical and Notes/Index audits agree. All direct-name lines, aliases, captions, implementation symbols, Index/split routes, priorities, stop cases, initial-condition limits, generalized/multiway boundaries, causal traces, adaptive extensions, and emulations are included or explicitly excluded. Zero evidence candidates remain unresolved; the right-side emptiness question is a documented evidence boundary assigned to T15, not a hidden assumption.

## Book Excerpts

All excerpts are verbatim from `BOOK`.

### E01 — finite string state and left-to-right first-match semantics

`BOOK:1056-1062`, Chapter 3, “Sequential Substitution Systems”:

> variants of substitution systems that work essentially just like standard text editors.
>
> think of substitution systems as operating not on sequences of colored elements but rather on strings of elements or letters. Thus for example the state of a substitution system at a particular step can be represented by the string ABBBABA
>
> sequential substitution systems, in which the idea is instead to scan the string from left to right, looking for a particular sequence of elements, and then to perform a replacement for the first such sequence that is found.

This fixes ordered word state, scan direction, literal sequence matching, and one selected occurrence.

### E02 — exact one-clause rule, seed, and event marks

`BOOK:1064-1068`:

> the rule specifies simply that the first sequence of the form BA found at each step should be replaced with the sequence ABA.
>
> the string which exists at that step should be scanned from left to right, and the first sequence BA that is found should be replaced by ABA. In the picture, the black dots indicate which elements are being replaced at each step. In the case shown, the initial string is BABA.

The dots identify the consumed match interval; they are an event observer, not extra state.

### E03 — clause order is outside occurrence order

`BOOK:1070-1078`:

> at each step to scan the string repeatedly, trying successive replacements on successive scans, and stopping as soon as a replacement that can be used is found.
>
> rule  $\{ABA \rightarrow AAB, A \rightarrow ABA\}$  involving two possible replacements. Since the sequence ABA occurs in the initial string that is given, the first replacement is used on the first step. But the string BAAB that is produced at the second step does not contain ABA, so now the first replacement cannot be used. Nevertheless, since the string does contain the single element A, the second replacement can still be used.
>
> At each step, the whole string is scanned once to try to apply the first replacement, and is then scanned again if necessary to try to apply the second replacement.

The defining priority is `(clause order, leftmost match within that clause)`.

### E04 — rule-list size, seed, event view, and compressed observer

`BOOK:1086-1106`:

> if one allows more than two possible replacements then one can indeed immediately get more complex behavior.
>
> Examples of sequential substitution systems whose rules involve three possible replacements. In all cases, the systems are started from the initial string BAB. The black dots indicate the elements that are replaced at each step.
>
> The compressed picture on the left is made by evolving for a million steps, but showing only steps at which the string becomes longer than it has ever been before.

Three clauses and `BAB` are experimental parameters. Record-high-length filtering is downstream observation, not evolution or termination.

### E05 — one block per step and the one-dimensional scan boundary

`BOOK:2358-2366`:

> sequential substitution systems, in which just a single block of elements are replaced at each step. And what we did to find which block of elements should be replaced at a given step was to scan the whole sequence of elements from left to right.
>
> there seems to be no immediate way to generalize sequential substitution systems to two or more dimensions.

An arbitrary 2D traversal is not a hidden T16 geometry parameter; the native order is one-dimensional.

### E06 — multiway systems share clauses but change successor algebra

`BOOK:2508-2510`:

> Multiway systems can in general use any sets of rules that define replacements for blocks of elements in sequences. We already saw exactly these kinds of rules when we discussed sequential substitution systems on page 88. But in sequential substitution systems the idea was to do just one replacement at each step.
>
> In multiway systems, however, the idea is to do all possible replacements at each step—and then to keep all the possible different sequences that are generated.

T16 has at most one deterministic successor; T23-style multiway branching is not a selector option inside it.

### E07 — exact selection scheme and causal event trace

`BOOK:5928-5940`, Chapter 9:

> Such systems in general take a string of elements and at each step replace blocks of these elements with other elements according to some definite rule.
>
> In a sequential substitution system only the first replacement that is found to apply in a left-to-right scan is ever performed at any step.
>
> One scheme for deciding which replacement to make is just to scan the string from left to right and then pick the first replacement that applies. This scheme corresponds exactly to the sequential substitution systems we discussed in Chapter 3.

The selected interval is an event source from which causal relations can later be derived.

### E08 — all-fitting replacement is a different construction

`BOOK:5944-5954`:

> what happens if one again scans from left to right, but now one performs all replacements that fit, rather than just the first one.
>
> every replacement that is found to fit in a left-to-right scan is performed at each step.
>
> for the vast majority of rules ... using different schemes yields quite different behavior—and a quite different causal network.

First-only versus all-fitting is defining update/schedule semantics, not an optimization.

### E09 — one deterministic string versus every possible string

`BOOK:6016-6022`:

> Both types of systems perform the same type of replacements on strings of elements. But while in a substitution system one always carries out just a single set of replacements at each step, getting a single new string, in a multiway system one instead carries out every possible replacement, thereby typically generating many new strings.

This independently guards single-successor determinism.

### E10 — CA emulation has a different realization

`BOOK:7948-7960`:

> it can take progressively larger numbers of cellular automaton steps to reproduce each successive step in the evolution of the substitution system
>
> The same kind of problem occurs in sequential substitution systems ... it is still perfectly possible to emulate systems like these using cellular automata.
>
> A cellular automaton set up to emulate a sequential substitution system. The cellular automaton involves 28 colors and nearest-neighbor rules. The strings produced by the sequential substitution system appear on successive diagonal stripes

A CA compiler is a time/space encoding, not native T16 support.

### E11 — sequential substitution can emulate cellular automata

`BOOK:8030-8040`:

> What about sequential substitution systems? Here again it turns out to be fairly easy to emulate cellular automata
>
> Sequential substitution systems that emulate cellular automata with rules 90 and 30. ... The sequential substitution systems involve elements with 3 possible colors.

This relation supplies universality pressure but does not replace the literal rewrite constructor.

### E12 — associative word representation and literal block clauses

`BOOK:12265-12279`, Notes “Implementation”:

> Sequential substitution systems can be implemented quite directly by using Mathematica's standard mechanism for applying transformation rules to symbolic expressions.
>
> `Attributes[s] = Flat`
>
> the state ... can be represented by a symbolic expression such as s[1, 0, 1, 0]. The rule ... can then be given simply as  $s[1, 0] \rightarrow s[0, 1, 0]$
>
> `{s[0, 1, 0] \rightarrow s[0, 0, 1], s[0] \rightarrow s[0, 1, 0]}`
>
> The *Flat* attribute of s makes these rules apply ... to any subsequence such as s[1, 0].

Associativity exposes contiguous literal subsequences without making the word orderless.

### E13 — one host replacement, explicit match position, and all-occurrence rejection

`BOOK:12281-12286`:

> `SSSEvolveList[rule_, init_s, t_Integer] :=`
> `NestList[# /. rule &, init, t]`
>
> one can explicitly set up rules based on patterns ... And by using rules such as ... `Length[s[x]]` one can keep track of the positions at which substitutions are made. (`StringReplace` replaces all occurrences of a given substring, not just the first one, so cannot be used directly as an alternative to having a flat function.)

Position/event data is observable; a bulk string replacement API has the wrong semantics.

### E14 — exact sorting fixture, intrinsic no-match stop, and ordered priority

`BOOK:12288-12289`:

> Even with the single rule  $\{s[1, 0] \rightarrow s[0, 1]\}$ , a sequential substitution system can sort its initial conditions so that all 0's occur before all 1's.
>
> For many sequential substitution systems the evolution effectively stops because a string is produced to which none of the replacements given apply. ... the order in which the replacements are tried matters. (Multiway systems ... are what result if all possible replacements are performed at each step.)

No applicable clause is a construction-specific terminal condition.

### E15 — aliases, history, and adaptive extension

`BOOK:12290-12292`:

> often considered examples of production systems or string rewriting systems. In the form I discuss here, they seem to have arisen first under the name "normal algorithms" in the work of Andrei Markov
>
> text editors like TECO and ed used sequential substitution system rules, as have string-processing languages such as SNOBOL and perl.
>
> new rules can be added to a sequential substitution system incrementally without changing its basic structure

The base program remains a fixed ordered clause list during an episode; incremental mutation is an explicit adaptive-program variant.

### E16 — finite initial-condition capability

`BOOK:13265` and `14275`:

> sequential substitution systems or cyclic tag systems ... cannot meaningfully be given infinite random initial conditions ... Their initial conditions correspond in a sense to integers rather than real numbers.
>
> Sequential substitution systems, however, rely on scanning limited sequences of elements, and so cannot readily be given infinite random initial conditions.

Native T16 matching is over a finite word; padding or a finite crop is not an infinite input semantics.

### E17 — one-replacement implementation versus all-fitting implementation

`BOOK:16404-16415`, Notes “The Sequencing of Events in the Universe”:

> Sequential substitution systems in which only one replacement is ever done at each step can just be implemented using `/.` as described on page 893. Substitution systems in which all replacements are done that are found to fit in a left-to-right scan can be implemented as follows

The separate implementation confirms that all-fit generalized substitution is not the same update with a rendering change.

### E18 — generated-element provenance and sequential depth-first limit

`BOOK:16418-16426`:

> If every element generated in the evolution of a generalized substitution system is assigned a unique number, then events can be represented for example by  $\{4, 5\} \rightarrow \{11, 12, 13\}$
>
> If there is a tree of possible replacements (as in "A"  $\rightarrow$  "AA"), then the sequential substitution system in a sense does depth-first recursion in the infinite tree, never returning from the single path it takes. Other schemes are closer to breadth-first recursion.

Consumed-to-created occurrence records can support a lossless event/causal trace without becoming rule-readable state.

### E19 — CA-to-T16 compiler is an encoding relation

`BOOK:18478-18486`:

> Given the rules for an elementary cellular automaton ... the following will construct a sequential substitution system which emulates it
>
> The initial condition {0, 0, 2, 0, 0} for the sequential substitution system corresponds to a single black cell surrounded by white cells in the cellular automaton.

The compiler is a valuable cross-construction test, but no T16 API may require a CA source program.

### E20 — block lengths need not be uniform

`BOOK:19164`:

> dealing with blocks of different sizes requires going beyond an ordinary cellular automaton rule. But in a sequential substitution system ... this can be done just as part of an ordinary rule.

Both left and right block lengths are clause data; fixed arity or fixed output width is false.

### E21 — operator-evolution analogy

`BOOK:20184`:

> operator evolution systems similar to symbolic systems ... have essentially the same relationship to operator systems as sequential substitution systems do to multiway systems.

This is a relation to T20/operator systems, not permission to pack a tree expression into a T16 symbol.

## Construction Model

### Base deterministic ordered rewrite

Let `Sigma` be a finite declared alphabet, `w in Sigma*` a finite word, and the fixed program be an ordered nonempty sequence

```text
P = [RewriteClause(lhs_i, rhs_i) for i in 0..m-1]
lhs_i in Sigma+                 # directly required
rhs_i in Sigma+                 # evidence-strict T16 base; T15 must re-audit deletion
```

The first applicable source is

```text
M(w,P) = min_lex {
    (i,p) |
    0 <= i < m,
    0 <= p <= |w|-|lhs_i|,
    w[p:p+|lhs_i|] == lhs_i
}
```

where lexicographic order compares clause index before position. This is operationally equivalent to:

```text
for i, clause in enumerate(P):
    for p from 0 through len(w) - len(clause.lhs):
        if w[p:p+len(clause.lhs)] == clause.lhs:
            choose RewriteMatch(i, [p,p+len(lhs)), consumed_occurrences)
            stop both scans
```

If the set is empty, the current configuration is retained once as the final snapshot and the step outcome is `Terminal(NoApplicableClause)` with zero successors. Otherwise exactly one atomic event occurs:

```text
prefix = w[:p]
matched = w[p:q]
suffix = w[q:]
next = prefix ++ rhs_i ++ suffix
```

No replacement inside `rhs_i`, prefix, or suffix is reconsidered until the next logical step, when scanning restarts at clause 0 and position 0.

The typed shared-executor path is:

```text
program = OrderedLiteralRewriteProgram(clauses)
source  = FirstApplicableMatch.select(old_state, program)

if source is NoApplicableClause:
    outcome = Terminal(old_state, reason=NoMatch)
else:
    read    = MatchedWord.read(old_state, source)
    result  = program.apply(source, read)
            = ReplaceInterval(source, program[source.clause_index].rhs)
    outcome = SingleSpliceUpdate.apply(old_state, result)
```

`FirstApplicableMatch` is a closed typed source policy, not a regex/callback. It gets left sides from the same immutable `program` used to obtain the right side. The spec rejects a selector and rule table that disagree. This is an explicit intrinsic coupling under Principle 9, not duplicated logic.

For occurrence-aware state, the old prefix/suffix handles persist. The match handles are consumed and new handles are derived from the event and output ordinal. A transition can emit:

```text
RewriteEvent(
    clause_index=i,
    old_interval=[p,q),
    consumed_ids=(...),
    produced_ids=(...),
    produced_symbols=rhs_i,
)
```

Integer positions are valid inside one snapshot/event but are not persistent identity after length-changing splices. IDs and causal edges remain trace provenance because base T16 clauses inspect symbols only.

| Dimension | T16 semantics |
|---|---|
| State/support | Finite discrete ordered symbol word; no cursor or hidden scan state. |
| Alphabet | Finite declared `Sigma`; both clause sides are alphabet-closed. |
| Program | Fixed ordered nonempty list of literal block clauses; list order is semantic and is never sorted/deduplicated. |
| Sources | Zero or one `RewriteMatch` from rule-major, then leftmost-position matching over the old snapshot. |
| Read | Exact variable-length matched interval, with snapshot ownership and clause equality validation. |
| Result | Typed `ReplaceInterval(match, nonempty_word)`. |
| Update | Atomic `SingleSpliceUpdate`; preserve prefix/suffix, consume match, create replacement in word order. |
| Successor | One deterministic successor for a match; zero successors and final retained state for `NoMatch`. |
| Seed | Independent finite initial word; canonical `BABA`, secondary `BAB`, and arbitrary finite binary sort inputs. |
| Boundary | None: matching never wraps and reads no position outside the finite word. |
| Trace | Ragged word snapshots plus selected clause/interval and consumed-to-produced provenance; record-length filtering and causal graphs are downstream. |

### Structural and termination invariants

For a match `[p,q)` using clause `i`:

```text
0 <= p < q <= |w|
w[p:q] == lhs_i
|next| = |w| - |lhs_i| + |rhs_i|
next[:p] == w[:p]
next[p+|rhs_i|:] == w[q:]
```

Selection must also prove:

```text
for every j < i: lhs_j has no occurrence in w
for every r < p: w[r:r+|lhs_i|] != lhs_i
```

An overlap does not branch: `AA -> B` on `AAA` selects `[0,2)` and produces `BA`. Duplicate left sides are not silently rejected, sorted, or merged; a later duplicate is shadowed by order, which is inspectable program data.

`NoMatch` is the only intrinsic base terminal reason. It is not inferred from state equality or length:

- `A -> A` on `A` performs an event and has a successor equal in symbols.
- `A -> AA` grows forever despite repeatedly matching the same logical pattern.
- a rule can shrink, preserve, or grow length without that determining termination.
- horizon exhaustion retains a resumable nonterminal state and reports `Horizon`, not `NoMatch`.
- invalid programs/matches report validation errors and do not become terminal states.

### Exact trajectory oracles

Canonical single clause, from E02:

```text
P = [BA -> ABA]
t0 BABA
t1 ABABA       # clause 0, start 0
t2 AABABA      # clause 0, start 1
t3 AAABABA     # clause 0, start 2
t4 AAAABABA    # clause 0, start 3
```

Canonical ordered pair, from E03:

```text
P = [ABA -> AAB, A -> ABA]
t0 BABA
t1 BAAB        # clause 0, start 1
t2 BABAAB      # clause 1, start 1
t3 BAABAB      # clause 0, start 1
t4 BAAABB      # clause 0, start 2
```

Independent sorting fixture, from E14:

```text
P = [10 -> 01]
11010 -> 10110 -> 01110 -> 01101 -> 01011 -> 00111 -> NoMatch
```

Adversarial rule/position discriminator:

```text
P = [BA -> X, AB -> Y]
ABA -> AX
```

Clause 0 matches later at position 1 and must beat clause 1 at position 0. A position-major engine would incorrectly produce `YA`.

### Variant disposition

| Candidate | Disposition |
|---|---|
| Multiple ordered clauses | Native parameter; clause order is defining semantics. |
| Different literal block sizes | Native parameter (`BOOK:19164`). |
| Right-to-left, persistent cursor, or wraparound scan | No T16 evidence; excluded from base. |
| Empty left side | Unsupported/ambiguous infinite-position matching; rejected. |
| Empty right side/deletion | Not established directly for T16; evidence-strict base rejects pending T15 re-audit. |
| Identity clause | Native applicable event; never conflated with no match. |
| Generalized all-fitting replacement | Different source coverage/update (`BOOK:5944-5954`). |
| Multiway all-possible replacement | Different branching successor algebra (`BOOK:2508-2510`). |
| Confluent rules | Property of selected rule sets/underlying multiway relation, not a selector replacement. |
| Incrementally added rules | Adaptive-program variant; program mutation must be visible if later implemented. |
| Infinite random word | Not a native base seed because the global scan has no finite completion. |
| Two-dimensional scanning | No canonical direct generalization; not an arbitrary traversal parameter. |
| Sequential cellular automaton | Separate fixed-support in-place construction. |
| CA emulation in either direction | Relation/compiler and conformance fixture, never native mechanism. |
| Causal network, black dots, record-length frames | Observers derived from full event/snapshot trace. |
| Operator evolution | Related hierarchical construction requiring its own T20 evidence. |

## Current API Fit

| Concern | Fit | Finding |
|---|---|---|
| Canonical dense domain/address | SEMANTIC MISMATCH | `simple_programs.md:1-24,87-113` makes state a fixed `D -> A` field at `[t,x,y,z]`; T16 needs a changing finite ordered support and row-local snapshot positions. |
| Alphabet | DIRECT | `ALPHABET` as a value set (`:200-233`) can describe finite symbols, provided support and rule roles stay separate. |
| Seed | PRINCIPLED EXTENSION | Current support/fill/distribution seed (`:235-290`) materializes a fixed slice; T16 needs an explicit finite word independent of the program. |
| Boundary | NOT APPLICABLE | Current boundary policies resolve rectangular out-of-range reads (`:292-358`); literal finite-word matching neither wraps nor reads beyond an endpoint. |
| Neighborhood/read | SEMANTIC MISMATCH | Ordered finite relative offsets (`:360-731`) cannot express a clause-dependent variable-length interval. Integer proximity must not stand in for sequence topology. |
| Frontier/source | SEMANTIC MISMATCH | The document selects absolute writable next coordinates (`:1412-1510`). T16 selects an old-snapshot matched interval and applicability depends on the ordered program. |
| Rule | SEMANTIC MISMATCH | Current rules return one next value per writable target (`:1767-1793`). T16 owns ordered literal clauses and returns a typed interval replacement word. |
| Formulaic rule | SEMANTIC MISMATCH | `FORMULAIC` receives the whole field (`:2036-2073`) and could hide scanning/splicing, but doing so would make component boundaries vacuous. |
| Update | SEMANTIC MISMATCH | Current semantics write all selected coordinates in parallel and copy others (`:1767-1793,2156-2199`); T16 performs one support-changing splice. |
| Successor/termination | PRINCIPLED EXTENSION | The fixed-horizon loop has no zero-successor terminal outcome; T16 requires retained final snapshot plus `NoMatch`. |
| Trace/encoding | SEMANTIC MISMATCH | Persistent fixed-domain trajectory and canonical coordinate allocation cannot losslessly represent ragged frames, occurrence persistence, or rewrite events without a separate lowering. |
| Rule ID/count | NOT APPLICABLE | The book gives no bounded enumeration. An integer ID cannot be mandatory for arbitrary ordered finite clauses. |
| Observers | PARAMETERIZATION | Dots, causal graphs, and record-length filtering can be downstream transformations once the raw event trace is retained. |

## Current Runtime Fit

- `alphabets.symbolic()` is useful finite-value machinery (`src/ca/alphabets.py:146-177`), but it does not define ordered support or clause sides.
- `CoordinateSpace` is finite rank 0-3 (`src/ca/loci.py:31-94`). It cannot represent length-changing occurrence support, and dense coordinate proximity cannot substitute for word order plus snapshot ownership.
- `Dynamics.shape` is mandatory and fixed (`src/ca/specs.py:24-55`); `rollout` rejects seed/produced shape mismatches (`src/ca/rollout.py:40-75`). T16 rule lengths can change every step.
- `RawEpisode`/`RawBatch` require one NumPy state array and an integer `rule_id` (`src/ca/specs.py:58-82`). They cannot preserve ragged frames, no-match terminal reasons, or structured clauses/events.
- `frontiers.py` exposes only dense `time_slice` (`src/ca/frontiers.py:38-80`), and rollout rejects any other frontier (`src/ca/rollout.py:825-831`). There is no interval match source.
- `neighborhoods.py` builds finite relative coordinate stencils (`src/ca/neighborhoods.py:110-549`); there is no literal variable-span matcher or matched-word read.
- `Rule` stores a family string, optional integer ID, `Any` params, and optional callable (`src/ca/rules.py:30,65-78`). These are not typed rewrite clauses. `formulaic(fn)` (`:316-328`) would smuggle the whole construction into a callback and is rejected.
- `_rollout_states` and `_rollout_batch_states` branch on `rule.family` (`src/ca/rollout.py:145-212`). Adding `sequential_substitution` there would violate the shared-executor requirement.
- Spatial rollout preallocates fixed NumPy arrays and computes scalar values for every site (`src/ca/rollout.py:576-660`). It has no one-splice structural update, preserved occurrence IDs, terminal outcome, or event record.
- `canonical_coords` emits one identical dense grid per time (`src/ca/rollout.py:215-267`); T16 needs explicit ragged lowering and cannot treat row-local `x` as identity.
- Current seeds render fixed arrays for a requested shape (`src/ca/seeds.py:879-939`), and dataset batching stacks equal shapes (`src/ca/datasets.py:313-334`). Padding/masks are allowed only after native trace generation.
- Current tests preserve fixed-shape and full-frontier behavior (`tests/test_rollout.py:263-309,529-560`; `tests/test_viz_export.py:72-105`). No test covers rule-major matching, overlaps, one-event splicing, match provenance, no-match termination, identity events, or finite-word scan semantics. Existing tests must remain valid through the rederived raw boundary, not be weakened.

## Principles Audit

| Principles | T16 result |
|---|---|
| 0-3 | T13's independent `AllOccurrences` frontier does not compose. Refine source selection to accept an authoritative program-owned applicability view; do not duplicate LHS data or add a T16 rollout. |
| 4 | `ReplaceInterval` is an explicit structural result. `SingleSpliceUpdate` is a sibling update algebra, not scalar assignment or parallel concatenation. |
| 5 | State is the finite word. There is no hidden cursor; adaptive rule mutation would have to become visible program/control state. |
| 6-8,12 | Sequence order, occurrence identity, row-local position, ragged storage, ANKoS coordinates, padding, and rendering remain distinct. |
| 9 | Clause order, LHS applicability, RHS lookup, matched read, and splice result are intrinsically coupled through one validated program; seed and observers remain independent. |
| 10 | A `sequential_substitution` preset returns an ordinary literal-rewrite specification and terminal policy, never a family executor. |
| 11 | Rule-major priority, left-to-right matching, one event, and restart are defining semantics. Host matcher choice is acceptable only when it is proved equivalent. |
| 13-15 | Later-rule/earlier-position, overlap, no-match/no-op, newborn, changing-length, provenance, and multiway/all-fit adversaries are mandatory conformance tests. |
| 16 | Typed matcher/program/result/update/outcome boundaries are architecture; regex callbacks, family switches, padding, CA compilation, and stutter-as-halt are shims. |

The refined substantive shell is:

```text
source  = SOURCE.select(old_state, program.applicability)
reads   = READ.read(old_state, source)
results = RULE(program, source, reads)
outcome = UPDATE.apply(old_state, results)
```

T01/T09/T12 use program-independent fixed/control source policies; T13 uses program-independent `AllOccurrences`; T16 supplies an explicitly coupled literal applicability object. This changes the independence assumption, not the source-first meaning established by D009. No prior construction needs a behavior change.

## Detailed Implementation Plan

1. Record the closed evidence audit, source repairs, and evidence-strict empty-side boundary.
2. Reconstruct rule-major matching as a typed source policy over one immutable ordered rewrite program, not a host callback.
3. Reuse T13 ordered sequence/occurrence support and introduce `RewriteMatch`, matched-span validation, `ReplaceInterval`, and `SingleSpliceUpdate` without weakening `ParallelReplaceConcat`.
4. Extend T12's typed outcomes with construction-specific `NoMatch`; prove an identity event and equal snapshot do not terminate.
5. Specify exact canonical, sorting, priority, overlap, newborn, terminal, lineage, validation, observer, and shared-executor conformance tests.
6. Reintegrate the evidence index, plan, and design ledger; reopen earlier stages only if the explicit program/source coupling invalidates their behavior.

## Goal 2 Implementation Stage

### G2-T16 — Ordered literal matching, single splice, and no-match termination

**Dependencies:** G2-T13 ordered sequence state, snapshot occurrence handles, ragged traces, and structural provenance; G2-T12 typed terminal/stop/error outcomes; synthesis-selected generic source/read/rule/update orchestration. T16 reuses neither T13 source coverage nor its update law.

**Implementation areas:**

- Synthesis-selected ordered-state module: reuse `OrderedSequence`/finite word and occurrence handles. T16 does not request T13's infinite support capability.
- Rewrite program module: immutable `RewriteClause(lhs: NonEmptyWord, rhs: NonEmptyWord)` and `OrderedLiteralRewriteProgram(clauses: NonEmptySequence)`, with alphabet closure and preserved clause order. Do not require a rule ID.
- Source-selection module/frontier: `FirstApplicableMatch` implementing exact nested loops `(clause_index, start_position)` and returning `RewriteMatch(snapshot_id, clause_index, start, stop, occurrence_ids)` or `NoApplicableClause`. It must read LHS patterns from the same program object used by the rule.
- Read module: `MatchedWord`, validating snapshot ownership, interval bounds, contiguous occurrence order, clause index, and exact LHS equality before evaluation.
- Result/update module: `ReplaceInterval(match, replacement_word)` and `SingleSpliceUpdate`; preserve prefix/suffix occurrences, consume only the match, create ordered output occurrences, and emit an optional `RewriteEvent`.
- Ordered edit core: T13 and T16 may share a private `ApplyOrderedSpans` kernel only after `ParallelReplaceConcat` validates complete ordered singleton coverage and `SingleSpliceUpdate` validates exactly one arbitrary span. The public commit laws remain distinct.
- Outcome/termination module: `TerminalReason.NoMatch` with the final snapshot retained once; keep terminal, external stop, horizon, and validation error distinct. An applicable identity clause produces a normal transition event.
- Generic executor: accept the typed program-coupled source contract and update/outcome member. Dispatch only through ordinary protocols/results supplied by the spec, never by T16/catalog name.
- `specs.py`/preset index: strict `sequential_substitution(alphabet, clauses)` returning the ordinary literal-rewrite spec. Initial word, horizon, and observers are episode choices.
- Structured raw trace: ragged words, step outcomes, selected clause/interval, and optional consumed/produced IDs. Downstream lowering can emit row-local `(t,x,0,0,symbol)` plus event tables; record-high frames and causal networks are observers.
- New `tests/test_t16_sequential_substitution.py` plus shared matcher/splice/outcome/trace conformance tests.
- T15 dependency note: separately re-audit deletion. If T15 establishes `rhs in Sigma*`, generalize the shared word/result/update type deliberately and re-run T13/T16 validators; do not preinstall an `allow_empty` flag.

**Canonical and adversarial tests:**

1. Assert E02 exactly: `BABA, ABABA, AABABA, AAABABA, AAAABABA`, with match starts `0,1,2,3` and one event per transition.
2. Assert E03 exactly through `BAAABB`, including clause indices and starts. At every step restart at clause 0 and word start.
3. Rule-major discriminator `[BA->X, AB->Y]`, `ABA -> AX`; reject position-major `YA`.
4. Use `AABA` with `[ABA->AAB, A->ABA]`: choose the later clause-0 occurrence and produce `AAAB`, not the earlier clause-1 result.
5. Overlap discriminator `AA->B`, `AAA -> BA`, not `AB`; prove no second match is applied in the same step.
6. Newborn discriminator `A->AA`, seed `A`: one step has length 2, not unbounded/in-step recursion; one event is recorded.
7. Sorting oracle `11010 -> ... -> 00111 -> NoMatch`; assert exactly five rewrite events, a retained final state, and zero successors after terminal.
8. Identity/no-match discriminator: `A->A` on `A` records an event and remains nonterminal; a word with no LHS match terminates even if a host `/.` would return the same value.
9. Vary LHS/RHS lengths and assert the length/prefix/suffix equations. Repeated symbols must still yield exact consumed occurrence handles.
10. Assert preserved prefix/suffix IDs, consumed interval IDs, ordered new IDs, event reconstruction, and equality up to provenance renaming where rules cannot read IDs.
11. Preserve duplicate/shadowed clause order; reject empty LHS, empty evidence-strict T16 RHS, clauses outside the alphabet, stale matches, mismatched clause/read data, invalid intervals, and nonliteral callbacks. None becomes skip, identity, or halt.
12. Reuse one program with multiple finite seeds, including an empty-word boundary that immediately yields `NoMatch`; seed never mutates program semantics.
13. Derive dots, causal events, and record-length-only frames from the same full trace; observers cannot affect selection or state equality.
14. Prove generalized all-fit and multiway enumerators produce observably different outputs on an overlap/priority fixture and cannot be passed as T16 source/update policies accidentally.
15. Run T01/T09/T12/T13/T16 through the same typed orchestration and statically reject family-name switches, regex/whole-word callbacks, CA compilers, fixed capacity, hidden cursors, and scalar-`Any` replacement results.
16. Do not add a canonical enumeration test. Assert instead that arbitrary clause/list lengths require structured program identity and that serialization round-trips exact order and words.

**Completion evidence:** all canonical/adversarial tests and the existing suite pass; selection is visibly rule-major/leftmost; exactly one structural event or a typed terminal outcome occurs; ragged words/events survive the raw boundary; T13 behavior remains unchanged; no T16 branch, host-regex escape hatch, fixed-capacity buffer, CA compiler, hidden cursor, global-leftmost shortcut, all-match fallback, or stutter-as-halt exists.

## No-Cheating Checks

- No family-name rollout, sequential-only executor, or boolean mode inside a generic substitution branch.
- No unrestricted whole-word function, regex callback, Mathematica engine, or `Any` result containing the transition.
- No copying LHS patterns into both a frontier callback and a separate rule table; one immutable program is authoritative.
- No unordered map, automatic clause sorting/deduplication, global-leftmost selector, right-to-left default, persistent cursor, or implicit wraparound.
- No applying every match, every clause, or every multiway successor while presenting the result as one sequential step.
- No rescanning replacement output or rewriting a newborn within the same logical step.
- No scalar `Assign`, next-target inversion, in-place shifting, fixed-capacity array, pad symbol, mask, truncation, or maximum-length buffer as word semantics.
- No same-valued successor or host-expression stutter treated as `NoMatch`; applicability and events decide termination.
- No missing/invalid clause or out-of-range match treated as skip, identity, fallback, or halt.
- No empty RHS claimed as native T16 before T15 supplies direct evidence and re-integration.
- No CA/multiway/operator compiler used to claim native support.
- No row-local coordinate treated as persistent identity; no required event provenance discarded before observer lowering.
- No record-length compression, causal rendering, or dots fed back into evolution.
- No existing fixed-support tests weakened; migrate the raw boundary truthfully and retain prior conformance.

## Completion Requirements

- [x] All aliases, captions, Notes, Index entries, splits, variants, duplicates, source defects, and false positives are resolved.
- [x] All unique construction-relevant excerpts have canonical provenance and disposition.
- [x] Finite word, ordered clauses, match source, rule/position priority, read, one-splice update, seed, successor, termination, and observables are reconstructed.
- [x] Canonical trajectories and adversarial priority/overlap/no-op/no-match/provenance invariants have independent conformance oracles.
- [x] Current API/runtime/test fit and T13 reuse/divergence are explicit under Principle 0.
- [x] Goal 2 implementation/conformance handoff is implementation-ready, including the T15 deletion re-audit boundary.
- [x] Global ledgers and plan are reintegrated and all verification checks pass.

## Stage Results

T16 is complete with zero unresolved evidence candidates. The nested scan is exactly rule-major then leftmost position, returns at most one snapshot-scoped interval, and restarts from clause 0 and the left edge after one splice. `FirstApplicableMatch` forces an honest refinement of the source-first shell because applicability and the ordered program are intrinsically coupled; one authoritative program supplies both matching left sides and the selected right side. `ReplaceInterval` plus `SingleSpliceUpdate` is distinct from T13's full-generation replacement, though both can reuse ordered support, provenance, and a policy-guarded private span-edit kernel. `NoMatch` is a typed zero-successor terminal outcome, while identity events, external stops, horizons, invalidity, and errors remain separate. Empty RHS is explicitly deferred to T15 evidence. The plan, evidence index, and design ledger are reintegrated; no prior stage is reopened. Focused source-reference, coverage, whitespace, and 102-test baseline verification passed. Next: T17 Tag Systems.
