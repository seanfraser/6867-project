import numpy as np
import cv2
import sys
import matlab.engine

from matplotlib import pyplot as plt
import scipy.misc
from PIL import Image
import os

def pre_process_by_L0(img_dir, img_name):

    eng = matlab.engine.start_matlab()

    Im = eng.imread(img_dir + img_name)

    new_img = (np.asarray(eng.L0Smoothing(Im,0.01))*255).astype(np.uint8)

    #im = Image.fromarray(new_img)

    eng.quit()

    return new_img

def get_average_superpixels(superpixel_dict,img,labels,output_dir,filename):
    average_dict = {}
    for key in superpixel_dict:
        average_dict[key] = np.round(np.average(np.asarray([img[x,y] for (x,y) in superpixel_dict[key]]),axis = 0))

    output_img = np.zeros(img.shape, dtype=np.uint8)
    for x in xrange(output_img.shape[0]):
        for y in xrange(output_img.shape[1]):
            output_img[x,y] = average_dict[labels[x,y]]

    # plt.imshow(img, interpolation='nearest')
    # plt.show()

    output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

    scipy.misc.imsave(output_dir + filename[:-4] + '.png', output_img)
    print 'saved: ', filename[:-4] + '.png' 

def display_superpixels(labels,seeds,img,color_img,display_mode):

    # labels output: use the last x bits to determine the color
    num_label_bits = 2
    labels &= (1<<num_label_bits)-1
    labels *= 1<<(16-num_label_bits)


    mask = seeds.getLabelContourMask(False)

    # stitch foreground & background together
    mask_inv = cv2.bitwise_not(mask)
    result_bg = cv2.bitwise_and(img, img, mask=mask_inv)
    result_fg = cv2.bitwise_and(color_img, color_img, mask=mask)
    result = cv2.add(result_bg, result_fg)

    if display_mode == 0:
        cv2.imshow('SEEDS', result)
    elif display_mode == 1:
        cv2.imshow('SEEDS', mask)
    else:
        cv2.imshow('SEEDS', labels)

    ch = cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():

    seeds = None
    display_mode = 0

    num_superpixels = 400
    num_iterations = 10

    prior = 2
    num_levels = 4
    num_histogram_bins = 5

    img_dir = 'cropped_images/'

    preprocessing = False

    output_dir = 'average_superpixels/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(img_dir):
        if file.endswith(".jpg"):

            path = (os.path.join(img_dir, file))
            img = cv2.imread(path)

            if preprocessing:
                new_img = pre_process_by_L0(img_dir,file)
            else:
                new_img = img

            converted_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)

            height,width,channels = converted_img.shape
            seeds = cv2.ximgproc.createSuperpixelSEEDS(width, height, channels,
                    num_superpixels, num_levels, prior, num_histogram_bins)
            color_img = np.zeros((height,width,3), np.uint8)
            color_img[:] = (0, 0, 255)

            seeds.iterate(converted_img, num_iterations)

            # retrieve the segmentation result
            labels = seeds.getLabels()

            superpixel_dict = {}

            for x in xrange(labels.shape[0]):
                for y in xrange(labels.shape[1]):
                    superpixel_dict.setdefault(labels[x,y], set()).add((x,y))

            get_average_superpixels(superpixel_dict,img, labels,output_dir, file)

            display_superpixels(labels,seeds,img,color_img,display_mode)


if __name__ == '__main__':
    main()