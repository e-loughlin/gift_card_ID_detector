#################################################################
#
#                           / ,e,                     
#    888-~\  e88~~8e  e88~88e  "  Y88b    /  e88~~8e  
#    888    d888  88b 888 888 888  Y88b  /  d888  88b 
#    888    8888__888 "88_88" 888   Y88b/   8888__888 
#    888    Y888    ,  /      888    Y8/    Y888    , 
#    888     "88___/  Cb      888     Y      "88___/  
#                      Y8""8D                         
#    re-give.com
#
#  Author: Evan Loughlin
#  Dec. 8 2020
#
#  main.py : Main Driver
#  ------------
# This program is used to read images of Gift Cards, and extract their ID
# numbers. The output is a CSV file.
#################################################################

import time
import cv2
from datetime import datetime
import sys
import glob
import os

import logging
import logging.config
import argparse

from matplotlib import pyplot as plt 
import pytesseract

image_base_name = None
DIRECTORIES = {}

from dataclasses import dataclass
from enum import Enum

args = None
def args():
    return args

def parseArgs():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("img_dir", help="Input image sequence directory.")
    parser.add_argument("--debug", action='store_false', help="Additional debug output, and image saving.")

    args = vars(parser.parse_args())

    if args["debug"]:
        logger.setLevel(logging.DEBUG)
    return args

def configureLogger(name, log_path):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'mode': 'w',
            }
        },
        'loggers': {
            'default': {
                'level': 'INFO',
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(name)

def configureDirectories(file_base_name):
    DIRECTORIES["output"] = os.path.join(os.getcwd(), "output")
    if not os.path.isdir(DIRECTORIES["output"]):
        os.makedirs(DIRECTORIES["output"])

def readImages(image_directory):
    file_types = ('*.jpg', '*.jpeg', '*.png')
    image_filepaths = []
    for ext in file_types:
        image_filepaths.extend(glob.glob(os.path.join(os.getcwd(), image_directory, ext)))
    
    logger.info("Reading images from {}".format(image_directory))

    image_filepaths.sort()
    for image_fp in image_filepaths:
        logger.info("Loaded image: {}".format(os.path.basename(image_fp)))
            
    images = [cv2.imread(image_filepath) for image_filepath in image_filepaths]
    
    if isDebug():
        showImages("Input", images)
    return images

def isDebug():
    return logger.getEffectiveLevel() >= 20

def showImages(images):
    for i, _ in enumerate(images):
        print(images[i].shape)
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.xticks([]),plt.yticks([])
    plt.show()

def main():
    args = parseArgs()

    logger.info("Initiating Gift Card ID Reader")
    images = readImages(args["img_dir"])

    gray_images = [cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) for im in images]
    showImages(gray_images)
    thresh_images = [cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2) for im in gray_images]

    showImages(thresh_images)
    logger.info("EVAN TEST")
    # Specify structure shape and kernel size.  
    # Kernel size increases or decreases the area  
    # of the rectangle to be detected. 
    # A smaller value like (10, 10) will detect  
    # each word instead of a sentence. 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 

    # Applying  dilation on the threshold image
    dilations = [cv2.dilate(im, rect_kernel, iterations=1) for im in thresh_images]

    # Finding Contours
    image_contours = [cv2.findContours(d, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) for d in dilations]

    copied_images = [im.copy() for im in images]

    for i, contours in enumerate(image_contours):
        file_name = "text_0{}.txt".format(i)
        file = open(file_name, "w+")
        file.write("")
        file.close()

        im2 = copied_images[i]

        # Looping through the identified contours 
        # Then rectangular part is cropped and passed on 
        # to pytesseract for extracting text from it 
        # Extracted text is then written into the text file 
        for cnt in contours: 
            x, y, w, h = cv2.boundingRect(cnt) 
            
            # Drawing a rectangle on copied image 
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            
            # Cropping the text block for giving input to OCR 
            cropped = im2[y:y + h, x:x + w] 
            
            # Open the file in append mode 
            file = open(file_name, "a") 
            
            # Apply OCR on the cropped image 
            text = pytesseract.image_to_string(cropped) 
            
            # Appending the text into file 
            file.write(text) 
            file.write("\n") 
            
            # Close the file 
            file.close()

if __name__ == "__main__":
    # log_name = "{}.log".format(datetime.now().strftime("%d-%m-%Y_%H-%M"))
    log_name = "output.log"
    logger = configureLogger('default', log_path=os.path.join(os.getcwd(), "logs", log_name))
    main()