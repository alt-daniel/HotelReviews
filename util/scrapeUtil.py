import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sys
sys.path.append('../')

from config import BASE_URL, HOTEL_URL

#  Return urls for hotels to scrape
def get_requested_url(hotelUrl):
    page = requests.get(hotelUrl)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        eu_body = soup.find('div', class_="lp-hotel__explore_world_continent", id="continent-content-EU")
        eu_onordered_list = 
        print(eu_body)


if __name__ == '__main__':
    get_requested_url(HOTEL_URL)
