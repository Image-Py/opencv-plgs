# -*- coding: utf-8 -*
import cv2
from imagepy.core.engine import Filter

class Plugin(Filter):
    title = 'Canny'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'sigma':2, 'low':10, 'high':20}
    view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix'),
            ('slide', 'low', (0,255), 0, 'low_threshold'),
            ('slide', 'high', (0,255), 0, 'high_threshold')]

    def run(self, ips, snap, img, para = None):
        l = int(para['sigma']*2.5)*2+1
        print(snap.shape, img.shape)
        img[:] = cv2.GaussianBlur(snap, (l, l), para['sigma'])
        return cv2.Canny(img, para['low'], para['high'])
