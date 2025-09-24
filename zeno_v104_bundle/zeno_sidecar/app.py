# ZENO Python sidecar (FastAPI + WebSocket) — streams system telemetry
import asyncio, json, os, time, signal, argparse, subprocess, shutil
from typing import Optional
import psutil

# Optional NVIDIA telemetry via NVML
try:
    import pynvml
    pynvml.nvmlInit()
    NVML = True
except Exception:
    NVML = False

# Optional generic GPU util via nvidia-smi (fallback when NVML not importable)
def nvidia_smi_util():
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        # Query utilization, memory used/total, temperature, and name in a single call
        # CSV format: utilization.gpu, memory.used, memory.total, temperature.gpu, name
        out = subprocess.check_output([exe, "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,name", "--format=csv,noheader,nounits"], stderr=subprocess.DEVNULL, timeout=1.0)
        line = out.decode("utf-8", "ignore").splitlines()[0]
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 5:
            return None
        util = int(parts[0])
        mem_used = float(parts[1]) / 1024.0  # MiB -> GiB approx if CSV returns MiB; if returns MiB, adjust; otherwise nounits returns raw
        mem_total = float(parts[2]) / 1024.0
        temp = int(parts[3])
        name = parts[4]
        return {"util": util, "mem_used_gb": mem_used, "mem_total_gb": mem_total, "temp": temp, "name": name}
    except Exception:
        return None

from fastapi import FastAPI, WebSocket
from fastapi.responses import PlainTextResponse

app = FastAPI()

def gpu_stats():
    # Priority: NVML (fast, direct) -> nvidia-smi -> None
    if NVML:
        try:
            count = pynvml.nvmlDeviceGetCount()
            if count < 1:
                return None
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = int(pynvml.nvmlDeviceGetUtilizationRates(handle).gpu)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            temp = int(pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU))
            name = pynvml.nvmlDeviceGetName(handle).decode("utf-8", "ignore")
            return {
                "util": util,
                "mem_used_gb": mem.used / (1024**3),
                "mem_total_gb": mem.total / (1024**3),
                "temp": temp,
                "name": name
            }
        except Exception:
            # Fall through to CLI-based check
            pass
    # Fallback to nvidia-smi if present
    return nvidia_smi_util()

@app.get("/", response_class=PlainTextResponse)
def root():
    return "ZENØ sidecar alive"

@app.websocket("/metrics")
async def metrics(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            payload = {
                "ts": time.time(),
                "cpu": {"percent": cpu_percent},
                "ram": {"used_gb": mem.used / (1024**3), "total_gb": mem.total / (1024**3)},
                "gpu": gpu_stats()
            }
            await ws.send_text(json.dumps(payload))
            await asyncio.sleep(1.0)
    except Exception:
        try:
            await ws.close()
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="ZENØ telemetry sidecar")
    parser.add_argument("--host", default=os.environ.get("ZENO_SIDECAR_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("ZENO_SIDECAR_PORT", "8765")))
    args = parser.parse_args()

    import uvicorn

    loop = asyncio.get_event_loop()

    # Graceful shutdown on SIGINT/SIGTERM
    stop_event = asyncio.Event()
    def _stop(*_):
        try:
            stop_event.set()
        except Exception:
            pass
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, _stop)
    except Exception:
        # Not all platforms allow installing signal handlers
        pass

    config = uvicorn.Config(app, host=args.host, port=args.port, reload=False, workers=1, log_level="info")
    server = uvicorn.Server(config)

    async def _serve():
        await server.serve()

    async def _main():
        await asyncio.gather(_serve(), stop_event.wait())
        if server.should_exit is False:
            server.should_exit = True

    try:
        loop.run_until_complete(_main())
    finally:
        if NVML:
            try: pynvml.nvmlShutdown()
            except Exception: pass

if __name__ == "__main__":
    main()
