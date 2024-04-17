import os
import pandas as pd
from countries import country_codes


def load_data() -> list:
    # Find raw_country data
    directory = None
    for root, dirs, files in os.walk('.'):
        if "raw_country_data" in dirs:
            directory = os.path.join(root, "raw_country_data")
            break

    if directory is None:
        print("Directory 'raw_country_data' not found.")
        return []

    files = os.listdir(directory)

    if len(files) == 0:
        print("No files found in 'raw_country_data' directory")

    dfs = []  # list to store the dataframes

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        dfs.append(df)

    return dfs


def save_processed_data(processed_dfs):
    if not os.path.exists("cleaned_port_data"):
        os.makedirs("cleaned_port_data")

    for processed_df in processed_dfs:
        # Check if the processed DataFrame is not empty
        if not processed_df.empty:
            # Check if the 'Country_code' column exists in the DataFrame
            if 'Country_code' in processed_df.columns:
                # Check if there are any rows in the DataFrame
                if not processed_df.index.empty:
                    country_code = processed_df["Country_code"].iloc[0]
                    country = country_codes.get(country_code, "Unknown")
                    filename = f"cleaned_port_data/{country_code}_{country}.csv"
                    processed_df.to_csv(filename, index=False)
                else:
                    print("Warning: No rows in the processed DataFrame. Skipping saving data.")
            else:
                print("Warning: 'Country_code' column not found in the processed DataFrame. Skipping saving data.")
        else:
            print("Warning: processed DataFrame is empty. Skipping saving data.")



def check_flagfile():
    flag_file_path = "cleaned_port_data/processing_completed.flag"
    return os.path.exists(flag_file_path)


def create_flag_file():
    flag_file_path = "cleaned_port_data/processing_completed.flag"
    with open(flag_file_path, "w"):
        pass
