# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from sciapp.action import ImageTool, Filter
from sciapp.util.shputil import draw_shp, mark2shp
from sciapp.object import Layers, Layer, Line
import numpy as np
import wx, cv2

class GrabCut(Filter):
    title = 'Grab Cut'
    note = ['rgb', 'not_slice', 'auto_snap', 'not_channel']

    def __init__(self, fore, back):
        self.fore, self.back = fore, back
    
    def run(self, ips, snap, img, para = None):
        mark = np.zeros(ips.shape, dtype=np.uint8)
        draw_shp(self.fore.to_geom(), mark, 2, 2)
        draw_shp(self.back.to_geom(), mark, 1, 2)
        mark[mark==0] = 4; mark -= 1
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        msk, bgdModel, fgdModel = cv2.grabCut(snap, mark, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
        img[msk%2 == 0] //= 3

class Plugin(ImageTool):
    title = 'Grabcut'
    """FreeLinebuf class plugin with events callbacks"""
    def __init__(self):
        self.status = -1
            
    def mouse_down(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Layer) or not len(ips.mark.body)==2:
            ips.mark = Layer([Layer(color=(255,0,0)), Layer(color=(0,0,255))])
        if btn in {1,3}:
            self.status = btn
            self.obj = Line([(x,y)])
            ips.mark.body[btn==1].body.append(self.obj)
    
    def mouse_up(self, ips, x, y, btn, **key):
        if self.status in {1,3} and len(self.obj.body)==1:
            ips.mark.body[btn==1].body.remove(self.obj)
            if self.status == 1: ips.mark = None
            else: GrabCut(* ips.mark.body).start(self.app)

        self.status = -1
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.status!=-1:
            self.obj.body = np.vstack((self.obj.body, [(x,y)]))
            ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass