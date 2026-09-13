"""Reusable menu row and focus cursor widgets."""
from dataclasses import dataclass
from .core import Label
from ..theme import ACCENT, FOREGROUND, MUTED


@dataclass(frozen=True)
class SelectionCursor:
    color: tuple = ACCENT
    inset: int = 2

    def draw(self, draw, box) -> None:
        x0,y0,x1,y1=box; n=4
        draw.line((x0+n,y0,x0,y0,x0,y1,x0+n,y1), fill=self.color)
        draw.line((x1-n,y0,x1,y0,x1,y1,x1-n,y1), fill=self.color)


@dataclass(frozen=True)
class MenuRow:
    label: str
    value: str = ""
    selected: bool = False

    def draw(self, draw, box) -> None:
        x0,y0,x1,y1=box
        if self.selected:
            SelectionCursor().draw(draw, box)
        Label(self.label, 8, FOREGROUND if self.selected else MUTED).draw(draw,(x0+7,y0+3))
        if self.value:
            Label(self.value, 8, ACCENT if self.selected else FOREGROUND).draw(draw,(x1-6,y0+3),anchor="ra")
