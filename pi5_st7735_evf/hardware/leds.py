from enum import Enum


class Led(str, Enum): POWER="POWER"; HDMI="HDMI"; ERROR="ERROR"; REC="REC"
class LedMode(str, Enum): OFF="OFF"; BLINK="BLINK"; SOLID="SOLID"


class LedController:
    def __init__(self) -> None: self.states = {led: LedMode.OFF for led in Led}
    def set(self, led: Led, mode: LedMode) -> None: self.states[led] = mode
