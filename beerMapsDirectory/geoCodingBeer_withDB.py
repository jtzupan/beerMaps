# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import sqlite3
from sqlite3 import OperationalError
from bs4 import BeautifulSoup


def getHTML(url):
    '''creates a beautiful soup object for url
    
    Args (URL):
        url for geolocation that will be mapped
    Returns (BS4_object):
        a beautiful soup object to be parsed
    '''
        
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html)
    return soup
    
    
def getDataSet(htmlInfo, tableName):
    
    get_data = htmlInfo.find_all('tr')
    
    #set up database where geodata will be stored
    conn = sqlite3.connect('beerGeoData.sqlite')
    cur = conn.cursor()
#    cur.execute('''DROP TABLE DetroitBeerLocations''')
#    select list of bars already table, if the table already exists
    cur.execute('''
                CREATE TABLE IF NOT EXISTS {} (
                ID              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name            VARCHAR(255),
                type            VARCHAR(100),                
                address         VARCHAR(255),
                averageRating   FLOAT,
                numOfReviews    INT,
                latitude        FLOAT,
                longitude       FLOAT
                )'''.format(tableName))



    #code for ratebeer         
    for link in get_data[1:]:
        #store name and store type
        try:
            barName = link.contents[0].contents[0].text
            barType = link.contents[0].contents[2].text
            if barType in ['Beer Store', 'Grocery Store']:
                continue
        except AttributeError:
            #print 'encountered NavigableString error'
            barName = 'Name not found'
            barType = 'Type not found'
            #address
        try:
            barAddress = link.contents[1].contents[1].text
        except AttributeError:
            barAddress = 'Address not found'
            
            #average rating
        try:
            averageRating = link.contents[2].text
            if averageRating == 'N/A':
                continue
        except AttributeError:
            #print 'encountered NavigableString error'
            averageRating = 0
            
        #number of raters
        try:
            numberOfReviews = link.contents[3].text
            if int(numberOfReviews) < 3:
                continue
        #          print 'new section'
        except AttributeError:
            numberOfReviews = 0
        

        cur.execute('''SELECT * FROM {} WHERE name = ?'''.format(tableName),(barName,))
        if cur.fetchall() != []:
            continue
   
        cur.execute('''INSERT INTO {} (name, type, address, averageRating, numOfReviews, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)'''.format(tableName),(barName, barType, barAddress, averageRating, numberOfReviews, 0, 0))
        conn.commit()

        #print link, barName, barType, barAddress, averageRating, numberOfReviews