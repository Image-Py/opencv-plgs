from imagepy.core.util import fileio
from imagepy.core.engine import Free, Simple
from imagepy import IPy
from scipy.misc import imread, imsave
from imagepy.core.manager import ReaderManager, WriterManager
import cv2, wx, os
import numpy as np

class Writer(Simple):
	title = 'Video Writer'
	note = ['rgb', '8-bit']
	para = {'path':'','fps':24, 'down':1}
	#para = {'path':'./','name':'','format':'png'}

	view = [(int, (1,120), 0, 'frame', 'fps', '/s'),
			(int, (1,10), 0, 'down sample', 'down', '')]

	def show(self):
		self.para['name'] = self.ips.title
		rst = IPy.get_para('Save Video', self.view, self.para)
		if rst!=wx.ID_OK:return rst
		return IPy.getpath('Save Video', '%s files (*.%s)|*.%s'%('WMV','wmv','wmv'), 'save', self.para)

	#process
	def run(self, ips, imgs, para = None):
		path = para['path']+'/'+para['name']
		shp = imgs[0][::para['down'], ::para['down']].shape[:2]
		print(para['path'], cv2.VideoWriter_fourcc(*'MJPG'), para['fps'], shp[::-1])
		writer = cv2.VideoWriter(para['path'], cv2.VideoWriter_fourcc(*'MJPG'), para['fps'], shp[::-1])
		for i in range(len(imgs)):
			self.progress(i, len(imgs))
			buf = ips.lookup(imgs[i][::para['down'], ::para['down']])
			writer.write(buf[:,:,::-1])
		writer.release()

class Reader(Free):
	title = 'Video Reader'
	para = {'path':'', 'start':0, 'end':0, 'gray':False, 'title':'sequence'}

	def show(self):
		filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in (
			'wmv', 'avi', 'mov')])
		rst = IPy.getpath('Import Video', filt, 'open', self.para)
		if rst!=wx.ID_OK:return rst

		videoCapture = cv2.VideoCapture(self.para['path'])
		nfs = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
		videoCapture.release()
		self.para['end'] = nfs-1
		self.view = [(str, 'Title','title',''), 
					 (int, (0, nfs-1), 0, 'Start', 'start', '0~{}'.format(nfs)),
					 (int, (0, nfs-1), 0, 'End', 'end', '0~{}'.format(nfs)),
					 (bool, 'convert to gray', 'gray')]
		return IPy.get_para('Import sequence', self.view, self.para)

	#process
	def run(self, para = None):
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn)
		imgs = []
		videoCapture = cv2.VideoCapture(self.para['path'])
		videoCapture.set(cv2.CAP_PROP_POS_FRAMES, para['start'])
		for i in range(para['end']-para['start']):
			img = videoCapture.read()[1][:,:,::-1]
			if para['gray']:img = img[:,:,0].copy()
			imgs.append(img)
			self.progress(i, para['end']-para['start'])
		videoCapture.release()
		IPy.show_img(imgs, para['title'])

		print(fn, fe)

plgs = [Reader, Writer]
