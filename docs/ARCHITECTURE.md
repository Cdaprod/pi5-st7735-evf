# Architecture

## Ownership and runtime boundary

`pi5-x1301-bringup` owns TC358743/RP1 CFE discovery, EDID, signal and DV timing
detection, media graph configuration, readiness, and its watcher. It publishes
`/run/x1301/state.env`; `hdmi-status.sh --json` is the fallback. This repository
never imports bring-up code and does not discover or hard-code device nodes.

The production lifecycle is `x1301-edid.service` (load once), then
`x1301-hdmi-watch.service` (watch/configure), then `pi5-st7735-evf.service`.
The EVF wants and starts after the watcher, but source absence never prevents the
display and UI from starting.

## Video path

```text
Nikon / HDMI source
        |
        v
X1301 / HDMI-to-CSI-2 capture
        |
        +---- HDMI pass-through ----> full-size clean monitor
        |
        v
TC358743 / CSI-2
        |
        v
RP1 CFE and X1301 runtime state/watch service
        |
        v
runtime-provided /dev/video* node
        |
        v
OpenCV
        |
        +---- rotation
        +---- fit or center-crop
        +---- focus peaking
        +---- zebra
        |
        v
PIL display-resolution composition
        |
        +---- REC
        +---- FPS
        +---- resolution
        +---- timestamp
        +---- Pi temp
        +---- crosshair
        +---- thirds
        +---- histogram
        |
        v
cskau/Python_ST7735
        |
        v
RGB565 conversion
        |
        v
SPI0
        |
        v
1.44-inch 128x128 ST7735 EVF
```

The render layers are base video, focus peaking, zebra, guides, histogram,
camera/status HUD, menu, then error/status. Capture resolution is independent
of backend resolution. ST7735 is the prototype backend; a future 2.8-inch DSI
display can use a higher-resolution, 60 Hz compositor backend without changing
capture or UI logic. ST7789, DSI, and HDMI backends can implement the same
`DisplayBackend` contract.

## Design goals

- Keep HDMI pass-through independent from EVF software.
- Make the capture node configurable.
- Make panel offsets configurable.
- Use full-frame display transfers before attempting partial-update optimization.
- Keep overlays optional because the panel has only 16,384 pixels.
- Prefer center-crop for framing confidence and fit mode for complete composition.
- Treat focus peaking and zebra as convenience aids, not calibrated exposure/focus instruments.
