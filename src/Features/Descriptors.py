import cv2

def ORB(img):
    orb = cv2.ORB()
    kp = orb.detect(img,None)
    kp, des = orb.compute(img, kp)
    return cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0), des

def BRIEF(img):
    star = cv2.FeatureDetector_create("STAR")
    brief = cv2.DescriptorExtractor_create("BRIEF")
    kp = star.detect(img,None)
    kp, des = brief.compute(img, kp)    
    print brief.getInt('bytes')
    print des.shape
    return cv2.drawKeypoints(img,kp), des

def FREAK(img):
    star = cv2.FeatureDetector_create("FREAK")
    brief = cv2.DescriptorExtractor_create("FREAK")
    kp = star.detect(img,None)
    kp, des = brief.compute(img, kp)    
    print brief.getInt('bytes')
    print des.shape
    return cv2.drawKeypoints(img,kp)


def SURF(img):
    surf = cv2.SURF(400)
    surf.upright = True
    surf.hessianThreshold = 8000
    kp, des = surf.detectAndCompute(img,None)
    #surf.hessianThreshold = 50000
    return cv2.drawKeypoints(img,kp,None,(255,0,0),4), des

#slow
def SIFT(img):
    sift = cv2.SIFT()
    kp = sift.detect(img,None)
    return cv2.drawKeypoints(img,kp)