#!/usr/bin/env python3
"""Write a development X1301 state fixture.

Example: python tools/mock_x1301_state.py --state locked --width 1920 --height 1080 --video /dev/video0
"""
import argparse
from pathlib import Path
import sys
import tempfile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", choices=("disconnected", "present-no-signal", "locked", "mode-change", "error"), required=True)
    parser.add_argument("--width", type=int, default=0); parser.add_argument("--height", type=int, default=0)
    parser.add_argument("--fps", type=float, default=30); parser.add_argument("--video", default="")
    parser.add_argument("--output", type=Path, default=Path(tempfile.gettempdir()) / "x1301-state.env")
    args = parser.parse_args()
    configured = args.state == "locked" and bool(args.video)
    mode_id = f"{args.width}x{args.height}@{args.fps}/0Hz/RGB3" if configured else ""
    content = ("X1301_STATUS_SCHEMA=1\n"
               f"X1301_SIGNAL_STATE={args.state.upper().replace('-', '_')}\n"
               f"X1301_VIDEO={args.video}\nX1301_WIDTH={args.width}\n"
               f"X1301_HEIGHT={args.height}\nX1301_FPS={args.fps}\n"
               f"X1301_CONFIGURED={int(configured)}\nX1301_PIXELFORMAT=RGB3\n"
               f"X1301_MODE_ID='{mode_id}'\nX1301_MODE_GENERATION={int(configured)}\n")
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(content)
        print(args.output); return 0
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
