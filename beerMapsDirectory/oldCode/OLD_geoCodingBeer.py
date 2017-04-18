# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
from bs4 import BeautifulSoup

def getHTML(url):
    response = urllib2.urlopen(url)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html)
    return soup
    
    
def getDataSet(htmlInfo):
    fullList = []    
    get_data = htmlInfo.find_all('tr')
            
    #code for ratebeer         
    for link in get_data:
        #store name and store type
        try:
            barName = link.contents[0].contents[0].text
            barType = link.contents[0].contents[2].text
            #print 'new section'
        except AttributeError:
            #print 'encountered NavigableString error'
            barName = 'Name not found'
            barType = 'Type not found'
        #address
        try:
            barAddress = link.contents[1].contents[1].text
#            print 'new section'
        except AttributeError:
            #print 'encountered NavigableString error'
            barAddress = 'Address not found'
        #average rating
        try:
            averageRating = link.contents[2].text
#            print 'new section'
        except AttributeError:
            #print 'encountered NavigableString error'
            averageRating = 0
        #number of raters
        try:
            numberOfReviews = link.contents[3].text
#            print 'new section'
        except AttributeError:
            #print 'encountered NavigableString error'
            numberOfReviews = 0
        
        #else: print 'NEW RESTAURANT'
        
        fullList.append((barName, barType, barAddress, averageRating, numberOfReviews))
        
    fullList.pop(0)
        
    
    #remove any locations that are listed as stores or do not have a rating
    finalList = [x for x in fullList if x[3] != 'N/A' and x[1] != 'Beer Store'
                and x[1] != 'Grocery Store' and int(x[4]) > 1]    
        
    return finalList
        
    