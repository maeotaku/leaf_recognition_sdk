import time
import cv2
import numpy as np
import Constants as C
from numpy import random
from sklearn.neighbors import NearestNeighbors, DistanceMetric
from sklearn.neighbors.ball_tree import BallTree
from LeafImages.LeafImage import LeafImage

class SimilaritySearch():

    def euclidean(self, x, y):
        return np.sum((x-y)**2)
    
    #no normalization
    def intersection(self, x, y):
        return np.sum(x) - np.sum(np.minimum(x,y))

    def __init__(self, k=C.KNN_DEFAULT, data=None, labels=None):
        self.knn = NearestNeighbors(n_neighbors=k, algorithm='ball_tree', metric='pyfunc', func=self.intersection)
        #self.knn = NearestNeighbors(n_neighbors=k, algorithm='ball_tree', metric='minkowski')
        self.k = k
        if not data is None:
            self.data = data
            self.labels = labels
            self.train()
        else:
            self.data = []
            self.labels = []

    def addHistogram(self, hist, label):
        self.data.append(hist)
        self.labels.append(label)

    def train(self):
        self.knn.fit(np.array(self.data), np.array(self.labels))
    
    def findk(self, hist):
        dist, neigh = self.knn.kneighbors(np.array([hist]))
        return neigh, dist