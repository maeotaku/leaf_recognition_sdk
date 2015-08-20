import time
import random
#sudo pip install XlsxWriter
import xlsxwriter
from ExperimentSingle import *
from ExperimentCombined import *
from ExperimentBase import *
from Data.DataSet import *
from Data.DataSetSeparate import *

class MultipleRuns(object):

    def __init__(self, name, trainingPath, testingPath, resultPath, histogramTypes, description="", numberRuns=1, maxk=10, trainingPerc=-1):
        self.name = name
        self.description = description
        self.runs = []
        self.numberRuns = numberRuns
        self.root = getPath(resultPath, name + "_" + self.getCurrentDateTime() )
        self.maxk = maxk
        self.histogramTypes = histogramTypes
        self.log = Log()
        self.trainingPerc = trainingPerc
        if self.trainingPerc != -1:
            self.testingPerc = 1 - self.trainingPerc
        self.datasets = {}
        if trainingPath == testingPath:
            for ht in self.histogramTypes:
                if isinstance(ht, int):
                    dataset = DataSet()
                    dataset.load(ht, trainingPath)
                    self.datasets[ht] = dataset
        else:
            for ht in self.histogramTypes:
                if isinstance(ht, int):
                    dataset = DataSetSeparate()
                    dataset.load(ht, trainingPath, testingPath)
                    self.datasets[ht] = dataset
    '''                
    def getShuffledPositions(self, dataset):
        n = dataset.getDataSize()
        positions = range(0, n)
        random.shuffle(positions)
        return positions  
    
    def getOrderedPositions(self, dataset):
        n = dataset.getDataSize()
        positions = range(0, n)
        return positions       
    '''
                    
    def getCurrentDateTime(self):
        d = datetime.now()
        return str(d.strftime("%Y-%m-%d_%I_%M_%p"))
    
    def buildRuns(self):
        #if self.trainingPerc == -1: #if no percentage, all must be used for both training and testing
        #self.buildRunsOneVsAll()
        #else:
        #    self.buildRunsRandom()
        print('Building Multi Run')
        for ht in self.histogramTypes:
            currentht = []
            if isinstance(ht, int):
                dataset = self.datasets[ht]
                exp = ExperimentSingle(self.name, ht, dataset)
                exp.run(self.maxk)
                currentht.append(exp)
            else:
                dataset1 = self.datasets[ht[0]]
                dataset2 = self.datasets[ht[1]]
                exp = ExperimentCombined(self.name, ht, dataset1, dataset2)
                exp.run(self.maxk)
                currentht.append(exp)
            self.runs.append([ht, currentht])
        
    '''
    def buildRunsOneVsAll(self):
        for ht in self.histogramTypes:
            currentht = []
            if isinstance(ht, int):
                dataset = self.datasets[ht]
                dataset.AllvsAll()
                exp = ExperimentSingle(self.name, ht, dataset)
                exp.run(self.maxk)
                currentht.append(exp)
            else:
                dataset1 = self.datasets[ht[0]]
                dataset2 = self.datasets[ht[1]]
                exp = ExperimentCombined(self.name, ht, dataset1, dataset2)
                exp.run(self.maxk)
                currentht.append(exp)
            self.runs.append([ht, currentht])
    '''
    
    '''
    def buildRunsRandom(self):
        for ht in self.histogramTypes:
            currentht = []
            if isinstance(ht, int):
                dataset = self.datasets[ht]
                for i in range(0, self.numberRuns):
                    dataset.randomize(self.trainingPerc, self.testingPerc)
                    exp = ExperimentSingle(self.name, ht, dataset)
                    exp.run(self.maxk)
                    currentht.append(exp)
            else:
                dataset1 = self.datasets[ht[0]]
                dataset2 = self.datasets[ht[1]]
                for i in range(0, self.numberRuns):
                    positions = self.getShuffledPositions(dataset1)
                    dataset1.randomizeWithPositions(self.trainingPerc, self.testingPerc, positions, dataset1.getDataSize())
                    dataset2.randomizeWithPositions(self.trainingPerc, self.testingPerc, positions, dataset1.getDataSize())
                    exp = ExperimentCombined(self.name, ht, dataset1, dataset2)
                    exp.run(self.maxk)
                    currentht.append(exp)
            self.runs.append([ht, currentht])
    '''
    def generateMainTab(self, workbook): 
        worksheet = workbook.add_worksheet("Main")
        worksheet.write(0, 0, "k")
        col=1
        for ht in self.histogramTypes:
            worksheet.write(0, col, C.matchHistToName(ht))
            col+=1
        row=1
        for k in range(1, self.maxk+1):
            col=1
            for ht, currentht in self.runs:
                row = (k-1) * (self.numberRuns) + 1
                worksheet.write(row, 0, k)
                
                for exp in currentht:
                    #print(exp.hitsBySpecies)
                    if isinstance(exp, ExperimentSingle):
                        if k==1:
                            exp.log.toDisk(getPath(self.root , C.matchHistToName(ht) + '_' + str(row) + '_log.txt'))
                        worksheet.write(row, col, str(exp.getAccuracy(k)))
                    else:
                        colaux = col
                        for perc in C.PERC_COMBS:
                            worksheet.write(row, colaux, str(exp.getAccuracy((perc, k))))
                            colaux+=1
                    row+=1
                col+=1
    
    
    def generateSpeciesTab(self, workbook):
        worksheet = workbook.add_worksheet("Species")
        row=0
        #for k in range(1, self.maxk+1):
        for ht, currentht in self.runs:
            for exp in currentht:
                #one experiment per row
                if isinstance(exp, ExperimentSingle):
                    values=exp.getSpeciesAccuracyVector()
                    for dataRow in values:
                        col=1
                        worksheet.write(row, 0, C.matchHistToName(ht))
                        for cellData in dataRow:
                            worksheet.write(row, col, cellData)
                            col+=1
                        row+=1
                    '''
                    else:
                        colaux = col
                        for perc in C.PERC_COMBS:
                            worksheet.write(row, colaux, str(exp.getAccuracy((perc, k))))
                            colaux+=1
                    row+=1
                    '''
        
        
    def generateExcel(self):
        createFolder(self.root)
        print("Generating report...")
        workbook = xlsxwriter.Workbook(getPath(self.root , self.name+"_" +'_report.xlsx'))
        self.generateMainTab(workbook)
        self.generateSpeciesTab(workbook)
        workbook.close()
        
    '''
    def generateLog(self):
        self.log.write(self.description)
        self.log.write("K: " + self.k)
        self.log.toDisk(getPath(self.root , 'results.txt'))
    '''
        
            