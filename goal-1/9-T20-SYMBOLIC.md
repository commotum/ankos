# 9-T20-SYMBOLIC

Status: **COMPLETE — EVIDENCE AND ARCHITECTURE RECLOSED**

Architecture authority: the T20 row and runner contract in `architecture-audit.md` supersede any prohibition on transparent structured values or symbolic-executor framing below.

The evidence/search closure and conformance fixtures remain valid. Recursive tagged expressions and prefix-free replacements are transparent CONFIGURATION/RULE/UPDATE schemas inside the shared runner, not a symbolic executor.

## Current Facts

- Exact catalog row: T20, CSV line 21, `Symbolic Systems`; taxonomy seed `ref/notes/CA-Types.md:524-551`.
- The native state is a finite, well-founded, rooted ordered expression tree. General expressions may have expression-valued heads and several ordered arguments; the Chapter 3 construction restricts applications to one argument, so its expressions are binary trees.
- In functional notation, `e[x][y]` is `Apply(Apply(Atom(e), x), y)`. A head is itself a semantic child and a possible match occurrence; it cannot be discarded by an argument-only tree model.
- Rules are inert structural pattern/template data. In `e[x_][y_] -> x[x[y]]`, `e` is literal and the named blanks bind whole subexpressions. Template references may duplicate, delete, or rearrange bound subtrees.
- One canonical timestep is exactly one `ReplaceAll` pass, not normalization with `ReplaceRepeated`. The scan visits the functional form left to right, applies the first ordered rule that matches at a visited occurrence, prunes that occurrence's descendants, and continues to every later disjoint match.
- Selection is greedy and ordered, but all selected paths are pairwise prefix-incomparable and all bindings come from the old tree. Their replacements commit atomically. A redex created by the pass waits until the next timestep.
- No match returns the identical expression. Exact reference sampling is therefore event-free absorbing `Quiescent(NoPatternMatch)`; a stop-on-quiescence or stop-on-value-equality observer is an explicit episode policy.
- An applicable identity rewrite remains an `Advanced(changed=false)` event. It is not no-match quiescence even though a value-only fixed-point observer may stop on it.
- The canonical seed `e[e[e][e]][e][e]` has invariant value 256 under `V(e)=0; V(x[y])=2^V(x)+V(y)`. It first reaches `Nest[e,e,256]` at zero-based state `t=263`: 263 successful passes and 264 initial-inclusive displayed configurations.
- The page-118 seed `e[e][e][e][e][e]` first reaches `Nest[e,e,65536]` at zero-based `t=65,554`, giving 65,555 initial-inclusive configurations. Published “step” counts use the displayed-configuration convention.
- With `k` symbols and `n` leaves, the unary-expression profile contains `Catalan(n-1) k^n` structured expressions. No numeric rule/program codec or digit significance is supplied.
- Functional, Polish, operator, binary-tree, and one-symbol bracket forms are representations or codecs. Brackets alone are lossless only for one-symbol unary expressions; bracket bitmaps, leaf count, depth, invariant values, and size differences are observers.
- Combinators are a native specialization with ordered S/K rules; deterministic operator evolution is a broader one-pass pattern variant. Confluence, normalization, multiway equation application, CA emulation, lambda compilation, valuations, universality tests, and network analogs are relations or analyses, not alternate base execution.
- T13's ordered lineage and T16's program-coupled matching are reusable responsibilities. T13 all-occurrence concatenation and T16 single-interval splice cannot implement a maximal nonoverlapping tree rewrite; T20 proves a fifth sibling update law.
- The current dense rank-0..3 runtime has no expression tree, typed tree path, pattern AST, binding environment, prefix-free match source, inert template instantiation, subtree replacement result, or ragged structural trace. No existing family branch is a semantic fit.

## Updated Assumptions

- Tree topology consists of ordered `Head` and `Argument(i)` roles. Display coordinates, textual bracket offsets, host object identity, memory sharing, and drawing layout are not semantic addresses.
- The atom universe is explicit finite program data for the evidenced profiles. Pattern-variable identifiers occupy a separate meta-level and are never expression atoms.
- A matcher ranges over whole expression values. It is neither substring/regex matching nor a predicate callback. Repeated named binders, when an extended structural profile permits them, require exact subtree equality; anonymous blanks do not create bindings.
- One immutable ordered program is authoritative for both applicability and result selection. The source may be program-coupled without duplicating the pattern table or hiding matching in a callback.
- Functional left-to-right order is represented as outermost preorder: try the current expression, then its head, then arguments from left to right. A selected ancestor suppresses all descendant candidates for that pass.
- “Wherever possible without overlap” means the deterministic maximal set produced by that traversal, not every maximum-cardinality antichain, an unordered set, or a branch over alternative match sets.
- Semantic state is a tree even if an implementation internally hash-conses immutable nodes. Every repeated RHS reference creates a distinct semantic occurrence and distinct lineage; no rewrite can observe alias identity.
- A selected subtree is consumed. Unselected context persists; each RHS binding reference derives a copied occurrence of its bound old subtree; unused bound content disappears; literal/template nodes are newly created.
- Structural `Pattern` and `Template` sums must be closed and serializable. Unrestricted Mathematica conditions, evaluation attributes, delayed host code, or template functions are not admitted through `Any`; unsupported operator-pattern features fail validation.
- The exact `/.` pass, optional first-application technique, `//.` normalization, multiway application, and fixed-point observation are separate typed protocols rather than switches that silently change one executor.
- No-match, applicable identity, value-fixed observation, cycle detection, explicit horizon, invalid pattern, instantiation error, and resource failure remain distinct outcomes.

## Big Picture Objective

Reconstruct the complete symbolic-system expression carrier, pattern/binding language, traversal and overlap policy, template substitution, atomic tree update, fixed-point behavior, seeds, variants, observers, and computational relations. Determine the smallest construction-bearing tree-rewrite extension without flattening, unrestricted host evaluation, mutable-DAG semantics, family dispatch, fixed capacity, or conflation with T13, T16, T29, or T30.

## Catalog Identity

- Stable ID: T20.
- Exact name: Symbolic Systems.
- CSV provenance: `ref/notes/CA-Types.csv:21`; taxonomy provenance: `ref/notes/CA-Types.md:524-551`.
- Entry kind: deterministic hierarchical term-rewrite construction; one pass may replace several disjoint subexpressions.
- Evidenced native aliases/specializations: structure transformations, symbolic expressions, combinators, and one-pass operator evolution. “Rewrite system” is useful search vocabulary but not asserted as a unique local alias.
- `ReplaceAll` (`/.`) names the one-pass implementation. `ReplaceRepeated` (`//.`) names repeated normalization and is not one timestep.
- Search vocabulary: symbolic system/expression; structure transformation; combinator/S/K/j; operator evolution/system; application/head/argument/tree/subexpression; functional/Polish/bracket form; pattern/blank/binding; rule/rewrite/replacement; left/right/order/overlap; `ReplaceAll`/`ReplaceRepeated`; fixed point/normal form/Church-Rosser; leaf/depth/valuation; seed/initial expression; CA emulation; network analog; universality.

## Search Log

1. Verified the exact CSV/taxonomy join and read the complete taxonomy section as search vocabulary only.
2. Searched the canonical monolith for the combined direct/alias query `symbolic system(s)|symbolic expression(s)|combinator(s)|operator system(s)|Church-Rosser|rewrite system(s)`: 272 occurrences on 166 unique lines. The components were 73/60, 23/21, 117/74, 50/42, 5/5, and 4/4 occurrences/lines respectively.
3. A narrower exact-name audit dispositioned all 73 `symbolic system(s)` occurrences on 60 lines. Expanding through evidenced combinator/operator aliases gave 227 occurrences on 138 lines; adding control/observer aliases gave 238 on 140 lines. The larger query above catches additional generic wording and supplies the conservative closure count.
4. Searched exact rule forms, `functional representation`, `Polish representation`, `tree representation`, brackets, left-to-right/overlap language, `NestList[# /.`, `expr /.`, `LeafCount`, `Depth`, pattern variables, fixed points, long halting, valuations, seeds, rule order, CA emulation, network analogs, and every exact implementation/compiler symbol separately.
5. Inspected the native core at `BOOK:1220-1246`, all Notes at `12405-12486`, combinator specialization at `8568-8606` and `18924-19024`, CA relations at `8034-8052` and `18500-18512`, and confluence/operator/algebraic relations at `16530-16540`, `20184`, and `20261`.
6. Inspected the original raster figures for pages 117, 118, 119, 683, 726-729, 912, and 913. This recovered the page-117 caption and the six page-119 rules that are absent from Markdown, and verified that boxed redexes and tree diagrams bind entire subtrees.
7. Verified split files. `CHAPTERS/3-The-World-of-Simple-Programs/The-World-of-Simple-Programs.md:537-563` duplicates the core. The file named `BACK-MATTER/Index/Index.md:308-389` is actually a duplicate of the Notes, while `BACK-MATTER/Notes/Notes.md` is unusable. Canonical provenance is recorded once against the monolith.
8. Followed the actual alphabetic Index in the merged monolith and resolved its OCR-interleaved T20 route set against the official primary index: base page 102; networks 898; combinators 711; confluence 1036/1113; CA emulation 668/1113; history 898; implementation 896; operator systems 1172; universality test 1123; tree representation 897; valuation functions 916.
9. Rejected false neighboring Index routes for random initial conditions, state-transition graphs, Turing machines, undecidability, and one-element dependence. Their apparent association on merged line 22150 is a three-column OCR artifact.
10. Narrowly repaired representation-table/code-fence OCR, the malformed exponent tower, Church clause, and Smullyan spelling from official primary Notes. None changes the reconstructed transition law. The page-119 rules and page-117 caption came from repository raster originals.
11. Used official `ReplaceAll` and pattern documentation only to make the book's named host operation operationally testable: rules are tried in order at a part, a matched part suppresses descendants, no match returns the part unchanged, and repeated named blanks constrain equal expressions. Production conformance does not delegate to that host engine.
12. Excluded unrelated generic symbolic-expression uses in number representation, PDE sampling, theorem proving, communication, and book production. All direct, alias, caption, Notes, Index, split, history, variant, observer, and compiler candidates are dispositioned; unresolved native-mechanics count is zero.

## Book Excerpts

`BOOK` below means `ref/A-New-Kind-of-Science/A-New-Kind-of-Science.md`. These 24 groups capture every unique material passage; split duplicates are logged above.

### E01 — Native expression, base rule, and whole-expression variables

- Provenance: `BOOK:1220-1222`, Chapter 3, “Symbolic Systems.”
- Fact: the construction repeatedly transforms expressions such as `e[e[e][e]][e][e]` with `e[x_][y_] -> x[x[y]]`; `x_` and `y_` stand for any expression.

### E02 — One left-to-right nonoverlapping pass

- Provenance: `BOOK:1224-1226`.
- Fact: every step scans once left to right and applies the rule wherever possible without overlapping.

### E03 — Boxed-region figure and exact host-operation correspondence

- Provenance: `CHAPTERS/3-The-World-of-Simple-Programs/Images/_page_117_Figure_5.jpeg`.
- Fact: the embedded caption says every boxed region is transformed in the step and identifies the operation as `expression /. rule`. The boxes resolve simultaneous disjoint coverage and later-pass overlap.

### E04 — One-symbol bracket projection

- Provenance: `BOOK:1228-1238`, page-118 pictures.
- Fact: for the shown one-symbol unary expressions, opening/closing brackets completely encode structure. Pictures cut wide configurations on the right, so display width is not semantic truncation.

### E05 — Exact fixed configurations, nonlocality, and timing convention

- Provenance: `BOOK:1238-1240`.
- Fact: the first evolution has 264 initial-inclusive configurations and ends at 256 opening then 256 closing brackets; another has 65,555 configurations and 65,536 pairs. The rules are nonlocal and the base rule always reaches a fixed configuration, potentially after an iterated-exponential time.

### E06 — Nonstabilizing one-rule variants and common seed

- Provenance: `BOOK:1242-1246`, `_page_119_Figure_3.jpeg`.
- Fact: other rules may repeat, nest, grow, or appear complex. All six use `e[e[e][e]][e][e]`; their exact RHSs are `x[e[y]][x]`, `x[y][e[y]]`, `x[y[e][e]]`, `x[y[x]]`, `e[x[e][y[e]]]`, and `e[y[e[e][e]][x]]`. The lower plots show successive size differences, an observer.

### E07 — Exact one-pass implementation

- Provenance: `BOOK:12405-12407`.
- Fact: `NestList[# /. e[x_][y_] -> x[x[y]] &, init, t]` returns the initial state plus `t` one-pass successors. This distinguishes one step from `//.` normalization.

### E08 — Expression-valued heads and arity/currying boundary

- Provenance: `BOOK:12408`.
- Fact: in a general symbolic expression, the head in `h[x]` can itself be any expression, and several-argument expressions are native. Currying can represent them but is not generally treated as identical.

### E09 — Functional, Polish, operator, and tree representations

- Provenance: `BOOK:12409-12426`.
- Fact: the Notes give conversions among representations and state that unary expressions form binary trees. These are bijective codecs only over their declared domains, not alternate native update laws.

### E10 — Bracket encoding's exact domain

- Provenance: `BOOK:12428-12433`.
- Fact: when one symbol appears, removing it leaves a balanced opening/closing-bracket description. This does not justify unlabeled bracket state for several symbols or arities.

### E11 — Expression measures, enumeration, and structured count

- Provenance: `BOOK:12435-12444`.
- Fact: `LeafCount` and `Depth` are observers; recursive enumeration gives `Binomial(2n-2,n-1) Length[s]^n/n` expressions with `n` leaves over symbol list `s`. No integer expression or rule code is defined.

### E12 — Fixed forms, invariant, and tower-time bound

- Provenance: `BOOK:12446-12454`.
- Fact: every base-rule seed reaches `Nest[e,e,m]`; replacing `e->0` and `x[y]->2^x+y` gives invariant `m`. The Notes characterize maximum values, inner active depth, and an iterated-exponential upper timing expression.

### E13 — Arbitrary structural LHSs, wildcard deletion, and literal-free rules

- Provenance: `BOOK:12456`.
- Fact: LHSs may be whole patterns such as `e[e[x_]][y_]` or `e[e][x_[y_]]`; `e[x_][_] -> e[x[e[e][e]][e]]` discards a matched argument; `x_[y_] -> x[y][x[y]]` and `x_ -> x[x]` show literal-free structural rules.

### E14 — Long halting times and proof limits

- Provenance: `BOOK:12457`, with cross-reference `19443`.
- Fact: `e[x_][y_] -> Nest[x,y,r]` can take an order of iterated powers; simple rules may have arbitrarily fast fixed-point times or termination beyond a chosen axiom system. This is analysis, not a halt opcode.

### E15 — Tree transformations are direct structure

- Provenance: `BOOK:12458-12464`, page-912 tree figures.
- Fact: the base and page-119 transformations are drawn directly on trees and early trajectories are tree sequences. Variables replace entire subtrees, not bracket substrings.

### E16 — Exact order dependence and Church-Rosser boundary

- Provenance: `BOOK:12466-12470`, `16530-16540`.
- Fact: `expr /. lhs->rhs` scans the functional representation left to right and avoids overlaps. A technique can restrict application to once. Church-Rosser may make a reached fixed form order-independent, but it does not remove the documented transient order or create branching execution.

### E17 — Combinator history and untyped expression structure

- Provenance: `BOOK:12472-12474`.
- Fact: symbolic systems are historically related to Schönfinkel/Curry combinators. Their lack of built-in object/function type hierarchy is a property of expression use, not permission for host-language `Any`.

### E18 — Deterministic operator evolution versus multiway equations

- Provenance: `BOOK:12476-12484`, `20184`.
- Fact: one-way operator evolution generalizes pattern forms while applying `/.` once per step. Applying an equation in all possible ways belongs to multiway systems. `x_ -> x∘x` yields a balanced tree.

### E19 — Network analog is a separate topology

- Provenance: `BOOK:12486`.
- Fact: every symbolic state is a tree. A general network supports network-substitution analogs, and path-unfolding it to an infinite tree usually does not preserve simple rule application. General evolving graphs remain T29.

### E20 — Cellular-automaton emulation is a compiler relation

- Provenance: `BOOK:8034-8052`, `18500-18512`.
- Fact: symbolic systems can emulate CAs through a structured encoding. The exact compiler has timing `t(t+Length[init]+3)` for CA step `t` and explicitly depends on replacement order. It is not native T20 state or timing.

### E21 — Exact S/K combinator specialization

- Provenance: `BOOK:8568-8606`, `18924-18940`, page-726 rule picture.
- Fact: the ordered rules are `s[x_][y_][z_] -> x[z][y[z]]` and `k[x_][y_] -> x`. S duplicates/rearranges `z`; K deletes `y`. Identity/composition and lambda conversion are derived relations; combinator evolution can be universal.

### E22 — Combinator counts, fixed points, and order

- Provenance: `BOOK:18956-18972`.
- Fact: S/K expressions with `n` leaves number `2^n Catalan(n-1)`, giving `2,4,16,80,448,2688,...`. The Notes analyze fixed forms and state that application order affects behavior. The single-j system supplies another literal/program specialization, not another executor.

### E23 — Generic expression corroboration and universality tests

- Provenance: `BOOK:18130`, `19024`.
- Fact: generic `head[args]` structure corroborates expression-valued heads; testing for expressions with S/K behavior is an analysis for universality, not transition semantics.

### E24 — Algebraic translation and valuation are observers/relations

- Provenance: `BOOK:13129-13135`, `20261`.
- Fact: expression trees may receive numeric valuations or algebraic translations. These interpretations do not replace labeled ordered trees or feed the rewrite engine.

## Construction Model

### State, atom universe, and typed paths

The smallest carrier that preserves both the general expression model and the unary Chapter 3 profile is:

```text
SymbolId      = stable declared atom key
Expression    = Atom(symbol: SymbolId)
              | Apply(
                    head: Expression,
                    arguments: NonEmptyTuple[Expression]
                )

PathEdge      = Head | Argument(index: Natural)
ExpressionPath = Tuple[PathEdge, ...]  # root is ()

ExpressionState = {
    root: finite well-founded Expression
}
```

The owning spec declares a finite `AtomUniverse`; every atom in seed, pattern, and template must belong to it. Variable IDs are a separate typed namespace. `Apply` preserves argument arity and order. The canonical `UnaryApplicationProfile` validates exactly one argument at every application and atom universe `{e}`; combinators use `{s,k}`.

Paths address occurrences, not values. Equal subtrees at two paths are two occurrences. `Head` is not argument zero: preserving its role catches the first canonical rewrite at the seed's head. Cyclic objects, empty argument tuples, undeclared atoms, malformed paths, and objects with observable pointer aliasing are invalid before execution.

### Closed pattern and template data

```text
Pattern =
    LiteralAtom(symbol)
  | Bind(variable)                  # any whole expression
  | AnonymousAny
  | ApplyPattern(head, nonempty ordered arguments)

Template =
    LiteralAtom(symbol)
  | Bound(variable)
  | ApplyTemplate(head, nonempty ordered arguments)

RewriteClause = {
    id: stable ClauseId,
    left: Pattern,
    right: Template
}

OrderedRewriteProgram = {
    atoms: AtomUniverse,
    clauses: NonEmptyTuple[RewriteClause]
}
```

Matching is structural and inert:

- literals compare declared atom IDs;
- application patterns require the same arity and recursively match head then arguments;
- the first `Bind(v)` stores the whole subtree in an immutable `BindingEnvironment`;
- a repeated `Bind(v)` in an extended structural pattern requires semantic subtree equality with the stored value;
- `AnonymousAny` matches without adding an environment entry;
- every `Bound(v)` on the RHS must have been bound on the LHS;
- a bound variable may occur zero, one, or several times in the RHS, supporting deletion, preservation, and duplication.

Base and figure presets use unique LHS binders. Repeated-binder equality is a closed structural feature corroborated by the named Mathematica pattern operation; it does not admit conditions or predicates. Sequence blanks, alternatives, optional/default arguments, attributes such as flat/orderless matching, conditions, delayed evaluation, and RHS computation require explicit future AST members plus conformance evidence. They cannot enter as host callbacks.

Static constructions such as a fixed `Nest[x,y,r]` RHS expand to an ordinary finite template at validation time. There is no evaluator inside instantiation.

### Program-coupled source selection and reads

The authoritative source is `OutermostNonOverlappingPatternMatches(program)`. Selection is deterministic:

```text
select(node, path):
    for clause in program order:
        if structural_match(clause.left, node):
            emit TreeMatch(path, clause.id, node, bindings)
            return                    # prune every descendant

    if node is Apply:
        select(node.head, path + Head)
        for i, argument in left-to-right order:
            select(argument, path + Argument(i))
```

The emitted list is:

- ordered by functional left-to-right discovery;
- pairwise prefix-incomparable;
- maximal under this greedy traversal;
- rule-prioritized at each occurrence;
- scoped to one immutable old-state ID.

This is not an optimization detail. Bottom-up traversal, arguments-before-head, rule-major whole-tree scans, maximum-cardinality packing, an unordered match set, or revisiting a replacement gives a different trajectory.

Each `TreeMatch` is both the firing source and the exact structural read:

```text
TreeMatch = {
    old_state_id,
    path,
    clause_id,
    matched_subtree,
    bindings: OrderedMap[VariableId, Expression]
}
```

The program is coupled only through an inspectable applicability interface. Source and result lookup share one immutable program object; there is no duplicate LHS catalog, hidden scan cursor, matcher function, or rule-family dispatcher.

### Inert result instantiation

`InstantiateTemplate` recursively constructs one replacement per match:

```text
ReplaceSubtree = {
    source: TreeMatch,
    instantiated: Expression,
    derivations: Tuple[NodeDerivation, ...]
}
```

Literal/template application nodes receive creation provenance from `(clause_id, match_path, rhs_path)`. Every `Bound(v)` occurrence copies the bound old subtree into a distinct semantic result occurrence and records:

```text
(old match path + bound-relative path)
    -> (rhs binding-reference occurrence)
    -> (new replacement-relative path)
```

Repeated references may share immutable storage privately, but equality, matching, serialization, and later rewriting observe a tree. Unused bindings and unmatched descendants of a consumed subtree have deletion provenance. No template can mutate an old bound value.

### Fifth sibling update law

`ParallelPrefixFreeTreeReplace` is a new public commit algebra:

1. Validate that every result names the same old state and a path resolving to the recorded matched subtree.
2. Validate one result per selected source, pairwise prefix-incomparable paths, unique paths, valid template trees, and declared atoms.
3. Rebuild the tree once from the old root, replacing a selected path by its instantiated result and otherwise preserving the ordered context.
4. Emit one atomic event containing the ordered match/result list and structural provenance.

Replacing one subtree by one subtree preserves sibling-role indices outside the selected occurrences, but it may change arbitrary depth and leaf count. There is no conflict merge because prefix-free coverage is a precondition, not a last-writer policy.

This law is not:

- T13 `ParallelReplaceConcat`, which consumes every scalar occurrence and concatenates child words;
- T16 `SingleSpliceUpdate`, which replaces exactly one flat interval;
- T17 queue consumption/append;
- fixed-support assignment; or
- a sequence of in-place tree mutations whose later paths see earlier outputs.

It is the fifth evidenced `UPDATE` sibling. A private persistent-tree reconstruction kernel may be shared, but its public invariants remain construction-specific.

### Exact step and outcome semantics

```text
step(spec, old):
    matches = OutermostNonOverlappingPatternMatches(spec.program).select(old)

    if matches is empty:
        return Quiescent(
            reason=NoPatternMatch,
            state=old,
            reference_successor=old,
            events=()
        )

    results = [InstantiateTemplate(clause.right, match.bindings)
               for match in matches]
    new, event = ParallelPrefixFreeTreeReplace.commit(old, results)
    return Advanced(
        state=new,
        events=(event,),
        changed=(new != old)
    )
```

Exact `NestList` reference sampling may request arbitrarily many repeated quiescent frames. `UntilQuiescent` may retain the first quiescent state and then stop without inventing a rewrite. `UntilValueFixed` may also stop after an applicable identity event; it must report a different observation reason. Longer cycles require an explicit cycle observer. Horizon, cancellation, resource exhaustion, invalid data, and internal error are never semantic fixed points.

### Programs, seeds, profiles, and identity

The canonical preset is:

```text
atoms = {e}
rule  = e[x_][y_] -> x[x[y]]
seed  = e[e[e][e]][e][e]
scan  = one functional-left-to-right outermost prefix-free pass
```

The six page-119 programs change only the single RHS recorded in E06. The combinator preset is one ordered program:

```text
s[x_][y_][z_] -> x[z][y[z]]
k[x_][y_]     -> x
```

The documented single-j form and the four operator-evolution examples are additional structured presets. The latter exact rules are `x_ -> x∘x`, `x_∘y_ -> (y∘x)∘y`, `x_∘y_ -> (y∘y)∘(x∘x)`, and `x_∘y_ -> y∘(x∘x)`.

Program identity is its atom universe plus ordered structural clauses. Behaviorally equivalent rules, reordered clauses, duplicate clauses, and alpha-renamed serialized binders are not silently quotienting identities. A canonical binder-normalization codec may be an explicit analysis, but the book provides no numeric rule number.

Every finite valid expression is a possible seed. A seed is independent of the rule program. The one-symbol unary enumeration profile has:

```text
E(k,n) = Catalan(n-1) * k^n
       = Binomial(2n-2,n-1) * k^n / n
```

For `k=1`, `n=1..8` gives `1,1,2,5,14,42,132,429`. For `k=2`, it gives `2,4,16,80,448,2688,16896,109824`. This is a count over structured trees, not permission to execute numeric encodings.

### Representations and observers

- `FunctionalCodec` and `TreeCodec` preserve labeled head/argument roles.
- `PolishCodec` is allowed only with a total domain validator and exact round trip.
- `OneSymbolUnaryBracketCodec` is bijective only for its restricted profile.
- Operator-parenthesis rendering is a view unless a typed operator atom/program is explicitly selected.
- `LeafCount`, structural maximum depth, right-branch depth, bracket raster, expression-size difference, invariant valuation, normal-form detection, causal/lineage tree, and cropped display are downstream observers.
- Hash-consing, memoization, and compact exponent/tower analysis are realization or analysis choices. They never change tree occurrence semantics.

### Independent exact oracles

A separate tiny recursive matcher/rewriter, not production code and not host `ReplaceAll`, established these goldens.

Canonical base trajectory:

```text
t0 e[e[e][e]][e][e]
t1 e[e][e][e[e][e][e]][e]
t2 e[e[e]][e[e[e]][e]][e]
t3 e[e][e[e][e[e[e]][e]]][e]
t4 e[e[e[e][e[e[e]][e]]]][e]
t5 e[e[e][e[e[e]][e]]][e[e[e][e[e[e]][e]]][e]]
```

- At `t0`, the only selected path is `Head`, with `x=e[e][e]` and `y=e`. This catches argument-only addressing and flat-string errors.
- At `t1`, paths `Head/Head` and `Head/Argument(0)/Head` fire disjointly. At `t4`, the root fires.
- `V(e)=0; V(Apply(x,y))=2^V(x)+V(y)` remains exactly 256.
- The first no-match normal form is zero-based `t263 = Nest[e,e,256]`, with 257 leaves and 256 bracket pairs. A 264th pass is not required; the published 264 counts the initial state. A subsequent requested reference sample stutters.
- `e[e][e][e][e][e]` reaches `Nest[e,e,65536]` at zero-based `t=65,554`; this is a slow/analytical conformance witness, not a reason for compact semantic state.

Adversarial one-step goldens:

```text
disjoint:
  e[e][e][e[e][e]]
    -> e[e[e]][e[e[e]]]
  selected paths = Head, Argument(0)

overlap:
  e[e[e][e]][e]
    -> e[e][e][e[e][e][e]]
  selected path = root; nested redex suppressed

newborn deferral:
  e[e[e]][e]
    -> e[e][e[e][e]]
    -> e[e[e[e][e]]]
```

Additional required oracles:

- canonical duplication gives two equal but occurrence-distinct descendants with separate derivations;
- `k[e[e]][e[e][e]] -> e[e]` proves whole-subtree deletion;
- two identical LHS clauses returning `x` and `y` on `e[e[e]][e]` return `e[e]` in that order and `e` when reversed;
- a repeated named binder matches equal subtrees and rejects unequal subtrees in the extended structural profile;
- `e[e[e]]` produces event-free `Quiescent(NoPatternMatch)`;
- an identity clause on `e[e][e]` produces one `Advanced(changed=false)` event;
- malformed/cyclic trees, undeclared atoms, unbound RHS references, invalid argument indices, duplicate match paths, and non-prefix-free commit inputs are rejected;
- parse/render/Polish/bracket codecs round-trip exactly on their declared domains and reject out-of-domain trees;
- semantic tree equality and trajectories ignore internal allocation/hash-consing while provenance preserves occurrence multiplicity.

### Variant and relation disposition

| Candidate | Disposition |
|---|---|
| Page-119 single-rule systems | Native deterministic programs under the same executor |
| S/K and single-j combinators | Native ordered-program specializations; same tree/matcher/update |
| First-application-only technique | Documented selector variant over the same structural matcher; not the canonical all-disjoint pass |
| Deterministic operator evolution | Native broader closed-pattern profile with once-per-step semantics; unsupported host features reject explicitly |
| `//.` standard evaluation/normalization | Repeated-step protocol or observer; never one T20 timestep |
| Church-Rosser/confluence | Relation on alternative rewrite paths/final forms; canonical transient order remains |
| Multiway application of equations | T30 branching successor construction |
| Network substitution/path unfolding | T29 dynamic topology relation; not tree aliasing |
| CA emulation | Compiler with changed representation and timing |
| Lambda/Church numeral compilation | Expressiveness/interpretation relation |
| Valuation, depth, leaf count, brackets, size plots | Observers/codecs |
| Universality and Busy Beaver analyses | Properties/searches over structured programs |

## Corrected Architecture and Goal 2 Handoff

T20 is a SimpleProgram over an explicit recursive tree topology with a transparent tagged expression ALPHABET. FRONTIER performs the old-snapshot ordered maximal prefix-free match selection, NEIGHBORHOOD supplies matched subtrees/bindings, RULE instantiates replacement trees, and a tree-capable UPDATE applies the prefix-free path writes atomically. A whole expression may also have a lossless structured codec, but no opaque singleton/callback may hide matching or replacement.

Revised G2-T20 adds recursive expression/path/pattern/template schemas, program-coupled tree FRONTIER, binding access, typed subtree replacements, and a prefix-free tree UPDATE strategy inside the common runner. It removes the fifth-law/symbolic-executor framing and the blanket prohibition on transparent structured values while retaining traversal, overlap, duplication/deletion, quiescence, identity, provenance, and exact trajectory oracles.

The historical API/handoff below remains evidence provenance; this section governs its executor/class classification.

## Historical Current API Fit (Superseded by Architecture Audit)

| T20 responsibility | Current proposal fit | Required conclusion |
|---|---|---|
| Finite expression tree | `simple_programs.md` state is dense `D -> A` with rank-0..3 shape | SEMANTIC MISMATCH; add a native tree carrier |
| Atom values | Explicit symbolic alphabets can name finite atoms | PARAMETERIZATION only; atoms do not encode applications, variables, or entire trees |
| Tree occurrences | Lattice coordinates and selector loci have no head/argument roles | PRINCIPLED EXTENSION: typed `ExpressionPath` |
| Active source | Frontier is described as writable next coordinates | SEMANTIC MISMATCH; program-coupled pattern matches are firing sources |
| Reads | Neighborhoods gather fixed coordinate stencils | SEMANTIC MISMATCH; read is matched structure plus bindings |
| Rule | Scalar-return tables/formulas | SEMANTIC MISMATCH; closed structural clauses and inert templates |
| Result | Per-target scalar value | SEMANTIC MISMATCH; typed subtree replacement with derivations |
| Update | Fixed-support parallel copy/assign | SEMANTIC MISMATCH; add prefix-free atomic tree replacement |
| Boundaries | Spatial boundary policies | NOT APPLICABLE to finite trees |
| Trace | Fixed `[t,x,y,z]` extent | SEMANTIC MISMATCH; ragged trees, paths, matches, and lineage precede lowering |
| Orchestration | Source/read/result/update separation | DIRECT at the responsibility level once each member is construction-bearing |
| Seed/program/horizon separation | Already a stated responsibility | DIRECT; preserve it without a symbolic family branch |

T13 contributes ordered occurrence/lineage ideas, and T16 contributes program-coupled applicability and ordered priority. Neither contributes an equivalent source coverage or update. No earlier stage is reopened.

## Historical Current Runtime Fit (Superseded by Architecture Audit)

| Runtime area | Finding | T20 disposition |
|---|---|---|
| `alphabets.py` | Finite explicit symbolic scalar values | Reuse only for `SymbolId` declaration; never put a whole tree in one scalar |
| `loci.py` | Rank-0..3 coordinates, finite universes, mask selectors | Cannot address head/argument tree paths |
| `neighborhoods.py` | Coordinate-relative/current-history gathers | Not a structural pattern matcher |
| `frontiers.py` | Only full time-slice frontier | No pattern source or overlap semantics |
| `rules.py` | `Any`, callable formula rules, named families | Reject for T20; add closed pattern/template data |
| `specs.py` | Fixed shape, loosely typed rule, six family resolver | Cannot validate trees/program coupling; family resolver must not grow |
| `rollout.py` | Family switches, NumPy arrays, scalar writes, fixed frames | No reusable T20 execution path beyond old-snapshot intent |
| `datasets.py` | Integer rule IDs and `np.stack` batching | Downstream lowering only; ragged trees require explicit collation |
| tests | No expression/pattern/tree rewrite tests | Add independent semantic conformance suite |

The runtime contains no occurrence of a construction-bearing tree, pattern, binding, or rewrite primitive. A host symbolic package is useful only as an optional differential oracle; calling it from production would conceal exactly the semantics T20 is meant to represent.

## Historical Principles Audit (Superseded by Architecture Audit)

- **Principle 0:** a typed tree matcher, binding environment, template instantiator, and prefix-free commit expose the construction. `expression -> host_replace(expression)` does not.
- **Principles 1-2:** state, path, source, read, result, and update are all explicit. Atom values do not smuggle topology or programs.
- **Principles 3-4:** the one-pass event is atomic; bindings and paths refer to one old snapshot; newborns wait.
- **Principle 5:** structural patterns and templates are closed sums. No `Any`, predicates, conditions, or RHS callbacks.
- **Principles 6-8:** native finite trees, computation realization, ragged trace, bracket raster, and fixed-capacity batches remain separate.
- **Principles 9-10:** the base, six figure rules, S/K, j, and operator examples are strict presets over generic data semantics, not family-specific rollout names.
- **Principle 11:** program-coupled applicability is honest coupling through one immutable program, not a duplicated selector/rule table.
- **Principle 12:** `Advanced`, no-match quiescence, value-fixed observation, cycles, horizon, and errors are trace-distinct.
- **Principles 13-17:** compilers, codecs, confluence, normalization, and visualization are explicit downstream relations; none substitutes for native execution.

Rejected shortcuts:

- flattening to brackets, Polish tokens, strings, a CA row, a scalar code, or a padded tensor as native state;
- regex, substring, host AST replacement, evaluator attributes, arbitrary matcher/template functions, or `Any`;
- a first-match-only flat splice for the canonical pass;
- overlapping or unordered match sets, bottom-up scans, sequential in-place mutation, or same-pass newborn rescanning;
- mutable DAG alias semantics or pointer-identity matching;
- fixed depth/node capacity, silent truncation, or display cropping;
- treating `//.`, confluence, or state equality as the one-step transition;
- compiling through T13/T16/T29/T30/CA or adding a `symbolic` rollout branch.

## Historical Detailed Implementation Plan (Superseded by Architecture Audit)

1. Closed the exact-name, alias, mechanism, caption/figure, Notes, actual Index, split, history, implementation, pattern, order, overlap, fixed-point, observer, variant, and compiler searches with zero unresolved candidates.
2. Reconstructed general and unary expression grammars, atom/variable namespaces, typed paths, structural patterns, binding equality, templates, ordered programs, seeds, counts, and representation boundaries.
3. Derived the functional outermost preorder selector, rule priority, prefix-free coverage, old-snapshot bindings, newborn deferral, inert instantiation, duplication/deletion provenance, and quiescent reference outcome.
4. Challenged T13 and T16 reuse and established `ParallelPrefixFreeTreeReplace` as a fifth update sibling without reopening either construction.
5. Reproduced the canonical trajectory, invariant, fixed forms/timings, expression counts, overlap/disjoint/newborn cases, S/K deletion, priority, identity, no-match, validation, and codec oracles independently.
6. Audited every current API/runtime responsibility and identified the exact tree, matcher, result, update, outcome, and trace additions required for Goal 2.
7. Dispositioned combinators and deterministic operator evolution as native profiles; normalization, confluence, multiway, networks, emulations, valuations, and views remain explicit relations.
8. Reintegrated the new decisions into the global plan, evidence index, and design ledger; no completed earlier stage is contradicted.

## Historical Goal 2 Implementation Stage (Superseded by Corrected Handoff)

### G2-T20 — Ordered expression trees and atomic nonoverlapping pattern passes

Dependencies: shared typed outcomes and source/read/result/update orchestration; T13 lineage concepts; T16 program-coupled applicability. Do not depend on a T13/T16 executor or host symbolic engine.

1. Add immutable `Expression`, `AtomUniverse`, `ExpressionPath`, structural equality/hash, validators, and canonical functional/tree codecs in a tree-owned module. Keep occurrence identity out of rule-visible values.
2. Add closed `Pattern`, `Template`, `RewriteClause`, `OrderedRewriteProgram`, and profile validators. Implement literal/application/bind/anonymous matching, repeated-binder equality, and inert template substitution without callbacks.
3. Add `OutermostNonOverlappingPatternMatches`, `TreeMatch`, and `BindingEnvironment`. Prove traversal order, rule priority, head eligibility, maximal prefix-free output, old-state scoping, and deterministic serialization.
4. Add `ReplaceSubtree`, structural derivation records, and `ParallelPrefixFreeTreeReplace`. Validate exact coverage and prefix independence, rebuild atomically, and preserve duplication/deletion/context lineage.
5. Route these members through the shared generic transition orchestration. Return `Advanced(changed=...)` for any applicable pass and event-free `Quiescent(NoPatternMatch)` otherwise; add explicit reference-stutter and stop observers without a family branch.
6. Add strict presets for the base rule, six page-119 rules, S/K, single-j, and four operator examples. Keep seeds separate and provide no invented numeric rule codec.
7. Add functional, tree, Polish, and restricted one-symbol bracket codecs plus leaf/depth/value/size observers outside execution. All lowerings must validate domains and round-trip.
8. Migrate raw result/episode handling to admit ragged structured states and events before optional batching. Dense padding or tokenization must be an explicit downstream transform with masks and original paths.
9. Add the exact oracle suite in this stage, using hard-coded goldens and an independent tiny test oracle. Optional Wolfram differential tests are diagnostic only and never a production dependency.
10. Audit exports, serialization, docs, dataset collation, and generic executor dispatch. Search production for `ReplaceAll`, regex execution, callbacks, `Any` terms/results, family-name branches, fixed tree limits, hidden cursors, and unlabeled flattening.

Completion requires:

- every tree/path/pattern/template/program invariant to reject malformed input before execution;
- exact t0-t5, selected-path, invariant, first-fixed, count, disjoint, overlap, newborn, duplication, deletion, priority, repeated-binding, identity, no-match, and provenance tests;
- tree/Polish/bracket round trips and out-of-domain rejection;
- equality/allocation-independence and optional persistent-sharing tests;
- reference stutter and explicit stop/horizon/cycle distinctions;
- no changes to T13/T16 semantics and no symbolic-specific rollout;
- all current and new tests passing with a clean static no-cheating audit.

## Historical No-Cheating Checks (Superseded where they prohibit transparent structured values)

- No symbolic-family rollout, host `ReplaceAll`, regex/text execution, formula/matcher/template callback, evaluator, or `Any` term/result.
- No whole expression packed into a scalar alphabet member, CA row, Polish token stream, bracket string, numeric valuation, or integer rule code for native execution.
- No fixed depth, node budget, padded/ring tree, silent crop, or fake maximum.
- No hidden scan cursor, candidate queue, binding table, rule priority, simplifier, memoized state, or stop flag.
- No descendants selected beneath a chosen ancestor; no unordered/overlapping commit; no sequential address drift; no newborn rescanning.
- No pointer/DAG alias observed by matching or mutation; duplicated bindings remain distinct occurrences.
- No first-match-only T16 splice or all-occurrence T13 concatenation relabeled as tree rewriting.
- No `//.` normalization, confluence quotient, value-fixed observer, multiway branch, network unfolding, or CA compiler presented as one canonical step.
- No brackets, tree drawings, size/depth plots, valuations, or cropped rasters feeding execution.

## Completion Requirements

- [x] All direct names, aliases, captions/figures, Notes, actual Index entries, splits, history, variants, observers, and cross-references are resolved with zero silent remainder.
- [x] Expression topology, atom/variable domains, paths, patterns, bindings, traversal, rule priority, overlap, instantiation, commit, seed, successor, and fixed behavior are reconstructed.
- [x] Exact trajectories, fixed-point timing convention, counts, invariant, disjoint/overlap/newborn, duplication/deletion, priority, identity/no-match, validation, codec, and provenance oracles are specified.
- [x] Current API/runtime fit and T13/T16 reuse/divergence are explicit.
- [x] Principle 0 and every no-cheating pressure are audited.
- [x] Goal 2 implementation/conformance handoff and global reintegration are complete.

## Architecture-Reclosed Stage Result

**COMPLETE.** T20 uses a discrete recursive-tree DOMAIN/topology, typed match loci and structural access, closed pattern/template RULE data, and a prefix-free tree UPDATE policy inside the common runner. Transparent structured values are native; opaque host evaluation and a symbolic executor remain rejected.

## Historical Stage Results (Evidence Retained; Architecture Superseded)

T20 is complete. The conservative combined search dispositioned 272 direct/alias occurrences on 166 lines; the exact-name audit independently closed all 73 occurrences on 60 lines. Twenty-four canonical evidence groups cover the core, all figures/captions, Notes, actual Index routes, representations, combinators, operator evolution, order/confluence, fixed-point properties, and compiler boundaries with zero unresolved native-mechanics candidates.

The construction is a finite ordered expression tree plus an immutable ordered structural rewrite program. One step greedily selects the functional-left-to-right outermost prefix-free match set from the old tree, instantiates inert RHS templates from whole-subexpression bindings, and atomically replaces every selected subtree. This adds `ExpressionPath`, closed pattern/template data, explicit bindings, typed match/result provenance, and `ParallelPrefixFreeTreeReplace` as a fifth update law. No-match is exact quiescence; applicable identity remains an event.

The canonical t0-t5 trajectory, head-path first match, disjoint and nested overlap sets, newborn deferral, invariant 256, initial-inclusive 264/65,555 timing convention, Catalan counts, S/K deletion/duplication, rule priority, identity, and no-match cases close the implementation handoff. T13 lineage and T16 program coupling compose at the responsibility level, but their update laws remain distinct. No prior stage is reopened.

## Historical Integration Results (Superseded by Architecture Audit)

- Added native finite expression trees, typed head/argument paths, structural pattern/template programs, binding reads, and deterministic prefix-free source selection to the semantic inventory.
- Added `ParallelPrefixFreeTreeReplace` as the fifth public update sibling and structural duplication/deletion lineage to trace requirements.
- Refined deterministic successors with event-free no-match quiescence and applicable unchanged events.
- Recorded restricted representation codecs, structured expression counts without rule numbering, and deterministic operator/combinator profiles.
- Preserved T01/T09/T12/T13/T16/T17/T19 conclusions. General networks remain T29; branching rewrites remain T30.
- Next stage: T27, Geometric Replacement And Fractal Systems.
