#this program reads a gcode file and checks for features that may cause problems
#it is intended to be used with the gcode generated by the slic3r program
#functions are explorations of different ways to analyze the gcode

import sys
import re
import matplotlib.pyplot as plt
import numpy as np

layerStartPositions = []
lines = []

#read the file

filename = sys.argv[1]
f = open(filename, 'r')
lines = f.readlines()
print('Read ' , len(lines) , 'lines.\n')
f.close()


#each time the text "LAYER_CHANGE" is found, the layer number is incremented
def countLayers(lines):
    layer = 0
    lineCount = 0
    for line in lines:
        lineCount += 1
        if line.find(';LAYER_CHANGE') != -1:
            layer += 1
            layerStartPositions.append(lineCount)
    return layer

#getLayerLines returns a list of lines for a given layer
def getLayerLines(layerNumber):
    layerLines = []
    if layerNumber == 1:
        for i in range(layerStartPositions[layerNumber-1]):
            layerLines.append(lines[i])
    else:
        for i in range(layerStartPositions[layerNumber-2], layerStartPositions[layerNumber-1]):
            layerLines.append(lines[i])
    return layerLines

#use layerLines to print the number of lines in each layer
def printLayerLines(lines):
    for i in range(1, countLayers(lines)+1):
        print("Layer " , i , " has " , len(getLayerLines(i)) , " lines.")

#this function plots a list of the number of lines in each layer
def plotLayerLines():
    layerLines = []
    for i in range(1, countLayers(lines)+1):
        layerLines.append(len(getLayerLines(i)))
    plt.plot(layerLines)
    #caption the plot:
    plt.title('Number of lines in each layer')
    #plt.show()
    #save the plot as a png file named after the gcode file
    plt.savefig(filename + '.png')

def plotLayers3D():
    xycords = []
    for i in range(1, countLayers(lines)+1):
        for line in getLayerLines(i):
            if line.find('G1') != -1:
                #extract the x, y, and z values from the line and append to x, y, and z
                #print("found a G1 line", line)
                #split the line into a list of words
                words = line.split()
                x = 0
                y = 0
                #identify x and y coordinates and append to xycords
                for word in words:
                    if word.find('X') != -1:
                        x = float(word[1:])
                    if word.find('Y') != -1:
                        y = float(word[1:])
                xycords.append([x,y])
    print(xycords)
    #plot the x and y coordinates
    x = []
    y = []
    for i in range(len(xycords)):
        x.append(xycords[i][0])
        y.append(xycords[i][1])
    #clear the plot
    plt.clf()
    plt.title('some sort of plot')
    plt.plot(x,y)
    plt.savefig(filename + '2.png')


def main():

    print("There are " , countLayers(lines) , " layers.")
    #printLayerLines(lines)
    plotLayerLines()
    plotLayers3D()

main()