import random
import numpy as np
import time
import Constants as C
from Experiments.Log import Log
from LeafImages.LeafImage import LeafImage
from Files import *
from ImageCoreManipulation import *
from Search.Label import *
from Search.SimilaritySearch import SimilaritySearch
from Data.DataSet import *

class MobileSimulation():

    def __init__(self, maxk, path, disks, circumferences):
        self.knn1 = None
        self.knn2 = None
        self.path = path
        self.maxk = maxk
        self.disks = disks
        self.circumferences = circumferences
        self.ds1 = self.loadDataset(C.HIST_HCoS, path)
        self.ds2 = self.loadDataset(C.HIST_LBP_R1P8_R3P16_CONCAT, path)
        self.log = Log()
        
    def loadDataset(self, ht, trainingPath):
        dataset = DataSet()
        dataset.load(ht, trainingPath)
        return dataset
    
    def addHistogramsAndLabels(self, ds, knn):
        for i in range(0, ds.getTrainingSize()):
            hist = ds.trainingData[i]
            label = ds.trainingLabels[i]
            knn.addHistogram(hist, label)
        knn.train()
    
    def train(self):
        self.knn1 = SimilaritySearch(k=self.ds1.getTrainingSize())
        self.knn2 = SimilaritySearch(k=self.ds2.getTrainingSize())
        self.addHistogramsAndLabels(self.ds1, self.knn1)
        self.addHistogramsAndLabels(self.ds2, self.knn2)
    
    def mergeResults(self, results1, results2, maxk):
        kResults={}
        for p in C.PERC_COMBS:
            results = {}
            for key, value in results1.items():
                if not key in results2:
                    results[key] =  value * p
            for key, value in results2.items():
                if not key in results1:
                    results[key] =  value * (1-p)
                    
            for key, value in results1.items():
                if key in results2:
                    v1 = value * p
                    v2 = (1-p) * results2[key]
                    results[key] = v1 + v2
            
            for k in range(1,maxk+1):
                kResults[(p,k)]=sorted(results, key=results.__getitem__)[0:k]
        return kResults

    def getSpeciesDictFromSearch(self, dist, neigh, ds, expectedLabel):
        labels = ds.trainingLabels
        neigh = neigh.flatten()
        dist = dist.flatten()
        maxi = np.max(dist)
        mini = np.min(dist)
        rankRange =  float(maxi - mini)
        if rankRange==0:
            rankRange = 1
        
        results =  {}
        for cont in range(0,len(neigh)):
            pos = neigh[cont]
            item = labels[pos]
            if not(expectedLabel.equals(item)):
                if not item.getKey() in results:
                    results[item.getKey()] = (dist[cont] - mini) / rankRange
        return results
    
    def getTopK(self, neighbours1, dist1, neighbours2, dist2, maxk, expectedLabel):  
        results1 = self.getSpeciesDictFromSearch(dist1, neighbours1, self.ds1, expectedLabel)
        results2 = self.getSpeciesDictFromSearch(dist2, neighbours2, self.ds2, expectedLabel)
        return self.mergeResults(results1, results2, maxk)
    
    def runKnn(self, knn, hist):
        return knn.findk(hist)
    
    def parseResults(self, results):
        aux = ""
        cont = 1
        for label in results:
            aux = aux + "\n" + str(cont) + "." + str(label)
            cont+=1
        return aux
    
    def run(self):
        self.train()
        speciesFolders = cleanHiddenFiles(getFolderContents(self.path))
        for speciesName in speciesFolders:
            speciesFolder = getPath(self.path, speciesName) #folder for 1 species
            if os.path.isdir(speciesFolder):
                images = cleanHiddenFiles(getFolderContents(speciesFolder))
                for imageName in images:
                    try:
                        name = getPath(speciesFolder, imageName)
                        img = loadImage(name)
                        start = time.time()
                        #a mobile phone would request to process the image and get the species list
                        speciesImage = LeafImage(inputImg=img, disks=self.disks, circumferences=self.circumferences)
                        neighbours1, dist1 = self.runKnn(self.knn1, speciesImage.getHistogram(C.HIST_HCoS))
                        neighbours2, dist2 = self.runKnn(self.knn2, speciesImage.getHistogram(C.HIST_LBP_R1P8_R3P16_CONCAT))
                        histPath = C.matchHistToName(C.HIST_HCoS)
                        expectedLabel = Label(speciesName, histPath, speciesFolder)
                        kResults = self.getTopK(neighbours1, dist1, neighbours2, dist2, self.maxk, expectedLabel)
                        
                        end = time.time()
                        elapsed = end - start
                        self.log.write(name  + "\t" + str(elapsed))
                        aux = self.parseResults(kResults) + "\n"
                        print(name  + "\t" + str(elapsed))
                    except Exception as e:
                        print(e)
        self.log.toDisk("/Users/maeotaku/Documents/time_results_noisy.txt")
    

    
                    