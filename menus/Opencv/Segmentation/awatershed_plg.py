# -*- coding: utf-8 -*
from sciapp.action import Filter
import numpy as np, cv2

class Plugin(Filter):
	title = 'Active Watershed'
	note = ['rgb', 'req_roi', 'not_channel', 'auto_snap']
	
	def run(self, ips, snap, img, para = None):
		a, msk = cv2.connectedComponents(ips.mask().astype(np.uint8))
		msk = cv2.watershed(img, msk)==-1
		img //= 2
		img[msk//2] = 255