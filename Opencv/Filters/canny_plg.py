# -*- coding: utf-8 -*
import cv2
from imagepy.core.engine import Filter

class Plugin(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':2, 'low':10, 'high':20}
    view = [(float, (0,10), 1,  'sigma', 'sigma', 'pix'),
            ('slide',(0,255), 'low_threshold', 'low',''),
            ('slide',(0,255), 'high_threshold', 'high','')]

    def run(self, ips, snap, img, para = None):
    	l = int(para['sigma']*2.5)*2+1
    	cv2.GaussianBlur(snap, (l, l), para['sigma'], dst=img)
    	return cv2.Canny(img, para['low'], para['high'])