"""Dependency-free pixel/vector icons drawn with Pillow primitives."""
from PIL import ImageDraw
from .theme import WHITE, GREEN, RED, YELLOW

def draw_icon(draw:ImageDraw.ImageDraw,name:str,box, color=WHITE):
    x0,y0,x1,y1=map(int,box); w=x1-x0; h=y1-y0; m=max(1,w//6)
    if name=="camera":
        draw.rectangle((x0,y0+m,x1-m,y1-m),outline=color); draw.polygon(((x1-m,y0+2*m),(x1,y0+m),(x1,y1-m),(x1-m,y1-2*m)),outline=color)
        draw.ellipse((x0+2*m,y0+2*m,x0+3*m,y0+3*m),fill=color)
    elif name in ("display","disconnected"):
        draw.rounded_rectangle((x0,y0,x1,y1-m),radius=2,outline=color,width=2); draw.line((x0+2*m,y1,x1-2*m,y1),fill=color,width=2)
        if name=="disconnected": draw.line((x0-1,y1+1,x1+1,y0-2),fill=color,width=2)
    elif name=="gear":
        cx=(x0+x1)//2; cy=(y0+y1)//2; r=max(2,w//4); draw.ellipse((cx-r,cy-r,cx+r,cy+r),outline=color,width=2)
        for dx,dy in ((0,-1),(1,0),(0,1),(-1,0)): draw.line((cx+dx*r,cy+dy*r,cx+dx*(r+3),cy+dy*(r+3)),fill=color,width=2)
    elif name=="info":
        draw.ellipse((x0,y0,x1,y1),fill=color); draw.text((x0+w//2,y0+h//2),"i",fill=(0,0,0),anchor="mm")
    elif name=="warning":
        draw.polygon(((x0+w//2,y0),(x1,y1),(x0,y1)),outline=RED); draw.line((x0+w//2,y0+4,x0+w//2,y1-5),fill=RED,width=2); draw.point((x0+w//2,y1-2),fill=RED)
    elif name=="mode":
        draw.arc((x0,y0,x1,y1),25,200,fill=YELLOW,width=3); draw.arc((x0,y0,x1,y1),205,380,fill=YELLOW,width=3)
        draw.polygon(((x0,y0+h//2),(x0+5,y0+h//2-1),(x0+2,y0+h//2+4)),fill=YELLOW); draw.polygon(((x1,y0+h//2),(x1-5,y0+h//2+1),(x1-2,y0+h//2-4)),fill=YELLOW)
    elif name=="power":
        draw.arc((x0,y0+2,x1,y1),-45,225,fill=color,width=3); cx=(x0+x1)//2; draw.line((cx,y0,cx,y0+h//2),fill=color,width=3)
    elif name=="battery":
        draw.rectangle((x0,y0+2,x1-2,y1-2),outline=color); draw.rectangle((x1-1,y0+h//3,x1,y1-h//3),fill=color)
    elif name=="signal":
        draw.ellipse((x0+w//3,y0+h//3,x1-w//3,y1-h//3),fill=GREEN)
