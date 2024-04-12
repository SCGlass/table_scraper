from LatLon23 import LatLon
import re
import pandas as pd
from geopy.geocoders import Nominatim
from data import load_data
from tqdm import tqdm


class PortCleaner:
    def __init__(self) -> None:
        self.df = load_data()

    @staticmethod
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
        df[['Country_code', 'Location_code']] = df['LOCODE'].str.extract(r'^\s*(\S+)\s+(.*)$')
        
        # Removing columns that are not needed
        df = df[df.columns[~df.columns.isin(["Ch", "SubDiv", "Function", "Date", "Remarks", "IATA", "LOCODE"])]]

        # Reordering the columns
        country_code_col = df.pop('Country_code')
        location_code_col = df.pop('Location_code')
        df.insert(0, 'Country_code', country_code_col)
        df.insert(1, 'Location_code', location_code_col)
    
        return df

    
    @staticmethod
    def parse_coordinate(coord_str):
        if isinstance(coord_str, str):
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
        
    @staticmethod
    def geolocate(df):
    
        geolocator = Nominatim(user_agent="Harbour_locations", timeout=10)

        # creating dataframe with nan values in lat and lon columns
        missing_coord = df[df["Latitude"].isnull() | df["Longitude"].isnull()].copy()

        # combining Name and Lo columns to create a location query
        missing_coord["query"] = missing_coord["Name"] + ", " + missing_coord["Country_code"]

        # Apply geocoding
        missing_coord["coords"] = missing_coord["query"].apply(geolocator.geocode)

        #Extract Lat and Lon from coords
        missing_coord["Lat"] = missing_coord["coords"].apply(lambda x: x.latitude if x else None)
        missing_coord["Lon"] = missing_coord["coords"].apply(lambda x: x.longitude if x else None)

        # Merge the missing coord with the df based on Name
        merged_df = pd.merge(df, missing_coord[["Name", "Lat", "Lon"]], on="Name", how="left", suffixes=('', '_missing'))

        # Update Latitude and Longitude columns in the original dataframe
        df['Latitude'] = merged_df['Lat'].fillna(df['Latitude']).astype(float)
        df['Longitude'] = merged_df['Lon'].fillna(df['Longitude']).astype(float)


        return df

    def process_dataframe(self) ->pd.DataFrame:
        
        df = self.df
        
        df = self.format_table(df)

        # Apply the parse_coordinate function to extract latitude and longitude
        coordinates_parsed = df['Coordinates'].apply(lambda x: PortCleaner.parse_coordinate(x)).apply(pd.Series)

        # Add the parsed coordinates to the DataFrame
        df[['Latitude', 'Longitude']] = coordinates_parsed

        # Filter out non-string values in the 'Coordinates' column
        non_string_indices = df[df['Coordinates'].apply(lambda x: not isinstance(x, str))].index

        # Assign None to Latitude and Longitude for rows with non-string coordinates
        df.loc[non_string_indices, ['Latitude', 'Longitude']] = None

        df = self.geolocate(df)

        
        df.drop(columns="Coordinates", inplace=True)

        return df

port_cleaner= PortCleaner()
df = port_cleaner.process_dataframe()
print(df.info())
    
