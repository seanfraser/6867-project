import numpy as np
import cv2
import sys
import scipy.misc
import os
from PIL import Image

def pre_process_by_L0(img_dir, img_name):

    eng = matlab.engine.start_matlab()

    Im = eng.imread(img_dir + img_name)

    new_img = (np.asarray(eng.L0Smoothing(Im,0.01))*255).astype(np.uint8)

    #im = Image.fromarray(new_img)

    eng.quit()

    return new_img

def main():

    seeds = None
    display_mode = 0

    num_superpixels = 400
    num_iterations = 10

    prior = 2
    num_levels = 4
    num_histogram_bins = 5

    img_dir = '../Documents/6.867Project/BSR/bench/benchmarks/'
    for filename in os.listdir(img_dir+'Im'):
        if filename.endswith(".jpg"):
            print img_dir +'Im/'+filename
            img = cv2.imread(img_dir +'Im/'+filename)

            #new_img = pre_process_by_L0(img_dir,img_name)

            converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            height,width,channels = converted_img.shape
            seeds = cv2.ximgproc.createSuperpixelSEEDS(width, height, channels,
                    num_superpixels, num_levels, prior, num_histogram_bins)
            color_img = np.zeros((height,width,3), np.uint8)
            color_img[:] = (0, 0, 255)

            seeds.iterate(converted_img, num_iterations)

            # retrieve the segmentation result
            labels = seeds.getLabels()
            img1 = Image.open(img_dir+'inm2/'+filename[:-3]+'png')
            A=np.array(img1)
            B=labels
            pix={}
            dim = A.shape
            C=np.zeros((dim[0],dim[1]))
            for i in xrange(dim[0]):
                for j in xrange(dim[1]):
                    k=B[i,j]
                    if k in pix:
                        pix[k]=pix[k]+((i,j),)
                    else:
                        pix[k]=((i,j),)
            for k in pix:
                count={}
                for (i,j) in pix[k]:
                    seg=A[i,j]
                    if seg in count:
                        count[seg]+=1
                    else:
                        count[seg]=1
                major=max(count.values())
                res=[m for m, v in count.iteritems() if v == major]
                for (a,b) in pix[k]:
                    C[a,b]=res[0]
            scipy.misc.toimage(C, cmin=0.0, cmax=float(np.amax(C))).save('../Documents/6.867Project/BSR/bench/benchmarks/inm3/'+filename[:-3]+'png')

if __name__ == '__main__':
    main()
