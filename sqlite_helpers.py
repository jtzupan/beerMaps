
from bs4 import BeautifulSoup
import sqlite3
import tqdm

import geocoordinate_helpers


def create_table(table_name: str):
    '''creates the sqllite table if it does not already exist

    Args:
        table_name (str): what the sqllite table will be called

    Returns:
        None
    '''

    # set up database where geodata will be stored
    conn = sqlite3.connect('beerGeoData.sqlite')
    with conn:
        cur = conn.cursor()
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
                    )'''.format(table_name))
        conn.commit()


def insert_records(bar_info, table_name: str):
    '''parses the BeautifulSoup object and saves the results to the SQLlite table.
        There is one entry for each location, missing values are filled

    Args:
        bar_info (BeautifulSoup.ResultSet): the BeautifulSoup object containing region's bars information
        table_name (str): sqllite table to insert results into

    Returns:
        None

    '''

    conn = sqlite3.connect('beerGeoData.sqlite')
    cur = conn.cursor()

    # iterate through parsed BeautifulSoup object collecting the name, address,
    #   rating, and number of reviews
    for link in bar_info[1:]:
        try:
            bar_name = link.contents[0].contents[0].text
            bar_type = link.contents[0].contents[2].text
            if bar_type in ['Beer Store', 'Grocery Store', 'Homebrew Shop']:
                continue
        except AttributeError:
            bar_name = 'Name not found'
            bar_type = 'Type not found'

        try:
            bar_address = link.contents[1].contents[1].text
        except AttributeError:
            bar_address = 'Address not found'

        try:
            average_rating = link.contents[2].text
            if average_rating == 'N/A':
                continue
        except AttributeError:
            average_rating = 0

        try:
            number_of_reviews = link.contents[3].text
            if int(number_of_reviews) < 3:
                continue
        except AttributeError:
            number_of_reviews = 0

        cur.execute('''SELECT * FROM {} WHERE name = ?'''.format(table_name),(bar_name,))
        if cur.fetchall() != []:
            continue

        cur.execute('''INSERT INTO {} (name, type, address, averageRating, numOfReviews, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)'''.format(table_name), (bar_name, bar_type, bar_address, average_rating, number_of_reviews, 0, 0))
        conn.commit()
    conn.close()


def add_geo_coordinates(table_name: str, state: str):
    '''uses googleGeoAPI to get lat/long for each bar.
        If an address already has non-zero lat and long, the API call is not made

    Args:
        table_name (str): sqllite table to insert results into
        state (str): the state of the city

    Returns:
        None

    '''

    conn = sqlite3.connect('beerGeoData.sqlite')
    with conn:
        cur = conn.cursor()
        cur.execute('''SELECT ID, address FROM {}
                        WHERE latitude = 0
                        OR longitude = 0
                        OR latitude = "no info"
                        OR longitude = "no info"'''.format(table_name))

        # get list of all beer locations from table
        list_of_locations = cur.fetchall()
        for id_address_tuple in tqdm.tqdm(list_of_locations):
            bar_id, bar_address = id_address_tuple[0], id_address_tuple[1]
            bar_coordinates = geocoordinate_helpers.get_lat_long(bar_address, state)

            cur.execute('''UPDATE {} SET latitude = ?,
                            longitude = ?
                            WHERE ID = ?'''.format(table_name), (bar_coordinates.latitude, bar_coordinates.longitude, bar_id))

            conn.commit()


def get_locations_list(table_name):
    conn = sqlite3.connect('beerGeoData.sqlite')
    with conn:
        cur = conn.cursor()
        cur.execute('''SELECT averageRating, latitude, longitude, name, address FROM {}
                    WHERE latitude <> "no info"'''.format(table_name))
        location_list = cur.fetchall()
    return location_list
