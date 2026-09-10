"""Runtime-authoritative HDMI-present/waiting scene."""
from PIL import Image, ImageDraw
from ..context import RenderContext
from ..theme import ACCENT, FOREGROUND, SUCCESS, WARNING
from ..widgets import Divider, Label, ProgressDots, StatusDot, ValueLabel
from .common import finish, scene_canvas


def _flag(runtime, name: str) -> bool:
    return bool(getattr(runtime, name, False)) if runtime is not None else False


def render_source_present(context: RenderContext) -> Image.Image:
    image=scene_canvas(context.width,context.height); draw=ImageDraw.Draw(image)
    power=_flag(context.runtime,"power_present"); locked=_flag(context.runtime,"timings_locked")
    configured=_flag(context.runtime,"configured")
    StatusDot(power,SUCCESS).draw(draw,(12,12)); Label("HDMI DETECTED",9,FOREGROUND,True).draw(draw,(20,8))
    Divider(ACCENT).draw(draw,22,context.width,8)
    Label("WAITING FOR SIGNAL",9,WARNING,True).draw(draw,(context.width//2,36),anchor="mm")
    ProgressDots().draw(draw,(context.width//2,53),context.phase)
    rows=(("POWER","PRESENT" if power else "UNKNOWN"),
          ("TIMINGS","LOCKED" if locked else "SEARCHING"),
          ("CONFIG","READY" if configured else "PENDING"))
    for i,(label,value) in enumerate(rows): ValueLabel(label,value).draw(draw,70+i*12,context.width)
    runtime=context.runtime
    if runtime is not None and getattr(runtime,"width",0) and getattr(runtime,"height",0):
        mode=f"{runtime.width}x{runtime.height}"
        if getattr(runtime,"fps",0): mode += f"  {runtime.fps:g} FPS"
        Label(mode,7,ACCENT).draw(draw,(context.width//2,114),anchor="mm")
    return finish(image)
