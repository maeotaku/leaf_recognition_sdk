from scipy import ndimage, interpolate, signal as sg
import cv2
import numpy as np
import os
from Disk import *
import time

from LeafImages.LeafImage import LeafImage
from Files import *
from Search.Label import *
from Search.FindK import *
from ImageCoreManipulation import *
from Experiments.MultipleRuns import *
from Constants import *
from Exceptions.CustomException import ContoursException
from Experiments.Log import Log
from Simulation.MobileSimulation import *


print(os.path.dirname(ndimage.__file__))
print(os.path.dirname(cv2.__file__))
print(os.path.dirname(np.__file__))
print(os.path.dirname(cv2.__file__))

def createHistogramFolders(folder, histogramTypes):
    for ht in histogramTypes:
        createFolder(getPath(folder, matchHistToName(ht)))
    createFolder(getPath(folder, "_Segmented"))
    createFolder(getPath(folder, "_Contours"))
    createFolder(getPath(folder, "_LBP"))
    createFolder(getPath(folder, "_Thumbnails"))
            
def saveImageObjs(folder, imagename, sample, histogramTypes):
    for ht in histogramTypes:
        saveObj(getPath(getPath(folder,matchHistToName(ht)), imagename + ".histogram"), sample.getHistogram(ht))
    saveImage(getPath(getPath(folder,"_Segmented"), imagename + "_seg.jpg"), sample.finalSegImg)
    saveImage(getPath(getPath(folder,"_Contours"), imagename + "_contour.jpg"), sample.contoursImg)
    #saveImage(getPath(getPath(folder,"_LBP"), imagename + "_LBPR1P8.jpg"), sample.venation.lbpR1P8pic)
    #saveImage(getPath(getPath(folder,"_LBP"), imagename + "_LBPR3P16.jpg"), sample.venation.lbpR3P16pic)
    #saveImage(getPath(getPath(folder,"_LBP"), imagename + "_LBPR3P16.jpg"), sample.venation.lbpR3P16pic)
    saveImage(getPath(getPath(folder,"_Thumbnails"), imagename + "_thumbnail.jpg"), sample.thumbnail)
    
      

def buildHistogramFiles(path, histogramTypes, disks, circumferences):
    #path = "/Users/maeotaku/Documents/Leaves/Flavia/Training/"
    speciesFolders = cleanHiddenFiles(getFolderContents(path))
    cont=1
    for folderName in speciesFolders:
        folder = getPath(path, folderName)
        if os.path.isdir(folder):
            print(folder)
            images = cleanHiddenFiles(getFolderContents(folder))
            createHistogramFolders(folder, histogramTypes)
            for imageName in images:
                try:
                    image = getPath(folder, imageName)
                    print(image)
                    imagename = getNameOfFile(image)
                    sample = LeafImage(disks, circumferences, path=image, species=cont, speciesInfo=imagename)
                    saveImageObjs(folder, imagename, sample, histogramTypes)
                except Exception as e:
                    #print("Error: " , imageName)
                    print(e)
            cont+=1
    
    
def runMobileSimulations(disks, circumferences):
    simulation = MobileSimulation(10, "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/", disks, circumferences)
    simulation.run()    
            
if __name__ == '__main__':
    disks = generateDiskKernelsMasks(25) #used for naive
    circumferences = generateDiskCircumferenceKernelsMasks(25)
    #disks = generateDiskKernels(25) #used for complex curvature based on paper
    
    es = LeafImage(disks, circumferences, path="/Users/maeotaku/Documents/Issues/AA 1.jpeg")    
    es.showImages()
    
    #buildHistogramFiles("/Users/maeotaku/Documents/DatasetsNon1/Flavia/", [C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT], disks, circumferences)
    #buildHistogramFiles("/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/", [C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT], disks, circumferences)
    #buildHistogramFiles("/Users/maeotaku/Documents/DatasetsNon1/CostaRica/ScannedClean/", [C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT], disks, circumferences)
    #buildHistogramFiles("/Users/maeotaku/Documents/DatasetsNon1/LeafSnap/lab", [C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT], disks, circumferences)
    '''
    runs = MultipleRuns("_Flavia",
                        "/Users/maeotaku/Documents/DatasetsNon1/Flavia/",
                        "/Users/maeotaku/Documents/DatasetsNon1/Flavia/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    '''
    runs = MultipleRuns("_LeafSnapFieldCut",
                        "/Users/maeotaku/Documents/DatasetsNon1/LeafSnapCut/field/",
                        "/Users/maeotaku/Documents/DatasetsNon1/LeafSnapCut/field/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    '''
    runs = MultipleRuns("_LeafSnapLab",
                        "/Users/maeotaku/Documents/DatasetsNon1/LeafSnap/lab/",
                        "/Users/maeotaku/Documents/DatasetsNon1/LeafSnap/lab/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    '''
    runs = MultipleRuns("_Testsssssss",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        ((C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT), C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    '''
    runs = MultipleRuns("_CostaRicaOnlyCamera",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        #( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    '''
    runs = MultipleRuns("_CostaRicaScannedClean",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/ScannedClean/",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/ScannedClean/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        #( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()


    runs = MultipleRuns("_CostaRicaBoth",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/ScannedClean/",
                        "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/",
                        "/Users/maeotaku/Dropbox/MSc TEC/Tesis2/Experiments/",
                        #( C.HIST_HCoS, C.HIST_LBP_R1P8, C.HIST_LBP_R2P16, C.HIST_LBP_R3P16, C.HIST_LBP_R1P8_R2P16_CONCAT, C.HIST_LBP_R1P8_R3P16_CONCAT, C.HIST_LBP_R2P16_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        ( C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT, (C.HIST_HCoS, C.HIST_LBP_R1P8_R3P16_CONCAT)),
                        #numberRuns=10,
                        maxk=10)
                        #trainingPerc=0.80)
    runs.buildRuns()
    runs.generateExcel()
    '''
    print("Done") 
    cv2.waitKey()
    