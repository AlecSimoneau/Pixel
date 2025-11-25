import random
from vidFrame import oldSize, VidFrame
import numpy as np
import cv2 as cv
import keyboard as kb
#random.seed(1)

#a binary from 0 to 99 to use as id's for pixels
ID_One = ['0', '1', '10', '11', '100', '101', '110', '111',  
        '1000', '1001', '1010', '1011', '1100', '1101',
        '1110', '1111', '10000', '10001', '10010', '10011',
        '10100', '10101', '10110', '10111', '11000', '11001',
        '11010', '11011', '11100', '11101', '11110', '11111',
        '100000', '100001', '100010', '100011', '100100',
        '100101', '100110', '100111', '101000', '101001',
        '101010', '101011', '101100', '101101', '101110',
        '101111', '110000', '110001', '110010', '110011',
        '110100', '110101', '110110', '110111', '111000',
        '111001', '111010', '111011', '111100', '111101',
        '111110', '111111', '1000000', '1000001', '1000010', 
        '1000011', '1000100', '1000101', '1000110', '1000111', 
        '1001000', '1001001', '1001010', '1001011', '1001100', 
        '1001101', '1001110', '1001111', '1010000', '1010001',
        '1010010', '1010011', '1010100', '1010101', '1010110', 
        '1010111', '1011000', '1011001', '1011010', '1011011', 
        '1011100', '1011101', '1011110', '1011111', '1100000',
        '1100001', '1100010', '1100011']

#ID_One = []
# This Code generates an array of 1 to 999 in binary
#for i in range(0,1000):
#    ID_One.append(bin(i)[2:])

#print(ID_One)

#### User Variables ######
var = {}
placeholder = ""
scaleFactor = 1
newCoords = []
tempCoords = []
sortedArray = []
index = 0
closestPoints = []
n_Closest_Points = 9
##########################

#This generates a coordinate grid of oldsize[0] x oldsize[1] 
for i in range(0,oldSize[0]):
    for j in range(0,oldSize[1]):
        newCoords.append((i,j))
# This randomly selects 100 unique coordinates from newChoords 
tempCoords.append(random.sample(newCoords,100))
#########


# This loop takes the id's from ID_One and assigns them a random pixel position, and whether its an even or odd
# number, they get the designation 'red' or 'blue'
for id in ID_One:
    assert ((id[-1] == "1") or (id[-1] == "0")), "Impropper ID" ## Messing around with assert statements
    if id[-1] == "0":
        placeholder = "red"
    if id[-1] == "1":
        placeholder = "blue"
    
    var.update({id: [tempCoords[0][index], placeholder]})
    index+=1

# Assigns FRAME_ONE the VidFrame class, and I don't need an individual pixel position
# Which is why i am passing in None, (throws an error otherwise)
FRAME_ONE = VidFrame(0)
# Making the frame
imageFrame = FRAME_ONE.makeFrame()

#This for loop takes the pixel position and color, 'red' or 'blue', for each id and 
# Draws them on the image that color
for id in ID_One:
    color = []
    assert (var.get(id)[1]  == "red" or var.get(id)[1] == "blue"), "Incorrect color id" ## Messing around with assert statements again
    if var.get(id)[1] == "red":
        color = [0,0,250]
    else:
        color = [250,0,0]    
    imageFrame[var.get(id)[0][0],var.get(id)[0][1]] = color

# A function to calculate the five closest pixels 
def findDistances(point,dictionary):
    distances = {}

    for key in dictionary:
        # Pythagorean theorem, finding the hypotenuse ( the distance ) from one pixel to the other based on x and y coords
        distances.update([(key,((dictionary.get(key)[0][0] - point[0]) ** 2 + (dictionary.get(key)[0][1] - point[1])**2) ** 0.5)])

    temp = []
    temp.append(list(distances.values()))
    sortedDistances = np.sort(temp)[0][1:n_Closest_Points+1]

    for i in range(len(sortedDistances)):
        for key in distances:
            value = distances.get(key)
            if value == sortedDistances[i]:
                sortedArray.append([key,value])

    return sortedArray

#Selects one random id from ID_One as the point from which the five closest pixels are calculated from
Point = str(random.sample(ID_One,1)[0])

#Creates an array of the sorted distances from Point with the id attached to each distance
sortedArray = findDistances(var.get(Point)[0],var)

#from sortedArray, find the pixel position of that id from var and append it to closestPoints in order of 
#closest to farthest 

for i in range(len(sortedArray)):
    for key in var:
        value = var.get(key)[0]
        if key == sortedArray[i][0]:
            closestPoints.append([key,value])
#print("Closest Points: ",closestPoints,"\n")


# shows the image with the colored in pixels
#FRAME_ONE.show(FRAME_ONE.upScale(scaleFactor,imageFrame))
cv.waitKey(0)
# draws a line from Point to the closest five pixels, with the closest pixel being drawn to in green
for i in range(len(closestPoints)):
    #FRAME_ONE.show(FRAME_ONE.upScale(1,imageFrame),delay=1)
    if str(kb.read_event()) == 'KeyboardEvent(esc up)':
        break
    lineColor = []
    if i > 0:
        lineColor = [0,0,250]
        #print(closestPoints[i][1])
    else:
        #print("Closest point: ",closestPoints[i][1])
        lineColor = [0,250,0]         
    cv.line(
    img = imageFrame,
    pt1 = [var.get(Point)[0][1],var.get(Point)[0][0]],
    pt2 = [closestPoints[i][1][1],closestPoints[i][1][0]],
    color = lineColor,
    thickness = 1
    )
    FRAME_ONE.show(FRAME_ONE.upScale(1,imageFrame),delay=250)
    
    


    
    
    
    
        
    
        



#numPixels = 0
#for i in range(0,127):
#    for j in range(0,127):
#        if ((imageFrame[i,j][0]) != [0] or (imageFrame[i,j][2] != [0])):
#            numPixels += 1
#print(numPixels)



