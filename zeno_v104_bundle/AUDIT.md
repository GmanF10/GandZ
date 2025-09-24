# ZENØ V104 — Code Audit & Review

This audit covers the **V104 HTML UI**, **Python sidecar**, **requirements**, and **packaging skeleton**.

## Frontend (zeno_v104.html)

**Strengths**
- Modern render loop using `setAnimationLoop` with a `THREE.Clock()` delta.
- Selective bloom with two composers, keeping HUD/stars crisp by default; optional star bloom.
- Fat-line path (LineSegments2/LineMaterial) for consistent, screen-space wire widths.
- Robust starfield: no depth test, DPR-aware point sizes, twinkle controls, explicit bounding sphere, culling disabled.
- Reduced-motion, visibility pause, context loss handling, auto-DPR tuner.
- Settings panel with persistence via `localStorage`.

**Risks & mitigations**
- **Non-module examples** order is brittle (fixed by ordering + runtime guards).
- **CDN dependencies**: not offline. For air-gapped use, vendor the scripts.
- **VignetteShader** may be missing on some CDNs → guarded in code.

**Suggestions (future)**
- Migrate to ESM + bundler (Vite) and import from `examples/jsm/*` to remove global ordering issues.
- Consider `InstancedMesh` if shells multiply or you add constellations.
- Add a “bloom-only” debug toggle to tune threshold quickly.

## Sidecar (zeno_sidecar/app.py)

**Strengths**
- Works without GPU / keys. Uses NVML if present, otherwise `nvidia-smi` CLI.
- Graceful shutdown and CLI args for host/port.
- 1Hz payload shaped for HUD.

**Risks**
- No AMD/Intel GPU utilization. (Out of scope here.)

**Suggestions**
- Add optional AMD (rocm-smi) and Intel (intel_gpu_top) adapters behind feature flags.
- Unit tests for parsers (NVML/CLI).

## requirements.txt

- Pinned, minimal, standard uvicorn extras. No keys needed. Good.

## Packaging (Tauri v2 skeleton)

- Capabilities kept narrow. Shell plugin is scoped to the sidecar binary.
- You’ll need platform **code-signing** keys to ship installers (not included):
  - **macOS**: Apple Developer ID certificate/signing.
  - **Windows**: Code Signing certificate for SmartScreen reputation.
  - **Linux**: Typically not required, but repository signing is common.

See `PACKAGING.md` for details.

