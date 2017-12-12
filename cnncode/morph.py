import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

folder = 'BSD500CNN_out'
for image in listdir(folder):
	# print(image)
	img = cv2.imread(folder + '/'+image, 0)
	cv2.imshow('sample', img)
	kernel = np.ones((4,4), np.uint8)
	erosion = cv2.erode(img, kernel, iterations = 1)
	image_name = image.split('.')[0]
	# print(image_name)
	cv2.imwrite('%s_morph.jpg' % str(image_name), erosion)
	# cv2.waitKey(0)