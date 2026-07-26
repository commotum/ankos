# Historical Visualization Design Conversation

> **Superseded design transcript:** This conversation predates the 0.2.0
> five-field runtime and uses removed `Dynamics`/`RawEpisode`/`RawBatch`
> spellings. It is retained as design history, not current API guidance. See
> [`README-V2.md`](README-V2.md) and [`api.md`](api.md) for current usage.

Jake:
I need to create a visualizer for this library. I want something ultra-fast, and ultra-lightweight. What's the best way for me to do this? Ideally we build something custom, not use an existing 3D or 2D graphics library since that comes with so much baggage and extra code. Like I want something super thin and fast.

ChatGPT:
I’ll ground the design in ANKoS’s actual rollout data, treating the visualizer as a thin renderer over RawEpisode/RawBatch NumPy arrays rather than a graphics engine. The goal is direct array-to-pixel/voxel rendering, with separate minimal paths for 1D, 2D, and 3D.

The best fit is a **custom raster/texture visualizer**, not a general 2D/3D graphics engine.

ANKoS already gives you the perfect renderer input: raw NumPy-compatible state arrays plus optional canonical `[t, x, y, z]` coordinates. `ca.rollout(...)` returns `RawEpisode.states` and optional `coords`, and the rollout layer explicitly avoids tokens, masks, torch tensors, device policy, and model-facing metadata.  For batches, `ca.rollout_batch(...)` returns `(B, T, *spatial_shape)` states with shared `(T * cell_count, 4)` coords, so the visualizer can handle many episodes without inventing a new data model.  The package is also intentionally light already: its project dependencies are just NumPy and pytest. 

## Recommendation

Build a **tiny browser-based viewer** with:

```text
Python / ANKoS
  -> RawEpisode or RawBatch
  -> compact binary state buffer + JSON header
  -> browser viewer

Browser viewer
  -> Canvas2D fast path for simple raster previews
  -> WebGL2 texture path for large/animated views
  -> optional WebGPU later only if needed
```

Do **not** start with Three.js, PixiJS, matplotlib, pyglet, pygame, VTK, VisPy, or a 3D scene graph. For cellular automata, the primitive is not “objects in a scene”; it is **dense integer fields over time**. Treat states as images/textures.

## Why this is the right shape

ANKoS trajectories are natively shaped like:

```text
t+0d: (T,)
t+1d: (T, X)
t+2d: (T, X, Y)
t+3d: (T, X, Y, Z)
```

and canonical coordinates use `[t, x, y, z]` across scalar through 3D systems.  That means visualization should mostly be a matter of picking a view into `states`, mapping integer state values through a palette, and drawing pixels.

## Minimal renderer modes

For the first version, support four views:

```text
t+0d
  strip chart: time on x, value as color or y position

t+1d
  spacetime bitmap: x on horizontal axis, t on vertical axis

t+2d
  frame viewer: x/y image for selected t
  optional tiled mode: many t slices in a grid

t+3d
  orthogonal slice viewer: xy / xz / yz at selected index
  optional projection: max, sum, first-active, or opacity projection
```

That covers nearly everything useful without building “real 3D.” For 3D cellular automata, slice/projection views are often more informative than a voxel scene anyway.

## Rendering backend choice

Use **Canvas2D first** for the MVP. It is extremely small: make an `ImageData`, fill its `Uint8ClampedArray`, and call `putImageData`. MDN documents `putImageData()` as the Canvas 2D method for painting an `ImageData` object, with optional dirty rectangles for partial updates. ([MDN Web Docs][1])

Then add **WebGL2 texture rendering** as the fast path. WebGL2 gives you a canvas rendering context based on OpenGL ES 3.0 without pulling in a graphics library. ([MDN Web Docs][2]) The implementation can be tiny: one full-screen quad, one texture containing state IDs, one palette texture, one fragment shader.

Use **OffscreenCanvas + Worker** when the UI starts feeling blocked. `transferControlToOffscreen()` transfers a canvas to an `OffscreenCanvas`, including for worker use, and OffscreenCanvas can be used detached from the DOM. ([MDN Web Docs][3]) Web Workers let long-running processing happen off the main UI thread. ([MDN Web Docs][4])

Keep **WebGPU** as a later backend. It is powerful, especially for compute-heavy projection or volume rendering, and MDN describes it as a successor to WebGL with better modern GPU access and general-purpose GPU computation. ([MDN Web Docs][5]) But it has more boilerplate than you need for the first visualizer.

## Concrete architecture

```text
ankos/
  src/ca/
    viz/
      __init__.py
      export.py          # RawEpisode/RawBatch -> compact binary bundle
      server.py          # optional stdlib local viewer server
      static/
        index.html
        ankos-viz.js
        render2d.js
        rendergl.js
```

Keep the core package clean by making this either:

```text
ca.viz
```

with no third-party dependencies, or a separate tiny package:

```text
ankos-viz
```

that imports `ca`.

The cleanest first version is a **static viewer plus exporter**:

```python
ca.viz.export_episode(episode, "rule30.ankos")
```

where `.ankos` is just:

```text
[fixed magic bytes]
[uint32 json_header_length]
[JSON header]
[raw state bytes]
```

Header example:

```json
{
  "version": 1,
  "kind": "RawEpisode",
  "domain": "t+2d",
  "shape": [11, 11],
  "steps": 64,
  "dtype": "uint8",
  "layout": "TXY",
  "alphabet": [0, 1],
  "rule_id": 30
}
```

This is faster and simpler than teaching the browser to parse `.npy` or `.npz`.

## Rendering loop

The core loop should be this simple:

```text
1. Load header.
2. Load state buffer as Uint8Array / Uint16Array / Float32Array.
3. Pick view:
   - t+1d: use whole (T, X) as image.
   - t+2d: use states[t].
   - t+3d: extract slice or projection.
4. Map state value -> RGBA.
5. Draw.
```

For Canvas2D:

```js
for (let i = 0; i < cellCount; i++) {
  const v = state[offset + i];
  const p = palette[v];
  rgba[4*i + 0] = p[0];
  rgba[4*i + 1] = p[1];
  rgba[4*i + 2] = p[2];
  rgba[4*i + 3] = 255;
}
ctx.putImageData(imageData, 0, 0);
```

For WebGL2:

```text
CPU:
  upload state IDs as one texture
  upload palette as tiny texture

GPU:
  fragment shader samples state ID
  fragment shader maps ID through palette
  output color
```

That avoids expanding every state into RGBA on the CPU every frame.

## Important performance rules

Use these constraints from day one:

```text
Use typed arrays only.
Never create per-cell objects.
Never render cells as DOM elements.
Never draw one rectangle per cell unless debugging tiny grids.
Never recompute coordinates per frame.
Never copy if a view/slice can be represented as offset + stride.
Use nearest-neighbor scaling.
Use one canvas.
Use one texture upload per frame.
Use palettes, not per-cell style logic.
```

For `t+1d`, the fastest visual is usually the whole spacetime diagram in one shot. For `t+2d`, upload one time slice per frame. For `t+3d`, start with slices; full voxel rendering is a later feature.

## What I would build first

Build this in order:

```text
1. Pure JS static viewer
   - load .ankos file
   - Canvas2D render path
   - support t+1d spacetime and t+2d frames

2. Python exporter
   - RawEpisode -> .ankos
   - RawBatch row selection -> .ankos

3. WebGL2 renderer
   - one quad
   - state texture + palette texture
   - nearest-neighbor zoom/pan

4. 3D slice/projection UI
   - xy/xz/yz slice
   - selected t
   - selected z/y/x
   - max/sum/first-active projection

5. Optional local live mode
   - stdlib HTTP server
   - endpoint returns latest header/state buffer
   - browser polls or requests frames
```

This gets you a useful visualizer quickly while staying very thin.

## My preferred API

```python
import ca
from ca.viz import save_viewer_bundle

episode = ca.rollout(
    dynamics=dynamics,
    rule_id=rule_id,
    seed_state=seed_state,
    steps=128,
)

save_viewer_bundle(
    episode,
    "out/rule_030.ankos",
    palette="binary",
)
```

For batches:

```python
batch = ca.rollout_batch(
    dynamics=dynamics,
    rule_ids=rule_ids,
    seed_states=seed_states,
    steps=128,
)

save_viewer_bundle(
    batch,
    "out/batch.ankos",
    row=0,
)
```

## One design decision I would make now

Do **not** visualize from `coords` by default. Use `states` layout directly.

`coords` are useful for overlays, transformed coordinate experiments, picking, and debugging. But for dense CA rendering, `states` already has the native memory layout you want. The docs explicitly define `states` as the raw CA array and `coords` as optional materialized canonical coordinates.  Rendering from `coords` would be slower and more complex.

## Bottom line

Build a **custom texture viewer**:

```text
NumPy states
  -> compact binary state buffer
  -> Canvas2D for MVP
  -> WebGL2 for fast path
  -> OffscreenCanvas worker when needed
```

That gives you the “ultra-fast, ultra-lightweight” path without inheriting the baggage of a graphics engine. The renderer core can stay under a few hundred lines of JavaScript, and the Python side can be a small exporter plus optional stdlib server.

[1]: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/putImageData?utm_source=chatgpt.com "CanvasRenderingContext2D: putImageData() method"
[2]: https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext?utm_source=chatgpt.com "WebGL2RenderingContext - Web APIs - MDN - Mozilla"
[3]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/transferControlToOffscreen?utm_source=chatgpt.com "HTMLCanvasElement: transferControlToOffscreen() method"
[4]: https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API?utm_source=chatgpt.com "Web Workers API - MDN - Mozilla"
[5]: https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API?utm_source=chatgpt.com "WebGPU API - Web APIs | MDN - Mozilla"
