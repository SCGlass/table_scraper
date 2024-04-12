import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from countries import country_codes

def scrape_and_save_tables(country_dict: dict) -> None:
    # Create a folder to store the CSV files
    if not os.path.exists("raw_country_data"):
        os.makedirs("raw_country_data")
    
    for country_code, country in tqdm(country_dict.items(), desc="Progress", total=len(country_dict)):
        country_code = country_code.lower()
        country = country.lower()
        url = f"https://service.unece.org/trade/locode/{country_code}.htm"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all tables
            tables = soup.find_all('table')
            if tables:
                # Extracting table data
                data = []
                for table in tables:
                    for row in table.find_all('tr'):
                        row_data = []
                        for td in row.find_all('td'):
                            row_data.append(td.text.strip())
                        if row_data:
                            data.append(row_data)

                # Create the Data Frame
                df = pd.DataFrame(data)

                filename = f"raw_country_data/{country_code}_{country}.csv"
                df.to_csv(filename, index=False)
                print(f"Table scraped and saved for {country} as {filename}")
            else:
                print(f"No table found for {country}")
            

scrape_and_save_tables(country_codes)
