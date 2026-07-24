#!/usr/bin/env python3
"""Frozen Stage 9 Chapter 5 local-search route authoring specification.

This module is data only.  It does not read or write any audit ledger.
`ROUTE_SPECS` materializes the 137 new route rows in immutable final-F15
SEARCH_HIT order and within-hit locator order.  Existing-route uses and
rejected/non-bearing locators are frozen separately so every one of the 144
final F15 hit units has an explicit disposition.

Recovered candidate links use provisional names rather than unstable B IDs.
Existing candidates retain their already-governed B IDs.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


def uids(first: int, last: int | None = None) -> tuple[str, ...]:
    """Return an inclusive, zero-padded source-unit ID range."""

    end = first if last is None else last
    return tuple(f"U{number:06d}" for number in range(first, end + 1))


def aids(first: int, last: int | None = None) -> tuple[str, ...]:
    """Return an inclusive, zero-padded asset ID range."""

    end = first if last is None else last
    return tuple(f"A{number:06d}" for number in range(first, end + 1))


def bids(first: int, last: int | None = None) -> tuple[str, ...]:
    """Return an inclusive, zero-padded governed candidate ID range."""

    end = first if last is None else last
    return tuple(f"B{number:04d}" for number in range(first, end + 1))


def _tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(values)


def route(
    source_unit_id: str,
    discovery_hit_id: str,
    discovery_ordinal: int,
    literal_target: str,
    expected_topic: str,
    closure_scope: str,
    *,
    route_kind: str = "PAGE",
    target_unit_ids: tuple[str, ...] = (),
    target_asset_ids: tuple[str, ...] = (),
    candidate_ids: tuple[str, ...] = (),
    recovered_candidate_names: tuple[str, ...] = (),
    vocabulary_terms: tuple[str, ...] = (),
    defect_boundary: str = "",
    attempts: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Construct one route row before immutable route-ID allocation."""

    status = "RESOLVED" if closure_scope == "WITHIN_STAGE" else "PENDING"
    if attempts is None:
        if status == "RESOLVED":
            unit_boundary = ", ".join(target_unit_ids) or "none"
            asset_boundary = ", ".join(target_asset_ids) or "none"
            attempts = (
                f"Resolved literal target {literal_target!r} as "
                f"{expected_topic!r} within the assigned Chapter 5 "
                f"main/Notes sources; closure is bounded to target units "
                f"{unit_boundary} and target assets {asset_boundary}.",
            )
        else:
            attempts = (
                f"Queued literal target {literal_target!r} for topic "
                f"{expected_topic!r} outside the assigned Chapter 5 source "
                "range; no target mechanics were inferred and no target "
                "units or assets are claimed.",
            )
    return {
        "route_id": "",
        "source_unit_id": source_unit_id,
        "source_asset_id": "",
        "discovery_epoch": 2,
        "discovery_kind": "SEARCH_HIT",
        "discovery_id": discovery_hit_id,
        "discovery_family_ordinal": 15,
        "discovery_ordinal": discovery_ordinal,
        "literal_target": literal_target,
        "route_kind": route_kind,
        "expected_topic": expected_topic,
        "owning_stage": 9,
        "closure_scope": closure_scope,
        "status": status,
        "target_unit_ids": target_unit_ids,
        "target_asset_ids": target_asset_ids,
        "attempts": attempts,
        "vocabulary_terms": vocabulary_terms,
        "defect_boundary": defect_boundary,
        "reading_unit_ids": (source_unit_id,),
        "candidate_ids": candidate_ids,
        "recovered_candidate_names": recovered_candidate_names,
    }


WITHIN = "WITHIN_STAGE"
CROSS = "CROSS_RANGE"


_ROUTES = (
    route(
        "U000971", "H011605", 1,
        "the two-dimensional patterns from the bottom of the previous page",
        "code-942 two-dimensional cellular-automaton patterns used as stacked-history slices",
        WITHIN,
        target_unit_ids=uids(966, 968), target_asset_ids=aids(847),
        recovered_candidate_names=(
            "stacked two-dimensional-cellular-automaton history embedding",
        ),
        vocabulary_terms=("code 942", "stacked history", "two-dimensional cellular automaton"),
    ),
    route(
        "U000972", "H011606", 1,
        "The facing page and the one that follows",
        "two-dimensional cellular-automaton rule-pattern survey",
        WITHIN,
        target_unit_ids=uids(973, 976), target_asset_ids=aids(849, 850),
        candidate_ids=bids(712, 760),
        vocabulary_terms=("rule patterns", "two-dimensional cellular automata"),
    ),
    route(
        "U000972", "H011606", 2,
        "the previous page",
        "one-dimensional center-slice views of the surveyed two-dimensional cellular automata",
        WITHIN,
        target_unit_ids=uids(977, 978), target_asset_ids=aids(851),
        candidate_ids=bids(712, 760),
        vocabulary_terms=("center slices", "two-dimensional cellular automata"),
    ),
    route(
        "U000976", "H011608", 1,
        "the previous page",
        "the same two-dimensional cellular-automaton presets shown after fewer steps",
        WITHIN,
        target_unit_ids=uids(973, 974), target_asset_ids=aids(849),
        candidate_ids=bids(712, 760),
        vocabulary_terms=("continued evolution", "rule patterns", "two-dimensional cellular automata"),
    ),
    route(
        "U000978", "H011609", 1,
        "the previous two pages",
        "two-dimensional cellular-automaton patterns used by the center-slice observer",
        WITHIN,
        target_unit_ids=uids(973, 976), target_asset_ids=aids(849, 850),
        candidate_ids=bids(712, 760),
        vocabulary_terms=("center slices", "rule patterns", "two-dimensional cellular automata"),
    ),
    route(
        "U000980", "H011610", 1,
        "the picture on the facing page",
        "rough-surface eight-neighbor cellular automaton code 175850",
        WITHIN,
        target_unit_ids=uids(986, 989), target_asset_ids=aids(852, 853),
        candidate_ids=bids(661),
        vocabulary_terms=("code 175850", "rough surface", "two-dimensional cellular automaton"),
    ),
    route(
        "U000991", "H011615", 1,
        "the previous page",
        "related eight-neighbor retaining growth-rule family",
        WITHIN,
        target_unit_ids=uids(986, 989), target_asset_ids=aids(852, 853),
        candidate_ids=bids(662),
        vocabulary_terms=("eight-neighbor rule", "retaining rule", "two-dimensional cellular automaton"),
    ),
    route(
        "U000991", "H011615", 2,
        "the picture on the previous page",
        "row-of-seven black-cell initial condition",
        WITHIN,
        target_unit_ids=uids(986, 989), target_asset_ids=aids(852, 853),
        candidate_ids=bids(662),
        vocabulary_terms=("initial condition", "row of seven black cells"),
    ),
    route(
        "U000997", "H011617", 1,
        "the cellular automaton from the previous page",
        "eight-neighbor retaining cellular automaton whose successive patterns are stacked",
        WITHIN,
        target_unit_ids=uids(992, 993), target_asset_ids=aids(855),
        candidate_ids=bids(660),
        recovered_candidate_names=(
            "stacked two-dimensional-cellular-automaton history embedding",
        ),
        vocabulary_terms=("cellular automaton", "stacked history", "previous page"),
    ),
    route(
        "U001002", "H011618", 1,
        "the cellular automaton from the facing page",
        "continued evolution of the eight-neighbor retaining cellular automaton",
        WITHIN,
        target_unit_ids=uids(992, 993), target_asset_ids=aids(855),
        candidate_ids=bids(660),
        vocabulary_terms=("cellular automaton", "continued evolution", "row of eleven black cells"),
    ),
    route(
        "U001016", "H011620", 1,
        "The facing page",
        "five illustrated four-state two-dimensional Turing-machine presets",
        WITHIN,
        target_unit_ids=uids(1017, 1026), target_asset_ids=aids(866, 871),
        candidate_ids=bids(762, 766),
        vocabulary_terms=("four-state rules", "two-dimensional Turing machines"),
    ),
    route(
        "U001031", "H011621", 1,
        "rule (e) from the previous page",
        "four-state two-dimensional Turing-machine rule (e)",
        WITHIN,
        target_unit_ids=uids(1017, 1026), target_asset_ids=aids(866, 871),
        candidate_ids=bids(766),
        recovered_candidate_names=(
            "two-dimensional Turing-machine head-position trajectory observer",
        ),
        vocabulary_terms=("head path", "rule (e)", "two-dimensional Turing machine"),
    ),
    route(
        "U001038", "H011623", 1,
        "The next page",
        "nine page-188 two-dimensional substitution presets",
        WITHIN,
        target_unit_ids=uids(1040, 1041), target_asset_ids=aids(876),
        candidate_ids=bids(767, 775),
        vocabulary_terms=("page 188", "substitution presets", "two-dimensional substitution systems"),
    ),
    route(
        "U001046", "H011624", 1,
        "the picture on the next page",
        "overlap-producing geometrical replacement preset",
        WITHIN,
        target_unit_ids=uids(1047, 1049), target_asset_ids=aids(879, 880),
        candidate_ids=bids(673),
        vocabulary_terms=("geometrical replacement", "overlapping squares"),
    ),
    route(
        "U001050", "H011625", 1,
        "the pictures on the facing page",
        "four geometrical fractal-replacement presets",
        WITHIN,
        target_unit_ids=uids(1054, 1055), target_asset_ids=aids(881),
        candidate_ids=bids(671) + bids(776, 779),
        vocabulary_terms=("fractal patterns", "geometrical replacement"),
    ),
    route(
        "U001053", "H011627", 1,
        "geometrical replacement rules of the kind shown on the facing page",
        "neighbor-independent geometrical fractal-replacement family",
        WITHIN,
        target_unit_ids=uids(1054, 1055), target_asset_ids=aids(881),
        candidate_ids=bids(671) + bids(776, 779),
        vocabulary_terms=("fractal geometry", "geometrical replacement", "neighbor independent"),
    ),
    route(
        "U001056", "H011628", 1,
        "the picture at the top of the next page",
        "two-dimensional neighbor-dependent substitution mechanism",
        WITHIN,
        target_unit_ids=uids(1058, 1059), target_asset_ids=aids(882),
        candidate_ids=bids(674) + bids(780),
        vocabulary_terms=("neighbor-dependent substitution", "two-dimensional substitution"),
    ),
    route(
        "U001056", "H011628", 2,
        "the pictures on the next page",
        "eight neighbor-dependent substitution behavior presets",
        WITHIN,
        target_unit_ids=uids(1058, 1060), target_asset_ids=aids(882),
        candidate_ids=bids(674) + bids(781, 788),
        vocabulary_terms=("neighbor-dependent substitution", "two-dimensional substitution"),
    ),
    route(
        "U001075", "H011631", 1,
        "the pictures on the facing page",
        "binary-outdegree networks with recognizable array geometries",
        WITHIN,
        target_unit_ids=uids(1077, 1082), target_asset_ids=aids(884),
        candidate_ids=bids(789, 791),
        vocabulary_terms=("array geometry", "binary-outdegree networks"),
    ),
    route(
        "U001076", "H011632", 1,
        "the networks illustrated at the top of the facing page",
        "one-, two-, and three-dimensional array-network presets",
        WITHIN,
        target_unit_ids=uids(1077, 1082), target_asset_ids=aids(884),
        candidate_ids=bids(789, 791),
        vocabulary_terms=("array networks", "effective dimension"),
    ),
    route(
        "U001091", "H011633", 1,
        "the pictures at the top of the next page",
        "uniform linear binary-outdegree-network layout representation",
        WITHIN,
        target_unit_ids=uids(1092, 1094), target_asset_ids=aids(887),
        recovered_candidate_names=(
            "uniform linear binary-outdegree-network layout representation",
        ),
        vocabulary_terms=("linear layout", "network representation"),
    ),
    route(
        "U001095", "H011634", 1,
        "the pictures on the facing page",
        "four binary-outdegree network-rerouting presets",
        WITHIN,
        target_unit_ids=uids(1098, 1099), target_asset_ids=aids(888),
        candidate_ids=bids(679, 682),
        vocabulary_terms=("network rerouting", "rule presets"),
    ),
    route(
        "U001101", "H011635", 1,
        "the pictures on the next page",
        "two node-inserting network-rule presets",
        WITHIN,
        target_unit_ids=uids(1102, 1104), target_asset_ids=aids(889, 890),
        candidate_ids=bids(683, 684),
        vocabulary_terms=("network evolution", "node insertion"),
    ),
    route(
        "U001108", "H011636", 1,
        "the pictures on the facing page",
        "one-hop same-target/different-target conditional network rules",
        WITHIN,
        target_unit_ids=uids(1109, 1110), target_asset_ids=aids(891),
        candidate_ids=bids(685) + bids(794, 796),
        vocabulary_terms=("conditional network rules", "one-hop neighborhood"),
    ),
    route(
        "U001111", "H011637", 1,
        "the pictures on the next two pages",
        "distance-two distinct-node-count network-rule family and presets",
        WITHIN,
        target_unit_ids=uids(1114, 1121), target_asset_ids=aids(892, 893),
        candidate_ids=bids(686, 688) + bids(797, 799),
        vocabulary_terms=("distance two", "network rules", "node count"),
    ),
    route(
        "U001144", "H011640", 1,
        "the facing page",
        "period-1071 slow-growth multiway preset",
        WITHIN,
        target_unit_ids=uids(1140, 1143), target_asset_ids=aids(901, 902),
        candidate_ids=bids(691),
        vocabulary_terms=("multiway system", "period 1071", "slow growth"),
    ),
    route(
        "U001148", "H011642", 1,
        "the next page",
        "multiway state-collection survey presets",
        WITHIN,
        target_unit_ids=uids(1149, 1150), target_asset_ids=aids(904),
        candidate_ids=bids(805, 817),
        vocabulary_terms=("multiway survey", "state collections"),
    ),
    route(
        "U001151", "H011644", 1,
        "previous pages",
        "repeated-state evidence underlying the multiway quotient representation",
        WITHIN,
        target_unit_ids=uids(1126, 1150), target_asset_ids=aids(894, 904),
        candidate_ids=bids(693) + bids(818),
        vocabulary_terms=("multiway evolution", "repeated states", "state merging"),
    ),
    route(
        "U001152", "H011645", 1,
        "the picture at the top of the facing page",
        "explicit-once multiway evolution representation",
        WITHIN,
        target_unit_ids=uids(1153, 1155), target_asset_ids=aids(905, 906),
        candidate_ids=bids(693) + bids(818),
        vocabulary_terms=("multiway evolution", "sequence-transition network"),
    ),
    route(
        "U001166", "H011646", 1,
        "the picture at the top of the facing page",
        "one-dimensional at-least-one-unlike-neighbor constraint witnesses",
        WITHIN,
        target_unit_ids=uids(1167, 1169), target_asset_ids=aids(909),
        candidate_ids=bids(696),
        vocabulary_terms=("one-dimensional constraint", "unlike neighbor"),
    ),
    route(
        "U001178", "H011647", 1,
        "the pictures on the facing page",
        "two-dimensional fixed black/white-neighbor-count constraint census",
        WITHIN,
        target_unit_ids=uids(1179, 1181), target_asset_ids=aids(911),
        candidate_ids=bids(698) + bids(819, 842),
        vocabulary_terms=("neighbor-count constraints", "satisfying patterns"),
    ),
    route(
        "U001184", "H011648", 1,
        "the next two pages",
        "numbered 171-pattern witness collection for local-template constraints",
        WITHIN,
        target_unit_ids=uids(1186, 1188), target_asset_ids=aids(913, 914),
        candidate_ids=bids(699, 702),
        vocabulary_terms=("constraint numbering", "local templates", "repetitive patterns"),
    ),
    route(
        "U001185", "H011649", 1,
        "the set of 171 repetitive patterns on the next two pages",
        "complete 171-pattern witness basis for local-template constraints",
        WITHIN,
        target_unit_ids=uids(1186, 1188), target_asset_ids=aids(913, 914),
        candidate_ids=bids(699) + bids(702),
        recovered_candidate_names=(
            "two-dimensional local-template constraint census",
        ),
        vocabulary_terms=("171 repetitive patterns", "local-template constraints", "witness basis"),
    ),
    route(
        "U001188", "H011650", 1,
        "constraints of the type shown on the previous page",
        "two-dimensional overlapping local-template constraint family",
        WITHIN,
        target_unit_ids=uids(1182, 1185), target_asset_ids=aids(912),
        candidate_ids=bids(699) + bids(702),
        vocabulary_terms=("171-pattern basis", "local templates", "previous-page constraints"),
    ),
    route(
        "U001199", "H011651", 1,
        "the pictures on the next page",
        "iterative region-growth backtracking solver traces",
        WITHIN,
        target_unit_ids=uids(1204, 1205), target_asset_ids=aids(916),
        candidate_ids=bids(705),
        vocabulary_terms=("backtracking", "constraint solver", "region growth"),
    ),
    route(
        "U001201", "H011652", 1,
        "the third picture on the next page",
        "finite-region witness for globally unsatisfiable constraint 387520105",
        WITHIN,
        target_unit_ids=uids(1204, 1205), target_asset_ids=aids(916),
        candidate_ids=bids(705) + bids(707),
        vocabulary_terms=("constraint 387520105", "finite-region witness", "unsatisfiable constraint"),
    ),
    route(
        "U001206", "H011653", 1,
        "the system shown on the facing page",
        "first forced-nonrepetitive overlapping-template constraint",
        WITHIN,
        target_unit_ids=uids(1208, 1210), target_asset_ids=aids(917, 918),
        candidate_ids=bids(708),
        vocabulary_terms=("constraint 18762389", "forced nonrepetition", "nested pattern"),
    ),
    route(
        "U001212", "H011654", 1,
        "the kind of nested behavior seen on the previous page",
        "nested witness produced by required-template constraint 18762389",
        WITHIN,
        target_unit_ids=uids(1208, 1210), target_asset_ids=aids(917, 918),
        candidate_ids=bids(709),
        recovered_candidate_names=(
            "required-template constraint-family cardinality",
        ),
        vocabulary_terms=("nested witness", "required-template constraint", "previous page"),
    ),
    route(
        "U001217", "H011655", 1,
        "the example shown at the top of the facing page",
        "56-template rule-30-correspondence constraint and forced pattern",
        WITHIN,
        target_unit_ids=uids(1218, 1220), target_asset_ids=aids(921, 922),
        candidate_ids=bids(711),
        vocabulary_terms=("56 templates", "forced complex pattern", "rule 30 correspondence"),
    ),
    route(
        "U006082", "H011657", 1,
        "the 5-neighbor rules introduced on page 170",
        "main-text five-site square-neighborhood cellular-automaton family",
        WITHIN,
        target_unit_ids=uids(960, 965), target_asset_ids=aids(845, 846),
        candidate_ids=bids(853),
        vocabulary_terms=("5-neighbor rules", "cellular automaton", "page 170"),
    ),
    route(
        "U006085", "H011658", 1,
        "the 9-neighbor rules introduced on page 177",
        "main-text nine-site square-neighborhood cellular-automaton family",
        WITHIN,
        target_unit_ids=uids(980, 989), target_asset_ids=aids(852, 853),
        candidate_ids=bids(854),
        vocabulary_terms=("9-neighbor rules", "cellular automaton", "page 177"),
    ),
    route(
        "U006098", "H011659", 1,
        "page 53 for elementary rules",
        "elementary cellular-automaton neighborhood-configuration ordering",
        CROSS,
        candidate_ids=bids(857),
        recovered_candidate_names=(
            "general cellular-automaton rule-number codec",
        ),
        vocabulary_terms=("elementary rules", "neighborhood configurations", "rule numbering"),
    ),
    route(
        "U006098", "H011659", 2,
        "page 941 for 5-neighbor rules",
        "five-cell neighborhood-configuration ordering",
        WITHIN,
        target_unit_ids=uids(6286, 6287), target_asset_ids=aids(572),
        candidate_ids=bids(857),
        recovered_candidate_names=(
            "general cellular-automaton rule-number codec",
        ),
        vocabulary_terms=("5-neighbor rules", "neighborhood configurations", "rule numbering"),
    ),
    route(
        "U006106", "H011660", 1,
        "page 941",
        "the 32 five-cell neighborhoods used by the symmetric-class converter",
        WITHIN,
        target_unit_ids=uids(6286, 6287), target_asset_ids=aids(572),
        candidate_ids=bids(861),
        recovered_candidate_names=(
            "symmetric-5-neighbor-to-general-rule-code converter",
        ),
        vocabulary_terms=("32 neighborhoods", "5-neighbor rules", "symmetry classes"),
    ),
    route(
        "U006110", "H011661", 1,
        "the 9-neighbor examples on page 373",
        "nine-neighbor growth-rule examples",
        CROSS,
        candidate_ids=bids(860) + bids(862, 866),
        recovered_candidate_names=(
            "growth-totalistic trigger-list-to-outer-totalistic-code encoder",
        ),
        vocabulary_terms=("9-neighbor rules", "growth rules"),
    ),
    route(
        "U006126", "H011666", 1,
        "the Voronoi region (see page 987)",
        "Voronoi-cell derivation of nearest-neighbor lattice adjacency",
        CROSS,
        candidate_ids=bids(876),
        vocabulary_terms=("lattice adjacency", "nearest neighbors", "Voronoi region"),
    ),
    route(
        "U006130", "H011667", 1,
        "a nested Penrose tiling (see page 932)",
        "nested Penrose substitution tiling used as a cellular-automaton carrier",
        WITHIN,
        target_unit_ids=uids(6178, 6183), target_asset_ids=aids(550),
        candidate_ids=bids(884, 890),
        vocabulary_terms=("cellular automaton", "nested Penrose tiling", "page 932"),
    ),
    route(
        "U006130", "H011667", 2,
        "See also page 1027",
        "cellular automata on nonperiodic or nested tilings",
        CROSS,
        candidate_ids=bids(884, 890),
        vocabulary_terms=("cellular automaton", "nested tiling", "Penrose tiling"),
    ),
    route(
        "U006132", "H011668", 1,
        "See page 936",
        "binary-outdegree network mechanics underlying cellular automata on homogeneous networks",
        WITHIN,
        target_unit_ids=uids(6210, 6226),
        candidate_ids=bids(891),
        vocabulary_terms=("cellular automata on networks", "homogeneous networks", "network mechanics"),
    ),
    route(
        "U006132", "H011668", 2,
        "the constraints of the kind discussed on page 483",
        "longer-range network homogeneity constraints",
        CROSS,
        candidate_ids=bids(891),
        vocabulary_terms=("homogeneous networks", "longer-range rules", "network constraints"),
    ),
    route(
        "U006143", "H011670", 1,
        "the discussion of paths in substitution systems on page 892",
        "turn-relative path semantics in substitution systems",
        CROSS,
        candidate_ids=bids(895),
        vocabulary_terms=("paths", "substitution systems", "turning rules"),
    ),
    route(
        "U006145", "H011671", 1,
        "the rule on page 187",
        "page-187 two-dimensional block-substitution rule and seed",
        WITHIN,
        target_unit_ids=uids(1034, 1037), target_asset_ids=aids(874, 875),
        candidate_ids=bids(897, 898),
        vocabulary_terms=("block substitution", "page 187", "two-dimensional substitution"),
    ),
    route(
        "U006147", "H011672", 1,
        "the 1D case discussed on page 891",
        "one-dimensional digit-transducer substitution construction",
        CROSS,
        recovered_candidate_names=(
            "finite-automaton digit-array substitution-pattern generator",
        ),
        vocabulary_terms=("digit sequences", "finite automaton", "substitution systems"),
    ),
    route(
        "U006149", "H011673", 1,
        "the pattern on page 187",
        "page-187 Sierpiński block-substitution preset",
        WITHIN,
        target_unit_ids=uids(1034, 1037), target_asset_ids=aids(874, 875),
        candidate_ids=bids(898),
        recovered_candidate_names=(
            "finite-automaton digit-array substitution-pattern generator",
        ),
        vocabulary_terms=("page 187", "Sierpiński pattern", "substitution system"),
    ),
    route(
        "U006149", "H011673", 2,
        "patterns (a) through (f) on page 188",
        "page-188 two-dimensional substitution presets (a) through (f)",
        WITHIN,
        target_unit_ids=uids(1038, 1041), target_asset_ids=aids(876),
        recovered_candidate_names=(
            "finite-automaton digit-array substitution-pattern generator",
        ),
        vocabulary_terms=("page 188", "substitution presets"),
    ),
    route(
        "U006149", "H011673", 3,
        "See pages 608 and 1091",
        "digit-pair exclusion correspondences for the substitution generator",
        CROSS,
        recovered_candidate_names=(
            "finite-automaton digit-array substitution-pattern generator",
        ),
        vocabulary_terms=("digit pairs", "substitution systems"),
    ),
    route(
        "U006150", "H011674", 1,
        "Page 187 · Sierpiński pattern",
        "page-187 Sierpiński block-substitution pattern",
        WITHIN,
        target_unit_ids=uids(1034, 1037), target_asset_ids=aids(874, 875),
        recovered_candidate_names=(
            "binomial-parity Sierpiński array generator",
            "bitwise-AND-complement Sierpiński array generator",
            "rotate-add modulo-2 Sierpiński evolution generator",
            "convolution modulo-2 Sierpiński evolution generator",
            "bit-XOR recurrence Sierpiński array generator",
            "cumulative-sum modulo-2 Sierpiński evolution generator",
            "binomial-coefficient Sierpiński array generator",
            "bivariate-series Sierpiński array generator",
            "block-join substitution Sierpiński array generator",
            "affine-tripling Sierpiński coordinate enumerator",
            "complex-affine Sierpiński coordinate enumerator",
            "odd-multiplicity Sierpiński coordinate enumerator",
            "binary-position-fold Sierpiński coordinate enumerator",
            "nested-tree-path Sierpiński coordinate enumerator",
        ),
        vocabulary_terms=("page 187", "Sierpiński pattern"),
    ),
    route(
        "U006151", "H011675", 1,
        "see pages 611 and 870",
        "binomial-parity Sierpiński-array correspondences",
        CROSS,
        recovered_candidate_names=(
            "binomial-parity Sierpiński array generator",
        ),
        vocabulary_terms=("binomial parity", "Sierpiński array"),
    ),
    route(
        "U006152", "H011676", 1,
        "see pages 608 and 871",
        "bitwise-AND Sierpiński-array correspondences",
        CROSS,
        recovered_candidate_names=(
            "bitwise-AND-complement Sierpiński array generator",
        ),
        vocabulary_terms=("bitwise AND", "Sierpiński array"),
    ),
    route(
        "U006153", "H011677", 1,
        "see page 870",
        "rotate-add modulo-two Sierpiński evolution correspondence",
        CROSS,
        recovered_candidate_names=(
            "rotate-add modulo-2 Sierpiński evolution generator",
        ),
        vocabulary_terms=("modulo 2", "rotate add", "Sierpiński evolution"),
    ),
    route(
        "U006154", "H011678", 1,
        "see page 870",
        "convolution modulo-two Sierpiński evolution correspondence",
        CROSS,
        recovered_candidate_names=(
            "convolution modulo-2 Sierpiński evolution generator",
        ),
        vocabulary_terms=("convolution", "modulo 2", "Sierpiński evolution"),
    ),
    route(
        "U006155", "H011679", 1,
        "see page 906",
        "bit-XOR Sierpiński recurrence correspondence",
        CROSS,
        recovered_candidate_names=(
            "bit-XOR recurrence Sierpiński array generator",
        ),
        vocabulary_terms=("bit XOR", "recurrence", "Sierpiński array"),
    ),
    route(
        "U006156", "H011680", 1,
        "see page 1034",
        "cumulative-sum modulo-two Sierpiński correspondence",
        CROSS,
        recovered_candidate_names=(
            "cumulative-sum modulo-2 Sierpiński evolution generator",
        ),
        vocabulary_terms=("cumulative sum", "modulo 2", "Sierpiński evolution"),
    ),
    route(
        "U006157", "H011681", 1,
        "see pages 870 and 951",
        "binomial-coefficient Sierpiński-array correspondences",
        CROSS,
        recovered_candidate_names=(
            "binomial-coefficient Sierpiński array generator",
        ),
        vocabulary_terms=("binomial coefficients", "Sierpiński array"),
    ),
    route(
        "U006158", "H011682", 1,
        "see page 1091",
        "bivariate-series Sierpiński-array correspondence",
        CROSS,
        recovered_candidate_names=(
            "bivariate-series Sierpiński array generator",
        ),
        vocabulary_terms=("bivariate series", "Sierpiński array"),
    ),
    route(
        "U006163", "H011685", 1,
        "see page 358",
        "odd-multiplicity coordinate-enumerator correspondence",
        CROSS,
        recovered_candidate_names=(
            "odd-multiplicity Sierpiński coordinate enumerator",
        ),
        vocabulary_terms=("coordinate enumeration", "odd multiplicity", "Sierpiński pattern"),
    ),
    route(
        "U006164", "H011686", 1,
        "see page 870",
        "binary-position-fold coordinate-enumerator correspondence",
        CROSS,
        recovered_candidate_names=(
            "binary-position-fold Sierpiński coordinate enumerator",
        ),
        vocabulary_terms=("binary positions", "coordinate enumeration", "Sierpiński pattern"),
    ),
    route(
        "U006165", "H011687", 1,
        "see page 509",
        "nested-tree-path coordinate-enumerator correspondence",
        CROSS,
        recovered_candidate_names=(
            "nested-tree-path Sierpiński coordinate enumerator",
        ),
        vocabulary_terms=("coordinate enumeration", "nested tree", "Sierpiński pattern"),
    ),
    route(
        "U006172", "H011689", 1,
        "the 2D rule on page 187",
        "two-dimensional antecedent of the three-dimensional substitution preset",
        WITHIN,
        target_unit_ids=uids(1034, 1037), target_asset_ids=aids(874, 875),
        candidate_ids=bids(901),
        vocabulary_terms=("page 187", "three-dimensional substitution", "two-dimensional analog"),
    ),
    route(
        "U006175", "H011690", 1,
        "The systems on pages 187 and 188",
        "square-subdivision substitution systems contrasted with other-shape systems",
        WITHIN,
        target_unit_ids=uids(1034, 1041), target_asset_ids=aids(874, 876),
        candidate_ids=bids(902, 903),
        vocabulary_terms=("other shapes", "square subdivision", "substitution systems"),
    ),
    route(
        "U006178", "H011691", 1,
        "see page 943",
        "Penrose aperiodic-tiling identity and substitution provenance",
        WITHIN,
        target_unit_ids=uids(6310),
        candidate_ids=bids(904),
        vocabulary_terms=("Penrose tiling", "substitution tiling"),
    ),
    route(
        "U006182", "H011692", 1,
        "page 83",
        "one-dimensional Fibonacci substitution-system antecedent",
        CROSS,
        recovered_candidate_names=(
            "five-dimensional cut-and-project Penrose tiling generator",
        ),
        vocabulary_terms=("Fibonacci substitution", "Penrose pattern"),
    ),
    route(
        "U006182", "H011692", 2,
        "page 903",
        "GoldenRatio line-cut construction for the Fibonacci sequence",
        CROSS,
        recovered_candidate_names=(
            "five-dimensional cut-and-project Penrose tiling generator",
        ),
        vocabulary_terms=("cut and project", "Fibonacci sequence", "GoldenRatio"),
    ),
    route(
        "U006182", "H011692", 3,
        "See also page 943",
        "Penrose aperiodic-tiling identity and substitution provenance",
        WITHIN,
        target_unit_ids=uids(6310),
        recovered_candidate_names=(
            "five-dimensional cut-and-project Penrose tiling generator",
        ),
        vocabulary_terms=("Penrose tiling", "substitution tiling"),
    ),
    route(
        "U006184", "H011693", 1,
        "Page 189 · Dragon curve",
        "page-189 dragon-curve geometrical substitution preset",
        WITHIN,
        target_unit_ids=uids(1042, 1045), target_asset_ids=aids(877, 878),
        candidate_ids=bids(905),
        vocabulary_terms=("dragon curve", "geometrical substitution", "page 189"),
    ),
    route(
        "U006184", "H011693", 2,
        "page 892",
        "paperfolding path construction corresponding to the dragon curve",
        CROSS,
        candidate_ids=bids(905),
        vocabulary_terms=("dragon curve", "paperfolding", "substitution paths"),
    ),
    route(
        "U006185", "H011694", 1,
        "the rule on page 189",
        "page-189 dragon-curve geometrical substitution rule",
        WITHIN,
        target_unit_ids=uids(1042, 1045), target_asset_ids=aids(877, 878),
        candidate_ids=bids(905),
        vocabulary_terms=("dragon curve", "geometrical substitution", "page 189"),
    ),
    route(
        "U006185", "H011694", 2,
        "the rule on page 190",
        "page-190 overlap-producing geometrical substitution rule",
        WITHIN,
        target_unit_ids=uids(1046, 1049), target_asset_ids=aids(879, 880),
        candidate_ids=bids(906),
        vocabulary_terms=("geometrical substitution", "page 190"),
    ),
    route(
        "U006185", "H011694", 3,
        "rules (a), (b) and (c) (Koch curve) on page 191",
        "three page-191 geometrical substitution rules",
        WITHIN,
        target_unit_ids=uids(1050, 1055), target_asset_ids=aids(881),
        candidate_ids=bids(907, 909),
        vocabulary_terms=("geometrical substitution", "Koch curve", "page 191"),
    ),
    route(
        "U006187", "H011695", 1,
        "the patterns on page 189",
        "page-189 geometrical-substitution pattern",
        WITHIN,
        target_unit_ids=uids(1042, 1045), target_asset_ids=aids(877, 878),
        recovered_candidate_names=(
            "base-(i-1) binary-digit point-set generator",
        ),
        vocabulary_terms=("base i-1", "geometrical substitution", "page 189"),
    ),
    route(
        "U006189", "H011696", 1,
        "Compare page 1094",
        "complex-base representability and completeness conditions",
        CROSS,
        recovered_candidate_names=(
            "base-(i-1) binary-digit point-set generator",
        ),
        vocabulary_terms=("complex base", "representability", "digit point set"),
    ),
    route(
        "U006195", "H011698", 1,
        "the discussion of page 1138",
        "noncomputability limit for dimension observers",
        CROSS,
        recovered_candidate_names=(
            "box-counting fractal-dimension observer",
        ),
        vocabulary_terms=("fractal dimension", "noncomputability"),
    ),
    route(
        "U006196", "H011699", 1,
        "Compare page 959",
        "distribution-moment generalizations of fractal dimension",
        CROSS,
        recovered_candidate_names=(
            "grid-occupancy distribution-moment observer",
        ),
        vocabulary_terms=("distribution moments", "fractal dimension"),
    ),
    route(
        "U006202", "H011701", 1,
        "pages 407 and 1006",
        "parameter-space sets analogous to the Mandelbrot set",
        CROSS,
        recovered_candidate_names=(
            "Julia-set zero-membership to Mandelbrot-boundary relation",
        ),
        vocabulary_terms=("Mandelbrot set", "parameter space"),
    ),
    route(
        "U006205", "H011702", 1,
        "Page 192 · Neighbor-dependent substitution systems",
        "main-text neighbor-dependent two-dimensional substitution system",
        WITHIN,
        target_unit_ids=uids(1056, 1060), target_asset_ids=aids(882),
        candidate_ids=bids(914),
        vocabulary_terms=("neighbor-dependent substitution", "page 192"),
    ),
    route(
        "U006208", "H011703", 1,
        "Page 192 · Space-filling curves",
        "main-text two-dimensional grid-scanning problem and scan order",
        WITHIN,
        target_unit_ids=uids(1056, 1062), target_asset_ids=aids(882),
        candidate_ids=bids(915),
        vocabulary_terms=("grid scan", "page 192", "space-filling curves"),
    ),
