# Packaging & Signing (Overview)

This project provides a Tauri v2 skeleton for a desktop app wrapping the V104 UI and (optionally) a Python sidecar.

## Dev
- Run the sidecar manually:
  ```bash
  cd zeno_sidecar
  python -m venv .venv && . .venv/bin/activate
  pip install -r requirements.txt
  python app.py
  ```
- In a second shell:
  ```bash
  cd zeno_tauri2_skeleton
  npm install
  npm run dev
  ```

## Bundling the sidecar
- Build a standalone sidecar binary (e.g., PyInstaller) and place it at:
  `zeno_tauri2_skeleton/src-tauri/binaries/zeno_sidecar` (OS-specific suffixes as needed).
- Tauri config already references `bundle.externalBin` → the binary is included with app bundles.

## Signing / Keys (when you are ready to distribute)
No runtime API keys are required by this project. The only “keys” you may need are **code-signing** keys for distribution:

- **macOS**: Apple Developer account + Developer ID Application certificate. You’ll sign the app and the sidecar. (Not included here.)
- **Windows**: An EV or standard Code Signing certificate to reduce SmartScreen warnings.
- **Linux**: Typically no signing, but package maintainers use repository signing.

Store these securely—**do not** commit to source control. Configure your CI (if any) to access them via environment variables or a secure key store.
