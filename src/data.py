import os
import pandas as pd
from countries import country_codes

def load_data() ->list:
    # Find raw_country data
    directory = None
    for root, dirs, files in os.walk('.'):
        if "raw_country_data" in dirs:
            directory = os.path.join(root, "raw_country_data")
            break
    
    if directory is None:
        print("Directory 'raw_country_data' not found.")
        return None
    
    files = os.listdir(directory)

    if len(files) == 0:
        print("No files found in 'raw_country_data' directory")

    dfs = [] # list to store the dataframes

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        df = pd.read_csv(file_path)
        dfs.append(df)

    return dfs

def save_processed_data(processed_dfs):
    if not os.path.exists("cleaned_port_data"):
        os.makedirs("cleaned_port_data")

    for processed_df in processed_dfs:
        country_code = processed_df["Country_code"].iloc[0]
        country = country_codes.get(country_code, "Unknown")
        filename = f"cleaned_port_data/{country_code}_{country}.csv"
        processed_df.to_csv(filename, index=False)