import random
import Constants as C
from Files import *
from Search.Label import Label
from DataSetBase import DataSetBase




class DataSetSeparate(DataSetBase):
    
    def __init__(self,):
        DataSetBase.__init__(self)
        
    def load(self, ht, trainingPath, testingPath):
        DataSetBase.load(self, ht, trainingPath, self.trainingData, self.trainingLabels)
        DataSetBase.load(self, ht, testingPath, self.testingData, self.testingLabels)
    '''
    def AllvsAll(self):
        aux = self.testingData + self.trainingData
        self.testingData = aux
        self.trainingData = aux
        aux = self.testingLabels + self.trainingLabels
        self.testingLabels = aux
        self.trainingLabels = aux  
    '''