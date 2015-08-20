import pickle
import os

def saveObj(nombre_archivo, obj):
    archivo = open(nombre_archivo, "wb")
    pickle.dump(obj, archivo)
    archivo.close()

def loadObj(nombre_archivo):
    archivo = open(nombre_archivo, "rb")
    obj = pickle.load(archivo)
    archivo.close()
    return obj

def createFolder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def fileExists(path):
    return os.path.exists(path)

def getPath(path,name):
    return os.path.join(path, name)

def getFolderContents(path):
    #print ([os.path.abspath(name) for name in os.listdir("/Users/maeotaku/Documents/Leaves/Flavia/Training/")])
    try:
        return os.listdir(path)
    except:
        return []

def cleanHiddenFiles(dirs):
    return filter( lambda f: not f.startswith('.'), dirs)

def getNameOfFile(path):
    base=os.path.basename(path)
    return os.path.splitext(base)[0]