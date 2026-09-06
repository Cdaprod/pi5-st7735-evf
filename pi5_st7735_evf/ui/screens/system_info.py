"""Scrollable dynamic X1301 and display diagnostics."""
import time
from ..icons import draw_icon
from ..theme import *
from .common import canvas,header

def system_info_screen(width=128,height=128,runtime=None,scroll=0,uptime=None,**_):
    def val(name,default="--"): return getattr(runtime,name,default) if runtime is not None else default
    locked=getattr(val("signal_state"),"value",str(val("signal_state"))).replace("_"," ").title()
    clock=float(val("pixel_clock_mhz",0) or 0)
    rows=(("HDMI",locked),("Resolution",f'{val("width",1920)}x{val("height",1080)}'),("Frame Rate",f'{float(val("fps",60)):.2f}'),("Pixel Clock",f"{clock:.1f} MHz" if clock else "--"),("Video Node",val("video_node")),("Media Node",val("media_node")),("Driver",val("driver")),("RP1 CFE","Detected" if val("rp1_cfe_detected",False) else "--"),("Display",f"ST7735 {width}x{height}"),("Uptime",time.strftime("%H:%M:%S",time.gmtime(time.monotonic() if uptime is None else uptime))))
    scroll=max(0,min(int(scroll),len(rows)-8)); im,d=canvas(width,height); header(d,"SYSTEM INFO","info",draw_icon,width)
    for i,(k,v) in enumerate(rows[scroll:scroll+8]): y=21+i*13; d.text((4,y),k,font=FONT_TINY,fill=WHITE); d.text((64,y),str(v or "--")[:15],font=FONT_TINY,fill=WHITE)
    if scroll<len(rows)-8:d.polygon(((122,121),(126,121),(124,125)),fill=GRAY)
    return im
