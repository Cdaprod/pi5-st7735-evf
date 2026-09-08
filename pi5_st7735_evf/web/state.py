"""Thread-safe latest-frame state shared by the EVF and HTTP clients."""
from __future__ import annotations

import io
import threading
import time
from dataclasses import asdict, is_dataclass
import cv2
import numpy as np


class SharedStateHub:
    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._source = None
        self._ui_png = b""
        self._status = {"application_state": "BOOTING", "screen": "boot",
                        "streaming": False, "timestamp": time.time()}
        self._generation = 0

    def publish(self, *, source_frame=None, ui_image=None, runtime=None,
                navigation=None, fps: float = 0.0, application_state=None) -> None:
        with self._condition:
            self._source = source_frame
            if ui_image is not None:
                output = io.BytesIO(); ui_image.save(output, "PNG"); self._ui_png = output.getvalue()
            runtime_data = asdict(runtime) if runtime is not None and is_dataclass(runtime) else {}
            nav_data = asdict(navigation) if navigation is not None and is_dataclass(navigation) else {}
            signal = runtime_data.get("signal_state", "UNKNOWN")
            if hasattr(signal, "value"): signal = signal.value
            app = getattr(application_state, "value", application_state)
            self._status = {
                "application_state": app or self._status["application_state"],
                "screen": nav_data.get("current_screen", self._status["screen"]),
                "signal_state": signal, "video_node": runtime_data.get("video_node"),
                "width": runtime_data.get("width"), "height": runtime_data.get("height"),
                "source_fps": runtime_data.get("fps"), "fps": round(float(fps), 2),
                "configured": bool(runtime_data.get("configured", False)),
                "streaming": bool(nav_data.get("streaming", False)),
                "focus_assist": bool(nav_data.get("focus_assist_enabled", False)),
                "zebra": bool(nav_data.get("zebra_enabled", False)),
                "crosshair": bool(nav_data.get("crosshair_enabled", False)),
                "histogram": bool(nav_data.get("histogram_enabled", False)),
                "menu_index": nav_data.get("menu_index", 0), "timestamp": time.time(),
                "generation": self._generation + 1,
            }
            self._generation += 1
            self._condition.notify_all()

    def status(self) -> dict:
        with self._condition: return dict(self._status)

    def ui_png(self) -> bytes:
        with self._condition: return self._ui_png

    def jpeg(self) -> bytes:
        with self._condition: frame = self._source
        if frame is None:
            frame = np.zeros((720, 1280, 3), np.uint8)
            cv2.putText(frame, "NO SIGNAL", (430, 380), cv2.FONT_HERSHEY_SIMPLEX,
                        2.3, (180, 180, 180), 4, cv2.LINE_AA)
        ok, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return encoded.tobytes() if ok else b""

    def wait_for_generation(self, generation: int, timeout: float = 1.0) -> int:
        with self._condition:
            self._condition.wait_for(lambda: self._generation != generation, timeout)
            return self._generation
