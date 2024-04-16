from process import PortCleaner
from scraper import scrape_and_save_tables
from data import load_data, save_processed_data
from data import check_flagfile, create_flag_file
from tqdm import tqdm
from countries import country_codes


def run_programme():

    if check_flagfile():
        print("Data processing has already been complete. Ending process")
        return

    dfs = load_data()

    if not dfs:
        user_input = input("Raw data n/a. Do you wish to download? (y/n)")
        if user_input == "y":
            scrape_and_save_tables(country_codes)
            # Load the data again after downloading
            dfs = load_data()
            if not dfs:
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
        proc_dfs = []
        prog_bar = tqdm(total=len(dfs), desc="Processing Data")
        for df in dfs:
            prog_bar.set_description(f"Processing: {len(proc_dfs)}/{len(dfs)}")
            port_cleaner = PortCleaner(df)
            processed_df = port_cleaner.process_dataframe()
            proc_dfs.append(processed_df)
            prog_bar.update(1)

        prog_bar.close()

        save_processed_data(proc_dfs)

        create_flag_file()
        print("Processing data is complete")
    else:
        print("Exiting programme")


run_programme()
