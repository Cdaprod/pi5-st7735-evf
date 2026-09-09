"""Selectable menu scene consuming, but never owning, navigation state."""
from PIL import Image, ImageDraw
from ..context import RenderContext
from ..theme import ACCENT, FOREGROUND
from ..widgets import Divider, Label, MenuRow
from .common import finish, scene_canvas


def render_menu(context: RenderContext, items, selected: int = 0) -> Image.Image:
    normalized=[(str(item[0]),str(item[1]) if len(item)>1 else "") for item in items]
    selected=max(0,min(int(selected),len(normalized)-1)) if normalized else 0
    image=scene_canvas(context.width,context.height); draw=ImageDraw.Draw(image)
    Label("EVF MENU",10,FOREGROUND,True).draw(draw,(8,7)); Label(f"{selected+1}/{len(normalized)}",7,ACCENT).draw(draw,(context.width-8,9),anchor="ra")
    Divider(ACCENT).draw(draw,20,context.width,7)
    row_height=13; visible=max(1,(context.height-24)//row_height)
    first=max(0,min(selected-visible+1,len(normalized)-visible))
    for slot,(label,value) in enumerate(normalized[first:first+visible]):
        y=24+slot*row_height; MenuRow(label,value,first+slot==selected).draw(draw,(3,y,context.width-4,y+11))
    return finish(image)
