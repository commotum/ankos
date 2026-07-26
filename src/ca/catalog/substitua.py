"""Whole-program constructors for structural substitution and growth.

This module owns audited catalog spellings whose dominant mechanic matches,
replaces, grows, deletes, or branches structure.  It does not own structural
identity primitives, component mechanics, metadata, application, conflict
repair, or execution dispatch. The implementations compose the five component
algebras into ordinary ``SimpleProgram`` values.

Each canonical family is an explicitly typed, transparent five-component
constructor.  Bounded presets below compile their semantic parameters into
those same five components; true aliases delegate to their canonical
constructor.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product as cartesian_product
from typing import TypeVar

from .. import alphabets, frontiers, loci, neighborhoods, rules, seeds
from ..alphabets import Alphabet
from ..frontiers import WritableRegion
from ..neighborhoods import ReadableRegion
from ..program import SimpleProgram
from ..rules import Rule
from ..seeds import Seed


C = TypeVar("C")
V = TypeVar("V")
W = TypeVar("W")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Phase 1. Canonical families
# ---------------------------------------------------------------------------


def append_only_sequence_generation(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF002 / F002: append finite output while preserving prior support."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def context_dependent_substitution(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF005 / F005: replace items from bounded old-generation context."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def first_passage_aggregation(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF015 / F016: attach a walker irreversibly at first contact."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def front_delete_rear_append_system(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF016 / F017: delete a prefix and append its selected production."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def global_score_sequential_placement(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF019 / F020: score globally and commit one structural placement."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def history_dependent_growth_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF022 / F023: grow support using occupancy and provenance history."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def indexed_history_recurrence(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF023 / F024: append a term read through value-addressed history."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def iterated_erasure_process(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF025 / F026: repeatedly erase selected ranked survivors."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def local_graph_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF028 / F029: replace graph matches through explicit interfaces."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def moving_frontier_shell_accretion(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF031 / F032: append geometric strips along a moving open rim."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def multiway_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF033 / F034: expose every witnessed successor before quotienting."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def parallel_independent_substitution(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF037 / F038: assemble independent offspring in one generation."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def parallel_network_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF038 / F040: commit compatible graph patches in parallel."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def random_functional_graph_construction(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF043 / F046: denote a random one-successor graph construction."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def structural_pattern_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """SPF049 / F052: rewrite structural matches with explicit scan conflicts."""

    return SimpleProgram(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 2. Presets
# ---------------------------------------------------------------------------

SemanticWord = tuple[alphabets.SemanticValue, ...]
WordProduction = tuple[alphabets.SemanticValue, SemanticWord]
ContextProduction = tuple[SemanticWord, SemanticWord]


def _certificate(
    kind: rules.CertificateKind,
    label: str,
) -> rules.Certificate:
    return rules.Certificate(kind, rules.literal_expr(label))


def _evidence_template(
    source_evidence: rules.EvidenceTerm | None,
) -> rules.EvidenceTerm | None:
    if source_evidence is None:
        return None
    if type(source_evidence) is not rules.EvidenceTerm:
        raise TypeError("source_evidence must be an EvidenceTerm")
    return rules.EvidenceTerm(
        "source-evidence",
        (source_evidence,),
    )


def _base_components(
    value: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
) -> tuple[
    loci.FiniteConfiguration,
    seeds.Seed,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
    rules.RuleContract,
]:
    source = loci.record_configuration((("state", value),))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    contract = rules.RuleContract(
        source.contract,
        alphabet.value_profile,
        readable.result_shape,
        readable.join_shape,
        writable.effect_profile,
    )
    return (
        source,
        seeds.exact(source, value_profile=alphabet.value_profile),
        alphabet,
        writable,
        readable,
        contract,
    )


def _expression_components(
    value: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    expression: rules.RuleExpr,
    *,
    label: str,
    source_evidence: rules.EvidenceTerm | None = None,
) -> tuple[
    seeds.Seed,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
    rules.Rule,
]:
    if type(expression) is not rules.RuleExpr:
        raise TypeError(f"{label} expression must be a RuleExpr")
    (
        _,
        seed,
        alphabet,
        frontier,
        neighborhood,
        contract,
    ) = _base_components(value, alphabet)
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (expression,),
        ),
        contract=contract,
        witness=rules.literal_expr("closed-expression"),
        provenance=("closed-expression",),
        certificate_template=_evidence_template(source_evidence),
    )
    return seed, alphabet, frontier, neighborhood, rule


def _conditional_components(
    value: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    condition: rules.RuleExpr,
    expression: rules.RuleExpr,
    *,
    label: str,
    source_evidence: rules.EvidenceTerm | None = None,
) -> tuple[
    seeds.Seed,
    alphabets.Alphabet,
    frontiers.WritableRegion,
    neighborhoods.ReadableRegion,
    rules.Rule,
]:
    if type(condition) is not rules.RuleExpr:
        raise TypeError(f"{label} condition must be a RuleExpr")
    if type(expression) is not rules.RuleExpr:
        raise TypeError(f"{label} expression must be a RuleExpr")
    (
        _,
        seed,
        alphabet,
        frontier,
        neighborhood,
        contract,
    ) = _base_components(value, alphabet)
    derivation = rules.DerivationClauseResult(
        (
            rules.ExistingDispositionPlan(
                rules.capability_index(0),
                rules.DispositionAction.REPLACE,
                expression,
            ),
        ),
        (),
        rules.Progress.ADVANCED,
        rules.Continue(),
        rules.literal_expr("conditional-replacement"),
        ("conditional-replacement",),
        _certificate(
            rules.CertificateKind.DERIVATION,
            "conditional-replacement:derived",
        ),
        certificate_template=_evidence_template(source_evidence),
    )
    terminal = rules.NoSuccessorClauseResult(
        rules.NoSuccessorOutcome.TERMINAL,
        rules.literal_expr("condition-false"),
        rules.literal_expr("condition-false"),
        ("conditional-replacement:terminal",),
        _certificate(
            rules.CertificateKind.TERMINALITY,
            "conditional-replacement:terminal",
        ),
    )
    rule = rules.clause_kernel(
        (
            rules.RuleClause(condition, derivation),
            rules.RuleClause(rules.literal_expr(True), terminal),
        ),
        contract=contract,
        completeness_evidence=_certificate(
            rules.CertificateKind.COMPLETENESS,
            "conditional-replacement:complete",
        ),
        selection=rules.ClauseSelection.FIRST,
    )
    return seed, alphabet, frontier, neighborhood, rule


def _semantic_index(
    values: tuple[alphabets.SemanticValue, ...],
    needle: alphabets.SemanticValue,
) -> int | None:
    for index, value in enumerate(values):
        if alphabets.semantic_equal(value, needle):
            return index
    return None


def _require_symbols(
    symbols: tuple[alphabets.SemanticValue, ...],
    *,
    label: str,
) -> alphabets.Alphabet:
    if type(symbols) is not tuple or not symbols:
        raise ValueError(f"{label} symbols must be a nonempty tuple")
    alphabet = alphabets.enum(symbols)
    for index, symbol in enumerate(symbols):
        if _semantic_index(symbols[:index], symbol) is not None:
            raise ValueError(f"{label} symbols must be semantically distinct")
    return alphabet


def _require_word_members(
    word: object,
    symbols: tuple[alphabets.SemanticValue, ...],
    *,
    label: str,
    nonempty: bool = False,
) -> SemanticWord:
    if type(word) is not tuple:
        raise TypeError(f"{label} must be an immutable tuple")
    if nonempty and not word:
        raise ValueError(f"{label} cannot be empty")
    for item in word:
        if _semantic_index(symbols, item) is None:
            raise ValueError(f"{label} contains a value outside symbols")
    return word


def _same_semantic_members(
    left: tuple[alphabets.SemanticValue, ...],
    right: tuple[alphabets.SemanticValue, ...],
) -> bool:
    return len(left) == len(right) and all(
        _semantic_index(right, item) is not None for item in left
    )


def _word_production_map(
    symbols: tuple[alphabets.SemanticValue, ...],
    productions: object,
    *,
    label: str,
    allow_empty: bool,
) -> alphabets.ValueNode:
    if type(productions) is not tuple or not productions:
        raise ValueError(f"{label} productions must be a nonempty tuple")
    keys: list[alphabets.SemanticValue] = []
    entries: list[alphabets.ValueNode] = []
    outputs: list[SemanticWord] = []
    for entry in productions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError(f"{label} production entries must be pairs")
        key, output = entry
        if _semantic_index(symbols, key) is None:
            raise ValueError(f"{label} production key is outside symbols")
        if _semantic_index(tuple(keys), key) is not None:
            raise ValueError(f"{label} production keys must be unique")
        checked_output = _require_word_members(
            output,
            symbols,
            label=f"{label} production output",
            nonempty=not allow_empty,
        )
        keys.append(key)
        outputs.append(checked_output)
        entries.append(
            alphabets.map_entry_value(
                key,
                alphabets.word_value(checked_output, tag="symbols"),
            )
        )
    if not _same_semantic_members(tuple(keys), symbols):
        raise ValueError(f"{label} productions must be total on symbols")
    return alphabets.map_value(tuple(entries), tag="word-productions")


def _context_production_map(
    symbols: tuple[alphabets.SemanticValue, ...],
    productions: object,
    *,
    width: int,
    label: str,
    allow_empty: bool,
) -> alphabets.ValueNode:
    if type(productions) is not tuple or not productions:
        raise ValueError(f"{label} productions must be a nonempty tuple")
    keys: list[alphabets.ValueNode] = []
    entries: list[alphabets.ValueNode] = []
    for entry in productions:
        if type(entry) is not tuple or len(entry) != 2:
            raise TypeError(f"{label} production entries must be pairs")
        raw_key, output = entry
        key = _require_word_members(
            raw_key,
            symbols,
            label=f"{label} production key",
        )
        if len(key) != width:
            raise ValueError(
                f"{label} production keys must have width {width}"
            )
        checked_output = _require_word_members(
            output,
            symbols,
            label=f"{label} production output",
            nonempty=not allow_empty,
        )
        key_value = alphabets.word_value(key, tag="symbols")
        if _semantic_index(tuple(keys), key_value) is not None:
            raise ValueError(f"{label} production keys must be unique")
        keys.append(key_value)
        entries.append(
            alphabets.map_entry_value(
                key_value,
                alphabets.word_value(checked_output, tag="symbols"),
            )
        )
    expected = tuple(
        alphabets.word_value(key, tag="symbols")
        for key in cartesian_product(symbols, repeat=width)
    )
    if not _same_semantic_members(tuple(keys), expected):
        raise ValueError(
            f"{label} productions must cover every width-{width} context"
        )
    return alphabets.map_value(tuple(entries), tag="context-productions")


def _require_rank_two_field(
    value: object,
    *,
    label: str,
) -> tuple[
    alphabets.ValueNode,
    tuple[str, ...],
    tuple[int, ...],
    tuple[alphabets.SemanticValue, ...],
]:
    if type(value) is not alphabets.ValueNode:
        raise TypeError(f"{label} must be a ValueNode")
    axes, shape, cells = alphabets.grid_field_parts(value)
    if len(axes) != 2:
        raise ValueError(f"{label} must be a rank-2 grid field")
    return value, axes, shape, cells


def _mosaic_production_map(
    source: alphabets.ValueNode,
    productions: object,
    *,
    label: str,
    expected_keys: tuple[alphabets.SemanticValue, ...] | None = None,
    require_closed_keys: bool = False,
) -> alphabets.ValueNode:
    _, source_axes, _, _ = _require_rank_two_field(source, label=f"{label} seed")
    if (
        type(productions) is not alphabets.ValueNode
        or productions.kind is not alphabets.ValueKind.MAP
    ):
        raise TypeError(f"{label} productions must be a MAP ValueNode")
    pairs = alphabets.map_entries(productions)
    if not pairs:
        raise ValueError(f"{label} productions cannot be empty")
    keys = tuple(key for key, _ in pairs)
    if expected_keys is not None and not _same_semantic_members(
        keys,
        expected_keys,
    ):
        raise ValueError(f"{label} productions do not cover the declared keys")
    common_shape: tuple[int, ...] | None = None
    produced_cells: list[alphabets.SemanticValue] = []
    for _, raw_tile in pairs:
        _, axes, shape, cells = _require_rank_two_field(
            raw_tile,
            label=f"{label} production tile",
        )
        if axes != source_axes:
            raise ValueError(
                f"{label} production axes must match the seed axes"
            )
        if common_shape is None:
            common_shape = shape
        elif shape != common_shape:
            raise ValueError(
                f"{label} production tiles must share one shape"
            )
        produced_cells.extend(cells)
    if require_closed_keys and any(
        _semantic_index(keys, cell) is None for cell in produced_cells
    ):
        raise ValueError(
            f"{label} production cells must remain inside the production keys"
        )
    return productions


def _context_mosaic_production_map(
    source: alphabets.ValueNode,
    symbols: tuple[alphabets.SemanticValue, ...],
    productions: object,
) -> alphabets.ValueNode:
    _, source_axes, _, _ = _require_rank_two_field(
        source,
        label="context-dependent-substitution-2d seed",
    )
    if (
        type(productions) is not alphabets.ValueNode
        or productions.kind is not alphabets.ValueKind.MAP
    ):
        raise TypeError(
            "context-dependent-substitution-2d productions must be a MAP "
            "ValueNode"
        )
    pairs = alphabets.map_entries(productions)
    keys: list[alphabets.ValueNode] = []
    common_shape: tuple[int, ...] | None = None
    for raw_key, raw_tile in pairs:
        if (
            type(raw_key) is not alphabets.ValueNode
            or raw_key.kind is not alphabets.ValueKind.WORD
            or raw_key.tag != "mosaic-context"
            or len(raw_key.items) != 4
        ):
            raise ValueError(
                "context-dependent-substitution-2d keys must be four-item "
                "mosaic-context words"
            )
        _require_word_members(
            raw_key.items,
            symbols,
            label="context-dependent-substitution-2d context",
        )
        keys.append(raw_key)
        _, axes, shape, cells = _require_rank_two_field(
            raw_tile,
            label="context-dependent-substitution-2d production tile",
        )
        if axes != source_axes:
            raise ValueError(
                "context-dependent-substitution-2d tile axes must match seed"
            )
        if common_shape is None:
            common_shape = shape
        elif shape != common_shape:
            raise ValueError(
                "context-dependent-substitution-2d tiles must share one shape"
            )
        _require_word_members(
            cells,
            symbols,
            label="context-dependent-substitution-2d tile",
        )
    expected = tuple(
        alphabets.word_value(context, tag="mosaic-context")
        for context in cartesian_product(symbols, repeat=4)
    )
    if not _same_semantic_members(tuple(keys), expected):
        raise ValueError(
            "context-dependent-substitution-2d productions must cover "
            "every four-symbol context"
        )
    return productions


def constant_digit_sequence(
    *,
    base: int,
    prefix: tuple[int, ...],
    next_digit: rules.RuleExpr,
    source_evidence: rules.EvidenceTerm,
) -> SimpleProgram:
    """Build T40's append-only digit-sequence branch.

    ``next_digit`` evaluates over ``observation(0)``, the complete current
    ``digits`` word.  ``source_evidence`` is retained as closed provenance
    evidence; the constructor does not claim to prove the represented
    mathematical constant.  Generic application validates the evaluated digit
    against the declared base before any successor is committed.
    """

    if type(base) is not int or base < 2:
        raise ValueError("constant-digit base must be an integer >= 2")
    if (
        type(prefix) is not tuple
        or not prefix
        or any(
            type(digit) is not int or digit < 0 or digit >= base
            for digit in prefix
        )
    ):
        raise ValueError(
            "constant-digit prefix must be a nonempty tuple of in-base digits"
        )
    if type(next_digit) is not rules.RuleExpr:
        raise TypeError("next_digit must be a RuleExpr")
    _evidence_template(source_evidence)
    state = alphabets.word_value(prefix, tag="digits")
    output = rules.concatenate(
        rules.observation(0),
        rules.word_value("digits", next_digit),
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        state,
        alphabets.word(alphabets.int_range_alphabet(base)),
        output,
        label="constant-digit-sequence",
        source_evidence=source_evidence,
    )
    return append_only_sequence_generation(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def neighbor_dependent_substitution(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[ContextProduction, ...],
) -> SimpleProgram:
    """Replace every overlapping open-right pair from one old generation."""

    symbol_alphabet = _require_symbols(
        symbols,
        label="neighbor-dependent-substitution",
    )
    initial = _require_word_members(
        initial,
        symbols,
        label="neighbor-dependent-substitution initial",
    )
    table = _context_production_map(
        symbols,
        productions,
        width=2,
        label="neighbor-dependent-substitution",
        allow_empty=False,
    )
    source = alphabets.word_value(initial, tag="symbols")
    source_expr = rules.observation(0)
    windows = rules.sliding_windows(
        source_expr,
        0,
        1,
        rules.SequenceBoundary.FIXED,
        exterior=rules.literal_expr(symbols[0]),
    )
    open_right_pairs = rules.slice_items(
        windows,
        rules.literal_expr(0),
        rules.subtract(rules.length(source_expr), rules.literal_expr(1)),
    )
    output = rules.flat_map_lookup(
        open_right_pairs,
        rules.literal_expr(table),
    )
    condition = rules.less_equal(
        rules.literal_expr(2),
        rules.length(source_expr),
    )
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        source,
        alphabets.word(symbol_alphabet),
        condition,
        output,
        label="neighbor-dependent-substitution",
    )
    return context_dependent_substitution(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def context_dependent_substitution_2d(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram:
    """Apply a periodic NW/N/W/self contextual mosaic substitution."""

    _require_symbols(symbols, label="context-dependent-substitution-2d")
    initial, _, _, cells = _require_rank_two_field(
        initial,
        label="context-dependent-substitution-2d initial",
    )
    _require_word_members(
        cells,
        symbols,
        label="context-dependent-substitution-2d initial cells",
    )
    productions = _context_mosaic_production_map(
        initial,
        symbols,
        productions,
    )
    output = rules.mosaic_substitute(
        rules.observation(0),
        rules.literal_expr(productions),
        offsets=((-1, -1), (-1, 0), (0, -1), (0, 0)),
        boundary=rules.SequenceBoundary.PERIODIC,
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        initial,
        alphabets.field(),
        output,
        label="context-dependent-substitution-2d",
    )
    return context_dependent_substitution(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def tag_system(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    n: int,
    appendants: tuple[ContextProduction, ...],
) -> SimpleProgram:
    """Delete ``n`` leading symbols and append the selected whole-prefix word."""

    symbol_alphabet = _require_symbols(symbols, label="tag-system")
    if type(n) is not int or n <= 0:
        raise ValueError("tag-system n must be a positive integer")
    initial = _require_word_members(
        initial,
        symbols,
        label="tag-system initial",
    )
    table = _context_production_map(
        symbols,
        appendants,
        width=n,
        label="tag-system",
        allow_empty=True,
    )
    source = alphabets.word_value(initial, tag="symbols")
    source_expr = rules.observation(0)
    prefix = rules.slice_items(
        source_expr,
        rules.literal_expr(0),
        rules.literal_expr(n),
    )
    tail = rules.slice_items(
        source_expr,
        rules.literal_expr(n),
        rules.length(source_expr),
    )
    appendant = rules.map_lookup(
        rules.literal_expr(table),
        prefix,
        rules.literal_expr(alphabets.word_value((), tag="symbols")),
    )
    condition = rules.less_equal(
        rules.literal_expr(n),
        rules.length(source_expr),
    )
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        source,
        alphabets.word(symbol_alphabet),
        condition,
        rules.concatenate(tail, appendant),
        label="tag-system",
    )
    return front_delete_rear_append_system(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def cyclic_tag_system(
    *,
    initial: tuple[bool, ...],
    blocks: tuple[tuple[bool, ...], ...],
    initial_phase: int = 0,
    trigger: bool = True,
) -> SimpleProgram:
    """Delete one bit, conditionally append the scheduled block, advance phase."""

    if (
        type(initial) is not tuple
        or any(type(bit) is not bool for bit in initial)
    ):
        raise TypeError("cyclic-tag initial must be a tuple of booleans")
    if (
        type(blocks) is not tuple
        or not blocks
        or any(
            type(block) is not tuple
            or any(type(bit) is not bool for bit in block)
            for block in blocks
        )
    ):
        raise ValueError(
            "cyclic-tag blocks must be a nonempty tuple of boolean tuples"
        )
    if (
        type(initial_phase) is not int
        or initial_phase < 0
        or initial_phase >= len(blocks)
    ):
        raise ValueError("cyclic-tag initial_phase is outside the block cycle")
    if type(trigger) is not bool:
        raise TypeError("cyclic-tag trigger must be a boolean")
    state = alphabets.record_value(
        (
            ("phase", initial_phase),
            ("word", alphabets.word_value(initial, tag="bits")),
        ),
        tag="front-delete-rear-append-state",
    )
    state_expr = rules.observation(0)
    word = rules.record_field(state_expr, "word")
    phase = rules.record_field(state_expr, "phase")
    head = rules.item_at(
        word,
        rules.literal_expr(0),
        rules.literal_expr(False),
    )
    tail = rules.slice_items(
        word,
        rules.literal_expr(1),
        rules.length(word),
    )
    scheduled = rules.lookup(
        tuple(
            alphabets.word_value(block, tag="bits")
            for block in blocks
        ),
        phase,
    )
    appended = rules.conditional(
        rules.equal(head, rules.literal_expr(trigger)),
        scheduled,
        rules.literal_expr(alphabets.word_value((), tag="bits")),
    )
    updated = rules.record_update(
        rules.record_update(
            state_expr,
            "word",
            rules.concatenate(tail, appended),
        ),
        "phase",
        rules.modulo(
            rules.add(phase, rules.literal_expr(1)),
            len(blocks),
        ),
    )
    alphabet = alphabets.record(
        (
            ("phase", alphabets.int_range_alphabet(len(blocks))),
            ("word", alphabets.word(alphabets.boolean())),
        )
    )
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        state,
        alphabet,
        rules.less_than(rules.literal_expr(0), rules.length(word)),
        updated,
        label="cyclic-tag-system",
    )
    return front_delete_rear_append_system(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def recursive_sequence(
    *,
    prefix: tuple[int | Fraction, ...],
    coefficients: tuple[int | Fraction, ...],
    bias: int | Fraction | None = None,
) -> SimpleProgram:
    """Append one exact affine recurrence term; coefficients are lag-one first."""

    if (
        type(prefix) is not tuple
        or not prefix
        or any(type(value) not in (int, Fraction) for value in prefix)
    ):
        raise ValueError(
            "recursive-sequence prefix must be a nonempty exact numeric tuple"
        )
    if (
        type(coefficients) is not tuple
        or not coefficients
        or any(type(value) not in (int, Fraction) for value in coefficients)
    ):
        raise ValueError(
            "recursive-sequence coefficients must be a nonempty exact "
            "numeric tuple"
        )
    numeric_type = type(prefix[0])
    if any(type(value) is not numeric_type for value in prefix):
        raise TypeError("recursive-sequence prefix must use one exact type")
    if any(type(value) is not numeric_type for value in coefficients):
        raise TypeError(
            "recursive-sequence coefficients must match the prefix type"
        )
    effective_bias: int | Fraction
    if bias is None:
        effective_bias = (
            0 if numeric_type is int else Fraction(0)
        )
    elif type(bias) is numeric_type:
        effective_bias = bias
    else:
        raise TypeError("recursive-sequence bias must match the prefix type")
    if len(prefix) < len(coefficients):
        raise ValueError(
            "recursive-sequence prefix must cover every declared lag"
        )
    source = alphabets.word_value(prefix, tag="sequence")
    source_expr = rules.observation(0)
    zero: int | Fraction = 0 if numeric_type is int else Fraction(0)
    terms = tuple(
        rules.multiply(
            rules.literal_expr(coefficient),
            rules.item_at(
                source_expr,
                rules.subtract(
                    rules.length(source_expr),
                    rules.literal_expr(lag),
                ),
                rules.literal_expr(zero),
            ),
        )
        for lag, coefficient in enumerate(coefficients, start=1)
    )
    next_term = rules.add(rules.literal_expr(effective_bias), *terms)
    output = rules.concatenate(
        source_expr,
        rules.word_value("sequence", next_term),
    )
    number_alphabet = (
        alphabets.integers()
        if numeric_type is int
        else alphabets.rationals()
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        source,
        alphabets.word(number_alphabet),
        output,
        label="recursive-sequence",
    )
    return indexed_history_recurrence(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def variable_index_recursive_sequence(
    *,
    prefix: tuple[int, ...],
    recurrence: rules.RuleExpr,
) -> SimpleProgram:
    """Append one natural-number term from a closed value-addressed recurrence.

    ``recurrence`` observes a record containing the current ``prefix`` word
    and one-origin ``next_index``.  Generic application validates its
    evaluated value against the natural-number history alphabet.
    """

    if (
        type(prefix) is not tuple
        or not prefix
        or any(type(value) is not int or value <= 0 for value in prefix)
    ):
        raise ValueError(
            "variable-index recurrence needs a nonempty positive-int prefix"
        )
    if type(recurrence) is not rules.RuleExpr:
        raise TypeError("recurrence must be a RuleExpr")
    state = alphabets.record_value(
        (
            ("next_index", len(prefix) + 1),
            ("prefix", alphabets.word_value(prefix, tag="history")),
        ),
        tag="indexed-history-state",
    )
    state_expr = rules.observation(0)
    prefix_expr = rules.record_field(state_expr, "prefix")
    updated = rules.record_update(
        rules.record_update(
            state_expr,
            "prefix",
            rules.concatenate(
                prefix_expr,
                rules.word_value("history", recurrence),
            ),
        ),
        "next_index",
        rules.add(
            rules.record_field(state_expr, "next_index"),
            rules.literal_expr(1),
        ),
    )
    alphabet = alphabets.record(
        (
            ("next_index", alphabets.naturals()),
            ("prefix", alphabets.word(alphabets.naturals())),
        )
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        state,
        alphabet,
        updated,
        label="variable-index-recursive-sequence",
    )
    return indexed_history_recurrence(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def number_theoretic_filtering(
    *,
    upper: int,
    lower: int = 2,
    first_divisor: int = 2,
) -> SimpleProgram:
    """Run the strict consecutive divisor-erasure process on a finite interval."""

    if type(lower) is not int or lower < 2:
        raise ValueError("number-theoretic lower must be an integer >= 2")
    if type(upper) is not int or upper < lower:
        raise ValueError("number-theoretic upper must be >= lower")
    if (
        type(first_divisor) is not int
        or first_divisor < 2
        or first_divisor > upper
    ):
        raise ValueError(
            "number-theoretic first_divisor must lie between 2 and upper"
        )
    state = alphabets.record_value(
        (
            (
                "candidates",
                alphabets.word_value(
                    tuple(range(lower, upper + 1)),
                    tag="candidates",
                ),
            ),
            ("divisor", first_divisor),
        ),
        tag="erasure-state",
    )
    state_expr = rules.observation(0)
    candidates = rules.record_field(state_expr, "candidates")
    divisor = rules.record_field(state_expr, "divisor")
    candidate = rules.bound_value()
    remainder = rules.subtract(
        candidate,
        rules.multiply(
            rules.floor_divide(candidate, divisor),
            divisor,
        ),
    )
    keep = rules.conditional(
        rules.less_equal(candidate, divisor),
        rules.literal_expr(True),
        rules.conditional(
            rules.equal(remainder, rules.literal_expr(0)),
            rules.literal_expr(False),
            rules.literal_expr(True),
        ),
    )
    updated = rules.record_update(
        rules.record_update(
            state_expr,
            "candidates",
            rules.filter_items(candidates, keep),
        ),
        "divisor",
        rules.add(divisor, rules.literal_expr(1)),
    )
    alphabet = alphabets.record(
        (
            ("candidates", alphabets.word(alphabets.naturals())),
            ("divisor", alphabets.naturals()),
        )
    )
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        state,
        alphabet,
        rules.less_equal(divisor, rules.literal_expr(upper)),
        updated,
        label="number-theoretic-filtering",
    )
    return iterated_erasure_process(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def neighbor_independent_substitution(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[WordProduction, ...],
) -> SimpleProgram:
    """Replace every symbol independently with one nonempty offspring word."""

    symbol_alphabet = _require_symbols(
        symbols,
        label="neighbor-independent-substitution",
    )
    initial = _require_word_members(
        initial,
        symbols,
        label="neighbor-independent-substitution initial",
    )
    table = _word_production_map(
        symbols,
        productions,
        label="neighbor-independent-substitution",
        allow_empty=False,
    )
    source = alphabets.word_value(initial, tag="symbols")
    output = rules.flat_map_lookup(
        rules.observation(0),
        rules.literal_expr(table),
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        source,
        alphabets.word(symbol_alphabet),
        output,
        label="neighbor-independent-substitution",
    )
    return parallel_independent_substitution(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def creation_destruction_substitution(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    productions: tuple[WordProduction, ...],
) -> SimpleProgram:
    """Replace symbols in parallel with explicit deletion and growth present."""

    symbol_alphabet = _require_symbols(
        symbols,
        label="creation-destruction-substitution",
    )
    initial = _require_word_members(
        initial,
        symbols,
        label="creation-destruction-substitution initial",
    )
    table = _word_production_map(
        symbols,
        productions,
        label="creation-destruction-substitution",
        allow_empty=True,
    )
    outputs = tuple(entry[1] for entry in productions)
    if not any(not output for output in outputs):
        raise ValueError(
            "creation-destruction substitution needs an empty production"
        )
    if not any(len(output) > 1 for output in outputs):
        raise ValueError(
            "creation-destruction substitution needs a growing production"
        )
    source = alphabets.word_value(initial, tag="symbols")
    output = rules.flat_map_lookup(
        rules.observation(0),
        rules.literal_expr(table),
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        source,
        alphabets.word(symbol_alphabet),
        output,
        label="creation-destruction-substitution",
    )
    return parallel_independent_substitution(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def substitution_system_2d(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram:
    """Apply one total rank-2 independent symbol-to-tile substitution."""

    _require_symbols(symbols, label="substitution-system-2d")
    initial, _, _, cells = _require_rank_two_field(
        initial,
        label="substitution-system-2d initial",
    )
    _require_word_members(
        cells,
        symbols,
        label="substitution-system-2d initial cells",
    )
    productions = _mosaic_production_map(
        initial,
        productions,
        label="substitution-system-2d",
        expected_keys=symbols,
    )
    for _, tile in alphabets.map_entries(productions):
        _, _, _, tile_cells = _require_rank_two_field(
            tile,
            label="substitution-system-2d tile",
        )
        _require_word_members(
            tile_cells,
            symbols,
            label="substitution-system-2d tile cells",
        )
    output = rules.mosaic_substitute(
        rules.observation(0),
        rules.literal_expr(productions),
    )
    seed, alphabet, frontier, neighborhood, rule = _expression_components(
        initial,
        alphabets.field(),
        output,
        label="substitution-system-2d",
    )
    return parallel_independent_substitution(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def geometric_substitution(
    *,
    seed: alphabets.ValueNode,
    productions: alphabets.ValueNode,
) -> SimpleProgram:
    """Apply one closed rank-2 independent mosaic with common tile geometry."""

    seed, _, _, cells = _require_rank_two_field(
        seed,
        label="geometric-substitution seed",
    )
    productions = _mosaic_production_map(
        seed,
        productions,
        label="geometric-substitution",
        require_closed_keys=True,
    )
    keys = tuple(key for key, _ in alphabets.map_entries(productions))
    if any(_semantic_index(keys, cell) is None for cell in cells):
        raise ValueError(
            "geometric-substitution seed cells need production keys"
        )
    output = rules.mosaic_substitute(
        rules.observation(0),
        rules.literal_expr(productions),
    )
    exact_seed, alphabet, frontier, neighborhood, rule = (
        _expression_components(
            seed,
            alphabets.field(),
            output,
            label="geometric-substitution",
        )
    )
    return parallel_independent_substitution(
        seed=exact_seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def continued_fraction_substitution(
    *,
    continued_fraction: tuple[int, ...],
    source_evidence: rules.EvidenceTerm,
) -> SimpleProgram:
    """Apply the reversed-tail binary substitutions for one finite CF record.

    The closed evidence term is preserved as source provenance.  It is not a
    proof that the finite continued-fraction record denotes any external
    mathematical source.
    """

    if (
        type(continued_fraction) is not tuple
        or not continued_fraction
        or any(type(value) is not int for value in continued_fraction)
        or any(value <= 0 for value in continued_fraction[1:])
    ):
        raise ValueError(
            "continued_fraction needs one signed integer followed by "
            "positive integers"
        )
    _evidence_template(source_evidence)
    schedule_values = tuple(reversed(continued_fraction[1:]))
    state = alphabets.record_value(
        (
            (
                "continued_fraction",
                alphabets.word_value(
                    continued_fraction,
                    tag="continued-fraction",
                ),
            ),
            ("cursor", 0),
            (
                "schedule",
                alphabets.word_value(schedule_values, tag="cf-schedule"),
            ),
            ("word", alphabets.word_value((0,), tag="cf-word")),
        ),
        tag="scheduled-substitution-state",
    )
    state_expr = rules.observation(0)
    cursor = rules.record_field(state_expr, "cursor")
    word = rules.record_field(state_expr, "word")
    variants: list[rules.RuleExpr] = []
    for partial_quotient in schedule_values:
        zero_image = alphabets.word_value(
            (0,) * (partial_quotient - 1) + (1,),
            tag="cf-word",
        )
        one_image = alphabets.word_value(
            (0,) * (partial_quotient - 1) + (1, 0),
            tag="cf-word",
        )
        table = alphabets.map_value(
            (
                alphabets.map_entry_value(0, zero_image),
                alphabets.map_entry_value(1, one_image),
            ),
            tag=f"continued-fraction-rho-{partial_quotient}",
        )
        variants.append(
            rules.flat_map_lookup(word, rules.literal_expr(table))
        )
    if variants:
        selected = variants[-1]
        for index in range(len(variants) - 2, -1, -1):
            selected = rules.conditional(
                rules.equal(cursor, rules.literal_expr(index)),
                variants[index],
                selected,
            )
        updated = rules.record_update(
            rules.record_update(state_expr, "word", selected),
            "cursor",
            rules.add(cursor, rules.literal_expr(1)),
        )
    else:
        updated = state_expr
    schedule = rules.record_field(state_expr, "schedule")
    alphabet = alphabets.record(
        (
            (
                "continued_fraction",
                alphabets.word(alphabets.integers()),
            ),
            ("cursor", alphabets.naturals()),
            ("schedule", alphabets.word(alphabets.naturals())),
            ("word", alphabets.word(alphabets.enum((0, 1)))),
        )
    )
    exact_seed, alphabet, frontier, neighborhood, rule = (
        _conditional_components(
            state,
            alphabet,
            rules.less_than(cursor, rules.length(schedule)),
            updated,
            label="continued-fraction-substitution",
            source_evidence=source_evidence,
        )
    )
    return parallel_independent_substitution(
        seed=exact_seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def sequential_substitution(
    *,
    symbols: tuple[alphabets.SemanticValue, ...],
    initial: SemanticWord,
    clauses: tuple[tuple[SemanticWord, SemanticWord], ...],
) -> SimpleProgram:
    """Apply the first matching rule and its leftmost match exactly once."""

    symbol_alphabet = _require_symbols(
        symbols,
        label="sequential-substitution",
    )
    initial = _require_word_members(
        initial,
        symbols,
        label="sequential-substitution initial",
    )
    if type(clauses) is not tuple or not clauses:
        raise ValueError(
            "sequential-substitution clauses must be a nonempty tuple"
        )
    rewrite_values: list[alphabets.ValueNode] = []
    for clause in clauses:
        if type(clause) is not tuple or len(clause) != 2:
            raise TypeError("sequential-substitution clauses must be pairs")
        lhs = _require_word_members(
            clause[0],
            symbols,
            label="sequential-substitution lhs",
            nonempty=True,
        )
        rhs = _require_word_members(
            clause[1],
            symbols,
            label="sequential-substitution rhs",
            nonempty=True,
        )
        rewrite_values.append(
            alphabets.rewrite_rule_value(
                alphabets.pattern_sequence(
                    tuple(alphabets.pattern_literal(item) for item in lhs)
                ),
                alphabets.template_sequence(
                    tuple(alphabets.template_literal(item) for item in rhs)
                ),
            )
        )
    rewrite_bundle = alphabets.rewrite_rules_value(tuple(rewrite_values))
    state = alphabets.word_value(initial, tag="symbols")
    rewrite_result = rules.pattern_rewrite(
        rules.observation(0),
        rules.literal_expr(rewrite_bundle),
        scan=rules.RewriteScan.RULE_PRIORITY_FIRST,
    )
    matches = rules.record_field(rewrite_result, "matches")
    result = rules.record_field(rewrite_result, "result")
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        state,
        alphabets.word(symbol_alphabet),
        rules.less_than(rules.literal_expr(0), rules.length(matches)),
        result,
        label="sequential-substitution",
    )
    return structural_pattern_rewrite(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def symbolic_system(
    *,
    expression: alphabets.ValueNode,
    rewrites: alphabets.ValueNode,
    scan: rules.RewriteScan = rules.RewriteScan.RULE_PRIORITY_FIRST,
) -> SimpleProgram:
    """Apply one closed ordered rewrite to a positional symbolic tree.

    Rewrite syntax is validated here; generic application validates the
    evaluated replacement against the symbolic-expression alphabet before
    committing it.
    """

    if (
        type(expression) is not alphabets.ValueNode
        or expression.kind is not alphabets.ValueKind.SYMBOLIC
    ):
        raise TypeError("symbolic-system expression must be a SYMBOLIC ValueNode")
    if (
        type(rewrites) is not alphabets.ValueNode
        or rewrites.kind is not alphabets.ValueKind.WORD
        or rewrites.tag != "rewrite-rules"
    ):
        raise TypeError(
            "symbolic-system rewrites must be a rewrite-rules WORD ValueNode"
        )
    if any(type(item) is not alphabets.ValueNode for item in rewrites.items):
        raise TypeError(
            "symbolic-system rewrite entries must be ValueNodes"
        )
    rewrites = alphabets.rewrite_rules_value(
        tuple(item for item in rewrites.items if type(item) is alphabets.ValueNode)
    )
    if len(rewrites.items) == 0:
        raise ValueError("symbolic-system rewrites cannot be empty")
    if type(scan) is not rules.RewriteScan:
        raise TypeError("symbolic-system scan is not recognized")
    rewrite_result = rules.pattern_rewrite(
        rules.observation(0),
        rules.literal_expr(rewrites),
        scan=scan,
    )
    matches = rules.record_field(rewrite_result, "matches")
    result = rules.record_field(rewrite_result, "result")
    seed, alphabet, frontier, neighborhood, rule = _conditional_components(
        expression,
        alphabets.symbolic_expression(),
        rules.less_than(rules.literal_expr(0), rules.length(matches)),
        result,
        label="symbolic-system",
    )
    return structural_pattern_rewrite(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


# ---------------------------------------------------------------------------
# Phase 3. True aliases
# ---------------------------------------------------------------------------


def multiway_system(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """An alias for SPF033 with the exact ``multiway_rewrite`` signature."""

    return multiway_rewrite(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )


def network_rewrite(
    *,
    seed: Seed[C],
    alphabet: Alphabet[V],
    frontier: WritableRegion[C, W],
    neighborhood: ReadableRegion[C, R],
    rule: Rule[R, W, C],
) -> SimpleProgram[C, V, W, R]:
    """An alias for SPF038 with the exact canonical network signature."""

    return parallel_network_rewrite(
        seed=seed,
        alphabet=alphabet,
        frontier=frontier,
        neighborhood=neighborhood,
        rule=rule,
    )

__all__ = (
    "append_only_sequence_generation",
    "constant_digit_sequence",
    "context_dependent_substitution_2d",
    "context_dependent_substitution",
    "continued_fraction_substitution",
    "creation_destruction_substitution",
    "cyclic_tag_system",
    "first_passage_aggregation",
    "front_delete_rear_append_system",
    "geometric_substitution",
    "global_score_sequential_placement",
    "history_dependent_growth_rewrite",
    "indexed_history_recurrence",
    "iterated_erasure_process",
    "local_graph_rewrite",
    "moving_frontier_shell_accretion",
    "multiway_rewrite",
    "multiway_system",
    "neighbor_dependent_substitution",
    "neighbor_independent_substitution",
    "network_rewrite",
    "number_theoretic_filtering",
    "parallel_independent_substitution",
    "parallel_network_rewrite",
    "random_functional_graph_construction",
    "recursive_sequence",
    "sequential_substitution",
    "structural_pattern_rewrite",
    "substitution_system_2d",
    "symbolic_system",
    "tag_system",
    "variable_index_recursive_sequence",
)
