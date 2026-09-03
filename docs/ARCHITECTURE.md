# Architecture

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
Raspberry Pi 5 V4L2 node
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
PIL 128x128 composition
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

## Design goals

- Keep HDMI pass-through independent from EVF software.
- Make the capture node configurable.
- Make panel offsets configurable.
- Use full-frame display transfers before attempting partial-update optimization.
- Keep overlays optional because the panel has only 16,384 pixels.
- Prefer center-crop for framing confidence and fit mode for complete composition.
- Treat focus peaking and zebra as convenience aids, not calibrated exposure/focus instruments.
