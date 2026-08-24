# 6-CUTOVER

## Current Facts

- The new kernel already owns the package root and passes its focused tests.
- Every old execution module is mutually tied to semantic loci/frontiers and
  cannot remain as an alternate honest execution path.
- There is no in-repository consumer or package entry point requiring legacy
  compatibility.
- NumPy was used only by the rejected dataset/RNG/viz-export path.
- The viewer's format decoder and static server are independent downstream
  utilities; bundle generation is not part of this kernel goal.

## Updated Assumptions

- The smallest coherent live package contains the core values, coordinate
  selectors, Space helpers, immutable executor, flat progress catalog, and an
  explicitly disconnected existing-bundle viewer.
- Alphabet and Neighborhood need no nominal owner classes or wrapper modules;
  `frozenset`, predicates, offset tuples, and selector functions are their
  public forms.
- Rule needs no owner module: an ordinary callable is the exact selected Rule.
- The canonical taxonomy should remain discoverable, but every family must
  fail honestly until a later preset goal implements it.

## Big Picture Objective

Remove the rejected runtime completely so `ca` has one execution model and no
legacy escape hatch, while retaining book-order taxonomy identity as honest
unimplemented progress markers.

## Detailed Implementation Plan

- Delete the legacy loci, Frontier, program, rule-expression, neighborhood,
  alphabet-contract, seed-spec, dataset, RNG, serialization, and viz-export
  modules.
- Remove the obsolete dataset export example and ECA/serialization smoke test.
- Replace the category catalog package with one flat progress module derived
  from `ref/types.csv`.
- Keep only the useful taxonomy integrity test plus explicit unimplemented
  behavior checks; remove planned-builder signature rewards.
- Remove NumPy from project dependencies and refresh the lock.
- Rewrite the configured README and desired API documents around the live
  primitive kernel.
- Inspect fresh imports and run the full retained suite.

## No-Cheating Checks

- No compatibility file named `loci.py` or `frontiers.py` may remain.
- No alternate module may import or execute the deleted application runtime.
- Catalog callables must raise before constructing anything.
- Passing tests may not be used to describe catalog families as implemented.
- Documentation must not promise preset, streaming, serialization, continuous
  time, or resource-control behavior that is not live.

## Completion Requirements

- Fresh `import ca` loads only the primitive kernel and flat catalog.
- Legacy source and stale imports are absent.
- Exactly sixty taxonomy rows map to sixty explicit unimplemented entries.
- All retained tests protect runtime behavior or taxonomy integrity.
- The package has no unused NumPy dependency.
- Full tests and `git diff --check` pass.

## Stage Results

- Pending final cutover verification.

