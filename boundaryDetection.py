import cv2 as cv
import numpy as np
import os
import glob

cwd = os.getcwd()
task1 = '\Slices'
pathToTask1 = cwd+task1
task2 = '\Boundaries'
pathToTask2 = cwd+task2
if not os.path.exists(pathToTask2):
   os.makedirs(pathToTask2)

folderNum = 0
while 1:
    folderNum = folderNum+1
    pathToImageFolder = pathToTask1+"\\"+str(folderNum)
    if os.path.exists(pathToImageFolder):
        pathToEachImageFolder = pathToTask2+"\\"+str(folderNum)
        if not os.path.exists(pathToEachImageFolder):
            os.makedirs(pathToEachImageFolder)
        os.chdir(pathToEachImageFolder)
        for images in glob.glob('%s\*.png' % pathToImageFolder):
            imageBaseName = os.path.basename(images)
            words = imageBaseName.split('.')
            imageNumber = words[0]

            img = cv.imread(images)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            blurred = cv.GaussianBlur(gray, (3, 3), 0)
            edged = cv.Canny(blurred, 10, 100)
            contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cv.drawContours(img, contours, -1, (0, 0, 255), 1)
            imageName = imageNumber + '.png'
            cv.imwrite(imageName, img)
    else:
        break
    os.chdir(cwd)