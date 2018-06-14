# -*- coding: utf-8 -*-
from imagepy import IPy
import numpy as np, cv2
from imagepy.core.engine import Filter
        
class Plugin(Filter):
    title = 'Adaptive Threshold'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    para = {'max':255, 'med':'mean', 'size':9, 'offset':2, 'inv':False}
    view = [(int, 'max', (0, 255), 0, 'maxvalue', ''),
            (list, 'med', ['mean', 'gauss'], str, 'method', ''),
            (int, 'size', (3, 31), 0, 'blocksize', 'pix'),
            (int, 'offset', (0, 50), 0, 'offset', ''),
            (bool , 'inv', 'binary invert')]
    
    #process
    def run(self, ips, snap, img, para = None):
        med = cv2.ADAPTIVE_THRESH_MEAN_C if para['med']=='mean' else cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        mtype = cv2.THRESH_BINARY_INV if para['inv'] else cv2.THRESH_BINARY
        cv2.adaptiveThreshold(snap, para['max'], med, para['inv'], para['size'], para['offset'], dst=img)