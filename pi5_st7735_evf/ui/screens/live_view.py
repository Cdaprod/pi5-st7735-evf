"""Native-resolution live view, analysis overlays, and camera HUD."""
import cv2
import numpy as np
from PIL import Image,ImageDraw
from ...render import resize_crop
from ...overlays import apply_focus_peaking,apply_zebra
from ..icons import draw_icon
from ..layout import layout_for
from ..theme import *

def sample_frame(width=160,height=90):
    yy,xx=np.indices((height,width)); frame=np.zeros((height,width,3),np.uint8)
    frame[...,0]=(45+xx)%180; frame[...,1]=(35+yy*2)%170; frame[...,2]=75
    cv2.circle(frame,(width//2,height//2),height//3,(185,195,210),-1); cv2.circle(frame,(width//2-12,height//2-4),5,(20,20,20),-1); cv2.circle(frame,(width//2+12,height//2-4),5,(20,20,20),-1); return frame
def _histogram(d,frame,box):
    x0,y0,x1,y1=box; d.rectangle(box,fill=BLACK,outline=DARK_GRAY); gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY); hist=cv2.calcHist([gray],[0],None,[22],[0,256]).ravel(); hist/=max(hist.max(),1)
    pts=[(x0+i*2,y1-1-int(v*(y1-y0-2))) for i,v in enumerate(hist)]; d.line(pts,fill=WHITE,width=1)
def live_view_screen(width=128,height=128,frame=None,focus=False,zebra=False,crosshair=True,fps=60.0,mode="1080p60",**_):
    lay=layout_for(width,height); frame=sample_frame() if frame is None else frame; vh=height-lay.top_bar_height-lay.bottom_bar_height
    view=resize_crop(frame,width,vh); view=apply_focus_peaking(view,80,thickness=1) if focus else view; view=apply_zebra(view,242) if zebra else view
    im=Image.new("RGB",(width,height),BLACK); im.paste(Image.fromarray(cv2.cvtColor(view,cv2.COLOR_BGR2RGB)),(0,lay.top_bar_height)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,width-1,15),fill=BLACK); draw_icon(d,"camera",(4,4,16,13)); d.text((width//2,3),mode,font=FONT_SMALL,fill=WHITE,anchor="ma"); draw_icon(d,"signal",(96,4,106,14)); draw_icon(d,"battery",(112,3,123,14))
    x0,y0,x1,y1=lay.viewport; n=lay.corner_guide_length
    for a,b,c,e in ((4,y0+4,4+n,y0+4),(4,y0+4,4,y0+4+n),(width-5,y0+4,width-5-n,y0+4),(width-5,y0+4,width-5,y0+4+n),(4,y1-4,4+n,y1-4),(4,y1-4,4,y1-4-n),(width-5,y1-4,width-5-n,y1-4),(width-5,y1-4,width-5,y1-4-n)): d.line((a,b,c,e),fill=GREEN,width=2)
    if crosshair:
        cx=width//2; cy=(y0+y1)//2; d.line((cx-8,cy,cx-2,cy),fill=WHITE); d.line((cx+2,cy,cx+8,cy),fill=WHITE); d.line((cx,cy-8,cx,cy-2),fill=WHITE); d.line((cx,cy+2,cx,cy+8),fill=WHITE)
    d.rectangle((0,100,width-1,height-1),fill=BLACK); d.text((4,102),"FPS",font=FONT_TINY,fill=GREEN); d.text((4,110),f"{fps:.0f}",font=FONT_HEADER,fill=GREEN)
    if focus: d.text((31,109),"PEAK",font=FONT_SMALL,fill=RED)
    _histogram(d,view,lay.histogram_box); d.text((102,103),"ISO",font=FONT_TINY,fill=WHITE); d.text((102,114),"ZEBRA",font=FONT_TINY,fill=WHITE); return im
