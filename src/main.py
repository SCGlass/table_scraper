import pandas as pd
from process import PortCleaner
from scraper import scrape_and_save_tables
from data import load_data, save_processed_data, check_flagfile, create_flag_file
from tqdm import tqdm
from countries import country_codes


def run_programme():

    if check_flagfile():
        print("Data processing has already been complete. Ending process")
        return

    dataframes = load_data()

    if not dataframes:
        user_input = input("Raw data does not exist. Do you wish to download? (y/n)")
        if user_input == "y":
            scrape_and_save_tables(country_codes)
            # Load the data again after downloading
            dataframes = load_data()
            if not dataframes:
                print("No data available after scraping. Exiting")
                return
        elif user_input != "n":
            print("Invalid input. Exiting program.")
            return
        else:
            print("Exiting program.")
            return

    user_input2 = input("Do you wish to process the raw data? (y/n)")
    if user_input2 == "y":
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

        create_flag_file()
        print("Processing data is complete")
    else: 
        print("Exiting programme")

run_programme()