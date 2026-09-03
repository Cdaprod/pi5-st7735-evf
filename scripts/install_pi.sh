#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

sudo apt-get update
sudo apt-get install -y \
  git \
  python3 \
  python3-dev \
  python3-venv \
  python3-pip \
  python3-numpy \
  python3-pil \
  python3-opencv \
  python3-spidev \
  python3-lgpio \
  v4l-utils \
  media-ctl \
  build-essential

# Enable SPI if raspi-config exists.
if command -v raspi-config >/dev/null 2>&1; then
  sudo raspi-config nonint do_spi 0 || true
fi

python3 -m venv --system-site-packages .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install Adafruit-GPIO

mkdir -p vendor

if [[ ! -d vendor/Python_ST7735/.git ]]; then
  git clone https://github.com/cskau/Python_ST7735.git vendor/Python_ST7735
else
  git -C vendor/Python_ST7735 pull --ff-only
fi

python -m pip install -e vendor/Python_ST7735

echo
echo "Installed."
echo "Next:"
echo "  source .venv/bin/activate"
echo "  python tools/display_test.py"
echo "  ./tools/probe_capture.sh"
echo "  python evf.py --source /dev/video0 --mode fit"
