import cv2
import numpy as np
import os
import glob
from matplotlib import pyplot as plt
from PIL import Image

cwd = os.getcwd()
pathToDataFolder = cwd+'\\testPatient'
task1 = '\Slices'
pathToTask1 = cwd+task1
if not os.path.exists(pathToTask1):
   os.makedirs(pathToTask1)

for globalImage in glob.glob('%s\*_thresh.png' % pathToDataFolder):
    words = globalImage.split('_')
    global_image_number = words[1]
    org_img = cv2.imread(globalImage)
    img_gray = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('template.png',0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    xstart = -1
    xdiff = -10
    ystart = -1
    ydiff = -10

    for pt in zip(*loc[::-1]):
        xtemp = pt[0]
        ytemp = pt[1]+h
        if(xstart == -1):
            xstart = xtemp
        if(ystart == -1):
            ystart = ytemp
        if(xdiff == -10 and xstart != xtemp):
            xdiff = xtemp - xstart
        if(ydiff == -10 and ystart != ytemp):
            ydiff = ytemp - ystart
        if(xstart != -1 and ystart != -1 and xdiff != -10 and ydiff != -10):
            break

    pathToEachImageFolder = pathToTask1+"\\"+str(global_image_number)
    if not os.path.exists(pathToEachImageFolder):
        os.makedirs(pathToEachImageFolder)
    os.chdir(pathToEachImageFolder)

    img1 = Image.open(globalImage)
    width, height = img1.size
    
    loc_img_count = 0

    for y0 in range(ystart, height, ydiff):
        for x0 in range(xstart, width, xdiff):
            if(x0+xdiff < width and y0+ydiff < height):
                box = (x0+5, y0,
                    x0+xdiff if x0+xdiff < width else  width,
                    y0+ydiff if y0+ydiff < height else height)
                img2 = img1.crop(box)
                extrema = img2.convert("L").getextrema()
                if extrema != (0, 0):
                    loc_img_count = loc_img_count + 1
                    img1.crop(box).save('%d.png' % loc_img_count)
    os.chdir(cwd)