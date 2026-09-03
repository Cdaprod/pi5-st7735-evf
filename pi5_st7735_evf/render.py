from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


def rotate_bgr(frame: np.ndarray, rotation: int) -> np.ndarray:
    if rotation == 0:
        return frame
    if rotation == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if rotation == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    if rotation == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    raise ValueError(f"Unsupported rotation: {rotation}")


def resize_fit(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """Fit complete frame inside destination while preserving aspect ratio."""
    src_h, src_w = frame.shape[:2]
    scale = min(width / src_w, height / src_h)
    dst_w = max(1, int(round(src_w * scale)))
    dst_h = max(1, int(round(src_h * scale)))

    resized = cv2.resize(
        frame,
        (dst_w, dst_h),
        interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR,
    )

    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    x = (width - dst_w) // 2
    y = (height - dst_h) // 2
    canvas[y:y + dst_h, x:x + dst_w] = resized
    return canvas


def resize_crop(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """Fill destination completely, center-cropping excess image."""
    src_h, src_w = frame.shape[:2]
    scale = max(width / src_w, height / src_h)
    dst_w = max(1, int(round(src_w * scale)))
    dst_h = max(1, int(round(src_h * scale)))

    resized = cv2.resize(
        frame,
        (dst_w, dst_h),
        interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR,
    )
    x = max(0, (dst_w - width) // 2)
    y = max(0, (dst_h - height) // 2)
    return resized[y:y + height, x:x + width]


def to_evf_frame(
    frame_bgr: np.ndarray,
    width: int,
    height: int,
    mode: str,
    rotation: int,
) -> np.ndarray:
    frame_bgr = rotate_bgr(frame_bgr, rotation)
    if mode == "fit":
        return resize_fit(frame_bgr, width, height)
    if mode == "crop":
        return resize_crop(frame_bgr, width, height)
    raise ValueError(f"Unknown render mode: {mode}")


def bgr_to_pil(frame_bgr: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb, mode="RGB")
