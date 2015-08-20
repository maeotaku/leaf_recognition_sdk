import cv2 
import numpy as np
from scipy import ndimage
from StopWatch import *
import Constants as C
from Exceptions.CustomException import ContoursException


def getNonSmallComponents(components, n):
    valid = []
    areas = [None]
    #masks = []
    for i in range(1, n+1):
        area = getComponentArea(components, i)
        areas+=[area]
        if area > 1000:
            valid+=[i]
            #masks+=[mask]
    return valid, areas#, masks

def getImageBorderMask(h, w):
    newBorderMask = np.ones((h, w), dtype=np.uint8)
    for hc in range(10, h-10):
        for wc in range(10, w-10):
            newBorderMask[hc][wc] = 0
    return newBorderMask

def getComponentIntersectionWithBorder(componentMask, borderMask, h, w):
    res = componentMask * borderMask
    return len(res[res==1])

def getComponentArea(mask, number):
    return len(mask[mask==number])

def getMaskFromAComponent(components, n):
    components[components != n] = 0
    components[components == n] = 1
    return components

def getBiggestComponent(img):
    components, n = ndimage.measurements.label(img)
    areas = []
    for i in range(1, n+1):
        areas+= [getComponentArea(components, i)]
    maxi = areas.index(max(areas)) + 1
    return getMaskFromAComponent(components, maxi)
    

def findLeafComponent(segImg, h, w):
    borderMask = getImageBorderMask(h,w)
    components, n = ndimage.measurements.label(segImg)
    ids, areas = getNonSmallComponents(components, n)
    if len(ids)==0:
        raise ContoursException("No contours found")
    if len(ids)==1: #if there is only one just send it back
        return getMaskFromAComponent(components, ids[0]), areas[ids[0]]
    pos = -1
    maxinters = 0
    posareas = []
    masks = []
    posactual = 0 #current position
    for i in ids: #iterate only on the ids we care about
        componentMask = getMaskFromAComponent(components.copy(), i)
        area = areas[i]
        inters = getComponentIntersectionWithBorder(componentMask, borderMask, h, w)
        posareas.append(area)
        masks.append(componentMask)
        if ((inters>maxinters)):
            maxinters = inters
            pos = posactual
        posactual+=1
    if pos>-1:
        posareas.pop(pos)
        masks.pop(pos)
    maxi = max(posareas)
    index = posareas.index(maxi)
    return masks[index],  maxi
    