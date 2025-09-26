# ZENØ — Living Polyhedron System (v2.0 Refactored)

Interactive, multi‑layered polyhedron rendered with **Three.js**.  
Emphasis on **modular architecture**, **rhythmic animation**, per‑layer styling, and a clean **post‑processing** pipeline.

> **Status (v2.0):** Stable single‑file HTML demo with modularized classes inside. Bloom wired; **selective bloom masking in progress**.

---

## ⏱ Quick Start

This project uses ES modules and an **import map**. Serve over HTTP (not `file://`).

```bash
# Option A — Python
python -m http.server 8000

# Option B — Node
npx http-server -p 8000
```

Open: `http://localhost:8000/zeno-polyhedron-refactored.html`


## Requirements
- Modern browser with **WebGL2** enabled
- Local HTTP server (ES modules + import map will not load from `file://`)

---

## 🎮 Controls

```
Space       → Pause/Resume animation
R           → Reset camera view and state
P           → Toggle performance monitor
B           → Toggle bloom on/off
S           → Toggle custom shaders (outer layer; Phase 3 hook)
I           → Adjust shader intensity (when shaders enabled)
1 / 2 / 3   → Switch system state (CALM / ALERT / DEFENSIVE)
H           → Toggle help/controls overlay
F           → Toggle fullscreen
```

OrbitControls are enabled with damping; use mouse/touch to orbit and zoom.

---

## 🧩 Features

- **Layered Polyhedron Stack** — Solid **core** + multiple **wireframe shells** (named layers) with independent scale, color, and complexity.
- **Rhythmic Animation** — Core “breathing”, counter‑rotations, opacity & vertex pulsing with per‑layer phase offsets.
- **Post‑Processing (Bloom v1)** — EffectComposer with `RenderPass → UnrealBloomPass → OutputPass`.
  - **Selective Bloom (in progress):** objects can be tagged to a bloom layer; masked dual‑pass composite is staged next.
- **Custom Shader Hooks (Phase 3)** — `ShaderManager` scaffolding for energy‑flow / Fresnel / holographic variants on the outer “Gates” layer.
- **System State HUD** — CALM / ALERT / DEFENSIVE with live integrity/sync indicators.
- **Performance Monitor** — FPS, draw calls, triangles, and resource **counts** (geometries / textures).
- **Responsive UI** — Legend, status line, controls helper, performance panel.
- **Resource Management** — Geometries/materials are registered and disposed on teardown.

> **Note on line thickness:** `LineBasicMaterial.linewidth` is driver‑limited in WebGL (often fixed at 1px). For thicker strokes, plan to adopt `Line2` from `three/examples` in a later update.

---

## 🏗 Architecture (modules/classes)

- **CONFIG** — Central config for camera & controls, layers, animation rhythms, lighting, materials, visual effects, and UI toggles.
- **Utils** — Device detection and small math/mapping helpers.
- **PerformanceMonitor** — Renders FPS, calls, triangles, and resource counts.
- **SystemStateManager** — State machine (CALM/ALERT/DEFENSIVE) + HUD binding.
- **ResourceManager** — Registers geometries/materials/textures for deterministic disposal.
- **LayerFactory** — Builds the **core** mesh and **wireframe shells** (edges/lines/points), optional glow/points passes.
- **AnimationController** — Runs rotation, breathing, opacity and vertex‑size pulsers per layer with phase offsets.
- **PostProcessingManager** — Creates the composer, wires bloom, exposes runtime toggles, handles resize & quality presets.
- **ShaderManager** — Registry + uniforms for optional custom materials (Phase 3 hooks).
- **SceneManager** — Renderer, scene, camera, lights (ambient/key/rim), OrbitControls setup.
- **ZenoApplication** — Boot, input wiring, per‑frame update/render, cleanup.

---

## ⚙️ Configuration Highlights

All knobs live in `CONFIG` near the top of the script:

- **Camera / Controls:** FOV, near/far, damping, min/max distance.
- **Layers:** Array of layer definitions (`name`, `scale`, `color`, `complexity`). Tip: use stepped base opacities like `[0.26, 0.22, 0.18, 0.14]` for clean depth.
- **Animation:** Rotation speeds, core “breathing,” opacity/vertex pulsing ranges & tempo (with per‑layer phase offsets).
- **Lighting:** Ambient + key + rim colors/intensity/positions.
- **Materials:** Core PBR params; wireframe opacity discipline; set `depthWrite: false` on wires to reduce stacking artifacts.
- **Visual Effects:** Bloom intensity/threshold/radius; optional slots for chromatic aberration, vignette, film grain (when enabled).
- **Quality:** Presets and (optional) adaptive downshift if FPS drops.

---

## 📉 Notes & Limitations

- **Selective Bloom:** Layer tagging is implemented; **masked dual‑pass** (darken non‑bloom, render layer‑1, composite) is a planned enhancement.
- **Memory Display:** Three.js exposes **counts** (`geometries`, `textures`), not bytes; the perf panel reports counts honestly.
- **Line Width:** Browser/GPU limits apply; expect 1px for `LineBasicMaterial` on most platforms.
- **Mobile:** Supported, but **desktop‑first**. Adaptive quality may disable heavy effects to preserve FPS.

---

## 🗺 Roadmap

### Help Wanted
- Implement **true selective bloom** (mask pass): darken non-bloom materials, render camera layer **1**, then composite.

- **Selective Bloom (true)** — Add masked dual‑pass (swap non‑bloom materials to black, render layer‑1, composite).
- **Shader Packs** — Energy‑flow / Fresnel / holographic variants for the “Gates” layer.
- **Crisp Lines** — Migrate selected shells to `Line2` for controllable line thickness.
- **Eye Mode (aesthetic)** — Optional iris ring + catchlight sprite + corneal bloom for a cinematic “eye” motif.
- **SMAA/FXAA** — Optional AA pass before bloom for crisper wires.

---

## Repository
- `zeno-polyhedron-refactored.html` — single-file app (modules/classes inlined)
- `README.md` — this file

---

## 🤝 Contributing

PRs welcome. For visual changes, include before/after PNGs and the precise `CONFIG` diff.  
For performance changes, include FPS / calls / triangles deltas from the monitor.

---

## 📄 License

MIT (proposed). Add a `LICENSE` file at the repo root if you adopt MIT (or replace with your preferred license).
