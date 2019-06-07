
import itertools
import numpy as np
import tqdm

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from collections import namedtuple


def get_lat_long(address: str, state: str, app_name: str = 'my_app'):
    '''hits google maps api to return lat and long of address

    Args:
        address (str): street address of location
        state (str): the state of the address

    Returns:
        (tuple): address
    '''

    bar_coords = namedtuple('BarCoords', 'bar_address latitude longitude')

    try:
        geolocator = Nominatim(user_agent=app_name)
        geo_data = geolocator.geocode(address + ' ' + state)
    except:
        pass

    try:
        latitude = geo_data.latitude
        longitude = geo_data.longitude
    except:
        latitude = 'no info'
        longitude = 'no info'

    bar_info = bar_coords(address, latitude, longitude)
    return bar_info


def get_city_centroid(city: str, state: str, app_name: str = 'my_app'):
    geolocator = Nominatim(user_agent=app_name)
    centroid_geo_data = geolocator.geocode(city + ' ' + state)
    city_centroid = (float(centroid_geo_data.latitude), float(centroid_geo_data.longitude))
    return city_centroid


def trim_points(list_of_locations: list, map_center: tuple, max_distance: float = 10.0):
    '''returns a list of points within max_distance of center point

    Args:
        list_of_locations (list):
        map_center (tuple):
        max_distance (float):

    Returns:
        list: 
    '''
    return [coordinate for coordinate in list_of_locations if
            geodesic((coordinate[1], coordinate[2]), map_center).miles < max_distance]


def find_one_mile(geocoordinate: tuple, direction: str = 'north_south'):
    '''
    '''
    if direction == 'north_south':
        adjusted_coordinate = (geocoordinate[0] + 1, geocoordinate[1])
        one_unit_distance = geodesic(geocoordinate, adjusted_coordinate).miles
        return 1 / one_unit_distance

    elif direction == 'east_west':
        adjusted_coordinate = (geocoordinate[0], geocoordinate[1] + 1)
        one_unit_distance = geodesic(geocoordinate, adjusted_coordinate).miles
        return 1 / one_unit_distance

    else:
        return -1


def create_empty_grid(city_centroid: tuple, height: int=10, width: int=10):
    '''
    '''
    # find miles in terms of longitude and latitude
    north_south_mile = find_one_mile(city_centroid, direction='north_south')
    east_west_mile = find_one_mile(city_centroid, direction='east_west')

    northernmost_coordinate = city_centroid[0] + ((height / 2.0) * north_south_mile)
    southernmost_coordinate = city_centroid[0] - ((height / 2.0) * north_south_mile)
    eastmost_coordinate = city_centroid[1] + ((width / 2.0) * east_west_mile)
    westmost_coordinate = city_centroid[1] - ((width / 2.0) * east_west_mile)

    north_south_coord_list = np.linspace(northernmost_coordinate, southernmost_coordinate, num=height*10)
    east_west_coord_list = np.linspace(westmost_coordinate, eastmost_coordinate, num=width*10)

    return list(itertools.product(north_south_coord_list, east_west_coord_list))


def create_score_grid(empty_grid, list_of_locations, location_percentile_scores):
    '''
    '''
    geocoordinate_score_list = list()

    print('Starting scoring\n')
    for point in tqdm.tqdm(empty_grid):
        point_total_score = 0
        for index, bar in enumerate(list_of_locations):
            miles_to_bar = geodesic(point, (bar[1], bar[2])).miles
            bar_score = ((location_percentile_scores[index] / 100.0) ** 3) - ((miles_to_bar) * .5)
            if bar_score > 0.0:
                point_total_score += bar_score
        if point_total_score > 0.0:
            geocoordinate_score_list.append((point, point_total_score))
    return geocoordinate_score_list
