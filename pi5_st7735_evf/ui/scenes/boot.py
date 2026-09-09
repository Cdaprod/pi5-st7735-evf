"""Loopable, deterministic power-on scene."""
from PIL import Image, ImageDraw
from ..context import RenderContext
from ..theme import ACCENT, FOREGROUND, MUTED
from ..widgets import FrameCorners, Label, ProgressDots, Spinner
from .common import finish, scene_canvas


def render_boot(context: RenderContext) -> Image.Image:
    image=scene_canvas(context.width,context.height); overlay=Image.new("RGBA",image.size,(0,0,0,0)); draw=ImageDraw.Draw(overlay)
    FrameCorners(length=7).draw(draw,(9,9,context.width-10,context.height-10))
    Spinner(radius=13).draw(draw,(context.width//2,42),context.phase)
    Label("CDA",12,FOREGROUND,True).draw(draw,(context.width//2-2,39),anchor="rm")
    Label("PROD",7,ACCENT,True).draw(draw,(context.width//2+1,40),anchor="lm")
    Label("EVF",11,FOREGROUND,True).draw(draw,(context.width//2,68),anchor="mm")
    Label("INITIALIZING",7,MUTED).draw(draw,(context.width//2,84),anchor="mm")
    ProgressDots().draw(draw,(context.width//2,103),context.phase)
    return finish(Image.alpha_composite(image,overlay))
