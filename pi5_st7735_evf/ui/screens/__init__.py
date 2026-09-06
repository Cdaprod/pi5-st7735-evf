"""Approved ST7735 screens and central name-based renderer."""
from .status import *
from .live_view import live_view_screen,sample_frame
from .menu import menu_screen,focus_settings_screen,MENU_ITEMS
from .system_info import system_info_screen

SCREEN_NAMES=("boot","no-signal","source-present","live","focus-assist","menu","focus-settings","system-info","capture-error","mode-change","shutdown")
def render_screen(name,width=128,height=128,**kwargs):
    renderers={"boot":boot_screen,"no-signal":no_signal_screen,"source-present":source_present_screen,"live":live_view_screen,"focus-assist":lambda **kw:live_view_screen(focus=True,**kw),"menu":menu_screen,"focus-settings":focus_settings_screen,"system-info":system_info_screen,"capture-error":capture_error_screen,"mode-change":mode_change_screen,"shutdown":shutdown_screen}
    try:return renderers[name](width=width,height=height,**kwargs)
    except KeyError as exc:raise ValueError(f"Unknown screen: {name}") from exc
