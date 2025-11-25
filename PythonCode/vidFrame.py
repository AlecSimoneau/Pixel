import cv2 as cv
import numpy as np
import keyboard as kb
import random

## VARS ##
pixPosition = []
oldSize = (1250,1250)#(127,127)#(1000,1000) 
##########

#random.seed()
class VidFrame(): 
    '''
    This is a file for the VidFrame Class which serves as an extension of the OpenCV 2 Python Library
    VidFrame takes no initial inputs but the functions within it such as makeFrame() allow you to specify the specific 
    number of pixels and colors
    You are able to call makeFrame() several times to add different numbers and colors of pixels to the same image
    '''
    #Initializes with height, width and color channels 
    def __init__(self,                  
                 height = oldSize[0], 
                 width = oldSize[1], 
                 channels = 3):
        self.height = height
        self.width = width
        self.channels = channels
        self.pixDict = dict()
        self.totalInitialPixels = 0
        self.numOfPixels: int = 0
        self.makeFrameCalls = 0
        self.newCoords = []
        self.im = []

    
    def makeFrame(self,
                  numOfPixels: int,
                  color: list = None):
        
        #some of this code only needs to run once, so this is just to keep track of that
        self.makeFrameCalls+=1
        
        #self.pixPosition = pixPosition
        self.numOfPixels += numOfPixels
        self.color = color
        self.totalInitialPixels += numOfPixels
        tempCoords = []
        if self.makeFrameCalls == 1:
            self.im = np.zeros((self.height,self.width,self.channels),np.uint8)
    
            #This generates a coordinate grid of oldsize[0] x oldsize[1] 

            for i in range(0,self.height):
                for j in range(0,self.width):
                    self.newCoords.append((i,j))
            #return tempCoords,newCoords
    
            # This randomly selects numOfPixels unique coordinates from newChoords 
            tempCoords.append(random.sample(self.newCoords,k = self.numOfPixels))
            tempCoords = tempCoords[0]
        
        #same code as right above
        if self.makeFrameCalls > 1:
            tempCoords.append(random.sample(self.newCoords,k = self.numOfPixels))
            tempCoords = tempCoords[0]

        #Removes existing pixel coords from sample space of possible pixel positions
        index = 0
        for i in tempCoords:
            for j in self.newCoords:  
                if j == i:
                    self.newCoords.remove(i)
                    break
                index += 1

        if self.numOfPixels > 1:
            if self.color != None:
                pixColor = self.color
            else:
                pixColor = [255,255,255]
            for i in range(0,len(tempCoords)):
                self.im[tempCoords[i][1],tempCoords[i][0]] = pixColor
            
        else:
            pass #print("There are no pixels to draw.")      

        return self.im,self
                
    ## This is to scale up the image, to reduce the initial amount of pixels i work with
    ## It works so thats good
    def upScale(self,scaleFactor,image):
        if scaleFactor > 0:
            self.height = int(self.height * scaleFactor)
            self.width = int(self.width * scaleFactor)
            return cv.resize(image,(self.height, self.width),interpolation = cv.INTER_LINEAR_EXACT)
        elif scaleFactor < 0:
            self.height = self.height // (scaleFactor * -1)
            self.width = self.width // (scaleFactor * -1)
            return cv.resize(image,(self.height, self.width),interpolation = cv.INTER_LINEAR_EXACT)
        else:
            return image
        

    ## This just makes a window with a 'title' and puts the image 'frame' in it
    def show(self,image,title: str = None, delay = None):
        if title == None:
            title = ""
        cv.imshow(title,image)
        
        # delays window closure 'delay' ms if entered, else until keypress
        if delay == None:
           cv.waitKey(0)
        else:
           cv.waitKey(delay)


    def moveDown(self,im,scaleFactor):
        self.upScale(-1*scaleFactor,im)
        im[self.pixPosition[0], self.pixPosition[1]] = [0,0,0]
        pixPositionNew = [int(self.pixPosition[0])+1,int(self.pixPosition[1])]
        im[pixPositionNew[0],pixPositionNew[1]] = [0,0,255]
        self.pixPosition = pixPositionNew
        return self.show("title",self.upScale(scaleFactor,im))

    def moveUp(self,im,scaleFactor):
        self.upScale(-1*scaleFactor,im)
        im[self.pixPosition[0], self.pixPosition[1]] = [0,0,0]  
        pixPositionNew = [int(self.pixPosition[0])-1,int(pixPosition[1])]
        im[pixPositionNew[0],pixPositionNew[1]] = [0,0,255]  
        pixPosition = pixPositionNew  
        return self.show("title",self.upScale(scaleFactor,im))

    def moveRight(self,im,scaleFactor):
        self.upScale(-1*scaleFactor,im)
        im[pixPosition[0], pixPosition[1]] = [0,0,0]
        pixPositionNew = [int(pixPosition[0]),int(pixPosition[1])+1]
        im[pixPositionNew[0],pixPositionNew[1]] = [0,0,255]
        pixPosition = pixPositionNew
        return self.show("title",self.upScale(scaleFactor,im))
        

    def moveLeft(self,im,scaleFactor,pixPosition):
        self.upScale(-1*scaleFactor,im)
        im[pixPosition[0], pixPosition[1]] = [0,0,0]
        pixPositionNew = [int(pixPosition[0]),int(pixPosition[1])-1]
        im[pixPositionNew[0],pixPositionNew[1]] = [0,0,255]
        pixPosition = pixPositionNew
        return self.show("title",self.upScale(scaleFactor,im))
    
    def closestPoints(self,image,Point,closestNPoints,show=False,scaleFactor=1):
        #All the local variables
        points = []
        PointInPoints = False
        distances = []
        sortedDist = []
        temp = []
        closestPoints = []
        self.scaleFactor = scaleFactor

        #Adds the coordanites of the points with their colors to 
        # the list points
        for i in range(0,self.height):
            for j in range(0,self.width):               
                for k in range(3): 
                    if image[i,j][k] != 0:
                        points.append([[i,j],image[i,j][0]])
                        k=0
                        if j < 99:
                            j+=1
                        elif i < 99:
                            j=0
                            i+=1
                        else:
                            break
                        break
        self.points = points
        #seeing if the user wants a random point or a specific point 
        # in most usecases this will be a specific point                
        if (type(Point) == str) and (Point == "Any"):
            Point = random.sample(points,k = 1)
        else:
            assert(type(Point) == list), "Point must be a list"
        
        #used a lot later so just stored for conveniencee
        pointsSize = len(points)

        # Makes sure the Point we are calculating from actually has a
        # pixel there
        for i in range(pointsSize):
            if Point == points[i][0]:
                PointInPoints = True
#        assert(PointInPoints == True), "Point does not have a pixel at that location"

        #list stuff made Point like [[[thing1,thing2]]] so this fixes that
        Point = Point[0][0]

        # to the list distances, adds [distance from Point , coordanite]
        for i in range(pointsSize):
            distances.append( (  ( (Point[0]-points[i][0][0]) ** 2 + (Point[1]-points[i][0][1]) ** 2 ) ** 0.5 , points[i][0] ))
    
        # adds just the distances into the list sortedDist
        for i in range(pointsSize): 
            sortedDist.append(distances[i][0])

        # sorts the distances
        sortedDist = np.sort(sortedDist)
        
        # matches the distances to the coordanites in the sorted order
        for i in range(pointsSize):
            for j in range(pointsSize):
                if sortedDist[i] == distances[j][0]:
                    temp.append(distances[j])
        temp = temp[:closestNPoints+1]
        for i in range(0,len(temp)):
            closestPoints.append(temp[i][1])

        #trying nested functions, this took a little to figure out because 
        # of scoping and my general incompetence
        def showClosestPoints(self):
            #clearly shows the selected pixel by drawing a white square on it
            # although for this you loose the pixels color
            for i in range(-1,2):
                for j in range(-1,2):
                    image[Point[0]+i,Point[1]+j] = [255,255,255]
            #draws lines to all of the closest points
            for i in range(len(closestPoints)):
                cv.line(
                        img = image,
                        pt1 = [Point[1],Point[0]],
                        pt2 = [closestPoints[i][1],closestPoints[i][0]],
                        color = [150,150,150],
                        thickness = 1
                        )
            #scalefactor can break things if the image is resized above default [oldsize[0],oldsize[1]]
            return self.show(image=self.upScale(image=image,scaleFactor=self.scaleFactor))
        #shows the result
        if show == True:
            return closestPoints, showClosestPoints(self)
        #or just returns the list
        else:
            return closestPoints
