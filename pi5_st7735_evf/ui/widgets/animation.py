"""Deterministic widgets driven exclusively by a caller-supplied phase."""
import math
from dataclasses import dataclass
from ..theme import ACCENT, MUTED


@dataclass(frozen=True)
class ProgressDots:
    count: int = 3

    def draw(self, draw, center, phase: float) -> None:
        cx, cy = center; active = int(phase) % self.count
        for i in range(self.count):
            x = cx + (i - (self.count-1)/2) * 12
            draw.ellipse((x-2, cy-2, x+2, cy+2), fill=ACCENT if i == active else MUTED)


@dataclass(frozen=True)
class Spinner:
    radius: int = 12
    segments: int = 8

    def draw(self, draw, center, phase: float) -> None:
        cx, cy = center; active = int(phase) % self.segments
        for i in range(self.segments):
            angle = 2 * math.pi * i / self.segments
            inner = self.radius - 4; outer = self.radius
            points = (cx+math.cos(angle)*inner, cy+math.sin(angle)*inner,
                      cx+math.cos(angle)*outer, cy+math.sin(angle)*outer)
            draw.line(points, fill=ACCENT if i == active else MUTED, width=2 if i == active else 1)
