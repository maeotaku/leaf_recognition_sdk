import math
import numpy as np

def generateDiskKernels(maxn):
    h=[]
    rlist = range(1, maxn+1)
    for k in range(0, maxn):
        r = rlist[k];
        x = range(-int(math.ceil(r)),int(math.ceil(r))+1)
        [b,a] = np.meshgrid(x,x)
        h.append( np.array((a**2)+(b**2) <= (r**2)).astype(float) )
        h[k] =  h[k] /np.sum(h[k])
    return h

def generateDiskKernelsMasks(maxn):
    h=[]
    rlist = range(1, maxn+1)
    for k in range(0, maxn):
        r = rlist[k];
        x = range(-int(math.ceil(r)),int(math.ceil(r))+1)
        [b,a] = np.meshgrid(x,x)
        h.append( np.array((a**2)+(b**2) <= (r**2)).astype(float) )
    return h


def isPixelCircum(disk, row, col, height):
    
    if row-1>=0 and not(disk[row-1][col]):
        return True
    if row+1<height and not(disk[row+1][col]):
        return True
    if col-1>=0 and not(disk[row][col-1]):
        return True
    if col+1<height and not(disk[row][col+1]):
        return True
    return False

def extractCircumOnly(disk):
    newdisk = disk.copy()
    h = len(disk)
    for i in range(0, h):
        for j in range(0, h):
            if not(isPixelCircum(disk, i, j, h)):
                newdisk[i][j] = False
    return newdisk

def generateDiskCircumferenceKernelsMasks(maxn):
    h=[]
    rlist = range(1, maxn+1)
    for k in range(0, maxn):
        r = rlist[k];
        x = range(-int(math.ceil(r)),int(math.ceil(r))+1)
        [b,a] = np.meshgrid(x,x)
        circun = extractCircumOnly((a**2)+(b**2) <= (r**2))
        h.append( circun.astype(float) )
    return h