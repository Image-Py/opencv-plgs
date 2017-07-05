# -*- coding: utf-8 -*
from imagepy.core.engine import Filter
import numpy as np, cv2

class Plugin(Filter):
	title = 'Active Watershed'
	note = ['rgb', 'not_slice', 'auto_snap']
	
	def run(self, ips, snap, img, para = None):
		a, msk = cv2.connectedComponents(ips.get_msk().astype(np.uint8))
		msk = cv2.watershed(img, msk)==-1
		img //= 2
		img[msk] = 255