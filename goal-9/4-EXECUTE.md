# 4-EXECUTE

## Current Facts

- SimpleProgram and Seed compatibility are already checked without legacy
  contracts.
- Selector returns full ordered addresses and does not resolve values.
- Relational execution needs Seed context, so the resolved transition signature
  is `step(trajectory, state)`.

## Updated Assumptions

- The first executor supports one finite realized support and one available
  source-time slice. This is sufficient to prove the kernel and does not
  pre-commit dynamic support or temporal-memory semantics.
- A Space coordinate function enumerates non-temporal addresses from Seed.
- Fixed boundary supplies a value; periodic or reflective boundary uses a
  Space normalization function; missing access with no resolver is an error.
- Rule is always invoked as `rule(observed_values, source_coordinate)`.

## Big Picture Objective

Implement a transparent reference transition that reads one immutable State,
constructs every coordinate of a complete new `t+1` State, and appends those
States into an Episode.

## Detailed Implementation Plan

- Add primitive Space helpers for finite box support, relational support,
  fixed boundary values, periodic wrapping, and reflection.
- Add Space read resolution that preserves the requested time and rejects an
  unavailable source time.
- Implement `step(trajectory, state)` and `rollout(trajectory, limit)` in a new
  module with no call to old `apply` or rollout.
- Validate complete current support and every Rule output directly.
- Strengthen Episode to require consecutive explicit times.
- Expose `step` and `rollout` from package root.
- Add anonymous Cartesian fixed/periodic and relational fixtures.

## No-Cheating Checks

- Do not import `program.py`, old rules, old neighborhoods, loci, or frontiers.
- Do not emit KEEP/preserve/replace/delete actions.
- Do not mutate or reuse the prior State as the successor.
- Do not hide time in tuple position alone without verifying it on every State.
- Do not implement a canonical CA or graph preset in test helpers.

## Completion Requirements

- Cartesian and relational exact successors pass.
- Fixed and periodic boundaries differ at a known coordinate.
- Rollout contains the Seed plus exactly `limit` successor States.
- Earlier States remain immutable and unchanged.
- Historical/future reads unavailable in the one-slice executor fail directly.
- Alphabet-invalid Rule output fails directly.
- Focused tests and source no-cheating scans pass.

## Stage Results

- Pending implementation.
