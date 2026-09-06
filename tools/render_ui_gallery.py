#!/usr/bin/env python3
"""Render approved UI PNGs. Example: python tools/render_ui_gallery.py --contact-sheet"""
import argparse
from pathlib import Path
import sys
from PIL import Image,ImageDraw

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pi5_st7735_evf.ui.screens import SCREEN_NAMES,render_screen

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",default="artifacts/ui"); parser.add_argument("--contact-sheet",action="store_true"); args=parser.parse_args()
    out=Path(args.output)
    try: out.mkdir(parents=True,exist_ok=True)
    except OSError as exc: print(f"cannot create {out}: {exc}",file=sys.stderr); return 1
    images=[]
    for name in SCREEN_NAMES:
        image=render_screen(name); image.save(out/f"{name}.png"); images.append((name,image))
    if args.contact_sheet:
        sheet=Image.new("RGB",(4*256,3*280),(28,31,32)); draw=ImageDraw.Draw(sheet)
        for i,(name,image) in enumerate(images):
            x=(i%4)*256+64; y=(i//4)*280+20; sheet.paste(image.resize((256,256),Image.Resampling.NEAREST),(x-64,y)); draw.text((x,y+258),name,fill="white",anchor="ma")
        sheet.save(out/"contact-sheet.png")
    print(f"rendered {len(images)} screens in {out}"); return 0
if __name__=="__main__": raise SystemExit(main())
