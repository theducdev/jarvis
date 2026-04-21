"""Clap wake listener — runs alongside backend.

Listens to default mic, fires POST /api/v1/system/wake on double-clap.
Calibration: during first 3s after start, collects RMS stats to auto-tune threshold.
"""
import os
import sys
import time
import argparse
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "clap-detection"))

from audio_stream_reader import AudioStreamReader  # noqa: E402
from double_clap_detector import DoubleClapDetector  # noqa: E402

WAKE_URL = os.getenv("WAKE_URL", "http://localhost:8000/api/v1/system/wake")
MIC_DEVICE = os.getenv("CLAP_MIC_DEVICE_INDEX")
MIC_DEVICE = int(MIC_DEVICE) if MIC_DEVICE and MIC_DEVICE.isdigit() else None


def calibrate(reader, duration_s=3.0):
    """Sample ambient noise to set a sane baseline threshold."""
    print(f"[CALIBRATE] Sampling {duration_s:.1f}s of ambient noise — stay quiet...")
    samples = []
    deadline = time.monotonic() + duration_s
    for rms in reader.rms_stream():
        samples.append(rms)
        if time.monotonic() >= deadline:
            break
    noise_floor = max(samples) if samples else 0.02
    threshold = max(noise_floor * 4.0, 0.08)
    print(f"[CALIBRATE] Noise floor={noise_floor:.4f}, threshold={threshold:.4f}")
    return threshold


def fire_wake():
    try:
        r = requests.post(WAKE_URL, timeout=2.0)
        print(f"[WAKE] POST {WAKE_URL} -> {r.status_code} {r.text}")
    except Exception as e:
        print(f"[WAKE] Failed to POST wake: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=None,
                        help="Override RMS threshold (skip calibration)")
    parser.add_argument("--device", type=int, default=MIC_DEVICE,
                        help="Microphone device index")
    parser.add_argument("--list-devices", action="store_true",
                        help="List audio devices and exit")
    args = parser.parse_args()

    if args.list_devices:
        import sounddevice as sd
        print(sd.query_devices())
        return

    reader = AudioStreamReader(samplerate=16000, window_ms=50, device=args.device)
    reader.start()

    try:
        threshold = args.threshold if args.threshold else calibrate(reader)
        detector = DoubleClapDetector(threshold=threshold)

        print(f"[READY] Listening. Clap twice to wake JARVIS. (device={args.device})")
        for rms in reader.rms_stream():
            if detector.feed(rms):
                print(f"[CLAP-CLAP] rms={rms:.4f} -> wake")
                fire_wake()
    except KeyboardInterrupt:
        print("\n[EXIT] Shutting down listener")
    finally:
        reader.close()


if __name__ == "__main__":
    main()
