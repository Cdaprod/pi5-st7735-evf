"""Full-screen menu and interactive focus-peaking detail."""
import cv2
from PIL import Image,ImageDraw
from ...overlays import apply_focus_peaking
from ...render import resize_crop
from ..icons import draw_icon
from ..theme import *
from .common import canvas,header
from .live_view import live_view_screen,sample_frame

MENU_ITEMS=(("Focus Peaking","ON"),("Zebra","OFF"),("Crosshair","ON"),("Histogram","ON"),("Brightness","8"),("Display Rotation","0"),("System Info",">"))
def _rows(d,items,selected,width,start=20,row_height=15):
    visible=(128-start)//row_height; first=max(0,min(selected-len(items)+visible,selected))
    for slot,(label,value) in enumerate(items[first:first+visible]):
        idx=first+slot; y=start+slot*row_height
        if idx==selected: d.rectangle((0,y,width-1,y+row_height-1),fill=BLUE); prefix="> "
        else: prefix="  "
        row_font=FONT_TINY if len(label)>15 else FONT_SMALL
        d.text((3,y+2),prefix+label,font=row_font,fill=WHITE); d.text((width-5,y+2),value,font=FONT_SMALL,fill=WHITE,anchor="ra")
def menu_screen(width=128,height=128,selected=0,items=MENU_ITEMS,**_):
    selected=max(0,min(int(selected),len(items)-1)); im,d=canvas(width,height); header(d,"MENU","gear",draw_icon,width); _rows(d,items,selected,width); return im
def focus_settings_screen(width=128,height=128,selected=0,enabled=True,color="Red",threshold=5,thickness=2,frame=None,**_):
    selected=max(0,min(int(selected),3)); im,d=canvas(width,height); header(d,"FOCUS PEAKING","gear",draw_icon,width)
    values=[("Enable","ON" if enabled else "OFF"),("Color",color),("Threshold",str(threshold)),("Thickness",str(thickness))]
    for i,(label,value) in enumerate(values):
        y=20+i*14
        if i==selected:d.rectangle((0,y,width-1,y+13),fill=BLUE)
        d.text((5,y+2),label,font=FONT_SMALL,fill=WHITE)
        if i>=2:
            d.rectangle((69,y+4,105,y+10),outline=GRAY); fill=int(35*max(0,min(10,int(value)))/10); d.rectangle((70,y+5,70+fill,y+9),fill=WHITE)
        d.text((122,y+2),value,font=FONT_SMALL,fill=WHITE,anchor="ra")
    preview_bgr=resize_crop(sample_frame() if frame is None else frame,120,32)
    if enabled: preview_bgr=apply_focus_peaking(preview_bgr,max(20,int(threshold)*18),thickness=int(thickness))
    preview=Image.fromarray(cv2.cvtColor(preview_bgr,cv2.COLOR_BGR2RGB))
    im.paste(preview,(4,94)); d.rectangle((3,93,124,126),outline=GRAY); return im
