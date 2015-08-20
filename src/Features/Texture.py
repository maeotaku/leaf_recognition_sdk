import cv2
from mahotas.features import lbp
from ImageCoreManipulation import *

class Texture(object):

    def __init__(self, img):
        self.img = img#threadsHolding(img)
        #self.pixels = pixels  
        print("Extracting LBP...")
        self.lbpR1P8 = normalize(np.float32(lbp(self.img, 1, 8, ignore_zeros=False)))
        self.lbpR2P16 = normalize(np.float32(lbp(self.img, 2, 16, ignore_zeros=False)))
        self.lbpR3P16 = normalize(np.float32(lbp(self.img, 3, 16, ignore_zeros=False)))
        #self.lbpR3P24 = normalize(np.float32(lbp.lbp(self.img, 3, 24, ignore_zeros=False)))
        self.lbpR1P8_R2P16 = np.float32(np.concatenate([self.lbpR1P8, self.lbpR2P16]))
        self.lbpR1P8_R3P16 = np.float32(np.concatenate([self.lbpR1P8, self.lbpR3P16]))
        self.lbpR2P16_R3P16 = np.float32(np.concatenate([self.lbpR2P16, self.lbpR3P16]))
        
        #self.lbpR1P8pic = np.float32(lbp.lbp_transform(self.img, 1, 8, ignore_zeros=False))
        #self.lbpR2P16pic = np.float32(lbp.lbp_transform(self.img, 2, 16, ignore_zeros=False))
        #self.lbpR3P16pic = np.float32(lbp.lbp_transform(self.img, 3, 16, ignore_zeros=False))
        #self.lbpR3P24pic = np.float32(lbp.lbp_transform(self.img, 3, 24, ignore_zeros=False))
        
        '''
        self.SURFFimg, self.SURFdescs = SURF(self.img)
        self.BRIEFimg, self.BRIEFdescs = BRIEF(self.img)
        self.ORBimg, self.ORBdescs = ORB(self.img)
        '''