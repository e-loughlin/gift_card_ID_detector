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

from common import *

def main():
    args = parseArgs()

    logger.info("Initiating Gift Card ID Reader")
    images = readImages(args["img_dir"])

if __name__ == "__main__":
    global logger
    # log_name = "{}.log".format(datetime.now().strftime("%d-%m-%Y_%H-%M"))
    log_name = "output.log"
    logger = configureLogger('default', log_path=os.path.join(os.getcwd(), "logs", log_name))
    main()