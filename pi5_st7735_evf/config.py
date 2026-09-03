from __future__ import annotations

from dataclasses import dataclass
import argparse
import os


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value in (None, "") else int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value in (None, "") else float(value)


def _env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None else value


@dataclass(slots=True)
class EvfConfig:
    source: str = "/dev/video0"
    capture_width: int = 1920
    capture_height: int = 1080
    capture_fps: float = 30.0
    capture_fourcc: str = ""

    width: int = 128
    height: int = 128
    mode: str = "fit"
    rotation: int = 0

    spi_port: int = 0
    spi_device: int = 0
    spi_hz: int = 16_000_000
    dc: int = 24
    rst: int = 25
    x_offset: int = 0
    y_offset: int = 0
    gpio_backend: str = "lgpio"

    overlays: tuple[str, ...] = ("rec", "fps", "resolution", "clock", "crosshair")
    peaking_threshold: int = 90
    zebra_threshold: int = 245
    label: str = "Z7"

    reconnect_delay: float = 1.0
    no_display: bool = False
    preview_window: bool = False


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Raspberry Pi 5 ST7735 EVF for HDMI-to-CSI-2 / V4L2 capture."
    )
    p.add_argument("--source", default=_env_str("EVF_SOURCE", "/dev/video0"))
    p.add_argument("--capture-width", type=int, default=_env_int("EVF_CAPTURE_WIDTH", 1920))
    p.add_argument("--capture-height", type=int, default=_env_int("EVF_CAPTURE_HEIGHT", 1080))
    p.add_argument("--capture-fps", type=float, default=_env_float("EVF_CAPTURE_FPS", 30.0))
    p.add_argument("--fourcc", default=_env_str("EVF_CAPTURE_FOURCC", ""))

    p.add_argument("--mode", choices=("fit", "crop"), default=_env_str("EVF_MODE", "fit"))
    p.add_argument("--rotation", type=int, choices=(0, 90, 180, 270),
                   default=_env_int("EVF_ROTATION", 0))

    p.add_argument("--spi-port", type=int, default=_env_int("EVF_SPI_PORT", 0))
    p.add_argument("--spi-device", type=int, default=_env_int("EVF_SPI_DEVICE", 0))
    p.add_argument("--spi-hz", type=int, default=_env_int("EVF_SPI_HZ", 16_000_000))
    p.add_argument("--dc", type=int, default=_env_int("EVF_DC", 24))
    p.add_argument("--rst", type=int, default=_env_int("EVF_RST", 25))
    p.add_argument("--x-offset", type=int, default=_env_int("EVF_X_OFFSET", 0))
    p.add_argument("--y-offset", type=int, default=_env_int("EVF_Y_OFFSET", 0))
    p.add_argument("--gpio-backend", choices=("lgpio", "adafruit"),
                   default=_env_str("EVF_GPIO_BACKEND", "lgpio"))

    p.add_argument(
        "--overlay",
        default=_env_str("EVF_OVERLAY", "rec,fps,resolution,clock,crosshair"),
        help="Comma-separated overlays: rec,fps,resolution,clock,temp,crosshair,thirds,histogram,peaking,zebra,label",
    )
    p.add_argument("--peaking-threshold", type=int,
                   default=_env_int("EVF_PEAKING_THRESHOLD", 90))
    p.add_argument("--zebra-threshold", type=int,
                   default=_env_int("EVF_ZEBRA_THRESHOLD", 245))
    p.add_argument("--label", default=_env_str("EVF_LABEL", "Z7"))

    p.add_argument("--reconnect-delay", type=float, default=1.0)
    p.add_argument("--no-display", action="store_true",
                   help="Do not open the ST7735. Useful for capture/render testing.")
    p.add_argument("--preview-window", action="store_true",
                   help="Open a desktop OpenCV preview in addition to the TFT.")
    p.add_argument("--list-devices", action="store_true",
                   help="Print candidate /dev/video* nodes and exit.")
    return p


def from_args(args: argparse.Namespace) -> EvfConfig:
    overlays = tuple(
        x.strip().lower() for x in args.overlay.split(",") if x.strip()
    )
    return EvfConfig(
        source=args.source,
        capture_width=args.capture_width,
        capture_height=args.capture_height,
        capture_fps=args.capture_fps,
        capture_fourcc=args.fourcc,
        mode=args.mode,
        rotation=args.rotation,
        spi_port=args.spi_port,
        spi_device=args.spi_device,
        spi_hz=args.spi_hz,
        dc=args.dc,
        rst=args.rst,
        x_offset=args.x_offset,
        y_offset=args.y_offset,
        gpio_backend=args.gpio_backend,
        overlays=overlays,
        peaking_threshold=args.peaking_threshold,
        zebra_threshold=args.zebra_threshold,
        label=args.label,
        reconnect_delay=args.reconnect_delay,
        no_display=args.no_display,
        preview_window=args.preview_window,
    )
