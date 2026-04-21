"""Audio stream reader. Yields window RMS values from the default mic."""
import queue
import numpy as np
import sounddevice as sd


class AudioStreamReader:
    """Wraps sounddevice.InputStream, exposes RMS values at fixed window size."""

    def __init__(self, samplerate=16000, window_ms=50, device=None):
        self.samplerate = samplerate
        self.window_samples = int(samplerate * window_ms / 1000)
        self.device = device
        self._q = queue.Queue()
        self._stream = None

    def _callback(self, indata, frames, time_info, status):
        if status:
            pass  # dropped frames - ignore
        self._q.put(indata[:, 0].copy())

    def start(self):
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            blocksize=self.window_samples,
            dtype="float32",
            callback=self._callback,
            device=self.device,
        )
        self._stream.start()

    def rms_stream(self):
        """Blocking generator: yields RMS of each window."""
        while True:
            block = self._q.get()
            rms = float(np.sqrt(np.mean(block ** 2)))
            yield rms

    def close(self):
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
