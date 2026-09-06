"""Screen drawing helpers."""
from PIL import Image,ImageDraw
from ..theme import BLACK,WHITE,FONT_SMALL,FONT_HEADER

def canvas(width=128,height=128):
    image=Image.new("RGB",(width,height),BLACK); return image,ImageDraw.Draw(image)
def centered(draw,y,text,font=FONT_SMALL,fill=WHITE,width=128):
    draw.text((width//2,y),text,font=font,fill=fill,anchor="ma")
def header(draw,title,icon,draw_icon,width=128):
    draw_icon(draw,icon,(5,3,17,15)); chosen=FONT_HEADER
    if draw.textbbox((0,0),title,font=chosen)[2] > width-26: chosen=FONT_SMALL
    draw.text((23,3),title,font=chosen,fill=WHITE); draw.line((0,18,width-1,18),fill=(65,68,70))
