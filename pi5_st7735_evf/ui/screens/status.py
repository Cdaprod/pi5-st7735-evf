"""Boot, source-state, error, transition, and shutdown screens."""
from ..context import RenderContext
from ..icons import draw_icon
from ..scenes import render_boot, render_source_present
from ..theme import *
from .common import canvas,centered

def boot_screen(width=128,height=128,**_):
    return render_boot(RenderContext.from_kwargs(width, height, **_))
def no_signal_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"disconnected",(43,22,85,48)); centered(d,59,"NO SIGNAL",FONT_HEADER,width=width)
    centered(d,79,"Camera may be off",FONT_SMALL,GRAY,width); centered(d,91,"or no HDMI output.",FONT_SMALL,GRAY,width); return im
def source_present_screen(width=128,height=128,phase=0,**_):
    return render_source_present(RenderContext.from_kwargs(width, height, phase=phase, **_))
def capture_error_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"warning",(43,20,85,58)); centered(d,70,"CAPTURE ERROR",FONT_HEADER,RED,width); centered(d,91,"Failed to read frames.",FONT_SMALL,WHITE,width); centered(d,103,"Will retry automatically.",FONT_TINY,WHITE,width); return im
def mode_change_screen(width=128,height=128,phase=0,**_):
    im,d=canvas(width,height); draw_icon(d,"mode",(43,18,85,60)); centered(d,70,"MODE CHANGE",FONT_HEADER,WHITE,width); centered(d,88,"Reconfiguring...",FONT_SMALL,WHITE,width)
    d.rectangle((20,108,107,114),outline=GRAY); x=21+(phase%12)*5; d.rectangle((x,109,min(x+25,106),113),fill=YELLOW); return im
def shutdown_screen(width=128,height=128,**_):
    im,d=canvas(width,height); draw_icon(d,"power",(45,19,83,59)); centered(d,72,"SHUTTING DOWN",FONT_HEADER,WHITE,width); centered(d,94,"Goodbye!",FONT_SMALL,WHITE,width); return im
