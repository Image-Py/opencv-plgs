# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.engine import Tool, Filter
import numpy as np
import wx, cv2

class Mark():
    def __init__(self):
        self.foreline, self.backline = [], []

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,0,0), width=2, style=wx.SOLID))
        for line in self.foreline: dc.DrawLines([f(*i) for i in line])
        dc.SetPen(wx.Pen((0,0,255), width=2, style=wx.SOLID))
        for line in self.backline: dc.DrawLines([f(*i) for i in line])

    def line(self, img, line, color):
        x0, y0 = line[0]
        for x, y in line[1:]:
            cv2.line(img, (int(x0), int(y0)), (int(x), int(y)), color, 2)
            x0, y0 = x, y

    def buildmsk(self, shape):
        img = np.zeros(shape[:2], dtype=np.uint8)
        img[:] = 3
        for line in self.foreline: self.line(img, line, 1)
        for line in self.backline: self.line(img, line, 0)
        return img

class GrabCut(Filter):
    title = 'Grab Cut'
    note = ['rgb', 'not_slice', 'auto_snap', 'not_channel']
    
    def run(self, ips, snap, img, para = None):
        msk = ips.mark.buildmsk(img.shape)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        msk, bgdModel, fgdModel = cv2.grabCut(snap, msk,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
        img[msk%2 == 0] //= 3


class Plugin(Tool):
    title = 'Grabcut'
    """FreeLinebuf class plugin with events callbacks"""
    def __init__(self):
        self.status = -1
            
    def mouse_down(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Mark):
            ips.mark = Mark()
        if btn==1 and not key['ctrl']:
            self.status = 1
            self.cur = [(x, y)]
            ips.mark.foreline.append(self.cur)
        if btn==1 and key['ctrl']:
            del ips.mark.foreline[:]
            del ips.mark.backline[:]
        if btn==3 and not key['ctrl']:
            self.status = 0
            self.cur = [(x, y)]
            ips.mark.backline.append(self.cur)
        if btn==3 and key['ctrl']:
            GrabCut().start()
        ips.update = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        if self.status==1 and len(self.cur)==1:
            ips.mark.foreline.remove(self.cur)
        if self.status==0 and len(self.cur)==1:
            ips.mark.backline.remove(self.cur)
        self.status = -1
        ips.update = True
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.status!=-1:
            self.cur.append((x, y))
            ips.update = True
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass