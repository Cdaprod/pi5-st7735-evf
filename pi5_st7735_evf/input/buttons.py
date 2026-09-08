"""Optional active-low lgpio button backend with debounce."""
from __future__ import annotations

import time
from collections.abc import Mapping
from .events import InputEvent


class LGPIOButtonBackend:
    def __init__(self, pins: Mapping[InputEvent, int], debounce: float = .05,
                 chip: int = 0, module=None, clock=time.monotonic) -> None:
        if module is None:
            import lgpio as module
        self._gpio, self._clock = module, clock
        self._handle = module.gpiochip_open(chip)
        self._pins = {event: int(pin) for event, pin in pins.items()}
        self._last = {event: 1 for event in pins}
        self._changed = {event: float("-inf") for event in pins}
        self._debounce = debounce
        for pin in self._pins.values():
            module.gpio_claim_input(self._handle, pin, module.SET_PULL_UP)

    def poll(self) -> InputEvent | None:
        now = self._clock()
        for event, pin in self._pins.items():
            value = self._gpio.gpio_read(self._handle, pin)
            old = self._last[event]
            if value != old and now - self._changed[event] >= self._debounce:
                self._last[event], self._changed[event] = value, now
                if value == 0:
                    return event
        return None

    def close(self) -> None:
        if self._handle is not None:
            self._gpio.gpiochip_close(self._handle)
            self._handle = None
