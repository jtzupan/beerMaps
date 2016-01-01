# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:41:56 2015

@author: tzupan
"""

import numpy as np
from math import radians, sin, cos, sqrt, asin

def findCentroid(listOfCoords):
    return np.mean(listOfCoords, axis = 0)
    
    
def haversineDistance(coord1, coord2):
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