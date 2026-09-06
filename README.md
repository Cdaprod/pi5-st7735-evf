# Pi 5 ST7735 HDMI/CSI-2 EVF

A repository-ready Raspberry Pi 5 electronic viewfinder (EVF) prototype that:

1. Captures an HDMI source exposed to Linux through an HDMI-to-CSI-2 capture board such as the Geekworm X1301 / TC358743 path.
2. Reads the capture device through V4L2/OpenCV.
3. Scales or center-crops the incoming video for a 1.44-inch 128×128 ST7735 SPI TFT.
4. Draws configurable EVF overlays.
5. Pushes each composed PIL frame through the `cskau/Python_ST7735` driver.

The code intentionally keeps the display output path independent from the capture board's HDMI pass-through.

## Target hardware

- Raspberry Pi 5
- HDMI -> CSI-2 capture board / X1301-style TC358743 capture path
- ST7735 1.44-inch 128×128 SPI TFT
- Raspberry Pi OS Bookworm or newer
- Nikon Z7 or any compatible HDMI source

## ST7735 wiring

Default BCM pin assignments:

| TFT pin | Raspberry Pi 5 |
|---|---|
| GND | GND |
| VCC | 3.3 V |
| SCL / SCK | GPIO11 / SPI0 SCLK, physical pin 23 |
| SDA / MOSI | GPIO10 / SPI0 MOSI, physical pin 19 |
| RES / RST | GPIO25, physical pin 22 |
| DC | GPIO24, physical pin 18 |
| CS | GPIO8 / SPI0 CE0, physical pin 24 |
| BL | 3.3 V for always-on backlight |

The project defaults to SPI bus `0`, device `0`, DC `24`, and RST `25`.

## Why this repository uses a GPIO shim on Pi 5

`cskau/Python_ST7735` follows the older Adafruit GPIO API. The driver accepts a custom GPIO object, so this project supplies an `lgpio`-backed compatibility shim by default. That keeps the upstream ST7735 drawing/display API while avoiding direct dependence on legacy `RPi.GPIO` behavior for the display control pins.

The SPI transport still uses `Adafruit_GPIO.SPI.SpiDev`, matching the upstream examples.

## Quick start

```bash
git clone https://github.com/Cdaprod/pi5-st7735-evf.git
cd pi5-st7735-evf

sudo ./scripts/install_pi.sh
source .venv/bin/activate

python evf.py
```

The EVF starts before an HDMI source is present. The X1301 watcher supplies the
current node, timing, format, and generation, and the EVF automatically closes
and reopens capture across connects, disconnects, source replacement, and mode
changes. Development requires no Pi:

```bash
python evf.py --mock --mock-signal locked --preview-window
python evf.py --mock --mock-signal disconnected --preview-window
python tools/mock_x1301_state.py --state locked --width 1920 --height 1080 --video /dev/video0
python -m unittest discover -s tests -v
```

Render the approved screens and exact-size inspection gallery without hardware:

```bash
python evf.py --mock --screen boot
python evf.py --mock --screen no-signal
python evf.py --mock --screen source-present
python evf.py --mock --screen live
python evf.py --mock --screen focus-assist
python evf.py --mock --screen menu
python evf.py --mock --screen focus-settings
python evf.py --mock --screen system-info
python evf.py --mock --screen capture-error
python evf.py --mock --screen mode-change
python evf.py --mock --screen shutdown
python tools/render_ui_gallery.py --contact-sheet
```

PNGs are written under `artifacts/ui/`. Launch on the configured Raspberry Pi
with `source .venv/bin/activate && python evf.py`.

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

## Capture test

Normal production operation does not use `EVF_SOURCE` or `--source`. It reads
the producer's atomically published `/run/x1301/state.env`, falling back first
to `/usr/local/lib/x1301/runtime-status.sh --json` (cached watcher state) and
then `/usr/local/lib/x1301/hdmi-status.sh --json` (direct diagnostics). Only
`LOCKED` with `configured=true` and a nonempty video node is capture-ready.

The producer states map to the approved screens: `DISCONNECTED` to no-signal,
`PRESENT_NO_SIGNAL` to source-present, `MODE_CHANGE` to mode-change, and
`ERROR` or a locked capture failure to capture-error. Failed capture opens and
reads are retried without restarting the EVF.

The required producer contract is maintained by
[`pi5-x1301-bringup`](https://github.com/Cdaprod/pi5-x1301-bringup/tree/codex/implement-hdmi-hot-plug-lifecycle).
Its environment uses `X1301_`-prefixed fields and its JSON uses corresponding
lower-case names except `X1301_STATUS_SCHEMA`. Device nodes are discoveries,
not stable identifiers.

`--source` is retained only as an explicit diagnostic node override. It never
promotes an unconfigured producer state to capture-ready:

Find a diagnostic video node:

```bash
v4l2-ctl --list-devices
v4l2-ctl --device /dev/video0 --all
v4l2-ctl --device /dev/video0 --list-formats-ext
```

Then run:

```bash
python evf.py \
  --source /dev/video0 \
  --capture-width 1920 \
  --capture-height 1080 \
  --capture-fps 30 \
  --mode fit \
  --spi-hz 16000000
```

### Center-cropped EVF mode

Uses the full 128×128 panel:

```bash
python evf.py --source /dev/video0 --mode crop
```

### Letterboxed telemetry mode

Keeps the full 16:9 image and leaves room for overlays:

```bash
python evf.py --source /dev/video0 --mode fit \
  --overlay rec,fps,resolution,clock,crosshair
```

### Focus peaking

```bash
python evf.py --source /dev/video0 --mode crop \
  --overlay rec,fps,crosshair,peaking
```

### Zebra exposure warning

```bash
python evf.py --source /dev/video0 --overlay rec,zebra
```

## Useful controls

While the EVF has terminal focus:

- `q` or `Esc` — quit
- `m` — toggle crop / fit mode
- `o` — toggle overlay visibility
- `p` — toggle focus peaking
- `z` — toggle zebra warning
- `g` — toggle rule-of-thirds grid
- `c` — toggle center crosshair
- `h` — toggle mini histogram

## Performance notes

A 128×128 RGB565 frame is only 32 KiB, but the upstream driver converts each PIL frame to RGB565 and writes through Python. The effective frame rate therefore depends on:

- SPI clock
- wiring quality
- Python / NumPy conversion overhead
- capture pixel format and conversion cost
- enabled overlays
- HDMI capture format

Start at 8–16 MHz SPI. Raise it only after the display is stable.

The upstream driver defaults to a 4 MHz SPI clock internally. `pi5_st7735_evf/display.py` updates the module's `SPI_CLOCK_HZ` before constructing the display so the requested `--spi-hz` value is actually used.

## 128×128 panel offsets

Many 1.44-inch ST7735 modules use a controller RAM area larger than the visible glass and require x/y offsets. The correct offsets are panel-specific.

Defaults are `0,0`.

Try common small values:

```bash
python tools/display_test.py --x-offset 2 --y-offset 1
python tools/display_test.py --x-offset 2 --y-offset 3
python tools/display_test.py --x-offset 0 --y-offset 2
```

Once the exact module is confirmed, put the values in `config/evf.env`.

## Configuration file

Copy:

```bash
cp config/evf.env.example config/evf.env
```

Then:

```bash
set -a
source config/evf.env
set +a
python evf.py
```

CLI arguments override environment variables.

## Systemd

After the display and capture are stable:

```bash
sudo cp systemd/pi5-st7735-evf.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now pi5-st7735-evf.service
journalctl -u pi5-st7735-evf.service -f
```

Do not enable the unit until hardware validation is complete. To run it without
making HDMI presence a startup dependency:

```bash
sudo systemctl start x1301-edid.service
sudo systemctl start x1301-hdmi-watch.service
sudo systemctl start pi5-st7735-evf.service
```

Edit the service first if the repository is not located at `/home/pi/pi5-st7735-evf`.

## Repository structure

```text
pi5-st7735-evf/
├── evf.py
├── pi5_st7735_evf/
│   ├── capture.py
│   ├── config.py
│   ├── display.py
│   ├── gpio_lgpio.py
│   ├── overlays.py
│   └── render.py
├── tools/
│   ├── display_test.py
│   └── probe_capture.sh
├── scripts/
│   └── install_pi.sh
├── systemd/
│   └── pi5-st7735-evf.service
├── config/
│   └── evf.env.example
├── requirements.txt
├── Makefile
├── LICENSE
└── .gitignore
```

## Current design boundary

This is the first real EVF implementation:

```text
HDMI source
    |
    v
HDMI -> CSI-2 capture
    |
    v
V4L2 capture node
    |
    v
OpenCV frame
    |
    +--> scale/crop
    +--> peaking/zebra
    +--> PIL overlays
    |
    v
128x128 RGB image
    |
    v
cskau/Python_ST7735
    |
    v
SPI -> ST7735 EVF
```

The capture board's HDMI pass-through remains separate from this software-rendered EVF path.

## Roadmap

- [x] V4L2/OpenCV capture abstraction
- [x] 128×128 crop/fit rendering
- [x] REC / FPS / source-resolution / clock overlays
- [x] crosshair / thirds overlays
- [x] simple focus peaking
- [x] zebra exposure warning
- [x] mini luminance histogram
- [x] Pi temperature display
- [x] Pi 5 `lgpio` compatibility shim
- [ ] derive camera metadata from Nikon HDMI / USB/PTP where available
- [ ] hardware buttons / rotary encoder
- [ ] brightness PWM
- [ ] capture-device reconnect watchdog
- [ ] optimized direct RGB565 framebuffer path
- [ ] service watchdog + boot splash
- [ ] optional recording-state integration

## License

MIT. See `LICENSE`.

`cskau/Python_ST7735` is an external MIT-licensed dependency and is not vendored in this archive.
