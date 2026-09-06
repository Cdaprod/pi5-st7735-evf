"""Boot, source-state, error, transition, and shutdown screens."""
from ..icons import draw_icon
from ..theme import *
from .common import canvas,centered

def boot_screen(width=128,height=128,**_):
    im,d=canvas(width,height); centered(d,37,"EVF",FONT_LARGE,width=width); d.rectangle((91,47,97,53),fill=RED); d.line((14,75,width-15,75),fill=GRAY)
    centered(d,84,"PI5 + X1301",FONT_BODY,width=width); centered(d,105,"v0.1.0",FONT_SMALL,GRAY,width); return im
def no_signal_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"disconnected",(43,22,85,48)); centered(d,59,"NO SIGNAL",FONT_HEADER,width=width)
    centered(d,79,"Camera may be off",FONT_SMALL,GRAY,width); centered(d,91,"or no HDMI output.",FONT_SMALL,GRAY,width); return im
def source_present_screen(width=128,height=128,phase=0,**_):
    im,d=canvas(width,height); draw_icon(d,"display",(45,23,83,47)); centered(d,59,"HDMI DETECTED",FONT_HEADER,width=width); centered(d,80,"Waiting for signal...",FONT_SMALL,WHITE,width)
    for i,x in enumerate((52,64,76)): d.ellipse((x-3,104,x+3,110),fill=GREEN if i==phase%3 else DARK_GRAY)
    return im
def capture_error_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"warning",(43,20,85,58)); centered(d,70,"CAPTURE ERROR",FONT_HEADER,RED,width); centered(d,91,"Failed to read frames.",FONT_SMALL,WHITE,width); centered(d,103,"Will retry automatically.",FONT_TINY,WHITE,width); return im
def mode_change_screen(width=128,height=128,phase=0,**_):
    im,d=canvas(width,height); draw_icon(d,"mode",(43,18,85,60)); centered(d,70,"MODE CHANGE",FONT_HEADER,WHITE,width); centered(d,88,"Reconfiguring...",FONT_SMALL,WHITE,width)
    d.rectangle((20,108,107,114),outline=GRAY); x=21+(phase%12)*5; d.rectangle((x,109,min(x+25,106),113),fill=YELLOW); return im
def shutdown_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"power",(45,19,83,59)); centered(d,72,"SHUTTING DOWN",FONT_HEADER,WHITE,width); centered(d,94,"Goodbye!",FONT_SMALL,WHITE,width); return im
