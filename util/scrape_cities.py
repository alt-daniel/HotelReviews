import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sys
sys.path.append('../')

from config import BASE_URL, HOTEL_URL, CITIES_URL_CSV_PATH

#  Return urls for hotels to scrape
page = requests.get(HOTEL_URL)

if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')

    # Most popular cities from Europe
    eu_body = soup.find('div', class_='lp-hotel__explore_world_continent', id="continent-content-EU")
    eu_unordered_list = eu_body.find('ul', class_='lp-hotel__explore_world_city')
    eu_items = eu_unordered_list.find_all('li', class_='bui-list__item')
    eu_hrefs = [ eu_item.find('a', href=True) for eu_item in eu_items] 
    eu_urls = [item['href'] for item in eu_hrefs] ## all urls in list

    urls = pd.DataFrame({"url": eu_urls})
    if not urls.empty:
        urls.to_csv(CITIES_URL_CSV_PATH, header=True)



if __name__ == '__main__':
    get_requested_url(HOTEL_URL)
