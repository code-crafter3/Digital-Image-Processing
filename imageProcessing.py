import numpy as np
from PIL import Image
import math

class ImageProcessing:
    def __init__(self,h,w):
        self.height = h
        self.width = w
        
        
    def flipImageVertically(self,imgArray, dtype):
        if self.width > self.height:
            flipimage = np.zeros((self.width,self.width),dtype)
        else:
            flipimage = np.zeros((self.height,self.height),dtype)
        y = self.height-1
        for i in range(self.height): 
            for j in range(self.width):
                flipimage[j][y] = imgArray[i][j]
            y -= 1
        self.saveImage(flipimage,"flipImageVertically.png")
    
    def negativeImage(self,imgArray, dtype):
        negImage = np.zeros((self.height,self.width),dtype)
        for i in range(self.height):
            for j in range(self.width):
                negImage[i][j] = 255 - imgArray[i][j]
        self.saveImage(negImage,"negativeImage.png")
    
    
    def bitOfBinary(self,pixel,depth):
        binary = []
        while(pixel > 0):
            binary.append(pixel%2)
            pixel = pixel // 2
        for i in range(8-len(binary)):
            binary.append(0)
        return binary[depth]
    
    def bitPlane(self,imgArray,depth):
        print("bitPlaneStart")
        for i in range(self.height):
            bitImage = ""
            for j in range(self.width):
                bitImage +=  str(self.bitOfBinary(imgArray[i][j],depth))
            print(bitImage)
        print("bitPlaneEnd")
        
            
    
    def Brightness(self,imgArray):
        avg = 0
        for i in range(self.height):
            for j in range(self.width):
                avg += (1/(self.height*self.width))*imgArray[i][j]
        return avg
    
    def DisplayContrast(self,imgArray):
        bright = self.Brightness(imgArray)
        avgSquare = 0
        for i in range(self.height):
            for j in range(self.width):
                avgSquare += (1/(self.height*self.width))*(pow((imgArray[i][j]-bright),2))
        print("Contrast: "+str(round(math.sqrt(avgSquare))))

    def threshold(self,imgArray, dtype):
        tImage = np.zeros((self.height,self.width),dtype)
        avgIntensity = self.Brightness(imgArray)
        print("Average Intensity: "+ str(round(avgIntensity)))
        for i in range(self.height):
            for j in range(self.width):
                if imgArray[i][j] > avgIntensity:
                    tImage[i][j] = 255
                else:
                    tImage[i][j] = 0
        self.saveImage(tImage,"thresholding.png")
    
    def powerLawTransformation(self,rArray, dtype):
        c = 1
        gamma = float(input("Enter the gamma value: "))
        sArray = np.zeros((self.height,self.width),dtype)
        for i in range(self.height):
            for j in range(self.width):
                sArray[i][j] = c * round(pow(rArray[i][j],gamma))
        self.saveImage(sArray,"powerLawTransformation.png")
    
    def contrastStretching(self,rArray, dtype):
        a = 0
        b = 255
        c = np.amin(rArray) 
        d = np.amax(rArray)
        sArray = np.zeros((self.height,self.width),dtype)
        for i in range(self.height):
            for j in range(self.width):
                sArray[i][j] = round((rArray[i][j]-c)*((b-a)/(d-c))+a)
        self.saveImage(sArray,"contrastStretching.png")
    
    def saveImage(self,imgArray,imgname):
        image = Image.fromarray(imgArray)
        image.save(imgname)
    
    def entropy(self,rArray):
        calEntropy = 0
        (unique,freq) = np.unique(rArray, return_counts=True)
        for i in range(len(freq)):
            calEntropy += (freq[i]/(self.height*self.width))*(np.log2(freq[i]/(self.height*self.width)))
        print("Entropy: "+str((-1)*calEntropy))
    
def main():
    #Enter the input image
    img = Image.open("horse.png")
    if img.mode == 'RGB':
        img = img.convert("L")
    imgArray = np.array(img)
    h,w = imgArray.shape
    obj = ImageProcessing(h,w)
    obj.flipImageVertically(imgArray,imgArray.dtype)
    obj.negativeImage(imgArray,imgArray.dtype)
    obj.entropy(imgArray)
    obj.DisplayContrast(imgArray)
    obj.threshold(imgArray,imgArray.dtype)
    obj.powerLawTransformation(imgArray,imgArray.dtype)
    obj.contrastStretching(imgArray,imgArray.dtype)
    depth = int(input("Enter the depth for bitPlane: "))
    obj.bitPlane(imgArray,depth)
    
if __name__ == "__main__":
    main()
