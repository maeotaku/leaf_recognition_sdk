import numpy as np
import cv2
import os 
import math
import Constants as C

def saveImage(name, img):
    cv2.imwrite(name,img)

def loadImage(name):
    img = cv2.imread(name)
    return img

def toGray(img):
    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gimg

def toHSV(img):
    gimg = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return gimg

def toSV(img): 
    hsv = toHSV(img)
    return hsv[:,:,[1,2]] #get rid of hue

def split_HSV(hsv_img):
    h, s, v = cv2.split(hsv_img)
    return h, s, v#hs_img

def resizeImage(img, resx, resy):
    ar = getAspectRatio(img)
    if ar > 1.0:
        img = rotateImage(img, 1)
    return cv2.resize(img, (resx, resy), interpolation=cv2.INTER_AREA)

def cutImage(img, x1, y1, x2, y2):
    return img[int(x1):int(x2+1), int(y1):int(y2+1)]
                
def normalize(histogram):
    return np.divide(histogram, np.sum(histogram))
    
def getImageSizes(img):
    if len(img.shape) == 2:
        height, width = img.shape
    else:
        height, width, _ = img.shape
    return height, width

def getAspectRatio(img):
    height, width = getImageSizes(img)
    return float(height) / float(width)

def rotateImage(image, times):
    return np.rot90(image,times)

def showImage(img, title):
    cv2.imshow(title,img) 
    
def threadsHolding(img):
    return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2)

def closing(img, kernel):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)

def opening(img):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)

def dilation(img):
    kernel = np.ones((1, 1), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, iterations=1)

def topHat(img, kernel):
    return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
      
