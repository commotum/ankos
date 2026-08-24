# 5-SOURCES

## Current Facts

- The live kernel accepts one definite Space, Alphabet, Neighborhood, Rule,
  and Seed using ordinary Python values.
- Shape and complete initial values belong to Seed; changing finite shape does
  not require changing a shape-polymorphic SimpleProgram.
- Compatibility is checked directly by `Trajectory(program, seed)`.

## Updated Assumptions

- Python tuples and generator functions already provide the plural layer.
- Dependencies between sources are clearest as function arguments and nested
  loops, not as a universal Cartesian-product engine.
- A future named preset can be an ordinary module containing these functions;
  it does not need a runtime `Preset` object.

## Big Picture Objective

Prove that plural sources can yield fully definite singular values and can be
mixed explicitly, without implementing a canonical preset or introducing a
source-class hierarchy.

## Detailed Implementation Plan

- Define anonymous test-only source functions for Spaces, Alphabets,
  Neighborhoods, Rules, and Seeds.
- Make Neighborhood sources accept the selected Space and Rule sources accept
  the selected Alphabet and Neighborhood, exposing dependencies plainly.
- Compose definite SimplePrograms with nested loops.
- Generate Seeds independently, including one that is valid under one
  Alphabet and invalid under another.
- Form Trajectories directly and use ordinary exception handling when a caller
  wants to filter incompatible combinations.

## No-Cheating Checks

- Add no production generator abstraction.
- Add no `Preset`, factory, builder contract, constraint solver, or parameter
  object.
- Give fixtures no canonical family names or behavior.
- Assert executable behavior for a compatible result, not merely source
  counts or signatures.

## Completion Requirements

- More than one Space, Rule, and Seed is yielded by plain generators.
- Every composed SimpleProgram has one selected value in every field.
- One Seed is directly shown incompatible with a binary Alphabet and
  compatible with a ternary Alphabet.
- At least one composed Trajectory executes successfully.
- Focused tests, source scans, and `git diff --check` pass.

## Stage Results

- Added `tests/test_sources.py` using only ordinary generator functions and
  explicit nested loops. The sources yield two Spaces, two Alphabets, two
  Neighborhoods per compatible Space, two exact Rule callables, and three
  independently generated Seeds.
- Every emitted SimpleProgram is singular and fully selected. The source
  dependency order is visible in ordinary function calls rather than stored
  in a framework.
- A Seed containing value `2` is rejected under the binary Alphabet and
  accepted under the ternary Alphabet at `Trajectory` construction. A
  compatible composed Trajectory also completes a real rollout.
- Verification:
  - `uv run pytest -q tests/test_sources.py tests/test_execution.py tests/test_selector.py tests/test_core_values.py`
    -> `17 passed`.
  - A source scan found no `Preset`, `PresetSpec`, `Factory`,
    `BuilderContract`, preset directory, or canonical family implementation in
    the live kernel or source fixture.
  - `find src -type d -name presets` returned nothing.
  - `git diff --check` passed.
- No production plural-source code was needed. A future preset is simply a
  module of functions shaped like the anonymous fixture.
