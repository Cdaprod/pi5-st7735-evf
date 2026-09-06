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


def _value(data: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    """Read JSON, legacy env, or canonical X1301-prefixed env names."""
    for name in names:
        for candidate in (name, name.upper(), f"X1301_{name.upper()}"):
            if candidate in data:
                return data[candidate]
    return default


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
    power_present: bool = False
    timings_locked: bool = False
    audio_present: bool = False
    audio_sampling_rate: int = 0
    pixel_clock_hz: int = 0
    pixel_format: str | None = None
    mode_id: str | None = None
    mode_generation: int = 0
    driver: str | None = None
    rp1_cfe_detected: bool = False
    last_change: str | None = None

    @property
    def pixel_clock_mhz(self) -> float:
        """Pixel clock normalized for UI presentation; the contract is Hz."""
        return self.pixel_clock_hz / 1_000_000.0

    @property
    def ready(self) -> bool:
        return self.signal_state is SignalState.LOCKED and self.configured and bool(self.video_node)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "X1301State":
        pixel_clock_hz = _integer(_value(data, "pixelclock_hz", "pixel_clock_hz"))
        if not pixel_clock_hz:
            # Compatibility with the old EVF-specific MHz field only.
            pixel_clock_hz = int(_float(_value(data, "pixel_clock_mhz")) * 1_000_000)
        return cls(
            signal_state=SignalState.parse(_value(data, "signal_state", "state")),
            video_node=_value(data, "video", "video_node") or None,
            media_node=_value(data, "media", "media_node") or None,
            subdev_node=_value(data, "subdev", "subdev_node") or None,
            width=_integer(_value(data, "width")), height=_integer(_value(data, "height")),
            fps=_float(_value(data, "fps")), configured=_bool(_value(data, "configured")),
            error=_value(data, "error") or None,
            power_present=_bool(_value(data, "power_present")),
            timings_locked=_bool(_value(data, "timings_locked")),
            audio_present=_bool(_value(data, "audio_present")),
            audio_sampling_rate=_integer(_value(data, "audio_sampling_rate")),
            pixel_clock_hz=pixel_clock_hz,
            pixel_format=_value(data, "pixelformat", "pixel_format") or None,
            mode_id=_value(data, "mode_id") or None,
            mode_generation=_integer(_value(data, "mode_generation")),
            driver=_value(data, "driver") or None,
            rp1_cfe_detected=_bool(_value(data, "rp1_cfe_detected", "rp1_cfe")),
            last_change=_value(data, "last_change") or None,
        )
