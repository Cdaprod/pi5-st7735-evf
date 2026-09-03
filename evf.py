#!/usr/bin/env python3
from __future__ import annotations

import sys
import time
import traceback

import cv2

from pi5_st7735_evf.capture import V4L2Capture, list_video_devices
from pi5_st7735_evf.config import build_parser, from_args
from pi5_st7735_evf.display import ST7735Display
from pi5_st7735_evf.overlays import (
    FpsMeter,
    apply_focus_peaking,
    apply_zebra,
    compose_overlays,
)
from pi5_st7735_evf.render import bgr_to_pil, to_evf_frame


def print_devices() -> None:
    devices = list_video_devices()
    if not devices:
        print("No /dev/video* devices found.")
        return
    print("Candidate V4L2 video nodes:")
    for dev in devices:
        print(f"  {dev}")


def handle_key(key: int, state: dict) -> bool:
    if key in (27, ord("q")):
        return False
    if key == ord("m"):
        state["mode"] = "crop" if state["mode"] == "fit" else "fit"
    elif key == ord("o"):
        state["show_overlays"] = not state["show_overlays"]
    elif key == ord("p"):
        state["toggle_overlay"]("peaking")
    elif key == ord("z"):
        state["toggle_overlay"]("zebra")
    elif key == ord("g"):
        state["toggle_overlay"]("thirds")
    elif key == ord("c"):
        state["toggle_overlay"]("crosshair")
    elif key == ord("h"):
        state["toggle_overlay"]("histogram")
    return True


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_devices:
        print_devices()
        return 0

    cfg = from_args(args)
    active_overlays = set(cfg.overlays)

    def toggle_overlay(name: str) -> None:
        if name in active_overlays:
            active_overlays.remove(name)
        else:
            active_overlays.add(name)
        print(f"[overlay] {name}={'on' if name in active_overlays else 'off'}")

    state = {
        "mode": cfg.mode,
        "show_overlays": True,
        "toggle_overlay": toggle_overlay,
    }

    capture = V4L2Capture(
        cfg.source,
        cfg.capture_width,
        cfg.capture_height,
        cfg.capture_fps,
        cfg.capture_fourcc,
    )

    display = None
    if not cfg.no_display:
        display = ST7735Display(
            width=cfg.width,
            height=cfg.height,
            dc=cfg.dc,
            rst=cfg.rst,
            spi_port=cfg.spi_port,
            spi_device=cfg.spi_device,
            spi_hz=cfg.spi_hz,
            x_offset=cfg.x_offset,
            y_offset=cfg.y_offset,
            gpio_backend=cfg.gpio_backend,
        )

    fps_meter = FpsMeter()

    print(
        "[evf] "
        f"source={cfg.source} "
        f"capture={cfg.capture_width}x{cfg.capture_height}@{cfg.capture_fps:g} "
        f"display={cfg.width}x{cfg.height} "
        f"spi={cfg.spi_hz / 1_000_000:.1f}MHz "
        f"mode={state['mode']}"
    )

    try:
        capture.open()
        print(
            "[capture] opened "
            f"{capture.stats.width}x{capture.stats.height} "
            f"reported_fps={capture.stats.reported_fps:g}"
        )

        if display is not None:
            display.open()
            print("[display] ST7735 initialized")

        consecutive_failures = 0

        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                consecutive_failures += 1
                if consecutive_failures < 10:
                    time.sleep(0.01)
                    continue

                print("[capture] frame failures; attempting capture reopen")
                try:
                    capture.reopen_after(cfg.reconnect_delay)
                    consecutive_failures = 0
                    continue
                except Exception as exc:
                    print(f"[capture] reopen failed: {exc}", file=sys.stderr)
                    time.sleep(cfg.reconnect_delay)
                    continue

            consecutive_failures = 0
            fps = fps_meter.tick()

            evf_bgr = to_evf_frame(
                frame,
                cfg.width,
                cfg.height,
                state["mode"],
                cfg.rotation,
            )

            if "peaking" in active_overlays:
                evf_bgr = apply_focus_peaking(
                    evf_bgr,
                    threshold=cfg.peaking_threshold,
                )

            if "zebra" in active_overlays:
                evf_bgr = apply_zebra(
                    evf_bgr,
                    threshold=cfg.zebra_threshold,
                )

            image = bgr_to_pil(evf_bgr)

            if state["show_overlays"]:
                image = compose_overlays(
                    image,
                    evf_bgr,
                    active_overlays,
                    fps=fps,
                    source_width=frame.shape[1],
                    source_height=frame.shape[0],
                    label=cfg.label,
                )

            if display is not None:
                display.show(image)

            if cfg.preview_window:
                # Preview the exact composed 128x128 image.
                preview_bgr = cv2.cvtColor(
                    __import__("numpy").array(image),
                    cv2.COLOR_RGB2BGR,
                )
                cv2.imshow("Pi5 ST7735 EVF", preview_bgr)
                key = cv2.waitKey(1) & 0xFF
                if not handle_key(key, state):
                    break

    except KeyboardInterrupt:
        print("\n[evf] interrupted")
    except Exception as exc:
        print(f"[fatal] {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1
    finally:
        capture.close()
        if display is not None:
            display.close()
        if cfg.preview_window:
            cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
