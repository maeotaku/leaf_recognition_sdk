from Files import *
from Search.Label import *
from DataSetBase import DataSetBase
import Constants as C
import random

class DataSet(DataSetBase):
    
    def __init__(self,):
        DataSetBase.__init__(self)
        self.data = []
        self.labels = []
    
    #uses the trainign set to train the kNN
    def load(self, ht, path):
        DataSetBase.load(self, ht, path, self.data, self.labels)
        self.testingData = self.data
        self.trainingData = self.data
        self.testingLabels = self.labels
        self.trainingLabels = self.labels

    '''
    def randomize(self, trainingPerc, testingPerc):  
        n = self.getDataSize()
        positions = range(0, n)
        random.shuffle(positions)
        self.randomizeWithPositions(trainingPerc, testingPerc, positions, n)          
    
    def randomizeWithPositions(self, trainingPerc, testingPerc, positions, n):
        self.testingData = []
        self.testingLabels = []
        self.trainingData = []
        self.trainingLabels = []
    
        trainingCut = int(trainingPerc * n)
        pos = 0
        while pos<trainingCut:
            self.trainingData.append(self.data[positions[pos]])
            self.trainingLabels.append(self.labels[positions[pos]])
            pos+=1
        while pos<n:
            self.testingData.append(self.data[positions[pos]])
            self.testingLabels.append(self.labels[positions[pos]])
            pos+=1     
    '''
        
    def add(self, data, label):
        self.data.append(data)
        self.labels.append(label)
        
    def getDataSize(self):
        return len(self.data)
    '''
    def AllvsAll(self):
        self.testingData = self.data
        self.trainingData = self.data
        self.testingLabels = self.labels
        self.trainingLabels = self.labels
    '''  
            
'''
class DataSet():
    
    def __init__(self, dataPath, testingPath=None):
        self.dataPath = dataPath
        if testingPath != None:
            self.testingPath = testingPath
        self.data = []
        self.labels = []
        self.testingData = []
        self.trainingData = []
        self.testingLabels = []
        self.trainingLabels = []
    
    def getTrainingSize(self):
        return len(self.trainingData)
    
    def getTestingSize(self):
        return len(self.testingData) 
    
    def add(self, data, label):
        self.data.append(data)
        self.labels.append(label)
        
    def getDataSize(self):
        return len(self.data)
    
    #uses the trainign set to train the kNN
    def load(self, ht):
        speciesFolders = cleanHiddenFiles(getFolderContents(self.dataPath))
        for speciesName in speciesFolders:
            speciesFolder = getPath(self.dataPath, speciesName) #folder for 1 species
            if os.path.isdir(speciesFolder):
                folder = getPath(speciesFolder, C.matchHistToName(ht)) #go inside to the folder related to the type of histogram
                histogramsPaths = cleanHiddenFiles(getFolderContents(folder))
                for histPath in histogramsPaths:
                    try:
                        hist = loadObj(getPath(folder, histPath))
                        #print(hist, len(hist))
                        self.data.append(hist)
                        self.labels.append(Label(speciesName, histPath, speciesFolder))
                        del hist
                    except Exception as e:
                        print(str(e))
                        
    def AllvsAll(self):
        self.testingData = self.data
        self.trainingData = self.data
        self.testingLabels = self.labels
        self.trainingLabels = self.labels
          
    def randomize(self, trainingPerc, testingPerc):  
        n = self.getDataSize()
        positions = range(0, n)
        random.shuffle(positions)
        self.randomizeWithPositions(trainingPerc, testingPerc, positions, n)          
    
    def randomizeWithPositions(self, trainingPerc, testingPerc, positions, n):
        self.testingData = []
        self.testingLabels = []
        self.trainingData = []
        self.trainingLabels = []
    
        trainingCut = int(trainingPerc * n)
        pos = 0
        while pos<trainingCut:
            self.trainingData.append(self.data[positions[pos]])
            self.trainingLabels.append(self.labels[positions[pos]])
            pos+=1
        while pos<n:
            self.testingData.append(self.data[positions[pos]])
            self.testingLabels.append(self.labels[positions[pos]])
            pos+=1     
'''