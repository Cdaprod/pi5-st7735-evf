from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from PIL import Image

class DisplayBackend(Protocol):
    width: int
    height: int
    def open(self) -> None: ...
    def close(self) -> None: ...
    def show(self, image: Image.Image) -> None: ...
    def clear(self) -> None: ...
    def set_brightness(self, value: float) -> None: ...


class OffsetST7735:
    """ST7735 subclass that applies visible-panel RAM x/y offsets."""

    def __init__(self, *args, x_offset: int = 0, y_offset: int = 0, **kwargs):
        self.x_offset = int(x_offset)
        self.y_offset = int(y_offset)
        import ST7735 as TFT
        self._driver = TFT.ST7735(*args, **kwargs)
        self.width, self.height = self._driver.width, self._driver.height

    def __getattr__(self, name):
        return getattr(self._driver, name)

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        if x1 is None:
            x1 = self.width - 1
        if y1 is None:
            y1 = self.height - 1

        x0 += self.x_offset
        x1 += self.x_offset
        y0 += self.y_offset
        y1 += self.y_offset

        import ST7735 as TFT
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
        self._gpio: Optional[object] = None
        self._disp = None

    def open(self) -> None:
        # Upstream ST7735.__init__ applies module-level SPI_CLOCK_HZ, so set it
        # before constructing the device.
        import ST7735 as TFT
        import Adafruit_GPIO.SPI as SPI
        TFT.SPI_CLOCK_HZ = int(self.spi_hz)

        class OffsetDriver(TFT.ST7735):
            def set_window(driver, x0=0, y0=0, x1=None, y1=None):
                if x1 is None: x1 = driver.width - 1
                if y1 is None: y1 = driver.height - 1
                x0 += self.x_offset; x1 += self.x_offset
                y0 += self.y_offset; y1 += self.y_offset
                driver.command(TFT.ST7735_CASET)
                for value in (x0 >> 8, x0, x1 >> 8, x1): driver.data(value)
                driver.command(TFT.ST7735_RASET)
                for value in (y0 >> 8, y0, y1 >> 8, y1): driver.data(value)
                driver.command(TFT.ST7735_RAMWR)

        gpio = None
        if self.gpio_backend == "lgpio":
            from .gpio_lgpio import LGPIOCompat
            self._gpio = LGPIOCompat()
            gpio = self._gpio

        spi = SPI.SpiDev(
            self.spi_port,
            self.spi_device,
            max_speed_hz=self.spi_hz,
        )

        self._disp = OffsetDriver(
            self.dc,
            rst=self.rst,
            spi=spi,
            gpio=gpio,
            width=self.width,
            height=self.height,
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

    def clear(self) -> None:
        if self._disp is not None:
            self._disp.clear((0, 0, 0)); self._disp.display()

    def set_brightness(self, value: float) -> None:
        """Backlight is currently wired directly; retained as a backend contract."""


ST7735Backend = ST7735Display


@dataclass
class MockDisplayBackend:
    width: int = 128
    height: int = 128
    last_frame: Image.Image | None = None
    is_open: bool = False

    def open(self) -> None: self.is_open = True
    def close(self) -> None: self.is_open = False
    def clear(self) -> None: self.last_frame = Image.new("RGB", (self.width, self.height))
    def set_brightness(self, value: float) -> None: pass
    def show(self, image: Image.Image) -> None:
        if not self.is_open: raise RuntimeError("Display is not open")
        if image.size != (self.width, self.height): raise ValueError("Incorrect frame size")
        self.last_frame = image.copy()
