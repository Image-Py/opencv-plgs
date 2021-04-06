from sciapp.action import dataio
from sciapp.action import Free, Simple
from imageio import imread, imsave
import cv2, wx, os
import numpy as np

class Writer(dataio.ImageWriter):
	title = 'Video Writer'
	filt = ['WMV', 'AVI', 'MOV']
	note = ['rgb', '8-bit']
	para = {'path':'','fps':10, 'down':1, 'fmt':'DIVX'}
	#para = {'path':'./','name':'','format':'png'}

	view = [(int, 'fps', (1,120), 0, 'frame', '/s'),
			(int, 'down', (1,10), 0, 'down sample', ''),
			(list, 'fmt', ['DIVX','MJPG','XVID','X264'], str, 'compress', 'fmt')]

	def show(self):
		if not dataio.ImageWriter.show(self): return
		return Simple.show(self)

	#process
	def run(self, ips, imgs, para = None):
		shp = imgs[0][::para['down'], ::para['down']].shape[:2]
		fmt =  cv2.VideoWriter_fourcc(*para['fmt'])
		writer = cv2.VideoWriter(para['path'], fmt, para['fps'], shp[::-1])
		for i in range(len(imgs)):
			self.progress(i, len(imgs))
			writer.write(imgs[i] if ips.channels==1 else imgs[i][:,:,::-1])
		writer.release()

class Reader(dataio.Reader):
	title = 'Video Reader'
	tag = 'img'
	filt = ['WMV', 'AVI', 'MOV']
	para = {'path':'', 'start':0, 'end':-1, 'step':1}

	def show(self):
		if not dataio.Reader.show(self): return
		videoCapture = cv2.VideoCapture(self.para['path'])
		nfs = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
		videoCapture.release()
		self.para['end'] = nfs-1
		self.view = [(int, 'start', (0, nfs-1), 0, 'start',  '0~{}'.format(nfs)),
					 (int, 'end', (0, nfs-1), 0, 'end',  '0~{}'.format(nfs)),
					 (int, 'step', (0, 100), 0, 'step',  '0~100')]
		return Free.show(self)

	#process
	def run(self, para = None):
		fp, fn = os.path.split(para['path'])
		fn, fe = os.path.splitext(fn)
		imgs = []
		videoCapture = cv2.VideoCapture(self.para['path'])
		fms = range(para['start'], para['end'], para['step'])
		videoCapture.set(cv2.CAP_PROP_POS_FRAMES, para['start'])
		for i in fms:
			if para['step']!=1: videoCapture.set(cv2.CAP_PROP_POS_FRAMES, i)
			imgs.append(videoCapture.read()[1][:,:,::-1])
			self.progress(i, para['end']-para['start'])
		videoCapture.release()
		self.app.show_img(imgs, fn)

plgs = [Reader, Writer]
