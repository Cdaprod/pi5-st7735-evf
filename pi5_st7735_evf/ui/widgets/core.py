"""Small stateless drawing components."""
from dataclasses import dataclass
from PIL import ImageDraw
from ..theme import ACCENT, FOREGROUND, LINE_WIDTH, MUTED, font


@dataclass(frozen=True)
class Label:
    text: str
    size: int = 9
    color: tuple = FOREGROUND
    bold: bool = False

    def draw(self, draw: ImageDraw.ImageDraw, xy, *, anchor=None) -> None:
        draw.text(xy, self.text, fill=self.color, font=font(self.size, self.bold), anchor=anchor)


@dataclass(frozen=True)
class ValueLabel:
    label: str
    value: str

    def draw(self, draw, y: int, width: int, *, x: int = 12) -> None:
        Label(self.label, 7, MUTED).draw(draw, (x, y))
        Label(self.value, 7).draw(draw, (width - x, y), anchor="ra")


@dataclass(frozen=True)
class StatusDot:
    active: bool
    color: tuple = ACCENT

    def draw(self, draw, center, radius: int = 2) -> None:
        x, y = center
        draw.ellipse((x-radius, y-radius, x+radius, y+radius),
                     fill=self.color if self.active else MUTED)


@dataclass(frozen=True)
class Divider:
    color: tuple = MUTED

    def draw(self, draw, y: int, width: int, inset: int = 8) -> None:
        draw.line((inset, y, width-inset-1, y), fill=self.color, width=LINE_WIDTH)


@dataclass(frozen=True)
class FrameCorners:
    color: tuple = ACCENT
    length: int = 8

    def draw(self, draw, box) -> None:
        x0, y0, x1, y1 = box; n = self.length
        for points in (((x0,y0+n),(x0,y0),(x0+n,y0)), ((x1-n,y0),(x1,y0),(x1,y0+n)),
                       ((x0,y1-n),(x0,y1),(x0+n,y1)), ((x1-n,y1),(x1,y1),(x1,y1-n))):
            draw.line(points, fill=self.color, width=LINE_WIDTH)
