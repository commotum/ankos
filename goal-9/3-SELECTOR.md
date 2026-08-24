# 3-SELECTOR

## Current Facts

- The live root now imports only the ordinary-value core.
- States use full coordinate tuples, so relative selectors can preserve and
  alter time explicitly rather than relying on a hidden current slice.
- Seed contains plain immutable relation mappings and complete values, giving
  relational selectors enough realization context without a Graph class.

## Updated Assumptions

- A Neighborhood needs only one of two runtime shapes initially: an ordered
  tuple of full-coordinate offsets or a callable receiving `(source, seed)`.
- Relation ordering is supplied by Seed and is Rule-visible. Arbitrary vertex
  values must never be sorted to manufacture an order.
- Boundary resolution remains entirely outside Selector.

## Big Picture Objective

Add a small coordinate-only selector module that covers Cartesian offsets and
plain relational adjacency without transporting any part of the old locus,
region, selector-expression, or capability hierarchies.

## Detailed Implementation Plan

- Add direct relative-coordinate translation.
- Add current-address selection.
- Add a small relation selector constructor and the conventional `adjacent`
  selector using `Seed.relations`.
- Add one `select` dispatcher for offset tuples and address callables.
- Validate address rank, relation completeness, relation endpoints, and result
  shape directly.
- Add focused tests for ordered offsets, explicit temporal offsets, relation
  order, and invalid endpoints.

## No-Cheating Checks

- Do not import `loci`, `neighborhoods`, `frontiers`, or old state/configuration
  machinery.
- Do not create Locus, Region, Selector, Graph, Vertex, or relation classes.
- Do not resolve fixed/periodic/reflective values in selector functions.
- Do not close a selector over one concrete Seed relation.

## Completion Requirements

- Cartesian and `(t,v)` relational addresses use ordinary tuples.
- Ordered relation values reach Rule order unchanged.
- Every relation endpoint must occur in the Seed's realized support.
- Selector functions return addresses only.
- Focused tests and diff checks pass.

## Stage Results

- Added `src/ca/selector.py` with five small functions and no selector class:
  ordered relative translation, current-address selection, relation selection,
  conventional adjacency, and one offset/callable dispatcher.
- Relative offsets operate on full coordinates, so temporal offsets remain
  explicit.
- Relational selection reads plain ordered mappings from Seed, verifies exact
  realized sources and endpoints, and never sorts vertex values.
- Root now exposes the lightweight `selector` module without importing legacy
  neighborhoods or loci.
- `uv run pytest -q tests/test_selector.py tests/test_core_values.py` passed:
  8 tests.
- A source scan found none of `Locus`, `Region`, `Graph`, `Vertex`, Frontier,
  capability, or `loci` in `selector.py`.
- `git diff --check` passed.
- Stage 3 is complete. Boundary resolution remains for Stage 4's Space read.
