"""Read-only inputs shared by lightweight UI scenes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RenderContext:
    width: int = 128
    height: int = 128
    phase: float = 0.0
    runtime: Any = None
    navigation: Any = None
    fps: float = 0.0
    application_state: Any = None

    @classmethod
    def from_kwargs(cls, width: int = 128, height: int = 128, **values: Any) -> "RenderContext":
        return cls(width=width, height=height,
                   phase=float(values.get("phase", 0.0) or 0.0),
                   runtime=values.get("runtime"), navigation=values.get("navigation"),
                   fps=float(values.get("fps", 0.0) or 0.0),
                   application_state=values.get("application_state"))
