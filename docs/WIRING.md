# Wiring

## Default ST7735 -> Pi 5 wiring

```text
ST7735       Raspberry Pi 5
-------      -----------------------------
GND       -> GND
VCC       -> 3V3
SCL/SCK   -> GPIO11 / SPI0_SCLK / pin 23
SDA/MOSI  -> GPIO10 / SPI0_MOSI / pin 19
RES/RST   -> GPIO25 / pin 22
DC        -> GPIO24 / pin 18
CS        -> GPIO8 / SPI0_CE0 / pin 24
BL        -> 3V3
```

The display is write-only in this project; MISO is not required.

## SPI device

With SPI enabled, verify:

```bash
ls -l /dev/spidev*
```

Expected default:

```text
/dev/spidev0.0
```

## Capture

The HDMI-to-CSI-2 board is not accessed over SPI. Its captured frames should appear through the Linux media/V4L2 subsystem.

Probe with:

```bash
./tools/probe_capture.sh
```
