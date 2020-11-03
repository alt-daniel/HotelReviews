from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.append('../')
from config import HOTELS_URL_CSV_PATH, BASE_URL, SCRAPED_RAW_REVIEWS_PATH
import time
import pandas as pd


reviews = []
# test url
# url = 'https://www.booking.com/hotel/nl/bij-paul-in-almere.en-gb.html?label=gen173nr-1DCAMoUDi1AkgJWARoqQGIAQGYAQm4AQfIAQzYAQPoAQH4AQKIAgGoAgO4Apy9-vwFwAIB0gIkNjAzZWNjYTItYWVjNC00YmUxLThjMzMtMGQzNWUxNjdiZDI52AIE4AIB;sid=a3d850b2621de6ff2e3e9ca9e14f9401;dest_id=-2140394;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=6;hpos=6;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=price;srepoch=1604324700;srpvid=22a060adef020180;type=total;ucfs=1&#hotelTmpl'

data = pd.read_csv(HOTELS_URL_CSV_PATH, index_col=0)

driver = webdriver.Chrome(ChromeDriverManager().install())

# accept cookies once
driver.get(BASE_URL)
cookie_btn = driver.find_element_by_css_selector('#onetrust-accept-btn-handler')
if cookie_btn:
    cookie_btn.click()

for url, hotel_name in zip(data.url, data.hotel_name):
    driver.get(BASE_URL+url)

    # Accept cookies
    next_review_btn = None
    review_button = driver.find_element_by_id('show_reviews_tab')
    review_button.click()
    time.sleep(2.0)

    # english_review_button = driver.find

    soup2 = BeautifulSoup(driver.page_source, 'html.parser')

    review_container = soup2.find('div', id='review_list_page_container')
    next_page = review_container.find('div', class_='bui-pagination__prev_arrow')
    next_pagelink = soup2.find('div', class_='bui-pagination__item bui-pagination__prev_arrow')
    # review_elements = review_container.find_all('li', class_='review_list_new_item_block')
    review_elements = []

    next_review_container = review_container.find('div', class_='bui-pagination__next-arrow')
    if next_review_container:
        next_review_btn = next_review_container.find('a', class_='pagenext') 

    counter = 0

    # Max 5 pages of reviews
    while True and counter <5:
        time.sleep(1.0)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        review_container = soup2.find('div', id='review_list_page_container')
        review_elements += review_container.find_all('li', class_='review_list_new_item_block')
       
        try:
            next_arrow = driver.find_element_by_class_name('bui-pagination__next-arrow')
            next_arrow.click()
            if 'bui-pagination__item--disabled' in next_arrow.get_attribute('class'):
                break
        except NoSuchElementException:
            pass
        counter += 1


    for review in review_elements:

        nation= review.find('span', class_='bui-avatar-block__subtitle')
        score= review.find('div', class_='bui-review-score__badge')
        title = review.find('h3', class_='c-review-block__title')
        positive_review = review.find('span', class_='c-review__body')
        negative_review = review.find('div', class_='lalala')

        if nation:
            nation = nation.get_text()
        else:
            nation = ""

        if score:
            score = score.get_text()
        else:
            score = ""

        if title:
            title = title.get_text()
        else:
            title = "" 

        if positive_review:
            positive_review = positive_review.get_text()
        else:
            positive_review = ""
        
        if negative_review:
            negative_review = negative_review.find('span', class_='c-review__body').get_text()
        else:
            negative_review = ""

        scrape = [hotel_name, nation, score, title, positive_review, negative_review]
        reviews.append(scrape)

import pandas as pd
df = pd.DataFrame(reviews)
df.columns = ['hotel_name','nation', 'score', 'title', 'positive_review', 'negative_review']

if not df.empty:
    df.to_csv("raw_reviews.csv", header=True)

driver.quit()