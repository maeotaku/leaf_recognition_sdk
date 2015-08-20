import numpy as np
from datetime import datetime
from Search.Label import Label
from Search.SimilaritySearch import SimilaritySearch
from Log import Log

class ExperimentBase(object):
    
    def __init__(self, name, histogramType):
        self.name = name #name of the experiment
        self.ht = histogramType
        self.log = Log()
        self.hits = {}
        self.hitsBySpecies = {}
        self.attemptsBySpecies = {}
        self.attempts = 0
        
    def getAccuracy(self, k):
        if self.attempts != 0:
            return float(self.hits[k]) / float(self.attempts)
        return -1
    
    def writeAccuracy(self, k):
        self.log.writeWithDateTime("Accuracy for k=" + str(k) + ": " + str(self.getAccuracy(k)))
    
    def writeWithDateTime(self, text):
        self.log.writeWithDateTime(text)
    
    def getCurrentDateTime(self):
        d = datetime.now()
        return str(d.strftime("%Y-%m-%d_%I_%M_%p"))
    
    def getTopK(self, neighbours, dist, labels, k, expectedLabel):
        neighbours = neighbours.flatten()
        dist = dist.flatten()
        #if len(dist)>=1 and dist[0]==0: #in case all vs all
        #    dist = np.delete(dist, 0)
        #    neighbours = np.delete(neighbours, 0)
        results = []
        resultsdists = []
        cont=0
        while cont<len(neighbours) and k>0:
            pos = neighbours[cont]
            item = labels[pos] 
            if not(expectedLabel.equals(item)):
                item.setDistance(dist[cont])
                if not item in results and dist[cont]>0:
                    results.append(item)
                    resultsdists.append(dist[cont])
                    k-=1
            cont+=1
        return results
    
    def incHitsBySpecies(self, key):
        if key in self.hitsBySpecies:
            self.hitsBySpecies[key]+=1
        else:
            self.hitsBySpecies[key]=1
    
    def incHits(self, key):
        if key in self.hits:
            self.hits[key]+=1
        else:
            self.hits[key]=1
    
    def hit(self, key, keySpecies, results, expectedLabel):
        self.incAttemptsBySpecies(keySpecies)
        if expectedLabel in results:
            self.incHits(key)
            self.incHitsBySpecies(keySpecies)
            return True
        return False
            
    def incAttemptsBySpecies(self, key):
        if key in self.attemptsBySpecies:
            self.attemptsBySpecies[key]+=1
        else:
            self.attemptsBySpecies[key]=1

    def isHit(self, results, expectedLabel):
        if expectedLabel in results:
            return True
        return False

    def resultsToSpecies(self, results, labels):
        l = []
        for r in results.flatten():
            l.append(labels[r])
        return l

    
    def getSpeciesAccuracyVector(self):
        res=[]
        for key in self.hitsBySpecies:
            accuracy = float(self.hitsBySpecies[key]) / float(self.attemptsBySpecies[key])
            if len(key)==2:
                res+=[[key[0], key[1], accuracy]]
        return res
                