import traceback
from scipy import ndimage, interpolate, signal as sg
import cv2
import numpy as np
import os
from bottle import route, run, template, request
import jsonpickle
from Files import *
from ImageCoreManipulation import *
from Experiments.MultipleRuns import *
from Constants import *
from Search.Label import *
from Search.FindK import *
from Data.DataSet import *
from Data.DataSetSeparate import *
from Disk import *
from Exceptions.CustomException import ContoursException

def parseResults(results):
    aux = ""
    cont = 1
    for label in results:
        aux = aux + "\n" + str(cont) + "." + str(label)
        cont+=1
    return aux

def getNPFromFile(f):
    return np.asarray(bytearray(f.read()), dtype=np.uint8)
     
     
#if __name__ == '__main__':
print("Preparing Leaf Search Engine...")
disks = generateDiskKernelsMasks(25) #used for naive
circumferences = generateDiskCircumferenceKernelsMasks(25)
dataset = DataSet()
dataset.load(C.HIST_HCoS, "/Users/maeotaku/Documents/DatasetsNon1/CostaRica/OnlyCamera/")
finder = FindK(dataset, C.KNN_DEFAULT, disks, circumferences)
print("Done.")

@route('/', method='POST')
def do_upload():
    try:
        aux = ""
        files = request.files
        for name in files:
            fileUpload = files[name]
            if fileUpload:
                file = fileUpload.file
                img = cv2.imdecode(getNPFromFile(file), cv2.CV_LOAD_IMAGE_UNCHANGED) # This is dangerous for big files
                #img = loadImage("/Users/maeotaku/Documents/Issues/Solved/WrongResize_IMG_6632.JPG")
                results = finder.find(img, C.HIST_HCoS)
                aux += parseResults(results) + "\n"
                #p = jsonpickle.pickler.Pickler()
                #return str(p.flatten(results))
        return aux

    except Exception as e:
        print(e)
        return "Exception: " + traceback.format_exc()
    return "No classification done."

run(host='localhost', port=9093)



    