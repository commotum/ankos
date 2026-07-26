# Historical ANKoS 0.1 Visualization Feature Spec

> **Superseded design record:** The specification below was written against
> the removed 0.1 `Dynamics`, `RawEpisode`, and `RawBatch` surface. Its bundle
> format history remains useful, but its Python API examples are not current.
> ankos 0.2.0 visualization consumes explicit downstream
> `DatasetEpisode`/`DatasetBatch` views; see [`README-V2.md`](README-V2.md),
> [`api.md`](api.md), and `src/ca/viz/`.

## Purpose

Add an ultra-lightweight visualization feature for ANKoS that renders raw CA
rollouts directly from NumPy state arrays. The feature should stay close to the
current project shape: small, explicit, dependency-light, and centered on
experiments rather than graphics-engine abstractions.

The design is derived from `render-chat.md` and the current repository API. The
core idea is:

```text
ca.RawEpisode or ca.RawBatch
  -> compact .ankos binary bundle
  -> static browser viewer
  -> Canvas2D MVP
  -> WebGL2 fast path later
```

The renderer should treat cellular automata as dense fields over time, not as
objects in a scene.

## Verified Basis

This spec was checked against the current repository and browser/platform
primitives.

Repo facts:

- `ca.rollout(...)` and `ca.rollout_batch(...)` are the only current trajectory
  generation paths.
- `RawEpisode.states` is `(T, *shape)`.
- `RawBatch.states` is `(B, T, *shape)`.
- Current executable rollout families materialize `states` as integer NumPy
  arrays, usually `int64` with small binary or modular values.
- `coords` are optional and may be omitted with `return_coords=False`.
- Batch coordinates, when present, are shared across rows and do not include a
  batch axis.
- The current package has no `ca.viz` module and no browser assets.

Platform facts:

- Browser file-picker input can be read into an `ArrayBuffer` with
  `Blob.arrayBuffer()` or `FileReader.readAsArrayBuffer()`.
- Canvas `ImageData` is an RGBA row-major pixel buffer backed by a typed array.
- `CanvasRenderingContext2D.putImageData()` directly paints an `ImageData`
  buffer to a canvas.
- WebGL2 is available from `canvas.getContext("webgl2")` and can upload 2D
  textures with `texImage2D`.
- `OffscreenCanvas` can move rendering work away from the DOM/main thread, but
  it should be deferred until Canvas2D UI blocking is measurable.
- Python `http.server` is suitable for a local convenience server, but it is not
  a production server.

## Repository Context

ANKoS is currently a compact Python package imported as `ca`.

Relevant public runtime path:

```text
ca.Dynamics + rule_id + seed_state + steps
    -> ca.rollout(...)
    -> ca.RawEpisode
```

Relevant batch path:

```text
ca.Dynamics + rule_ids + seed_states + steps
    -> ca.rollout_batch(...)
    -> ca.RawBatch
```

Current dependencies are only NumPy and pytest. Visualization should not add a
graphics dependency to normal rollout, seed, rule, neighborhood, or coordinate
code.

Current state layouts:

```text
RawEpisode.states
  t+0d: (T,)
  t+1d: (T, X)
  t+2d: (T, X, Y)
  t+3d: (T, X, Y, Z)

RawBatch.states
  t+0d: (B, T)
  t+1d: (B, T, X)
  t+2d: (B, T, X, Y)
  t+3d: (B, T, X, Y, Z)
```

`coords` are optional canonical `[t, x, y, z]` arrays. They are useful for
overlays, picking, debug views, and coordinate experiments, but the primary
renderer must use `states` directly for speed.

## Goals

- Render ANKoS trajectories without matplotlib, Pillow, pygame, pyglet, PixiJS,
  Three.js, VTK, VisPy, or another scene graph.
- Preserve the library's direct NumPy model: no token ids, no torch tensors, no
  PE/model batching concepts, and no DOM-per-cell rendering.
- Support all current domains: `t+0d`, `t+1d`, `t+2d`, and `t+3d`.
- Provide a static browser viewer that can open a local `.ankos` bundle through
  a file picker.
- Provide a Python exporter under `ca.viz` that writes compact binary bundles.
- Keep the MVP useful with Canvas2D before adding WebGL2.
- Make large rollouts possible by storing compact typed state buffers and
  mapping values through palettes.

## Non-Goals

- No full voxel renderer in the MVP.
- No live notebook widget in the MVP.
- No graphics library, build chain, TypeScript compiler, bundler, or frontend
  framework in the MVP.
- No changes to `ca.rollout`, `ca.rollout_batch`, rule semantics, seed
  rendering, or coordinate generation.
- No model-facing serialization, tokenizer behavior, or PE integration.
- No dependency on `coords` for dense rendering.

## Feature Shape

Add a new optional visualization subpackage:

```text
src/ca/viz/
|-- __init__.py
|-- export.py          # RawEpisode/RawBatch -> .ankos bundle
|-- format.py          # binary format constants and helpers
|-- server.py          # optional stdlib local server
`-- static/
    |-- index.html
    |-- ankos-viz.js   # bundle parser and app state
    |-- render2d.js    # Canvas2D renderer
    `-- rendergl.js    # later WebGL2 fast path
```

The static viewer should be usable without a Python server:

```text
open src/ca/viz/static/index.html
select a .ankos file
inspect the rollout
```

To preserve `file://` usability, the MVP viewer must use classic browser
scripts or inline JavaScript. It must not require ES module loading, `fetch()`
of local files, npm, a bundler, or a dev server. Bundle bytes should come from
the user's selected `File` object through `Blob.arrayBuffer()`.

The optional server is a convenience wrapper around the standard library HTTP
server, not a web framework.

## Public Python API

MVP API:

```python
from ca.viz import save_viewer_bundle

save_viewer_bundle(
    source,
    "out/run.ankos",
    palette="auto",
    row=None,
    include_coords=False,
    storage_dtype="auto",
    title=None,
    metadata=None,
)
```

Arguments:

- `source`: `ca.RawEpisode` or `ca.RawBatch`.
- `path`: output `.ankos` file path.
- `palette`: `"auto"`, `"binary"`, `"categorical"`, `"heat"`, or an explicit
  list of RGBA colors.
- `row`: optional batch row selection. For MVP, `RawBatch` requires `row=int`.
  `row=None` is valid only for `RawEpisode`.
- `include_coords`: writes `coords` into the bundle when available. Default is
  `False`.
- `storage_dtype`: `"auto"` chooses a compact unsigned state buffer. Explicit
  MVP values are `"uint8"` and `"uint16"`. Signed or large raw values should be
  represented through `value_map` codes rather than drawn directly.
  `"int32"`/`"float32"` state storage is deferred until the viewer has explicit
  numeric plot modes for those arrays.
- `title`: optional display title.
- `metadata`: optional JSON-safe metadata merged into bundle metadata.

Return value:

```python
VizBundleInfo(
    path: str,
    kind: str,
    domain: str,
    state_shape: tuple[int, ...],
    state_storage_dtype: str,
    storage_mode: str,
    bytes_written: int,
)
```

Convenience API:

```python
from ca.viz import serve

serve("out/run.ankos", port=0)
```

`port=0` should pick an available port and print the local viewer URL.

## `.ankos` Bundle Format

The bundle is a simple binary file:

```text
8 bytes   magic: ASCII "ANKOSV1\0"
4 bytes   little-endian unsigned padded header length
N bytes   UTF-8 JSON header plus ASCII space padding
M bytes   raw payload buffers
```

The exporter must pad the header so the payload base offset
`12 + header_length` is divisible by 8. This keeps typed-array views aligned for
`Uint16Array`, `Int32Array`, and optional coordinate buffers. The JSON parser
can accept trailing whitespace in the header bytes.

All payload offsets in the header are relative to the aligned payload base.

Header example:

```json
{
  "format": "ankos.viz.bundle",
  "version": 1,
  "kind": "RawEpisode",
  "domain": "t+2d",
  "shape": [128, 128],
  "steps": 256,
  "title": "dyadaxes rule 91",
  "rule_id": 91,
  "states": {
    "layout": "TXY",
    "shape": [256, 128, 128],
    "source_dtype": "int64",
    "storage_dtype": "uint8",
    "storage_mode": "raw",
    "byte_offset": 0,
    "byte_length": 4194304,
    "byte_order": "little"
  },
  "coords": null,
  "value_map": null,
  "palette": {
    "name": "binary",
    "colors": [[255, 255, 255, 255], [0, 0, 0, 255]]
  },
  "metadata": {
    "boundary": {"policy": "fixed", "value": 0}
  }
}
```

Layout strings:

```text
RawEpisode:
  t+0d: T
  t+1d: TX
  t+2d: TXY
  t+3d: TXYZ

RawBatch:
  t+0d: BT
  t+1d: BTX
  t+2d: BTXY
  t+3d: BTXYZ
```

MVP `RawBatch` row export writes one selected row with `kind="RawEpisode"` and
the corresponding episode layout. `RawBatch` layout strings are reserved for
the deferred full-batch bundle format.

If stored values are compact codes instead of raw values, the header must
include:

```json
"value_map": {
  "code_dtype": "uint8",
  "raw_dtype": "int64",
  "values": [0, 1, 5, 8]
}
```

In that case, `states.storage_mode` must be `"indexed"`. The renderer maps
state code `i` to `value_map.values[i]` for labels and to `palette.colors[i]`
for drawing. For current built-in binary and AR2 examples, raw integer storage
is expected to be enough.

Optional `coords` payload:

```json
"coords": {
  "layout": "N4",
  "shape": [4194304, 4],
  "source_dtype": "int64",
  "storage_dtype": "int32",
  "byte_offset": 4194304,
  "byte_length": 67108864,
  "byte_order": "little"
}
```

The exporter should store coords as `int32` after a range check. If any
coordinate exceeds `int32`, export should fail with a clear error rather than
silently losing precision.

## Export Rules

The exporter must:

- Accept only `RawEpisode` and `RawBatch`.
- Validate that `states` is numeric and C-contiguous after conversion.
- Treat integer states as the MVP path because current rollout emits integer
  arrays.
- Store the drawable state payload as unsigned codes.
- Use raw `uint8` when values are already dense non-negative codes in
  `0..255`.
- Use raw `uint16` when values are already dense non-negative codes in
  `0..65535`.
- Use indexed storage plus `value_map` when raw values are sparse, negative, or
  too large but the number of distinct values is small enough for compact
  codes.
- Reject states with more than 65,536 distinct values in the MVP unless an
  explicit large-value mode is added.
- Reject float states in the MVP unless float support is implemented
  deliberately with tests.
- Reject object arrays.
- Reject string/symbolic states in the MVP. The current executable rollout path
  does not produce them.
- Preserve native state layout in the bundle.
- Store `coords` only when `include_coords=True`.
- Merge source metadata and caller metadata into JSON-safe metadata.
- Never mutate the source episode or batch.

For `RawBatch`, MVP behavior should be:

```text
row=int
  -> export one selected row using episode layout
  -> preserve original batch metadata and selected rule_id

row=None
  -> reject with a clear error in MVP
```

## Viewer Modes

The viewer should choose a default mode from `domain`, with explicit controls
for alternatives.

### `t+0d`

Views:

- Color strip: time on x, value mapped through palette.
- Value plot: time on x, numeric value on y for scalar recurrences.

MVP requirement:

- Color strip.

### `t+1d`

Views:

- Spacetime bitmap: x on the horizontal axis, t on the vertical axis.
- Optional row cursor for current time.

MVP requirement:

- Full spacetime bitmap in one draw.

### `t+2d`

Views:

- Frame viewer: selected time `t` as an x/y image.
- Playback controls over time.
- Optional tiled mode showing many time slices in a grid.

MVP requirement:

- Frame viewer with time slider and play/pause.

Display mapping:

- Preserve native memory order in storage.
- Display x horizontally and y vertically.
- The renderer may transpose from native `(X, Y)` memory to display rows as
  needed.
- For native state index `(t, x, y)`, the Canvas pixel index is `(x, y)` with
  `width=X` and `height=Y`, so the RGBA expansion loops display rows by `y`
  while reading source values by `(x, y)`.

### `t+3d`

Views:

- Orthogonal slices: `xy`, `xz`, or `yz` at selected index.
- Projection: `max`, `sum`, `first-active`, or opacity projection.

MVP requirement:

- Orthogonal slice viewer for selected `t`.

Slice mapping:

- `xy`: width `X`, height `Y`, fixed `z`.
- `xz`: width `X`, height `Z`, fixed `y`.
- `yz`: width `Y`, height `Z`, fixed `x`.

Full voxel rendering is deferred.

## Viewer Controls

The static viewer should provide:

- File picker for `.ankos`.
- View mode selector.
- Time slider.
- Play/pause and step controls for animated views.
- Batch row selector once full-batch bundles are supported.
- Slice axis and slice index controls for `t+3d`.
- Projection selector for `t+3d`.
- Palette selector.
- Zoom, pan, and reset.
- Cell inspector showing raw value and coordinates for the hovered cell when
  enough mapping information is available.

The main surface should be one canvas. Do not render cells as DOM nodes.

## Canvas2D MVP

Canvas2D should be the first renderer because it needs no shader setup and no
third-party code.

Renderer loop:

```text
1. Select a logical view into the typed state buffer.
2. Expand state values or compact codes into an ImageData RGBA buffer.
3. Put the ImageData into an offscreen/native-resolution canvas.
4. Draw that canvas into the visible canvas with image smoothing disabled.
```

Rules:

- Use typed arrays only.
- Reuse `ImageData` buffers where dimensions do not change.
- Use nearest-neighbor scaling.
- Set `imageSmoothingEnabled = false` on the visible canvas context.
- Avoid per-cell objects.
- Avoid one rectangle draw call per cell except for tiny debug cases.
- Avoid recomputing coordinates per frame.
- Represent slices by offset and stride when possible.

## WebGL2 Fast Path

Add WebGL2 after Canvas2D is correct.

Target architecture:

```text
CPU:
  upload state IDs as a texture
  upload palette as a tiny RGBA texture

GPU:
  render one full-screen quad
  fragment shader samples state ID
  fragment shader maps state ID through palette
  output RGBA
```

Implementation constraints:

- One canvas.
- One full-screen quad.
- One state texture per frame or view.
- One palette texture.
- Nearest-neighbor sampling.
- No scene graph.
- Prefer WebGL2 integer textures for indexed state codes, such as `R8UI` or
  `R16UI` with integer samplers. If that path becomes too much for the first
  GPU pass, upload CPU-expanded RGBA textures as a fallback.

For large `t+1d` spacetime diagrams, upload the whole `T x X` state image once
when possible. For `t+2d`, upload or reinterpret one time slice per frame. For
`t+3d`, start with slices and projections.

## Worker and OffscreenCanvas

Defer worker rendering until UI blocking is measurable.

When added:

- Use `OffscreenCanvas` only for rendering or heavy palette expansion.
- Keep parsing and file ownership explicit.
- Transfer buffers instead of copying when possible.
- Keep a main-thread fallback.

## Palette Rules

Built-in palettes:

- `binary`: value/code `0` is white, value/code `1` is black.
- `categorical`: deterministic distinct colors for small finite alphabets.
- `heat`: numeric scalar gradient for scalar recurrence views.
- `gray`: monotone grayscale.

`palette="auto"` should choose:

```text
binary values {0, 1}       -> binary
integer values <= 32       -> categorical
scalar numeric t+0d values -> heat or gray
otherwise                  -> categorical hash with inspector labels
```

The renderer should use palette lookup rather than per-cell style logic.

## Local Server

`ca.viz.serve(...)` should use only the Python standard library.

Responsibilities:

- Serve `static/index.html` and JS files.
- Serve one selected `.ankos` file with the correct content type.
- Print the URL.
- Bind to `127.0.0.1` by default.
- Avoid long-running background processes unless the caller keeps the server
  alive.

No Flask, FastAPI, or ASGI server should be introduced.

## Testing

Add focused tests:

```text
tests/test_viz_export.py
```

Python tests should cover:

- RawEpisode export for `t+0d`, `t+1d`, `t+2d`, and `t+3d`.
- RawBatch row export.
- Header magic/version/schema.
- Header padding and 8-byte payload alignment.
- Header payload offsets and byte lengths.
- Safe dtype downcasting.
- Indexed storage and `value_map` for sparse small alphabets.
- Explicit `storage_dtype` validation.
- `include_coords=False` default.
- `include_coords=True` when coords are present.
- Coord int32 range validation.
- Object dtype rejection.
- Float and symbolic state rejection until those modes are intentionally added.
- Existing `uv run pytest -q` remains green.

Static JS can initially be tested with a tiny checked-in HTML fixture and manual
browser verification. If automated JS tests are added, they should not require
a frontend build chain.

## Acceptance Criteria

MVP is complete when:

- `ca.viz.save_viewer_bundle(...)` writes a valid `.ankos` file for
  `RawEpisode`.
- `RawBatch` can be exported with `row=int`.
- The static viewer loads a `.ankos` file through a file picker.
- `t+1d` episodes render as spacetime bitmaps.
- `t+2d` episodes render as time-selectable frames.
- `t+0d` episodes render as a time strip.
- `t+3d` episodes render as orthogonal slices.
- Rendering uses `states` directly, not `coords`.
- Binary payloads are aligned and can be parsed as typed-array views without
  copying.
- No runtime visualization dependency is added to the core package.
- Existing tests pass.

## Implementation Plan

1. Add `src/ca/viz/format.py` and `src/ca/viz/export.py`.
2. Add Python tests for bundle export and dtype behavior.
3. Add `src/ca/viz/static/index.html`, `ankos-viz.js`, and `render2d.js`.
4. Implement bundle parsing in browser typed arrays.
5. Implement Canvas2D rendering for `t+0d`, `t+1d`, and `t+2d`.
6. Add `t+3d` orthogonal slice mode.
7. Add `server.py` convenience serving.
8. Add WebGL2 renderer behind feature detection.
9. Add full RawBatch viewer support with row selector and optional atlas view.

## Deferred Work

- Full-batch `.ankos` bundles with row selector.
- Batch atlas or comparison grid.
- Float-valued rollout visualization.
- Symbolic value rendering once executable rollout supports symbolic states.
- WebGL2 state and palette texture renderer.
- OffscreenCanvas worker rendering.
- Projection acceleration for large `t+3d` volumes.
- Full voxel or isosurface rendering.
- Export snapshots to PNG.
- Live polling mode for long-running experiments.
- Viewer-side overlays from `coords`.

## Research References

- MDN `Blob.arrayBuffer()`:
  https://developer.mozilla.org/en-US/docs/Web/API/Blob/arrayBuffer
- MDN `ImageData`:
  https://developer.mozilla.org/en-US/docs/Web/API/ImageData
- MDN `CanvasRenderingContext2D.putImageData()`:
  https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/putImageData
- MDN `WebGL2RenderingContext`:
  https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext
- MDN `texImage2D()`:
  https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/texImage2D
- MDN `OffscreenCanvas`:
  https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas
- Python `http.server`:
  https://docs.python.org/3/library/http.server.html
- NumPy `ndarray.tobytes()`:
  https://numpy.org/doc/stable/reference/generated/numpy.ndarray.tobytes.html
