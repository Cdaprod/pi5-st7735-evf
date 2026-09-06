#!/usr/bin/env python3
"""Run the EVF. Examples: python evf.py; python evf.py --mock --screen live"""
from __future__ import annotations

import sys
import time
from dataclasses import replace
import cv2
import numpy as np

from pi5_st7735_evf.capture import CaptureController, list_video_devices
from pi5_st7735_evf.config import build_parser, from_args
from pi5_st7735_evf.display import MockDisplayBackend, ST7735Backend
from pi5_st7735_evf.overlays import FpsMeter
from pi5_st7735_evf.application import application_state, screen_for_state
from pi5_st7735_evf.ui.screens import SCREEN_NAMES, render_screen
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
    if cfg.screen:
        if not cfg.mock:
            print("--screen requires --mock", file=sys.stderr); return 2
        if cfg.screen not in SCREEN_NAMES:
            print(f"unknown screen {cfg.screen!r}; choose: {', '.join(SCREEN_NAMES)}", file=sys.stderr); return 2
        from pathlib import Path
        output=Path(cfg.output or f"artifacts/ui/{cfg.screen}.png"); output.parent.mkdir(parents=True,exist_ok=True)
        render_screen(cfg.screen,cfg.width,cfg.height).save(output); print(output); return 0
    client = X1301Client(cfg.state_file, cfg.status_command, cfg.diagnostic_command)
    capture = CaptureController(fourcc=cfg.capture_fourcc, reconnect_delay=cfg.reconnect_delay)
    display = MockDisplayBackend(cfg.width, cfg.height) if cfg.mock or cfg.no_display else ST7735Backend(
        width=cfg.width, height=cfg.height, dc=cfg.dc, rst=cfg.rst, spi_port=cfg.spi_port,
        spi_device=cfg.spi_device, spi_hz=cfg.spi_hz, x_offset=cfg.x_offset,
        y_offset=cfg.y_offset, gpio_backend=cfg.gpio_backend)
    overlays = set(cfg.overlays); meter = FpsMeter()
    display.open()
    display.show(render_screen("boot", display.width, display.height))
    time.sleep(.8)
    try:
        while True:
            runtime = mock_state(cfg.mock_signal) if cfg.mock else client.read()
            if cfg.source and runtime.signal_state is SignalState.LOCKED:
                runtime = replace(runtime, video_node=cfg.source,
                                  width=runtime.width or cfg.capture_width,
                                  height=runtime.height or cfg.capture_height,
                                  fps=runtime.fps or cfg.capture_fps, configured=True)
            streaming = runtime.ready if cfg.mock else capture.sync(runtime)
            ok, frame = (True, mock_frame()) if cfg.mock and streaming else capture.read()
            if ok and frame is not None:
                image = render_screen("focus-assist" if "peaking" in overlays else "live",display.width,display.height,
                                      frame=frame,fps=meter.tick(),zebra="zebra" in overlays,
                                      crosshair="crosshair" in overlays,mode=f"{runtime.height or frame.shape[0]}p{runtime.fps:g}",
                                      resize_mode=cfg.mode,rotation=cfg.rotation,
                                      peaking_threshold=cfg.peaking_threshold,
                                      zebra_threshold=cfg.zebra_threshold)
            else:
                state=application_state(runtime,False); screen=screen_for_state(state)
                image=render_screen(screen,display.width,display.height,phase=int(time.monotonic()*3),runtime=runtime)
            display.show(image)
            if cfg.preview_window:
                cv2.imshow("Pi5 EVF", cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR))
                if cv2.waitKey(1) & 0xff in (27, ord("q")): break
            time.sleep(1 / 30 if streaming else .25)
    except KeyboardInterrupt:
        return 0
    finally:
        try: display.show(render_screen("shutdown",display.width,display.height)); time.sleep(.35)
        except Exception: pass
        capture.close(); display.close()
        if cfg.preview_window: cv2.destroyAllWindows()


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr); raise SystemExit(1)
