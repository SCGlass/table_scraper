import pandas as pd
from process import PortCleaner
from scraper import scrape_and_save_tables
import os
from countries import country_codes
from data import load_data, save_processed_data


def run_programme():

    # Load data
    dataframes = load_data()

    if dataframes is None:
        # if no raw data is found, scrape and save the tables
        scrape_and_save_tables()

        
        if dataframes is None:
            print("No data available after scraping. Exiting")
            return

    # Process raw data
    processed_dfs = []
    for df in dataframes:
        cleaner = PortCleaner()
        processed_df = cleaner.process_dataframe(df)
        processed_dfs.append(processed_df)
    
    save_processed_data(processed_dfs)

run_programme()