import random
import numpy as np
from ExperimentBase import *
import Constants as C



class ExperimentCombined(ExperimentBase):

    def __init__(self, name, histogramType, dataset1, dataset2):
        ExperimentBase.__init__(self, name, histogramType)
        self.knn1 = None
        self.knn2 = None
        self.ds1 = dataset1
        self.ds2 = dataset2
        self.hits = {}
        
    def getAccuracy(self, key):
        if self.attempts != 0:
            return float(self.hits[key]) / float(self.attempts)
        return -1

    def run(self, maxk):
        self.train()
        self.executeExperiment(maxk)
    
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
        #if len(dist)>=1 and dist[0]==0: #in case all vs all
        #    dist = np.delete(dist, 0)
        #    neigh = np.delete(neigh, 0)
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
    
    def executeExperiment(self, maxk):
        self.attempts = self.ds1.getTestingSize()
        for perc in C.PERC_COMBS:
            for k in range(1, maxk+1):
                self.hits[(perc, k)] = 0
        for i in range(0,self.attempts):
            neighbours1, dist1 = self.runKnn(self.knn1, self.ds1.testingData[i])
            neighbours2, dist2 = self.runKnn(self.knn2, self.ds2.testingData[i])
            expectedLabel = self.ds2.testingLabels[i]
            kResults = self.getTopK(neighbours1, dist1, neighbours2, dist2, maxk, expectedLabel)
            for perc in C.PERC_COMBS:
                for k in range(1, maxk+1):
                    self.hit((perc, k), (expectedLabel.getKey(), perc, k), kResults[(perc,k)], expectedLabel.getKey())
    
                    