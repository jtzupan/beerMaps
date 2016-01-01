# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 10:58:51 2015

@author: tzupan
"""

import googleGeoAPI.googleAPI
import geoCodingBeer.getHTML
import geoCodingBeer.getDataSet

def mainFunction():
    url = geoCodingBeer.getHTML('')

    listOfLocations = geoCodingBeer.getData(url)

    locationsWithCoords = []

    for i in listOfLocations:
        infoWithCoords = googleGeoAPI.googleAPI(i, 1)
        locationsWithCoords.append(infoWithCoords)
    
    return locationsWithCoords