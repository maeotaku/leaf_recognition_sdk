import numpy as np
import cv2
import os 
import math
from scipy import ndimage
from StopWatch import *
import Constants as C
from Components import *
from Exceptions.CustomException import ContoursException
from ImageCoreManipulation import *
from Contours import *


def cleanStem(segImg, h, w):
    print("Cleaning stem....")
    t = StopWatch()
    _, nComponents = ndimage.measurements.label(segImg)
    '''
    def getContourAspectRatio(contour):
        _,_,w,h = cv2.boundingRect(contour)
        a = cv2.contourArea(contour)
        return float(w)/float(h) * a
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(C.STEM_KERNEL_SIZE,C.STEM_KERNEL_SIZE))
    th = topHat(segImg, kernel)
    contours, _ =  cv2.findContours(th.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    n = len(contours)
    posactual = 0
    while posactual < n:
        mask = segImg.copy()
        cv2.drawContours(mask, contours[posactual],-1,0,-1)
        _, nCComponents = ndimage.measurements.label(mask)
        if nCComponents == nComponents: #eliminate small contours, mostly garbage
            contours.pop(posactual)
            n = len(contours)
        else:
            posactual+=1
    if contours == []:
        t.stopAndPrint()
        return segImg
    ars = [getContourAspectRatio(ctr) for ctr in contours]
    stem = contours[ars.index(max(ars))]
    cv2.drawContours(segImg, [stem],-1,0,-1) #deletethe stem from the segmentation
    #segImg = getBiggestComponent(segImg) * 255
    #segImg = segImg.astype(np.uint8)
    t.stopAndPrint()
    return segImg