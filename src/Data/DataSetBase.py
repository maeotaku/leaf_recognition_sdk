from Files import *
from Search.Label import Label
import Constants as C
import random

class DataSetBase():
    
    def __init__(self):
        self.testingData = []
        self.trainingData = []
        self.testingLabels = []
        self.trainingLabels = []
    
    def getTrainingSize(self):
        return len(self.trainingData)
    
    def getTestingSize(self):
        return len(self.testingData) 
    
    #uses the trainign set to train the kNN
    def load(self, ht, path, data, labels):
        speciesFolders = cleanHiddenFiles(getFolderContents(path))
        for speciesName in speciesFolders:
            speciesFolder = getPath(path, speciesName) #folder for 1 species
            if os.path.isdir(speciesFolder):
                folder = getPath(speciesFolder, C.matchHistToName(ht)) #go inside to the folder related to the type of histogram
                histogramsPaths = cleanHiddenFiles(getFolderContents(folder))
                for histPath in histogramsPaths:
                    try:
                        hist = loadObj(getPath(folder, histPath))
                        #print(hist, len(hist))
                        data.append(hist)
                        labels.append(Label(speciesName, histPath, speciesFolder))
                        del hist
                    except Exception as e:
                        print(str(e))
                        

          
    