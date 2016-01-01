# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:01:42 2015

@author: tzupan
"""

#import sys
#import csv
import urllib2
import xml.etree.ElementTree as et
#csv.field_size_limit(sys.maxsize)


def googleAPI(informationTuple, APIType):
    '''
    fileType allows you to return JSON or XML
    '''
#    urlBase = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    urlBase = 'https://maps.googleapis.com/maps/api/geocode/xml?address='
    APIKey =  'AIzaSyBsNtXRijhCY6bap_U94KfuwGG15JrcApw'
    
    address = str(informationTuple[2])
    
    address = address.replace(' ', '+')
    address += ',+MI&key='
    
    finalURL = urlBase + address + APIKey
    #print finalURL
    
    try:
        tree = et.parse(urllib2.urlopen(finalURL)) 
        #print tree
    except: 
        #fw.writerow([line])
        pass
    try:
        for e in tree.findall('./result/geometry/location/lat'):
            latitude = e.text
        for e in tree.findall('./result/geometry/location/lng'):
            longitude = e.text
    except:
        latitude = 'no info'
        longitude = 'no info'
        
    return (informationTuple, (float(latitude), float(longitude)))
