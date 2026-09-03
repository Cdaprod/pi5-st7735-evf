from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PIL import Image

import ST7735 as TFT
import Adafruit_GPIO.SPI as SPI

from .gpio_lgpio import LGPIOCompat


class OffsetST7735(TFT.ST7735):
    """ST7735 subclass that applies visible-panel RAM x/y offsets."""

    def __init__(self, *args, x_offset: int = 0, y_offset: int = 0, **kwargs):
        self.x_offset = int(x_offset)
        self.y_offset = int(y_offset)
        super().__init__(*args, **kwargs)

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        if x1 is None:
            x1 = self.width - 1
        if y1 is None:
            y1 = self.height - 1

        x0 += self.x_offset
        x1 += self.x_offset
        y0 += self.y_offset
        y1 += self.y_offset

        self.command(TFT.ST7735_CASET)
        self.data(x0 >> 8)
        self.data(x0)
        self.data(x1 >> 8)
        self.data(x1)

        self.command(TFT.ST7735_RASET)
        self.data(y0 >> 8)
        self.data(y0)
        self.data(y1 >> 8)
        self.data(y1)

        self.command(TFT.ST7735_RAMWR)


@dataclass
class ST7735Display:
    width: int = 128
    height: int = 128
    dc: int = 24
    rst: int = 25
    spi_port: int = 0
    spi_device: int = 0
    spi_hz: int = 16_000_000
    x_offset: int = 0
    y_offset: int = 0
    gpio_backend: str = "lgpio"

    def __post_init__(self):
        self._gpio: Optional[LGPIOCompat] = None
        self._disp = None

    def open(self) -> None:
        # Upstream ST7735.__init__ applies module-level SPI_CLOCK_HZ, so set it
        # before constructing the device.
        TFT.SPI_CLOCK_HZ = int(self.spi_hz)

        gpio = None
        if self.gpio_backend == "lgpio":
            self._gpio = LGPIOCompat()
            gpio = self._gpio

        spi = SPI.SpiDev(
            self.spi_port,
            self.spi_device,
            max_speed_hz=self.spi_hz,
        )

        self._disp = OffsetST7735(
            self.dc,
            rst=self.rst,
            spi=spi,
            gpio=gpio,
            width=self.width,
            height=self.height,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )
        self._disp.begin()
        self._disp.clear((0, 0, 0))
        self._disp.display()

    def show(self, image: Image.Image) -> None:
        if self._disp is None:
            raise RuntimeError("Display is not open")
        if image.size != (self.width, self.height):
            raise ValueError(
                f"Expected image {(self.width, self.height)}, got {image.size}"
            )
        if image.mode != "RGB":
            image = image.convert("RGB")
        self._disp.display(image)

    def close(self) -> None:
        if self._disp is not None:
            try:
                self._disp.clear((0, 0, 0))
                self._disp.display()
            except Exception:
                pass
            self._disp = None

        if self._gpio is not None:
            self._gpio.close()
            self._gpio = None
