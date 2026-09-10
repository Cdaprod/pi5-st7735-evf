#!/usr/bin/env python3
"""Render hardware-free scene previews. Example: python tools/render_ui_preview.py --scene boot"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pi5_st7735_evf.navigation import MENU_ITEMS
from pi5_st7735_evf.ui.screens import render_screen
from pi5_st7735_evf.x1301 import SignalState, X1301State

OUTPUT = Path("artifacts/ui-preview")


def frames(scene: str):
    if scene == "boot":
        return [(f"phase-{p}", render_screen("boot", phase=p)) for p in range(8)]
    if scene == "source-present":
        states = (("power", X1301State(SignalState.PRESENT_NO_SIGNAL, power_present=True)),
                  ("locked", X1301State(SignalState.PRESENT_NO_SIGNAL, width=1920, height=1080,
                                        fps=59.94, power_present=True, timings_locked=True)),
                  ("configured", X1301State(SignalState.PRESENT_NO_SIGNAL, width=1280, height=720,
                                            fps=30, configured=True, power_present=True, timings_locked=True)))
        return [(name, render_screen(scene, runtime=runtime, phase=i)) for i,(name,runtime) in enumerate(states)]
    items = tuple((name, "ON" if i % 2 else "OFF") for i,name in enumerate(MENU_ITEMS))
    return [(f"selection-{i}", render_screen("menu", items=items, selected=i)) for i in range(len(items))]


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--scene", choices=("boot","source-present","menu"), required=True)
    try:
        selected=parser.parse_args().scene; rendered=frames(selected); OUTPUT.mkdir(parents=True,exist_ok=True)
        for name,image in rendered: image.save(OUTPUT/f"{selected}-{name}.png")
        sheet=Image.new("RGB",(len(rendered)*128,148),(18,18,18)); draw=ImageDraw.Draw(sheet)
        for i,(name,image) in enumerate(rendered): sheet.paste(image,(i*128,0)); draw.text((i*128+3,132),name,fill=(220,220,220))
        path=OUTPUT/f"{selected}-contact-sheet.png"; sheet.save(path); print(path); return 0
    except (OSError, ValueError) as exc:
        print(f"preview failed: {exc}",file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
