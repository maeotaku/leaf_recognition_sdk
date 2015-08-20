import cv2
from scipy import ndimage
from scipy import interpolate
from scipy import signal as sg
from ImageCoreManipulation import *




class Curvature():
    
    def __init__(self, finalSegImg, contoursSmall, disks, circumferences):
        self.finalSegImg = finalSegImg.copy()
        #self.HCoS = self.extractHCoS(self.resizedLeafImg, contoursSmall[0][:,0], disks)
        self.HCoS = self.extractHoCSNaive(self.finalSegImg, contoursSmall[0][:,0], disks, circumferences)
    
    def binarize(self, M):
        _, MM = cv2.threshold(M, 10, 255, cv2.THRESH_BINARY_INV)
        return (MM / 255.0)
    '''
    def pointIsInImageBorder(self, pointh, pointw, h, w):
            if (pointh<=1 or pointh>=h-1):
                return 1
            if (pointw<=1 or pointw>=w-1):
                return 1
            return 0
    def calculateIntersectionWithImageBorder(self, contour, h, w):
        ws = contour[:,0]
        hs = contour[:,1]
        pointIsInImageBorder = np.vectorize(self.pointIsInImageBorder)
        inters = np.sum(pointIsInImageBorder(hs, ws, h, w))
        if inters>0:
            return True
        return False

    def distanceFromPointToPoint(self, pointh, pointw, toh, tow): 
            return math.sqrt(math.pow(pointw - tow,2) + math.pow(pointw - toh,2))
    def distanceContourToCenter(self, contour, centerh, centerw):
        n = len(contour)
        ws = contour[:,0]
        hs = contour[:,1]
        distanceFromPointToPoint = np.vectorize(self.distanceFromPointToPoint)
        return np.sum(distanceFromPointToPoint(hs, ws, centerh, centerw)) / n
    '''
    
    #used to draw in the image the area calculated, given an specific point of the boundary
    #not used normally only to show hw the disk area is drawn
    def drawDiskMaskInImg(self, img, mask, maskcenter, row, col):
        h, _ = getImageSizes(mask)
        he, wi = getImageSizes(img)
        startcol = col
        for i in range(0, h):
            startrow = row
            for j in range(0, h):
                if startrow>=0 and startcol>=0 and startrow<he and startcol<wi and mask[j,i]==255:
                    img[startrow, startcol] = 150
                startrow+=1
            startcol+=1
        print(row, col)
        showImage(img, "Disk Area Around Boundary Point")
        cv2.waitKey()
   
    #finds a submatrix or subimage that has the common area of the disk with the leaf boundary at point col, row
    def findAreaAndArcSegment(self, segImg, mask, circumference, maskcenter, row, col):
        segImgSegment = cutImage(segImg, row-maskcenter, col-maskcenter, row+maskcenter, col+maskcenter)
        segArea = segImgSegment * mask
        segArc = segImgSegment * circumference
        return segArea, segArc
    
    def extractHoCSNaive(self, segImg, contours, disks, circumferences):
        print("Extracting HCoS...")
        t = StopWatch()
        ys = contours[:,1]
        xs = contours[:,0]
        n = len(xs)
        nrad = 25
        histAreas = [] #this will hold all histograms, 25 diff ones, one per radius
        histArcs = [] #this will hold all histograms, 25 diff ones, one per radius, for arcs
        for k in range(0,nrad): #calculate 25 diff areas
            imgBoundaryIncreased = self.increaseImageBundaries(segImg, disks[k]) #generates the same image with increased boundaries
            areas = [] #all areas from all point at certain disk radius
            arcs = []
            for i in range(0, n): #go through every boundary point
                area, arc = self.findAreaAndArc(imgBoundaryIncreased, disks[k], circumferences[k], ys[i], xs[i])
                arcs = arcs + [arc]
                areas = areas + [area]  
            histArea, bin = np.histogram(areas, density=False, bins=21)
            histArea = normalize(np.float32(histArea))
            histAreas.append(histArea)
            histArc, bin = np.histogram(arcs, density=False, bins=21)
            histArc = normalize(np.float32(histArc))
            histArcs.append(histArc)
            '''
            plt.bar(bin[:-1], histArc, width = 1)
            plt.xlim(min(bin), max(bin))
            plt.show()
            '''
            
        hcos = np.float32(np.concatenate(histAreas+histArcs))
        t.stopAndPrint()
        return hcos
    
    def increaseImageBundaries(self, img, disk):
        p = len(disk)
        d1 = int(math.floor(p/2))
        d2 = p-d1-1
        endRow = len(img)
        endCol = len(img[0])
        xx = img
        #stack rows
        xx = img[d1:0:-1,:]
        xx = np.vstack([xx, img])
        xx = np.vstack([xx, xx[endRow-1:endRow-d2-1:-1,:]])
        #stack cols
        xx = np.hstack([xx[:,d1:0:-1], xx])
        xx = np.hstack([xx, xx[:,endCol-1:endCol-d2-1:-1] ] )
        return xx
    
    #finds the area of the intersection of a disk with the leaf at a pojnt of its boundary
    def findAreaAndArc(self, segImg, disk, circumference, row, col):
        maskcenter = math.floor(len(disk)/2) #get center of the disk/mask
        #img = self.increaseImageBundaries(segImg, disk) #generates the same image with increased boundaries
        segArea, segArc = self.findAreaAndArcSegment(segImg, disk, circumference, maskcenter, row + maskcenter, col + maskcenter)
        #area = np.sum(segArea)
        #arc = np.sum(segArc)
        #area = np.product(segArea[segArea > 0].shape)
        #arc = np.product(segArc[segArc > 0].shape)
        area = len(segArea[segArea > 0])
        arc = len(segArc[segArc > 0])
        #activate HCOS visible
        #if maskcenter==24:
        #    self.drawDiskMaskInImg(self.finalSegImg.copy() ,segArea, maskcenter, row - maskcenter, col - maskcenter)
        return area, arc

    '''
    #-- this section implements the HoCS using convolution and interpolation
    def applyConvolution(self, M, h):
        xx = self.increaseImageBundaries(M, h)
        p = len(h)
        d1 = math.floor(p/2)
        #d2 = p-d1-1
        endRow = len(M)
        endCol = len(M[0])
        Mh = sg.fftconvolve(xx, h, mode='full')#,boundary="wrap")
        Mh = Mh[ (2*d1)+1:(2*d1+endRow)+1, (2*d1)+1:(2*d1+endCol)+1 ]
        #print(p, d1, d2, endRow, endCol, len(Mh), len(Mh[0]))
        return Mh
   
    def resampleCurvature(self, bound0, size):
        nbound = size #size to which resample
        nbound0 = len(bound0[:,0]) #get actual size of the curvature bound
        t = np.linspace(0, nbound0, nbound)
        xs = interpolate.splmake(bound0[:,0], np.transpose(t))
        #xs = interpolate.UnivariateSpline(bound0[:,0],t,k=3,s=0)
        ys = interpolate.splmake(bound0[:,1], t, order=3, kind='smoothest')
        [_, pt] = min(xs)
        bound = np.array([xs[pt:], ys[0:pt]])
        return bound
    
    def extractHCoS(self, M, contour, h):
        bound = contour#self.resampleCurvature(contour, 500)
        print("Extracting HCoS...")
        MM = self.binarize(M)
        hists = []
        bins = []
        ys = bound[:,1]
        xs = bound[:,0]
        nrad = 25
        he, wi = M.shape
        initial = 0
        for k in range(initial,nrad):
            Mh = self.applyConvolution(MM, h[k])
            X = range(1,he+1)
            Y = range(1,wi+1)
            ip = interpolate.RectBivariateSpline(X,Y,Mh, kx=2, ky=2)
            zi = ip.ev(ys, xs)#,dx=0,dy=0)  
            #zi = 1.0 - zi          
            hist, bin = np.histogram(zi, density=False, bins=21)#, range=(0.01,1.0))
            hist = normalize(np.float32(hist))
            hists.append(hist)
            #bins.append(bin)
        hcos = np.float32(np.concatenate(hists))
        return hcos
    '''
        
        