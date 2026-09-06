from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    MENU="MENU"; BACK="BACK"; UP="UP"; DOWN="DOWN"; LEFT="LEFT"; RIGHT="RIGHT"
    SELECT="SELECT"; F1="F1"; F2="F2"; F3="F3"; F4="F4"


@dataclass
class Menu:
    items: tuple[str, ...]
    selected: int = 0
    visible: bool = False

    def dispatch(self, action: Action) -> str | None:
        if action is Action.MENU: self.visible = not self.visible
        elif action is Action.BACK: self.visible = False
        elif self.visible and action in (Action.UP, Action.LEFT): self.selected = (self.selected - 1) % len(self.items)
        elif self.visible and action in (Action.DOWN, Action.RIGHT): self.selected = (self.selected + 1) % len(self.items)
        elif self.visible and action is Action.SELECT: return self.items[self.selected]
        return None
