import requests
import sqlite3
from bs4 import BeautifulSoup


def get_soup_object(url: str):
    '''creates a beautiful soup object for url

    Args:
        url (str): ratebeer url for specified region
            example url: http://www.ratebeer.com/places/regions/detroit-warren-livonia/2160/22/
    Returns:
         bs4.BeautifulSoup.ResultSet : a BeautifulSoup object created from the url
    '''

    with requests.Session() as s:
        html = s.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup.find_all('tr')
