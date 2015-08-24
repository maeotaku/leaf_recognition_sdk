import numpy as np
import cv2
import math
from Contours import *
#Basic measures

def calcLeafMinAndMaxContourPoints(binaryImage, contours=None):
    if (contours==None):
        contours = getContours(binaryImage)
    xs = contours[0][:,0][:,0]
    ys = contours[0][:,0][:,1]
    minx = np.min(xs)
    miny = np.min(ys)
    maxx = np.max(xs)
    maxy = np.max(ys)
    return minx, miny, maxx, maxy

def calcLeafWidthAndLength(binaryImage, contours=None, draw=False):
    minx, miny, maxx, maxy = calcLeafMinAndMaxContourPoints(binaryImage, contours)
    first = maxx - minx
    second = maxy - miny
    if (first > second): #we take the biggest always as length based on aspect ratio
        length = first
        width = second
    else:
        length = second
        width = first
    if (draw):
        return length, width, binaryImage
    else:
        return length, width, binaryImage
         
#a binary image must be set, 0 for non-leaf, meaning segmentation has to be done perviously
def calcLeafArea(binaryImage, draw=False):
    if (draw):
        return len(binaryImage[binaryImage > 0]), binaryImage
    else:
        return len(binaryImage[binaryImage > 0]), binaryImage

def calcLeafPerimeter(image, contours=None, draw=False):
    if (contours==None):
        contours = getContours(image)
    if (draw):
        return len(contours[0]), image
    else:
        return len(contours[0]), image

def calcLeafCompactness(binaryImage, area=None, perimeter=None, draw=False):
    if (area==None):
        area = calcLeafArea(binaryImage)
    if(perimeter==None):
        perimeter= calcLeafPerimeter(binaryImage)
    if(draw):
        return float(area) /  float(math.sqrt(perimeter)), binaryImage
    else:
        return float(area) /  float(math.sqrt(perimeter)), binaryImage
    
#longest distance between any 2 points of the margin of the leaf 
def calcLeafDiameter(binaryImage, contours=None, draw=False):
    return None

#Proportions
def calcLeafAspectRatio(binaryImage, width=None, length=None, contours=None, draw=False):
    if (width==None or length==None):
        length, width = calcLeafWidthAndLength(binaryImage, contours, draw)
    if (draw):
        return float(length) / float(width), binaryImage
    else:   
        return float(length) / float(width), binaryImage

#differ between the shape and a circle, also called Form Factor
def calcLeafRoundness(binaryImage, area=None, perimeter=None, draw=False):
    if (area==None):
        area= calcLeafArea(binaryImage)
    if (perimeter==None):
        perimeter=calcLeafPerimeter(binaryImage)
    if (draw):
        return float(4.0 * math.pi * area) / float(perimeter**2), binaryImage
    else:
        return float(4.0 * math.pi * area) / float(perimeter**2), binaryImage

def calcLeafRectangularity(binaryImage, width=None, length=None, area=None, contours=None, draw=False):
    if (width==None or length==None):
        length, width = calcLeafWidthAndLength(binaryImage, contours, draw)
    if (area==None):
        area = calcLeafArea(binaryImage)
    if (draw):
        return float(length * width) / float(area), binaryImage
    else:
        return float(length * width) / float(area), binaryImage

#Vein related
def calcMainVein(image, draw=False):
    return None
    

    