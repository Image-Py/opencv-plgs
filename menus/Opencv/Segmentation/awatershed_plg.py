# -*- coding: utf-8 -*
from sciapp.action import Filter
import numpy as np, cv2
from sciapp.object import image

class Plugin(Filter):
    title = 'Active Watershed'
    note = ['rgb', 'req_roi', 'not_slice', 'auto_snap']

    def run(self, ips, snap, img, para=None):
        a, msk = cv2.connectedComponents(ips.mask('in').astype(np.uint8))
        msk = cv2.watershed(ips.img, msk) == -1
        ips.img //= 2
        ips.img[msk] = 255
