"""Focused tests for sealed word and symbolic-tree pattern rewrites."""

from __future__ import annotations

import pytest

import ca
from ca import (
    alphabets,
    frontiers,
    loci,
    neighborhoods,
    program,
    rules,
    seeds,
)


def _readable_view():
    source = loci.record_configuration((("fixture", 0),))
    return neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabets.ValueProfile.STRUCTURAL,
    ).resolve(source)


def _evaluate(expression: rules.RuleExpr) -> alphabets.SemanticValue:
    result, proof = rules._evaluate_proven(  # noqa: SLF001 - interpreter test
        expression,
        _readable_view(),
        anchor=None,
    )
    assert proof.steps[-1].expression == expression
    assert proof.steps[-1].result == result
    return result


def _word(
    tag: str,
    *items: alphabets.SemanticValue,
) -> alphabets.ValueNode:
    return alphabets.word_value(items, tag=tag)


def _sequence_rule(
    pattern: tuple[alphabets.ValueNode, ...],
    template: tuple[alphabets.ValueNode, ...],
) -> alphabets.ValueNode:
    return alphabets.rewrite_rule_value(
        alphabets.pattern_sequence(pattern),
        alphabets.template_sequence(template),
    )


def _rewrite(
    source: alphabets.SemanticValue,
    rewrite_rules: alphabets.ValueNode,
    *,
    scan: rules.RewriteScan = rules.RewriteScan.RULE_PRIORITY_FIRST,
) -> alphabets.ValueNode:
    result = _evaluate(
        rules.pattern_rewrite(
            rules.literal_expr(source),
            rules.literal_expr(rewrite_rules),
            scan=scan,
        )
    )
    assert type(result) is alphabets.ValueNode
    assert result.kind is alphabets.ValueKind.RECORD
    assert result.tag == "pattern-rewrite"
    return result


def _fields(value: alphabets.ValueNode) -> dict[str, alphabets.SemanticValue]:
    return dict(value.fields)


def _public_apply_value(
    source_value: alphabets.SemanticValue,
    alphabet: alphabets.Alphabet,
    expression: rules.RuleExpr,
) -> alphabets.SemanticValue:
    source = loci.record_configuration((("state", source_value),))
    writable = frontiers.everywhere(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    readable = neighborhoods.global_view(
        configuration_contract=source.contract,
        value_profile=alphabet.value_profile,
    )
    rule = rules.expression(
        rules.ExistingPlan(
            rules.ExistingPlanKind.BY_INDEX,
            (expression,),
        ),
        contract=rules.RuleContract(
            source.contract,
            alphabet.value_profile,
            readable.result_shape,
            readable.join_shape,
            writable.effect_profile,
        ),
        witness=rules.literal_expr("pattern-rewrite-public-apply"),
        provenance=("test:pattern-rewrite-public-apply",),
    )
    simple_program = ca.SimpleProgram(
        seed=seeds.exact(
            source,
            value_profile=alphabet.value_profile,
        ),
        alphabet=alphabet,
        frontier=writable,
        neighborhood=readable,
        rule=rule,
    )

    applied = ca.apply(simple_program, source)

    assert type(applied) is program.ApplicationComplete
    groups = applied.successor_quotient_with_derivation_fibers.atoms
    assert len(groups) == 1
    assert type(groups[0]) is program.SuccessorGroup
    successor = groups[0].successor
    assert type(successor) is loci.FiniteConfiguration
    assert len(successor.entries) == 1
    return successor.entries[0][1]


def _match_records(
    result: alphabets.ValueNode,
) -> tuple[alphabets.ValueNode, ...]:
    matches = _fields(result)["matches"]
    assert type(matches) is alphabets.ValueNode
    assert matches.kind is alphabets.ValueKind.WORD
    assert matches.tag == "pattern-matches"
    assert all(type(item) is alphabets.ValueNode for item in matches.items)
    return tuple(
        item for item in matches.items if type(item) is alphabets.ValueNode
    )


def test_rule_priority_exact_discriminator_retains_match_witness() -> None:
    source = _word("letters", "A", "B", "A", "B", "A")
    first = _sequence_rule(
        (
            alphabets.pattern_literal("B"),
            alphabets.pattern_literal("A"),
        ),
        (alphabets.template_literal("X"),),
    )
    second = _sequence_rule(
        (
            alphabets.pattern_literal("A"),
            alphabets.pattern_literal("B"),
        ),
        (alphabets.template_literal("Y"),),
    )

    result = _rewrite(
        source,
        alphabets.rewrite_rules_value((first, second)),
    )

    result_fields = _fields(result)
    assert result_fields["matched"] is True
    assert result_fields["result"] == _word(
        "letters",
        "A",
        "X",
        "B",
        "A",
    )
    (match,) = _match_records(result)
    match_fields = _fields(match)
    path = match_fields["path"]
    assert type(path) is alphabets.ValueNode
    assert path.kind is alphabets.ValueKind.WORD
    assert path.tag == "rewrite-path"
    assert path.items == (1,)
    assert match_fields["span"] == 2
    assert match_fields["rule_index"] == 0
    bindings = match_fields["bindings"]
    assert type(bindings) is alphabets.ValueNode
    assert bindings.kind is alphabets.ValueKind.MAP
    assert bindings.tag == "rewrite-bindings"
    assert alphabets.map_entries(bindings) == ()


def test_location_priority_and_nonoverlap_are_deterministic() -> None:
    source = _word("letters", "A", "B", "A", "B", "A")
    rules_value = alphabets.rewrite_rules_value(
        (
            _sequence_rule(
                (
                    alphabets.pattern_literal("B"),
                    alphabets.pattern_literal("A"),
                ),
                (alphabets.template_literal("X"),),
            ),
            _sequence_rule(
                (
                    alphabets.pattern_literal("A"),
                    alphabets.pattern_literal("B"),
                ),
                (alphabets.template_literal("Y"),),
            ),
        )
    )

    first_location = _rewrite(
        source,
        rules_value,
        scan=rules.RewriteScan.LOCATION_PRIORITY_FIRST,
    )
    nonoverlapping = _rewrite(
        source,
        rules_value,
        scan=rules.RewriteScan.LOCATION_PRIORITY_NONOVERLAPPING,
    )

    assert _fields(first_location)["result"] == _word(
        "letters",
        "Y",
        "A",
        "B",
        "A",
    )
    assert _fields(nonoverlapping)["result"] == _word(
        "letters",
        "Y",
        "Y",
        "A",
    )
    assert tuple(
        _fields(match)["path"].items
        for match in _match_records(nonoverlapping)
        if type(_fields(match)["path"]) is alphabets.ValueNode
    ) == ((0,), (2,))
    assert tuple(
        _fields(match)["rule_index"]
        for match in _match_records(nonoverlapping)
    ) == (1, 1)


def test_symbolic_add_x_zero_rewrites_to_the_bound_subtree() -> None:
    x = alphabets.symbolic_value("x")
    source = alphabets.symbolic_value("add", items=(x, 0))
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "add",
            (
                alphabets.pattern_bind("value"),
                alphabets.pattern_literal(0),
            ),
        ),
        alphabets.template_binding("value"),
    )

    result = _rewrite(
        source,
        alphabets.rewrite_rules_value((rewrite_rule,)),
    )

    assert _fields(result)["result"] == x
    (match,) = _match_records(result)
    match_fields = _fields(match)
    assert match_fields["path"].items == ()
    assert match_fields["span"] == 1
    bindings = match_fields["bindings"]
    assert type(bindings) is alphabets.ValueNode
    assert alphabets.map_get(bindings, "value") == x


def test_repeated_binders_require_exact_semantic_equality() -> None:
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "pair",
            (
                alphabets.pattern_bind("same"),
                alphabets.pattern_bind("same"),
            ),
        ),
        alphabets.template_binding("same"),
    )
    rewrite_rules = alphabets.rewrite_rules_value((rewrite_rule,))

    equal_result = _rewrite(
        alphabets.symbolic_value("pair", items=("a", "a")),
        rewrite_rules,
    )
    unequal_result = _rewrite(
        alphabets.symbolic_value("pair", items=("a", "b")),
        rewrite_rules,
    )

    assert _fields(equal_result)["matched"] is True
    assert _fields(equal_result)["result"] == "a"
    assert _fields(unequal_result)["matched"] is False
    assert _match_records(unequal_result) == ()


def test_template_binding_subset_is_validated_at_evaluation() -> None:
    rewrite_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_bind("known"),
        alphabets.template_binding("unknown"),
    )
    expression = rules.pattern_rewrite(
        rules.literal_expr(alphabets.symbolic_value("source")),
        rules.literal_expr(
            alphabets.rewrite_rules_value((rewrite_rule,))
        ),
    )

    with pytest.raises(ValueError, match="unbound"):
        _evaluate(expression)


@pytest.mark.parametrize(
    ("source", "rewrite_rule"),
    (
        (
            _word("letters", "a"),
            alphabets.rewrite_rule_value(
                alphabets.pattern_node(
                    "node",
                    (alphabets.pattern_bind("x"),),
                ),
                alphabets.template_binding("x"),
            ),
        ),
        (
            alphabets.symbolic_value("node", items=("a",)),
            _sequence_rule(
                (alphabets.pattern_literal("a"),),
                (alphabets.template_literal("b"),),
            ),
        ),
        (
            alphabets.symbolic_value("node", items=("a",)),
            alphabets.rewrite_rule_value(
                alphabets.pattern_node(
                    "node",
                    (
                        alphabets.pattern_sequence(
                            (alphabets.pattern_literal("a"),)
                        ),
                    ),
                ),
                alphabets.template_binding("unused"),
            ),
        ),
    ),
)
def test_mixed_word_tree_or_nested_sequence_patterns_fail_closed(
    source: alphabets.SemanticValue,
    rewrite_rule: alphabets.ValueNode,
) -> None:
    expression = rules.pattern_rewrite(
        rules.literal_expr(source),
        rules.literal_expr(
            alphabets.rewrite_rules_value((rewrite_rule,))
        ),
    )

    with pytest.raises(ValueError):
        _evaluate(expression)


def test_malformed_rule_container_fails_closed() -> None:
    malformed = alphabets.word_value(
        (
            alphabets.product_value(
                (
                    alphabets.pattern_literal("a"),
                    alphabets.template_literal("b"),
                ),
                tag="not-rewrite",
            ),
        ),
        tag="rewrite-rules",
    )

    with pytest.raises(ValueError):
        _rewrite(_word("letters", "a"), malformed)


def test_no_match_and_matched_identity_are_distinct() -> None:
    source = _word("letters", "A")
    no_match = _rewrite(
        source,
        alphabets.rewrite_rules_value(
            (
                _sequence_rule(
                    (alphabets.pattern_literal("B"),),
                    (alphabets.template_literal("C"),),
                ),
            )
        ),
    )
    identity = _rewrite(
        source,
        alphabets.rewrite_rules_value(
            (
                _sequence_rule(
                    (alphabets.pattern_literal("A"),),
                    (alphabets.template_literal("A"),),
                ),
            )
        ),
    )

    assert _fields(no_match)["matched"] is False
    assert _fields(no_match)["result"] is source
    assert _match_records(no_match) == ()
    assert _fields(identity)["matched"] is True
    assert alphabets.semantic_equal(_fields(identity)["result"], source)
    assert len(_match_records(identity)) == 1


def test_tree_nonoverlap_accepts_siblings_and_ancestors_suppress_descendants() -> None:
    source = alphabets.symbolic_value(
        "root",
        items=(
            alphabets.symbolic_value("branch", items=("a",)),
            alphabets.symbolic_value("branch", items=("a",)),
        ),
    )
    branch_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "branch",
            (alphabets.pattern_bind("child"),),
        ),
        alphabets.template_literal("branch-result"),
    )
    leaf_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_literal("a"),
        alphabets.template_literal("leaf-result"),
    )
    sibling_result = _rewrite(
        source,
        alphabets.rewrite_rules_value((branch_rule, leaf_rule)),
        scan=rules.RewriteScan.LOCATION_PRIORITY_NONOVERLAPPING,
    )

    assert _fields(sibling_result)["result"] == alphabets.symbolic_value(
        "root",
        items=("branch-result", "branch-result"),
    )
    assert tuple(
        _fields(match)["path"].items
        for match in _match_records(sibling_result)
    ) == ((0,), (1,))

    root_rule = alphabets.rewrite_rule_value(
        alphabets.pattern_node(
            "root",
            (
                alphabets.pattern_bind("left"),
                alphabets.pattern_bind("right"),
            ),
        ),
        alphabets.template_literal("whole-result"),
    )
    ancestor_result = _rewrite(
        source,
        alphabets.rewrite_rules_value(
            (leaf_rule, root_rule, branch_rule)
        ),
        scan=rules.RewriteScan.LOCATION_PRIORITY_NONOVERLAPPING,
    )

    assert _fields(ancestor_result)["result"] == "whole-result"
    (root_match,) = _match_records(ancestor_result)
    assert _fields(root_match)["path"].items == ()
    assert _fields(root_match)["rule_index"] == 1


def test_word_tree_and_nonoverlap_rewrites_execute_through_public_apply() -> None:
    letters = _word("letters", "A", "B", "A", "B", "A")
    letter_rules = alphabets.rewrite_rules_value(
        (
            _sequence_rule(
                (
                    alphabets.pattern_literal("B"),
                    alphabets.pattern_literal("A"),
                ),
                (alphabets.template_literal("X"),),
            ),
            _sequence_rule(
                (
                    alphabets.pattern_literal("A"),
                    alphabets.pattern_literal("B"),
                ),
                (alphabets.template_literal("Y"),),
            ),
        )
    )
    letter_result = rules.record_field(
        rules.pattern_rewrite(
            rules.observation(0),
            rules.literal_expr(letter_rules),
        ),
        "result",
    )
    assert _public_apply_value(
        letters,
        alphabets.word(
            alphabets.symbolic(("A", "B", "X", "Y"))
        ),
        letter_result,
    ) == _word("letters", "A", "X", "B", "A")

    x = alphabets.symbolic_value("x")
    add_source = alphabets.symbolic_value("add", items=(x, 0))
    add_rules = alphabets.rewrite_rules_value(
        (
            alphabets.rewrite_rule_value(
                alphabets.pattern_node(
                    "add",
                    (
                        alphabets.pattern_bind("value"),
                        alphabets.pattern_literal(0),
                    ),
                ),
                alphabets.template_binding("value"),
            ),
        )
    )
    add_result = rules.record_field(
        rules.pattern_rewrite(
            rules.observation(0),
            rules.literal_expr(add_rules),
        ),
        "result",
    )
    assert _public_apply_value(
        add_source,
        alphabets.symbolic_expression(),
        add_result,
    ) == x

    tree_source = alphabets.symbolic_value(
        "root",
        items=(
            alphabets.symbolic_value("branch", items=("a",)),
            alphabets.symbolic_value("branch", items=("a",)),
        ),
    )
    tree_rules = alphabets.rewrite_rules_value(
        (
            alphabets.rewrite_rule_value(
                alphabets.pattern_node(
                    "branch",
                    (alphabets.pattern_bind("child"),),
                ),
                alphabets.template_node(
                    "done",
                    (alphabets.template_binding("child"),),
                ),
            ),
        )
    )
    tree_result = rules.record_field(
        rules.pattern_rewrite(
            rules.observation(0),
            rules.literal_expr(tree_rules),
            scan=rules.RewriteScan.LOCATION_PRIORITY_NONOVERLAPPING,
        ),
        "result",
    )
    assert _public_apply_value(
        tree_source,
        alphabets.symbolic_expression(),
        tree_result,
    ) == alphabets.symbolic_value(
        "root",
        items=(
            alphabets.symbolic_value("done", items=("a",)),
            alphabets.symbolic_value("done", items=("a",)),
        ),
    )


def test_pattern_rewrite_constructor_rejects_unknown_scan() -> None:
    source = rules.literal_expr(_word("letters", "a"))
    rewrite_rules = rules.literal_expr(
        alphabets.rewrite_rules_value(
            (
                _sequence_rule(
                    (alphabets.pattern_literal("a"),),
                    (alphabets.template_literal("b"),),
                ),
            )
        )
    )

    with pytest.raises(TypeError):
        rules.pattern_rewrite(  # type: ignore[arg-type]
            source,
            rewrite_rules,
            scan="rule-priority-first",
        )
    with pytest.raises(ValueError):
        rules.RuleExpr(
            rules.ExpressionPrimitive.PATTERN_REWRITE,
            (source, rewrite_rules, "unknown-scan"),
        )
