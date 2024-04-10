from LatLon23 import LatLon
import re
import pandas as pd
from geopy.geocoders import Nominatim



df = pd.read_csv("../src/raw_country_data/no_norway.csv")

def parse_coordinate(coord_str):
    
    
    if coord_str:
        pattern = r'(\d{2})(\d{2})([NS])\s*(\d{3})(\d{2})([EW])'
        match = re.match(pattern, coord_str)
        if match:

            lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir = match.groups()
            lat = int(lat_deg) + int(lat_min) / 60 * (-1 if lat_dir == 'S' else 1)
            lon = int(lon_deg) + int(lon_min) / 60 * (-1 if lon_dir == 'W' else 1)
            
            # Use LatLon23 to convert decimal degrees
            latlon = LatLon(lat, lon)
            
            return latlon.lat.decimal_degree, latlon.lon.decimal_degree
        else:
            return None, None
    else:
        return None, None
    

def format_table(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows and set columns based on your existing logic
    df = df.drop(df.index[:3], inplace=False)
    df.columns = df.iloc[0]
    df = df.drop(3)
    
    # Filter rows where 'Function' column contains '1'
    df = df[df["Function"].str.contains("1")]
    
    # Reset index
    df.reset_index(drop=True, inplace=True)

    # Extract country code and location code from LOCODE column
    df[['country_code', 'location_code']] = df['LOCODE'].str.extract(r'^\s*(\S+)\s+(.*)$')
    
    # Removing columns that are not needed
    df = df[df.columns[~df.columns.isin(["Ch", "SubDiv", "Function", "Date", "Remarks", "IATA", "LOCODE"])]]

    # Reordering the columns
    country_code_col = df.pop('country_code')
    location_code_col = df.pop('location_code')
    df.insert(0, 'country_code', country_code_col)
    df.insert(1, 'location_code', location_code_col)

    # Extract latitude and longitude from 'Coordinates' column
    df['Latitude'], df['Longitude'] = zip(*df['Coordinates'].apply(parse_coordinate))
    
    return df

format_table(df)

print(df)
