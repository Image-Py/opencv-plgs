from sciapp.action import Simple
import numpy as np 
import cv2
import pandas as pd
from sciapp.object import mark2shp
# from imagepy.core.mark import GeometryMark

class Meanshift(Simple):
    """FillHoles: derived from imagepy.core.engine.Filter """
    title = 'Meanshift'
    note = ['rgb', 'req_roi']

    def run(self, ips, imgs, para = None):
        sc, sr = ips.rect
        c,r,w,h=sr.start, sc.start, sr.stop-sr.start, sc.stop-sc.start
        roi = imgs[0][r:r+h, c:c+w].copy()
        track_window = (c,r,w,h)
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0], mask, [180], [0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        n=len(imgs)
        locs, mark = [], {'type':'layers', 'body':{}}
        for i in range(n):
            prgs=(i,n)
            frame=imgs[i].copy()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180], 1)
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)
            x,y,w,h = track_window
            locs.append([x,y,w,h])
            layer = {'type':'layer', 'body':[]}
            layer['body'].append({'type':'rectangle', 'body':(x, y, w, h)})
            mark['body'][i] = layer

        ips.mark = mark2shp(mark)
        self.app.show_table(pd.DataFrame(locs, columns= ['X','Y','W','H']), ips.title+'-region')
        
class Camshift(Simple):
    """FillHoles: derived from imagepy.core.engine.Filter """
    title = 'Camshift'
    note = ['rgb', 'req_roi']

    def run(self, ips, imgs, para = None):
        sc, sr = ips.rect
        c,r,w,h=sr.start,sc.start,sr.stop-sr.start,sc.stop-sc.start
        roi = imgs[0][r:r+h, c:c+w].copy()
        track_window = (c,r,w,h)
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        n=len(imgs)
        locs = []
        locs,mark = [], {'type':'layers', 'body':{}}

        for i in range(n):
            prgs=(i,n)
            frame=imgs[i].copy()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, track_window = cv2.CamShift(dst, track_window, term_crit)
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)

            layer = {'type':'layer', 'body':[]}
            temp=[tuple(i) for i in pts]
            layer['body'].append({'type':'line', 'body':[(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1]),(pts[2][0],pts[2][1]),(pts[3][0],pts[3][1])]})
            layer['body'].append({'type':'line', 'body':[(pts[0][0],pts[0][1]),(pts[3][0],pts[3][1])]})
            mark['body'][i] = layer
            locs.append([pts[0][0],pts[0][1],pts[1][0],pts[1][1],pts[2][0],pts[2][1],pts[3][0],pts[3][1]])

        ips.mark = mark2shp(mark)
        self.app.show_table(pd.DataFrame(locs, columns=  ['P1_X','P1_y','P2_X','P2_y','P3_X','P3_y','P4_X','P4_y',]), ips.title+'-region')

plgs = [Camshift, Meanshift]