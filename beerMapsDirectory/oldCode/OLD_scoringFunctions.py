# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 20:39:41 2016

@author: johnzupan
"""

from GPSCoords import haversineDistance

def createGrid(barCoords, NS_mile, EW_mile, gridSize):
    '''this function will create the grid of points surrounding the bar
    gridSize should be a float
    
    '''
    assert type(gridSize) == float
    
    NS_mile_denomination = (NS_mile / 2) / gridSize
    EW_mile_denomination = (EW_mile / 2) /gridSize
    
    GPSGridPoints = []
    
    for i in range(-1 * int(gridSize), int(gridSize) + 1):
        for j in range(-1 * int(gridSize), int(gridSize) + 1):
            #print i,j
            nPoint = (barCoords[0] + (NS_mile_denomination * i), barCoords[1] + (EW_mile_denomination * j))
            GPSGridPoints.append(nPoint)
           
    assert len(GPSGridPoints) == ((gridSize * 2) + 1) ** 2
    return GPSGridPoints
    
def scoreOfSingleBar(barCoordsGrid, allOtherBarsCoords, barPercentileRank):
    '''
    '''
    listOfPoints = []
    for point in barCoordsGrid:
        totalScore = ((barPercentileRank/100) ** 3)
        for bar in allOtherBarsCoords:
            distToBar = haversineDistance(point, (bar[1], bar[2]))
            totalScore -= distToBar * 100
        listOfPoints.append((point, totalScore))
    return listOfPoints
        
    