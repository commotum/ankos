#!/usr/bin/env python3
"""Frozen Stage 9 Chapter 5 local-search route authoring specification.

This module is data only.  It does not read or write any audit ledger.
`ROUTE_SPECS` materializes the 151 new route rows in immutable final-F15
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
        "U006078", "H011656", 1,
        "Page 170 · 1D phenomena",
        "dimension-specific phenomenon boundary for the main-text cellular-automaton setting",
        WITHIN,
        target_unit_ids=uids(960, 965), target_asset_ids=aids(845, 846),
        vocabulary_terms=("dimensional boundary", "one-dimensional phenomena", "page 170"),
    ),
    route(
        "U006078", "H011656", 2,
        "see page 981",
        "reversible-rule phase-transition comparison for dimensional phenomena",
        CROSS,
        vocabulary_terms=("phase transition", "reversible evolution", "one dimension"),
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
        "U006121", "H011664", 1,
        "discussed on page 979",
        "fixed-interior and cycling-region behavior of cellular automaton code 746",
        CROSS,
        candidate_ids=bids(662),
        vocabulary_terms=("approximate circle", "code 746", "cycling regions"),
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
        "U006126", "H011666", 2,
        "Compare pages 1029 and 986",
        "crystallographic terminology and Voronoi-region shape comparison",
        CROSS,
        candidate_ids=bids(876),
        vocabulary_terms=("crystallography", "lattice geometry", "Voronoi region"),
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
        "U006159", "H011683", 1,
        "compare page 1073",
        "alternate formula comparison for the block-join Sierpiński array generator",
        CROSS,
        recovered_candidate_names=(
            "block-join substitution Sierpiński array generator",
        ),
        vocabulary_terms=("block join", "formula comparison", "Sierpiński array"),
    ),
    route(
        "U006162", "H011684", 1,
        "compare page 1005",
        "alternate formula comparison for the complex-affine Sierpiński coordinate enumerator",
        CROSS,
        recovered_candidate_names=(
            "complex-affine Sierpiński coordinate enumerator",
        ),
        vocabulary_terms=("complex affine", "coordinate enumeration", "formula comparison"),
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
    route(
        "U006227", "H011705", 1,
        "discussed on page 1121",
        "combinator-system comparison for the binary-outdegree network representation",
        CROSS,
        vocabulary_terms=("binary-outdegree network", "combinator systems", "data structures"),
    ),
    route(
        "U006227", "H011705", 2,
        "Page 202 · Properties",
        "page-202(c) network node-count sequence and binary-digit recurrence",
        WITHIN,
        target_unit_ids=uids(1111, 1115), target_asset_ids=aids(892),
        recovered_candidate_names=(
            "page-202(c) network node-count sequence generator",
        ),
        vocabulary_terms=("binary-digit recurrence", "network node count", "page 202"),
    ),
    route(
        "U006234", "H011706", 1,
        "page 479",
        "network dimension defined by radius-r reachable-volume growth",
        CROSS,
        recovered_candidate_names=(
            "network dimensionality observer",
        ),
        vocabulary_terms=("dimension", "network radius", "reachable volume"),
    ),
    route(
        "U006234", "H011706", 2,
        "the systems on pages 202 and 203",
        "network-rule systems used by the dimensionality observer",
        WITHIN,
        target_unit_ids=uids(1111, 1121), target_asset_ids=aids(892, 893),
        recovered_candidate_names=(
            "network dimensionality observer",
        ),
        vocabulary_terms=("dimension", "network rules", "pages 202 and 203"),
    ),
    route(
        "U006236", "H011707", 1,
        "page 259",
        "finite-size cellular-automaton comparison for homogeneous-network automata",
        CROSS,
        candidate_ids=bids(891),
        vocabulary_terms=("cellular automata", "finite size", "homogeneous networks"),
    ),
    route(
        "U006238", "H011708", 1,
        "Chapter 6",
        "behavior classes of random Boolean networks",
        CROSS,
        route_kind="SECTION",
        candidate_ids=bids(920),
        vocabulary_terms=("behavior classes", "random Boolean networks"),
    ),
    route(
        "U006238", "H011708", 2,
        "page 963",
        "random-mapping comparison for random Boolean networks",
        CROSS,
        candidate_ids=bids(920),
        vocabulary_terms=("random Boolean networks", "random mappings"),
    ),
    route(
        "U006248", "H011709", 1,
        "The case shown on page 206",
        "page-206 three-rule slow-growth multiway preset",
        WITHIN,
        target_unit_ids=uids(1140, 1143), target_asset_ids=aids(901, 902),
        candidate_ids=bids(922),
        vocabulary_terms=("multiway preset", "page 206", "three rules"),
    ),
    route(
        "U006252", "H011710", 1,
        "pictures like those on page 208",
        "page-208 multiway state collections used to illustrate polynomial growth",
        WITHIN,
        target_unit_ids=uids(1148, 1150), target_asset_ids=aids(904),
        recovered_candidate_names=(
            "polynomial-growth string-multiway preset",
            "polynomial-growth multiway state-count asymptotic profile",
        ),
        vocabulary_terms=("multiway state count", "page 208", "polynomial growth"),
    ),
    route(
        "U006255", "H011711", 1,
        "Page 206 · Properties",
        "page-206 multiway preset properties and state-count diagnostics",
        WITHIN,
        target_unit_ids=uids(1140, 1143), target_asset_ids=aids(901, 902),
        candidate_ids=bids(691),
        recovered_candidate_names=(
            "multiway state-count and first-difference observer",
        ),
        vocabulary_terms=("first differences", "multiway state count", "page 206"),
    ),
    route(
        "U006256", "H011712", 1,
        "as on page 208",
        "page-208 layered display of complete multiway state collections",
        WITHIN,
        target_unit_ids=uids(1148, 1150), target_asset_ids=aids(904),
        recovered_candidate_names=(
            "stacked multiway-state evolution representation",
        ),
        vocabulary_terms=("layered history", "multiway states", "page 208"),
    ),
    route(
        "U006258", "H011713", 1,
        "In analogy with page 796",
        "bounded-length reachability display for a string multiway system",
        CROSS,
        recovered_candidate_names=(
            "bounded-length multiway reachability observer",
        ),
        vocabulary_terms=("bounded length", "multiway reachability", "strings"),
        defect_boundary=(
            "The source reads “shows wh different strings”; the missing OCR "
            "word and the plotted axis/string encoding are not inferred."
        ),
        attempts=(
            "Queued literal target 'In analogy with page 796' for the "
            "bounded-length reachability display outside the assigned "
            "Chapter 5 source range. The target was not opened, no target "
            "mechanics were inferred, and the OCR-defective phrase “shows "
            "wh different strings” remains unresolved.",
        ),
    ),
    route(
        "U006261", "H011714", 1,
        "as on page 206",
        "page-206 string multiway system used by the group and semigroup interpretation",
        WITHIN,
        target_unit_ids=uids(1140, 1143), target_asset_ids=aids(901, 902),
        candidate_ids=bids(921) + bids(924, 925),
        vocabulary_terms=("group", "multiway system", "page 206", "semigroup"),
    ),
    route(
        "U006263", "H011715", 1,
        "the ones shown on page 196",
        "tree-network exemplars for the free-semigroup Cayley graph",
        WITHIN,
        target_unit_ids=uids(1083, 1085), target_asset_ids=aids(885),
        recovered_candidate_names=(
            "group-or-semigroup Cayley-graph generator family",
            "free-semigroup Cayley-tree preset",
        ),
        vocabulary_terms=("Cayley graph", "free semigroup", "tree network"),
    ),
    route(
        "U006264", "H011716", 1,
        "Compare page 945",
        "homogeneous-network context for the A5 Cayley-graph presentation",
        WITHIN,
        target_unit_ids=uids(6132),
        recovered_candidate_names=(
            "A5 icosahedral-group presentation",
        ),
        vocabulary_terms=("A5", "Cayley graph", "homogeneous network"),
    ),
    route(
        "U006265", "H011717", 1,
        "See also pages 945 and 1032",
        "Monster Group finite-group denotation and referenced omitted presentation",
        CROSS,
        target_unit_ids=uids(6132),
        recovered_candidate_names=(
            "Monster Group finite-group denotation with source-omitted presentation",
        ),
        vocabulary_terms=("finite group", "Monster Group", "order", "presentation"),
        defect_boundary=(
            "The source gives the exact group order but only says that a "
            "dozen rules yield the group; it omits the generators, relations, "
            "rule list, and quotient reconstruction."
        ),
        attempts=(
            "Resolved the page-945 half of literal target 'See also pages "
            "945 and 1032' only to U006132, which states the homogeneous "
            "Cayley-graph carrier context. Page 1032 lies outside the "
            "assigned Chapter 5 range and was not opened; no generators, "
            "relations, rule list, or quotient mechanics were inferred.",
        ),
    ),
    route(
        "U006267", "H011718", 1,
        "page 1104",
        "Chomsky hierarchy classification of the displayed grammar families",
        CROSS,
        candidate_ids=bids(926, 929),
        vocabulary_terms=("Chomsky hierarchy", "generative grammars", "formal languages"),
    ),
    route(
        "U006268", "H011719", 1,
        "page 957",
        "finite-automaton recognition of the no-adjacent-B regular language",
        CROSS,
        candidate_ids=bids(926),
        recovered_candidate_names=(
            "no-adjacent-B regular-grammar preset",
        ),
        vocabulary_terms=("finite automaton", "no adjacent B", "regular language"),
    ),
    route(
        "U006269", "H011720", 1,
        "pages 1091 and 1103",
        "context-free-language properties of the AxA-or-B grammar",
        CROSS,
        candidate_ids=bids(927),
        recovered_candidate_names=(
            "AxA-or-B context-free-grammar preset",
        ),
        vocabulary_terms=("AxA or B", "context-free grammar", "formal language"),
    ),
    route(
        "U006272", "H011721", 1,
        "See also page 944",
        "inspected page-944 comparison boundary for the formal-language discussion",
        WITHIN,
        target_unit_ids=uids(6114, 6125),
        target_asset_ids=(
            "A000527", "A000528", "A000541", "A000542",
        ),
        vocabulary_terms=("formal languages", "page 944", "comparison boundary"),
        defect_boundary=(
            "The source gives only a bare cross-reference. Inspected page "
            "944 contains two-dimensional cellular-automaton history, rules, "
            "behavior, and projections, but states no grammar identity or "
            "equivalence."
        ),
        attempts=(
            "Resolved literal target 'See also page 944' to inspected units "
            "U006114-U006125 and referenced assets A000527, A000528, "
            "A000541, and A000542. Those targets contain two-dimensional "
            "cellular-automaton material; no explicit comparison predicate, "
            "grammar identity, or grammar equivalence is asserted or "
            "inferred.",
        ),
    ),
    route(
        "U006275", "H011723", 1,
        "page 933",
        "fractal-dimension comparison for the numeric multiway evolution",
        WITHIN,
        target_unit_ids=uids(6184, 6196), target_asset_ids=aids(551, 552),
        candidate_ids=bids(932),
        vocabulary_terms=("fractal dimension", "multiway system", "numeric evolution"),
    ),
    route(
        "U006275", "H011723", 2,
        "discussed on page 907",
        "recursive-sequence comparison for the numeric multiway system",
        CROSS,
        candidate_ids=bids(932),
        vocabulary_terms=("numeric multiway system", "recursive sequences"),
    ),
    route(
        "U006275", "H011723", 3,
        "page 937",
        "network representation of the numeric multiway evolution",
        WITHIN,
        target_unit_ids=uids(6253, 6254),
        candidate_ids=bids(932),
        vocabulary_terms=("multiway network", "numeric evolution", "page 937"),
    ),
    route(
        "U006276", "H011724", 1,
        "But see page 766",
        "computational-power exception boundary for nondeterministic systems",
        CROSS,
        vocabulary_terms=("computational power", "nondeterministic systems"),
    ),
    route(
        "U006276", "H011724", 2,
        "page 871",
        "bitwise-XOR characterization used by the nim losing-position predicate",
        CROSS,
        candidate_ids=bids(933),
        recovered_candidate_names=(
            "nim zero-XOR losing-position predicate",
        ),
        vocabulary_terms=("bitwise XOR", "losing position", "nim"),
    ),
    route(
        "U006279", "H011725", 1,
        "page 923",
        "initial-value and boundary-value formulation of partial differential equations",
        CROSS,
        candidate_ids=bids(935, 936),
        vocabulary_terms=("boundary value", "initial value", "partial differential equation"),
    ),
    route(
        "U006282", "H011726", 1,
        "Page 211 · 1D constraints",
        "main-text one-dimensional allowed-block constraints",
        WITHIN,
        target_unit_ids=uids(1162, 1171), target_asset_ids=aids(908, 909),
        candidate_ids=bids(940, 941),
        vocabulary_terms=("allowed blocks", "one-dimensional constraints", "page 211"),
    ),
    route(
        "U006284", "H011727", 1,
        "The constraint on page 210",
        "period-four witness for the main-text one-dimensional constraint",
        WITHIN,
        target_unit_ids=uids(1162, 1165), target_asset_ids=aids(908),
        candidate_ids=bids(940, 941),
        vocabulary_terms=("allowed blocks", "period four", "one-dimensional constraint"),
    ),
    route(
        "U006284", "H011727", 2,
        "See also page 266",
        "one-dimensional constraint periodicity comparison",
        CROSS,
        candidate_ids=bids(940, 941),
        vocabulary_terms=("constraint periodicity", "one-dimensional constraint"),
    ),
    route(
        "U006285", "H011728", 1,
        "page 225",
        "cellular-automaton convergence to invariant configurations",
        CROSS,
        candidate_ids=bids(942),
        vocabulary_terms=("cellular automaton", "invariant configurations"),
    ),
    route(
        "U006285", "H011728", 2,
        "See page 954",
        "cellular-automaton invariant-configuration correspondence",
        CROSS,
        candidate_ids=bids(942),
        vocabulary_terms=("cellular automaton", "fixed point", "invariant configuration"),
    ),
    route(
        "U006285", "H011728", 3,
        "See page 958",
        "finite-complement-language and subshift-of-finite-type terminology",
        CROSS,
        candidate_ids=bids(940),
        vocabulary_terms=("finite complement language", "subshift of finite type"),
    ),
    route(
        "U006285", "H011728", 4,
        "Page 215 · 2D constraints",
        "main-text minimal two-dimensional local-template constraints",
        WITHIN,
        target_unit_ids=uids(1186, 1188), target_asset_ids=aids(913, 914),
        candidate_ids=bids(943),
        vocabulary_terms=("local templates", "minimal constraints", "two-dimensional constraints"),
    ),
    route(
        "U006286", "H011729", 1,
        "See also page 927",
        "canonical binary rule-number ordering used by the constraint-number decoder",
        WITHIN,
        target_unit_ids=uids(6096, 6101),
        candidate_ids=bids(943),
        recovered_candidate_names=(
            "two-dimensional constraint-number decoder",
        ),
        vocabulary_terms=("binary code", "constraint numbering", "template ordering"),
    ),
    route(
        "U006290", "H011730", 1,
        "page 213",
        "main-text periodic tessellation encoded by overlapping corners",
        WITHIN,
        target_unit_ids=uids(1182, 1184), target_asset_ids=aids(912),
        recovered_candidate_names=(
            "overlapping-corner tessellation descriptor and Fill generator",
        ),
        vocabulary_terms=("Fill", "overlapping corners", "periodic tessellation"),
    ),
    route(
        "U006295", "H011731", 1,
        "page 1139",
        "undecidability of infinite-pattern constraint satisfaction",
        CROSS,
        candidate_ids=bids(945),
        vocabulary_terms=("constraint satisfaction", "infinite pattern", "undecidability"),
    ),
    route(
        "U006295", "H011731", 2,
        "page 1145",
        "NP-completeness of finite-region constraint satisfaction",
        CROSS,
        candidate_ids=bids(945),
        vocabulary_terms=("finite region", "NP-complete", "satisfaction"),
    ),
    route(
        "U006295", "H011731", 3,
        "Compare page 959",
        "enumeration and solver comparison for two-dimensional constraints",
        CROSS,
        candidate_ids=bids(945),
        vocabulary_terms=("constraint solver", "enumeration", "two-dimensional constraints"),
    ),
    route(
        "U006295", "H011731", 4,
        "Page 219 · Non-periodic pattern",
        "main-text forced-nonperiodic constraint witness",
        WITHIN,
        target_unit_ids=uids(1208, 1210), target_asset_ids=aids(917, 918),
        candidate_ids=bids(945),
        vocabulary_terms=("forced nonperiodicity", "non-periodic pattern", "page 219"),
    ),
    route(
        "U006297", "H011732", 1,
        "page 117",
        "nested-pattern comparison for the exhaustive constraint search",
        CROSS,
        candidate_ids=bids(945),
        vocabulary_terms=("constraint search", "nested pattern"),
    ),
    route(
        "U006301", "H011733", 1,
        "page 188",
        "main-text two-dimensional substitution patterns used by the Ammann-derived constraint",
        WITHIN,
        target_unit_ids=uids(1038, 1041), target_asset_ids=aids(876),
        candidate_ids=bids(948),
        recovered_candidate_names=(
            "Ammann 16-symbol substitution system",
            "substitution-pattern local-template occurrence extractor",
        ),
        vocabulary_terms=("Ammann", "local template", "substitution system"),
    ),
    route(
        "U006305", "H011734", 1,
        "pages 941 and 954",
        "constraint-number decoding and cellular-automaton correspondence",
        CROSS,
        target_unit_ids=uids(6286, 6289), target_asset_ids=aids(572),
        candidate_ids=bids(949),
        vocabulary_terms=("cellular automaton", "constraint numbering", "nested pattern"),
        attempts=(
            "Resolved the page-941 half of literal target 'pages 941 and "
            "954' to U006286-U006289/A000572, which supplies the canonical "
            "constraint-number decoder and satisfaction check. Page 954 "
            "lies outside the assigned Chapter 5 range and was not opened; "
            "no cellular-automaton correspondence mechanics were inferred.",
        ),
    ),
    route(
        "U006305", "H011734", 2,
        "page 170",
        "main-text five-site cellular-automaton family used in the constraint correspondence",
        WITHIN,
        target_unit_ids=uids(960, 965), target_asset_ids=aids(845, 846),
        candidate_ids=bids(949),
        vocabulary_terms=("cellular automaton", "constraint correspondence", "page 170"),
    ),
    route(
        "U006310", "H011735", 1,
        "page 1139",
        "undecidability boundary for determining whether a tiling exists",
        CROSS,
        candidate_ids=bids(951, 952),
        vocabulary_terms=("tiling existence", "undecidability"),
    ),
    route(
        "U006310", "H011735", 2,
        "see page 994",
        "fivefold-symmetry comparison for the Penrose tiling",
        CROSS,
        candidate_ids=bids(951, 952),
        vocabulary_terms=("fivefold symmetry", "Penrose tiling"),
    ),
    route(
        "U006312", "H011736", 1,
        "page 221",
        "main-text aperiodic tiling and nonrepetitive-pattern examples",
        WITHIN,
        target_unit_ids=uids(1217, 1220), target_asset_ids=aids(921, 922),
        candidate_ids=bids(951, 952),
        vocabulary_terms=("aperiodic tiling", "nonrepetitive pattern", "page 221"),
    ),
    route(
        "U006313", "H011737", 1,
        "See also page 1139",
        "undecidability evidence boundary for aperiodic tiling constraints",
        CROSS,
        candidate_ids=bids(951, 952),
        vocabulary_terms=("aperiodic tiling", "tiling constraints", "undecidability"),
    ),
    route(
        "U006318", "H011738", 1,
        "page 1141",
        "enumeration complexity for square-free sequences",
        CROSS,
        candidate_ids=bids(958),
        vocabulary_terms=("enumeration", "square-free sequence"),
    ),
    route(
        "U006321", "H011739", 1,
        "page 83",
        "Thue-Morse nested-sequence antecedent for cube-free blocks",
        CROSS,
        candidate_ids=bids(960),
        vocabulary_terms=("cube-free", "nested sequence", "Thue-Morse"),
    ),
    route(
        "U006322", "H011740", 1,
        "page 1068",
        "unavoidable-block-pattern bounds",
        CROSS,
        candidate_ids=bids(961),
        vocabulary_terms=("avoidable pattern", "block pattern", "unavoidable pattern"),
    ),
    route(
        "U006323", "H011741", 1,
        "page 938",
        "formal-language grammar families used to express one-dimensional constraints",
        WITHIN,
        target_unit_ids=uids(6267, 6271),
        vocabulary_terms=("formal language", "generative grammar", "one-dimensional constraint"),
    ),
    route(
        "U006323", "H011741", 2,
        "page 210",
        "main-text one-dimensional constraint as a regular-language special case",
        WITHIN,
        target_unit_ids=uids(1162, 1165), target_asset_ids=aids(908),
        vocabulary_terms=("one-dimensional constraint", "regular language"),
    ),
    route(
        "U006323", "H011741", 3,
        "page 940",
        "finite-complement and subshift terminology for regular-language constraints",
        WITHIN,
        target_unit_ids=uids(6285),
        vocabulary_terms=("finite complement language", "regular language", "subshift of finite type"),
    ),
    route(
        "U006330", "H011742", 1,
        "page 1078",
        "primitive Pythagorean-triple parameterization",
        CROSS,
        candidate_ids=bids(969),
        recovered_candidate_names=(
            "primitive Pythagorean-triple parameterization",
        ),
        vocabulary_terms=("primitive triples", "Pythagorean triples", "parameterization"),
    ),
    route(
        "U006332", "H011743", 1,
        "page 1160",
        "odd-binomial-coefficient parity relation",
        CROSS,
        recovered_candidate_names=(
            "odd-binomial-coefficient parity relation",
        ),
        vocabulary_terms=("binomial coefficient", "odd parity", "Diophantine relation"),
    ),
    route(
        "U006335", "H011744", 1,
        "See pages 791 and 1164",
        "sparse-solution and higher-power comparison for the Fermat relation",
        CROSS,
        candidate_ids=bids(978),
        vocabulary_terms=("Fermat relation", "higher powers", "sparse solutions"),
    ),
    route(
        "U006336", "H011745", 1,
        "See also page 805",
        "matrix-power pattern constraints",
        CROSS,
        candidate_ids=bids(979),
        vocabulary_terms=("matrix powers", "pattern constraints"),
    ),
    route(
        "U006336", "H011745", 2,
        "page 938",
        "simple finite-group classification context",
        WITHIN,
        target_unit_ids=uids(6264, 6266),
        recovered_candidate_names=(
            "finite group-and-semigroup count-by-order observer",
        ),
        vocabulary_terms=("finite groups", "simple groups", "classification"),
    ),
    route(
        "U006336", "H011745", 3,
        "See also pages 938 and 1032",
        "finite-group classification and enumeration boundary",
        CROSS,
        target_unit_ids=uids(6264, 6266),
        recovered_candidate_names=(
            "finite group-and-semigroup count-by-order observer",
        ),
        vocabulary_terms=("enumeration", "finite groups", "simple groups"),
        attempts=(
            "Resolved the page-938 half of literal target 'See also pages "
            "938 and 1032' to U006264-U006266, which supplies finite-group "
            "examples and the classification context. Page 1032 lies "
            "outside the assigned Chapter 5 range and was not opened; no "
            "practical enumeration algorithm or omitted mechanics were "
            "inferred.",
        ),
    ),
)


# Final family-15 hit order.  H011603 corresponds to the first unit and the
# IDs then increase by one through H011746.
F15_HIT_UNITS = (
    "U000965", "U000968", "U000971", "U000972", "U000974", "U000976",
    "U000978", "U000980", "U000981", "U000982", "U000983", "U000984",
    "U000991", "U000995", "U000997", "U001002", "U001005", "U001016",
    "U001031", "U001033", "U001038", "U001046", "U001050", "U001052",
    "U001053", "U001056", "U001057", "U001062", "U001075", "U001076",
    "U001091", "U001095", "U001101", "U001108", "U001111", "U001113",
    "U001129", "U001144", "U001147", "U001148", "U001150", "U001151",
    "U001152", "U001166", "U001178", "U001184", "U001185", "U001188",
    "U001199", "U001201", "U001206", "U001212", "U001217", "U006078",
    "U006082", "U006085", "U006098", "U006106", "U006110", "U006112",
    "U006114", "U006121", "U006123", "U006126", "U006130", "U006132",
    "U006139", "U006143", "U006145", "U006147", "U006149", "U006150",
    "U006151", "U006152", "U006153", "U006154", "U006155", "U006156",
    "U006157", "U006158", "U006159", "U006162", "U006163", "U006164",
    "U006165", "U006168", "U006172", "U006175", "U006178", "U006182",
    "U006184", "U006185", "U006187", "U006189", "U006192", "U006195",
    "U006196", "U006197", "U006202", "U006205", "U006208", "U006226",
    "U006227", "U006234", "U006236", "U006238", "U006248", "U006252",
    "U006255", "U006256", "U006258", "U006261", "U006263", "U006264",
    "U006265", "U006267", "U006268", "U006269", "U006272", "U006273",
    "U006275", "U006276", "U006279", "U006282", "U006284", "U006285",
    "U006286", "U006290", "U006295", "U006297", "U006301", "U006305",
    "U006310", "U006312", "U006313", "U006318", "U006321", "U006322",
    "U006323", "U006330", "U006332", "U006335", "U006336", "U006338",
)


def f15_hit_id(source_unit_id: str) -> str:
    """Return the frozen final-F15 hit ID for one hit unit."""

    return f"H{11603 + F15_HIT_UNITS.index(source_unit_id):06d}"


def existing_route_use(
    route_id: str,
    source_unit_id: str,
    literal_target: str,
    expected_topic: str,
    *,
    route_kind: str = "PAGE",
) -> dict[str, Any]:
    """Record a final-F15 locator already governed by an existing route."""

    return {
        "source_unit_id": source_unit_id,
        "discovery_kind": "SEARCH_HIT",
        "discovery_id": f15_hit_id(source_unit_id),
        "discovery_family_ordinal": 15,
        "literal_target": literal_target,
        "route_kind": route_kind,
        "expected_topic": expected_topic,
        "existing_route_id": route_id,
        "rationale": (
            f"Final family-15 search rediscovered literal target "
            f"{literal_target!r}, already governed by {route_id}; no "
            "duplicate route is authored."
        ),
    }


# All Stage-9-owned routes from the earlier sequential review remain retained.
# R000225 is not itself a final-F15 use because U001216 did not match F15.
STAGE_EXISTING_ROUTE_IDS = tuple(
    f"R{number:06d}" for number in range(203, 249)
)

EXISTING_ROUTE_USES = (
    existing_route_use(
        "R000203", "U000965", "page 173",
        "two-dimensional CA rule-code numbering",
    ),
    existing_route_use(
        "R000204", "U000968", "page 173",
        "two-dimensional CA rule-code numbering",
    ),
    existing_route_use(
        "R000205", "U000974", "page 60",
        "earlier cellular-automaton code convention",
    ),
    existing_route_use(
        "R000206", "U000981", "page 178",
        "approximate-circle two-dimensional cellular automaton",
    ),
    existing_route_use(
        "R000207", "U000982", "pages 179–181",
        "eight-neighbor exactly-three retaining cellular automaton",
    ),
    existing_route_use(
        "R000208", "U000983", "top of page 179",
        "seed-length sweep for exactly-three retaining CA",
    ),
    existing_route_use(
        "R000209", "U000984", "page 181",
        "row-of-eleven evolution for exactly-three retaining CA",
    ),
    existing_route_use(
        "R000210", "U000995", "pages 182 and 183",
        "three-dimensional cellular-automaton examples",
    ),
    existing_route_use(
        "R000211", "U001005", "page 171",
        "two-dimensional nested cellular-automaton analog",
    ),
    existing_route_use(
        "R000212", "U001016", "page 186",
        "complex four-state two-dimensional Turing-machine rule",
    ),
    existing_route_use(
        "R000213", "U001033", "page 82",
        "one-dimensional substitution-system mechanics",
    ),
    existing_route_use(
        "R000214", "U001038", "page 83",
        "one-dimensional substitution-system nested patterns",
    ),
    existing_route_use(
        "R000215", "U001052", "page 85",
        "neighbor interaction in one-dimensional substitution systems",
    ),
    existing_route_use(
        "R000216", "U001057", "Chapter 3",
        "parallel and sequential one-dimensional substitution schedules",
        route_kind="SECTION",
    ),
    existing_route_use(
        "R000217", "U001062", "Chapter 9",
        "order-independent higher-dimensional sequential substitution",
        route_kind="SECTION",
    ),
    existing_route_use(
        "R000218", "U001113", "Chapter 9",
        "network-system variants for space and spacetime",
        route_kind="SECTION",
    ),
    existing_route_use(
        "R000219", "U001129", "page 88",
        "sequential substitution replacement rules",
    ),
    existing_route_use(
        "R000220", "U001147", "page 205",
        "rapid-growth multiway rule",
    ),
    existing_route_use(
        "R000221", "U001150", "page 205",
        "multiway rules (d) and (f)",
    ),
    existing_route_use(
        "R000222", "U001150", "previous page",
        "multiway rule (k)",
    ),
    existing_route_use(
        "R000223", "U001206", "pages 214 and 215",
        "ordering of local-template constraints",
    ),
    existing_route_use(
        "R000224", "U001212", "page 216",
        "required-template constraint family",
    ),
    existing_route_use(
        "R000226", "U001217", "rule 30 cellular automaton",
        (
            "constraint correspondence with a shifted elementary cellular-"
            "automaton rule-30 pattern"
        ),
        route_kind="OTHER",
    ),
    existing_route_use(
        "R000227", "U006078", "page 929",
        "other lattice constructions",
    ),
    existing_route_use(
        "R000228", "U006112", "page 171",
        "cellular automaton code 942 underlying the displayed slices",
    ),
    existing_route_use(
        "R000229", "U006121", "page 1092",
        "additive cellular-automaton rules",
    ),
    existing_route_use(
        "R000230", "U006121", "page 980",
        "cellular automaton code 175850",
    ),
    existing_route_use(
        "R000231", "U006121", "page 177",
        "main-text cellular automaton code 175850 construction",
    ),
    existing_route_use(
        "R000232", "U006121", "page 178",
        "main-text cellular automaton code 746 construction",
    ),
    existing_route_use(
        "R000233", "U006121", "page 181",
        "main-text cellular automaton code 174826 construction",
    ),
    existing_route_use(
        "R000234", "U006123", "page 183",
        "underlying rules for 3D projection panels (a) and (b)",
    ),
    existing_route_use(
        "R000235", "U006139", "page 185",
        "rules for 2D Turing-machine head paths (a) through (e)",
    ),
    existing_route_use(
        "R000236", "U006168", "page 583",
        "non-white-background substitution systems and their nested structure",
    ),
    existing_route_use(
        "R000237", "U006192", "pages 407 and 1006",
        "parameter-space sets for geometric substitution systems",
    ),
    existing_route_use(
        "R000238", "U006208", "page 1127",
        "sigma-function scan of an infinite grid quadrant",
    ),
    existing_route_use(
        "R000239", "U006226", "Chapter 9",
        "undirected-network update rules",
        route_kind="SECTION",
    ),
    existing_route_use(
        "R000240", "U006273", "page 508",
        "network substitution systems",
    ),
    existing_route_use(
        "R000241", "U006273", "page 1141",
        "multiway tag systems",
    ),
    existing_route_use(
        "R000242", "U006276", "page 504",
        "multiway systems in fundamental physics",
    ),
    existing_route_use(
        "R000243", "U006310", "page 932",
        "exact Penrose tile subdivision",
    ),
    existing_route_use(
        "R000244", "U006318", "page 981",
        "exact Ising-model energy law",
    ),
    existing_route_use(
        "R000245", "U006318", "page 757",
        "correspondence systems",
    ),
    existing_route_use(
        "R000246", "U006336", "page 1073",
        "Hadamard matrix property",
    ),
    existing_route_use(
        "R000247", "U006336", "page 887",
        "finite group/semigroup multiplication-table constraints",
    ),
    existing_route_use(
        "R000248", "U006338", "page 1129",
        "formula constraints and expression complexity",
    ),
)


def non_bearing_locator(
    source_unit_id: str,
    literal_target: str,
    rationale: str,
) -> dict[str, Any]:
    """Record a final-F15 locator that does not warrant a route."""

    return {
        "source_unit_id": source_unit_id,
        "discovery_kind": "SEARCH_HIT",
        "discovery_id": f15_hit_id(source_unit_id),
        "discovery_family_ordinal": 15,
        "literal_target": literal_target,
        "disposition": "NON_BEARING",
        "rationale": rationale,
    }


NON_BEARING_LOCATORS = (
    non_bearing_locator(
        "U006114", "pages 876–878",
        "The locator supports only a history-of-study statement.",
    ),
    non_bearing_locator(
        "U006114", "page 170",
        "The locator is part of the historical von Neumann attribution.",
    ),
    non_bearing_locator(
        "U006114", "page 177",
        "The locator is part of the historical Moore attribution.",
    ),
    non_bearing_locator(
        "U006114", "page 369",
        "The locator is part of the historical Golay attribution.",
    ),
    non_bearing_locator(
        "U006114", "page 1077",
        "The image-processing reference supplies history, not rule mechanics.",
    ),
    non_bearing_locator(
        "U006114", "page 877",
        "The Ulam-collaborator reference supplies provenance only.",
    ),
    non_bearing_locator(
        "U006121", "Page 174 · Cellular automaton art",
        (
            "The labelled passage concerns an application and display "
            "choices, not an independently delimited native construction."
        ),
    ),
    non_bearing_locator(
        "U006121", "Compare page 872",
        "The rug-and-design comparison is application context only.",
    ),
    non_bearing_locator(
        "U006197", "page 43",
        "The locator occurs only in the history of fractal art.",
    ),
    non_bearing_locator(
        "U006197", "page 918",
        "The locator occurs only in the history of fractal functions.",
    ),
    non_bearing_locator(
        "U006197", "page 191",
        "The locator occurs only in the historical Koch attribution.",
    ),
    non_bearing_locator(
        "U006197", "page 187",
        "The locator occurs only in the historical Sierpiński attribution.",
    ),
    non_bearing_locator(
        "U006197", "page 188",
        "The locator occurs only in the historical Menger attribution.",
    ),
    non_bearing_locator(
        "U006197", "page 190",
        "The locator occurs only in the historical Lévy attribution.",
    ),
    non_bearing_locator(
        "U006227", "Page 199 · Computer science",
        (
            "The labelled passage is an analogy to practical data structures "
            "and garbage collection, not new network-rule mechanics."
        ),
    ),
    non_bearing_locator(
        "U006261", "page 1150",
        (
            "The mathematical-proof comparison belongs to historical and "
            "terminological context for multiway systems."
        ),
    ),
    non_bearing_locator(
        "U006282", "See pages 342 and 1185",
        (
            "The molecular examples are applications of variational "
            "principles and do not supply a new constraint construction."
        ),
    ),
)


ROUTE_SPECS = tuple(
    {
        **spec,
        "route_id": f"R{route_number:06d}",
    }
    for route_number, spec in enumerate(_ROUTES, start=249)
)

LOCATOR_DISPOSITIONS = (
    tuple(
        {
            "disposition": "NEW_ROUTE",
            "source_unit_id": spec["source_unit_id"],
            "discovery_id": spec["discovery_id"],
            "literal_target": spec["literal_target"],
            "route_id": spec["route_id"],
        }
        for spec in ROUTE_SPECS
    )
    + tuple(
        {
            "disposition": "EXISTING_ROUTE",
            "source_unit_id": use["source_unit_id"],
            "discovery_id": use["discovery_id"],
            "literal_target": use["literal_target"],
            "route_id": use["existing_route_id"],
        }
        for use in EXISTING_ROUTE_USES
    )
    + tuple(
        {
            "disposition": "NON_BEARING",
            "source_unit_id": item["source_unit_id"],
            "discovery_id": item["discovery_id"],
            "literal_target": item["literal_target"],
            "route_id": "",
        }
        for item in NON_BEARING_LOCATORS
    )
)

EXPECTED_COUNTS = {
    "f15_hit_units": 144,
    "new_routes": 151,
    "new_route_source_units": 117,
    "within_stage_routes": 86,
    "cross_range_routes": 65,
    "stage_existing_routes": 46,
    "f15_existing_route_uses": 45,
    "f15_existing_route_source_units": 37,
    "non_bearing_locators": 17,
    "non_bearing_source_units": 6,
    "locator_dispositions": 213,
}


def canonical_spec_payload() -> dict[str, Any]:
    """Return the complete frozen data projection covered by the digest."""

    return {
        "route_specs": list(ROUTE_SPECS),
        "stage_existing_route_ids": list(STAGE_EXISTING_ROUTE_IDS),
        "existing_route_uses": list(EXISTING_ROUTE_USES),
        "non_bearing_locators": list(NON_BEARING_LOCATORS),
        "f15_hit_units": list(F15_HIT_UNITS),
        "locator_dispositions": list(LOCATOR_DISPOSITIONS),
        "expected_counts": EXPECTED_COUNTS,
    }


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def route_spec_digest() -> str:
    """Return the canonical digest of only the 151 authored route rows."""

    return hashlib.sha256(_canonical_json_bytes(list(ROUTE_SPECS))).hexdigest()


def canonical_spec_digest() -> str:
    """Return the canonical digest of routes plus every audit inventory."""

    return hashlib.sha256(
        _canonical_json_bytes(canonical_spec_payload())
    ).hexdigest()


ROUTE_SPEC_DIGEST = route_spec_digest()
CANONICAL_SPEC_DIGEST = canonical_spec_digest()
EXPECTED_CANONICAL_SPEC_DIGEST = (
    "5e575deef81eb316173de75edad0a2d1857e14b7327984f290a3a954c1bae27f"
)


def assert_frozen_spec() -> str:
    """Fail closed if route order, scope, coverage, or frozen data drifts."""

    if len(F15_HIT_UNITS) != EXPECTED_COUNTS["f15_hit_units"]:
        raise AssertionError("final-F15 hit-unit count drifted")
    if len(set(F15_HIT_UNITS)) != len(F15_HIT_UNITS):
        raise AssertionError("final-F15 hit-unit order contains duplicates")
    if f15_hit_id(F15_HIT_UNITS[0]) != "H011603":
        raise AssertionError("first final-F15 hit ID drifted")
    if f15_hit_id(F15_HIT_UNITS[-1]) != "H011746":
        raise AssertionError("last final-F15 hit ID drifted")

    if len(ROUTE_SPECS) != EXPECTED_COUNTS["new_routes"]:
        raise AssertionError("new route count drifted")
    expected_route_ids = tuple(
        f"R{number:06d}" for number in range(249, 400)
    )
    route_ids = tuple(spec["route_id"] for spec in ROUTE_SPECS)
    if route_ids != expected_route_ids:
        raise AssertionError("new route-ID allocation drifted")

    route_source_units = {
        spec["source_unit_id"] for spec in ROUTE_SPECS
    }
    if (
        len(route_source_units)
        != EXPECTED_COUNTS["new_route_source_units"]
    ):
        raise AssertionError("new-route source-unit count drifted")

    scope_counts = {
        scope: sum(
            spec["closure_scope"] == scope for spec in ROUTE_SPECS
        )
        for scope in (WITHIN, CROSS)
    }
    if scope_counts != {
        WITHIN: EXPECTED_COUNTS["within_stage_routes"],
        CROSS: EXPECTED_COUNTS["cross_range_routes"],
    }:
        raise AssertionError(f"route scope partition drifted: {scope_counts}")

    route_discovery_keys: list[tuple[int, int]] = []
    route_identities: set[tuple[str, str, str]] = set()
    for spec in ROUTE_SPECS:
        source_unit_id = spec["source_unit_id"]
        if source_unit_id not in F15_HIT_UNITS:
            raise AssertionError(
                f"route source is outside final F15: {source_unit_id}"
            )
        expected_hit = f15_hit_id(source_unit_id)
        if (
            spec["discovery_kind"] != "SEARCH_HIT"
            or spec["discovery_id"] != expected_hit
            or spec["discovery_family_ordinal"] != 15
        ):
            raise AssertionError(
                f"route discovery anchor drifted: {spec['route_id']}"
            )
        discovery_key = (
            int(spec["discovery_id"][1:]),
            spec["discovery_ordinal"],
        )
        route_discovery_keys.append(discovery_key)
        identity = (
            source_unit_id,
            spec["literal_target"],
            spec["expected_topic"],
        )
        if identity in route_identities:
            raise AssertionError(f"duplicate route identity: {identity!r}")
        route_identities.add(identity)
        if not spec["attempts"] or not all(spec["attempts"]):
            raise AssertionError(
                f"route has no auditable attempt: {spec['route_id']}"
            )
        if not spec["literal_target"] or not spec["expected_topic"]:
            raise AssertionError(
                f"route has an empty governed claim: {spec['route_id']}"
            )
        if spec["route_kind"] not in {"PAGE", "SECTION", "OTHER"}:
            raise AssertionError(
                f"route kind drifted: {spec['route_id']}"
            )
        if spec["closure_scope"] == WITHIN:
            if spec["status"] != "RESOLVED":
                raise AssertionError(
                    f"within-stage route is not resolved: {spec['route_id']}"
                )
            if not spec["target_unit_ids"] and not spec["target_asset_ids"]:
                raise AssertionError(
                    f"resolved route has no target: {spec['route_id']}"
                )
        elif spec["status"] != "PENDING":
            raise AssertionError(
                f"cross-range route is not pending: {spec['route_id']}"
            )
        if len(spec["candidate_ids"]) != len(set(spec["candidate_ids"])):
            raise AssertionError(
                f"route repeats a candidate ID: {spec['route_id']}"
            )
        if any(
            len(candidate_id) != 5
            or not candidate_id.startswith("B")
            or not candidate_id[1:].isdigit()
            for candidate_id in spec["candidate_ids"]
        ):
            raise AssertionError(
                f"route has an invalid candidate ID: {spec['route_id']}"
            )
        if len(spec["recovered_candidate_names"]) != len(
            set(spec["recovered_candidate_names"])
        ):
            raise AssertionError(
                f"route repeats a recovered candidate: {spec['route_id']}"
            )

    if route_discovery_keys != sorted(route_discovery_keys):
        raise AssertionError("new routes are not in final-F15 locator order")
    grouped_ordinals: dict[str, list[int]] = {}
    for spec in ROUTE_SPECS:
        grouped_ordinals.setdefault(spec["discovery_id"], []).append(
            spec["discovery_ordinal"]
        )
    for hit_id, ordinals in grouped_ordinals.items():
        if ordinals != list(range(1, len(ordinals) + 1)):
            raise AssertionError(
                f"non-contiguous locator ordinals for {hit_id}: {ordinals}"
            )

    if (
        len(STAGE_EXISTING_ROUTE_IDS)
        != EXPECTED_COUNTS["stage_existing_routes"]
    ):
        raise AssertionError("Stage-9 existing route count drifted")
    expected_existing_uses = (
        set(STAGE_EXISTING_ROUTE_IDS) - {"R000225"}
    )
    actual_existing_uses = {
        use["existing_route_id"] for use in EXISTING_ROUTE_USES
    }
    if actual_existing_uses != expected_existing_uses:
        raise AssertionError("final-F15 existing-route inventory drifted")
    if (
        len(EXISTING_ROUTE_USES)
        != EXPECTED_COUNTS["f15_existing_route_uses"]
    ):
        raise AssertionError("final-F15 existing-route use count drifted")
    if (
        len({use["source_unit_id"] for use in EXISTING_ROUTE_USES})
        != EXPECTED_COUNTS["f15_existing_route_source_units"]
    ):
        raise AssertionError(
            "final-F15 existing-route source-unit count drifted"
        )

    if (
        len(NON_BEARING_LOCATORS)
        != EXPECTED_COUNTS["non_bearing_locators"]
    ):
        raise AssertionError("non-bearing locator count drifted")
    if (
        len({item["source_unit_id"] for item in NON_BEARING_LOCATORS})
        != EXPECTED_COUNTS["non_bearing_source_units"]
    ):
        raise AssertionError("non-bearing source-unit count drifted")

    for item in (*EXISTING_ROUTE_USES, *NON_BEARING_LOCATORS):
        if item["discovery_id"] != f15_hit_id(item["source_unit_id"]):
            raise AssertionError(
                "inventory discovery anchor drifted: "
                f"{item['source_unit_id']} {item['literal_target']!r}"
            )

    disposition_keys = [
        (
            item["disposition"],
            item["source_unit_id"],
            item["literal_target"],
            item["route_id"],
        )
        for item in LOCATOR_DISPOSITIONS
    ]
    if len(disposition_keys) != len(set(disposition_keys)):
        raise AssertionError("locator disposition inventory has duplicates")
    if (
        len(LOCATOR_DISPOSITIONS)
        != EXPECTED_COUNTS["locator_dispositions"]
    ):
        raise AssertionError("locator disposition count drifted")
    covered_units = {
        item["source_unit_id"] for item in LOCATOR_DISPOSITIONS
    }
    if covered_units != set(F15_HIT_UNITS):
        missing = sorted(set(F15_HIT_UNITS) - covered_units)
        extra = sorted(covered_units - set(F15_HIT_UNITS))
        raise AssertionError(
            f"final-F15 disposition coverage drifted; "
            f"missing={missing}, extra={extra}"
        )

    digest = canonical_spec_digest()
    if digest != EXPECTED_CANONICAL_SPEC_DIGEST:
        raise AssertionError(
            "canonical route-audit digest drifted: "
            f"{digest} != {EXPECTED_CANONICAL_SPEC_DIGEST}"
        )
    return digest
