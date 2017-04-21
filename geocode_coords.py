# -*- coding: utf-8 -*-
"""

"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from collections import namedtuple
import time
import random


def geocode_address(address, state=None):
    '''
    this function uses the Google Geo API to append the GPS coordinates to 
    the address.
    address (str): the address 
    state (str): the state of the address
    
    Returns:
    
    '''
    
    bar_coords = namedtuple('BarCoords', 'bar_address latitude longitude')
    
    geolocator = Nominatim()
    try:
        geocoordinate = geolocator.geocode(address)
    except GeocoderServiceError:
        time.sleep(random.randint(0,7))
        geocoordinate = geolocator.geocode(address)
    
    try:
        latitude = geocoordinate[1][0]
        longitude = geocoordinate[1][1]
    except:
        latitude = 'No latitude info'
        longitude = 'No longitude info'
    
    bar_info = bar_coords(address, latitude, longitude)
        
    return bar_info