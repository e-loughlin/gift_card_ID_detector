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
#  ------------
#  common.py : Common utility functions
#################################################################

import glob
import os
import cv2
import sys

import logging
import logging.config
import argparse

logger = logging.getLogger("default")

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

def showImages(title, images):
    for i, image in enumerate(images):
        title_with_number = "{} {}".format(title, str(i).zfill(2))
        showImageAndWait(title_with_number, image)

def showImageAndWait(title, image):
    cv2.imshow(title, image)
    
    while cv2.getWindowProperty(title, 0) >= 0:
        key_code = cv2.waitKey(50)
        if key_code > -1:
            cv2.destroyAllWindows()
            break