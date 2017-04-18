# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:01:42 2015

@author: tzupan
"""

import urllib2
import xml.etree.ElementTree as et


def googleAPI(informationTuple, state):
    '''
    this function uses the Google Geo API to append the GPS coordinates to 
    the address.
    informationTuple (): the address 
    state (str): the state of the address
    
    Returns:
    
    '''
#    urlBase = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    urlBase = 'https://maps.googleapis.com/maps/api/geocode/xml?address='
    APIKey =  'AIzaSyBsNtXRijhCY6bap_U94KfuwGG15JrcApw'
    
    #address = str(informationTuple[2])
    address = informationTuple
    
    address = address.replace(' ', '+')
    address += ',+'+state+'&key='
    
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
        
    return informationTuple, (float(latitude), float(longitude))
