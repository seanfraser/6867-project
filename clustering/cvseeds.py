import numpy as np
import cv2
import sys


if __name__ == '__main__':

    seeds = None
    display_mode = 1

    num_superpixels = 400
    num_iterations = 10

    prior = 2
    num_levels = 4
    num_histogram_bins = 5

    img = cv2.imread('296028.jpg')
    converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    height,width,channels = converted_img.shape
    seeds = cv2.ximgproc.createSuperpixelSEEDS(width, height, channels,
            num_superpixels, num_levels, prior, num_histogram_bins)
    color_img = np.zeros((height,width,3), np.uint8)
    color_img[:] = (0, 0, 255)

    seeds.iterate(converted_img, num_iterations)

    # retrieve the segmentation result
    labels = seeds.getLabels()


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