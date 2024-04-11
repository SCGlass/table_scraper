import pandas as pd
#from process import PortCleaner
#from scraper import scrape_and_save_tables
#from countries import country_codes

def load_data() ->pd.DataFrame:
    df = pd.read_csv("../src/raw_country_data/no_norway.csv")
    return df

def save_processed_data():
    pass