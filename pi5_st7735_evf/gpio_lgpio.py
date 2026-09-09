from __future__ import annotations

import lgpio


class LGPIOCompat:
    """Minimal Adafruit_GPIO-compatible output shim for Raspberry Pi 5.

    cskau/Python_ST7735 accepts an explicit ``gpio=`` object.  Only setup(),
    output(), set_high(), and set_low() are required by that driver.
    """

    def __init__(self, chip: int = 15) -> None:
        self._handle = lgpio.gpiochip_open(chip)
        self._claimed: set[int] = set()

    def setup(self, pin: int, mode) -> None:
        # The ST7735 driver only asks for output pins.
        if pin in self._claimed:
            return
        lgpio.gpio_claim_output(self._handle, int(pin), 0)
        self._claimed.add(int(pin))

    def output(self, pin: int, value) -> None:
        lgpio.gpio_write(self._handle, int(pin), 1 if value else 0)

    def set_high(self, pin: int) -> None:
        self.output(pin, True)

    def set_low(self, pin: int) -> None:
        self.output(pin, False)

    def close(self) -> None:
        if getattr(self, "_handle", None) is not None:
            lgpio.gpiochip_close(self._handle)
            self._handle = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
