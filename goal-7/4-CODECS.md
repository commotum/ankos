# 4-CODECS

## Stage-Start Facts

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
  is codec-to-owner only.
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

### Authoritative behavior

- `ca.serialization` now owns one explicit closed registry for 178 public
  sealed owner types and 387 inventory variants. Registry initialization
  fails if an owner type, dataclass field, enum member, tag syntax/uniqueness,
  version, or aggregate count drifts; the executable inventory join freezes
  each explicit tag independently of Python class/module spelling.
- Canonical bytes distinguish `None`, booleans, arbitrary integers, strings,
  exact `Fraction` values, tuples, enums, and frozen records. Accepted bytes
  must be UTF-8 JSON with the canonical ordering, escaping, numeric spelling,
  envelope shape, and recomputed SHA-256 digest.
- `SimpleProgram` uses tag `ca.simple-program`, schema version `1`, and
  exactly the five payload keys `seed`, `alphabet`, `frontier`,
  `neighborhood`, and `rule`. No catalog receipt, constructor spelling,
  alias, observer value, legacy manifest, or sixth semantic field is
  admitted.
- Decoding is total and fail-closed: it returns only `Decoded(value)` or
  `DecodeRejected(DecodeFault)`. Unknown tags, versions, fields, primitives,
  enum values, noncanonical bytes, malformed UTF-8/JSON, duplicate keys,
  forged digests, invalid reconstructed records, and unavailable migrations
  reject without a partial value or side effect.
- The root façade now exposes the module-qualified `ca.serialization`
  namespace as its eleventh name. Codec records and functions remain
  namespace-qualified, and catalog remains blocked and unexposed.
- CT09 exercises exactly 387 schema representatives: 137 record values and
  all 250 members of the registered enum types, spanning all 178 owner types.
  These are exhaustive schema/type/member representatives, not a claim to
  enumerate every possible inhabitant of an infinite value type.
- CT10 proves all eight exact PX10 relations over both points of their
  declared finite domains. Each actual relation uses one shared
  `SimpleProgram`; its source and terminal target are reconstructed from real
  workspace loci, including fresh and multistep mechanics. For each relation,
  a separate test-owned conjugacy uses one fixed native program and one fixed
  represented program across both points and compares every field of their
  complete application results after only declared value and derived-identity
  mapping. This normalization is proof machinery, not a production mapping
  API.
- Lossy, approximate, and out-of-image relations remain explicit and cannot
  call the exact inverse.

### Files and boundaries

- Replaced the inert `src/ca/serialization.py` shell with the closed codec and
  exposed only its namespace from `src/ca/__init__.py`.
- Tightened local construction validity in `alphabets.py`, `loci.py`,
  `rules.py`, and `program.py` where hostile codec cases demonstrated that a
  structurally forged record could otherwise cross the encode boundary.
  Version fields now require exact integer `1`, not equal-valued booleans or
  rationals.
- Refined `codec-inventory.csv` only where the executable registry established
  the canonical `SimpleProgram` tag or a stricter local validator.
- Added exhaustive samples and activated the serialization, CT09, CT10,
  observer-boundary, inventory-join, and public-surface tests. No G7-03 skip
  remains.
- The CT10 review disproved part of the earlier PX10 mechanics evidence.
  `tests/conformance/g7_mechanics.py` was repaired and G7-02 was reclosed; the
  exact correction is recorded in `3-MECHANICS.md`.
- No production catalog module, Goal 2, Goal 5, Goal 6, dataset, RNG,
  visualization, lockfile dependency, or release surface changed.

### Hostile review and repaired assumptions

The hostile pass rejected several initially green shortcuts. Dedicated
regressions now establish that:

- identity normalization is field-qualified and cannot erase an ordinary
  semantic string, a 64-hex string, caller lineage, or a semantic value equal
  to a real derived identity;
- atom and successor aliases use representation-stable structural keys plus
  occurrence disambiguation; distinct same-provenance witnesses and swapped
  probability masses cannot collide during complete-result comparison;
- explicit wire tags survive a simulated Python type rename/module move,
  while a genuinely new unregistered sealed owner type still fails closed;
- context-sensitive records, invalid semantic payloads, forged enum
  singletons, bool/rational version impostors, and bool/int-collapsed
  structures cannot encode;
- a newly added public sealed owner type fails registry initialization until
  explicitly registered;
- lone-surrogate Python strings encode canonically, and recursive
  type-sensitive revalidation fails closed rather than using Python's loose
  equality;
- all exact representation profiles and the explicit lossy/approximate
  distinctions survive the codec;
- each actual PX10 relation point executes real mechanics through the same
  program, while the independent expected graph is never obtained from the
  relation under test;
- prefix creation, interval continuation, pointer reconstruction, fresh
  region children, explicit basis projection, causal residual
  reconstruction, and XOR tag/order/involution cannot be replaced by a
  precomputed answer sidecar; and
- one fixed native/represented conjugate pair proves both domain points,
  including complete witnesses, dispositions, cardinalities, fibers,
  measures, continuation, fresh bindings, lineage, and application evidence.

No production API correction was required by the reopened mechanics evidence.
The valid dependency direction is codec-to-owner: serialization imports the
seven sealed owner modules, while no owner imports serialization.

### Verification

The completed tree passed:

```text
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs \
  tests/test_serialization.py \
  tests/test_alphabets.py \
  tests/test_loci.py \
  tests/test_rules.py \
  tests/test_program.py \
  tests/test_public_api.py \
  tests/conformance/test_codec_inventory.py \
  tests/conformance/test_serialization_contract.py \
  tests/conformance/test_representation_commutation.py \
  tests/conformance/test_observer_boundary.py
-> 178 passed, 1 skipped

UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q \
  tests/conformance/test_representation_commutation.py \
  tests/conformance/test_family_coverage.py
-> 87 passed, 2 skipped

UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs tests
-> 413 passed, 13 skipped

UV_CACHE_DIR=/tmp/uv-cache uv lock --check
-> resolved successfully

deterministic hostile-byte decode probe
-> 5,000 inputs returned a typed total result

git diff --check
-> pass
```

Static inspection additionally established:

- registry counts are exactly `178 types / 387 variants / 178 unique tags`;
- exactly one production `apply` remains, in `src/ca/program.py`;
- no semantic owner imports serialization;
- neither serialization nor program imports catalog;
- serialization contains no pickle, dynamic import, unsafe evaluator, RNG,
  or NumPy fallback;
- no catalog path or frozen Goal 2, Goal 5, or Goal 6 path changed from the
  G7-03 baseline; and
- the 13 retained skips are exactly five CT11 catalog-expansion tests, five
  catalog unit tests, two catalog portions of family coverage, and one
  callable-free role-metadata test. All belong to G7-04.

No migration was needed or implemented for the new canonical v1 schema;
unknown and legacy versions reject. G7-03 is complete. The first G7-04 action
is to create `5-CATALOG.md`, resync the inert catalog shells against the exact
Goal 6 migration ledger, and activate only catalog-owned behavior. No G7-04
file or implementation began here.

### G7-04 dependency reopening

The later preset-domain audit reopened G7-02 for reusable closed mechanics
that were not present in the original 387-row inventory. G7-03 is consequently
reopened-pending: once the mechanics delta closes, every new sealed type,
field, enum member, expression primitive, evidence value, and exact
representation must be added to the explicit codec registry and inventory,
round-tripped, mutation-tested, and included in the hostile fail-closed gate.

The existing schema version remains `1` unless the new mechanics force a wire
incompatibility. This reopening does not authorize catalog tags, constructor
receipts, permissive migration, or a second codec.

### G7-04 dependency reclosure

The reopened stage resumed from clean commit
`a36cfe1aee7cb2d658c72c97350d2c9e9a787f47`, after G7-02's preset
mechanics and final record were complete. Its baseline was
`804 passed, 11 skipped`; every skip was already G7-04-owned.

The inventory and production registry were mechanically complete at entry,
but the audit rejected the shortcut of treating one record inhabitant per
type as exhaustive evidence. The exact delta from the original closed G7-03
surface is:

- nine additional sealed owner types;
- fifty-four additional inventory variants;
- four expanded version-1 record shapes;
- fifty additional enum members; and
- twenty-nine additional `ExpressionPrimitive` members.

The live totals remain exact at `187 owner types / 441 variants`:
`141` frozen-record representatives and every one of `300` enum members.
The four expanded records are `WritableRegion`, `ReadDependency`,
`ReadableRegion`, and `CapabilitySelector`; their new fields are required,
and wire forms that omit them reject rather than acquiring defaults.

Requirement-specific codec evidence now goes beyond the aggregate type count:

- all twenty-nine reopened Rule-expression primitives have inhabitable
  canonical round trips and hostile argument-shape mutations;
- fixed, periodic, and reflective windows; all three rewrite scans; and
  independent plus fixed/periodic/reflective contextual mosaics retain
  distinct exact bytes;
- mixed string/integer value paths, all five predicate forms, all three anchor
  cardinalities, rational intervals, symbolic-expression alphabets,
  semantic-key maps, pattern/template rewrite bundles, rank-four dense
  fields, and rank-four configurations/programs round-trip;
- actual value-anchored writable/readable/dependency/view records,
  group-item selectors, all three conflict policies, anchored denotations,
  complete anchored Rules/programs, and their `ApplicationComplete` results
  round-trip and re-encode identically; and
- complete public application results for composite/comprehension,
  pattern-rewrite, and mosaic mechanics cross the same codec boundary.

Hostile signed-wire tests cover unknown values for every affected enum schema,
missing or invalid expanded fields, malformed paths and predicates, reordered
or incomplete interval descriptors, noncanonical structural ordering,
duplicate semantic map keys, forged window/scan/offset forms, invalid
group-item operands, non-group anchored proposals, proposed zero-anchor
writes, impossible anchored regions/views, and pre-delta record shapes.

The hostile review exposed three real owner-validation gaps and repaired them
without changing the public API or codec algorithm:

- `IntensionalReadableView` now rejects finite value-anchor dependencies;
- `ReadableView` checks the declared anchor cardinality against distinct
  realized source anchors; and
- `Rule` itself, not only the public builders, checks ordinary and anchored
  clause denotations' required write effects and replay-key requirements.

Those checks are necessary because a fail-closed decoder reconstructs public
records directly through their owner validators. The codec still does not
dispatch on `ValueNode` tags: malformed specialized grid, pattern, or rewrite
conventions remain valid generic structural values until their declared
specialized parser or Rule operation consumes them.

No new `RepresentationRelation` was introduced by the preset-mechanics
delta. The eight exact PX10 relations and their complete-result commutation
test are byte-for-byte unchanged from the catalog baseline and passed again.
Lossy, approximate, and out-of-image qualifications remain explicit.

Schema version `1` remains correct. The earlier G7-03 bytes were an internal,
explicitly nonpublishable Goal 7 checkpoint, not a released compatibility
surface. This reclosure replaces that draft before the first `0.2.0` release;
the four expanded record shapes are the canonical v1 shapes, and draft blobs
missing their required fields fail closed. No migration or fallback decoder
was added.

The reclosed tree passed:

```text
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs \
  tests/test_serialization.py \
  tests/test_neighborhoods.py \
  tests/test_rules.py \
  tests/test_anchored_rule_kernel.py \
  tests/test_value_anchored_regions.py
-> 167 passed

UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs \
  tests/test_rule_comprehensions.py \
  tests/test_pattern_rewrite.py \
  tests/test_mosaic_substitution.py \
  tests/test_reopened_mechanics_apply.py \
  tests/test_composite_values.py \
  tests/test_structural_values.py \
  tests/test_rank_interval_dynamic_width.py
-> 188 passed

UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs \
  tests/conformance/test_codec_inventory.py \
  tests/conformance/test_serialization_contract.py \
  tests/conformance/test_representation_commutation.py \
  tests/conformance/test_observer_boundary.py \
  tests/conformance/test_import_and_dispatch.py
-> 61 passed, 1 G7-04-owned skip

UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q -rs tests
-> 829 passed, 11 skipped

UV_CACHE_DIR=/tmp/uv-cache uv lock --check
-> resolved successfully

UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall -q src tests
-> pass

deterministic hostile-byte decode probe
-> 5,000 inputs returned typed total results

git diff --check
-> pass
```

The eleven skips remain exactly five CT11 catalog-expansion tests, five
catalog unit tests, and the F010/F042 callable-free role test. Static gates
also prove five stored program fields, 187 unique v1 tags, exactly one
production `apply`, rollout calling it, frozen Goals 2/5/6, catalog-free
serialization, and the owner-to-codec import direction.

G7-03 is reclosed. G7-04 is resumable at its preset and compatibility
implementation gate; no catalog behavior was implemented during this codec
stage, and Goal 7 is not release-ready.
