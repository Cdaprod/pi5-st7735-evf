#!/usr/bin/env python3
"""Run the EVF. Examples: python evf.py; python evf.py --mock --screen live"""
from __future__ import annotations

import sys
import time
from queue import Empty, SimpleQueue
from dataclasses import replace
import cv2
import numpy as np

from pi5_st7735_evf.capture import CaptureController, list_video_devices
from pi5_st7735_evf.config import build_parser, from_args
from pi5_st7735_evf.display import MockDisplayBackend, ST7735Backend
from pi5_st7735_evf.overlays import FpsMeter
from pi5_st7735_evf.application import application_state, screen_for_state
from pi5_st7735_evf.input import InputController, InputEvent, InputMapper
from pi5_st7735_evf.navigation import MENU_ITEMS as NAV_MENU_ITEMS, NavigationState
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


def apply_source_override(runtime: X1301State, source: str, width: int,
                          height: int, fps: float) -> X1301State:
    """Override only capture addressing; producer readiness remains authoritative."""
    if not source:
        return runtime
    return replace(runtime, video_node=source,
                   width=runtime.width or width,
                   height=runtime.height or height,
                   fps=runtime.fps or fps)


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
    navigation = NavigationState(focus_assist_enabled="peaking" in overlays,
                                 zebra_enabled="zebra" in overlays,
                                 crosshair_enabled="crosshair" in overlays,
                                 histogram_enabled="histogram" in overlays,
                                 focus_threshold=cfg.peaking_threshold)
    actions = SimpleQueue()
    mapper = InputMapper()
    input_controller = InputController()
    input_controller.subscribe(lambda event: actions.put(action)
                               if (action := mapper.map(event)) else None)
    buttons = None
    if cfg.button_pins:
        from pi5_st7735_evf.input.buttons import LGPIOButtonBackend
        pins = {InputEvent[f"BUTTON_{name}"]: pin for name, pin in cfg.button_pins}
        buttons = LGPIOButtonBackend(pins, cfg.button_debounce)
    web = hub = None
    if cfg.web:
        from pi5_st7735_evf.web import SharedStateHub, WebServer
        hub = SharedStateHub(); web = WebServer(hub, actions.put, cfg.web_host, cfg.web_port); web.start()
    display.open()
    display.show(render_screen("boot", display.width, display.height))
    time.sleep(.8)
    try:
        while True:
            if buttons:
                event = buttons.poll()
                if event: input_controller.dispatch(event)
            while True:
                try: navigation.dispatch(actions.get_nowait())
                except Empty: break
            if navigation.shutdown_requested: break
            runtime = mock_state(cfg.mock_signal) if cfg.mock else client.read()
            if cfg.source:
                runtime = apply_source_override(runtime, cfg.source, cfg.capture_width,
                                                cfg.capture_height, cfg.capture_fps)
            streaming = runtime.ready if cfg.mock else capture.sync(runtime)
            ok, frame = (True, mock_frame()) if cfg.mock and streaming else capture.read()
            state = application_state(runtime, bool(ok and frame is not None))
            runtime_screen = screen_for_state(state)
            navigation.set_runtime_screen(runtime_screen,
                                          connected=runtime.signal_state is not SignalState.DISCONNECTED,
                                          streaming=state.value == "STREAMING")
            measured_fps = meter.tick() if ok and frame is not None else 0.0
            if navigation.current_screen in ("live", "focus-assist") and ok and frame is not None:
                screen = "focus-assist" if navigation.focus_assist_enabled else "live"
                image = render_screen(screen,display.width,display.height,
                                      frame=frame,fps=measured_fps,zebra=navigation.zebra_enabled,
                                      crosshair=navigation.crosshair_enabled,histogram=navigation.histogram_enabled,
                                      mode=f"{runtime.height or frame.shape[0]}p{runtime.fps:g}",
                                      resize_mode=cfg.mode,rotation=cfg.rotation,
                                      peaking_threshold=navigation.focus_threshold,
                                      zebra_threshold=cfg.zebra_threshold)
            else:
                screen = navigation.current_screen
                kwargs = {"phase": int(time.monotonic()*3), "runtime": runtime}
                if screen == "menu":
                    enabled = (navigation.focus_assist_enabled, True, navigation.zebra_enabled,
                               navigation.crosshair_enabled, navigation.histogram_enabled)
                    values = tuple("ON" if value else "OFF" for value in enabled)
                    items = tuple((name, values[i] if i < len(values) else ">")
                                  for i, name in enumerate(NAV_MENU_ITEMS))
                    kwargs.update(selected=navigation.menu_index, items=items)
                elif screen == "focus-settings": kwargs.update(threshold=max(0, navigation.focus_threshold // 18))
                image=render_screen(screen,display.width,display.height,**kwargs)
            display.show(image)
            if hub: hub.publish(source_frame=frame if ok else None, ui_image=image, runtime=runtime,
                                navigation=navigation, fps=measured_fps, application_state=state)
            if cfg.preview_window:
                cv2.imshow("Pi5 EVF", cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR))
                if cv2.waitKey(1) & 0xff in (27, ord("q")): break
            time.sleep(1 / 30 if streaming else .25)
    except KeyboardInterrupt:
        return 0
    finally:
        try: display.show(render_screen("shutdown",display.width,display.height)); time.sleep(.35)
        except Exception: pass
        if web: web.close()
        if buttons: buttons.close()
        capture.close(); display.close()
        if cfg.preview_window: cv2.destroyAllWindows()


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr); raise SystemExit(1)
