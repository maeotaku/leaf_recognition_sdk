from ExperimentBase import *
        
class ExperimentSingle(ExperimentBase): #one set to be divided

    def __init__(self, name, histogramType, dataset):
        ExperimentBase.__init__(self, name, histogramType)
        self.dataset = dataset
        self.sim = None
        
    def run(self, maxk):
        self.sim = SimilaritySearch()
        self.writeWithDateTime("Experiment Start: " + self.name)
        self.log.writeWithDateTime("Start ")
        #self.randomize(self.trainingPerc, self.testingPerc)
        self.train()
        self.executeExperiment(maxk)
        self.log.writeWithDateTime("Finished ")
    
    #uses rthe trainign set to train the kNN
    def train(self):
        self.log.writeWithDateTime("Training...")
        self.totalTrainingImages = self.dataset.getTrainingSize()
        self.log.writeWithDateTime("Init Training...")
        for i in range(0, self.dataset.getTrainingSize()):
            hist = self.dataset.trainingData[i]
            label = self.dataset.trainingLabels[i]
            self.sim.addHistogram(hist, label)
            self.log.writeWithDateTime(label.imagePath)
        self.sim.train()
    
    def executeExperiment(self, maxk):
        self.attempts = self.dataset.getTestingSize()
        for k in range(1, maxk+1):
            self.hits[k] = 0
        for i in range(0,self.attempts):
            #self.hits = 0
            hist = self.dataset.testingData[i]
            neighbours, dist = self.sim.findk(hist)
            expectedLabel = self.dataset.testingLabels[i]
            for k in range(1, maxk+1):
                results = self.getTopK(neighbours, dist, self.dataset.trainingLabels, k, expectedLabel)
                if self.hit(k, (expectedLabel.getKey(), k), results, expectedLabel):
                    self.log.writeWithDateTime("Hit: " + str(expectedLabel) + " and got " + ''.join(map(str,results)))
                else:
                    self.log.writeWithDateTime("Failed: expected: " + str(expectedLabel) + " and got " + ''.join(map(str,results)))
        self.log.writeWithDateTime("Training Set: " + str(self.dataset.getTrainingSize()))
        self.log.writeWithDateTime("Attempts: " + str(self.attempts))
        for k in range(1, maxk+1):
            self.log.writeWithDateTime("Hits for k=" + str(k) + ": " + str(self.hits[k]))
            self.log.writeWithDateTime("Accuracy for k=" + str(k) + ": " + str(self.getAccuracy(k)))
        
        
