import cv2
import numpy as np

def cleanShadows(img, h, w):
    np.set_printoptions(threshold=np.nan)
    b = img.astype(np.double)
    #print(b)
    
    def log(x):
        return math.log(x)
    
    def mini(x):
        return min(x)
    
    def maxi(x):
        return max(x)
    
    def exp(x):
        return math.exp(x)
    
    def inti(x):
        return int(x)
    
    log = np.vectorize(log)
    exp = np.vectorize(exp)
    mini = np.vectorize(mini)
    maxi = np.vectorize(maxi)
    inti = np.vectorize(inti)
    
    b[b == 0]=0.001
    r_b = log(np.divide(b[:,:,0], b[:,:,2]))
    g_b = log(np.divide(b[:,:,1], b[:,:,2]))  
    
    deg=51
    rad = deg*(math.pi/180)
    #print(rad)
    inv = (math.cos(rad)*r_b) - (math.sin(rad)*g_b)
    invexp = exp(inv)
    #print(min(invexp.flatten()))
    invexp=invexp - min(invexp.flatten())
    #print(max(invexp.flatten()))
    invexp= invexp*255 / max(invexp.flatten())
    
    x= (max(g_b.flatten()) + min(g_b.flatten())) / 2
    c1 = g_b[g_b >= x]
    c2 = g_b[g_b < x]
    mc1=np.median(c1)
    mc2=np.median(c2)
    #print(x, mc1, mc2)
    logresRG = np.ones((h, w), dtype=np.double)
    logresBG = np.ones((h, w), dtype=np.double)
    lol = np.zeros((h, w), dtype=np.double)
    i=0
    while i<h:
        j=0
        while j<w:
            if g_b[i,j] >=x:
                logresRG[i,j] = inv[i,j]*math.cos(-rad) + mc1*math.sin(-rad)
                logresBG[i,j] = -inv[i,j]*math.sin(-rad) + mc1*math.cos(-rad)  
                lol[i,j] = 255          
            else:
                logresRG[i,j] = inv[i,j]*math.cos(-rad) + mc2*math.sin(-rad)
                logresBG[i,j] = -inv[i,j]*math.sin(-rad) + mc2*math.cos(-rad)
            j+=1
        i+=1                    
    resRG = exp(logresRG)
    resBG = exp(logresBG)
    rgb = np.ones((h, w, 3), dtype=np.double)
    
    B = (3*invexp) / (resRG + resBG + 1)
    B=B-min(B.flatten())
    B=B/(max(B.flatten()))
    
    R = resRG * B
    R=R-min(R.flatten())
    R=R/(max(R.flatten()))
    
    G = resBG*B
    G=G-min(G.flatten())
    G=G/(max(G.flatten()))
    
    rgb[:,:,0] = (B/2)
    rgb[:,:,1] = G
    rgb[:,:,2] = R

    
    rgb = np.array(g_b*255).astype(np.uint8) #like black and white only
    #equ = cv2.equalizeHist(rgb)
    return rgb 
    #thresh = 127
    #ret = cv2.threshold(rgb, thresh, 255, cv2.THRESH_BINARY)[1]
    #ret = cv2.adaptiveThreshold(rgb,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_OTSU,11,2)
    #return lol 