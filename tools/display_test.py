#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pi5_st7735_evf.display import ST7735Display


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--spi-hz", type=int, default=8_000_000)
    p.add_argument("--x-offset", type=int, default=0)
    p.add_argument("--y-offset", type=int, default=0)
    p.add_argument("--dc", type=int, default=24)
    p.add_argument("--rst", type=int, default=25)
    p.add_argument("--gpio-backend", choices=("lgpio", "adafruit"), default="lgpio")
    args = p.parse_args()

    image = Image.new("RGB", (128, 128), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Border reveals bad offsets immediately.
    draw.rectangle((0, 0, 127, 127), outline=(255, 255, 255))
    draw.line((0, 0, 127, 127), fill=(255, 0, 0))
    draw.line((127, 0, 0, 127), fill=(0, 255, 0))

    # Color bars.
    bars = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 255),
    ]
    bar_w = 128 // len(bars)
    for i, color in enumerate(bars):
        x0 = i * bar_w
        x1 = 127 if i == len(bars) - 1 else (i + 1) * bar_w - 1
        draw.rectangle((x0, 44, x1, 77), fill=color)

    draw.rectangle((13, 10, 115, 33), fill=(0, 0, 0))
    draw.text((17, 14), "ST7735 128x128", fill=(255, 255, 255))
    draw.text((27, 94), f"offset {args.x_offset},{args.y_offset}",
              fill=(255, 255, 255))

    disp = ST7735Display(
        spi_hz=args.spi_hz,
        dc=args.dc,
        rst=args.rst,
        x_offset=args.x_offset,
        y_offset=args.y_offset,
        gpio_backend=args.gpio_backend,
    )

    try:
        disp.open()
        disp.show(image)
        print("Test image drawn. Ctrl+C to clear and exit.")
        while True:
            __import__("time").sleep(1)
    except KeyboardInterrupt:
        return 0
    finally:
        disp.close()


if __name__ == "__main__":
    raise SystemExit(main())
