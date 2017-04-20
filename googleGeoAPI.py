# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:01:42 2015

@author: tzupan
"""

import requests
import xml.etree.ElementTree as et


def googleAPI(addressTuple, state):
    '''
    this function uses the Google Geo API to append the GPS coordinates to 
    the address.
    informationTuple (): the address 
    state (str): the state of the address
    
    Returns:
    
    '''
    
    urlBase = 'https://maps.googleapis.com/maps/api/geocode/xml?address='
    APIKey =  'AIzaSyBsNtXRijhCY6bap_U94KfuwGG15JrcApw'
    
    address = addressTuple
    
    address = address.replace(' ', '+')
    address += ',+'+state+'&key='
    
    finalURL = urlBase + address + APIKey
    
    try:
        with requests.Session() as s:
            html = s.get(finalURL)
        tree = et.fromstring(html.text) 

    except: 
        pass
 
    try:
        for e in tree.findall('./result/geometry/location/lat'):
            latitude = e.text
        for e in tree.findall('./result/geometry/location/lng'):
            longitude = e.text
    except:
        latitude = 'no info'
        longitude = 'no info'
        
    return addressTuple, (float(latitude), float(longitude))
