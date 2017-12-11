import numpy as np
import os

from PIL import Image

'''Crops all BSD images from 321 x 481 and saves them to a new directory'''
def crop_images(img_dir, output_dir):
    for file in os.listdir(img_dir):
        if file.endswith(".jpg"):
            path = (os.path.join(img_dir, file))
            img = Image.open(path)
            img = img.crop((0, 0, img.size[0]-1, img.size[1]-1))
            img.save(output_dir + file)
            print "done with ", file
    print "done with ", img_dir

def main():
    img_dir = '../BSR/BSDS500/data/images/'
    output_dir = 'cropped_images/'

    for endpoint in ['train/', 'val/', 'test/']:
        final_img_dir = img_dir + endpoint
        crop_images(final_img_dir, output_dir)


if __name__ == '__main__':
    main()