"""Integer-coordinate layout profile for the native 128x128 panel."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Layout:
    width:int=128; height:int=128; margin:int=4; top_bar_height:int=16
    bottom_bar_height:int=28; row_height:int=15; icon_size:int=14
    corner_guide_length:int=8; menu_highlight_height:int=15
    histogram_box:tuple[int,int,int,int]=(53,104,98,126)
    @property
    def viewport(self): return (0,self.top_bar_height,self.width-1,self.height-self.bottom_bar_height-1)

def layout_for(width:int=128,height:int=128)->Layout:
    return Layout(width=width,height=height)
