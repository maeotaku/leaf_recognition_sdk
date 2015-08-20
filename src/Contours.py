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


def getContourAspectRatio(contour):
    _,_,w,h = cv2.boundingRect(contour)
    a = cv2.contourArea(contour)
    return float(w)/float(h) * a

def pointIsInImageBorder(pointh, pointw, h, w):
    if (pointh<=10 or pointh>=h-10):
        return 1
    if (pointw<=10 or pointw>=w-10):
        return 1
    return 0

def calculateIntersectionWithImageBorder(contour, h, w):
    ws = contour[:,0]
    hs = contour[:,1]
    foo = np.vectorize(pointIsInImageBorder)
    inters = np.sum(foo(hs, ws, h, w))
    area = cv2.contourArea(contour)
    return inters, area

def cleanSmallComponents(contours):
    n = len(contours)
    posactual = 0
    while posactual < n:
        #print(contours[posactual].shape[0])
        if contours[posactual].shape[0] < C.MINIMUM_LEAF_VALID_CONTOUR_POINT_NUMBER: #eliminate small contours, mostly garbage
            contours.pop(posactual)
            n = len(contours)
        else:
            posactual+=1
    return contours

def compactContours(contours):
    aux = []
    for ctr in contours:
        for pair in ctr:
            aux = aux + [pair[0].tolist()]
    return aux 

def getContours(img):
    contours, _ =  cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    return contours

def getBiggestContour(img):
    contours, _ =  cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    areas = [cv2.contourArea(ctr) for ctr in contours]
    return [contours[areas.index(max(areas))]]

def extractContours(segImg, checkImgBorders, h, w):
    print("Extracting contours...")
    t = StopWatch()
    contours, _ =  cv2.findContours(segImg.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    maxi = 0
    if checkImgBorders:
        contours = cleanSmallComponents(contours)
        if len(contours)==0:
            raise ContoursException("No contours found")
        if len(contours)==1: #if there is only one just send it back
            return [contours[0]]
        pos = -1
        posactual = 0
        maxinters = 0
        posareas = []
        for ctr in contours:
            inters, area = calculateIntersectionWithImageBorder(ctr[:,0], h, w)
            posareas.append(area)
            if ((inters>maxinters)):
                maxinters = inters
                pos = posactual
            posactual+=1
        if pos>-1:
            posareas.pop(pos)
            contours.pop(pos)
        maxi = contours[posareas.index(max(posareas))]
    else:
        areas = [cv2.contourArea(ctr) for ctr in contours]
        maxi = contours[areas.index(max(areas))]
    if maxi.shape[0] < C.MINIMUM_LEAF_VALID_CONTOUR_POINT_NUMBER:
        raise ContoursException("No valid leaf found. Contours too small, most likely segmentation error.")
    t.stopAndPrint()
    return [maxi]