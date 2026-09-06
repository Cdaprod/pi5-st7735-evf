#!/usr/bin/env python3
"""Run the EVF. Example: python evf.py --mock --mock-signal locked"""
from __future__ import annotations

import sys
import time
import cv2
import numpy as np

from pi5_st7735_evf.capture import CaptureController, list_video_devices
from pi5_st7735_evf.config import build_parser, from_args
from pi5_st7735_evf.display import MockDisplayBackend, ST7735Backend
from pi5_st7735_evf.overlays import FpsMeter, apply_focus_peaking, apply_zebra, compose_overlays
from pi5_st7735_evf.render import bgr_to_pil, to_evf_frame
from pi5_st7735_evf.ui.status import no_signal_screen
from pi5_st7735_evf.x1301 import SignalState, X1301Client, X1301State


def mock_state(name: str) -> X1301State:
    state = SignalState.parse(name)
    return X1301State(state, "mock" if state is SignalState.LOCKED else None,
                      width=1920, height=1080, fps=30, configured=state is SignalState.LOCKED)


def mock_frame(width: int = 640, height: int = 360) -> np.ndarray:
    x = np.linspace(0, 255, width, dtype=np.uint8)
    frame = np.empty((height, width, 3), dtype=np.uint8)
    frame[..., 0] = x; frame[..., 1] = x[::-1]; frame[..., 2] = 96
    cv2.putText(frame, "X1301 MOCK", (30, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame


def main() -> int:
    args = build_parser().parse_args()
    if args.list_devices:
        print("\n".join(list_video_devices()) or "No /dev/video* devices found."); return 0
    cfg = from_args(args)
    client = X1301Client(cfg.state_file, cfg.status_command)
    capture = CaptureController(fourcc=cfg.capture_fourcc)
    display = MockDisplayBackend(cfg.width, cfg.height) if cfg.mock or cfg.no_display else ST7735Backend(
        width=cfg.width, height=cfg.height, dc=cfg.dc, rst=cfg.rst, spi_port=cfg.spi_port,
        spi_device=cfg.spi_device, spi_hz=cfg.spi_hz, x_offset=cfg.x_offset,
        y_offset=cfg.y_offset, gpio_backend=cfg.gpio_backend)
    overlays = set(cfg.overlays); meter = FpsMeter(); last_mode = ""
    display.open()
    try:
        while True:
            runtime = mock_state(cfg.mock_signal) if cfg.mock else client.read()
            if cfg.source and runtime.signal_state is SignalState.LOCKED:
                runtime = X1301State(runtime.signal_state, cfg.source, runtime.media_node, runtime.subdev_node,
                                     runtime.width or cfg.capture_width, runtime.height or cfg.capture_height,
                                     runtime.fps or cfg.capture_fps, True)
            streaming = runtime.ready if cfg.mock else capture.sync(runtime)
            ok, frame = (True, mock_frame()) if cfg.mock and streaming else capture.read()
            if ok and frame is not None:
                last_mode = f"{runtime.width}x{runtime.height}@{runtime.fps:g}"
                rendered = to_evf_frame(frame, display.width, display.height, cfg.mode, cfg.rotation)
                if "peaking" in overlays: rendered = apply_focus_peaking(rendered, cfg.peaking_threshold)
                if "zebra" in overlays: rendered = apply_zebra(rendered, cfg.zebra_threshold)
                image = compose_overlays(bgr_to_pil(rendered), rendered, overlays, fps=meter.tick(),
                                         source_width=frame.shape[1], source_height=frame.shape[0], label=cfg.label)
            else:
                details = {SignalState.DISCONNECTED: "HDMI disconnected",
                           SignalState.PRESENT_NO_SIGNAL: "HDMI detected / waiting",
                           SignalState.MODE_CHANGE: "Changing video mode",
                           SignalState.ERROR: "X1301 error"}
                image = no_signal_screen(display.width, display.height,
                                         details.get(runtime.signal_state, "Waiting for capture"), last_mode)
            display.show(image)
            if cfg.preview_window:
                cv2.imshow("Pi5 EVF", cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR))
                if cv2.waitKey(1) & 0xff in (27, ord("q")): break
            time.sleep(1 / 30 if streaming else .25)
    except KeyboardInterrupt:
        return 0
    finally:
        capture.close(); display.close()
        if cfg.preview_window: cv2.destroyAllWindows()


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr); raise SystemExit(1)
