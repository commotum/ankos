# 4-CODECS

## Current Facts

- G7-03 starts from clean commit
  `d71626fcd6d649d630473f8f3d5bda098fabc790`.
- The owned baseline command,
  `UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs tests`, reports
  `356 passed, 26 skipped`.
- G7-00 through G7-02 are complete. The runtime has exactly five stored
  program fields, one family-blind `apply`, one apply-owned `rollout`, and
  reusable mechanics for all 60 audited families.
- `goal-7/codec-inventory.csv` contains 387 rows covering 178 public sealed
  types across `loci`, `alphabets`, `seeds`, `frontiers`, `neighborhoods`,
  `rules`, and `program`.
- `src/ca/serialization.py` is still an inert scaffold: `dumps` and `loads`
  raise `NotImplementedError`, and the root does not expose the namespace.
- G7-03 owns 13 current skips: five serialization unit tests, five CT09
  tests, two CT10 tests, and one observer/serialization-boundary test.
  The other 13 skips belong to G7-04 catalog work.
- Catalog modules physically exist as inert shells but remain unexposed.
  G7-03 may neither import nor implement them.

## Updated Assumptions

- The 387-row inventory is an exhaustive schema worklist, not runtime input.
  Production codecs need a closed, explicit registry whose tags, versions,
  fields, and enum values cannot expand through accidental reflection.
- Canonical JSON is sufficient as the wire container if every semantic scalar
  and node has an explicit tagged encoding, duplicate fields are detected
  before dictionary construction, and accepted bytes must equal canonical
  re-encoding.
- Arbitrary integers use canonical signed decimal text and rationals use
  normalized numerator/denominator text. Python floats are never admitted as
  exact semantic values.
- Owner dataclass constructors and `__post_init__` validators remain the
  authoritative local validation boundary after structural decoding.
- A derived SHA-256 digest may protect the canonical envelope, but it is never
  trusted as identity and must be recomputed from the validated payload.
- The existing exact `RepresentationRelation` mechanics are reusable. G7-03
  must add complete-result mapping evidence and cannot settle CT10 by
  comparing rendered successor state alone.

## Big Picture Objective

Implement one lossless, versioned, fail-closed, catalog-free codec boundary
for every G7-01/G7-02 semantic value, expose it as `ca.serialization`, and
prove every exact representation claim through inverse-on-image and complete
one-step result commutation.

## Detailed Implementation Plan

1. Freeze the schema registry.
   - Translate every inventory owner/type/tag/version/field/enum value into a
     production-owned closed registry.
   - Validate registry declarations against the imported sealed owner types
     at serialization-module initialization.
   - Add an executable inventory join proving no row, type, field, tag,
     version, or enum value is omitted or added.
2. Implement canonical structural encoding.
   - Encode `None`, booleans, arbitrary integers, strings, normalized
     `Fraction` values, immutable tuples, enums, and registered frozen
     dataclasses with distinct versioned tags.
   - Encode `SimpleProgram` with outer tag `ca.simple-program`, schema version
     `1`, and a payload containing exactly `seed`, `alphabet`, `frontier`,
     `neighborhood`, and `rule`.
   - Derive the envelope digest from canonical payload bytes and require
     byte-for-byte canonical re-encoding.
3. Implement typed fail-closed decoding.
   - Detect malformed UTF-8/JSON and duplicate, missing, or extra fields.
   - Reject unknown tags, versions, enum values, primitives, unsupported
     exactness, noncanonical numeric spellings, forged digests, lossy or
     unavailable migrations, and invalid reconstructed descriptors.
   - Return only `Decoded(value)` or `DecodeRejected(DecodeFault)`; never leak
     a partially initialized object or raise for untrusted bytes.
4. Activate CT09.
   - Build valid samples spanning every registered sealed type and enum
     variant, including all component, Rule, application, evidence, measure,
     trace, law, fresh-reference, and intensional forms.
   - Assert equality and identical re-encoding for every sample.
   - Add targeted exact-distinction and hostile mutation tests for the
     program envelope and nested nodes.
5. Activate CT10.
   - Prove inverse-on-image for every exact PX10 representation fixture.
   - Map complete represented application results back to native semantics,
     comparing outcomes, total dispositions, cardinalities, witnesses,
     provenance, continuation, probability/submeasure views, fresh bindings,
     fibers, lineage, and evidence.
   - Keep lossy, approximate, and out-of-image relations explicit.
6. Expose only the codec namespace.
   - Add lazy/eager-safe `ca.serialization` to the curated root without
     flattening codec records or importing catalog/downstream modules.
   - Activate the observer exclusion that proves pure observer/tooling values
     do not enter canonical semantic payloads.
7. Close the stage.
   - Run all changed-owner unit and CT09/CT10 suites, the complete active
     suite, static import/schema/pending checks, lock validation,
     `git diff --check`, and a hostile codec review.
   - Record exact results here and fold durable facts into `0-plan.md`.
   - Do not create `5-CATALOG.md` or begin G7-04.

Expected implementation owners are `src/ca/serialization.py` and
`src/ca/__init__.py`. Expected tests are `tests/test_serialization.py`,
`tests/conformance/test_serialization_contract.py`,
`tests/conformance/test_representation_commutation.py`,
`tests/conformance/test_observer_boundary.py`, and inventory/sample helpers
under `tests/conformance/`.

## No-Cheating Checks

- Semantic owner modules do not import `serialization`; dependency direction
  is owners to codec only.
- `serialization.py` and `program.py` do not import catalog, and decoding
  succeeds while catalog imports are blocked.
- The wire never stores SPF/F/T IDs, catalog category/name, constructor
  spelling/arguments, source citation, alias, invocation receipt, callback,
  Python class/module path, object identity, hash, or memory address.
- Registry membership is explicit. A newly discovered dataclass, enum member,
  tag, version, field, or primitive fails until deliberately added.
- Decoding uses no pickle, `eval`, `exec`, dynamic import, reflection-selected
  constructor path, compatibility executor, hidden solver, ambient RNG, or
  “try new then old” fallback.
- Program payload has exactly five expanded field keys. Digest, schema
  version, and envelope metadata remain outside semantic identity.
- Unknown/malformed/lossy input returns a typed rejection without a partial
  value, default field, commit, draw, or other side effect.
- Exact integers, rationals, algebraics, represented numerics, complexes,
  laws, measures, structural references, and intensional ASTs never collapse
  through float or rendered text.
- CT10 compares the complete application algebra, not only successor state,
  and never routes its expected side through the same mapping under test.
- Exactly one production `apply` remains; codec tags never select application
  mechanics.
- Goal 2, Goal 5, Goal 6, catalog, datasets, RNG, visualization, and release
  documentation remain unchanged.

## Completion Requirements

- Every one of the 387 inventory rows and all 178 owner types has an exact
  registered schema and executable coverage.
- `dumps(value)` and `loads(blob)` round-trip every public semantic variant;
  accepted blobs re-encode identically.
- `DecodeFault`, `DecodeRejected`, and `Decoded` form one typed, fail-closed
  public result boundary.
- The canonical `SimpleProgram` envelope is tag `ca.simple-program`, version
  `1`, with exactly the five expanded payload keys.
- Unknown tags, versions, primitives, fields, enum values, migrations,
  malformed/duplicate/noncanonical input, forged digests, and invalid
  descriptors are rejected.
- No 0.1 `Dynamics` manifest, catalog recipe, alias-only payload, or
  constructor receipt is accepted.
- CT09 passes exhaustively and every G7-03 serialization skip is removed.
- CT10 proves inverse-on-image and complete-result commutation for exact
  representation fixtures; lossy and approximate relations remain qualified.
- `ca.serialization` is exposed without eager catalog or auxiliary imports,
  while codec record names remain module-qualified.
- The full active suite is green with only the 13 explicitly G7-04-owned
  skips retained.
- Static and hostile review find no catalog-backed codec, covert sixth field,
  permissive reflection, lossy fallback, digest authority, alternate
  executor, or incomplete inventory coverage.

## Stage Results

In progress.
