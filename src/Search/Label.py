import os
from Files import *

class Label():
    
    
    def testImageExtension(self, folder, histName):
        partial = getPath(folder, getNameOfFile(histName))
        if fileExists(partial+".JPG"):
            return partial + ".JPG"
        if fileExists(partial+".jpeg"):
            return partial + ".jpeg"
        if fileExists(partial+".jpg"):
            return partial + ".jpg"
        if fileExists(partial+".PNG"):
            return partial + ".PNG"
        if fileExists(partial+".png"):
            return partial + ".png"
        return ""
    
    def __init__(self, speciesName, histName, folder):
        self.speciesName = speciesName
        self.histName = histName
        self.folder = folder
        self.imagePath = self.testImageExtension(folder, histName)
        #self.info = os.stat(self.imagePath)
        self.distance = 0
    
    def getKey(self):
        return self.speciesName
    
    def equals(self, other):
        return self.speciesName == other.speciesName and self.imagePath == other.imagePath
            
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.speciesName == other.speciesName
    
    def __str__(self):
        return self.speciesName + "-" + self.histName + "-" + str(self.distance)
    
    def setDistance(self, distance):
        self.distance = distance