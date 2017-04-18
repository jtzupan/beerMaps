# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 10:58:51 2015

@author: tzupan
"""
import numpy as np
import googleGeoAPI
import geoCodingBeer_withDB
import GPSCoords
import scoringFunctions
import sqlite3
import scipy.stats as stats
import csv
reload(googleGeoAPI)
reload(geoCodingBeer_withDB)
reload(GPSCoords)
reload(scoringFunctions)

def mainFunction():
#    #gets a BeautifulSoup formatted string
#    url = geoCodingBeer_withDB.getHTML('http://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/')
#    #parses the formatted string and puts the info into a database
#    geoCodingBeer_withDB.getDataSet(url)
#
    conn = sqlite3.connect('beerGeoData.sqlite')
    cur = conn.cursor()
#    cur.execute('''SELECT ID, address FROM beerLocations''')
#    listOfLocations = cur.fetchall()
#    for i in listOfLocations:
#        ID = i[0]
#        print ID, i[1] 
#        
#        #if record already exists in table with updated GPS coordinates
#        # skip record.  Saves calls to Google API
#        cur.execute('''SELECT latitude, longitude FROM beerLocations 
#                            WHERE id = (?)''',(ID,))
#        
#        latitudeCheck = cur.fetchone()[0]                
#        if latitudeCheck != 0.0:
#            print 'Record already exists in table'
#            continue
#
#        bar, latlong = googleGeoAPI.googleAPI(i[1], 1)
#        print bar, latlong[0], latlong[1]
#        latitude = latlong[0]
#        longitude = latlong[1]
#        cur.execute('''UPDATE beerLocations SET latitude = ?,
#                                                longitude = ?
#                                            WHERE ID = ?''', (latitude, longitude, ID))
#
#        conn.commit()
#        
    
    #limits the results to only bars within set number of miles from central location
    cur.execute('''SELECT averageRating, latitude, longitude FROM beerLocations''')
    coordsList = cur.fetchall()    
    trimmedCoordsList =  GPSCoords.trimPoints(coordsList)
    avgRatingList = [x[0] for x in trimmedCoordsList if type(x[0]) == float]    
    
    finalScoreList = []    
    
    for bar in trimmedCoordsList:
        currentLocation = (bar[1], bar[2])
        NS_mile, EW_mile = GPSCoords.findOneMile(currentLocation) # was bar
        #change the last argument in createGrid to get more/less grid points
        currentLocation = (bar[1], bar[2])
        barGrid = scoringFunctions.createGrid(currentLocation, NS_mile, EW_mile, 5.0)
        #return barGrid
        percentileRankOfBar = stats.percentileofscore(avgRatingList, bar[0])
        finalGrid = scoringFunctions.scoreOfSingleBar(barGrid, trimmedCoordsList, percentileRankOfBar)       
        finalScoreList.extend(finalGrid)
        
    return finalScoreList

def writeToCSV(inputFile, outputFileName):
    '''
    '''
    inputFile.sort(key = lambda s: s[1])
    inputFile.reverse()
    maxIter = min(1000, len(inputFile))
    print maxIter
    finalList = []
    for point1 in range(maxIter):
        newPoint = inputFile[point1]
        for point2 in range(maxIter):
            if point1 == point2:
                continue
            if GPSCoords.haversineDistance(inputFile[point1][0], inputFile[point2][0]) < 0.08:
                newCoord = ((inputFile[point1][0][0] + inputFile[point2][0][0]) / 2, (inputFile[point1][0][1] + inputFile[point2][0][1]) / 2)
                newScore = inputFile[point1][1] - inputFile[point2][1]               
                newPoint = (newCoord, newScore)
                break
        finalList.append(newPoint)
    #return finalList
    f = open(outputFileName, 'wb')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Latitude', 'Longitude', 'Score') )
        for i in range(maxIter):
            
            writer.writerow( (finalList[i][0][0], finalList[i][0][1], finalList[i][1]) )
            #writer.writerow( (inputFile[i][0][0], inputFile[i][0][1], inputFile[i][1]) )
    finally:
        f.close()
        
        
        finalList = []


    