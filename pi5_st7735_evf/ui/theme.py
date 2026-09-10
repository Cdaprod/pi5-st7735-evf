"""Shared 128-pixel camera-monitor visual theme."""
from functools import lru_cache
from pathlib import Path
from PIL import ImageFont

BLACK=(0,0,0); WHITE=(245,245,245); GRAY=(105,110,114); DARK_GRAY=(38,42,44)
GREEN=(25,225,91); YELLOW=(255,213,48); RED=(250,45,58); BLUE=(12,108,232)

# Semantic names used by scene/widget renderers.  Keep the legacy constants above
# for screens that have not migrated yet.
BACKGROUND = BLACK
FOREGROUND = WHITE
MUTED = GRAY
PANEL = DARK_GRAY
ACCENT = (55, 169, 238)
SUCCESS = GREEN
WARNING = YELLOW
ERROR = RED
SPACING = 4
LINE_WIDTH = 1

@lru_cache(maxsize=None)
def font(size: int, bold: bool=False):
    names = ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf") if bold else ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")
    for name in names:
        path=Path("/usr/share/fonts/truetype/dejavu")/name
        if path.exists():
            try: return ImageFont.truetype(str(path), size)
            except OSError: pass
    return ImageFont.load_default()

FONT_TINY=font(7); FONT_SMALL=font(9); FONT_BODY=font(10); FONT_HEADER=font(11,True); FONT_LARGE=font(30,True)
