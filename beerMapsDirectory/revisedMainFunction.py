# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:52:50 2016

@author: johnzupan
"""

import googleGeoAPI
import geoCodingBeer_withDB
import GPSCoords
import revisedScoringFunction
import sqlite3
import scipy.stats as stats
import csv
reload(googleGeoAPI)
reload(geoCodingBeer_withDB)
reload(GPSCoords)
reload(revisedScoringFunction)

def buildMainList(targetURL, state, tableName):
    '''Creates list with geographic information
    targetURL: url from ratebeer.com
    state: two letter state code 
    tableName: destination table name ie 'SDBeer'
    '''
#    #gets a BeautifulSoup formatted string
#    targetURL = 'http://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/'
    url = geoCodingBeer_withDB.getHTML(targetURL)
    #parses the formatted string and puts the info into a database
    geoCodingBeer_withDB.getDataSet(url, tableName)

    conn = sqlite3.connect('beerGeoData.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT ID, address FROM {}'''.format(tableName))
    listOfLocations = cur.fetchall()
    for i in listOfLocations:
        ID = i[0]
        print ID, i[1] 
        
        #if record already exists in table with updated GPS coordinates
        # skip record.  Saves calls to Google API
        cur.execute('''SELECT latitude, longitude FROM {} 
                            WHERE id = (?)'''.format(tableName),(ID,))
        
        latitudeCheck = cur.fetchone()[0]                
        if latitudeCheck != 0.0:
            print 'Record already exists in table'
            continue

        bar, latlong = googleGeoAPI.googleAPI(i[1], state)
        latitude = latlong[0]
        longitude = latlong[1]
        cur.execute('''UPDATE {} SET latitude = ?,
                        longitude = ?
                        WHERE ID = ?'''.format(tableName), (latitude, longitude, ID))

        conn.commit()
        
    
    #limits the results to only bars within set number of miles from central location
    cur.execute('''SELECT averageRating, latitude, longitude, name, address FROM {}'''.format(tableName))
    coordsList = cur.fetchall()    
    
    centroidList = [(x[1], x[2]) for x in coordsList]
    centroid = GPSCoords.findCentroid(centroidList)
    
    #ENTER CUSTOM CENTROID HERE IF THE DATA IS DISPERSED ENOUGH
    #THAT YOU ARE NOT GETTING GOOD RESULTS
    #centroid = (32.8244637,-117.377787)
    trimmedCoordsList =  GPSCoords.trimPoints(coordsList, centroid)
    avgRatingList = [x[0] for x in trimmedCoordsList if type(x[0]) == float]    
    
    percentileRankList = [stats.percentileofscore(avgRatingList, x) for x in avgRatingList] 

    

    NS_mile, EW_mile = GPSCoords.findOneMile(centroid)

    barGrid = revisedScoringFunction.createGrid(centroid, NS_mile, EW_mile, 100.0)       
    finalScoreList = revisedScoringFunction.scoreOfSingleBar(barGrid, trimmedCoordsList, percentileRankList)
        
    return finalScoreList, centroid, trimmedCoordsList

################################################################################################
################################################################################################
################################################################################################

def writeToCSV(inputFile, outputFileName):
    '''
    '''
    inputFile.sort(key = lambda s: s[1])
    inputFile.reverse()
    maxIter = 1500
    f = open(outputFileName, 'wb')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Latitude', 'Longitude', 'Score') )
        for i in range(maxIter):
            
            writer.writerow( (inputFile[i][0][0], inputFile[i][0][1],inputFile[i][1]) )
    finally:
        f.close()


################################################################################################
################################################################################################
################################################################################################
import json
import codecs
#
#conn = sqlite3.connect('geodata.sqlite')
#cur = conn.cursor()
#
#cur.execute('SELECT * FROM Locations')


def writeJSON(inputFile, barList, centroid, outputFileName):
    finalFile = [x for x in inputFile if x[1]>0]
    numOfRecords = len(finalFile)   
    inputFile.sort(key = lambda s: s[1])
    inputFile.reverse()
    inputFile = inputFile[: numOfRecords]   

    
    fhand = codecs.open(outputFileName,'w', "utf-8")
#    write centroid object 
    centroidObject = "mycentroid = ["+str(centroid[0])+","+str(centroid[1])+"];\n"
    fhand.write(centroidObject)
    fhand.write("myData = [\n")
    for bar in barList:
        barLat = bar[1]
        barLng = bar[2]
        try:
            barInfo = ('NAME: ' + str(bar[3])+ ' ADDRESS: '+str(bar[4]))
        except UnicodeEncodeError:
            barInfo = 'No Information available'
        barDotType = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
        barCoords = "["+str(barLat)+","+str(barLng)+", '"+barDotType+"','"+str(barInfo)+"'],\n"
        fhand.write(barCoords)
    count = 0
    for row in finalFile :

        try:
            if count > 0:
                fhand.write(",\n")
            lat = row[0][0]
#            site.append(str(lat))
            lng = row[0][1]
#            site.append(str(lon))
            print lat, lng
            if count <= numOfRecords * 0.05:
                dotType = "https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0"
#                dotType = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
            elif count <= numOfRecords * 0.25:
                dotType = "https://storage.googleapis.com/support-kms-prod/SNP_2752264_en_v0"
            elif count <= numOfRecords * 0.5:
                dotType = "https://storage.googleapis.com/support-kms-prod/SNP_2752068_en_v0"
            elif count <= numOfRecords * 0.75:
                dotType = "https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0"
            else:
                dotType = "https://storage.googleapis.com/support-kms-prod/SNP_2752063_en_v0" 
            count += 1
            output = "["+str(lat)+","+str(lng)+", '"+dotType+"']"
            fhand.write(output)

            
        except: 
            continue
    
    fhand.write("\n];\n")
    #cur.close()
    fhand.close()
    print count, "records written to {}".format(outputFileName)
    print "Open where.html to view the data in a browser"


    