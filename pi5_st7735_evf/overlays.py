from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def _font(size: int = 10):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


FONT_8 = _font(8)
FONT_9 = _font(9)
FONT_10 = _font(10)


@dataclass
class FpsMeter:
    window: int = 20
    samples: deque[float] = field(default_factory=lambda: deque(maxlen=20))
    last: float | None = None

    def tick(self) -> float:
        now = time.monotonic()
        if self.last is not None:
            dt = now - self.last
            if dt > 0:
                self.samples.append(1.0 / dt)
        self.last = now
        if not self.samples:
            return 0.0
        return sum(self.samples) / len(self.samples)


def read_pi_temp_c() -> float | None:
    path = Path("/sys/class/thermal/thermal_zone0/temp")
    try:
        return float(path.read_text().strip()) / 1000.0
    except Exception:
        return None


def apply_focus_peaking(frame_bgr: np.ndarray, threshold: int = 90) -> np.ndarray:
    """Overlay high-frequency edges in red."""
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
    mag = cv2.convertScaleAbs(lap)
    mask = mag >= int(threshold)
    out = frame_bgr.copy()
    out[mask] = (0, 0, 255)
    return out


def apply_zebra(frame_bgr: np.ndarray, threshold: int = 245) -> np.ndarray:
    """Mark near-clipped luminance with diagonal black/white zebra stripes."""
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    yy, xx = np.indices(gray.shape)
    hot = gray >= int(threshold)
    stripe = ((xx + yy) // 3) % 2 == 0

    out = frame_bgr.copy()
    out[hot & stripe] = (255, 255, 255)
    out[hot & ~stripe] = (0, 0, 0)
    return out


def draw_crosshair(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    cx, cy = width // 2, height // 2
    color = (255, 255, 255)
    draw.line((cx - 6, cy, cx - 2, cy), fill=color)
    draw.line((cx + 2, cy, cx + 6, cy), fill=color)
    draw.line((cx, cy - 6, cx, cy - 2), fill=color)
    draw.line((cx, cy + 2, cx, cy + 6), fill=color)


def draw_thirds(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    color = (180, 180, 180)
    x1, x2 = width // 3, (2 * width) // 3
    y1, y2 = height // 3, (2 * height) // 3
    draw.line((x1, 0, x1, height - 1), fill=color)
    draw.line((x2, 0, x2, height - 1), fill=color)
    draw.line((0, y1, width - 1, y1), fill=color)
    draw.line((0, y2, width - 1, y2), fill=color)


def draw_histogram(
    draw: ImageDraw.ImageDraw,
    frame_bgr: np.ndarray,
    width: int,
    height: int,
) -> None:
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [32], [0, 256]).flatten()
    max_v = max(float(hist.max()), 1.0)

    graph_w = min(64, width)
    graph_h = 18
    x0 = width - graph_w
    y0 = height - graph_h

    draw.rectangle((x0, y0, width - 1, height - 1), fill=(0, 0, 0))
    bar_w = graph_w / len(hist)
    for i, v in enumerate(hist):
        h = int((float(v) / max_v) * (graph_h - 2))
        x = int(x0 + i * bar_w)
        draw.line((x, height - 2, x, height - 2 - h), fill=(220, 220, 220))


def draw_text_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    *,
    font=FONT_8,
    anchor: str | None = None,
) -> None:
    # PIL anchors are not consistent across every old distro build, so compute
    # a compact background using textbbox and only use anchor when supplied.
    if anchor:
        bbox = draw.textbbox(xy, text, font=font, anchor=anchor)
        draw.rectangle(bbox, fill=(0, 0, 0))
        draw.text(xy, text, font=font, fill=(255, 255, 255), anchor=anchor)
    else:
        bbox = draw.textbbox(xy, text, font=font)
        draw.rectangle(bbox, fill=(0, 0, 0))
        draw.text(xy, text, font=font, fill=(255, 255, 255))


def compose_overlays(
    image: Image.Image,
    frame_bgr: np.ndarray,
    overlays: set[str],
    *,
    fps: float,
    source_width: int,
    source_height: int,
    label: str,
) -> Image.Image:
    out = image.copy()
    draw = ImageDraw.Draw(out)
    width, height = out.size

    if "thirds" in overlays:
        draw_thirds(draw, width, height)

    if "crosshair" in overlays:
        draw_crosshair(draw, width, height)

    if "histogram" in overlays:
        draw_histogram(draw, frame_bgr, width, height)

    # Top row.
    x = 2
    if "rec" in overlays:
        draw.ellipse((2, 2, 7, 7), fill=(255, 0, 0))
        draw_text_box(draw, (9, 1), "REC", font=FONT_8)
        x = 32

    if "label" in overlays and label:
        draw_text_box(draw, (x, 1), label[:10], font=FONT_8)

    if "fps" in overlays:
        text = f"{fps:4.1f}fps"
        draw_text_box(draw, (width - 2, 1), text, font=FONT_8, anchor="ra")

    # Bottom row.
    bottom_parts: list[str] = []
    if "resolution" in overlays:
        bottom_parts.append(f"{source_width}x{source_height}")
    if "temp" in overlays:
        temp = read_pi_temp_c()
        if temp is not None:
            bottom_parts.append(f"{temp:.0f}C")
    if bottom_parts:
        draw_text_box(draw, (2, height - 1), " ".join(bottom_parts),
                      font=FONT_8, anchor="ld")

    if "clock" in overlays:
        draw_text_box(
            draw,
            (width - 2, height - 1),
            datetime.now().strftime("%H:%M:%S"),
            font=FONT_8,
            anchor="rd",
        )

    return out
