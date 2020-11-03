import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sys
sys.path.append('../')

from config import BASE_URL, HOTEL_URL, CITIES_URL_CSV_PATH, HOTELS_URL_CSV_PATH

#  Return urls for hotels to scrape
data = pd.read_csv(CITIES_URL_CSV_PATH, index_col=0)

page_example = data.iloc[0][0]
hotel_names = []
hotel_urls = []
urls = []
hotel_average_scores = []

for url in data['url']:
    page = requests.get(BASE_URL+url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        hotel_card_elements = soup.find_all('div', class_='sr__card js-sr-card')
        hotel_card_content = [item.find('div', class_='sr__card_content') for item in hotel_card_elements]
        hotel_name_elements = [item.find('span', class_='bui-card__title') for item in hotel_card_content ]
        hotel_url_elements = [item.find('a', href=True) for item in hotel_card_content]
        hotel_average_score_elements = [item.find('div', class_='bui-review-score__badge') for item in hotel_card_content]

        hotel_names += [item.get_text() for item in hotel_name_elements]
        hotel_average_scores += [item.get_text() for item in hotel_average_score_elements]
        hotel_urls += [item['href'] for item in hotel_url_elements]

df = pd.DataFrame({
    "hotel_name": hotel_names,
    "average_score": hotel_average_scores,
    "url": hotel_urls
})

if not df.empty:
    df.to_csv(HOTELS_URL_CSV_PATH, header=True)


