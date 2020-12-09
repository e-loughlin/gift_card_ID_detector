
import cv2
import numpy as np
import scipy as sp
import unittest
import matplotlib.pyplot as plt
import sys
import glob

import os

IMG_FOLDER = "images/source/frame"
OUTPUT_FOLDER = "images/output"

class Assignment8Test(unittest.TestCase):

    def setUp(self):
        file_types = ('*.jpg', '*.jpeg', '*.png')
        image_filepaths = []
        for ext in file_types:
            # print(os.path.join(os.getcwd(), IMG_FOLDER, ext))
            image_filepaths.extend(glob.glob(os.path.join(os.getcwd(), IMG_FOLDER, ext)))

        image_filepaths.sort()
        
        self.images = [cv2.imread(image_filepath) for image_filepath in image_filepaths]
        

if __name__ == '__main__':
    unittest.main()
