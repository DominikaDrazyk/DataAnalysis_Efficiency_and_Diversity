#!/usr/bin/env python
# coding: utf-8

# __author__ = Dominika Drazyk
# __maintainer__ = Dominika Drazyk
# __email__ = dominika.a.drazyk@gmail.com
# __copyright__ = Dominika Drazyk
# __license__ = Apache License 2.0
# __version__ = 1.0.0
# __status__ = Production
# __date__ = 30/09/2025

# Required libraries:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from pyjstat import pyjstat
from datetime import datetime
import pandas as pd
import requests
import time
import re
import os

# Paths
path = os.path.dirname(os.path.dirname( __file__ ))

# Functions
def extract_data():
    print("---- O1.1 Extracting Eurostat datasets:")
    
    print("• Extracting expenditure data (htec_sti_exp2)")
    url_exp2 = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/htec_sti_exp2?lang=en"
    response_exp2 = requests.get(url_exp2)
    response_exp2.raise_for_status()
    data_exp2 = response_exp2.json()
    data_exp2 = pyjstat.from_json_stat(data_exp2, naming = 'id')[0]
    print(f"✓ Expenditure data extracted: {len(data_exp2):,} records")
    print(f"  Sample data: {data_exp2.shape}")

    print("• Extracting personnel data (htec_sti_pers2)")
    url_pers2 = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/htec_sti_pers2?lang=en"
    response_pers2 = requests.get(url_pers2)
    response_pers2.raise_for_status()
    data_pers2 = response_pers2.json()
    data_pers2 = pyjstat.from_json_stat(data_pers2, naming = 'id')[0]
    print(f"✓ Personnel data extracted: {len(data_pers2):,} records")
    print(f"  Sample data: {data_pers2.shape}")

    print("• Extracting female researcher data")
    url_fem2 = "https://db.nomics.world/Eurostat/rd_p_bempoccr2?dimensions=%7B%22freq%22%3A%5B%22A%22%5D%2C%22nace_r2%22%3A%5B%22G-N%22%5D%7D&tab=table"
    fem2_path = os.path.join(path, 'data/rd_p_bempoccr2.csv')
    data_fem2 = pd.read_csv(fem2_path)
    
    # Process column names
    for col in data_fem2.columns:
        if col.startswith('Annual'):
            match = re.search(r'\.([A-Z]{2,3})\)$', col)
            if match and match.group(1):
              geo = match.group(1)
            else:
              geo = 'UU'
            data_fem2 = data_fem2.rename(columns={col: geo})
    
    # Reshape data
    data_fem2 = data_fem2.melt(id_vars = ['period'], 
                               value_vars = data_fem2.columns[1:274], 
                               var_name = 'geo', 
                               value_name = 'fem2_FTE_RSE')
    data_fem2 = data_fem2[data_fem2['geo'] != "UU"]
    data_fem2 = data_fem2.rename(columns={'period': 'time'})
    data_fem2['time'] = data_fem2['time'].map(str)
    data_fem2['nace_r2'] = 'G-N'
    print(f"✓ Female researcher data processed: {len(data_fem2):,} records")
    print(f"  Sample data: {data_fem2.shape}")
    print()
    
    return data_exp2, data_pers2, data_fem2

def extract_metadata():
    print("---- O1.2 Extracting dataset metadata:")
    
    print("• Extracting expenditure dataset metadata")
    url_exp2_meta = 'https://ec.europa.eu/eurostat/databrowser/view/htec_sti_exp2/default/table'
    print(f"  Source: {url_exp2_meta}")
    
    chrome_options = Options()
    driver_exp2 = webdriver.Chrome(options = chrome_options)
    driver_exp2.get(url_exp2_meta)
    print("  • Webpage opened")
    time.sleep(20) 
    r = driver_exp2.page_source
    print("  • Page source extracted")
    soup_exp2 = bs(r, "html.parser")
    driver_exp2.close()
    print("  • Browser closed")

    print("  • Parsing metadata fields")
    body = soup_exp2.find('body')
    marker = body.find('span', string = "last update")
    tag = marker.find_next("b", class_ = "infobox-text-data")
    exp2_date = tag.get_text(strip = True)
    print(f"    - Last updated: {exp2_date}")
    
    marker = body.find('span', string = "Source of data:")
    tag = marker.find_next("span")
    exp2_source = tag.get_text(strip = True)
    print(f"    - Source: {exp2_source}")
    
    exp2_title = soup_exp2.find('h1', class_ = "ecl-page-header__title").get_text()
    print(f"    - Title: {exp2_title}")
    
    marker = body.find('span', string = "Online data code:")
    tag = marker.find_next("b", class_ = "infobox-text-data")
    exp2_id = tag.get_text(strip = True)
    print(f"    - Dataset ID: {exp2_id}")
    
    exp2_meta = [exp2_id, exp2_source, exp2_title, exp2_date]
    print()

    print("• Extracting personnel dataset metadata")
    url_pers2_meta = 'https://ec.europa.eu/eurostat/databrowser/view/htec_sti_pers2/default/table'
    print(f"  Source: {url_pers2_meta}")
    
    chrome_options = Options()
    driver_pers2 = webdriver.Chrome(options = chrome_options)
    driver_pers2.get(url_pers2_meta)
    print("  • Webpage opened")
    time.sleep(20) 
    r = driver_pers2.page_source
    print("  • Page source extracted")
    soup_pers2 = bs(r, "html.parser")
    driver_pers2.close()
    print("  • Browser closed")

    print("  • Parsing metadata fields")
    body = soup_pers2.find('body')
    marker = body.find('span', string = "last update")
    tag = marker.find_next("b", class_ = "infobox-text-data")
    pers2_date = tag.get_text(strip = True)
    print(f"    - Last updated: {pers2_date}")
    
    marker = body.find('span', string = "Source of data:")
    tag = marker.find_next("span")
    pers2_source = tag.get_text(strip = True)
    print(f"    - Source: {pers2_source}")
    
    pers2_title = soup_pers2.find('h1', class_ = "ecl-page-header__title").get_text()
    print(f"    - Title: {pers2_title}")
    
    marker = body.find('span', string = "Online data code:")
    tag = marker.find_next("b", class_ = "infobox-text-data")
    pers2_id = tag.get_text(strip = True)
    print(f"    - Dataset ID: {pers2_id}")
    
    pers2_meta = [pers2_id, pers2_source, pers2_title, pers2_date]
    print()

    print("• Extracting female researcher dataset metadata")
    url_fem2_meta = 'https://db.nomics.world/Eurostat/rd_p_bempoccr2?dimensions=%7B%22freq%22%3A%5B%22A%22%5D%2C%22nace_r2%22%3A%5B%22G-N%22%5D%7D&tab=table'
    print(f"  Source: {url_fem2_meta}")
    
    chrome_options = Options()
    driver_fem2 = webdriver.Chrome(options = chrome_options)
    driver_fem2.get(url_fem2_meta)
    print("  • Webpage opened")
    time.sleep(20) 
    r = driver_fem2.page_source
    print("  • Page source extracted")
    soup_fem2 = bs(r, "html.parser")
    driver_fem2.close()
    print("  • Browser closed")

    print("  • Parsing metadata fields")
    body = soup_fem2.find('body')
    marker = body.find("p", class_ = "my-8")
    text = marker.get_text(strip = True)
    match = re.search(r'on(\w+\s+\d+,\s+\d+)\s+\((\d+:\d+\s+[AP]M)\)', text)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        dt = datetime.strptime(f"{date_str} {time_str}", "%B %d, %Y %I:%M %p")
        fem2_date = dt.strftime("%d/%m/%Y %H:%M")
        print(f"    - Last updated: {fem2_date}")
    else: 
        fem2_date = 'None'
        print(f"    - Last updated: {fem2_date}")
    
    div = body.find('div', class_ = "container")
    span = div.find('span', class_ = "hover:text-foreground transition-colors")
    a = span.find_next('a', class_ = "text-muted-foreground link")
    fem2_source = a.get_text(strip = True)[1:-1]
    print(f"    - Source: {fem2_source}")
    
    div = body.find('div', class_ = "container")
    h1 = div.find('h1', class_ = "text-3xl mb-10")
    spans = h1.find_all('span')
    fem2_title = spans[3].get_text(strip = True)
    print(f"    - Title: {fem2_title}")
    
    marker = h1.find('span', class_ = "text-muted-foreground")
    fem2_id = marker.get_text(strip = True)[1:-1]
    print(f"    - Dataset ID: {fem2_id}")
    
    fem2_meta = [fem2_id, fem2_source, fem2_title, fem2_date]
    print()

    print("• Creating metadata dataset")
    meta = pd.DataFrame([exp2_meta, pers2_meta, fem2_meta], 
                       columns = ['dataset_id', 'dataset_source', 'dataset_title', 'dataset_last_updated'])
    print(f"✓ Metadata dataset created: {meta.shape[0]} datasets")
    print(meta)

    print("• Saving metadata")
    meta.to_csv('../data/scraper_metadata.csv', encoding='utf-8', index = False)
    print("✓ Metadata saved: ../data/scraper_metadata.csv")
    print()
    
    return meta

def extract_countries_list():
    print("---- O1.3 Extracting EU + EFTA countries list:")
    
    url_countries_meta = 'https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes'
    print(f"• Source: {url_countries_meta}")
    
    chrome_options = Options()
    driver_co = webdriver.Chrome(options = chrome_options)
    driver_co.get(url_countries_meta)
    print("  • Webpage opened")
    time.sleep(20) 
    r = driver_co.page_source
    print("  • Page source extracted")
    soup_co = bs(r, "html.parser")
    driver_co.close()
    print("  • Browser closed")

    print("  • Parsing country data from tables")
    content_div = soup_co.find('div', {'id': 'mw-content-text'})
    tables = content_div.find_all('table')
    eu_efta_countries = []
    
    for i, table in enumerate(tables):
        if (i == 0) or (i == 1):  
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                for j in range(0, len(cells), 2):
                    if j + 1 < len(cells):
                        if cells[j].get_text(strip=True) == '':
                            j = j + 1
                        country_name = cells[j].get_text(strip=True)
                        country_code = cells[j + 1].get_text(strip=True)
                        country_code = country_code.replace('(', '').replace(')', '').strip()
                        print(f"    - {country_name}: {country_code}")

                        country_data = {'Country': country_name, 'geo': country_code}
                        eu_efta_countries.append(country_data)
    
    eu_efta_countries_df = pd.DataFrame.from_dict(eu_efta_countries)
    print(f"✓ Countries extracted: {len(eu_efta_countries_df)} countries")

    print("• Saving countries list")
    eu_efta_countries_df.to_csv('../data/eu_efta_countries.csv', encoding = 'utf-8', index = False)
    print("✓ Countries saved: ../data/eu_efta_countries.csv")
    print()
    
    return eu_efta_countries_df

def process_datasets(data_exp2, data_pers2):
    print("---- O2 Preprocessing datasets:")
    
    print("• Cleaning datasets")
    data_exp2.drop(columns = ['freq'], inplace = True)
    data_pers2.drop(columns = ['freq'], inplace = True) 
    print("  ✓ Unused columns removed")

    print("• Transforming expenditure data to wide format")
    data_exp2_wide = data_exp2.pivot(index = ['nace_r2', 'geo', 'time'], columns = 'unit', values = 'value').reset_index()
    data_exp2_wide = data_exp2_wide.rename(columns=lambda x: f"exp2_{x}" if x not in ['nace_r2', 'geo', 'time'] else x)
    print(f"  ✓ Expenditure data: {data_exp2_wide.shape[0]:,} rows × {data_exp2_wide.shape[1]} columns")
    print(f"    Sample: {data_exp2_wide.shape}")

    print("• Transforming personnel data to wide format")
    data_pers2_wide = data_pers2.pivot(index = ['nace_r2', 'geo', 'time', 'prof_pos'], columns = ['unit'], values = 'value').reset_index()
    data_pers2_wide = data_pers2_wide.pivot(index = ['nace_r2', 'geo', 'time'], columns = ['prof_pos'], values = ['FTE','HC']).reset_index()
    data_pers2_wide.columns = ["_".join([str(c) for c in col if c != ""])
                                for col in data_pers2_wide.columns.to_flat_index()]
    data_pers2_wide = data_pers2_wide.rename(columns=lambda x: f"pers2_{x}" if x not in ['nace_r2', 'geo', 'time'] else x)
    print(f"  ✓ Personnel data: {data_pers2_wide.shape[0]:,} rows × {data_pers2_wide.shape[1]} columns")
    print(f"    Sample: {data_pers2_wide.shape}")
    
    return data_exp2_wide, data_pers2_wide

def merge_datasets(data_exp2_wide, data_pers2_wide, data_fem2):
    print("---- O3 Merging datasets:")

    print("• Merging all datasets")
    data = pd.merge(data_pers2_wide, data_exp2_wide, on = ['nace_r2', 'geo', 'time'], how = 'left') 
    data = pd.merge(data, data_fem2, on = ['nace_r2', 'geo', 'time'], how = 'left') 
    print(f"✓ Merged dataset: {data.shape[0]:,} rows × {data.shape[1]} columns")
    print(f"  Sample data: {data.shape}")

    print("• Dataset summary:")
    print(f"  - NACE levels: {data['nace_r2'].unique().tolist()}")
    print(f"  - Geographic levels: {len(data['geo'].unique())} countries")
    print(f"  - Time levels: {len(data['time'].unique())} years")

    print("• Saving merged dataset")
    data.to_csv('../data/scraper_data.csv', encoding='utf-8', index = False)
    print("✓ Merged dataset saved: ../data/scraper_data.csv")
    print()
    
    return data

def main():
    print("=" * 60)
    print("Efficiency and Diversity of R&D in Knowledge‑Intensive Services (2005‑2023)")
    print("Data Scraping Pipeline")
    print("=" * 60)
    print()
    
    data_exp2, data_pers2, data_fem2 = extract_data()
    
    meta = extract_metadata()
    
    countries_df = extract_countries_list()
    
    data_exp2_wide, data_pers2_wide = process_datasets(data_exp2, data_pers2)

    merged_data = merge_datasets(data_exp2_wide, data_pers2_wide, data_fem2)

    print(f"Final dataset: {merged_data.shape[0]:,} rows × {merged_data.shape[1]} columns")

if __name__ == "__main__":
    main()

