# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:01:42 2015

@author: tzupan
"""

import requests
import xml.etree.ElementTree as et
from collections import namedtuple


def googleAPI(address, state):
    '''
    this function uses the Google Geo API to append the GPS coordinates to 
    the address.
    informationTuple (): the address 
    state (str): the state of the address
    
    Returns:
    
    '''
    
    bar_coords = namedtuple('BarCoords', 'bar_address latitude longitude')
    
    urlBase = 'https://maps.googleapis.com/maps/api/geocode/xml?address='
    APIKey =  'AIzaSyBsNtXRijhCY6bap_U94KfuwGG15JrcApw'

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
    
    bar_info = bar_coords(address, latitude, longitude)
    return bar_info
