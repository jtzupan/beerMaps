# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 10:58:51 2015

@author: tzupan
"""
import numpy as np
import googleGeoAPI
import geoCodingBeer
reload(googleGeoAPI)
reload(geoCodingBeer)

def mainFunction():
    url = geoCodingBeer.getHTML('http://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/')

    listOfLocations = geoCodingBeer.getDataSet(url)

    locationsWithCoords = []

    for i in listOfLocations:
        infoWithCoords = googleGeoAPI.googleAPI(i, 1)
        locationsWithCoords.append(infoWithCoords)
    
    return locationsWithCoords