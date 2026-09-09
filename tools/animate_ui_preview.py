#!/usr/bin/env python3
"""Write sequential boot PNGs. Example: python tools/animate_ui_preview.py --frames 16"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pi5_st7735_evf.ui.screens import render_screen


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--frames",type=int,default=16); args=parser.parse_args()
    if args.frames < 1:
        parser.error("--frames must be positive")
    try:
        output=Path("artifacts/ui-preview/boot-animation"); output.mkdir(parents=True,exist_ok=True)
        for phase in range(args.frames): render_screen("boot",phase=phase).save(output/f"frame-{phase:03d}.png")
        print(output); return 0
    except OSError as exc:
        print(f"animation preview failed: {exc}",file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
