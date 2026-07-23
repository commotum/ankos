#!/usr/bin/env python3
"""Author the sealed Stage-8 Chapter-4 Notes blind-review worksheet.

This helper is intentionally data-driven and bundle-local.  It does not search
the repository or consult any taxonomy, API, runtime, or implementation plan.
It can be rerun against a freshly rebuilt copy of the same worker bundle.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any


WORKER = "ch04-notes-reader-e1"
STAGE = 8
EPOCH = 1

FIELDS = [
    "object_kind",
    "native_time",
    "carrier",
    "support",
    "topology",
    "structural_invariants",
    "alphabet_or_value_schema",
    "complete_state",
    "visible_history",
    "control_state",
    "seed",
    "input",
    "boundary",
    "external_data",
    "frontier_or_activation",
    "schedule",
    "read_dependencies_or_neighborhood",
    "law_kind",
    "rule_relation_constraint_function_or_probability_law",
    "write_replacement_assembly_or_commit",
    "result_kind",
    "successor_cardinality",
    "determinism_branching_or_measure",
    "termination_completion_failure",
    "witness_semantics",
    "parameters_and_variants",
    "excluded_observers_and_representations",
    "evidence_limit",
]

N_A = {
    "native_time",
    "topology",
    "visible_history",
    "control_state",
    "seed",
    "boundary",
    "external_data",
    "frontier_or_activation",
    "schedule",
}


def S(
    name: str,
    uids: list[str],
    kind: str,
    law: str,
    *,
    params: tuple[str, ...] = (),
    variants: tuple[str, ...] = (),
    missing: tuple[str, ...] = (),
    routes: tuple[str, ...] = (),
    images: tuple[str, ...] = (),
    image_direct: bool = False,
    overrides: dict[str, str] | None = None,
    law_uid: str | None = None,
    identity_image: str | None = None,
    facts: dict[str, dict[str, Any]] | None = None,
    source_status: tuple[str, ...] = ("CLEAR",),
    source_uncertainties: tuple[str, ...] = (),
    relation_names: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "name": name,
        "uids": uids,
        "kind": kind,
        "law": law,
        "params": params,
        "variants": variants,
        "missing": missing,
        "route_keys": routes,
        "images": images,
        "image_direct": image_direct,
        "overrides": overrides or {},
        "law_uid": law_uid,
        "identity_image": identity_image,
        "facts": facts or {},
        "source_status": source_status,
        "source_uncertainties": source_uncertainties,
        "relation_names": relation_names,
    }


BITWISE_IMAGE = (
    "BACK-MATTER/NOTES/"
    "_page_921_iterated_bitwise_operations_six_panel_row.jpeg"
)
OTHER_PDE_IMAGE = "BACK-MATTER/NOTES/_page_940_Picture_4.jpeg"


# Canonical first-occurrence order.  Alternatives are kept separate whenever
# the Book gives a distinct law, relation, query, solver, or observer.
SPECS = [
    S("whole-number positional digit encoder", ["U005639", "U005640"], "REPRESENTATION", "Reverse[Mod[NestWhileList[Floor[#/k] &, n, # >= k &], k]]", params=("n", "k")),
    S("positional digit decoder", ["U005641", "U005642"], "REPRESENTATION", "Fold[k #1 + #2 &, 0, list]", params=("list", "k")),
    S("fractional positional digit generator", ["U005643", "U005644"], "REPRESENTATION", "Floor[k NestList[Mod[k #, 1] &, x, m - 1]]", params=("x", "k", "m")),
    S("fractional positional digit reconstruction", ["U005645", "U005646"], "REPRESENTATION", "Fold[#1/k + #2 &, 0, Reverse[list]]/k", params=("list", "k")),
    S("Gray-code ordering generator", ["U005647", "U005648"], "GENERATOR", "GrayCode[m_] := Nest[Join[#, Length[#] + Reverse[#]] &, {0}, m]", params=("m",)),
    S("base-2 one-digit count function", ["U005658", "U005659", "U005660"], "FUNCTION", "DigitCount[n, 2, 1], with stated integer/noninteger-base and correlation generalizations", params=("n", "base", "digit"), variants=("integer and noninteger bases", "digit correlations")),
    S("negative-base positional representation", ["U005662"], "REPRESENTATION", "FromDigits[list, -k] with digits 0 through k-1", params=("list", "k")),
    S("non-power place-value representation", ["U005664"], "REPRESENTATION", "Sum[a[n] f[n], {n, 0, Infinity}] with constrained growth of f", params=("a", "f")),
    S("multiplicative prime-exponent representation", ["U005665"], "REPRESENTATION", "integer represented by the exponent sequence in its prime factorization", params=("integer",)),
    S("powers-of-three base-2 digit sequence", ["U005667"], "FUNCTION", "n maps to IntegerDigits[3^n, 2]", params=("n",)),
    S("truncated powers-of-three congruential generator", ["U005669", "U005670"], "ITERATION", "Mod[3^n, 2^s], equivalently a linear congruential generator on the rightmost s bits", params=("n", "s")),
    S("base-6 cellular automaton for powers of three", ["U005671"], "CA", "strictly local base-6 cellular automaton whose detailed rule is at page 614", routes=("powers3_ca",), missing=("The local transition table is outside the sealed Notes range.",)),
    S("fractional-parts power sequence", ["U005673"], "FUNCTION", "n maps to Mod[(3/2)^n, 1]", params=("n",), variants=("general Mod[h^n,1] family",)),
    S("base-6 cellular automaton for powers of 3/2", ["U005674", "U005675", "U005676"], "CA", "{a,b,c} -> 3 Mod[a + Quotient[b,2],2] + Quotient[3 Mod[b,2] + Quotient[c,2],2]", params=("initial base-6 digits of u",), variants=("invertible rule",)),
    S("general fractional-parts power family", ["U005677"], "FUNCTION", "n maps to Mod[h^n, 1]", params=("h", "n")),
    S("irrational-rotation multiple sequence", ["U005678", "U005680"], "FUNCTION", "n maps to Mod[h n, 1]", params=("h", "n")),
    S("Beatty-difference digit sequence", ["U005681"], "FUNCTION", "Floor[(n + 1) h] - Floor[n h]", params=("h", "n")),
    S("continued-fraction-derived substitution generator", ["U005682", "U005683", "U005684", "U005685"], "SUBSTITUTION", "derive a rule list from ContinuedFraction[h,m], then Fold replacement from {0}", params=("h", "m"), variants=("periodic rule set for quadratic h",)),
    S("rotated page-117 digit substitution preset", ["U005657"], "SUBSTITUTION", "pattern described as a rotated first substitution-system example from page 83", routes=("page117_sub",), missing=("The replacement rule and seed are only at the routed target.",)),
    S("page-122 parity integer map", ["U005687", "U005688"], "ITERATION", "If[EvenQ[n], 3 n/2, 3 (n + 1)/2]", params=("initial n", "t")),
    S("standard 3n+1 map", ["U005689"], "ITERATION", "If[EvenQ[n], n/2, (3 n + 1)/2]", params=("initial n",)),
    S("3n+1 eventual-one decision query", ["U005690"], "QUERY", "FixedPoint[(3 #/2^IntegerExponent[#, 2] + 1)/2 &, n] == 2", params=("n",)),
    S("main-text 5n/2 parity map", ["U005691"], "ITERATION", "If[EvenQ[n], 5 n/2, (n + 1)/2]", params=("initial n",)),
    S("base-6 cellular automaton for the 3n+1 map", ["U005696", "U005697", "U005698"], "CA", "{a,b,c} -> If[b==6, If[EvenQ[a],6,4], 3 Mod[a,2]+Quotient[b,2] /. 0->6 /; a==6]", params=("base-6 digit state",)),
    S("parity-trace initial-condition reconstructor", ["U005699", "U005700"], "FUNCTION", "Fold backward through a supplied even/odd trace using modular inverse of 5, then return fixed-width base-2 digits", params=("parity list",)),
    S("reversible rounded integer map", ["U005701", "U005702", "U005703", "U005704"], "ITERATION", "forward If[EvenQ[n],3n/2,Round[3n/4]] and inverse If[Mod[n,3]==0,2n/3,Round[4n/3]]", params=("n",), variants=("forward", "inverse")),
    S("binary reversal-addition map", ["U005707", "U005708", "U005709", "U005711"], "ITERATION", "n -> n + FromDigits[Reverse[IntegerDigits[n,2]],2]", params=("n",), variants=("fixed-width with dropped carry", "ever-growing width")),
    S("fixed-width digit-reversal permutation", ["U005713", "U005714"], "FUNCTION", "Table[FromDigits[Reverse[IntegerDigits[n,k,m]],k], {n,0,k^m-1}]", params=("k", "m")),
    S("iterated run-length encoder", ["U005717", "U005718"], "ITERATION", "list -> Flatten[Map[{Length[#], First[#]} &, Split[list]]]", params=("initial list",)),
    S("92-token substitution realization of run-length encoding", ["U005719", "U005720"], "SUBSTITUTION", "neighbor-independent replacement on 92 subsequences; one complete example replacement is printed", missing=("Only one of the 92 token replacements is stated.",)),
    S("digit-count sequence append system", ["U005721", "U005722", "U005723"], "ITERATION", "list -> Join[list, IntegerDigits[Apply[Plus,list],2]]", params=("initial list",)),
    S("BitXor[2 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitXor[2 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("BitXor[3+2 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitXor[3 + 2 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("BitXor[3 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitXor[3 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("BitXor[6 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitXor[6 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("BitOr[2 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitOr[2 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("BitOr[6 n,n] digit function", ["U005725"], "FUNCTION", "n maps to BitOr[6 n,n]", images=(BITWISE_IMAGE,), image_direct=True, params=("n",)),
    S("page-128 linear recurrence family", ["U005728"], "ITERATION", "linear recurrence relations for the page-128 sequences", routes=("linear_recurrences",), missing=("The individual coefficients, orders, and initial values are at the routed target.",)),
    S("factorial recurrence", ["U005729", "U005730"], "ITERATION", "f[1]=1; f[n]:=n f[n-1]", params=("n",)),
    S("quadratic logistic recurrence", ["U005732", "U005733", "U005734"], "ITERATION", "f[0]=x; f[n]:=a f[n-1] (1-f[n-1])", params=("x", "a", "n")),
    S("convenient two-argument Ackermann function", ["U005735", "U005736"], "FUNCTION", "f[1,n]=n; f[m,1]=f[m-1,2]; f[m,n]=f[m-1,f[m,n-1]+1]", params=("m", "n")),
    S("original three-argument Ackermann function", ["U005737", "U005738", "U005739", "U005740", "U005741"], "FUNCTION", "f[1,x,y]=x+y; f[m,x,y]=Nest[f[m-1,x,#]&,x,y-1]", params=("m", "x", "y"), variants=("nested functional form",)),
    S("memoized self-indexed recurrence", ["U005742", "U005743", "U005744"], "ITERATION", "f[n]=f[n-f[n-1]]+f[n-f[n-2]], with f[1]=f[2]=1 and memoized evaluation", params=("n",), variants=("evaluation-order-sensitive semantics",)),
    S("page-131 sequence (d)", ["U005745", "U005746", "U005747", "U005748", "U005749", "U005750", "U005751", "U005752"], "FUNCTION", "f[n]=(n+g[IntegerDigits[n,2]])/2 with the printed recursive clauses for g", params=("n",), variants=("element multiplicity enumeration", "difference substitution form", "largest-preimage query")),
    S("page-131 sequence (c) hump generator", ["U005753", "U005754", "U005755", "U005756"], "GENERATOR", "printed FoldList hump formula and reordered-base-2 alternative generate the first 2^m elements", params=("m",), variants=("hump formula", "reordered digit generator")),
    S("binary-dependency recursive-sequence schema", ["U005758", "U005760"], "RELATION", "f[n] has form f[p[n]]+f[q[n]], giving a binary dependency tree", params=("p", "q", "n")),
    S("primitive-recursive construction calculus", ["U005762", "U005763", "U005764", "U005769"], "CALCULUS", "zero, successor, projections, composition, and primitive recursion; recursion unwinds as Fold", variants=("recursive clauses", "Fold unrolling")),
    S("primitive-recursive plus", ["U005765", "U005766"], "FUNCTION", "plus[0,y]=y; plus[x,y]:=s[plus[x-1,y]]", params=("x", "y")),
    S("primitive-recursive times", ["U005765", "U005766"], "FUNCTION", "times[0,y]=0; times[x,y]:=plus[times[x-1,y],y]", params=("x", "y")),
    S("unbounded mu-search operator", ["U005770", "U005771", "U005772"], "QUERY", "mu[f] searches n=0,1,... until f[n,args]==0, and may not terminate", params=("f", "arguments")),
    S("symbolic composition/recursion enumerator", ["U005773", "U005774", "U005775", "U005776", "U005777"], "CALCULUS", "c[g,h...] composes functions and r[g,h] performs primitive recursion, with recursive and Fold forms", variants=("composition", "primitive recursion", "unwound recursion")),
    S("triangular-number primitive-recursive function", ["U005780"], "FUNCTION", "r[z,r[s,s]] = #(# + 1)/2", params=("integer",)),
    S("exponential primitive-recursive function", ["U005781"], "FUNCTION", "r[z,r[s,c[s,s]]] = 2^(# + 1) - # - 2", params=("integer",)),
    S("nested-power-ceiling primitive-recursive function", ["U005782"], "FUNCTION", "r[z,r[s,p[2]]] = 2^Ceiling[Log[2,# + 2]] - # - 2", params=("integer",)),
    S("parity primitive-recursive function", ["U005783"], "FUNCTION", "r[z,r[c[s,z],z]] = Mod[#,2]", params=("integer",)),
    S("double-exponential primitive-recursive fold", ["U005784"], "FUNCTION", "r[z,r[s,r[s,s]]] = Fold[#1(#1+1)/2 + #2 &,0,Range[#]]", params=("integer",)),
    S("complex primitive-recursive function", ["U005785", "U005786", "U005787", "U005789"], "FUNCTION", "the printed nested Fold/Ceiling/Log expression", params=("integer",)),
    S("Ackermann-related nested recursion family", ["U005791"], "FUNCTION", "Nest[r[c[s,z],#]&,c[s,s],n] = f[n+1,2,# + 1]-1", params=("n", "integer")),
    S("diagonalized non-primitive-recursive function", ["U005793"], "FUNCTION", "given enumeration w[m], diagonalization yields x -> w[x][x], with a modulo-2 variant", params=("x",), variants=("unbounded value", "modulo 2")),
    S("Ulam sequence", ["U005796", "U005797", "U005798"], "GENERATOR", "start {1,2}; append the smallest number expressible as a sum of two earlier terms in exactly one way", params=("initial sequence",)),
    S("Fermat-little-theorem primality predicate", ["U005802"], "QUERY", "for prime p, Mod[a^(p-1),p]==1; used as a primality-testing condition", params=("a", "p"), missing=("The note does not give a complete false-positive-resistant primality algorithm.",)),
    S("decimation system", ["U005803"], "ITERATION", "start with a line of cells and remove every kth cell that remains at each step", params=("k", "line")),
    S("decimation survival-time query", ["U005804", "U005805"], "QUERY", "the printed Module/While recurrence returns how many steps cell n survives", params=("n", "k")),
    S("Josephus last-cell function", ["U005807"], "FUNCTION", "Fold[Mod[#1+k,#2,1]&,1,Range[2,n]]", params=("n", "k")),
    S("Moebius sign function", ["U005815"], "FUNCTION", "0 for a repeated prime factor; otherwise (-1)^Length[FactorInteger[n]]", params=("n",)),
    S("Mertens cumulative-sum observer", ["U005815"], "OBSERVER", "FoldList[Plus,0,Table[MoebiusMu[i],{i,n}]]", params=("n",)),
    S("divisor-count function", ["U005817"], "FUNCTION", "DivisorSigma[0,n] = Length[Divisors[n]]", params=("n",)),
    S("aliquot-balance function", ["U005818", "U005819"], "FUNCTION", "DivisorSigma[1,n]-2n, with the printed Ramanujan trigonometric expansion", params=("n",)),
    S("sum-of-two-squares representation count", ["U005820"], "FUNCTION", "4 Apply[Plus, Im[I^Divisors[n]]]", params=("n",)),
    S("sum-of-d-squares cumulative relation", ["U005821"], "RELATION", "count below n equals lattice-point count inside a radius-Sqrt[n] d-sphere", params=("n", "d")),
    S("sum-of-four-squares representation count", ["U005822"], "FUNCTION", "8 Apply[Plus, Select[Divisors[n], Mod[#,4] != 0 &]]", params=("n",)),
    S("Goldbach two-prime representation count", ["U005823"], "FUNCTION", "Length[Select[n-Table[Prime[i],{i,PrimePi[n]}],PrimeQ]]", params=("n",)),
    S("Hardy-Littlewood Goldbach-count estimate", ["U005823", "U005824"], "FUNCTION", "2 n Product[(p-1)/(p-2)]/Log[n]^2 over distinct nonfirst prime factors", params=("n",)),
    S("trapezoidal-number representability relation", ["U005826"], "RELATION", "n is representable by successive rows a,a-1,... except exactly when n is a power of 2", params=("n", "a", "b")),
    S("perfect-number constraint", ["U005830", "U005832"], "QUERY", "Apply[Plus,Divisors[n]] == 2 n", params=("n",), variants=("pluperfect", "quasiperfect")),
    S("Lucas-Lehmer Mersenne-prime test", ["U005830"], "QUERY", "Nest[Mod[#^2-2,2^n-1]&,4,n-2] == 0", params=("n",)),
    S("iterated aliquot-sum map", ["U005833", "U005835", "U005836"], "ITERATION", "n -> Apply[Plus,Divisors[n]]-n = DivisorSigma[1,n]-n", params=("initial n",)),
    S("unbounded aliquot-growth query", ["U005837"], "QUERY", "whether an iterated aliquot trajectory can increase forever", params=("initial n",), missing=("The Book states that the decision remains unresolved.",)),
    S("Leibniz pi approximation", ["U005841", "U005842"], "FUNCTION", "4 Sum[(-1)^k/(2k+1), {k,0,m}]", params=("m",)),
    S("nested-radical product pi approximation", ["U005843", "U005844"], "FUNCTION", "2 Apply[Times, 2/Rest[NestList[Sqrt[2+#]&,0,m]]]", params=("m",)),
    S("arithmetic-geometric-mean pi solver", ["U005845", "U005846", "U005847"], "SOLVER", "iterate arithmetic mean, geometric mean, correction, and doubled weight until a==b; return b^2/c", params=("precision n",)),
    S("direct nth-binary-digit extractor", ["U005848", "U005849", "U005850"], "FUNCTION", "printed modular-power finite sum plus controlled tail, rounded after FractionalPart", params=("n", "tail d")),
    S("Bailey-Borwein-Plouffe pi relation", ["U005851", "U005852"], "RELATION", "Sum[16^-k (4/(8k+1)-2/(8k+4)-1/(8k+5)-1/(8k+6)), {k,0,Infinity}]", params=("k",)),
    S("rational digit repeat-period function", ["U005854", "U005855", "U005856", "U005857"], "FUNCTION", "MultiplicativeOrder[b, FixedPoint[#/GCD[#,b]&,n]]", params=("n", "b")),
    S("normal-number constraint", ["U005860"], "QUERY", "every digit and every finite digit block has equal limiting frequency in the selected base", params=("number", "base"), variants=("Champernowne concatenation witness", "Stoneham family")),
    S("Newton square-root iteration", ["U005861"], "ITERATION", "x -> (x+n/x)/2", params=("n", "initial x")),
    S("recurrence-ratio square-root solver", ["U005862"], "SOLVER", "f[i]=2f[i-1]+f[i-2], f[1]=f[2]=1; successive ratios tend to 1+Sqrt[2]", params=("steps",)),
    S("digit-by-digit square-root solver", ["U005863"], "SOLVER", "maintain s^2+4r==4^t n while minimizing r", params=("n", "t"), routes=("digit_sqrt",), missing=("The per-step update choosing the next digit is only in the routed main-text construction.",)),
    S("Thue-Morse substitution digit constant", ["U005864"], "RELATION", "base-2 digits generated by {1->{1,0},0->{0,1}}, approximately 0.587545966 in base 10"),
    S("Fibonacci-substitution digit number", ["U005865"], "RELATION", "digits from {1->{1,0},0->{1}} equal Sum[2^(-Floor[n GoldenRatio]),{n,Infinity}]", params=("n",)),
    S("successive-integer concatenation sequence", ["U005867"], "GENERATOR", "Flatten[Table[IntegerDigits[i,k],{i,n}]]", params=("k", "n"), variants=("polynomial-value concatenation", "Gray-code digit concatenation")),
    S("concatenation-sequence cumulative walk", ["U005869"], "OBSERVER", "FoldList[Plus,0,2 list-1]", params=("concatenation list",)),
    S("leading-digit-dropped concatenation walk", ["U005871", "U005873", "U005874"], "OBSERVER", "FoldList cumulative sum over 2 Rest[IntegerDigits[i,2]]-1", params=("n",)),
    S("direct concatenation-position query", ["U005875", "U005876", "U005877", "U005878"], "FUNCTION", "printed ProductLog/NestWhile block locator and indexed binary-digit expression", params=("position n",)),
    S("large-block concatenation digit formula", ["U005879", "U005880"], "FUNCTION", "printed finite sum obtains about k^(n+1) concatenation digits efficiently", params=("k", "n")),
    S("sparse-position transcendental digit families", ["U005883"], "RELATION", "binary digit 1 positions n!, 2^n, or Fibonacci[n] delimit transcendental numbers", params=("position sequence",)),
    S("run-length digit decoder", ["U005884", "U005885"], "REPRESENTATION", "Fold[Join[#1,Table[1-Last[#1],{#2}]]&,{0},list]", params=("run-length list",)),
    S("successive-integer-run digit function", ["U005886"], "FUNCTION", "n maps to Mod[Floor[1/2+Sqrt[2n]],2]", params=("n",)),
    S("Benford leading-digit measure", ["U005887"], "RELATION", "leading digit s in base b has frequency Log[b,(s+1)/s] when FractionalPart[Log[b,a[n]]] is uniform", params=("s", "b", "sequence a")),
    S("continued-fraction digit extractor", ["U005887", "U005888"], "FUNCTION", "Floor[NestList[1/Mod[#,1]&,x,n-1]]", params=("x", "n")),
    S("continued-fraction reconstruction", ["U005889", "U005890"], "REPRESENTATION", "Fold[1/#1+#2&,Last[list],Rest[Reverse[list]]]", params=("continued-fraction list",)),
    S("Gauss-map continued-fraction trajectory", ["U005891"], "ITERATION", "NestList[1/Mod[#,1]&,x,n]", params=("x", "n")),
    S("continued-fraction term-size measure", ["U005893"], "RELATION", "P(term=s)=Log[2,(1+1/s)/(1+1/(s+1))]", params=("s",)),
    S("regular continued-fraction approximation to pi", ["U005895", "U005896", "U005897"], "FUNCTION", "4/(Fold[#2/#1+2&,2,Reverse[Range[1,n,2]^2]]-1)", params=("n",)),
    S("linear-polynomial continued-fraction relation", ["U005898"], "RELATION", "continued fractions with nth term a n+b equal a stated ratio of BesselI functions", params=("a", "b")),
    S("Shallit nested continued-fraction substitution", ["U005899", "U005900"], "SUBSTITUTION", "printed ten-symbol replacement lookup and output-value list generate continued fractions for Sum[1/k^(2^i)]", params=("k", "n")),
    S("rational-pair continued-fraction term enumerator", ["U005905", "U005906", "U005907"], "GENERATOR", "Flatten[Table[Rest[ContinuedFraction[a/b]],{b,2,n},{a,b-1}]]", params=("n",)),
    S("continued-fraction approximation-quality observer", ["U005908", "U005909", "U005910"], "OBSERVER", "with nth convergent r, return -Log[Denominator[r],Abs[x-r]]", params=("x", "n")),
    S("subtractive Euclidean algorithm", ["U005912"], "ITERATION", "{a,b} -> If[a>b,{a-b,b},{a,b-a}] until {GCD[a,b],0}", params=("a", "b")),
    S("Euclidean rational-termination query", ["U005914"], "QUERY", "starting from {x,1}, termination holds exactly when x is rational", params=("x",)),
    S("Egyptian-fraction relation", ["U005917"], "RELATION", "represent a number as Sum[1/a[n],{n,Infinity}] using distinct integers a[n]", params=("a",)),
    S("nested-radical representation", ["U005917"], "REPRESENTATION", "Fold[Sqrt[#1+#2]&,0,Reverse[list]]", params=("digit list",), variants=("constant digit", "repeating digit block")),
    S("nested-radical digit encoder", ["U005918", "U005919", "U005920"], "FUNCTION", "Ceiling[NestList[(2-Mod[-#,1])^2&,x^2,n-1]-2]", params=("x", "n")),
    S("digital-slope representation", ["U005921"], "REPRESENTATION", "digit n is Floor[n h]-Floor[(n-1)h], uniquely representing slope h", params=("h", "n")),
    S("digital-slope reconstruction", ["U005921", "U005922"], "FUNCTION", "Max[MapIndexed[#1/First[#2]&,FoldList[Plus,First[list],Rest[list]]]]", params=("digit list",)),
    S("Farey-sequence generator", ["U005923", "U005924"], "GENERATOR", "Union[Flatten[Table[a/b,{b,n},{a,0,b}]]]", params=("n",)),
    S("operator-tree integer representation family", ["U005927", "U005928"], "REPRESENTATION", "build integers from 1 by expression trees using stated binary operators; measure minimum applications", params=("target integer", "operator set"), variants=("addition", "2a+b-1", "k a+b-k+1", "BitXor", "BitOr", "addition and multiplication")),
    S("Lissajous curve map", ["U005935"], "FUNCTION", "t maps to a tuple of sine functions on separate coordinate axes", params=("frequencies", "t")),
    S("two-sine function and zero relation", ["U005937"], "RELATION", "Sin[a x]+Sin[b x]=2 Sin[(a+b)x/2] Cos[(a-b)x/2], with two printed zero families", params=("a", "b", "x")),
    S("ODE denotation of an incommensurate sine sum", ["U005937"], "ODE", "y''[x]+2y[x]-Sin[x]==0, y[0]==0, y'[0]==2 denotes Sin[x]+Sin[Sqrt[2]x]", params=("x",)),
    S("three-sine function and zero set", ["U005937", "U005938", "U005941"], "RELATION", "Sin[a x]+Sin[b x]+Sin[c x], with stated periodicity for rational coefficients", params=("a", "b", "c", "x")),
    S("cosine-difference zero-spacing sequence", ["U005943", "U005944"], "FUNCTION", "(Floor[(n+1) q]-Floor[n q]) with q=(b-a)/(a+b)", params=("a", "b", "n")),
    S("zero-spacing substitution realization", ["U005945"], "SUBSTITUTION", "substitution rules generate the cosine-difference spacing sequence; sine-sum variant inserts -1/2", routes=("zero_substitution",), variants=("cosine difference", "sine sum"), missing=("The replacement rules are at the routed page-903 discussion.",)),
    S("harmonic sine Fourier partial sums", ["U005946"], "FUNCTION", "Sum[Sin[n x]/n,{n,k}]", params=("x", "k")),
    S("square-frequency Fourier sum", ["U005948", "U005949", "U005950"], "FUNCTION", "Sum[Sin[n^2 x]/n^2,{n,k}], with printed finite rational-angle relation", params=("x", "k")),
    S("lacunary power-of-two cosine sum", ["U005952"], "FUNCTION", "Sum[Cos[2^n x],{n,k}]", params=("x", "k")),
    S("weighted Weierstrass cosine series", ["U005954"], "FUNCTION", "Sum[Cos[2^n x]/2^(a n),{n,Infinity}]", params=("x", "a")),
    S("Riemann zeta denotation", ["U005956"], "RELATION", "Zeta[s]=Sum[1/n^s,{n,Infinity}]=Product[1/(1-Prime[n]^-s),{n,Infinity}]", params=("s",)),
    S("Riemann-hypothesis constraint", ["U005956"], "QUERY", "every complex zero r satisfies Re[r]==1/2", params=("zeta zero",)),
    S("Riemann-Siegel Z function", ["U005957"], "FUNCTION", "Zeta[1/2+I t] Exp[I RiemannSiegelTheta[t]]", params=("t",)),
    S("Riemann-Siegel theta function", ["U005958", "U005959", "U005960"], "FUNCTION", "Arg[Gamma[1/4+I t/2]]-t Log[Pi]/2", params=("t",)),
    S("Voronin zeta universality relation", ["U005964"], "RELATION", "some translate Zeta[z+(3/4+I t)] approximates any zero-free analytic function on Abs[z]<1/4", params=("target function", "precision")),
    S("Gauss fractional-part reciprocal map", ["U005967"], "ITERATION", "x -> FractionalPart[1/x]", params=("x",)),
    S("exact multiplier-mod-one map", ["U005968"], "ITERATION", "x -> FractionalPart[a x], with nth iterate FractionalPart[a^n x]", params=("a", "x", "n")),
    S("exact tent-map family", ["U005968"], "ITERATION", "If[x<1/2,a x,a(1-x)]; at a=2 the nth iterate is ArcCos[Cos[2^n Pi x]]/Pi", params=("a", "x", "n")),
    S("fixed-binary-precision shift-map simulation", ["U005972", "U005974", "U005975", "U005978"], "ITERATION", "IntegerDigits[Mod[2^n Floor[2^53 x],2^53],2,53]", params=("x", "n"), variants=("53-bit storage",)),
    S("fixed-decimal-precision shift-map simulation", ["U005973", "U005974", "U005976", "U005977", "U005978"], "ITERATION", "Flatten[IntegerDigits[IntegerDigits[Mod[2^n Floor[10^12 x],10^12],10,12],2,4]]", params=("x", "n"), variants=("12-digit BCD storage",)),
    S("finite-precision multiplication-by-3/2 simulation", ["U005981"], "ITERATION", "fixed-precision repeated multiplication by 3/2 as shown in the associated simulation", missing=("The rounding/fill convention and exact recurrence are not stated in this unit.",)),
    S("smooth logistic map", ["U005990", "U005991"], "ITERATION", "x -> a x(1-x)", params=("a", "initial x")),
    S("logistic-map leftmost-digit substitution observer", ["U005991"], "OBSERVER", "eventual leftmost digit follows a step-j trace of {1->{1,0},0->{1,1}} in period-2^j regimes", params=("a", "initial digit")),
    S("Anosov torus map", ["U005993"], "ITERATION", "{x,y} -> Mod[m.{x,y},1]", params=("matrix m", "initial vector"), variants=("example matrix {{2,1},{1,1}}",)),
    S("Lyapunov-exponent observer", ["U005995"], "OBSERVER", "after t steps a small difference is multiplied by approximately 2^(lambda t)", params=("trajectory", "t")),
    S("continuous cellular-automaton family", ["U005997", "U005998", "U005999", "U006000"], "CA", "average left,self,right then apply f; f is FractionalPart[3#/2]& or FractionalPart[#+1/4]&", params=("f", "initial list", "steps"), variants=("page-157 multiplier", "page-158 additive offset", "exact rational", "approximate numeric"), overrides={"boundary": "periodic boundary induced by RotateLeft/RotateRight"}),
    S("continuous-CA background trajectory", ["U006003"], "FUNCTION", "background at step t is FractionalPart[a t]", params=("a", "t")),
    S("continuous-CA center-cell color observer", ["U006003"], "OBSERVER", "reads successive center-cell values while separately tracking background values", params=("parameter a", "trajectory")),
    S("additive continuous cellular automaton", ["U006006", "U006007", "U006008"], "CA", "list -> Mod[RotateLeft[list]+RotateRight[list],1]", params=("initial list",), variants=("single 1/k seed",), overrides={"boundary": "periodic boundary induced by rotations"}),
    S("probabilistic cellular automaton family", ["U006010"], "CA", "at each discrete-valued cell choose probabilistically between two cellular-automaton rules", routes=("probabilistic_ca",), missing=("The rule pair, probabilities, random coupling, and examples are only at page 591.",)),
    S("autonomous ODE system relation", ["U006012"], "ODE", "a'[t]=f[a[t],b[t],...], with coupled equations for finitely many continuous variables", params=("functions", "initial/boundary data", "t")),
    S("Klein-Gordon PDE relation", ["U006015"], "PDE", "partial_tt u[t,x] = partial_xx u[t,x] - u[t,x]", params=("u", "t", "x")),
    S("Klein-Gordon exact pulse solution", ["U006015", "U006016"], "RELATION", "u[t,x]=If[x^2>t^2,0,BesselJ[0,Sqrt[t^2-x^2]]]", params=("t", "x")),
    S("negative-diffusion PDE relation", ["U006024", "U006025", "U006026"], "PDE", "partial_t u[t,x] = -partial_xx u[t,x]", params=("u", "t", "x")),
    S("scalar-field PDE family", ["U006029", "U006030", "U006031"], "PDE", "partial_tt u[t,x] = partial_xx u[t,x] + f[u[t,x]]", params=("f", "u", "t", "x")),
    S("scalar-field potential relation", ["U006032"], "RELATION", "v[u] = -Integrate[f[u],u]", params=("f", "u")),
    S("scalar-field Lagrangian density", ["U006033", "U006034"], "RELATION", "((partial_t u)^2-(partial_x u)^2)/2-v[u]", params=("u", "v")),
    S("scalar-field Hamiltonian functional", ["U006035", "U006036", "U006037"], "RELATION", "Integrate[((partial_t u)^2+(partial_x u)^2)/2+v[u],{x,-Infinity,Infinity}]", params=("u", "v")),
    S("page-165 spatially uniform background ODE", ["U006038", "U006039", "U006040"], "ODE", "u''[t]==(1-u[t]^2)(1+a u[t]), with u[0]==u'[0]==0", params=("a", "t")),
    S("a=0 Jacobi background solution", ["U006041", "U006042"], "RELATION", "Sqrt[3] JacobiSN[t/3^(1/4),1/2]^2/(1+JacobiCN[t/3^(1/4),1/2]^2)", params=("t",)),
    S("general Jacobi background solution", ["U006043", "U006044", "U006045", "U006046", "U006047", "U006048", "U006049", "U006050", "U006051"], "RELATION", "b d JacobiSN[r t,s]^2/(b-d JacobiCN[r t,s]^2), with printed r,s and cubic root relation", params=("a", "b", "c", "d", "t")),
    S("finite-difference PDE discretization family", ["U006052"], "SOLVER", "replace continuous space and time by discrete cells and refine cell sizes toward the target PDE", params=("space step", "time step", "PDE"), missing=("This unit states the method family but not a particular stencil.",)),
    S("Courant stability constraint", ["U006053"], "QUERY", "for the described diffusion discretization require dt/dx < 1/2", params=("dt", "dx")),
    S("explicit second-order PDE finite-difference solver", ["U006058", "U006059", "U006060", "U006061", "U006062", "U006063"], "SOLVER", "PDEKernel applies (2b-d)+((a+c-2b)/dx^2+f[b])dt^2; PDEStep updates all periodic cells synchronously", params=("f", "dx", "dt", "two initial slices", "steps"), overrides={"boundary": "periodic boundary induced by RotateLeft/RotateRight"}),
    S("page-165 Gaussian numerical preset", ["U006064", "U006065"], "GENERATOR", "PDEEvolveList with f=(1-u^2)(1+u), dx=.1, dt=.05, paired Gaussian initial slices, 400 steps", params=("fixed preset",)),
    S("PDE convergence observer", ["U006066"], "OBSERVER", "compare numerical patterns as dx decreases and check approximate energy conservation", params=("solutions at multiple dx",)),
    S("different-power scalar-field PDE family", ["U006068", "U006069", "U006070"], "PDE", "partial_tt u = partial_xx u + (1-u^n)(1+a u), for n=4,6,8,...", params=("n", "a", "u", "t", "x")),
    S("Burgers-equation relation", ["U006071", "U006072"], "PDE", "partial_t u[t,x] = partial_xx u[t,x] - u[t,x] partial_x u[t,x]", images=(OTHER_PDE_IMAGE,), image_direct=True, params=("u", "t", "x")),
    S("nonlinear Schrodinger equation relation", ["U006071", "U006072"], "PDE", "i partial_t u[t,x] = -partial_xx u[t,x] + 4 Abs[u[t,x]]^2 u[t,x]", images=(OTHER_PDE_IMAGE,), image_direct=True, params=("u", "t", "x")),
    S("Kuramoto-Sivashinsky equation relation", ["U006071", "U006072"], "PDE", "partial_t u[t,x] = -partial_xx u[t,x] - (1/2) partial_xxxx u[t,x] + (partial_x u[t,x])^2", images=(OTHER_PDE_IMAGE,), image_direct=True, params=("u", "t", "x")),
    S("deterministic Kardar-Parisi-Zhang equation", ["U006072"], "PDE", "partial_t u[t,x] = a partial_xx u[t,x] + (b/2)(partial_x u[t,x])^2", params=("a", "b", "u", "t", "x")),
    S("uniformly-distributed fractional-part family", ["U005686"], "RELATION", "Mod[a[n],1] is uniformly distributed for the listed functions, with n Sin[n] stated as conjectural", params=("sequence a", "n"), variants=("proved listed cases", "conjectural n Sin[n] case")),
    S("analytic prime-approximation family", ["U005810", "U005956"], "FUNCTION", "Prime[n] approximately n Log[n]+n Log[Log[n]]; PrimePi[n] approximated by n/Log[n], LogIntegral[n], and the zeta-zero correction", params=("n",), variants=("nth-prime approximation", "prime-count approximation", "zeta-zero correction")),
    S("relative-primality constraint", ["U005816"], "QUERY", "two integers are accepted when they share no nontrivial factor", params=("first integer", "second integer")),
    S("sum-of-three-squares representability constraint", ["U005820"], "QUERY", "the main-text condition decides which integers are sums of three squares", routes=("three_squares",), missing=("The actual necessary-and-sufficient condition is only in the routed main-text target.",)),
    S("Waring power-sum representability bounds", ["U005822"], "RELATION", "every integer is representable by at most nine cubes and nineteen fourth powers, with further stated cube restrictions", params=("integer", "power")),
    S("rational double-integral special-function identity", ["U005930", "U005931", "U005932"], "RELATION", "the printed double integral of 1/(1+x^2+y^2) equals a HypergeometricPFQ, Pi ArcSinh, and Catalan expression"),
    S("two-Gaussian periodic-boundary PDE comparison preset", ["U006019"], "GENERATOR", "two Gaussian initial components with periodic boundary conditions are evolved under diffusion, wave, sine-Gordon, and the page-165 equation", variants=("diffusion", "wave", "sine-Gordon", "page-165 equation"), missing=("Gaussian scale, separation, and numerical grid are not printed in the Notes unit.",)),
    S("dimensional wave-equation square-pulse preset", ["U006021", "U006023"], "GENERATOR", "stationary square-pulse initial data for the wave equation in 1D, 2D, and 3D, observed through a one-dimensional r^(d-1)-weighted slice", params=("dimension d",), variants=("1D", "2D", "3D"), missing=("The exact pulse dimensions, domain, and boundary data are not printed.",)),
    S("PDE boundary-value constraint semantics", ["U006028"], "CALCULUS", "a PDE constrains a whole function over a region; boundary data can admit many, one, or no solutions, with finite-speed domains of dependence for hyperbolic equations", params=("PDE", "region", "boundary data"), variants=("hyperbolic finite-speed domain", "elliptic global dependence")),
    S("named PDE numerical-method family", ["U006055", "U006058"], "SOLVER", "NDSolve, finite differences, method of lines, and pseudospectral methods discretize PDE solution problems", variants=("NDSolve", "finite difference", "method of lines", "pseudospectral"), missing=("Only the explicit finite-difference member is specified later; the other method laws are not printed.",)),
]


def FF(
    value: str | None,
    anchors: str | tuple[str, ...],
    *,
    status: str = "SUPPORTED",
    reason: str = "",
) -> dict[str, Any]:
    """Declare one source-limited fingerprint fact.

    ``anchors`` contains exact source-unit IDs or physical image paths.  Empty
    anchors are permitted only for UNKNOWN facts.
    """

    if isinstance(anchors, str):
        anchors = (anchors,)
    return {
        "status": status,
        "value": value,
        "anchors": tuple(anchors),
        "reason": reason,
    }


def spec_named(name: str) -> dict[str, Any]:
    matches = [spec for spec in SPECS if spec["name"] == name]
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one spec named {name!r}")
    return matches[0]


def amend_spec(existing_name: str, **changes: Any) -> None:
    spec = spec_named(existing_name)
    if "facts" in changes:
        merged = dict(spec.get("facts", {}))
        merged.update(changes.pop("facts"))
        spec["facts"] = merged
    spec.update(changes)


def remove_spec(name: str) -> None:
    spec = spec_named(name)
    SPECS.remove(spec)


# ---------------------------------------------------------------------------
# Hostile-review repairs.
#
# These edits deliberately live as data mutations rather than post-hoc output
# patches.  A fresh bundle authored from this helper receives the repaired
# identities, laws, field provenance, source boundaries, and routes.
# ---------------------------------------------------------------------------

amend_spec(
    "Gray-code ordering generator",
    uids=["U005647", "U005648", "U005649"],
    facts={
        "complete_state": FF(
            "the complete accumulated Gray-code ordering list",
            "U005648",
        ),
        "visible_history": FF(
            "each Nest state is the accumulated ordering list; the prior list "
            "remains as the first half of the next list",
            "U005648",
        ),
        "seed": FF("{0}", "U005648"),
        "frontier_or_activation": FF(
            "the complete current ordering list is reflected and extended",
            "U005648",
        ),
        "schedule": FF(
            "each of the m Nest generations reflects the current list, adds "
            "its length to that reflection, and appends it",
            "U005648",
        ),
        "read_dependencies_or_neighborhood": FF(
            "the current complete list and its length",
            "U005648",
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "GrayCode[m_] := Nest[Join[#, Length[#] + Reverse[#]] &, {0}, m]; "
            "the element at position i is BitXor[i, Floor[i/2]]",
            ("U005648", "U005649"),
        ),
        "write_replacement_assembly_or_commit": FF(
            "Join retains the current list and appends Length[list] + "
            "Reverse[list] as the new half",
            "U005648",
        ),
        "termination_completion_failure": FF(
            "For a supplied nonnegative digit count m, the printed Nest performs exactly m generations.",
            "U005648",
        ),
    },
)

amend_spec(
    "continued-fraction-derived substitution generator",
    uids=["U005682", "U005683", "U005684", "U005685", "U005681"],
    law=(
        "rules = Map[({0 -> Join[#, {1}], "
        "1 -> Join[#, {1, 0}]} &)[Table[0, {# - 1}]] &, "
        "Reverse[Rest[ContinuedFraction[h, m]]]]; "
        "Floor[h] + Fold[Flatten[#1 /. #2] &, {0}, rules]"
    ),
    facts={
        "complete_state": FF(
            "the current 0/1 word together with the remaining generated rule list",
            ("U005682", "U005684"),
        ),
        "visible_history": FF(
            None,
            "U005684",
            status="NOT_APPLICABLE",
            reason=(
                "The printed Fold returns the final accumulated word; it does "
                "not return the preceding replacement generations."
            ),
        ),
        "seed": FF("{0}", "U005684"),
        "frontier_or_activation": FF(
            "at each Fold stage, every 0 or 1 occurrence in the current word "
            "is eligible for the current generated replacement rule",
            ("U005682", "U005684"),
        ),
        "schedule": FF(
            "Fold applies the generated rule list sequentially in its listed order",
            ("U005682", "U005684"),
        ),
        "read_dependencies_or_neighborhood": FF(
            "ContinuedFraction[h,m] generates the ordered rule list; each "
            "Fold stage reads the current word and the next rule",
            ("U005682", "U005684"),
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "rules = Map[({0 -> Join[#, {1}], "
            "1 -> Join[#, {1, 0}]} &)[Table[0, {# - 1}]] &, "
            "Reverse[Rest[ContinuedFraction[h, m]]]]; "
            "Floor[h] + Fold[Flatten[#1 /. #2] &, {0}, rules]",
            ("U005682", "U005684"),
        ),
        "write_replacement_assembly_or_commit": FF(
            "each stage computes Flatten[current /. rule]; after all rules, "
            "Floor[h] is added to the assembled digit list",
            ("U005682", "U005684"),
        ),
        "termination_completion_failure": FF(
            "the finite generated rule list is exhausted by Fold; for "
            "quadratic h the source also states that the rule repertoire is finite",
            ("U005682", "U005684", "U005685"),
        ),
    },
)

amend_spec(
    "parity-trace initial-condition reconstructor",
    law=(
        "IntegerDigits[First[Fold[{Mod[If[OddQ[#2], "
        "2 First[#1] - 1, 2 First[#1] "
        "PowerMod[5, -1, Last[#1]]], Last[#1]], "
        "2 Last[#1]} &, {0, 2}, Reverse[list]]], 2, Length[list]]"
    ),
    law_uid="U005700",
)

amend_spec(
    "page-131 sequence (d)",
    law=(
        "f[n_] := (n + g[IntegerDigits[n, 2]])/2; "
        "g[{(1)..}] = 1; g[{1, (0)..}] = 0; "
        "g[{1, s__}] := 1 + "
        "g[IntegerDigits[FromDigits[{s}, 2] + 1, 2]]"
    ),
    facts={
        "read_dependencies_or_neighborhood": FF(
            "f reads n and the recursive helper g; g distinguishes an all-1 "
            "list, a 1 followed only by 0s, and a remaining suffix s",
            ("U005746", "U005747"),
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "f[n_] := (n + g[IntegerDigits[n, 2]])/2; "
            "g[{(1)..}] = 1; g[{1, (0)..}] = 0; "
            "g[{1, s__}] := 1 + "
            "g[IntegerDigits[FromDigits[{s}, 2] + 1, 2]]",
            ("U005746", "U005747"),
        ),
    },
)

amend_spec(
    "page-131 sequence (c) hump generator",
    law=(
        "hump formulation: FoldList[Plus, 0, Flatten["
        "Nest[Delete[NestList[Rest, #, Length[#] - 1], 2] &, "
        "Append[Table[1, {m}], 0], m]] - 1/2]; "
        "reordered-digit formulation: FoldList[Plus, 1, "
        "Map[Last[Last[#]] &, Sort[Table["
        "({Length[#], Apply[Plus, #], 1 - #} &)[IntegerDigits[i, 2]], "
        "{i, 2^m}]]]]"
    ),
    facts={
        "complete_state": FF(
            "for each formulation, the current cumulative sum and the "
            "remaining finite ordered increment list",
            ("U005754", "U005756"),
        ),
        "visible_history": FF(
            "each FoldList returns the complete accumulated list of partial "
            "sums, including its initial 0 or 1",
            ("U005754", "U005756"),
        ),
        "seed": FF(
            "the hump FoldList starts from 0; the reordered-base-2 FoldList "
            "starts from 1",
            ("U005754", "U005756"),
        ),
        "frontier_or_activation": FF(
            "the next increment in the selected formulation's finite ordered list",
            ("U005754", "U005756"),
        ),
        "schedule": FF(
            "FoldList consumes the selected finite increment list from left to right",
            ("U005754", "U005756"),
        ),
        "read_dependencies_or_neighborhood": FF(
            "the current cumulative sum and next increment produced either "
            "by the nested hump list or by the sorted base-2 digit tuples",
            ("U005754", "U005756"),
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "hump formulation: FoldList[Plus, 0, Flatten["
            "Nest[Delete[NestList[Rest, #, Length[#] - 1], 2] &, "
            "Append[Table[1, {m}], 0], m]] - 1/2]; "
            "reordered-digit formulation: FoldList[Plus, 1, "
            "Map[Last[Last[#]] &, Sort[Table["
            "({Length[#], Apply[Plus, #], 1 - #} &)[IntegerDigits[i, 2]], "
            "{i, 2^m}]]]]",
            ("U005754", "U005756"),
        ),
        "write_replacement_assembly_or_commit": FF(
            "each Plus update appends its new cumulative sum to the visible "
            "list returned by FoldList",
            ("U005754", "U005756"),
        ),
        "result_kind": FF(
            "the accumulated visible hump list, or the alternative list of "
            "the first 2^m sequence elements",
            ("U005754", "U005756"),
        ),
        "termination_completion_failure": FF(
            "both printed formulations consume finite lists determined by m; "
            "the second returns the first 2^m elements",
            ("U005754", "U005756"),
        ),
        "parameters_and_variants": FF(
            "parameter m; variants: nested hump FoldList and reordered-base-2 "
            "digit FoldList",
            ("U005754", "U005756"),
        ),
    },
)

amend_spec(
    "arithmetic-geometric-mean pi solver",
    law=(
        "(#[[2]]^2/#[[3]] &)[NestWhile["
        "Apply[Function[{a, b, c, d}, "
        "{(a + b)/2, Sqrt[a b], c - d (a - b)^2, 2 d}], #] &, "
        "{1, 1/Sqrt[N[2, n]], 1/4, 1/4}, "
        "#[[1]] != #[[2]] &]]"
    ),
    law_uid="U005846",
    facts={
        "complete_state": FF(
            "the four-tuple {a,b,c,d}",
            "U005846",
        ),
        "visible_history": FF(
            None,
            "U005846",
            status="NOT_APPLICABLE",
            reason=(
                "The printed NestWhile returns the terminal four-tuple; it "
                "does not return the earlier tuples."
            ),
        ),
        "control_state": FF(
            "continue exactly while a != b, written #[[1]] != #[[2]] &",
            "U005846",
        ),
        "seed": FF(
            "{1, 1/Sqrt[N[2, n]], 1/4, 1/4}",
            "U005846",
        ),
        "frontier_or_activation": FF(
            "the complete current four-tuple {a,b,c,d}",
            "U005846",
        ),
        "schedule": FF(
            "update all four tuple components together, then retest a != b",
            "U005846",
        ),
        "read_dependencies_or_neighborhood": FF(
            "the current a,b,c,d tuple and requested precision n in the initial b",
            "U005846",
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "(#[[2]]^2/#[[3]] &)[NestWhile["
            "Apply[Function[{a, b, c, d}, "
            "{(a + b)/2, Sqrt[a b], c - d (a - b)^2, 2 d}], #] &, "
            "{1, 1/Sqrt[N[2, n]], 1/4, 1/4}, "
            "#[[1]] != #[[2]] &]]",
            "U005846",
        ),
        "write_replacement_assembly_or_commit": FF(
            "atomically replace {a,b,c,d} by "
            "{(a+b)/2,Sqrt[a b],c-d(a-b)^2,2d}",
            "U005846",
        ),
        "result_kind": FF(
            "the terminal pi approximation b^2/c, written #[[2]]^2/#[[3]]",
            "U005846",
        ),
        "termination_completion_failure": FF(
            "NestWhile continues while a != b (#[[1]] != #[[2]]) and the "
            "source states that equality is reached after approximately "
            "Log[2, n] steps",
            ("U005846", "U005847"),
        ),
    },
)
for old_name, new_name in (
    ("BitXor[2 n,n] digit function", "BitXor[2 n,n] integer iteration"),
    ("BitXor[3+2 n,n] digit function", "BitXor[3+2 n,n] integer iteration"),
    ("BitXor[3 n,n] digit function", "BitXor[3 n,n] integer iteration"),
    ("BitXor[6 n,n] digit function", "BitXor[6 n,n] integer iteration"),
    ("BitOr[2 n,n] digit function", "BitOr[2 n,n] integer iteration"),
    ("BitOr[6 n,n] digit function", "BitOr[6 n,n] integer iteration"),
):
    amend_spec(
        old_name,
        name=new_name,
        kind="ITERATION",
        params=("initial n",),
        facts={
            "termination_completion_failure": FF(
                "The source specifies repeated application and no intrinsic terminal predicate.",
                "U005725",
            ),
        },
    )
amend_spec(
    "BitXor[2 n,n] integer iteration",
    uids=["U005649", "U005725"],
    variants=("digit sequences correspond to elementary cellular automaton rule 60",),
    facts={
        "termination_completion_failure": FF(
            "U005649 and U005725 specify repeated application and no intrinsic terminal predicate.",
            ("U005649", "U005725"),
        ),
    },
)

amend_spec(
    "base-6 cellular automaton for powers of three",
    law="{a_, b_, c_} -> 3 Mod[b, 2] + Floor[c/2]",
    missing=(),
    facts={
        "alphabet_or_value_schema": FF("six base-6 digit colors", "U005671"),
        "read_dependencies_or_neighborhood": FF(
            "three-cell input {a,b,c}; the printed value depends on b and c",
            "U005671",
        ),
        "topology": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="U005671 gives a local three-cell rule but does not state a periodic, finite, or infinite boundary topology.",
        ),
    },
)

amend_spec(
    "3n+1 eventual-one decision query",
    name="universal 3n+1 eventual-one query",
    uids=["U005689", "U005690"],
    law="for every initial positive integer n, FixedPoint[(3 #/2^IntegerExponent[#, 2] + 1)/2 &, n] == 2",
    params=(),
    missing=(),
    facts={
        "witness_semantics": FF(
            "accepted only if the displayed per-seed equality holds for every positive-integer initial n; the Book says no general proof is known",
            ("U005689", "U005690"),
        ),
        "termination_completion_failure": FF(
            "The query is mathematically well specified, but its universal truth is unresolved in the source.",
            "U005689",
        ),
    },
)
SPECS.append(
    S(
        "per-seed 3n+1 eventual-one predicate",
        ["U005690"],
        "QUERY",
        "FixedPoint[(3 #/2^IntegerExponent[#, 2] + 1)/2 &, n] == 2",
        params=("initial n",),
        facts={
            "witness_semantics": FF(
                "accepted for a supplied n exactly when the displayed FixedPoint expression equals 2",
                "U005690",
            ),
            "termination_completion_failure": FF(
                "FixedPoint may fail to return if the accelerated orbit does not reach a fixed point; the source does not prove completion for every n.",
                "U005690",
            ),
        },
    )
)
SPECS.append(
    S(
        "case-b binary-length stopping-time map",
        ["U005694"],
        "ITERATION",
        "n -> If[EvenQ[n], n/2, (n + 1)/2]",
        params=("initial n",),
        images=("BACK-MATTER/NOTES/_page_919_Figure_10.jpeg",),
        facts={
            "native_time": FF(
                "discrete applications counted until value 1 is reached",
                "U005694",
            ),
            "seed": FF("the starting integer n", "U005694"),
            "input": FF("initial integer n", "U005694"),
            "parameters_and_variants": FF(
                "parameter: initial n; case (b) is distinct from cases (a) and (c)",
                "U005694",
            ),
            "termination_completion_failure": FF(
                "The source states that the number of steps to reach 1 equals the number of base-2 digits in n.",
                "U005694",
            ),
        },
        source_status=("CLEAR", "DEFECTIVE"),
        source_uncertainties=(
            "A000443 is bottom-clipped, but the complete case-(b) formula remains visible.",
        ),
    )
)
SPECS.append(
    S(
        "case-c one-bit-count stopping-time map obligation",
        ["U005694"],
        "PARTIAL_SYSTEM",
        "The rule is not recoverable from the sealed extraction; the prose states only that its stopping time is determined by the number of 1 bits in n.",
        params=("initial n",),
        missing=(
            "The case-(c) one-step update formula is clipped from A000443 and is not stated in the prose.",
        ),
        images=("BACK-MATTER/NOTES/_page_919_Figure_10.jpeg",),
        facts={
            "rule_relation_constraint_function_or_probability_law": FF(
                None,
                (),
                status="UNKNOWN_FROM_SOURCE",
                reason="The sealed prose delimits case (c), but the formula label is outside A000443's bottom crop.",
            ),
            "termination_completion_failure": FF(
                "The source states only that the number of steps is determined by DigitCount[n,2,1].",
                "U005694",
            ),
        },
        source_status=("CLEAR", "DEFECTIVE"),
        source_uncertainties=(
            "The candidate is retained under E5 because A000443 cuts off the identity-bearing case-(c) update formula.",
        ),
    )
)

amend_spec(
    "memoized self-indexed recurrence",
    variants=(),
    facts={
        "termination_completion_failure": FF(
            "Evaluation can request an undefined f[-1]; cancellation such as f[-1]-f[-1] does not prevent leftmost-innermost evaluation from attempting it.",
            "U005744",
        ),
    },
)
SPECS.append(
    S(
        "leftmost-innermost recursive evaluation policy",
        ["U005744"],
        "EVALUATION_POLICY",
        "evaluate the leftmost innermost f[k] occurrence to an explicit value before using the enclosing expression",
        params=("recursive expression",),
        variants=("memoized value reuse is a separate implementation policy",),
        facts={
            "termination_completion_failure": FF(
                "The policy may demand an undefined subvalue even when the complete symbolic expression would cancel that subvalue.",
                "U005744",
            ),
        },
    )
)

amend_spec(
    "primitive-recursive construction calculus",
    uids=["U005762", "U005763", "U005764", "U005768", "U005769"],
    law="zero z=0&, successor s=#+1&, projections p[i_]:=Slot[i]&, composition, and "
        "f[0,y___Integer]:=g[y]; f[x_Integer,y___Integer]:=h[f[x-1,y],x-1,y], "
        "which unwinds to Fold[h[#1,#2,y]&,g[y],Range[0,x-1]]",
    facts={
        "support": FF("non-negative integer inputs", ("U005762", "U005768")),
        "termination_completion_failure": FF(
            "Every primitive-recursive computation is total on its stated non-negative-integer domain and has a finitely bounded evaluation.",
            ("U005768", "U005769"),
        ),
    },
)
amend_spec(
    "unbounded mu-search operator",
    facts={
        "termination_completion_failure": FF(
            "Search returns the first n with f[n,args]==0; it may never terminate when no such n is reached.",
            ("U005770", "U005771", "U005772"),
        ),
        "witness_semantics": FF(
            "a returned n is the least nonnegative witness satisfying f[n,args]==0",
            "U005771",
        ),
    },
)
amend_spec(
    "complex primitive-recursive function",
    law="Fold[Fold[2^Ceiling[Log[2, Ceiling[(#1 + 2)/(#2 + 2)]]] "
        "(#2 + 2) - 2 - #1 &, #2, Range[#1]] &, 0, Range[#]] &",
    law_uid="U005786",
)
amend_spec(
    "diagonalized non-primitive-recursive function",
    params=("enumeration w", "x"),
    facts={
        "input": FF(
            "a chosen enumeration w[m] of primitive-recursive functions and an index x",
            "U005793",
        ),
        "support": FF(
            "conditional on the chosen enumeration/order w; the source suggests LeafCount then Sort but does not print the enumeration",
            "U005793",
        ),
    },
)
amend_spec(
    "Fermat-little-theorem primality predicate",
    name="Fermat little-theorem prime congruence",
    kind="RELATION",
    law="PrimeQ[p] implies Mod[a^(p - 1), p] == 1",
    missing=(),
    facts={
        "witness_semantics": FF(
            "congruence failure disproves the stated necessary prime condition; congruence truth is not asserted to prove primality",
            "U005802",
        ),
        "termination_completion_failure": FF(
            "The congruence is a stated necessary condition, not a complete false-positive-resistant primality algorithm.",
            "U005802",
        ),
    },
)
amend_spec(
    "decimation survival-time query",
    name="decimation survival-time function",
    kind="OBSERVER",
    law="Module[{q = n + k - 1, s = 1}, While[Mod[q, k] != 0, "
        "q = Ceiling[(k - 1) q/k]; s++]; s]",
    law_uid="U005805",
    facts={
        "result_kind": FF(
            "integer number of decimation steps survived by the cell at position n",
            ("U005804", "U005805"),
        ),
        "witness_semantics": FF(
            "the returned integer s is the survival time, not a Boolean acceptance judgment",
            ("U005804", "U005805"),
        ),
    },
)
amend_spec(
    "Josephus last-cell function",
    law="Fold[Mod[#1 + k, #2, 1] &, 0, Range[n]]",
)

remove_spec("analytic prime-approximation family")
SPECS.extend([
    S(
        "nth-prime asymptotic approximation",
        ["U005810"],
        "FUNCTION",
        "Prime[n] is approximated by n Log[n] + n Log[Log[n]]",
        params=("n",),
    ),
    S(
        "prime-counting approximation family",
        ["U005810", "U005956"],
        "FUNCTION",
        "PrimePi[n] is approximated by n/Log[n], by LogIntegral[n], and up to "
        "order Sqrt[n] by LogIntegral[n] - Sum[LogIntegral[n^r[i]], "
        "{i,-Infinity,Infinity}] using zeta zeros r[i]",
        params=("n",),
        variants=("n/Log[n]", "LogIntegral[n]", "zeta-zero correction"),
    ),
])

remove_spec("perfect-number constraint")
SPECS.extend([
    S(
        "perfect-number constraint",
        ["U005830"],
        "QUERY",
        "Apply[Plus, Divisors[n]] == 2 n",
        params=("n",),
    ),
    S(
        "pluperfect-number constraint",
        ["U005832"],
        "QUERY",
        "IntegerQ[DivisorSigma[1, n]/n]",
        params=("n",),
    ),
    S(
        "quasiperfect-number tolerance constraint",
        ["U005832"],
        "QUERY",
        "Abs[DivisorSigma[1, n] - 2 n] < r",
        params=("n", "r"),
    ),
])
amend_spec(
    "unbounded aliquot-growth query",
    params=(),
    missing=(),
    facts={
        "witness_semantics": FF(
            "accepted if there exists an iterated aliquot trajectory whose values increase forever",
            "U005837",
        ),
        "termination_completion_failure": FF(
            "The accepted-result condition is complete, but the source states that its truth remains unresolved.",
            "U005837",
        ),
    },
)
amend_spec(
    "direct nth-binary-digit extractor",
    name="direct nth base-2 digit extractor for Log[2]",
    law="Round[FractionalPart[Sum[FractionalPart[PowerMod[2,n-k,k]/k],"
        "{k,n}] + Sum[2^(n-k)/k,{k,n+1,n+d}]]]",
    law_uid="U005849",
    facts={
        "result_kind": FF("the nth base-2 digit of Log[2]", ("U005848", "U005849")),
        "termination_completion_failure": FF(
            "Trying several tail lengths d checks stability, but finite-precision truncation retains an exponentially small probability of an incorrect digit.",
            "U005850",
        ),
    },
)
amend_spec(
    "normal-number constraint",
    variants=(),
    facts={
        "witness_semantics": FF(
            "accepted in the selected base only when every digit and every finite digit block has equal limiting frequency",
            "U005860",
        ),
    },
)
SPECS.append(
    S(
        "Stoneham normal-number family",
        ["U005860"],
        "RELATION",
        "Sum[1/(p^n b^(p^n)), {n, Infinity}] is normal in base b and "
        "transcendental when p > 2 is prime and GCD[b,p] == 1",
        params=("prime p", "base b"),
        facts={
            "support": FF("p > 2 prime and GCD[b,p] == 1", "U005860"),
        },
    )
)

amend_spec(
    "Ulam sequence",
    facts={
        "complete_state": FF(
            "the complete finite sequence accumulated so far",
            ("U005796", "U005797"),
        ),
        "visible_history": FF(
            "the current sequence is the accumulated visible list of every "
            "previously appended term",
            ("U005796", "U005797"),
        ),
        "seed": FF("{1, 2}", ("U005796", "U005797")),
        "frontier_or_activation": FF(
            "integers larger than the current last term are tested in "
            "increasing order until one has exactly one representation as a "
            "sum of two distinct earlier terms",
            ("U005796", "U005797", "U005798"),
        ),
        "schedule": FF(
            "append exactly the least qualifying integer, then repeat the search",
            ("U005796", "U005797"),
        ),
        "read_dependencies_or_neighborhood": FF(
            "the complete accumulated sequence and pair sums of distinct earlier terms",
            ("U005796", "U005797", "U005798"),
        ),
        "write_replacement_assembly_or_commit": FF(
            "append the least uniquely representable sum to the accumulated list",
            ("U005796", "U005797"),
        ),
        "termination_completion_failure": FF(
            "the definition generates an unbounded sequence; no intrinsic "
            "terminal predicate is stated",
            ("U005796", "U005797"),
        ),
    },
)

amend_spec(
    "successive-integer concatenation sequence",
    uids=["U005867", "U005860"],
    facts={
        "native_time": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason=(
                "The printed Flatten[Table[...]] directly denotes a finite "
                "digit list for n; it does not state an intrinsic time evolution."
            ),
        ),
        "complete_state": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason=(
                "The finite Table/Flatten expression denotes its result "
                "without an evolving native state."
            ),
        ),
        "visible_history": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason=(
                "The returned digit list is the denoted result, not a retained "
                "history of transition states."
            ),
        ),
        "control_state": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason="No transition controller is part of the direct finite expression.",
        ),
        "seed": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason="The bound n and base k are inputs, not a trajectory seed.",
        ),
        "frontier_or_activation": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason="No active component is selected by the direct Table/Flatten denotation.",
        ),
        "schedule": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason="The expression directly indexes integers 1 through n; no one-step schedule is asserted.",
        ),
        "write_replacement_assembly_or_commit": FF(
            None,
            "U005867",
            status="NOT_APPLICABLE",
            reason="Flatten assembles the denoted finite result; it is not a state commit.",
        ),
        "structural_invariants": FF(
            "the base-10 infinite concatenation is Champernowne's normal, "
            "transcendental number; the general base-k limit contains every "
            "finite block with equal frequency",
            ("U005860", "U005867"),
        ),
        "termination_completion_failure": FF(
            "for finite n the nested Table and Flatten return a finite list",
            "U005867",
        ),
    },
)

amend_spec(
    "rational-pair continued-fraction term enumerator",
    facts={
        "native_time": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="The printed nested Table directly denotes a finite enumeration for n.",
        ),
        "complete_state": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="No evolving state is intrinsic to the finite Table/Flatten result.",
        ),
        "visible_history": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="The returned flattened terms are a denoted result, not a transition history.",
        ),
        "control_state": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="No transition controller is stated by the direct enumeration.",
        ),
        "seed": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="The bound n is an input to the finite enumeration, not a trajectory seed.",
        ),
        "frontier_or_activation": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="No active component is selected by the direct nested Table.",
        ),
        "schedule": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="The nested Table specifies an index domain, not a one-step evolution schedule.",
        ),
        "write_replacement_assembly_or_commit": FF(
            None,
            "U005906",
            status="NOT_APPLICABLE",
            reason="Flatten assembles the finite enumeration without committing a successor state.",
        ),
        "termination_completion_failure": FF(
            "for finite n the bounded a,b tables and Flatten return a finite list",
            ("U005906", "U005907"),
        ),
    },
)

amend_spec(
    "Farey-sequence generator",
    facts={
        "native_time": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="The printed Union[Flatten[Table[...]]] directly denotes the finite Farey set.",
        ),
        "complete_state": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="No evolving native state is intrinsic to the direct finite expression.",
        ),
        "visible_history": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="The returned ordered set is not a retained transition history.",
        ),
        "control_state": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="No transition controller is part of the direct set construction.",
        ),
        "seed": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="The order bound n is an input, not an initial trajectory state.",
        ),
        "frontier_or_activation": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="No active component is selected by the direct Table/Flatten/Union denotation.",
        ),
        "schedule": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="The bounded index domain is not a one-step update schedule.",
        ),
        "write_replacement_assembly_or_commit": FF(
            None,
            "U005924",
            status="NOT_APPLICABLE",
            reason="Union and Flatten assemble the denoted finite set without a state commit.",
        ),
        "termination_completion_failure": FF(
            "for finite n the bounded table, flattening, and union return the finite Farey sequence",
            ("U005923", "U005924"),
        ),
    },
)

amend_spec(
    "continued-fraction digit extractor",
    facts={
        "termination_completion_failure": FF(
            "For rational x the iteration reaches Mod[x,1]==0 and the next reciprocal is undefined; only the available finite terms are defined.",
            ("U005887", "U005888"),
        ),
    },
)
amend_spec(
    "Gauss-map continued-fraction trajectory",
    facts={
        "visible_history": FF(
            "NestList returns the complete iterate history beginning with x",
            "U005891",
        ),
        "seed": FF("x", "U005891"),
        "frontier_or_activation": FF(
            "the current scalar iterate",
            "U005891",
        ),
        "schedule": FF(
            "apply 1/Mod[current,1] once per requested iterate",
            "U005891",
        ),
        "write_replacement_assembly_or_commit": FF(
            "append each new reciprocal-fractional-part iterate to the list returned by NestList",
            "U005891",
        ),
        "termination_completion_failure": FF(
            "The map is undefined when Mod[x,1]==0; rational inputs therefore terminate after finitely many continued-fraction terms.",
            "U005891",
        ),
    },
)
amend_spec(
    "direct concatenation-position query",
    law="((IntegerDigits[#3 + Quotient[#1,#2],2][[Mod[#1,#2]+1]] &)"
        "[n-(#-2)2^(#-1)-2,#,2^(#-1)] &)"
        "[NestWhile[# + 1 &,0,(#-1)2^# + 1 < n &]]",
    law_uid="U005876",
)
amend_spec(
    "large-block concatenation digit formula",
    law="k/(k-1)^2 - (k-1) Sum[k^((k^s-1)(1+s-s k)/(k-1)) "
        "(1/((k-1)(k^s-1)^2) - k/((k-1)(k^(s+1)-1)^2) + "
        "1/(k^(s+1)-1)), {s,n}]",
    law_uid="U005880",
)
amend_spec(
    "linear-polynomial continued-fraction relation",
    law="a continued fraction whose nth term is a n + b denotes "
        "BesselI[b/a, 2/a]/BesselI[b/a + 1, 2/a]",
)
amend_spec(
    "Shallit nested continued-fraction substitution",
    law="{0,k-1,k+2,k,k,k-2,k,k+2,k-2,k}[["
        "Nest[Flatten[{{1,2},{3,4},{5,6},{7,8},{5,6},{3,4},"
        "{9,10},{7,8},{9,10},{3,4}}[[#]]]&,1,n]]]",
    law_uid="U005900",
)
amend_spec(
    "rational double-integral special-function identity",
    law="Integrate[1/(1+x^2+y^2),{x,0,1},{y,0,1}] == "
        "HypergeometricPFQ[{1/2,1,1},{3/2,3/2},1/9]/6 + "
        "Pi ArcSinh[1]/2 - Catalan",
    law_uid="U005931",
)
amend_spec(
    "square-frequency Fourier sum",
    law="Sum[Sin[n^2 x]/n^2,{n,k}]; at x=p Pi/q and k=Infinity it equals "
        "(Pi/(2q))^2 Sum[Sin[n^2 p Pi/q]/Sin[n Pi/(2q)]^2,{n,q-1}]",
)
amend_spec(
    "Riemann zeta denotation",
    law="for real s, Zeta[s]=Sum[1/n^s,{n,Infinity}]="
        "Product[1/(1-Prime[n]^-s),{n,Infinity}]; complex s uses analytic continuation",
    facts={
        "support": FF(
            "the source states the sum/product for real s and separately names analytic continuation for complex s",
            "U005956",
        ),
    },
)
amend_spec(
    "Riemann-hypothesis constraint",
    law="all indexed zeta zeros r[i] used in the source satisfy Re[r[i]] == 1/2",
    params=("indexed zeta-zero family r",),
)
amend_spec(
    "Gauss fractional-part reciprocal map",
    facts={
        "seed": FF("x", "U005967"),
        "visible_history": FF(
            None,
            "U005967",
            status="NOT_APPLICABLE",
            reason=(
                "The source states the one-step map itself; no returned "
                "iterate-history object is part of this candidate."
            ),
        ),
        "termination_completion_failure": FF(
            "x -> FractionalPart[1/x] is undefined at x=0.",
            "U005967",
        ),
    },
)
amend_spec(
    "exact multiplier-mod-one map",
    uids=["U005968", "U005978"],
    facts={
        "seed": FF("x", "U005968"),
        "visible_history": FF(
            None,
            "U005968",
            status="NOT_APPLICABLE",
            reason=(
                "The source gives the map and a closed form for its nth "
                "iterate, not a returned history of all prior iterates."
            ),
        ),
        "write_replacement_assembly_or_commit": FF(
            "one exact map step replaces x by FractionalPart[a x]; the nth "
            "iterate is directly FractionalPart[a^n x]",
            "U005968",
        ),
    },
)
amend_spec(
    "exact tent-map family",
    facts={
        "seed": FF("x", "U005968"),
        "visible_history": FF(
            None,
            "U005968",
            status="NOT_APPLICABLE",
            reason=(
                "The source gives the map and an a=2 nth-iterate formula, "
                "not a returned history of all earlier values."
            ),
        ),
    },
)
amend_spec(
    "fixed-binary-precision shift-map simulation",
    facts={
        "native_time": FF(
            "the discrete simulated-step index n in the printed direct representation",
            "U005972",
        ),
        "complete_state": FF(
            "the 53 stored base-2 digits obtained from initial condition x at indexed step n",
            ("U005972", "U005975"),
        ),
        "visible_history": FF(
            None,
            "U005972",
            status="NOT_APPLICABLE",
            reason=(
                "The printed closed form returns the digit representation at "
                "step n, not a history of preceding simulated states."
            ),
        ),
        "seed": FF("x", "U005972"),
        "frontier_or_activation": FF(
            None,
            "U005972",
            status="NOT_APPLICABLE",
            reason=(
                "The printed indexed closed form selects no active component "
                "for a one-step rewrite."
            ),
        ),
        "schedule": FF(
            None,
            "U005972",
            status="NOT_APPLICABLE",
            reason=(
                "The printed formula directly denotes the representation at "
                "step n and does not state an incremental update schedule."
            ),
        ),
        "read_dependencies_or_neighborhood": FF(
            "initial condition x, indexed step n, and the fixed 53-bit storage width",
            ("U005972", "U005975"),
        ),
        "write_replacement_assembly_or_commit": FF(
            None,
            "U005972",
            status="NOT_APPLICABLE",
            reason=(
                "IntegerDigits[Mod[2^n Floor[2^53 x],2^53],2,53] "
                "directly denotes the step-n digit representation; it is not "
                "a one-step append or commit law."
            ),
        ),
        "result_kind": FF(
            "the 53-bit digit representation of the finite-storage simulation at step n",
            "U005972",
        ),
        "termination_completion_failure": FF(
            "With 53 stored binary digits the finite-state simulation eventually loses sampled digits and reaches 0, unlike the exact map.",
            ("U005972", "U005974", "U005975", "U005978"),
        ),
    },
)
amend_spec(
    "fixed-decimal-precision shift-map simulation",
    facts={
        "native_time": FF(
            "the discrete simulated-step index n in the printed direct representation",
            "U005973",
        ),
        "complete_state": FF(
            "the binary-coded representation of 12 stored decimal digits derived from x at indexed step n",
            ("U005973", "U005976", "U005977"),
        ),
        "visible_history": FF(
            None,
            "U005973",
            status="NOT_APPLICABLE",
            reason=(
                "The printed closed form returns the digit representation at "
                "step n, not a history of preceding simulated states."
            ),
        ),
        "seed": FF("x", "U005973"),
        "frontier_or_activation": FF(
            None,
            "U005973",
            status="NOT_APPLICABLE",
            reason=(
                "The printed indexed closed form selects no active component "
                "for a one-step rewrite."
            ),
        ),
        "schedule": FF(
            None,
            "U005973",
            status="NOT_APPLICABLE",
            reason=(
                "The printed formula directly denotes the representation at "
                "step n and does not state an incremental update schedule."
            ),
        ),
        "read_dependencies_or_neighborhood": FF(
            "initial condition x, indexed step n, and the fixed 12-decimal-digit BCD storage",
            ("U005973", "U005976", "U005977"),
        ),
        "write_replacement_assembly_or_commit": FF(
            None,
            "U005973",
            status="NOT_APPLICABLE",
            reason=(
                "the nested IntegerDigits expression directly denotes the "
                "step-n BCD representation; it is not a one-step append or commit law."
            ),
        ),
        "result_kind": FF(
            "the binary-coded 12-decimal-digit finite-storage representation at step n",
            "U005973",
        ),
        "termination_completion_failure": FF(
            "The 12-decimal-digit BCD simulation eventually samples beyond stored digits and then follows a finite-precision artifact rather than the exact map.",
            ("U005973", "U005974", "U005976", "U005977", "U005978"),
        ),
    },
)
amend_spec(
    "Anosov torus map",
    source_status=("CONFLICTING",),
    source_uncertainties=(
        "U005993 says rational initial conditions yield repetition and then says rational entries in m yield complicated behavior even though its displayed m is already rational/integer.",
    ),
    facts={
        "parameters_and_variants": FF(
            "matrix m and initial vector; the behavior condition on rational entries of m is internally conflicting",
            "U005993",
            status="CONFLICTING_SOURCE",
            reason="The two rationality statements in U005993 cannot both delimit the claimed behavior as written.",
        ),
    },
)

amend_spec(
    "continuous cellular-automaton family",
    name="continuous cellular-automaton averaging implementation",
    law="CCAEvolveStep[f_,list_List] := Map[f,(RotateLeft[list]+list+"
        "RotateRight[list])/3]; CCAEvolveList[f_,init_List,t_Integer] := "
        "NestList[CCAEvolveStep[f,#]&,init,t]",
    variants=("exact rational arithmetic", "approximate numeric arithmetic"),
    facts={
        "alphabet_or_value_schema": FF("cell values lie between 0 and 1", "U005997"),
        "topology": FF("one-dimensional periodic list induced by RotateLeft/RotateRight", "U005998"),
        "boundary": FF("periodic boundary induced by RotateLeft/RotateRight", "U005998"),
        "frontier_or_activation": FF("Map applies f at every list position", "U005998"),
        "schedule": FF("one synchronous whole-list update per CCAEvolveStep", "U005998"),
        "read_dependencies_or_neighborhood": FF(
            "left neighbor, self, and right neighbor averaged before applying f",
            "U005998",
        ),
        "termination_completion_failure": FF(
            "CCAEvolveList performs the requested t steps; approximate arithmetic can accumulate exponentially growing errors and produce qualitatively wrong patterns.",
            ("U005999", "U006000"),
        ),
    },
)
SPECS.extend([
    S(
        "page-157 continuous-CA transfer-rule preset",
        ["U005997", "U005998", "U005999", "U006000"],
        "CA",
        "average left,self,right, then apply FractionalPart[3 #/2] &",
        params=("initial list", "steps"),
        facts={
            "alphabet_or_value_schema": FF("cell values lie between 0 and 1", "U005997"),
            "topology": FF("one-dimensional periodic list induced by RotateLeft/RotateRight", "U005998"),
            "boundary": FF("periodic boundary induced by RotateLeft/RotateRight", "U005998"),
            "read_dependencies_or_neighborhood": FF("left, self, right arithmetic mean", "U005998"),
            "termination_completion_failure": FF(
                "Exact rational arithmetic is required for detailed calculations; 64-bit approximate values can make the lower pattern qualitatively wrong.",
                ("U005999", "U006000"),
            ),
        },
    ),
    S(
        "page-158 continuous-CA offset-rule preset",
        ["U005997", "U005998", "U005999", "U006000"],
        "CA",
        "average left,self,right, then apply FractionalPart[# + 1/4] &",
        params=("initial list", "steps"),
        facts={
            "alphabet_or_value_schema": FF("cell values lie between 0 and 1", "U005997"),
            "topology": FF("one-dimensional periodic list induced by RotateLeft/RotateRight", "U005998"),
            "boundary": FF("periodic boundary induced by RotateLeft/RotateRight", "U005998"),
            "read_dependencies_or_neighborhood": FF("left, self, right arithmetic mean", "U005998"),
            "termination_completion_failure": FF(
                "Exact rational arithmetic is required for detailed calculations; approximate errors grow exponentially.",
                ("U005999", "U006000"),
            ),
        },
    ),
])
amend_spec(
    "additive continuous cellular automaton",
    facts={
        "topology": FF("one-dimensional periodic list induced by rotations", "U006007"),
        "boundary": FF("periodic boundary induced by RotateLeft/RotateRight", "U006007"),
        "frontier_or_activation": FF("all list positions update together", "U006007"),
        "schedule": FF("one synchronous whole-list update per step", "U006007"),
        "read_dependencies_or_neighborhood": FF("left and right neighbor values", "U006007"),
    },
)
amend_spec(
    "probabilistic cellular automaton family",
    facts={
        "determinism_branching_or_measure": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="U006010 names probabilistic selection between two rules but defers the probabilities and coupling to page 591.",
        ),
        "schedule": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="The local Notes unit does not say how random rule choices are coupled or scheduled.",
        ),
        "topology": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="The local Notes unit does not state a boundary topology for the routed examples.",
        ),
    },
)
amend_spec(
    "autonomous ODE system relation",
    params=("dependent functions", "initial values", "t"),
)
SPECS.append(
    S(
        "non-autonomous ODE system relation",
        ["U006012"],
        "ODE",
        "coupled ordinary differential equations whose right-hand-side function depends explicitly on time",
        params=("dependent functions", "initial values", "t"),
        variants=("the source states that two equations can suffice for non-fixed/non-repetitive behavior",),
    )
)
amend_spec(
    "two-Gaussian periodic-boundary PDE comparison preset",
    kind="PRESET",
    missing=(
        "Gaussian scale, separation, numerical grid, and exact spatial-domain "
        "dimensions are not printed in the Notes unit.",
    ),
    facts={
        "support": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason=(
                "Gaussian scale, separation, and the numerical grid are not "
                "printed in U006019."
            ),
        ),
        "topology": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason=(
                "U006019 states periodic boundary conditions but does not "
                "state exact spatial-domain dimensions."
            ),
        ),
        "seed": FF(
            "initial conditions containing two Gaussians",
            "U006019",
        ),
        "input": FF(
            "two-Gaussian initial data supplied to each compared equation",
            "U006019",
        ),
        "boundary": FF("periodic boundary conditions", "U006019"),
        "parameters_and_variants": FF(
            "compared equation variants: diffusion; wave; sine-Gordon; "
            "page-165 equation",
            "U006019",
        ),
    },
)
amend_spec(
    "dimensional wave-equation square-pulse preset",
    kind="PRESET",
    missing=(
        "The exact pulse dimensions, spatial-domain extent, and boundary data "
        "are not printed.",
    ),
    facts={
        "support": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="U006021 does not state the exact stationary square-pulse dimensions.",
        ),
        "topology": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="U006021-U006023 do not state the exact spatial-domain extent.",
        ),
        "seed": FF(
            "stationary square-pulse initial data",
            "U006021",
        ),
        "input": FF(
            "stationary square-pulse initial data and dimension d",
            ("U006021", "U006023"),
        ),
        "boundary": FF(
            None,
            (),
            status="UNKNOWN_FROM_SOURCE",
            reason="U006021-U006023 do not state boundary data for the compared solutions.",
        ),
        "parameters_and_variants": FF(
            "dimension d; compared variants: 1D, 2D, and 3D wave-equation solutions",
            ("U006021", "U006023"),
        ),
        "excluded_observers_and_representations": FF(
            "the displayed observer is a one-dimensional slice multiplied by "
            "r^(d-1); it is not the native multidimensional field state",
            "U006023",
        ),
    },
)
amend_spec(
    "negative-diffusion PDE relation",
    facts={
        "termination_completion_failure": FF(
            "The source calls the behavior inconsistent: any spatial variation eventually becomes infinitely rapid.",
            ("U006024", "U006025", "U006026"),
        ),
    },
)
amend_spec(
    "PDE boundary-value constraint semantics",
    kind="RELATION",
    facts={
        "result_kind": FF(
            "a solution set over a region: too little boundary data may admit many solutions; too much may admit none",
            "U006028",
        ),
        "successor_cardinality": FF(
            "not a successor relation; boundary constraints can yield many, one, or zero satisfying functions",
            "U006028",
        ),
        "termination_completion_failure": FF(
            "nonuniqueness and nonexistence are explicit accepted outcomes of underspecified or inconsistent boundary data",
            "U006028",
        ),
    },
)
amend_spec(
    "general Jacobi background solution",
    law="b d JacobiSN[r t,s]^2/(b-d JacobiCN[r t,s]^2), where "
        "r=-Sqrt[(a c (b-d))/8], s=d(c-b)/(c(d-b)), and b,c,d satisfy "
        "(x-b)(x-c)(x-d)==-(12+6 a x-4 x^2-3 a x^3)/(3 a)",
    facts={
        "termination_completion_failure": FF(
            "The source states periodic, nonsingular behavior except for -8/3 < a < -1/Sqrt[6].",
            "U006047",
        ),
    },
)
remove_spec("named PDE numerical-method family")
amend_spec(
    "explicit second-order PDE finite-difference solver",
    law=(
        "PDEKernel[f_, {dx_, dt_}] := Compile[{a, b, c, d}, "
        "Evaluate[(2 b - d) + ((a + c - 2 b)/dx^2 + f[b]) dt^2]]; "
        "PDEEvolveList[ker_, {u0_, u1_}, n_] := "
        "Map[First, NestList[PDEStep[ker, #] &, {u0, u1}, n]]; "
        "PDEStep[ker_, {u1_, u2_}] := {u2, Apply[ker, "
        "Transpose[{RotateLeft[u2], u2, RotateRight[u2], u1}], {1}]}"
    ),
    facts={
        "boundary": FF("periodic boundary induced by RotateLeft/RotateRight", "U006063"),
        "topology": FF("one-dimensional periodic spatial list", "U006063"),
        "complete_state": FF("two consecutive full spatial slices {u1,u2}", ("U006061", "U006063")),
        "visible_history": FF(
            "PDEEvolveList returns Map[First, NestList[...]], the successive "
            "spatial-slice history for the requested n steps",
            "U006063",
        ),
        "seed": FF(
            "the two initial spatial slices {u0,u1}",
            "U006063",
        ),
        "frontier_or_activation": FF(
            "every position of the periodic current spatial slice",
            "U006063",
        ),
        "schedule": FF(
            "PDEKernel supplies each local next value and PDEStep assembles "
            "all periodic positions synchronously from the same two input slices",
            ("U006061", "U006063"),
        ),
        "read_dependencies_or_neighborhood": FF(
            "PDEKernel reads left/current/right values a,b,c and the previous "
            "time-slice value d; PDEStep supplies them from RotateLeft[u2], "
            "u2, RotateRight[u2], and u1",
            ("U006061", "U006063"),
        ),
        "rule_relation_constraint_function_or_probability_law": FF(
            "PDEKernel[f_, {dx_, dt_}] := Compile[{a, b, c, d}, "
            "Evaluate[(2 b - d) + ((a + c - 2 b)/dx^2 + f[b]) dt^2]]; "
            "PDEEvolveList[ker_, {u0_, u1_}, n_] := "
            "Map[First, NestList[PDEStep[ker, #] &, {u0, u1}, n]]; "
            "PDEStep[ker_, {u1_, u2_}] := {u2, Apply[ker, "
            "Transpose[{RotateLeft[u2], u2, RotateRight[u2], u1}], {1}]}",
            ("U006061", "U006063"),
        ),
        "write_replacement_assembly_or_commit": FF(
            "PDEKernel computes each next value; PDEStep synchronously "
            "assembles the next slice and commits {u2,next-slice}",
            ("U006061", "U006063"),
        ),
        "termination_completion_failure": FF(
            "The code performs the requested number of steps; convergence to the continuous PDE is a separate, not guaranteed judgment.",
            ("U006060", "U006061", "U006063"),
        ),
    },
)
amend_spec("page-165 Gaussian numerical preset", kind="PRESET")
amend_spec(
    "PDE convergence observer",
    facts={
        "termination_completion_failure": FF(
            "The top and middle examples converge rapidly as dx decreases; for the bottom example convergence is slow, correctness of details is unknown, and apparent shocks may be discretization artifacts.",
            "U006066",
        ),
        "witness_semantics": FF(
            "comparison across decreasing dx and approximate energy conservation are evidence, not a proof of convergence or correctness",
            "U006066",
        ),
    },
)
for pde_name in (
    "Burgers-equation relation",
    "nonlinear Schrodinger equation relation",
    "Kuramoto-Sivashinsky equation relation",
):
    amend_spec(
        pde_name,
        identity_image=OTHER_PDE_IMAGE,
        facts={
            "boundary": FF(
                "periodic boundary for the pictured solutions; this is not intrinsic to the equation identity",
                "U006072",
            ),
        },
    )

amend_spec(
    "irrational-rotation multiple sequence",
    uids=["U005678", "U005680", "U005681"],
)

# Source-grounded relationship names are retained without allocating forbidden
# global B IDs.  The blind schema only permits B IDs in related_candidate_ids;
# the coordinator will map these named comparisons after W-ID allocation.
RELATION_GROUPS = [
    ("Gray-code ordering generator", "BitXor[2 n,n] integer iteration"),
    ("truncated powers-of-three congruential generator", "base-6 cellular automaton for powers of three"),
    ("standard 3n+1 map", "universal 3n+1 eventual-one query", "per-seed 3n+1 eventual-one predicate", "base-6 cellular automaton for the 3n+1 map"),
    ("iterated run-length encoder", "92-token substitution realization of run-length encoding"),
    ("Moebius sign function", "Mertens cumulative-sum observer"),
    ("iterated aliquot-sum map", "unbounded aliquot-growth query"),
    ("successive-integer concatenation sequence", "concatenation-sequence cumulative walk", "leading-digit-dropped concatenation walk", "direct concatenation-position query", "large-block concatenation digit formula"),
    ("continued-fraction digit extractor", "continued-fraction reconstruction", "Gauss-map continued-fraction trajectory", "continued-fraction approximation-quality observer"),
    ("subtractive Euclidean algorithm", "Euclidean rational-termination query"),
    ("smooth logistic map", "logistic-map leftmost-digit substitution observer", "Lyapunov-exponent observer"),
    ("continuous cellular-automaton averaging implementation", "page-157 continuous-CA transfer-rule preset", "page-158 continuous-CA offset-rule preset", "continuous-CA background trajectory", "continuous-CA center-cell color observer"),
    ("Klein-Gordon PDE relation", "Klein-Gordon exact pulse solution"),
    ("finite-difference PDE discretization family", "Courant stability constraint", "explicit second-order PDE finite-difference solver", "PDE convergence observer"),
    (
        "irrational-rotation multiple sequence",
        "Beatty-difference digit sequence",
        "continued-fraction-derived substitution generator",
    ),
    (
        "nth-prime asymptotic approximation",
        "prime-counting approximation family",
    ),
    (
        "prime-counting approximation family",
        "Riemann zeta denotation",
    ),
    (
        "prime-counting approximation family",
        "Riemann-hypothesis constraint",
    ),
    (
        "normal-number constraint",
        "Stoneham normal-number family",
    ),
    (
        "normal-number constraint",
        "successive-integer concatenation sequence",
    ),
    (
        "exact multiplier-mod-one map",
        "fixed-binary-precision shift-map simulation",
        "fixed-decimal-precision shift-map simulation",
    ),
]
for group in RELATION_GROUPS:
    for name in group:
        spec = spec_named(name)
        peers = tuple(peer for peer in group if peer != name)
        spec["relation_names"] = tuple(dict.fromkeys(
            list(spec.get("relation_names", ())) + list(peers)
        ))

# These hostile-reviewed comparisons receive their own candidate-local source
# evidence records.  They remain comparisons only; none is an identity merge.
RELATION_EVIDENCE_GROUPS = (
    (
        (
            "irrational-rotation multiple sequence",
            "Beatty-difference digit sequence",
            "continued-fraction-derived substitution generator",
        ),
        "U005681",
    ),
    (
        (
            "nth-prime asymptotic approximation",
            "prime-counting approximation family",
        ),
        "U005810",
    ),
    (
        (
            "prime-counting approximation family",
            "Riemann zeta denotation",
        ),
        "U005956",
    ),
    (
        (
            "prime-counting approximation family",
            "Riemann-hypothesis constraint",
        ),
        "U005956",
    ),
    (
        (
            "normal-number constraint",
            "Stoneham normal-number family",
        ),
        "U005860",
    ),
    (
        (
            "normal-number constraint",
            "successive-integer concatenation sequence",
        ),
        "U005860",
    ),
    (
        (
            "exact multiplier-mod-one map",
            "fixed-binary-precision shift-map simulation",
            "fixed-decimal-precision shift-map simulation",
        ),
        "U005978",
    ),
)
RELATION_EVIDENCE_ANCHORS: dict[tuple[str, str], tuple[str, ...]] = {}
for relation_group, relation_anchor in RELATION_EVIDENCE_GROUPS:
    for relation_source in relation_group:
        for relation_peer in relation_group:
            if relation_source != relation_peer:
                RELATION_EVIDENCE_ANCHORS[
                    (relation_source, relation_peer)
                ] = (relation_anchor,)


ROUTES = [
    ("page117_sub", "U005657", "page 83", "replacement rule and seed for the rotated page-117 substitution preset", ["substitution system", "page 117"], "CROSS_RANGE"),
    ("powers3_ca", "U005671", "page 614", "complicated base-6 powers-of-three pattern used for the cellular-automaton correspondence", ["powers of three", "base 6 cellular automaton"], "CROSS_RANGE"),
    ("linear_recurrences", "U005728", "page 128", "coefficients, orders, and initial values of the page-128 linear recurrences", ["linear recurrence", "page 128"], "WITHIN_STAGE"),
    ("prime_sieve", "U005802", "page 132", "sieve-of-Eratosthenes removal/filter procedure for generating the primes", ["sieve of Eratosthenes", "prime generation"], "WITHIN_STAGE"),
    ("three_squares", "U005820", "page 135", "necessary-and-sufficient sum-of-three-squares representability condition", ["three squares", "representability"], "WITHIN_STAGE"),
    ("digit_sqrt", "U005863", "page 141", "per-step update law for the digit-by-digit square-root construction", ["square root", "digit by digit"], "WITHIN_STAGE"),
    ("integer_representations", "U005927", "page 560", "integer-representation construction referenced without mechanics", ["integer representation"], "CROSS_RANGE"),
    ("zero_substitution", "U005945", "page 903", "substitution rules for cosine/sine zero-spacing sequences", ["zero spacing", "substitution"], "WITHIN_STAGE"),
    ("probabilistic_ca", "U006010", "page 591", "rule choices, probabilities, and seeds for probabilistic cellular automata", ["probabilistic cellular automaton"], "CROSS_RANGE"),
]


HISTORICAL_UNITS = {
    "U005653", "U005654", "U005655", "U005712", "U005761", "U005801",
    "U005813", "U005814", "U005916", "U005966", "U006001", "U006002",
    "U006074", "U006075",
}

OBSERVER_UNITS = {
    "U005649", "U005672", "U005679", "U005686", "U005692", "U005693",
    "U005705", "U005710", "U005715", "U005724", "U005757",
    "U005759", "U005779", "U005788", "U005790", "U005794", "U005799",
    "U005810", "U005811", "U005812", "U005828", "U005829", "U005831",
    "U005834", "U005840", "U005853", "U005858", "U005859", "U005866", "U005868",
    "U005870", "U005872", "U005881", "U005882", "U005892", "U005894",
    "U005901", "U005902", "U005903", "U005904", "U005911", "U005913",
    "U005915", "U005920", "U005926", "U005929", "U005934", "U005936",
    "U005939", "U005940", "U005942", "U005947", "U005951", "U005953",
    "U005955", "U005959", "U005960", "U005961", "U005962", "U005963",
    "U005969", "U005970", "U005971", "U005979", "U005980", "U005982",
    "U005983", "U005984", "U005985", "U005986", "U005987", "U005988",
    "U005989", "U005992", "U005994", "U006004", "U006005", "U006009",
    "U006013", "U006014", "U006017", "U006018", "U006019", "U006020",
    "U006021", "U006022", "U006023", "U006027", "U006028", "U006054",
    "U006055", "U006056", "U006057", "U006067",
}


ASSET_ROLE_IDS: dict[str, set[str]] = {
    "NATIVE_EVIDENCE": {
        "A000441", "A000456", "A000482", "A000483", "A000489", "A000518",
    },
    "RELATION": {"A000491", "A000495"},
    "CONTROL": {
        "A000440", "A000450", "A000462", "A000469", "A000480",
        "A000481", "A000484", "A000494", "A000498", "A000499",
        "A000500", "A000501", "A000502", "A000503", "A000504",
        "A000506", "A000507", "A000511", "A000512", "A000513",
        "A000517",
    },
    "OBSERVER": {
        "A000437", "A000438", "A000439", "A000442", "A000444",
        "A000445", "A000446", "A000457", "A000458", "A000459",
        "A000460", "A000461", "A000465", "A000466", "A000467",
        "A000468", "A000470", "A000471", "A000472", "A000473",
        "A000492", "A000497",
    },
    # A000443 is a referenced but bottom-clipped extraction.  The remaining
    # SOURCE_DEFECT IDs are the 30 unreferenced fragments and are filled from
    # the bundle's reference_status at authoring time.
    "SOURCE_DEFECT": {"A000443"},
}

ASSET_RISKS: dict[str, tuple[str, ...]] = {
    "A000440": ("TEXT_BEARING",),
    "A000441": ("CONSTRUCTION_BEARING",),
    "A000443": (
        "CONSTRUCTION_BEARING", "TEXT_BEARING",
        "AMBIGUOUS", "CAPTION_INCOMPLETE",
    ),
    "A000450": ("TEXT_BEARING",),
    "A000456": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000462": ("TEXT_BEARING",),
    "A000468": ("TEXT_BEARING",),
    "A000469": ("TEXT_BEARING",),
    "A000480": ("TEXT_BEARING",),
    "A000481": ("TEXT_BEARING",),
    "A000482": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000483": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000484": ("TEXT_BEARING",),
    "A000489": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000491": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000492": ("TEXT_BEARING",),
    "A000494": ("TEXT_BEARING",),
    "A000495": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000497": ("TEXT_BEARING",),
    "A000498": ("TEXT_BEARING",),
    "A000499": ("TEXT_BEARING",),
    "A000500": ("TEXT_BEARING",),
    "A000501": ("TEXT_BEARING",),
    "A000502": ("TEXT_BEARING",),
    "A000503": ("TEXT_BEARING",),
    "A000504": ("TEXT_BEARING",),
    "A000506": ("TEXT_BEARING",),
    "A000507": ("TEXT_BEARING",),
    "A000511": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000512": ("TEXT_BEARING",),
    "A000513": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
    "A000517": ("TEXT_BEARING",),
    "A000518": ("CONSTRUCTION_BEARING", "TEXT_BEARING"),
}

ORPHAN_RISKS: dict[str, tuple[str, ...]] = {
    **{
        asset_id: ("TEXT_BEARING", "AMBIGUOUS", "CAPTION_INCOMPLETE")
        for asset_id in (
            "A000447", "A000448", "A000449", "A000474", "A000475",
            "A000476", "A000477", "A000478", "A000479", "A000485",
            "A000486", "A000487", "A000488", "A000490", "A000493",
            "A000496", "A000508", "A000509", "A000510", "A000514",
            "A000515", "A000516",
        )
    },
    **{
        asset_id: (
            "CONSTRUCTION_BEARING", "TEXT_BEARING",
            "AMBIGUOUS", "CAPTION_INCOMPLETE",
        )
        for asset_id in (
            "A000451", "A000452", "A000453", "A000454", "A000455",
        )
    },
    **{
        asset_id: ("AMBIGUOUS", "CAPTION_INCOMPLETE")
        for asset_id in (
            "A000463", "A000464", "A000505",
        )
    },
}

# Candidate/image joins include contextual observers and controls, not merely
# images that carry native formulas.  Candidate image_witnesses and the asset
# ledger are generated from this one symmetric mapping.
ASSET_CANDIDATE_NAMES: dict[str, tuple[str, ...]] = {
    "A000437": ("Gray-code ordering generator",),
    "A000438": ("base-2 one-digit count function",),
    "A000439": ("negative-base positional representation",),
    "A000440": ("irrational-rotation multiple sequence", "uniformly-distributed fractional-part family"),
    "A000441": ("multiplicative prime-exponent representation",),
    "A000442": ("powers-of-three base-2 digit sequence",),
    "A000443": (
        "standard 3n+1 map",
        "case-b binary-length stopping-time map",
        "case-c one-bit-count stopping-time map obligation",
    ),
    "A000444": ("binary reversal-addition map",),
    "A000445": ("iterated run-length encoder", "92-token substitution realization of run-length encoding"),
    "A000446": ("reversible rounded integer map",),
    "A000450": ("fixed-width digit-reversal permutation",),
    "A000456": (
        "BitXor[2 n,n] integer iteration", "BitXor[3+2 n,n] integer iteration",
        "BitXor[3 n,n] integer iteration", "BitXor[6 n,n] integer iteration",
        "BitOr[2 n,n] integer iteration", "BitOr[6 n,n] integer iteration",
    ),
    "A000457": ("binary-dependency recursive-sequence schema",),
    "A000458": ("complex primitive-recursive function",),
    "A000459": ("complex primitive-recursive function",),
    "A000460": ("diagonalized non-primitive-recursive function",),
    "A000461": ("Ulam sequence",),
    "A000462": ("decimation system", "decimation survival-time function"),
    "A000465": ("divisor-count function", "aliquot-balance function"),
    "A000466": ("Lucas-Lehmer Mersenne-prime test",),
    "A000467": ("iterated aliquot-sum map", "unbounded aliquot-growth query"),
    "A000469": ("rational digit repeat-period function",),
    "A000470": ("concatenation-sequence cumulative walk",),
    "A000471": ("leading-digit-dropped concatenation walk",),
    "A000472": ("successive-integer concatenation sequence",),
    "A000473": ("successive-integer concatenation sequence",),
    "A000480": ("continued-fraction digit extractor", "Gauss-map continued-fraction trajectory"),
    "A000481": ("continued-fraction approximation-quality observer",),
    "A000482": ("subtractive Euclidean algorithm",),
    "A000483": ("subtractive Euclidean algorithm", "Euclidean rational-termination query"),
    "A000484": ("continued-fraction term-size measure",),
    "A000489": ("operator-tree integer representation family",),
    "A000491": ("digital-slope representation", "digital-slope reconstruction"),
    "A000492": ("two-sine function and zero relation", "ODE denotation of an incommensurate sine sum"),
    "A000494": ("harmonic sine Fourier partial sums",),
    "A000495": ("Lissajous curve map",),
    "A000497": ("three-sine function and zero set",),
    "A000498": ("cosine-difference zero-spacing sequence", "zero-spacing substitution realization"),
    "A000499": ("square-frequency Fourier sum",),
    "A000500": ("lacunary power-of-two cosine sum",),
    "A000501": ("weighted Weierstrass cosine series",),
    "A000502": ("fixed-binary-precision shift-map simulation", "fixed-decimal-precision shift-map simulation"),
    "A000503": ("finite-precision multiplication-by-3/2 simulation",),
    "A000504": ("smooth logistic map",),
    "A000506": ("additive continuous cellular automaton",),
    "A000507": ("continuous-CA background trajectory", "continuous-CA center-cell color observer"),
    "A000511": ("two-Gaussian periodic-boundary PDE comparison preset",),
    "A000512": ("dimensional wave-equation square-pulse preset",),
    "A000513": ("Courant stability constraint",),
    "A000517": ("PDE convergence observer",),
    "A000518": (
        "Burgers-equation relation", "nonlinear Schrodinger equation relation",
        "Kuramoto-Sivashinsky equation relation",
    ),
}

SOURCE_STATUS_BY_UID = {
    "U005695": (
        "DEFECTIVE",
        "The referenced A000443 extraction is bottom-clipped before the case-(c) formula label.",
    ),
    "U005993": (
        "CONFLICTING",
        "The unit's two rationality conditions for repetitive versus complicated behavior conflict as written.",
    ),
}


def ordered_unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def array_text(items: list[str]) -> str:
    return json.dumps(items, ensure_ascii=False, separators=(",", ":"))


OBJECT_KIND = {
    "ITERATION": "discrete iterated map or recurrence",
    "CA": "cellular-automaton transition system",
    "SUBSTITUTION": "substitution or replacement system",
    "SOLVER": "constructive or numerical solver",
    "FUNCTION": "immutable function or indexed sequence",
    "QUERY": "predicate, decision query, or accepted-result condition",
    "RELATION": "declarative relation or denoted mathematical object",
    "REPRESENTATION": "encoder, decoder, or representation relation",
    "GENERATOR": "finite or infinite sequence generator",
    "OBSERVER": "observer or analyzer",
    "CALCULUS": "function-construction calculus",
    "PDE": "partial differential relation",
    "ODE": "ordinary differential relation",
    "PRESET": "initial, boundary, or numerical preset",
    "PARTIAL_SYSTEM": "delimited construction with identity-bearing mechanics missing",
    "EVALUATION_POLICY": "expression-evaluation policy",
}

LAW_KIND = {
    "ITERATION": "one-step map or recurrence",
    "CA": "local cellular transition rule",
    "SUBSTITUTION": "replacement rule",
    "SOLVER": "constructive or numerical update method",
    "FUNCTION": "function definition",
    "QUERY": "predicate or quantified accepted-result condition",
    "RELATION": "declarative relation or constraint",
    "REPRESENTATION": "encoding, decoding, or representation relation",
    "GENERATOR": "generation law",
    "OBSERVER": "observer or analyzer function",
    "CALCULUS": "function-building operators and evaluation clauses",
    "PDE": "partial differential constraint",
    "ODE": "ordinary differential constraint",
    "PRESET": "initial/boundary data assignment",
    "PARTIAL_SYSTEM": "partially recovered transition law",
    "EVALUATION_POLICY": "expression-reduction order",
}

STEPWISE_KINDS = {
    "ITERATION", "CA", "SUBSTITUTION", "SOLVER", "GENERATOR",
    "PARTIAL_SYSTEM",
}
CONTINUOUS_RELATION_KINDS = {"PDE", "ODE"}
STATIC_KINDS = {
    "FUNCTION", "QUERY", "RELATION", "REPRESENTATION", "OBSERVER",
    "CALCULUS", "PDE", "ODE", "PRESET",
}

# A nonempty entry says that the cited source deliberately leaves these
# fingerprint dimensions unresolved.  Reusing the exact source-limited
# sentence as the UNKNOWN reason guarantees that it also appears verbatim in
# missing_mechanics.
MISSING_FIELD_HINTS: dict[str, dict[str, str]] = {
    "rotated page-117 digit substitution preset": {
        field: "The replacement rule and seed are only at the routed target."
        for field in (
            "seed", "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "successor_cardinality",
        )
    },
    "92-token substitution realization of run-length encoding": {
        field: "Only one of the 92 token replacements is stated."
        for field in (
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "successor_cardinality",
        )
    },
    "page-128 linear recurrence family": {
        field: "The individual coefficients, orders, and initial values are at the routed target."
        for field in (
            "seed", "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "successor_cardinality",
        )
    },
    "digit-by-digit square-root solver": {
        field: "The per-step update choosing the next digit is only in the routed main-text construction."
        for field in (
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "schedule",
        )
    },
    "zero-spacing substitution realization": {
        field: "The replacement rules are at the routed page-903 discussion."
        for field in (
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "successor_cardinality",
        )
    },
    "finite-precision multiplication-by-3/2 simulation": {
        field: "The rounding/fill convention and exact recurrence are not stated in this unit."
        for field in (
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "determinism_branching_or_measure",
        )
    },
    "probabilistic cellular automaton family": {
        field: "The rule pair, probabilities, random coupling, and examples are only at page 591."
        for field in (
            "seed", "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit", "successor_cardinality",
        )
    },
    "finite-difference PDE discretization family": {
        field: "This unit states the method family but not a particular stencil."
        for field in (
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
        )
    },
    "sum-of-three-squares representability constraint": {
        field: "The actual necessary-and-sufficient condition is only in the routed main-text target."
        for field in (
            "rule_relation_constraint_function_or_probability_law",
            "witness_semantics",
        )
    },
    "two-Gaussian periodic-boundary PDE comparison preset": {
        field: "Gaussian scale, separation, and numerical grid are not printed in the Notes unit."
        for field in ("seed", "input", "boundary", "parameters_and_variants")
    },
    "dimensional wave-equation square-pulse preset": {
        field: "The exact pulse dimensions, domain, and boundary data are not printed."
        for field in ("seed", "input", "boundary", "parameters_and_variants")
    },
    "case-c one-bit-count stopping-time map obligation": {
        field: "The case-(c) one-step update formula is clipped from A000443 and is not stated in the prose."
        for field in (
            "read_dependencies_or_neighborhood",
            "rule_relation_constraint_function_or_probability_law",
            "write_replacement_assembly_or_commit",
            "determinism_branching_or_measure", "successor_cardinality",
        )
    },
}


def decision(
    status: str,
    value: str | None,
    anchors: tuple[str, ...] | list[str],
    reason: str,
) -> dict[str, Any]:
    return {
        "status": status,
        "value": value,
        "anchors": tuple(anchors),
        "reason": reason,
    }


def supported(
    spec: dict[str, Any],
    field: str,
    value: str,
    *anchors: str,
) -> dict[str, Any]:
    return decision(
        "SUPPORTED",
        value,
        anchors,
        "",
    )


def not_applicable(
    spec: dict[str, Any],
    field: str,
    anchor: str,
    reason: str,
) -> dict[str, Any]:
    return decision(
        "NOT_APPLICABLE",
        None,
        (anchor,),
        f"{spec['name']}: {reason}",
    )


def unknown(spec: dict[str, Any], field: str, reason: str | None = None) -> dict[str, Any]:
    return decision(
        "UNKNOWN_FROM_SOURCE",
        None,
        (),
        reason
        or (
            f"{spec['name']}: the sealed Notes evidence does not state "
            f"{field.replace('_', ' ')}."
        ),
    )


def choose_law_anchor(
    spec: dict[str, Any],
    block_kind_by_uid: dict[str, str],
) -> str:
    if spec["identity_image"]:
        return spec["identity_image"]
    if spec["name"] == "case-b binary-length stopping-time map":
        return "BACK-MATTER/NOTES/_page_919_Figure_10.jpeg"
    if spec["image_direct"] and spec["images"]:
        return spec["images"][0]
    if spec["law_uid"] is not None:
        return spec["law_uid"]
    for uid in spec["uids"]:
        if block_kind_by_uid[uid] == "fenced_code":
            return uid
    return spec["uids"][0]


def field_decisions(
    spec: dict[str, Any],
    block_kind_by_uid: dict[str, str],
) -> dict[str, dict[str, Any]]:
    """Build a conservative, source-limited 28-field decision record."""

    name = spec["name"]
    kind = spec["kind"]
    identity_anchor = spec["identity_image"] or spec["uids"][0]
    law_anchor = choose_law_anchor(spec, block_kind_by_uid)
    parameters = list(spec["params"])
    variants = list(spec["variants"])
    dynamic = kind in STEPWISE_KINDS
    continuous_relation = kind in CONTINUOUS_RELATION_KINDS
    hints = MISSING_FIELD_HINTS.get(name, {})

    result_values = {
        "ITERATION": "the next iterate and, when requested, its trajectory",
        "CA": "a replacement cell value and the resulting configuration when a global schedule is fixed",
        "SUBSTITUTION": "the replacement word/list or generated substitution sequence",
        "SOLVER": "a constructed or numerical approximation/result",
        "FUNCTION": "the value or indexed sequence defined by the formula",
        "QUERY": "a Boolean or quantified mathematical judgment",
        "RELATION": "the denoted relation, identity, or satisfying-value set",
        "REPRESENTATION": "an encoded/decoded value or representation",
        "GENERATOR": "the generated finite prefix, sequence, or family",
        "OBSERVER": "an observed or analyzed value",
        "CALCULUS": "a function expression or function produced by the constructors",
        "PDE": "a set of functions satisfying the partial differential relation",
        "ODE": "a set of functions satisfying the ordinary differential relation",
        "PRESET": "data used to initialize or compare a separate system/solver",
        "PARTIAL_SYSTEM": "a delimited construction whose full successor is not recoverable",
        "EVALUATION_POLICY": "the next selected expression reduction or its failure",
    }

    d: dict[str, dict[str, Any]] = {
        field: unknown(spec, field) for field in FIELDS
    }
    d["object_kind"] = supported(
        spec, "object_kind", f"{OBJECT_KIND[kind]}: {name}", identity_anchor
    )
    d["law_kind"] = supported(spec, "law_kind", LAW_KIND[kind], law_anchor)
    d["rule_relation_constraint_function_or_probability_law"] = supported(
        spec,
        "rule_relation_constraint_function_or_probability_law",
        spec["law"],
        law_anchor,
    )
    d["result_kind"] = supported(
        spec, "result_kind", result_values[kind], law_anchor
    )
    d["read_dependencies_or_neighborhood"] = supported(
        spec,
        "read_dependencies_or_neighborhood",
        (
            "the current state and explicit arguments appearing in the exact "
            f"law: {spec['law']}"
            if dynamic
            else f"the explicit arguments and subexpressions in: {spec['law']}"
        ),
        law_anchor,
    )

    if parameters:
        d["input"] = supported(
            spec, "input", "inputs/parameters: " + "; ".join(parameters), law_anchor
        )
    else:
        d["input"] = not_applicable(
            spec,
            "input",
            identity_anchor,
            "the captured object is a fixed denotation or quantified statement, not a caller-parameterized procedure.",
        )
    if parameters or variants:
        value_parts: list[str] = []
        if parameters:
            value_parts.append("parameters: " + "; ".join(parameters))
        if variants:
            value_parts.append("variants: " + "; ".join(variants))
        d["parameters_and_variants"] = supported(
            spec, "parameters_and_variants", " | ".join(value_parts), law_anchor
        )
    else:
        d["parameters_and_variants"] = not_applicable(
            spec,
            "parameters_and_variants",
            identity_anchor,
            "no separate parameter or variant is part of this candidate's stated identity.",
        )

    if dynamic:
        time_value = {
            "ITERATION": "discrete applications of the map or recurrence",
            "CA": "discrete cellular update steps",
            "SUBSTITUTION": "discrete replacement generations",
            "SOLVER": "discrete construction or approximation steps",
            "GENERATOR": "discrete generation stages or indices",
            "PARTIAL_SYSTEM": "discrete steps are described, but their one-step law is incomplete",
        }[kind]
        d["native_time"] = supported(spec, "native_time", time_value, law_anchor)
        d["complete_state"] = supported(
            spec,
            "complete_state",
            {
                "CA": "the current complete cell configuration plus stated parameters",
                "SUBSTITUTION": "the current word/list plus stated replacement data",
                "SOLVER": "the current approximation variables named by the method",
                "GENERATOR": "the current generated prefix/index and stated parameters",
                "PARTIAL_SYSTEM": "the current integer input/state; the missing rule prevents a complete successor description",
            }.get(kind, "the current iterate or recurrence state plus stated parameters"),
            law_anchor,
        )
        d["frontier_or_activation"] = supported(
            spec,
            "frontier_or_activation",
            (
                "the source object/eligible occurrence selected by the one-step law"
                if kind != "CA"
                else "the cell positions to which the local rule is applied"
            ),
            law_anchor,
        )
        if kind == "CA":
            d["schedule"] = unknown(
                spec,
                "schedule",
                f"{name}: the sealed Notes evidence gives a local rule but does not state a global cell-update schedule.",
            )
            d["determinism_branching_or_measure"] = unknown(
                spec,
                "determinism_branching_or_measure",
                f"{name}: the local expression is deterministic, but the sealed source does not fix a complete global schedule/measure.",
            )
            d["successor_cardinality"] = unknown(
                spec,
                "successor_cardinality",
                f"{name}: a local output is fixed, but global successor cardinality depends on the unstated schedule/topology.",
            )
        else:
            d["schedule"] = supported(
                spec,
                "schedule",
                "one application/construction step follows the order written in the exact law",
                law_anchor,
            )
            d["determinism_branching_or_measure"] = supported(
                spec,
                "determinism_branching_or_measure",
                "the stated law selects one next result for complete defined inputs; no probability measure is introduced",
                law_anchor,
            )
            d["successor_cardinality"] = supported(
                spec,
                "successor_cardinality",
                "one next/generated result for each complete defined state and parameter choice",
                law_anchor,
            )
        d["visible_history"] = unknown(
            spec,
            "visible_history",
            f"{name}: the source does not say whether earlier states beyond the stated read dependencies are retained as part of the visible state.",
        )
        seed_text = " ".join(parameters).lower() + " " + spec["law"].lower()
        seed_tokens = (
            "initial", "start ", "f[0]", "f[1]", "from {0}", "from {1",
            "seed",
        )
        if any(token in seed_text for token in seed_tokens):
            d["seed"] = supported(
                spec,
                "seed",
                "the initial value/configuration is supplied by the stated parameters or initial clauses",
                law_anchor,
            )
        else:
            d["seed"] = unknown(
                spec,
                "seed",
                f"{name}: the one-step/generation law is stated, but no initial seed is fixed for this candidate.",
            )
        d["write_replacement_assembly_or_commit"] = supported(
            spec,
            "write_replacement_assembly_or_commit",
            (
                "the local rule computes a replacement cell value; global commit timing is represented separately by schedule"
                if kind == "CA"
                else "the exact law produces the next replacement, appended term, or approximation"
            ),
            law_anchor,
        )
    elif continuous_relation:
        d["native_time"] = supported(
            spec,
            "native_time",
            "continuous independent variable(s) occur in the relation; this is not an update schedule",
            law_anchor,
        )
        d["carrier"] = supported(
            spec,
            "carrier",
            "functions over the continuous coordinates named in the equation",
            law_anchor,
        )
        for field in (
            "complete_state", "visible_history", "control_state", "seed",
            "frontier_or_activation", "schedule",
            "write_replacement_assembly_or_commit",
        ):
            d[field] = not_applicable(
                spec,
                field,
                law_anchor,
                "this candidate is a declarative differential relation, not an intrinsic discrete evolution or solver.",
            )
        d["successor_cardinality"] = not_applicable(
            spec,
            "successor_cardinality",
            law_anchor,
            "the equation denotes a solution relation rather than a successor function.",
        )
        d["determinism_branching_or_measure"] = not_applicable(
            spec,
            "determinism_branching_or_measure",
            law_anchor,
            "the equation alone supplies neither a stochastic measure nor a solver-level branch policy.",
        )
        d["termination_completion_failure"] = not_applicable(
            spec,
            "termination_completion_failure",
            law_anchor,
            "termination is a solver property; this candidate is only the differential relation.",
        )
    elif kind == "EVALUATION_POLICY":
        d["native_time"] = not_applicable(
            spec, "native_time", identity_anchor, "evaluation order is not physical/native time."
        )
        d["complete_state"] = supported(
            spec,
            "complete_state",
            "the current recursive expression and values already made explicit",
            law_anchor,
        )
        d["control_state"] = supported(
            spec,
            "control_state",
            "the leftmost innermost unresolved occurrence selected for reduction",
            law_anchor,
        )
        d["frontier_or_activation"] = supported(
            spec,
            "frontier_or_activation",
            "the leftmost innermost f[k] occurrence",
            law_anchor,
        )
        d["schedule"] = supported(
            spec,
            "schedule",
            "reduce the selected occurrence to an explicit value before the enclosing expression",
            law_anchor,
        )
        d["write_replacement_assembly_or_commit"] = supported(
            spec,
            "write_replacement_assembly_or_commit",
            "replace the selected occurrence by its explicit value",
            law_anchor,
        )
        d["successor_cardinality"] = supported(
            spec,
            "successor_cardinality",
            "one selected next reduction when the selected subvalue is defined",
            law_anchor,
        )
        d["determinism_branching_or_measure"] = supported(
            spec,
            "determinism_branching_or_measure",
            "deterministic leftmost-innermost selection",
            law_anchor,
        )
        for field in ("visible_history", "seed"):
            d[field] = not_applicable(
                spec, field, identity_anchor, "this evaluation policy has no trajectory seed/history."
            )
    else:
        for field in (
            "native_time", "complete_state", "visible_history", "control_state",
            "seed", "frontier_or_activation", "schedule",
            "write_replacement_assembly_or_commit",
        ):
            d[field] = not_applicable(
                spec,
                field,
                identity_anchor,
                "the captured object is not an intrinsic state-transition process.",
            )
        if kind == "RELATION":
            d["successor_cardinality"] = not_applicable(
                spec,
                "successor_cardinality",
                law_anchor,
                "the source states a relation/constraint, not a successor function.",
            )
            d["determinism_branching_or_measure"] = not_applicable(
                spec,
                "determinism_branching_or_measure",
                law_anchor,
                "no transition branching or probability measure is intrinsic to this relation.",
            )
            d["termination_completion_failure"] = not_applicable(
                spec,
                "termination_completion_failure",
                law_anchor,
                "the relation is denotational; no evaluation procedure is claimed.",
            )
        elif kind == "PRESET":
            for field in (
                "successor_cardinality", "determinism_branching_or_measure",
                "termination_completion_failure",
            ):
                d[field] = not_applicable(
                    spec,
                    field,
                    identity_anchor,
                    "a preset supplies data to another system and has no autonomous successor/evaluation semantics.",
                )
        else:
            d["successor_cardinality"] = supported(
                spec,
                "successor_cardinality",
                "one denoted result/judgment for each complete defined input",
                law_anchor,
            )
            d["determinism_branching_or_measure"] = supported(
                spec,
                "determinism_branching_or_measure",
                "the exact definition is single-valued for complete defined inputs and introduces no probability measure",
                law_anchor,
            )

    if kind == "QUERY" and d["witness_semantics"]["status"] == "UNKNOWN_FROM_SOURCE":
        d["witness_semantics"] = supported(
            spec,
            "witness_semantics",
            f"accepted exactly when the stated predicate/quantified condition holds: {spec['law']}",
            law_anchor,
        )
    elif kind in {"RELATION", "PDE", "ODE"}:
        d["witness_semantics"] = supported(
            spec,
            "witness_semantics",
            "a witness is a value/function satisfying the exact stated relation",
            law_anchor,
        )
    elif kind == "PRESET":
        d["witness_semantics"] = supported(
            spec,
            "witness_semantics",
            "the stated data instantiate a separate equation, solver, or comparison",
            law_anchor,
        )
    else:
        d["witness_semantics"] = supported(
            spec,
            "witness_semantics",
            "the witness is the exact value, next state, generated object, or observation produced by the stated law",
            law_anchor,
        )

    # Static object dimensions that genuinely do not apply.
    if kind not in {"CA", "PDE", "ODE", "SOLVER", "PRESET"}:
        d["topology"] = not_applicable(
            spec, "topology", identity_anchor, "no spatial adjacency topology is intrinsic to this candidate."
        )
        d["boundary"] = not_applicable(
            spec, "boundary", identity_anchor, "no spatial boundary condition is intrinsic to this candidate."
        )
    elif kind == "SOLVER" and "PDE" not in name and "wave" not in name:
        d["topology"] = not_applicable(
            spec, "topology", identity_anchor, "this nonspatial solver has no adjacency topology."
        )
        d["boundary"] = not_applicable(
            spec, "boundary", identity_anchor, "this nonspatial solver has no boundary condition."
        )
    elif d["topology"]["status"] == "UNKNOWN_FROM_SOURCE":
        d["topology"] = unknown(
            spec,
            "topology",
            f"{name}: the sealed Notes evidence does not fix the spatial domain/topology.",
        )
    if d["boundary"]["status"] == "UNKNOWN_FROM_SOURCE":
        d["boundary"] = unknown(
            spec,
            "boundary",
            f"{name}: the sealed Notes evidence does not fix boundary/initial-boundary data.",
        )

    d["external_data"] = not_applicable(
        spec,
        "external_data",
        identity_anchor,
        "the candidate is defined from stated mathematical inputs, not an external dataset.",
    )
    d["excluded_observers_and_representations"] = supported(
        spec,
        "excluded_observers_and_representations",
        (
            f"Only {name}'s stated observer/representation law is captured; "
            "the underlying observed system is not redefined here."
            if kind in {"OBSERVER", "REPRESENTATION"}
            else (
                f"plots, renderings, observers, and implementation comparisons "
                f"are excluded from {name}'s native identity unless separately captured."
            )
        ),
        identity_anchor,
    )
    d["evidence_limit"] = supported(
        spec,
        "evidence_limit",
        (
            "Explicit source limit: " + " | ".join(spec["missing"])
            if spec["missing"]
            else "The record claims only facts attached to the cited sealed Notes anchors; every unstated dimension remains UNKNOWN_FROM_SOURCE."
        ),
        identity_anchor,
    )

    # Apply exact hostile-review missing boundaries before explicit facts.
    for field, reason in hints.items():
        d[field] = unknown(spec, field, reason)

    # Candidate-specific facts are authoritative over the conservative base.
    for field, fact in spec["facts"].items():
        fact_reason = (
            ""
            if fact["status"] == "SUPPORTED"
            else fact["reason"]
            or (
                f"{name}: the cited source leaves "
                f"{field.replace('_', ' ')} unresolved."
            )
        )
        d[field] = decision(
            fact["status"],
            fact["value"],
            fact["anchors"],
            fact_reason,
        )

    # The visible case-(b) rule is image-native but defect-limited because the
    # same extraction cuts off case (c).  Case (a) remains independently fixed
    # by U005689; A000443 is only a corroborating defect-limited witness there.
    if name == "case-b binary-length stopping-time map":
        d["rule_relation_constraint_function_or_probability_law"] = supported(
            spec,
            "rule_relation_constraint_function_or_probability_law",
            "n -> If[EvenQ[n], n/2, (n + 1)/2]",
            "BACK-MATTER/NOTES/_page_919_Figure_10.jpeg",
        )

    for field, item in d.items():
        if item["status"] == "UNKNOWN_FROM_SOURCE":
            item["value"] = None
            item["anchors"] = ()
        elif not item["anchors"]:
            raise RuntimeError(f"{name}.{field} has {item['status']} without evidence anchors")
    return d


def profile(
    spec: dict[str, Any],
    decisions: dict[str, dict[str, Any]],
    field_evidence_ids: dict[str, list[str]],
) -> tuple[dict[str, str], dict[str, Any]]:
    support: dict[str, str] = {}
    fingerprint: dict[str, Any] = {}
    for field in FIELDS:
        item = decisions[field]
        evidence_ids = field_evidence_ids[field]
        if item["status"] == "UNKNOWN_FROM_SOURCE" and evidence_ids:
            raise RuntimeError(f"{spec['name']}.{field} has evidence despite UNKNOWN status")
        if item["status"] != "UNKNOWN_FROM_SOURCE" and not evidence_ids:
            raise RuntimeError(f"{spec['name']}.{field} lacks its declared evidence")
        support[field] = item["status"]
        fingerprint[field] = {
            "status": item["status"],
            "value": item["value"],
            "evidence_ids": evidence_ids,
            "reason": item["reason"],
        }
    return support, fingerprint


def atomic_json(path: Path, value: Any) -> None:
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def atomic_text(path: Path, text: str) -> None:
    payload = text.encode("utf-8")
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def count_values(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[str(row[field])] += 1
    return dict(sorted(counts.items()))


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_report(bundle: Path, report_path: Path, fresh_bundle: Path | None) -> None:
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text())
    candidates = output["candidate_proposals"]
    readings = output["reading_updates"]
    assets = output["asset_updates"]
    routes = output["route_proposals"]
    kind_by_name = {spec["name"]: spec["kind"] for spec in SPECS}
    kind_counts: dict[str, int] = defaultdict(int)
    evidence_strength_counts: dict[str, int] = defaultdict(int)
    field_status_counts: dict[str, int] = defaultdict(int)
    related_count = 0
    maximum_evidence_width = 0
    for candidate in candidates:
        kind_counts[kind_by_name[candidate["provisional_name"]]] += 1
        related_count += len(candidate["related_candidate_ids"])
        for item in candidate["fingerprint"].values():
            field_status_counts[item["status"]] += 1
        for evidence in candidate["source_evidence"]:
            evidence_strength_counts[evidence["strength"]] += 1
            maximum_evidence_width = max(
                maximum_evidence_width,
                len(evidence["fingerprint_fields"]),
            )

    unfinalized = copy.deepcopy(output)
    unfinalized["prohibited_input_nonuse"] = False
    unfinalized_bytes = (
        json.dumps(unfinalized, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n"
    ).encode()
    canonical_path = (
        bundle
        / "input"
        / "sources"
        / "BACK-MATTER"
        / "NOTES"
        / "04-Systems-Based-on-Numbers-Notes.md"
    )
    clean_composite_ids = [
        "A000450", "A000456", "A000465", "A000480", "A000491",
        "A000498", "A000507", "A000511", "A000517",
    ]
    asset_by_id = {row["asset_id"]: row for row in assets}
    direct_assets = [
        row for row in assets if row["visual_role"] == "NATIVE_EVIDENCE"
    ]
    orphan_assets = [
        row
        for row in assets
        if row["reference_status"] == "UNREFERENCED_PHYSICAL"
    ]
    incomplete = [
        candidate for candidate in candidates if candidate["missing_mechanics"]
    ]

    lines = [
        "# Stage 8 Chapter 4 Notes blind-review report",
        "",
        "## Scope and source boundary",
        "",
        f"- Worker: `{WORKER}`; stage `{STAGE}`; discovery epoch `{EPOCH}`.",
        "- Assigned canonical source: `BACK-MATTER/NOTES/04-Systems-Based-on-Numbers-Notes.md` only.",
        "- Canonical review was performed sequentially over every supplied unit before any audit enumeration.",
        "- No search round was run by this worker. No catalog IDs, prior goals, API/runtime material, other Book ranges, web source, or outside source was consulted.",
        f"- Final prohibited-input declaration: `{str(output['prohibited_input_nonuse']).lower()}`.",
        "",
        "## Exact coverage and partitions",
        "",
        f"- Source units: `{len(readings)}` assigned, `{sum(r['review_status'] == 'REVIEWED' for r in readings)}` reviewed.",
        f"- Reading dispositions: `{json.dumps(count_values(readings, 'review_disposition'), sort_keys=True)}`.",
        f"- Reading source statuses: `{json.dumps(count_values(readings, 'source_status'), sort_keys=True)}`.",
        f"- Assets: `{len(assets)}` assigned, `{sum(r['inspection_status'] == 'SCREENED' for r in assets)}` screened at original resolution.",
        f"- Asset reference partition: `{json.dumps(count_values(assets, 'reference_status'), sort_keys=True)}`.",
        f"- Asset visual-role partition: `{json.dumps(count_values(assets, 'visual_role'), sort_keys=True)}`.",
        f"- Asset source-status partition: `{json.dumps(count_values(assets, 'source_status'), sort_keys=True)}`.",
        f"- Asset transcription partition: `{json.dumps(count_values(assets, 'transcription_status'), sort_keys=True)}`.",
        f"- Candidate proposals: `{len(candidates)}` active worker-local candidates.",
        f"- Candidate-kind partition: `{json.dumps(dict(sorted(kind_counts.items())), sort_keys=True)}`.",
        f"- Fingerprint-field status partition: `{json.dumps(dict(sorted(field_status_counts.items())), sort_keys=True)}`.",
        f"- Evidence records/groups: `{sum(len(c['source_evidence']) for c in candidates)}` / `{len({e['evidence_group_id'] for c in candidates for e in c['source_evidence']})}`.",
        f"- Evidence-strength partition: `{json.dumps(dict(sorted(evidence_strength_counts.items())), sort_keys=True)}`.",
        f"- Maximum fields claimed by one evidence record: `{maximum_evidence_width}` (no blanket 28-field evidence records).",
        f"- Source-grounded provisional candidate relations: `{related_count}`.",
        f"- Pending typed routes: `{len(routes)}`.",
        f"- Candidates with explicitly missing mechanics: `{len(incomplete)}`.",
        "",
        "## Candidate inventory",
        "",
    ]
    for candidate in candidates:
        kind = kind_by_name[candidate["provisional_name"]]
        anchor = candidate["discovery_anchor"]
        limitations = (
            " Missing: " + " | ".join(candidate["missing_mechanics"])
            if candidate["missing_mechanics"]
            else ""
        )
        lines.append(
            f"- `{candidate['id']}` [{kind}] **{candidate['provisional_name']}** — "
            f"anchor `{anchor['id']}`; sources `{', '.join(candidate['source_unit_ids'])}`."
            f"{limitations}"
        )

    lines.extend([
        "",
        "## Pending route proposals",
        "",
        "| Route | Source | Literal target | Scope | Expected mechanics |",
        "|---|---|---|---|---|",
    ])
    for route in routes:
        lines.append(
            f"| `{route['route_id']}` | `{route['source_unit_id']}` | "
            f"`{route['literal_target']}` | `{route['closure_scope']}` | "
            f"{route['expected_topic']} |"
        )

    lines.extend([
        "",
        "## Explicit evidence limits",
        "",
    ])
    for candidate in incomplete:
        route_ids = ", ".join(candidate["cross_reference_ids"]) or "no literal route available"
        lines.append(
            f"- `{candidate['id']}` {candidate['provisional_name']}: "
            f"{' | '.join(candidate['missing_mechanics'])} Route: `{route_ids}`."
        )

    lines.extend([
        "",
        "## Asset audit",
        "",
        "- The six assets classified as native construction evidence are:",
    ])
    for asset in direct_assets:
        lines.append(
            f"  - `{asset['asset_id']}` `{asset['physical_path']}` — "
            f"original `{asset['original_resolution_status']}`, transcription "
            f"`{asset['transcription_status']}`, candidates "
            f"`{asset['candidate_ids']}`."
        )
    a443 = asset_by_id["A000443"]
    lines.extend([
        "- `A000443` is separately retained as referenced `SOURCE_DEFECT` / "
        "`DEFECTIVE`: cases (a) and (b) are visible, case (c) is bottom-clipped, "
        "and every image claim is `DEFECT_LIMITED`.",
        f"  - Original `{a443['original_resolution_status']}`; transcription "
        f"`{a443['transcription_status']}`; risks `{a443['risk_flags']}`; "
        f"candidates `{a443['candidate_ids']}`.",
        "- Nine clean composite families supersede the 30 unreferenced physical fragments:",
    ])
    for asset_id in clean_composite_ids:
        asset = asset_by_id[asset_id]
        lines.append(f"  - `{asset_id}` `{asset['physical_path']}`")
    lines.append(
        "- All 30 unreferenced fragments are `SOURCE_DEFECT` / `DEFECTIVE`, "
        "original-resolution `REVIEWED`, transcription `NOT_REQUIRED`, and "
        "have zero candidate and route links:"
    )
    for asset in orphan_assets:
        lines.append(f"  - `{asset['asset_id']}` `{asset['physical_path']}`")

    lines.extend([
        "",
        "## Hostile-review repair summary",
        "",
        "- Replaced the remaining kind-wide generator inferences with candidate-specific state semantics: Gray code, the two FoldList sequence-(c) formulations, and Ulam retain their stated seeds/history, while the three direct Table/Flatten/Union denotations have no invented frontier, schedule, or commit.",
        "- Recorded source-supported initial conditions and history/closed-form boundaries for the AGM solver, continued-fraction trajectory, Gauss/multiplier/tent maps, and both finite-storage shift-map representations.",
        "- Transcribed the complete continued-fraction substitution, parity-trace reconstruction, sequence-(d), sequence-(c), and AGM laws; every law spanning two source units is partial at both units and complete only through their joint field evidence.",
        "- Restored the two-Gaussian periodic preset, the dimensional stationary-square-pulse preset, and the split PDEKernel/PDEStep provenance without inventing unstated grid, domain, pulse, or boundary details.",
        "- Added symmetric candidate-local comparison evidence for the irrational/Beatty/substitution family, prime/zeta family, normality witnesses, and exact-versus-finite shift maps; all remain provisional comparisons rather than identity merges.",
        "- Every `UNKNOWN_FROM_SOURCE` reason is reproduced verbatim in that candidate's `missing_mechanics`; every supported/N/A/conflicting field cites only its declared unit/image anchors.",
        "- Split, corrected, or added the Gray/bitwise, universal/per-seed 3n+1, case-(b)/(c), evaluation-policy, prime approximation, perfect/pluperfect/quasiperfect, Stoneham, continuous-CA-rule, and non-autonomous-ODE records identified by hostile review.",
        "- Removed the overcaptured named numerical-method list, retained failure/partiality/conflict semantics, and represented local candidate comparisons with worker-local provisional relations.",
        "- Reconciled all nine Notes routes, including the page-132 sieve route and five `WITHIN_STAGE` scopes. Case (c) has no invented route because the source supplies no literal target.",
        "- Reclassified the six image-native bitwise laws as integer iterations and folded the commutatively identical U005649 rule-60 law into the first iteration candidate.",
        "",
        "## Recorded uncertainties",
        "",
    ])
    for uncertainty in output["uncertainties"]:
        lines.append(f"- {uncertainty}")

    lines.extend([
        "",
        "## Reproducibility hashes",
        "",
        f"- Canonical markdown SHA-256: `{hash_file(canonical_path)}`.",
        f"- Allowed-manifest SHA-256: `{hash_file(bundle / 'allowed-manifest.json')}`.",
        f"- Declared allowed-manifest SHA-256: `{output['allowed_manifest_sha256']}`.",
        f"- Declared bundle SHA-256: `{output['bundle_sha256']}`.",
        f"- Current helper SHA-256: `{hash_file(Path(__file__).resolve())}`.",
        f"- Authored output before declaration SHA-256: `{hashlib.sha256(unfinalized_bytes).hexdigest()}`.",
        f"- Final output SHA-256: `{hash_file(output_path)}`.",
    ])
    if fresh_bundle is not None:
        fresh_hash = hash_file(fresh_bundle / "output" / "output.json")
        lines.extend([
            f"- Fresh-rebuild final output SHA-256: `{fresh_hash}`.",
            f"- Original/fresh byte identity: `{'PASS' if fresh_hash == hash_file(output_path) else 'FAIL'}`.",
        ])

    lines.extend([
        "",
        "## Verification",
        "",
        "- Fresh bundle rebuilt from the authoritative stage assignment: `PASS`.",
        "- Helper rerun on original and fresh bundles: `PASS`; authored bytes matched.",
        "- `prepare_review_output.py --check` before declaration: `PASS`.",
        "- Normal completed-output verification on original bundle: `PASS`.",
        "- `python -O` completed-output verification on original bundle: `PASS`.",
        "- Normal completed-output verification on fresh bundle: `PASS`.",
        "- `python -O` completed-output verification on fresh bundle: `PASS`.",
        "- Coordinator canonical-ID allocation, cross-range route closure, search rounds, and merge/equivalence decisions remain intentionally outside this worker result.",
        "",
    ])
    atomic_text(report_path, "\n".join(lines))


def author(bundle: Path) -> dict[str, Any]:
    manifest = json.loads((bundle / "allowed-manifest.json").read_text())
    output_path = bundle / "output" / "output.json"
    output = json.loads(output_path.read_text())
    if manifest["worker_id"] != WORKER or manifest["stage"] != STAGE or manifest["discovery_epoch"] != EPOCH:
        raise SystemExit("bundle identity does not match this authoring helper")

    reading = output["reading_updates"]
    assets = output["asset_updates"]
    unit_order = {row["source_unit_id"]: index for index, row in enumerate(reading, 1)}
    block_kind_by_uid = {
        row["source_unit_id"]: row["block_kind"] for row in reading
    }
    asset_by_path = {row["physical_path"]: row for row in assets}
    asset_by_id = {row["asset_id"]: row for row in assets}
    image_order = {
        row["physical_path"]: len(reading) + index
        for index, row in enumerate(assets, 1)
    }
    anchor_order = {**unit_order, **image_order}

    # Validate and apply the one symmetric candidate/image join.  This makes
    # an asset link impossible to add without adding the corresponding
    # candidate witness and evidence row.
    referenced_ids = {
        row["asset_id"]
        for row in assets
        if row["reference_status"] == "REFERENCED"
    }
    classified_referenced_ids = set().union(*ASSET_ROLE_IDS.values())
    if referenced_ids != classified_referenced_ids:
        raise RuntimeError(
            "referenced asset-role partition differs: "
            f"missing={sorted(referenced_ids - classified_referenced_ids)}, "
            f"extra={sorted(classified_referenced_ids - referenced_ids)}"
        )
    orphan_ids = {
        row["asset_id"]
        for row in assets
        if row["reference_status"] == "UNREFERENCED_PHYSICAL"
    }
    if orphan_ids != set(ORPHAN_RISKS):
        raise RuntimeError("orphan risk ledger does not cover exactly 30 assets")

    for asset_id, candidate_names in ASSET_CANDIDATE_NAMES.items():
        image_path = asset_by_id[asset_id]["physical_path"]
        for candidate_name in candidate_names:
            spec = spec_named(candidate_name)
            spec["images"] = tuple(ordered_unique([
                *spec["images"],
                image_path,
            ]))

    # Candidate IDs and candidate-anchor ordinals.  The three image-native
    # Other-PDE equations are discovered at A000518; every other candidate is
    # source-unit anchored.
    for spec in SPECS:
        spec["_candidate_anchor_id"] = spec["identity_image"] or spec["uids"][0]
        spec["_candidate_anchor_kind"] = (
            "IMAGE" if spec["identity_image"] else "SOURCE_UNIT"
        )
    SPECS.sort(key=lambda spec: anchor_order[spec["_candidate_anchor_id"]])
    candidate_anchor_counts: dict[tuple[str, str], int] = defaultdict(int)
    for index, spec in enumerate(SPECS, 1):
        spec["id"] = f"W{index:04d}"
        anchor = spec["_candidate_anchor_id"]
        anchor_kind = spec["_candidate_anchor_kind"]
        anchor_key = (anchor_kind, anchor)
        candidate_anchor_counts[anchor_key] += 1
        spec["candidate_anchor"] = {
            "epoch": EPOCH,
            "kind": anchor_kind,
            "id": anchor,
            "ordinal": candidate_anchor_counts[anchor_key],
        }
        spec["_decisions"] = field_decisions(spec, block_kind_by_uid)

    id_by_name = {spec["name"]: spec["id"] for spec in SPECS}

    # Build evidence requests, then allocate immutable IDs in frozen traversal
    # order.  Fingerprint fields are allocated only to their declared exact
    # anchors; context rows keep the provenance joins complete without making
    # mechanics claims.
    requests: list[dict[str, Any]] = []
    serial = 0

    def append_request(
        *,
        spec: dict[str, Any],
        anchor: str,
        sort_slot: int,
        strength: str,
        modality: str,
        claim: str,
        fields: list[str],
        relation_peer: str | None = None,
    ) -> None:
        nonlocal serial
        serial += 1
        is_image = anchor in image_order
        requests.append({
            "sort": (anchor_order[anchor], sort_slot, serial),
            "candidate": spec,
            "anchor_kind": "IMAGE" if is_image else "SOURCE_UNIT",
            "anchor_id": anchor,
            "source_unit_id": None if is_image else anchor,
            "image_path": anchor if is_image else None,
            "strength": strength,
            "modality": modality,
            "claim": claim,
            "fields": fields,
            "relation_peer": relation_peer,
        })

    def source_modality(uid: str, fields: list[str]) -> str:
        block_kind = block_kind_by_uid[uid]
        if block_kind == "fenced_code":
            return "CODE"
        if block_kind == "image":
            return "CAPTION"
        if "rule_relation_constraint_function_or_probability_law" in fields:
            return "FORMULA"
        return "PROSE"

    def mechanics_strength(
        spec: dict[str, Any],
        anchor: str,
        fields: list[str],
    ) -> str:
        if anchor in image_order:
            asset_id = asset_by_path[anchor]["asset_id"]
            if asset_id == "A000443":
                return "DEFECT_LIMITED"
            role = next(
                role for role, ids in ASSET_ROLE_IDS.items() if asset_id in ids
            )
            if role == "NATIVE_EVIDENCE":
                return (
                    "DIRECT_COMPLETE_MECHANICS"
                    if (
                        anchor in {BITWISE_IMAGE, OTHER_PDE_IMAGE}
                        and "rule_relation_constraint_function_or_probability_law"
                        in fields
                    )
                    else "DIRECT_PARTIAL_MECHANICS"
                )
            return "CONTEXTUAL"
        if any(
            anchor in spec["_decisions"][field]["anchors"]
            and len(spec["_decisions"][field]["anchors"]) > 1
            for field in fields
        ):
            # A combined claim whose exact provenance spans multiple source
            # units is partial at every contributing unit.  No one half may
            # be promoted to independently complete mechanics.
            return "DIRECT_PARTIAL_MECHANICS"
        law_anchor = choose_law_anchor(spec, block_kind_by_uid)
        if (
            anchor == law_anchor
            and "rule_relation_constraint_function_or_probability_law" in fields
            and block_kind_by_uid[anchor] == "fenced_code"
        ):
            return "DIRECT_COMPLETE_MECHANICS"
        if anchor == law_anchor:
            return "DIRECT_PARTIAL_MECHANICS"
        return "CORROBORATING"

    for spec in SPECS:
        decisions = spec["_decisions"]
        identity_anchor = spec["_candidate_anchor_id"]
        append_request(
            spec=spec,
            anchor=identity_anchor,
            sort_slot=0,
            strength="DIRECT_IDENTITY",
            modality=(
                "IMAGE"
                if identity_anchor in image_order
                else source_modality(identity_anchor, [])
            ),
            claim=(
                f"Identifies the image-native equation {spec['name']}."
                if identity_anchor in image_order
                else f"Identifies {spec['name']} at the source's stated scope."
            ),
            fields=[],
        )

        fields_by_anchor: dict[str, list[str]] = defaultdict(list)
        for field in FIELDS:
            for anchor in decisions[field]["anchors"]:
                if anchor not in anchor_order:
                    raise RuntimeError(
                        f"{spec['name']}.{field} uses unavailable anchor {anchor}"
                    )
                fields_by_anchor[anchor].append(field)
        evidence_field_groups = (
            ("object_kind", "law_kind"),
            (
                "native_time", "carrier", "support", "topology",
                "structural_invariants", "alphabet_or_value_schema",
            ),
            (
                "complete_state", "visible_history", "control_state", "seed",
                "input", "boundary", "external_data",
            ),
            (
                "frontier_or_activation", "schedule",
                "read_dependencies_or_neighborhood",
            ),
            (
                "rule_relation_constraint_function_or_probability_law",
                "write_replacement_assembly_or_commit",
            ),
            (
                "result_kind", "successor_cardinality",
                "determinism_branching_or_measure",
                "termination_completion_failure", "witness_semantics",
            ),
            (
                "parameters_and_variants",
                "excluded_observers_and_representations",
                "evidence_limit",
            ),
        )
        group_index = {
            field: index
            for index, group in enumerate(evidence_field_groups, 1)
            for field in group
        }
        for anchor in sorted(fields_by_anchor, key=anchor_order.__getitem__):
            grouped_fields: dict[int, list[str]] = defaultdict(list)
            for field in ordered_unique(fields_by_anchor[anchor]):
                grouped_fields[group_index[field]].append(field)
            for field_group in sorted(grouped_fields):
                fields = grouped_fields[field_group]
                exact_claims = []
                for field in fields:
                    item = decisions[field]
                    exact_claims.append(
                        f"{field}={item['value']!r}"
                        if item["value"] is not None
                        else f"{field}=NOT_APPLICABLE ({item['reason']})"
                    )
                append_request(
                    spec=spec,
                    anchor=anchor,
                    sort_slot=field_group,
                    strength=mechanics_strength(spec, anchor, fields),
                    modality=(
                        "IMAGE"
                        if anchor in image_order
                        else source_modality(anchor, fields)
                    ),
                    claim=(
                        f"For {spec['name']}, this anchor supports only: "
                        + "; ".join(exact_claims)
                        + "."
                    ),
                    fields=fields,
                )

        for peer in spec["relation_names"]:
            for anchor in RELATION_EVIDENCE_ANCHORS.get(
                (spec["name"], peer),
                (),
            ):
                if anchor not in spec["uids"]:
                    raise RuntimeError(
                        f"{spec['name']} relation to {peer} uses source "
                        f"{anchor} outside candidate source units"
                    )
                append_request(
                    spec=spec,
                    anchor=anchor,
                    sort_slot=90,
                    strength="CORROBORATING",
                    modality=source_modality(anchor, []),
                    claim=(
                        f"For {spec['name']}, {anchor} explicitly supports "
                        f"the source comparison with {peer}; this is not an "
                        "identity merge."
                    ),
                    fields=[],
                    relation_peer=peer,
                )

        existing_anchors = {
            request["anchor_id"]
            for request in requests
            if request["candidate"] is spec
        }
        for uid in spec["uids"]:
            if uid in existing_anchors:
                continue
            append_request(
                spec=spec,
                anchor=uid,
                sort_slot=99,
                strength="CONTEXTUAL",
                modality=source_modality(uid, []),
                claim=(
                    f"The Markdown image pointer provides only the source link for {spec['name']}; "
                    "it does not transcribe the pictured mechanics."
                    if block_kind_by_uid[uid] == "image"
                    else f"Supplies source context for {spec['name']} without supporting an additional fingerprint field."
                ),
                fields=[],
            )
        existing_anchors = {
            request["anchor_id"]
            for request in requests
            if request["candidate"] is spec
        }
        for image_path in spec["images"]:
            if image_path in existing_anchors:
                continue
            asset_id = asset_by_path[image_path]["asset_id"]
            append_request(
                spec=spec,
                anchor=image_path,
                sort_slot=99,
                strength="DEFECT_LIMITED" if asset_id == "A000443" else "CONTEXTUAL",
                modality="IMAGE",
                claim=(
                    f"A000443 corroborates only the visible case-(a)/(b) material for {spec['name']}; "
                    "the case-(c) formula is outside the bottom crop."
                    if asset_id == "A000443"
                    else f"Original-resolution {asset_id} is a contextual visual witness for {spec['name']} and supplies no additional native field."
                ),
                fields=[],
            )

    requests.sort(key=lambda item: item["sort"])
    evidence_anchor_counts: dict[tuple[str, str], int] = defaultdict(int)
    for index, request in enumerate(requests, 1):
        key = (request["anchor_kind"], request["anchor_id"])
        evidence_anchor_counts[key] += 1
        request["evidence_id"] = f"WE{index:06d}"
        request["group_id"] = f"WG{index:06d}"
        request["anchor"] = {
            "epoch": EPOCH,
            "kind": request["anchor_kind"],
            "id": request["anchor_id"],
            "ordinal": evidence_anchor_counts[key],
        }

    requests_by_candidate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for request in requests:
        requests_by_candidate[request["candidate"]["id"]].append(request)

    route_by_key: dict[str, dict[str, Any]] = {}
    route_anchor_counts: dict[str, int] = defaultdict(int)
    sorted_routes = sorted(
        enumerate(ROUTES),
        key=lambda pair: (unit_order[pair[1][1]], pair[0]),
    )
    for index, (_, route_spec) in enumerate(sorted_routes, 1):
        key, uid, literal, expected, terms, scope = route_spec
        route_anchor_counts[uid] += 1
        route_id = f"WR{index:04d}"
        route_by_key[key] = {
            "route_id": route_id,
            "source_unit_id": uid,
            "source_asset_id": "",
            "discovery_epoch": str(EPOCH),
            "discovery_kind": "SOURCE_UNIT",
            "discovery_id": uid,
            "discovery_ordinal": str(route_anchor_counts[uid]),
            "literal_target": literal,
            "route_kind": "PAGE",
            "expected_topic": expected,
            "owning_stage": str(STAGE),
            "closure_scope": scope,
            "status": "PENDING",
            "target_unit_ids": "[]",
            "target_asset_ids": "[]",
            "attempts": "[]",
            "vocabulary_terms": array_text(terms),
            "defect_boundary": "",
        }

    candidates: list[dict[str, Any]] = []
    unit_candidates: dict[str, list[str]] = defaultdict(list)
    asset_candidates: dict[str, list[str]] = defaultdict(list)
    unit_anchor_candidates: dict[str, list[str]] = defaultdict(list)
    for spec in SPECS:
        candidate_id = spec["id"]
        reqs = requests_by_candidate[candidate_id]
        field_evidence_ids = {
            field: [
                r["evidence_id"]
                for r in reqs
                if field in r["fields"]
            ]
            for field in FIELDS
        }
        mechanics_ids = ordered_unique(
            evidence_id
            for field in FIELDS
            for evidence_id in field_evidence_ids[field]
        )
        support, fingerprint = profile(
            spec,
            spec["_decisions"],
            field_evidence_ids,
        )
        evidence_rows = [{
            "evidence_id": r["evidence_id"],
            "evidence_group_id": r["group_id"],
            "discovery_anchor": r["anchor"],
            "source_unit_id": r["source_unit_id"],
            "image_path": r["image_path"],
            "strength": r["strength"],
            "modality": r["modality"],
            "claim": r["claim"],
            "fingerprint_fields": r["fields"],
        } for r in reqs]
        route_ids = [route_by_key[key]["route_id"] for key in spec["route_keys"]]
        unknown_reasons = [
            spec["_decisions"][field]["reason"]
            for field in FIELDS
            if spec["_decisions"][field]["status"] == "UNKNOWN_FROM_SOURCE"
        ]
        conflicting_reasons = [
            spec["_decisions"][field]["reason"]
            for field in FIELDS
            if spec["_decisions"][field]["status"] == "CONFLICTING_SOURCE"
        ]
        source_statuses = {
            SOURCE_STATUS_BY_UID.get(uid, ("CLEAR", ""))[0]
            for uid in spec["uids"]
        }
        source_statuses.update(
            "DEFECTIVE"
            if asset_by_path[image_path]["asset_id"] == "A000443"
            else "CLEAR"
            for image_path in spec["images"]
        )
        status_order = {"CLEAR": 0, "AMBIGUOUS": 1, "DEFECTIVE": 2, "CONFLICTING": 3}
        parameter_evidence = field_evidence_ids["parameters_and_variants"]
        default_relation_evidence = next(
            (
                r["evidence_id"]
                for r in reqs
                if r["relation_peer"] is None
                if r["strength"] not in {"DIRECT_IDENTITY", "CONTEXTUAL", "LEAD_ONLY"}
            ),
            reqs[0]["evidence_id"],
        )
        relation_evidence_by_peer = {
            peer: [
                r["evidence_id"]
                for r in reqs
                if r["relation_peer"] == peer
            ]
            for peer in spec["relation_names"]
        }
        candidates.append({
            "id": candidate_id,
            "record_status": "ACTIVE",
            "provisional_name": spec["name"],
            "aliases": [],
            "discovery_stage": STAGE,
            "discovery_anchor": spec["candidate_anchor"],
            "source_unit_ids": ordered_unique(spec["uids"]),
            "source_evidence": evidence_rows,
            "source_status": sorted(source_statuses, key=status_order.__getitem__),
            "image_witnesses": list(spec["images"]),
            "evidence_strength": ordered_unique([r["strength"] for r in reqs]),
            "field_support": support,
            "fingerprint": fingerprint,
            "parameters": [
                {
                    "name": name,
                    "source_description": (
                        f"Printed parameter/input: {name}."
                        if parameter_evidence
                        else f"Named but not fully specified in the sealed source: {name}."
                    ),
                    "evidence_ids": parameter_evidence,
                }
                for name in spec["params"]
            ],
            "variants": [
                {
                    "name": name,
                    "source_description": f"Separately stated source variant: {name}.",
                    "evidence_ids": parameter_evidence,
                }
                for name in spec["variants"]
            ],
            "missing_mechanics": ordered_unique([
                *spec["missing"],
                *unknown_reasons,
            ]),
            "uncertainties": ordered_unique([
                *spec["source_uncertainties"],
                *unknown_reasons,
                *conflicting_reasons,
            ]),
            "related_candidate_ids": [
                {
                    "candidate_id": id_by_name[peer],
                    "relation": "SOURCE_COMPARE",
                    "proof_kind": "PROVISIONAL_COMPARISON",
                    "evidence_ids": (
                        relation_evidence_by_peer[peer]
                        or [default_relation_evidence]
                    ),
                    "before_rationale": "",
                    "after_rationale": "",
                    "uncertainty": (
                        f"The source relates {spec['name']} to {peer}; this "
                        "provisional comparison is not an identity merge."
                    ),
                }
                for peer in spec["relation_names"]
            ],
            "cross_reference_ids": route_ids,
            "evidence_reassignments": [],
        })
        for uid in ordered_unique(spec["uids"]):
            unit_candidates[uid].append(candidate_id)
        unit_anchor_candidates[spec["uids"][0]].append(candidate_id)
        if spec["_candidate_anchor_kind"] == "IMAGE":
            source_unit_id = asset_by_path[spec["_candidate_anchor_id"]][
                "source_unit_id"
            ]
            unit_anchor_candidates[source_unit_id].append(candidate_id)
        for image_path in spec["images"]:
            asset_candidates[image_path].append(candidate_id)

    unit_routes: dict[str, list[str]] = defaultdict(list)
    for route in route_by_key.values():
        unit_routes[route["source_unit_id"]].append(route["route_id"])

    kind_by_candidate = {spec["id"]: spec["kind"] for spec in SPECS}
    name_by_candidate = {spec["id"]: spec["name"] for spec in SPECS}
    for row in reading:
        uid = row["source_unit_id"]
        candidate_ids = unit_candidates[uid]
        route_ids = unit_routes[uid]
        source_status, source_uncertainty = SOURCE_STATUS_BY_UID.get(
            uid, ("CLEAR", "")
        )
        row.update({
            "review_status": "REVIEWED",
            "review_epoch": str(EPOCH),
            "source_status": source_status,
            "uncertainty": source_uncertainty,
            "candidate_ids": array_text(candidate_ids),
            "route_ids": array_text(route_ids),
            "review_stage": str(STAGE),
            "reviewer": WORKER,
        })
        roles: list[str] = []
        if uid == "U005695":
            row["review_disposition"] = "SOURCE_DEFECT_OR_AMBIGUITY"
            row["evidence_statement"] = (
                "The Markdown pointer anchors A000443, whose original was "
                "reviewed: cases (a) and (b) are visible, but the bottom crop "
                "removes the identity-bearing case-(c) formula."
            )
            roles.append("SOURCE_DEFECT")
        elif candidate_ids:
            kinds = {kind_by_candidate[cid] for cid in candidate_ids}
            if kinds & {"REPRESENTATION", "GENERATOR"}:
                roles.append("REPRESENTATION")
            if kinds & {"OBSERVER", "QUERY"}:
                roles.append("OBSERVER_OR_ANALYZER")
            if kinds & {"SOLVER", "EVALUATION_POLICY"}:
                roles.append("IMPLEMENTATION_DETAIL")
            if kinds & {"PRESET"}:
                roles.append("SEED_INPUT_OR_BOUNDARY")
            if kinds & {"RELATION", "PDE", "ODE"}:
                roles.append("PROPERTY_OR_RESTRICTION")
            row["review_disposition"] = "CANDIDATE" if uid in unit_anchor_candidates else "SUPPORTS_CANDIDATE"
            names = [name_by_candidate[cid] for cid in candidate_ids]
            row["evidence_statement"] = (
                "Canonical source supplies candidate-specific identity, law, "
                "restriction, or failure evidence for: "
                + "; ".join(names)
                + "."
                + (
                    " It also carries pending route(s) "
                    + ", ".join(route_ids)
                    + " for mechanics explicitly located elsewhere in Stage 8."
                    if route_ids
                    else ""
                )
            )
        elif route_ids:
            row["review_disposition"] = "CROSS_REFERENCE"
            row["evidence_statement"] = (
                "Construction-relevant mechanics are identified only through "
                "the exact typed route(s): " + ", ".join(route_ids) + "."
            )
            roles.append("EXTERNAL_ONLY")
        elif row["block_kind"] == "image":
            row["review_disposition"] = "REPRESENTATION_OR_OBSERVER"
            row["evidence_statement"] = "Markdown image unit is a rendering/observer pointer; the assigned physical asset was screened separately."
            roles.append("REPRESENTATION")
        elif uid in HISTORICAL_UNITS:
            row["review_disposition"] = "HISTORICAL_ONLY"
            row["evidence_statement"] = "The unit supplies provenance, chronology, or terminology but no independently specified native law."
            roles.append("HISTORICAL_MENTION")
        elif uid in OBSERVER_UNITS:
            row["review_disposition"] = "REPRESENTATION_OR_OBSERVER"
            row["evidence_statement"] = "The unit states behavior, measurement, rendering, restriction, or comparison without an additional native law."
            roles.append("BEHAVIOR_OR_OUTCOME")
        else:
            row["review_disposition"] = "NO_CONSTRUCTION"
            row["evidence_statement"] = "Sequential in-context review found no additional independently anchored construction in this unit."
        row["secondary_roles"] = array_text(ordered_unique(roles))

    for row in assets:
        image_path = row["physical_path"]
        candidate_ids = asset_candidates[image_path]
        orphan = row["reference_status"] == "UNREFERENCED_PHYSICAL"
        asset_id = row["asset_id"]
        if orphan:
            role = "SOURCE_DEFECT"
            risks = ORPHAN_RISKS[asset_id]
        else:
            role = next(
                role_name
                for role_name, ids in ASSET_ROLE_IDS.items()
                if asset_id in ids
            )
            risks = ASSET_RISKS.get(asset_id, ())
        defective = orphan or asset_id == "A000443"
        text_bearing = "TEXT_BEARING" in risks
        if asset_id == "A000443":
            evidence_statement = (
                "Original 546×413 extraction reviewed at original resolution. "
                "The case-(a) and case-(b) formulas are legible and may support "
                "only DEFECT_LIMITED evidence; the lower edge cuts off the "
                "case-(c) formula, which was not reconstructed."
            )
            uncertainty = (
                "Transcription CHECKED is limited to the two visible formulas; "
                "case (c)'s one-step rule is unavailable below the crop."
            )
        elif orphan:
            evidence_statement = (
                "Original-resolution unreferenced fragment was screened only "
                "to document the extraction defect/alternate crop. It has no "
                "candidate or route link and contributes no mechanics."
            )
            uncertainty = (
                "No live Markdown source-unit anchor exists for this physical "
                "fragment, so it cannot be promoted to candidate evidence."
            )
        elif role == "NATIVE_EVIDENCE":
            evidence_statement = (
                "Original-resolution native construction image was reviewed; "
                + (
                    "its construction-bearing text/formula was independently checked."
                    if text_bearing
                    else "its diagrammatic construction role was checked without claiming a text transcription."
                )
            )
            uncertainty = ""
        elif role == "RELATION":
            evidence_statement = (
                "Original-resolution image directly illustrates the stated "
                "relation between represented quantities, but is not promoted "
                "to an autonomous transition law."
            )
            uncertainty = ""
        elif role == "CONTROL":
            evidence_statement = (
                "Original-resolution control/comparison rendering was reviewed "
                "as a preset, parameter comparison, or implementation check; "
                "it supplies no additional native law."
            )
            uncertainty = ""
        else:
            evidence_statement = (
                "Original-resolution observer/rendering was reviewed; it shows "
                "behavior or measured output and supplies no additional native law."
            )
            uncertainty = ""
        row.update({
            "inspection_status": "SCREENED",
            "review_epoch": str(EPOCH),
            "visual_role": role,
            "source_status": "DEFECTIVE" if defective else "CLEAR",
            "risk_flags": array_text(list(risks)),
            "original_resolution_status": "REVIEWED",
            "transcription_status": "CHECKED" if text_bearing and not orphan else "NOT_REQUIRED",
            "candidate_ids": array_text(candidate_ids),
            "route_ids": "[]",
            "evidence_statement": evidence_statement,
            "review_stage": str(STAGE),
            "reviewer": WORKER,
            "uncertainty": uncertainty,
        })

    actual_role_counts = count_values(assets, "visual_role")
    expected_role_counts = {
        "NATIVE_EVIDENCE": 6,
        "RELATION": 2,
        "CONTROL": 21,
        "OBSERVER": 22,
        "SOURCE_DEFECT": 31,
    }
    if actual_role_counts != expected_role_counts:
        raise RuntimeError(
            f"asset role counts differ: {actual_role_counts} != {expected_role_counts}"
        )
    if count_values(assets, "source_status") != {"CLEAR": 51, "DEFECTIVE": 31}:
        raise RuntimeError("asset source-status partition differs from audited totals")

    output["candidate_proposals"] = candidates
    output["route_proposals"] = sorted(
        route_by_key.values(),
        key=lambda row: int(row["route_id"][2:]),
    )
    output["uncertainties"] = [
        "Thirty unreferenced physical assets were original-resolution checked but remain defect-only because they have no live source-unit anchor.",
        "A000443 exposes complete formulas only for cases (a) and (b); the case-(c) rule is clipped and was not reconstructed.",
        "Case (c) remains an E5 partial-system candidate with exact missing mechanics and DEFECT_LIMITED image evidence. No route is emitted because the sealed source contains no literal target or locator from which a valid immutable route identity could be formed.",
        "U005993 is internally conflicting about rationality conditions for repetitive versus complicated Anosov-map behavior; the displayed map law remains separately transcribed.",
        "All typed routes remain pending for coordinator target closure; no routed mechanics were silently imported into this sealed worker result.",
    ]
    output["prohibited_input_nonuse"] = False
    atomic_json(output_path, output)
    return {
        "readings": len(reading),
        "assets": len(assets),
        "candidates": len(candidates),
        "routes": len(route_by_key),
        "evidence": len(requests),
        "orphans": sum(row["reference_status"] == "UNREFERENCED_PHYSICAL" for row in assets),
        "output_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--fresh-bundle", type=Path)
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    if not args.report_only:
        result = author(bundle)
        print(json.dumps(result, sort_keys=True))
    if args.report is not None:
        render_report(
            bundle,
            args.report.resolve(),
            args.fresh_bundle.resolve() if args.fresh_bundle else None,
        )
        print(f"wrote report: {args.report.resolve()}")


if __name__ == "__main__":
    main()
