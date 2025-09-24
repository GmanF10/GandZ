# ZENØ Sidecar (Telemetry)

A tiny FastAPI WebSocket server that streams local system telemetry to the ZENØ HUD.

- **CPU**: percent
- **RAM**: used / total (GiB)
- **GPU (NVIDIA)**: util %, temperature, VRAM used/total (GiB), name
  - Sources: NVML (`pynvml`) if importable; fallback to `nvidia-smi` CLI if available.
  - If no NVIDIA GPU is found, GPU fields are `null`.

## Quick start

```bash
cd zeno_sidecar
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
. .venv/bin/activate

pip install -r requirements.txt

# Start at ws://127.0.0.1:8765/metrics
python app.py

# or change host/port
python app.py --host 0.0.0.0 --port 9000
```

Now open **zeno_v104.html?ui=1&telemetry=1** and (optionally) set a custom WS URL in the settings panel.

### Configuration

Environment variables:
- `ZENO_SIDECAR_HOST` (default `127.0.0.1`)
- `ZENO_SIDECAR_PORT` (default `8765`)

CLI arguments override env values.

### Notes

- **No API keys** are required. Everything is local.
- On NVIDIA systems, `pynvml` gives the best results. If it can't initialize, the sidecar tries `nvidia-smi`.
- AMD/Intel GPUs: this sample does not query vendor APIs. You will still get CPU and RAM stats.
