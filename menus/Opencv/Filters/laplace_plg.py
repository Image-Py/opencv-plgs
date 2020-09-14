# -*- coding: utf-8 -*
import cv2
from sciapp.action import Filter

class Plugin(Filter):
    title = 'Laplacian'
    note = ['all', 'auto_msk', 'auto_snap']
    
    def run(self, ips, snap, img, para = None):
        return cv2.Laplacian(img, -1)
