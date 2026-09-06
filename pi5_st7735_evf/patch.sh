 (cd "$(git rev-parse --show-toplevel)" && printf '%s' 'diff --git a/README.md b/README.md
index 0d65b4a41a1243c7b4234c7b4157e500898a71bf..7038901939bb0b0f934ad8ce5d7edcd3ae36301e 100644
--- a/README.md
+++ b/README.md
@@ -42,50 +42,70 @@ The project defaults to SPI bus `0`, device `0`, DC `24`, and RST `25`.
 The SPI transport still uses `Adafruit_GPIO.SPI.SpiDev`, matching the upstream examples.
 
 ## Quick start
 
 ```bash
 git clone https://github.com/Cdaprod/pi5-st7735-evf.git
 cd pi5-st7735-evf
 
 sudo ./scripts/install_pi.sh
 source .venv/bin/activate
 
 ./tools/probe_capture.sh
 python evf.py --list-devices
 python evf.py --source /dev/video0 --mode fit
 ```
 
 Normally the X1301 watcher supplies the video node. Development requires no Pi:
 
 ```bash
 python evf.py --mock --mock-signal locked --preview-window
 python evf.py --mock --mock-signal disconnected --preview-window
 python tools/mock_x1301_state.py --state locked --width 1920 --height 1080 --video /dev/video0
 python -m unittest discover -s tests -v
 ```
 
+Render the approved screens and exact-size inspection gallery without hardware:
+
+```bash
+python evf.py --mock --screen boot
+python evf.py --mock --screen no-signal
+python evf.py --mock --screen source-present
+python evf.py --mock --screen live
+python evf.py --mock --screen focus-assist
+python evf.py --mock --screen menu
+python evf.py --mock --screen focus-settings
+python evf.py --mock --screen system-info
+python evf.py --mock --screen capture-error
+python evf.py --mock --screen mode-change
+python evf.py --mock --screen shutdown
+python tools/render_ui_gallery.py --contact-sheet
+```
+
+PNGs are written under `artifacts/ui/`. Launch on the configured Raspberry Pi
+with `source .venv/bin/activate && python evf.py`.
+
 If the driver clone is not already present, `scripts/install_pi.sh` clones:
 
 ```text
 https://github.com/cskau/Python_ST7735.git
 ```
 
 into `vendor/Python_ST7735` and installs it into the virtual environment.
 
 ## First hardware test: display only
 
 Before connecting the HDMI capture source:
 
 ```bash
 source .venv/bin/activate
 python tools/display_test.py
 ```
 
 If the image is shifted, use panel offsets:
 
 ```bash
 python tools/display_test.py --x-offset 2 --y-offset 1
 ```
 
 Then use the same values with `evf.py`.
 
diff --git a/artifacts/ui/boot.png b/artifacts/ui/boot.png
new file mode 100644
index 0000000000000000000000000000000000000000..ddf9ded569e776136dc0b1dedc962d8e7576759e
GIT binary patch
literal 1802
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

literal 0
HcmV?d00001

diff --git a/artifacts/ui/capture-error.png b/artifacts/ui/capture-error.png
new file mode 100644
index 0000000000000000000000000000000000000000..138f7133623c95e88400051cdd4c0d7602810544
GIT binary patch
literal 2913
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
AWdHyG

literal 0
HcmV?d00001

diff --git a/artifacts/ui/contact-sheet.png b/artifacts/ui/contact-sheet.png
new file mode 100644
index 0000000000000000000000000000000000000000..0d3c0a5236d929b0c7d87b484ff17732765ab56a
GIT binary patch
literal 47903
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
WM`!V~57C<YDfE=?$*kix*Z&LUg*a*e

literal 0
HcmV?d00001

diff --git a/artifacts/ui/focus-assist.png b/artifacts/ui/focus-assist.png
new file mode 100644
index 0000000000000000000000000000000000000000..a25cf975f5ab4851ad092cddd8be545c43bc9024
GIT binary patch
literal 3963
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
RkxNqzwA6LfN>yy0{STjoR>=SW

literal 0
HcmV?d00001

diff --git a/artifacts/ui/focus-settings.png b/artifacts/ui/focus-settings.png
new file mode 100644
index 0000000000000000000000000000000000000000..b036dc6ae0aed4fd9cabf6e7ed3807a7b7a3e56d
GIT binary patch
literal 4219
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

literal 0
HcmV?d00001

diff --git a/artifacts/ui/live.png b/artifacts/ui/live.png
new file mode 100644
index 0000000000000000000000000000000000000000..b6cd31302d3c4cb2e4758cd5f8e7703823729af6
GIT binary patch
literal 3818
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

literal 0
HcmV?d00001

diff --git a/artifacts/ui/menu.png b/artifacts/ui/menu.png
new file mode 100644
index 0000000000000000000000000000000000000000..413b60aa39aa936ea321bfa8d7bdf2e5ecc58936
GIT binary patch
literal 4882
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
BW+ngt

literal 0
HcmV?d00001

diff --git a/artifacts/ui/mode-change.png b/artifacts/ui/mode-change.png
new file mode 100644
index 0000000000000000000000000000000000000000..8a9e204cabbb2e083d3b02a8dad9e7bb02cefddd
GIT binary patch
literal 2218
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

literal 0
HcmV?d00001

diff --git a/artifacts/ui/no-signal.png b/artifacts/ui/no-signal.png
new file mode 100644
index 0000000000000000000000000000000000000000..0cc8f87ad5db678b925e5d93888699e6f5b4e90a
GIT binary patch
literal 2647
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
BC~E)!

literal 0
HcmV?d00001

diff --git a/artifacts/ui/shutdown.png b/artifacts/ui/shutdown.png
new file mode 100644
index 0000000000000000000000000000000000000000..5482843083769040e678058b8554d1cae367da41
GIT binary patch
literal 2289
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

literal 0
HcmV?d00001

diff --git a/artifacts/ui/source-present.png b/artifacts/ui/source-present.png
new file mode 100644
index 0000000000000000000000000000000000000000..db1f8e2e69425498f7ef0407d5a8d5c88beafa89
GIT binary patch
literal 1773
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
M5JPi=dXQ_v-;?iNRR910

literal 0
HcmV?d00001

diff --git a/artifacts/ui/system-info.png b/artifacts/ui/system-info.png
new file mode 100644
index 0000000000000000000000000000000000000000..fe285db672847f5f9ffd29bbed2d7c82a950851e
GIT binary patch
literal 3434
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

literal 0
HcmV?d00001

diff --git a/docs/UI_DESIGN.md b/docs/UI_DESIGN.md
new file mode 100644
index 0000000000000000000000000000000000000000..a3c4ada40bdd2012d7c77d724ec2c797eddb501a
--- /dev/null
+++ b/docs/UI_DESIGN.md
@@ -0,0 +1,56 @@
+# Approved ST7735 UI specification
+
+The approved reference board is the current visual direction and product UI
+specification for the 128×128 ST7735 prototype. It is not a disposable mockup.
+All coordinates are authored at the panel'\''s native resolution.
+
+## Visual system
+
+The interface uses black, clean white DejaVu Sans typography, thin gray rules,
+and sparse camera-monitor telemetry. Green means active/locked/OK, yellow means
+waiting or reconfiguration, red means error or focus peaking, blue means
+selection, and gray means unavailable. Font roles are centralized as tiny,
+small, body, header, and large, with Pillow'\''s built-in font as a safe fallback.
+
+Icons are drawn from Pillow lines, rectangles, polygons, ellipses, and arcs. The
+set contains camera/video, connected and disconnected displays, gear,
+information, warning, mode-change arrows, power, battery, and signal status. No
+external icon package or web asset is required.
+
+## Native layout
+
+Live View reserves pixels 0–15 for status, 16–99 for the source image, and
+100–127 for the HUD. The image is aspect-preserving and center-cropped into the
+viewport. Four short green corner guides frame it. The HUD contains FPS, an
+actual luminance histogram, and concise ISO/ZEBRA status. Focus edges are thin
+red accents; zebra uses alternating diagonal marks above its threshold.
+
+Menus use a 19-pixel icon/header area and 15-pixel rows. The active row is a
+full-width blue band. Main menu order is Focus Peaking, Zebra, Crosshair,
+Histogram, Brightness, Display Rotation, and System Info. Focus Peaking detail
+contains Enable, Color, Threshold, and Thickness plus an analyzed live preview.
+
+## Screen and runtime states
+
+| Runtime condition | Approved screen |
+|---|---|
+| Startup | EVF / PI5 + X1301 splash |
+| `DISCONNECTED` | No Signal |
+| `PRESENT_NO_SIGNAL` | HDMI Detected / animated waiting dots |
+| `LOCKED`, capture opening | Mode Change |
+| `LOCKED`, streaming | Live View |
+| Focus assist selected | Live View with red peaking |
+| `MODE_CHANGE` | Mode Change with indeterminate yellow bar |
+| Capture/runtime failure | Capture Error |
+| Clean exit | Shutting Down |
+
+Animations use elapsed-time phases and never sleep inside renderers. The capture
+loop remains responsible for pacing, retry, and input servicing. System Info
+takes resolution, rate, video node, and media node from current X1301 state.
+
+## 128-pixel constraints
+
+The complete diagnostic table cannot remain readable at once, so eight System
+Info rows appear per scroll page. Header and HUD labels use compact typography,
+and the focus preview is 120×32 pixels. These are spacing adjustments only;
+hierarchy, content, semantics, and the approved visual language are preserved.
diff --git a/docs/todo/AGENTS.md b/docs/todo/AGENTS.md
index b41f54c9bee100503aa0961af48c098e9b714f78..e69d028206f018c7b135c1783b4122f837a609fb 100644
--- a/docs/todo/AGENTS.md
+++ b/docs/todo/AGENTS.md
@@ -1,6 +1,7 @@
 # EVF integration ledger
 
+- [x] Implement the approved native 128×128 camera-monitor UI, programmatic icons, analysis overlays, menus, diagnostics, mock gallery, tests, and UI specification.
 - [x] Consume X1301 state file with JSON command fallback.
 - [x] Add resilient capture lifecycle, application states, no-signal UI, display abstraction, semantic input/menu/LED APIs, mock mode, fixture writer, tests, service, and architecture docs.
 - [ ] Validate ST7735 offsets, late HDMI connection, timing changes, and capture recovery on Raspberry Pi 5 hardware.
 - [ ] Implement and benchmark the selected DSI compositor backend after panel selection.
diff --git a/evf.py b/evf.py
index 365ae1f15aefe9de3233ac96ab720d73b9b04491..fe37f8f9f226668fb3e95c109ac0abdc0981b59b 100755
--- a/evf.py
+++ b/evf.py
@@ -1,84 +1,95 @@
 #!/usr/bin/env python3
-"""Run the EVF. Example: python evf.py --mock --mock-signal locked"""
+"""Run the EVF. Examples: python evf.py; python evf.py --mock --screen live"""
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
-from pi5_st7735_evf.ui.status import no_signal_screen
+from pi5_st7735_evf.application import application_state, screen_for_state
+from pi5_st7735_evf.ui.screens import SCREEN_NAMES, render_screen
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
+    if cfg.screen:
+        if not cfg.mock:
+            print("--screen requires --mock", file=sys.stderr); return 2
+        if cfg.screen not in SCREEN_NAMES:
+            print(f"unknown screen {cfg.screen!r}; choose: {'\'', '\''.join(SCREEN_NAMES)}", file=sys.stderr); return 2
+        from pathlib import Path
+        output=Path(cfg.output or f"artifacts/ui/{cfg.screen}.png"); output.parent.mkdir(parents=True,exist_ok=True)
+        render_screen(cfg.screen,cfg.width,cfg.height).save(output); print(output); return 0
     client = X1301Client(cfg.state_file, cfg.status_command)
     capture = CaptureController(fourcc=cfg.capture_fourcc)
     display = MockDisplayBackend(cfg.width, cfg.height) if cfg.mock or cfg.no_display else ST7735Backend(
         width=cfg.width, height=cfg.height, dc=cfg.dc, rst=cfg.rst, spi_port=cfg.spi_port,
         spi_device=cfg.spi_device, spi_hz=cfg.spi_hz, x_offset=cfg.x_offset,
         y_offset=cfg.y_offset, gpio_backend=cfg.gpio_backend)
     overlays = set(cfg.overlays); meter = FpsMeter(); last_mode = ""
     display.open()
+    display.show(render_screen("boot", display.width, display.height))
+    time.sleep(.8)
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
-                image = compose_overlays(bgr_to_pil(rendered), rendered, overlays, fps=meter.tick(),
-                                         source_width=frame.shape[1], source_height=frame.shape[0], label=cfg.label)
+                image = render_screen("focus-assist" if "peaking" in overlays else "live",display.width,display.height,
+                                      frame=rendered,fps=meter.tick(),zebra="zebra" in overlays,
+                                      crosshair="crosshair" in overlays,mode=f"{runtime.height or frame.shape[0]}p{runtime.fps:g}")
             else:
-                details = {SignalState.DISCONNECTED: "HDMI disconnected",
-                           SignalState.PRESENT_NO_SIGNAL: "HDMI detected / waiting",
-                           SignalState.MODE_CHANGE: "Changing video mode",
-                           SignalState.ERROR: "X1301 error"}
-                image = no_signal_screen(display.width, display.height,
-                                         details.get(runtime.signal_state, "Waiting for capture"), last_mode)
+                state=application_state(runtime,False); screen=screen_for_state(state)
+                if runtime.signal_state is SignalState.LOCKED and not streaming: screen="capture-error"
+                image=render_screen(screen,display.width,display.height,phase=int(time.monotonic()*3),runtime=runtime)
             display.show(image)
             if cfg.preview_window:
                 cv2.imshow("Pi5 EVF", cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR))
                 if cv2.waitKey(1) & 0xff in (27, ord("q")): break
             time.sleep(1 / 30 if streaming else .25)
     except KeyboardInterrupt:
         return 0
     finally:
+        try: display.show(render_screen("shutdown",display.width,display.height)); time.sleep(.35)
+        except Exception: pass
         capture.close(); display.close()
         if cfg.preview_window: cv2.destroyAllWindows()
 
 
 if __name__ == "__main__":
     try: raise SystemExit(main())
     except Exception as exc:
         print(f"fatal: {exc}", file=sys.stderr); raise SystemExit(1)
diff --git a/pi5_st7735_evf/application.py b/pi5_st7735_evf/application.py
index 6c4b32e6ef2bf8f15736c0ca86cca8aaa79aea85..f667609764c8e0c942efc3c5a672c355f71ac8db 100644
--- a/pi5_st7735_evf/application.py
+++ b/pi5_st7735_evf/application.py
@@ -1,18 +1,31 @@
 from enum import Enum
 from .x1301.state import SignalState
 
 
 class ApplicationState(str, Enum):
     BOOTING = "BOOTING"
     NO_SOURCE = "NO_SOURCE"
     SOURCE_PRESENT = "SOURCE_PRESENT"
     VIDEO_LOCKED = "VIDEO_LOCKED"
     STREAMING = "STREAMING"
+    MODE_CHANGE = "MODE_CHANGE"
+    CAPTURE_ERROR = "CAPTURE_ERROR"
     ERROR = "ERROR"
 
 
 def application_state(x1301, streaming: bool = False) -> ApplicationState:
     if x1301.signal_state is SignalState.ERROR: return ApplicationState.ERROR
     if x1301.signal_state is SignalState.DISCONNECTED: return ApplicationState.NO_SOURCE
-    if x1301.signal_state in (SignalState.PRESENT_NO_SIGNAL, SignalState.MODE_CHANGE): return ApplicationState.SOURCE_PRESENT
+    if x1301.signal_state is SignalState.MODE_CHANGE: return ApplicationState.MODE_CHANGE
+    if x1301.signal_state is SignalState.PRESENT_NO_SIGNAL: return ApplicationState.SOURCE_PRESENT
     return ApplicationState.STREAMING if streaming else ApplicationState.VIDEO_LOCKED
+
+
+def screen_for_state(state: ApplicationState) -> str:
+    """Map runtime application state to the approved visual state."""
+    return {
+        ApplicationState.BOOTING: "boot", ApplicationState.NO_SOURCE: "no-signal",
+        ApplicationState.SOURCE_PRESENT: "source-present", ApplicationState.VIDEO_LOCKED: "mode-change",
+        ApplicationState.STREAMING: "live", ApplicationState.MODE_CHANGE: "mode-change",
+        ApplicationState.CAPTURE_ERROR: "capture-error", ApplicationState.ERROR: "capture-error",
+    }[state]
diff --git a/pi5_st7735_evf/config.py b/pi5_st7735_evf/config.py
index 285322b76370baf0945d5ebac212b10828000cd6..888011cb417cdeba18daa664e85f194ddc9c1c65 100644
--- a/pi5_st7735_evf/config.py
+++ b/pi5_st7735_evf/config.py
@@ -33,50 +33,52 @@ class EvfConfig:
     mode: str = "fit"
     rotation: int = 0
     display_backend: str = "st7735"
 
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
     state_file: str = "/run/x1301/state.env"
     status_command: str = "hdmi-status.sh"
     mock: bool = False
     mock_signal: str = "locked"
+    screen: str = ""
+    output: str = ""
 
 
 def build_parser() -> argparse.ArgumentParser:
     p = argparse.ArgumentParser(
         description="Raspberry Pi 5 ST7735 EVF for HDMI-to-CSI-2 / V4L2 capture."
     )
     p.add_argument("--source", default=_env_str("EVF_SOURCE", ""),
                    help="Manual capture override; normally supplied by X1301 state")
     p.add_argument("--capture-width", type=int, default=_env_int("EVF_CAPTURE_WIDTH", 1920))
     p.add_argument("--capture-height", type=int, default=_env_int("EVF_CAPTURE_HEIGHT", 1080))
     p.add_argument("--capture-fps", type=float, default=_env_float("EVF_CAPTURE_FPS", 30.0))
     p.add_argument("--fourcc", default=_env_str("EVF_CAPTURE_FOURCC", ""))
 
     p.add_argument("--mode", choices=("fit", "crop"), default=_env_str("EVF_MODE", "fit"))
     p.add_argument("--display-backend", choices=("st7735",), default=_env_str("DISPLAY_BACKEND", "st7735"))
     p.add_argument("--width", type=int, default=_env_int("DISPLAY_WIDTH", 128))
     p.add_argument("--height", type=int, default=_env_int("DISPLAY_HEIGHT", 128))
     p.add_argument("--rotation", type=int, choices=(0, 90, 180, 270),
                    default=_env_int("DISPLAY_ROTATION", _env_int("EVF_ROTATION", 0)))
 
     p.add_argument("--spi-port", type=int, default=_env_int("EVF_SPI_PORT", 0))
     p.add_argument("--spi-device", type=int, default=_env_int("EVF_SPI_DEVICE", 0))
     p.add_argument("--spi-hz", type=int, default=_env_int("EVF_SPI_HZ", 16_000_000))
     p.add_argument("--dc", type=int, default=_env_int("EVF_DC", 24))
     p.add_argument("--rst", type=int, default=_env_int("EVF_RST", 25))
@@ -84,65 +86,69 @@ def build_parser() -> argparse.ArgumentParser:
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
     p.add_argument("--x1301-state-file", default=_env_str("X1301_STATE_FILE", "/run/x1301/state.env"))
     p.add_argument("--x1301-status-command", default=_env_str("X1301_STATUS_COMMAND", "hdmi-status.sh"))
     p.add_argument("--mock", action="store_true", help="Run without capture or Raspberry Pi hardware")
+    p.add_argument("--screen", default="", help="Render one approved mock screen to PNG and exit")
+    p.add_argument("--output", default="", help="PNG destination for --screen (default: artifacts/ui/<screen>.png)")
     p.add_argument("--mock-signal", choices=("locked", "disconnected", "present-no-signal", "mode-change", "error"),
                    default="locked")
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
         width=args.width,
         height=args.height,
         rotation=args.rotation,
         display_backend=args.display_backend,
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
         state_file=args.x1301_state_file,
         status_command=args.x1301_status_command,
         mock=args.mock,
         mock_signal=args.mock_signal,
+        screen=args.screen,
+        output=args.output,
     )
diff --git a/pi5_st7735_evf/overlays.py b/pi5_st7735_evf/overlays.py
index d6578fd4f91f2a3ea7e163988cbcaea7d498720f..a8394e70edc50349c6d5e57471d276eef147ea3c 100644
--- a/pi5_st7735_evf/overlays.py
+++ b/pi5_st7735_evf/overlays.py
@@ -34,56 +34,58 @@ FONT_10 = _font(10)
 class FpsMeter:
     window: int = 20
     samples: deque[float] = field(default_factory=lambda: deque(maxlen=20))
     last: float | None = None
 
     def tick(self) -> float:
         now = time.monotonic()
         if self.last is not None:
             dt = now - self.last
             if dt > 0:
                 self.samples.append(1.0 / dt)
         self.last = now
         if not self.samples:
             return 0.0
         return sum(self.samples) / len(self.samples)
 
 
 def read_pi_temp_c() -> float | None:
     path = Path("/sys/class/thermal/thermal_zone0/temp")
     try:
         return float(path.read_text().strip()) / 1000.0
     except Exception:
         return None
 
 
-def apply_focus_peaking(frame_bgr: np.ndarray, threshold: int = 90) -> np.ndarray:
+def apply_focus_peaking(frame_bgr: np.ndarray, threshold: int = 90, thickness: int = 1) -> np.ndarray:
     """Overlay high-frequency edges in red."""
     gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
     lap = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
     mag = cv2.convertScaleAbs(lap)
     mask = mag >= int(threshold)
+    if thickness > 1:
+        mask = cv2.dilate(mask.astype(np.uint8), np.ones((min(thickness, 3),) * 2, np.uint8)) > 0
     out = frame_bgr.copy()
     out[mask] = (0, 0, 255)
     return out
 
 
 def apply_zebra(frame_bgr: np.ndarray, threshold: int = 245) -> np.ndarray:
     """Mark near-clipped luminance with diagonal black/white zebra stripes."""
     gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
     yy, xx = np.indices(gray.shape)
     hot = gray >= int(threshold)
     stripe = ((xx + yy) // 3) % 2 == 0
 
     out = frame_bgr.copy()
     out[hot & stripe] = (255, 255, 255)
     out[hot & ~stripe] = (0, 0, 0)
     return out
 
 
 def draw_crosshair(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
     cx, cy = width // 2, height // 2
     color = (255, 255, 255)
     draw.line((cx - 6, cy, cx - 2, cy), fill=color)
     draw.line((cx + 2, cy, cx + 6, cy), fill=color)
     draw.line((cx, cy - 6, cx, cy - 2), fill=color)
     draw.line((cx, cy + 2, cx, cy + 6), fill=color)
diff --git a/pi5_st7735_evf/ui/icons.py b/pi5_st7735_evf/ui/icons.py
new file mode 100644
index 0000000000000000000000000000000000000000..5a4231a45ac03227dc025a5b896329700fc1599a
--- /dev/null
+++ b/pi5_st7735_evf/ui/icons.py
@@ -0,0 +1,28 @@
+"""Dependency-free pixel/vector icons drawn with Pillow primitives."""
+from PIL import ImageDraw
+from .theme import WHITE, GREEN, RED, YELLOW
+
+def draw_icon(draw:ImageDraw.ImageDraw,name:str,box, color=WHITE):
+    x0,y0,x1,y1=map(int,box); w=x1-x0; h=y1-y0; m=max(1,w//6)
+    if name=="camera":
+        draw.rectangle((x0,y0+m,x1-m,y1-m),outline=color); draw.polygon(((x1-m,y0+2*m),(x1,y0+m),(x1,y1-m),(x1-m,y1-2*m)),outline=color)
+        draw.ellipse((x0+2*m,y0+2*m,x0+3*m,y0+3*m),fill=color)
+    elif name in ("display","disconnected"):
+        draw.rounded_rectangle((x0,y0,x1,y1-m),radius=2,outline=color,width=2); draw.line((x0+2*m,y1,x1-2*m,y1),fill=color,width=2)
+        if name=="disconnected": draw.line((x0-1,y1+1,x1+1,y0-2),fill=color,width=2)
+    elif name=="gear":
+        cx=(x0+x1)//2; cy=(y0+y1)//2; r=max(2,w//4); draw.ellipse((cx-r,cy-r,cx+r,cy+r),outline=color,width=2)
+        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)): draw.line((cx+dx*r,cy+dy*r,cx+dx*(r+3),cy+dy*(r+3)),fill=color,width=2)
+    elif name=="info":
+        draw.ellipse((x0,y0,x1,y1),fill=color); draw.text((x0+w//2,y0+h//2),"i",fill=(0,0,0),anchor="mm")
+    elif name=="warning":
+        draw.polygon(((x0+w//2,y0),(x1,y1),(x0,y1)),outline=RED); draw.line((x0+w//2,y0+4,x0+w//2,y1-5),fill=RED,width=2); draw.point((x0+w//2,y1-2),fill=RED)
+    elif name=="mode":
+        draw.arc((x0,y0,x1,y1),25,200,fill=YELLOW,width=3); draw.arc((x0,y0,x1,y1),205,380,fill=YELLOW,width=3)
+        draw.polygon(((x0,y0+h//2),(x0+5,y0+h//2-1),(x0+2,y0+h//2+4)),fill=YELLOW); draw.polygon(((x1,y0+h//2),(x1-5,y0+h//2+1),(x1-2,y0+h//2-4)),fill=YELLOW)
+    elif name=="power":
+        draw.arc((x0,y0+2,x1,y1),-45,225,fill=color,width=3); cx=(x0+x1)//2; draw.line((cx,y0,cx,y0+h//2),fill=color,width=3)
+    elif name=="battery":
+        draw.rectangle((x0,y0+2,x1-2,y1-2),outline=color); draw.rectangle((x1-1,y0+h//3,x1,y1-h//3),fill=color)
+    elif name=="signal":
+        draw.ellipse((x0+w//3,y0+h//3,x1-w//3,y1-h//3),fill=GREEN)
diff --git a/pi5_st7735_evf/ui/layout.py b/pi5_st7735_evf/ui/layout.py
new file mode 100644
index 0000000000000000000000000000000000000000..987a2052959d89bc985ab3b22a7039e65d85362a
--- /dev/null
+++ b/pi5_st7735_evf/ui/layout.py
@@ -0,0 +1,14 @@
+"""Integer-coordinate layout profile for the native 128x128 panel."""
+from dataclasses import dataclass
+
+@dataclass(frozen=True)
+class Layout:
+    width:int=128; height:int=128; margin:int=4; top_bar_height:int=16
+    bottom_bar_height:int=28; row_height:int=15; icon_size:int=14
+    corner_guide_length:int=8; menu_highlight_height:int=15
+    histogram_box:tuple[int,int,int,int]=(53,104,98,126)
+    @property
+    def viewport(self): return (0,self.top_bar_height,self.width-1,self.height-self.bottom_bar_height-1)
+
+def layout_for(width:int=128,height:int=128)->Layout:
+    return Layout(width=width,height=height)
diff --git a/pi5_st7735_evf/ui/screens.py b/pi5_st7735_evf/ui/screens.py
deleted file mode 100644
index ceb8ee056104a28b144ccdbdeff1e2bab82493ae..0000000000000000000000000000000000000000
--- a/pi5_st7735_evf/ui/screens.py
+++ /dev/null
@@ -1,3 +0,0 @@
-"""Screen composition exports."""
-from .status import no_signal_screen
-__all__ = ["no_signal_screen"]
diff --git a/pi5_st7735_evf/ui/screens/__init__.py b/pi5_st7735_evf/ui/screens/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..a392e8db3eda61e48943016e5a89d18ea23c501f
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/__init__.py
@@ -0,0 +1,11 @@
+"""Approved ST7735 screens and central name-based renderer."""
+from .status import *
+from .live_view import live_view_screen,sample_frame
+from .menu import menu_screen,focus_settings_screen,MENU_ITEMS
+from .system_info import system_info_screen
+
+SCREEN_NAMES=("boot","no-signal","source-present","live","focus-assist","menu","focus-settings","system-info","capture-error","mode-change","shutdown")
+def render_screen(name,width=128,height=128,**kwargs):
+    renderers={"boot":boot_screen,"no-signal":no_signal_screen,"source-present":source_present_screen,"live":live_view_screen,"focus-assist":lambda **kw:live_view_screen(focus=True,**kw),"menu":menu_screen,"focus-settings":focus_settings_screen,"system-info":system_info_screen,"capture-error":capture_error_screen,"mode-change":mode_change_screen,"shutdown":shutdown_screen}
+    try:return renderers[name](width=width,height=height,**kwargs)
+    except KeyError as exc:raise ValueError(f"Unknown screen: {name}") from exc
diff --git a/pi5_st7735_evf/ui/screens/common.py b/pi5_st7735_evf/ui/screens/common.py
new file mode 100644
index 0000000000000000000000000000000000000000..df15f515b9488f7396b93f8b1ef02357360a4b3e
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/common.py
@@ -0,0 +1,12 @@
+"""Screen drawing helpers."""
+from PIL import Image,ImageDraw
+from ..theme import BLACK,WHITE,FONT_SMALL,FONT_HEADER
+
+def canvas(width=128,height=128):
+    image=Image.new("RGB",(width,height),BLACK); return image,ImageDraw.Draw(image)
+def centered(draw,y,text,font=FONT_SMALL,fill=WHITE,width=128):
+    draw.text((width//2,y),text,font=font,fill=fill,anchor="ma")
+def header(draw,title,icon,draw_icon,width=128):
+    draw_icon(draw,icon,(5,3,17,15)); chosen=FONT_HEADER
+    if draw.textbbox((0,0),title,font=chosen)[2] > width-26: chosen=FONT_SMALL
+    draw.text((23,3),title,font=chosen,fill=WHITE); draw.line((0,18,width-1,18),fill=(65,68,70))
diff --git a/pi5_st7735_evf/ui/screens/live_view.py b/pi5_st7735_evf/ui/screens/live_view.py
new file mode 100644
index 0000000000000000000000000000000000000000..e66836faa8b357b020816cd638fe96cfa2535a43
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/live_view.py
@@ -0,0 +1,29 @@
+"""Native-resolution live view, analysis overlays, and camera HUD."""
+import cv2
+import numpy as np
+from PIL import Image,ImageDraw
+from ...render import resize_crop
+from ...overlays import apply_focus_peaking,apply_zebra
+from ..icons import draw_icon
+from ..layout import layout_for
+from ..theme import *
+
+def sample_frame(width=160,height=90):
+    yy,xx=np.indices((height,width)); frame=np.zeros((height,width,3),np.uint8)
+    frame[...,0]=(45+xx)%180; frame[...,1]=(35+yy*2)%170; frame[...,2]=75
+    cv2.circle(frame,(width//2,height//2),height//3,(185,195,210),-1); cv2.circle(frame,(width//2-12,height//2-4),5,(20,20,20),-1); cv2.circle(frame,(width//2+12,height//2-4),5,(20,20,20),-1); return frame
+def _histogram(d,frame,box):
+    x0,y0,x1,y1=box; d.rectangle(box,fill=BLACK,outline=DARK_GRAY); gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY); hist=cv2.calcHist([gray],[0],None,[22],[0,256]).ravel(); hist/=max(hist.max(),1)
+    pts=[(x0+i*2,y1-1-int(v*(y1-y0-2))) for i,v in enumerate(hist)]; d.line(pts,fill=WHITE,width=1)
+def live_view_screen(width=128,height=128,frame=None,focus=False,zebra=False,crosshair=True,fps=60.0,mode="1080p60",**_):
+    lay=layout_for(width,height); frame=sample_frame() if frame is None else frame; vh=height-lay.top_bar_height-lay.bottom_bar_height
+    view=resize_crop(frame,width,vh); view=apply_focus_peaking(view,80,thickness=1) if focus else view; view=apply_zebra(view,242) if zebra else view
+    im=Image.new("RGB",(width,height),BLACK); im.paste(Image.fromarray(cv2.cvtColor(view,cv2.COLOR_BGR2RGB)),(0,lay.top_bar_height)); d=ImageDraw.Draw(im)
+    d.rectangle((0,0,width-1,15),fill=BLACK); draw_icon(d,"camera",(4,4,16,13)); d.text((width//2,3),mode,font=FONT_SMALL,fill=WHITE,anchor="ma"); draw_icon(d,"signal",(96,4,106,14)); draw_icon(d,"battery",(112,3,123,14))
+    x0,y0,x1,y1=lay.viewport; n=lay.corner_guide_length
+    for a,b,c,e in ((4,y0+4,4+n,y0+4),(4,y0+4,4,y0+4+n),(width-5,y0+4,width-5-n,y0+4),(width-5,y0+4,width-5,y0+4+n),(4,y1-4,4+n,y1-4),(4,y1-4,4,y1-4-n),(width-5,y1-4,width-5-n,y1-4),(width-5,y1-4,width-5,y1-4-n)): d.line((a,b,c,e),fill=GREEN,width=2)
+    if crosshair:
+        cx=width//2; cy=(y0+y1)//2; d.line((cx-8,cy,cx-2,cy),fill=WHITE); d.line((cx+2,cy,cx+8,cy),fill=WHITE); d.line((cx,cy-8,cx,cy-2),fill=WHITE); d.line((cx,cy+2,cx,cy+8),fill=WHITE)
+    d.rectangle((0,100,width-1,height-1),fill=BLACK); d.text((4,102),"FPS",font=FONT_TINY,fill=GREEN); d.text((4,110),f"{fps:.0f}",font=FONT_HEADER,fill=GREEN)
+    if focus: d.text((31,109),"PEAK",font=FONT_SMALL,fill=RED)
+    _histogram(d,view,lay.histogram_box); d.text((102,103),"ISO",font=FONT_TINY,fill=WHITE); d.text((102,114),"ZEBRA",font=FONT_TINY,fill=WHITE); return im
diff --git a/pi5_st7735_evf/ui/screens/menu.py b/pi5_st7735_evf/ui/screens/menu.py
new file mode 100644
index 0000000000000000000000000000000000000000..df16027cda12858f690012b8a44019bf13a7a6ba
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/menu.py
@@ -0,0 +1,35 @@
+"""Full-screen menu and interactive focus-peaking detail."""
+import cv2
+from PIL import Image,ImageDraw
+from ...overlays import apply_focus_peaking
+from ...render import resize_crop
+from ..icons import draw_icon
+from ..theme import *
+from .common import canvas,header
+from .live_view import live_view_screen,sample_frame
+
+MENU_ITEMS=(("Focus Peaking","ON"),("Zebra","OFF"),("Crosshair","ON"),("Histogram","ON"),("Brightness","8"),("Display Rotation","0"),("System Info",">"))
+def _rows(d,items,selected,width,start=20,row_height=15):
+    visible=(128-start)//row_height; first=max(0,min(selected-len(items)+visible,selected))
+    for slot,(label,value) in enumerate(items[first:first+visible]):
+        idx=first+slot; y=start+slot*row_height
+        if idx==selected: d.rectangle((0,y,width-1,y+row_height-1),fill=BLUE); prefix="> "
+        else: prefix="  "
+        row_font=FONT_TINY if len(label)>15 else FONT_SMALL
+        d.text((3,y+2),prefix+label,font=row_font,fill=WHITE); d.text((width-5,y+2),value,font=FONT_SMALL,fill=WHITE,anchor="ra")
+def menu_screen(width=128,height=128,selected=0,**_):
+    selected=max(0,min(int(selected),len(MENU_ITEMS)-1)); im,d=canvas(width,height); header(d,"MENU","gear",draw_icon,width); _rows(d,MENU_ITEMS,selected,width); return im
+def focus_settings_screen(width=128,height=128,selected=0,enabled=True,color="Red",threshold=5,thickness=2,frame=None,**_):
+    selected=max(0,min(int(selected),3)); im,d=canvas(width,height); header(d,"FOCUS PEAKING","gear",draw_icon,width)
+    values=[("Enable","ON" if enabled else "OFF"),("Color",color),("Threshold",str(threshold)),("Thickness",str(thickness))]
+    for i,(label,value) in enumerate(values):
+        y=20+i*14
+        if i==selected:d.rectangle((0,y,width-1,y+13),fill=BLUE)
+        d.text((5,y+2),label,font=FONT_SMALL,fill=WHITE)
+        if i>=2:
+            d.rectangle((69,y+4,105,y+10),outline=GRAY); fill=int(35*max(0,min(10,int(value)))/10); d.rectangle((70,y+5,70+fill,y+9),fill=WHITE)
+        d.text((122,y+2),value,font=FONT_SMALL,fill=WHITE,anchor="ra")
+    preview_bgr=resize_crop(sample_frame() if frame is None else frame,120,32)
+    if enabled: preview_bgr=apply_focus_peaking(preview_bgr,max(20,int(threshold)*18),thickness=int(thickness))
+    preview=Image.fromarray(cv2.cvtColor(preview_bgr,cv2.COLOR_BGR2RGB))
+    im.paste(preview,(4,94)); d.rectangle((3,93,124,126),outline=GRAY); return im
diff --git a/pi5_st7735_evf/ui/screens/status.py b/pi5_st7735_evf/ui/screens/status.py
new file mode 100644
index 0000000000000000000000000000000000000000..7a7e09060392f59c1c7cb5608462d3364fa00542
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/status.py
@@ -0,0 +1,22 @@
+"""Boot, source-state, error, transition, and shutdown screens."""
+from ..icons import draw_icon
+from ..theme import *
+from .common import canvas,centered
+
+def boot_screen(width=128,height=128,**_):
+    im,d=canvas(width,height); centered(d,37,"EVF",FONT_LARGE,width=width); d.rectangle((91,47,97,53),fill=RED); d.line((14,75,width-15,75),fill=GRAY)
+    centered(d,84,"PI5 + X1301",FONT_BODY,width=width); centered(d,105,"v0.1.0",FONT_SMALL,GRAY,width); return im
+def no_signal_screen(width=128,height=128,**_):
+    im,d=canvas(width,height); draw_icon(d,"disconnected",(43,22,85,48)); centered(d,59,"NO SIGNAL",FONT_HEADER,width=width)
+    centered(d,79,"Camera may be off",FONT_SMALL,GRAY,width); centered(d,91,"or no HDMI output.",FONT_SMALL,GRAY,width); return im
+def source_present_screen(width=128,height=128,phase=0,**_):
+    im,d=canvas(width,height); draw_icon(d,"display",(45,23,83,47)); centered(d,59,"HDMI DETECTED",FONT_HEADER,width=width); centered(d,80,"Waiting for signal...",FONT_SMALL,WHITE,width)
+    for i,x in enumerate((52,64,76)): d.ellipse((x-3,104,x+3,110),fill=GREEN if i==phase%3 else DARK_GRAY)
+    return im
+def capture_error_screen(width=128,height=128,**_):
+    im,d=canvas(width,height); draw_icon(d,"warning",(43,20,85,58)); centered(d,70,"CAPTURE ERROR",FONT_HEADER,RED,width); centered(d,91,"Failed to read frames.",FONT_SMALL,WHITE,width); centered(d,103,"Will retry automatically.",FONT_TINY,WHITE,width); return im
+def mode_change_screen(width=128,height=128,phase=0,**_):
+    im,d=canvas(width,height); draw_icon(d,"mode",(43,18,85,60)); centered(d,70,"MODE CHANGE",FONT_HEADER,WHITE,width); centered(d,88,"Reconfiguring...",FONT_SMALL,WHITE,width)
+    d.rectangle((20,108,107,114),outline=GRAY); x=21+(phase%12)*5; d.rectangle((x,109,min(x+25,106),113),fill=YELLOW); return im
+def shutdown_screen(width=128,height=128,**_):
+    im,d=canvas(width,height); draw_icon(d,"power",(45,19,83,59)); centered(d,72,"SHUTTING DOWN",FONT_HEADER,WHITE,width); centered(d,94,"Goodbye!",FONT_SMALL,WHITE,width); return im
diff --git a/pi5_st7735_evf/ui/screens/system_info.py b/pi5_st7735_evf/ui/screens/system_info.py
new file mode 100644
index 0000000000000000000000000000000000000000..4c61e030a9ea988bc463f8d4bfe018b92ba116e9
--- /dev/null
+++ b/pi5_st7735_evf/ui/screens/system_info.py
@@ -0,0 +1,15 @@
+"""Scrollable dynamic X1301 and display diagnostics."""
+import time
+from ..icons import draw_icon
+from ..theme import *
+from .common import canvas,header
+
+def system_info_screen(width=128,height=128,runtime=None,scroll=0,uptime=None,**_):
+    def val(name,default="--"): return getattr(runtime,name,default) if runtime is not None else default
+    locked=getattr(val("signal_state"),"value",str(val("signal_state"))).replace("_"," ").title()
+    clock=float(val("pixel_clock_mhz",0) or 0)
+    rows=(("HDMI",locked),("Resolution",f'\''{val("width",1920)}x{val("height",1080)}'\''),("Frame Rate",f'\''{float(val("fps",60)):.2f}'\''),("Pixel Clock",f"{clock:.1f} MHz" if clock else "--"),("Video Node",val("video_node")),("Media Node",val("media_node")),("Driver",val("driver")),("RP1 CFE","Detected" if val("rp1_cfe_detected",False) else "--"),("Display",f"ST7735 {width}x{height}"),("Uptime",time.strftime("%H:%M:%S",time.gmtime(time.monotonic() if uptime is None else uptime))))
+    scroll=max(0,min(int(scroll),len(rows)-8)); im,d=canvas(width,height); header(d,"SYSTEM INFO","info",draw_icon,width)
+    for i,(k,v) in enumerate(rows[scroll:scroll+8]): y=21+i*13; d.text((4,y),k,font=FONT_TINY,fill=WHITE); d.text((64,y),str(v or "--")[:15],font=FONT_TINY,fill=WHITE)
+    if scroll<len(rows)-8:d.polygon(((122,121),(126,121),(124,125)),fill=GRAY)
+    return im
diff --git a/pi5_st7735_evf/ui/theme.py b/pi5_st7735_evf/ui/theme.py
new file mode 100644
index 0000000000000000000000000000000000000000..0c20caad2937035a3a2f97fbed5b2ba397d78cef
--- /dev/null
+++ b/pi5_st7735_evf/ui/theme.py
@@ -0,0 +1,19 @@
+"""Shared 128-pixel camera-monitor visual theme."""
+from functools import lru_cache
+from pathlib import Path
+from PIL import ImageFont
+
+BLACK=(0,0,0); WHITE=(245,245,245); GRAY=(105,110,114); DARK_GRAY=(38,42,44)
+GREEN=(25,225,91); YELLOW=(255,213,48); RED=(250,45,58); BLUE=(12,108,232)
+
+@lru_cache(maxsize=None)
+def font(size: int, bold: bool=False):
+    names = ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf") if bold else ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")
+    for name in names:
+        path=Path("/usr/share/fonts/truetype/dejavu")/name
+        if path.exists():
+            try: return ImageFont.truetype(str(path), size)
+            except OSError: pass
+    return ImageFont.load_default()
+
+FONT_TINY=font(7); FONT_SMALL=font(9); FONT_BODY=font(10); FONT_HEADER=font(11,True); FONT_LARGE=font(30,True)
diff --git a/pi5_st7735_evf/x1301/state.py b/pi5_st7735_evf/x1301/state.py
index d3946b606fa0c71e11a052f78719827d99e039f0..0dd343c3d12bca63a1e9720bb16216ec02c04dca 100644
--- a/pi5_st7735_evf/x1301/state.py
+++ b/pi5_st7735_evf/x1301/state.py
@@ -31,41 +31,47 @@ def _integer(value: object) -> int:
 
 
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
+    pixel_clock_mhz: float = 0.0
+    driver: str | None = None
+    rp1_cfe_detected: bool = False
 
     @property
     def ready(self) -> bool:
         return self.signal_state is SignalState.LOCKED and self.configured and bool(self.video_node)
 
     @classmethod
     def from_mapping(cls, data: Mapping[str, Any]) -> "X1301State":
         return cls(
             signal_state=SignalState.parse(_value(data, "signal_state", _value(data, "state"))),
             video_node=_value(data, "video_node", _value(data, "video")) or None,
             media_node=_value(data, "media_node", _value(data, "media")) or None,
             subdev_node=_value(data, "subdev_node", _value(data, "subdev")) or None,
             width=_integer(_value(data, "width")), height=_integer(_value(data, "height")),
             fps=_float(_value(data, "fps")), configured=_bool(_value(data, "configured")),
             error=_value(data, "error") or None,
+            pixel_clock_mhz=_float(_value(data, "pixel_clock_mhz", _value(data, "pixel_clock"))),
+            driver=_value(data, "driver") or None,
+            rp1_cfe_detected=_bool(_value(data, "rp1_cfe_detected", _value(data, "rp1_cfe"))),
         )
diff --git a/tests/test_integration.py b/tests/test_integration.py
index 592b964a3688ec245d98a82725c2c9c3176513ef..be494bca051d102d4c826fdbb76067141a89a1ca 100644
--- a/tests/test_integration.py
+++ b/tests/test_integration.py
@@ -1,75 +1,92 @@
 import json
 import subprocess
 import tempfile
 import unittest
 from pathlib import Path
 
 from PIL import Image
 
-from pi5_st7735_evf.application import ApplicationState, application_state
+from pi5_st7735_evf.application import ApplicationState, application_state, screen_for_state
 from pi5_st7735_evf.capture import CaptureController
 from pi5_st7735_evf.display import MockDisplayBackend
 from pi5_st7735_evf.input.controller import InputController
 from pi5_st7735_evf.input.events import InputEvent
 from pi5_st7735_evf.ui.menu import Action, Menu
 from pi5_st7735_evf.ui.status import no_signal_screen
+from pi5_st7735_evf.ui.screens import MENU_ITEMS, SCREEN_NAMES, render_screen
 from pi5_st7735_evf.x1301.client import X1301Client, parse_env
 from pi5_st7735_evf.x1301.state import SignalState, X1301State
 
 
 class FakeCapture:
     instances = []
     fail_read = False
     def __init__(self, *args): self.closed = False; self.args = args; self.instances.append(self)
     def open(self): pass
     def close(self): self.closed = True
     def read(self): return (False, None) if self.fail_read else (True, object())
 
 
 def state(signal=SignalState.LOCKED, width=1920):
     return X1301State(signal, "/dev/test-video", "/dev/test-media", "/dev/test-subdev",
                       width, 1080, 30, signal is SignalState.LOCKED)
 
 
 class IntegrationTests(unittest.TestCase):
     def setUp(self): FakeCapture.instances = []; FakeCapture.fail_read = False
 
     def test_env_parsing_and_state_file(self):
         parsed = parse_env('\''SIGNAL_STATE="LOCKED"\nVIDEO_NODE=/dev/video9 # comment\nWIDTH=1280\nHEIGHT=720\nFPS=30000/1001\nCONFIGURED=1\n'\'')
         self.assertEqual(parsed["VIDEO_NODE"], "/dev/video9")
         with tempfile.TemporaryDirectory() as tmp:
             path = Path(tmp) / "state.env"; path.write_text("\n".join(f"{k}={v}" for k, v in parsed.items()))
             current = X1301Client(str(path)).read()
         self.assertTrue(current.ready); self.assertAlmostEqual(current.fps, 29.97, places=2)
 
     def test_json_fallback(self):
         payload = {"signal_state": "locked", "video_node": "/dev/dynamic", "configured": True}
         runner = lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(payload), "")
         current = X1301Client("/missing", runner=runner).read()
         self.assertEqual(current.video_node, "/dev/dynamic")
 
     def test_application_and_no_signal(self):
         self.assertEqual(application_state(state(SignalState.DISCONNECTED)), ApplicationState.NO_SOURCE)
         self.assertEqual(application_state(state(SignalState.PRESENT_NO_SIGNAL)), ApplicationState.SOURCE_PRESENT)
         self.assertEqual(no_signal_screen(128, 128).size, (128, 128))
+        self.assertEqual(application_state(state(SignalState.MODE_CHANGE)), ApplicationState.MODE_CHANGE)
+        self.assertEqual(screen_for_state(ApplicationState.VIDEO_LOCKED), "mode-change")
+
+    def test_every_approved_screen_renders_at_native_size(self):
+        for name in SCREEN_NAMES:
+            with self.subTest(screen=name):
+                image = render_screen(name)
+                self.assertEqual(image.size, (128, 128))
+                self.assertEqual(image.mode, "RGB")
+
+    def test_menu_selection_is_clamped_and_focus_preview_updates(self):
+        self.assertEqual(render_screen("menu", selected=-50).size, (128, 128))
+        self.assertEqual(render_screen("menu", selected=len(MENU_ITEMS)+50).size, (128, 128))
+        low = render_screen("focus-settings", threshold=2, thickness=1)
+        high = render_screen("focus-settings", threshold=9, thickness=3)
+        self.assertNotEqual(low.tobytes(), high.tobytes())
 
     def test_capture_open_mode_change_reopen_and_failure(self):
         controller = CaptureController(factory=FakeCapture)
         self.assertTrue(controller.sync(state()))
         first = FakeCapture.instances[-1]
         self.assertFalse(controller.sync(state(SignalState.MODE_CHANGE)))
         self.assertTrue(first.closed)
         self.assertTrue(controller.sync(state(width=1280)))
         FakeCapture.fail_read = True
         self.assertEqual(controller.read(), (False, None)); self.assertFalse(controller.streaming)
 
     def test_display_input_and_menu(self):
         display = MockDisplayBackend(); display.open(); display.show(Image.new("RGB", (128, 128)))
         self.assertIsNotNone(display.last_frame)
         seen = []; controller = InputController(); controller.subscribe(seen.append)
         controller.dispatch(InputEvent.BUTTON_F1); self.assertEqual(seen, [InputEvent.BUTTON_F1])
         menu = Menu(("one", "two")); menu.dispatch(Action.MENU); menu.dispatch(Action.DOWN)
         self.assertEqual(menu.dispatch(Action.SELECT), "two")
 
 
 if __name__ == "__main__": unittest.main()
diff --git a/tools/render_ui_gallery.py b/tools/render_ui_gallery.py
new file mode 100644
index 0000000000000000000000000000000000000000..2b0821e07f81cf0230088c447b829bf9c7054443
--- /dev/null
+++ b/tools/render_ui_gallery.py
@@ -0,0 +1,25 @@
+#!/usr/bin/env python3
+"""Render approved UI PNGs. Example: python tools/render_ui_gallery.py --contact-sheet"""
+import argparse
+from pathlib import Path
+import sys
+from PIL import Image,ImageDraw
+
+sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
+from pi5_st7735_evf.ui.screens import SCREEN_NAMES,render_screen
+
+def main():
+    parser=argparse.ArgumentParser(); parser.add_argument("--output",default="artifacts/ui"); parser.add_argument("--contact-sheet",action="store_true"); args=parser.parse_args()
+    out=Path(args.output)
+    try: out.mkdir(parents=True,exist_ok=True)
+    except OSError as exc: print(f"cannot create {out}: {exc}",file=sys.stderr); return 1
+    images=[]
+    for name in SCREEN_NAMES:
+        image=render_screen(name); image.save(out/f"{name}.png"); images.append((name,image))
+    if args.contact_sheet:
+        sheet=Image.new("RGB",(4*256,3*280),(28,31,32)); draw=ImageDraw.Draw(sheet)
+        for i,(name,image) in enumerate(images):
+            x=(i%4)*256+64; y=(i//4)*280+20; sheet.paste(image.resize((256,256),Image.Resampling.NEAREST),(x-64,y)); draw.text((x,y+258),name,fill="white",anchor="ma")
+        sheet.save(out/"contact-sheet.png")
+    print(f"rendered {len(images)} screens in {out}"); return 0
+if __name__=="__main__": raise SystemExit(main())
' | git apply --3way)