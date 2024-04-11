import pandas as pd

def load_data() ->pd.DataFrame:
    df = pd.read_csv("../src/raw_country_data/no_norway.csv")
    return df

def save_processed_data():
    pass