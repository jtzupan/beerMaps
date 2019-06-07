

import argparse
import os
import pandas as pd
import scipy.stats as stats
from sklearn.preprocessing import MinMaxScaler

import geocoordinate_helpers
import map_helpers
import web_scraper
import sqlite_helpers


# # variables that will need to be replaced by argparse
# rate_beer_url = 'https://www.ratebeer.com/places/regions/cleveland-elyria-mentor/1680/35/'
# table_name = 'clevelandBeer'
# state = 'oh'
# city = 'Cleveland'
# max_distance = 10.0

################################################################
# command line arguments

parser = argparse.ArgumentParser(description='Create a beer map in a few easy steps')

parser.add_argument('-u', action='store', dest='rate_beer_url',
                    default='https://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/',
                    help='ratebeer.com url')

parser.add_argument('-t', action='store', dest='table_name',
                    default='detroitBeer',
                    help='table name')

parser.add_argument('-s', action='store', dest='state',
                    default='mi',
                    help='State name')

parser.add_argument('-c', action='store', dest='city',
                    default='Detroit',
                    help='City name')

parser.add_argument('-m', action='store', dest='max_distance',
                    default=10.0,
                    help='Max distance of search grid')

results = parser.parse_args()


rate_beer_url = results.rate_beer_url
table_name = results.table_name
state = results.state
city = results.city
max_distance = results.max_distance
################################################################


df_name = city + '_df.pkl'
df_path = os.path.join('results', df_name)
bar_df_name = city + '_bar_info.pkl'
bar_df_path = os.path.join('results', bar_df_name)

if not os.path.isfile(df_path):
    print('Dataframe not found.  Executing script.\n')

    # create soup object by passing raw url
    soup_result_set = web_scraper.get_soup_object(rate_beer_url)

    # if table does not exist, create it
    sqlite_helpers.create_table(table_name)

    # parses the formatted string and puts the info into a database
    sqlite_helpers.insert_records(soup_result_set, table_name)

    # add latitude and longitude to table
    sqlite_helpers.add_geo_coordinates(table_name, state)

    # return lat/long and other data for all records in the table
    # where the latitude is not "no info"
    location_full_info = sqlite_helpers.get_locations_list(table_name)

    # find the lat long of the city
    # will be used to trim any locations greater than x distance from city center
    city_centroid = geocoordinate_helpers.get_city_centroid(city, state)

    # returns the list of locations within max_distance of city center
    trimmed_location_list = geocoordinate_helpers.trim_points(location_full_info, city_centroid, max_distance)

    # write the locations to a pandas df
    # these points will be added to the heatmap 
    bar_df_name = city + '_bar_info.pkl'
    bar_df = pd.DataFrame(trimmed_location_list,
                            columns=['score','lat', 'lon', 'name', 'address'])
    bar_df.to_pickle(bar_df_path)

    # creates a list with the average score of all bars
    location_rating_list = [location_tuple[0] for location_tuple in trimmed_location_list 
                                            if type(location_tuple[0]) == float]


    percentile_rank_list = [stats.percentileofscore(location_rating_list, single_location)
                             for single_location in location_rating_list]

    # find the change in lat/long that corresponds to one mile
    # this will be used to create the grid which will be the base of the map
    north_south_mile = geocoordinate_helpers.find_one_mile(city_centroid, direction='north_south')
    east_west_mile = geocoordinate_helpers.find_one_mile(city_centroid, direction='east_west')

    # empty grid
    empty_grid = geocoordinate_helpers. create_empty_grid(city_centroid)

    # fill grid based on scoring formula
    scored_grid = geocoordinate_helpers. create_score_grid(empty_grid, trimmed_location_list, percentile_rank_list)

    scores_df = pd.DataFrame(scored_grid, columns=['Coords', 'Score'])
    scores_df['latitude'] = scores_df['Coords'].apply(lambda a: a[0])
    scores_df['longitude'] = scores_df['Coords'].apply(lambda a: a[1])

    scaler = MinMaxScaler()
    scores_df['Score_scaled'] = scaler.fit_transform(scores_df['Score'].values.reshape(-1,1))

    df_name = city + '_df.pkl'
    scores_df.to_pickle(os.path.join('results', df_name))

else:
    city_centroid = geocoordinate_helpers.get_city_centroid(city, state)


print('Generating map.\n')

scores_df = pd.read_pickle(df_path)
locations_df = pd.read_pickle(bar_df_path)

# create the map
map_helpers.create_map(scores_df, locations_df, city_centroid, city)
