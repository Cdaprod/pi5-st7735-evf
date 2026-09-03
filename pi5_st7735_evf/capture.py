from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import glob
import time
from typing import Optional

import cv2
import numpy as np


def list_video_devices() -> list[str]:
    return sorted(glob.glob("/dev/video*"))


@dataclass
class CaptureStats:
    width: int = 0
    height: int = 0
    reported_fps: float = 0.0
    frames: int = 0
    failures: int = 0


class V4L2Capture:
    def __init__(
        self,
        source: str,
        width: int = 1920,
        height: int = 1080,
        fps: float = 30.0,
        fourcc: str = "",
    ) -> None:
        self.source = source
        self.width = int(width)
        self.height = int(height)
        self.fps = float(fps)
        self.fourcc = fourcc
        self.cap: Optional[cv2.VideoCapture] = None
        self.stats = CaptureStats()

    def open(self) -> None:
        self.close()

        source_arg: str | int
        if self.source.isdigit():
            source_arg = int(self.source)
        else:
            source_arg = self.source

        self.cap = cv2.VideoCapture(source_arg, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            self.close()
            raise RuntimeError(f"Unable to open capture source: {self.source}")

        # Request minimal queueing for lowest practical preview latency.
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if self.fourcc:
            if len(self.fourcc) != 4:
                raise ValueError("--fourcc must be exactly four characters")
            self.cap.set(
                cv2.CAP_PROP_FOURCC,
                cv2.VideoWriter_fourcc(*self.fourcc),
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        self.stats.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.stats.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.stats.reported_fps = float(self.cap.get(cv2.CAP_PROP_FPS))

    def read(self) -> tuple[bool, Optional[np.ndarray]]:
        if self.cap is None:
            return False, None
        ok, frame = self.cap.read()
        if ok and frame is not None:
            self.stats.frames += 1
            return True, frame
        self.stats.failures += 1
        return False, None

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def reopen_after(self, delay: float) -> None:
        self.close()
        time.sleep(max(0.0, delay))
        self.open()
