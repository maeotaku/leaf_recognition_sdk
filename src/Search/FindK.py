from Data.DataSet import *
from Data.DataSetSeparate import *
from Search.SimilaritySearch import *
from LeafImages.LeafImage import LeafImage 
import Constants as C

class FindK():
	
	def __init__(self, dataset, k, disks, circumferences):
		self.dataset = dataset
		self.k = k
		self.disks = disks
		self.circumferences = circumferences
		self.sim = SimilaritySearch()
		self.train()
		
	def train(self):
		for i in range(0, self.dataset.getTrainingSize()):
		    hist = self.dataset.trainingData[i]
		    label = self.dataset.trainingLabels[i]
		    self.sim.addHistogram(hist, label)
		self.sim.train()
		
	def getTopK(self, neighbours, dist, labels, k):
		results = []
		resultsdists = []
		cont=0
		neighbours = neighbours.flatten()
		dist = dist.flatten()
		while cont<len(neighbours) and k>0:
			pos = neighbours[cont]
			item = labels[pos] 
			item.setDistance(dist[cont])
			if not item in results  and dist[cont]>0:
				results.append(item)
				resultsdists.append(dist[cont])
				k-=1
			cont+=1
		return results
	
	def find(self, img, ht):
		print("Searching...")
		speciesImage = SpeciesImage(inputImg=img, disks=self.disks, circumferences=self.circumferences)
		neighbours, dist = self.sim.findk(speciesImage.getHistogram(ht))
		results = self.getTopK(neighbours, dist, self.dataset.labels, self.k)
		return results