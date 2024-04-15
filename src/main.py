import pandas as pd
from process import PortCleaner
from scraper import scrape_and_save_tables
from data import load_data, save_processed_data
from tqdm import tqdm


def run_programme():

    # Load data

    dataframes = load_data()

    if dataframes is None:
        # if no raw data is found, scrape and save the tables
        scrape_and_save_tables()

        dataframes = load_data()

        
        if dataframes is None:
            print("No data available after scraping. Exiting")
            return

    # Process raw data
    processed_dfs = []
    progress_bar = tqdm(total=len(dataframes), desc="Processing Data")
    for df in dataframes:
        progress_bar.set_description(f"Processing Data - {len(processed_dfs)}/{len(dataframes)}")
        port_cleaner = PortCleaner(df)
        processed_df = port_cleaner.process_dataframe()
        processed_dfs.append(processed_df)
        progress_bar.update(1)
    
    progress_bar.close()
    
    save_processed_data(processed_dfs)

run_programme()