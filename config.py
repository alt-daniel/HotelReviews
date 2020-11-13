import os

BASE_URL = "https://www.booking.com"
HOTEL_URL = "https://www.booking.com/hotel/index.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaKkBiAEBmAEJuAEHyAEM2AED6AEBiAIBqAIDuALD-er8BcACAdICJDg3NWI5YmI4LTdmN2YtNGIyNC1hMmI5LTExMjgyMTA5MmRmNtgCBOACAQ;sid=a3d850b2621de6ff2e3e9ca9e14f9401"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")

# Csv paths
CITIES_URL_CSV_PATH = os.path.join(STATIC_DIR, "csv/city_urls.csv")
HOTELS_URL_CSV_PATH = os.path.join(STATIC_DIR, "csv/hotel_urls.csv") 
SCRAPED_RAW_REVIEWS_PATH = os.path.join(STATIC_DIR, "csv/raw_reviews.csv") 

# Pickle paths
CITIES_URL_PICKLE_PATH_ = os.path.join(STATIC_DIR, "csv/city_urls.csv")
HOTELS_URL_PICKLE_PATH = os.path.join(STATIC_DIR, "csv/hotel_urls.csv") 
SCRAPED_RAW_REVIEWS_PICKLE = os.path.join(STATIC_DIR, "pickle/raw_reviews.csv") 