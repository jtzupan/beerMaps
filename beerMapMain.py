# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:52:50 2016

@author: johnzupan
"""

import web_scrape_bar_data
import googleGeoAPI
import GPSCoords
import scoringFunction
import sqlite3
import scipy.stats as stats
import csv
import tqdm
import datetime


reload(googleGeoAPI)
reload(web_scrape_bar_data)
reload(GPSCoords)
reload(scoringFunction)


def buildMainList(targetURL, city, state, tableName):
    '''Creates list with geographic information
    targetURL: url from ratebeer.com
    state: two letter state code 
    tableName: destination table name ie 'SDBeer'
    '''
#    #gets a BeautifulSoup formatted string
#    targetURL = 'http://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/'
    
    
    url = web_scrape_bar_data.getHTML(targetURL)
    #parses the formatted string and puts the info into a database
    web_scrape_bar_data.getDataSet(url, tableName)

    conn = sqlite3.connect('beerGeoData.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT ID, address FROM {}'''.format(tableName))
    listOfLocations = cur.fetchall()
    for address in tqdm.tqdm(listOfLocations):
        ID = address[0]
        print ID, address[1] 
        
        #if record already exists in table with updated GPS coordinates
        # skip record.  Saves calls to Google API
        cur.execute('''SELECT latitude, longitude FROM {} 
                            WHERE id = (?)'''.format(tableName),(ID,))
        
        recordCheck = cur.fetchone()[0]                
        if recordCheck != 0.0:
            print 'Record already exists in table'
            continue
        
        bar_address = address[1]

        bar_info = googleGeoAPI.googleAPI(bar_address, state)

        cur.execute('''UPDATE {} SET latitude = ?,
                        longitude = ?
                        WHERE ID = ?'''.format(tableName), (bar_info.latitude, bar_info.longitude, ID))

        conn.commit()
        
#    limits the results to only bars within set number of miles from central location
    cur.execute('''SELECT averageRating, latitude, longitude, name, address FROM {}
                    WHERE latitude <> "no info"'''.format(tableName))
    coordsList = cur.fetchall()    
    
#    use the latitude and longitude of city for center approximation
    centroid_tuple = googleGeoAPI.googleAPI(city, state)
    centroid = (float(centroid_tuple.latitude), float(centroid_tuple.longitude))

#    finds all the bars that are within 10 miles of the centroid
#    then finds the average rating of each bar in the result set
    trimmedCoordsList =  GPSCoords.trimPoints(coordsList, centroid)
    avgRatingList = [x[0] for x in trimmedCoordsList if type(x[0]) == float]    
    
    percentileRankList = [stats.percentileofscore(avgRatingList, x) for x in avgRatingList] 

    
    NS_mile, EW_mile = GPSCoords.findOneMile(centroid)
    startTime = datetime.datetime.now()
    barGrid = scoringFunction.createGrid(centroid, NS_mile, EW_mile, 100.0)       
    finalScoreList = scoringFunction.scoreOfSingleBar(barGrid, trimmedCoordsList, percentileRankList)
    endTime = datetime.datetime.now()
    
    timediff = endTime - startTime
    print timediff
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

import codecs

# maybe load from db instead of passing lists



def writeJS(inputFile, barList, centroid, outputFileName):
    finalFile = [x for x in inputFile if x[1]>0]
    numOfRecords = len(finalFile)     
    finalFile.sort(key = lambda s: s[1])
    finalFile.reverse()

    
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


    