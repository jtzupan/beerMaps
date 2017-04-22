# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:41:56 2015

@author: tzupan
"""

import numpy as np
from math import radians, sin, cos, sqrt, asin

def createCoordsArray(listOflocations):
    '''
    '''
    iterLength = len(listOflocations)
    listOfCoords = np.zeros((iterLength, 2))    
    
    for i in range(iterLength):
        listOfCoords[i][0] = listOflocations[i][1][0]
        listOfCoords[i][1] = listOflocations[i][1][1]
    
    return listOfCoords

# findCentroid may not be needed now that we are using the GPS coords of the 
# city as the map_center
def findCentroid(listOfCoords):
    '''
    '''
    return np.mean(listOfCoords, axis = 0)
    
    
def haversineDistance(coord1, coord2):
    '''
    '''
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    
    
    #radius of the earth in kilometers
    R = 6372.8
    
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    
    a = sin(dLat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2.0) ** 2
    c = 2 * asin(sqrt(a))
    
    return R * c * 0.6214
    
def findOneMile(coord1):
    '''finds the GPS distance for 1 mile North-South and 1 mile East-West
    
    '''
    #first coords are north south
    adjustedNSCoord = (coord1[0] + 1, coord1[1])
    NS_mile = 1 / haversineDistance(coord1, adjustedNSCoord)

    #second coords are east/west dist
    adjustedEWCoord = (coord1[0], coord1[1] + 1)
    EW_mile = 1 / haversineDistance(coord1, adjustedEWCoord)
    
    return NS_mile, EW_mile
    

def trimPoints(fullList, map_center):

    return [x for x in fullList if haversineDistance(np.array((x[1], x[2])), map_center) < 10.0]
    
    
    
    