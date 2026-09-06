from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class SignalState(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    PRESENT_NO_SIGNAL = "PRESENT_NO_SIGNAL"
    LOCKED = "LOCKED"
    MODE_CHANGE = "MODE_CHANGE"
    ERROR = "ERROR"

    @classmethod
    def parse(cls, value: object) -> "SignalState":
        normalized = str(value or "DISCONNECTED").strip().upper().replace("-", "_")
        aliases = {"NO_SIGNAL": cls.PRESENT_NO_SIGNAL, "PRESENT": cls.PRESENT_NO_SIGNAL}
        return aliases.get(normalized, cls.__members__.get(normalized, cls.ERROR))


def _value(data: Mapping[str, Any], name: str, default: Any = None) -> Any:
    return data.get(name, data.get(name.upper(), default))


def _integer(value: object) -> int:
    try:
        return int(float(str(value or 0)))
    except (TypeError, ValueError):
        return 0


def _float(value: object) -> float:
    text = str(value or 0).strip().split("/")
    try:
        return float(text[0]) / float(text[1]) if len(text) == 2 else float(text[0])
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def _bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class X1301State:
    signal_state: SignalState = SignalState.DISCONNECTED
    video_node: str | None = None
    media_node: str | None = None
    subdev_node: str | None = None
    width: int = 0
    height: int = 0
    fps: float = 0.0
    configured: bool = False
    error: str | None = None
    pixel_clock_mhz: float = 0.0
    driver: str | None = None
    rp1_cfe_detected: bool = False

    @property
    def ready(self) -> bool:
        return self.signal_state is SignalState.LOCKED and self.configured and bool(self.video_node)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "X1301State":
        return cls(
            signal_state=SignalState.parse(_value(data, "signal_state", _value(data, "state"))),
            video_node=_value(data, "video_node", _value(data, "video")) or None,
            media_node=_value(data, "media_node", _value(data, "media")) or None,
            subdev_node=_value(data, "subdev_node", _value(data, "subdev")) or None,
            width=_integer(_value(data, "width")), height=_integer(_value(data, "height")),
            fps=_float(_value(data, "fps")), configured=_bool(_value(data, "configured")),
            error=_value(data, "error") or None,
            pixel_clock_mhz=_float(_value(data, "pixel_clock_mhz", _value(data, "pixel_clock"))),
            driver=_value(data, "driver") or None,
            rp1_cfe_detected=_bool(_value(data, "rp1_cfe_detected", _value(data, "rp1_cfe"))),
        )
