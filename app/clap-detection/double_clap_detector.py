"""Double-clap detector. Consumes RMS stream, emits events on double-clap."""
import time


class DoubleClapDetector:
    """Detects two energy spikes within a time window.

    Spike = RMS crosses threshold (rising edge).
    Double-clap = 2 spikes separated by min_gap..max_gap seconds.
    Cooldown prevents rapid re-trigger.
    """

    def __init__(
        self,
        threshold=0.15,
        min_gap=0.12,
        max_gap=0.8,
        cooldown=2.0,
    ):
        self.threshold = threshold
        self.min_gap = min_gap
        self.max_gap = max_gap
        self.cooldown = cooldown
        self._last_spike_ts = 0.0
        self._last_trigger_ts = 0.0
        self._prev_rms = 0.0

    def feed(self, rms: float, now: float = None) -> bool:
        """Feed one RMS sample. Returns True if double-clap detected."""
        if now is None:
            now = time.monotonic()

        rising_edge = rms > self.threshold and self._prev_rms <= self.threshold
        self._prev_rms = rms

        if not rising_edge:
            return False

        if now - self._last_trigger_ts < self.cooldown:
            return False

        gap = now - self._last_spike_ts
        if self.min_gap <= gap <= self.max_gap:
            self._last_trigger_ts = now
            self._last_spike_ts = 0.0
            return True

        self._last_spike_ts = now
        return False

    def calibrate(self, rms_samples: list, multiplier: float = 0.6):
        """Auto-tune threshold from a list of clap RMS peaks."""
        if not rms_samples:
            return
        peak = max(rms_samples)
        self.threshold = peak * multiplier
