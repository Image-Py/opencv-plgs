from imagepy.core.engine import Filter
from imagepy import IPy
import numpy as np 
import cv2
class K_mean(Filter):
	"""FillHoles: derived from imagepy.core.engine.Filter """
	title = 'K-Mean'
	note = ['rgb','2float', 'not_channel','auto_msk', 'auto_snap','preview']
	para = {'nclusters':8,'criteria':cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,'max_iter':300,'epsilon':1.0,'flags':cv2.KMEANS_RANDOM_CENTERS}
	view = [(int, 'nclusters', (0,99999), 0,  'nclusters', ''),
	(int, 'max_iter', (0,99999), 0,  'max_iter', ''),
	(float, 'epsilon', (0,99999), 1,  'epsilon', ''),	
	(list, 'criteria', [cv2.TERM_CRITERIA_EPS,cv2.TERM_CRITERIA_MAX_ITER,cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER], int, 'criteria', ''),
	(list, 'flags', [cv2.KMEANS_RANDOM_CENTERS,cv2.KMEANS_PP_CENTERS], int, 'flags', '')]
	def run(self, ips, snap, img, para = None):
		Z = snap.reshape((-1,3))
		# convert to np.float32
		# Z = np.float32(Z)
		# define criteria, number of clusters(K) and apply kmeans()
		criteria = (para['criteria'], para['max_iter'], para['epsilon'])
		K = para['nclusters']
		ret,label,center=cv2.kmeans(Z,K,None,criteria,10,para['flags'])
		# Now convert back into uint8, and make original image
		center = np.uint8(center)
		res = center[label.flatten()]
		img[:,:,:] = res.reshape((img.shape))

plgs = [K_mean]