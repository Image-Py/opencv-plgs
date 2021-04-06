from sciapp.action import Filter
import numpy as np 
import cv2

class Plugin(Filter):
	title = 'K-Mean'
	note = ['rgb','2float', 'not_channel','auto_msk', 'auto_snap','preview']
	para = {'nclusters':8,'criteria':'EPS+ITER','max_iter':300,'epsilon':1.0,'flags':'RANDOM'}
	view = [(int, 'nclusters', (0,99999), 0,  'nclusters', ''),
		(int, 'max_iter', (0,99999), 0,  'max_iter', ''),
		(float, 'epsilon', (0,99999), 1,  'epsilon', ''),	
		(list, 'criteria', ['EPS','ITER','EPS+ITER'], str, 'criteria', ''),
		(list, 'flags', ['RANDOM','PP'], str, 'flags', '')]

	def run(self, ips, snap, img, para = None):
		criteria_dic={'EPS':cv2.TERM_CRITERIA_EPS,'ITER':cv2.TERM_CRITERIA_MAX_ITER,'EPS+ITER':cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER}
		flags_dic={'RANDOM':cv2.KMEANS_RANDOM_CENTERS,'PP':cv2.KMEANS_PP_CENTERS}
		Z = snap.reshape((-1,3))
		criteria = (criteria_dic[para['criteria']], para['max_iter'], para['epsilon'])
		K = para['nclusters']
		ret,label,center=cv2.kmeans(Z,K,None,criteria,10,flags_dic[para['flags']])
		center = np.uint8(center)
		res = center[label.flatten()]
		img[:,:,:] = res.reshape((img.shape))