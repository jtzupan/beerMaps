# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:32:02 2016

@author: johnzupan
"""


from GPSCoords import haversineDistance

def createGrid(barCoords, NS_mile, EW_mile, gridSize):
    '''this function will create the grid of points surrounding the bar
    gridSize should be a float
    
    '''
    assert type(gridSize) == float
    
    NS_mile_denomination = (NS_mile / 10)
    EW_mile_denomination = (EW_mile / 10)
    
    GPSGridPoints = []
    
    for i in range(-1 * int(gridSize), int(gridSize) + 1):
        for j in range(-1 * int(gridSize), int(gridSize) + 1):
            #print i,j
            nPoint = (barCoords[0] + (NS_mile_denomination * i), barCoords[1] + (EW_mile_denomination * j))
            GPSGridPoints.append(nPoint)
           
    assert len(GPSGridPoints) == ((gridSize * 2) + 1) ** 2
    return GPSGridPoints
    
def scoreOfSingleBar(fullGrid, allOtherBarsCoords, barPercentileRankList):
    '''
    '''
    listOfPoints = []
    for point in fullGrid:
        totalScore = 0
        
        for i,bar in enumerate(allOtherBarsCoords):
            distToBar = haversineDistance(point, (bar[1], bar[2]))
            scoreChange = ((barPercentileRankList[i] / 100.0) ** 3) - ((distToBar) * .5)
            if scoreChange > 0:
                totalScore += scoreChange
        listOfPoints.append((point, totalScore))
    return listOfPoints
        
 #   42.25935940214366, -83.189738396824
        #42.4064448,-83.1026078