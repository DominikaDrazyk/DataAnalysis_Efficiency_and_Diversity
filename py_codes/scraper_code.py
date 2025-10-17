#!/usr/bin/env python
# coding: utf-8

# Efficiency and Diversity of R&D in Knowledge‑Intensive Services (2005‑2023)

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

print('\n')
print('----- Efficiency and Diversity of R&D in Knowledge‑Intensive Services 2005‑2023 -----\n')

# A1. Data extraction using available API
print('--- O1 Data extraction using available API ...\n')

print('--- O11. Datasets ...\n')
url_exp2 = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/htec_sti_exp2?lang=en"
response_exp2 = requests.get(url_exp2)
response_exp2.raise_for_status()
data_exp2 = response_exp2.json()
data_exp2 = pyjstat.from_json_stat(data_exp2, naming = 'id')[0]
print('> Data from ', url_exp2,' was extracted.')
print(data_exp2.head())

url_pers2 = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/htec_sti_pers2?lang=en"
response_pers2 = requests.get(url_pers2)
response_pers2.raise_for_status()
data_pers2 = response_pers2.json()
data_pers2 = pyjstat.from_json_stat(data_pers2, naming = 'id')[0]
print('> Data from ', url_pers2,' was extracted.')
print(data_pers2.head())

url_fem2 = "https://db.nomics.world/Eurostat/rd_p_bempoccr2?dimensions=%7B%22freq%22%3A%5B%22A%22%5D%2C%22nace_r2%22%3A%5B%22G-N%22%5D%7D&tab=table"
fem2_path = os.path.join(path, 'data/rd_p_bempoccr2.csv')
data_fem2 = pd.read_csv(fem2_path)
for col in data_fem2.columns:
    if col.startswith('Annual'):
        match = re.search(r'\.([A-Z]{2,3})\)$', col)
        if match and match.group(1):
          geo = match.group(1)
        else:
          geo = 'UU'
        data_fem2 = data_fem2.rename(columns={col: geo})
data_fem2 = data_fem2.melt(id_vars = ['period'], 
                           value_vars = data_fem2.columns[1:274], 
                           var_name = 'geo', 
                           value_name = 'fem2_FTE_RSE')
data_fem2 = data_fem2[data_fem2['geo'] != "UU"]
data_fem2 = data_fem2.rename(columns={'period': 'time'})
data_fem2['time'] = data_fem2['time'].map(str)
data_fem2['nace_r2'] = 'G-N'
print('> Data from ', url_fem2,' was downloaded.')
print(data_fem2.head())
print('\n')

# ### A1.2 Metadata
print('--- O1.2 Metadata ...\n')

url_exp2_meta = 'https://ec.europa.eu/eurostat/databrowser/view/htec_sti_exp2/default/table'
print('> htec_sti_exp2 source webpage: ', url_exp2_meta)
chrome_options = Options()
driver_exp2 = webdriver.Chrome(options = chrome_options)
driver_exp2.get(url_exp2_meta)
print('> opened')
time.sleep(20) 
r = driver_exp2.page_source
print('> extracted')
soup_exp2 = bs(r, "html.parser")
driver_exp2.close()
print('> closed')

print('> htec_sti_exp2 dataset metadata:\n')
body = soup_exp2.find('body')
marker = body.find('span', string = "last update")
tag = marker.find_next("b", class_ = "infobox-text-data")
exp2_date = tag.get_text(strip = True)
print('\t dataset_last_updated: ', exp2_date)
marker = body.find('span', string = "Source of data:")
tag = marker.find_next("span")
exp2_source = tag.get_text(strip = True)
print('\t dataset_source: ', exp2_source)
exp2_title = soup_exp2.find('h1', class_ = "ecl-page-header__title").get_text()
print('\t dataset_title: ', exp2_title)
marker = body.find('span', string = "Online data code:")
tag = marker.find_next("b", class_ = "infobox-text-data")
exp2_id = tag.get_text(strip = True)
print('\t dataset_id: ', exp2_id)
exp2_meta = [exp2_id, exp2_source, exp2_title, exp2_date]
print('\n')

url_pers2_meta = 'https://ec.europa.eu/eurostat/databrowser/view/htec_sti_pers2/default/table'
print('> htec_sti_pers2 source webpage: ', url_pers2_meta)
chrome_options = Options()
driver_pers2 = webdriver.Chrome(options = chrome_options)
driver_pers2.get(url_pers2_meta)
print('> opened')
time.sleep(20) 
r = driver_pers2.page_source
print('> extracted')
soup_pers2 = bs(r, "html.parser")
driver_pers2.close()
print('> closed')

print('> htec_sti_pers2 dataset metadata:\n')
body = soup_pers2.find('body')
marker = body.find('span', string = "last update")
tag = marker.find_next("b", class_ = "infobox-text-data")
pers2_date = tag.get_text(strip = True)
print('\t dataset_last_updated: ', pers2_date)
marker = body.find('span', string = "Source of data:")
tag = marker.find_next("span")
pers2_source = tag.get_text(strip = True)
print('\t dataset_source: ', pers2_source)
pers2_title = soup_pers2.find('h1', class_ = "ecl-page-header__title").get_text()
print('\t dataset_title: ', pers2_title)
marker = body.find('span', string = "Online data code:")
tag = marker.find_next("b", class_ = "infobox-text-data")
pers2_id = tag.get_text(strip = True)
print('\t dataset_id: ', pers2_id)
pers2_meta = [pers2_id, pers2_source, pers2_title, pers2_date]
print('\n')

url_fem2_meta = 'https://db.nomics.world/Eurostat/rd_p_bempoccr2?dimensions=%7B%22freq%22%3A%5B%22A%22%5D%2C%22nace_r2%22%3A%5B%22G-N%22%5D%7D&tab=table'
print('> rd_p_bempoccr2 source webpage: ', url_fem2_meta)
chrome_options = Options()
driver_fem2 = webdriver.Chrome(options = chrome_options)
driver_fem2.get(url_fem2_meta)
print('> opened')
time.sleep(20) 
r = driver_fem2.page_source
print('> extracted')
soup_fem2 = bs(r, "html.parser")
driver_fem2.close()
print('> closed')

print('> rd_p_bempoccr2 dataset metadata:\n')
body = soup_fem2.find('body')
marker = body.find("p", class_ = "my-8")
text = marker.get_text(strip = True)
match = re.search(r'on(\w+\s+\d+,\s+\d+)\s+\((\d+:\d+\s+[AP]M)\)', text)
if match:
    date_str = match.group(1)
    time_str = match.group(2)
    dt = datetime.strptime(f"{date_str} {time_str}", "%B %d, %Y %I:%M %p")
    fem2_date = dt.strftime("%d/%m/%Y %H:%M")
    print('\t dataset_last_updated: ', fem2_date)
else: fem2_date = 'None'
div = body.find('div', class_ = "container")
span = div.find('span', class_ = "hover:text-foreground transition-colors")
a = span.find_next('a', class_ = "text-muted-foreground link")
fem2_source = a.get_text(strip = True)[1:-1]
print('\t dataset_source: ', fem2_source)
div = body.find('div', class_ = "container")
h1 = div.find('h1', class_ = "text-3xl mb-10")
spans = h1.find_all('span')
fem2_title = spans[3].get_text(strip = True)
print('\t dataset_title: ', fem2_title)
marker = h1.find('span', class_ = "text-muted-foreground")
fem2_id = marker.get_text(strip = True)[1:-1]
print('\t dataset_id: ', fem2_id)
fem2_meta = [fem2_id, fem2_source, fem2_title, fem2_date]
print('\n')

meta = pd.DataFrame([exp2_meta,pers2_meta,fem2_meta], columns = ['dataset_id', 'dataset_source', 'dataset_title', 'dataset_last_updated'])
print('> Metadata dataset was created:')
print(meta)

meta.to_csv('../data/scraper_metadata.csv', encoding='utf-8', index = False)
print('\n')
print('> Metadata dataset was saved into \'../data/scraper_metadata.csv\'.')
print('\n')

# List of European + EFTA countries

url_countries_meta = 'https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes'
print('> European+EFTA countries source webpage: ', url_countries_meta)
chrome_options = Options()
driver_co = webdriver.Chrome(options = chrome_options)
driver_co.get(url_countries_meta)
print('> opened')
time.sleep(20) 
r = driver_co.page_source
print('> extracted')
soup_co = bs(r, "html.parser")
driver_co.close()
print('> closed')

content_div = soup_co.find('div', {'id': 'mw-content-text'})
tables = content_div.find_all('table')
eu_efta_countries = []
for i, table in enumerate(tables):
    if (i == 0)  or (i == 1):  
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
                    print(f"\t Country: {country_name}, geo: {country_code}")

                    country_data = {'Country': country_name, 'geo': country_code}
                    eu_efta_countries.append(country_data)
eu_efta_countries_df = pd.DataFrame.from_dict(eu_efta_countries)

eu_efta_countries_df.to_csv('../data/eu_efta_countries.csv', encoding = 'utf-8', index = False)
print('> EU + EFTA countries list was saved into \'../data/eu_efta_countries.csv\'.')
print('\n')

# A2. Cleaning and pre-processing datasets
print('--- O2 Cleaning and pre-processing datasets ...\n')

data_exp2.drop(columns = ['freq'], inplace = True)
data_pers2.drop(columns = ['freq'], inplace = True) 
print('> Unused columns were removed.')

data_exp2_wide = data_exp2.pivot(index = ['nace_r2', 'geo', 'time'], columns = 'unit', values = 'value').reset_index()
data_exp2_wide = data_exp2_wide.rename(columns=lambda x: f"exp2_{x}" if x not in ['nace_r2', 'geo', 'time'] else x)
print('> Dataset exp2 was transformed into a wide format:')
print(data_exp2_wide.sample(5))

data_pers2_wide = data_pers2.pivot(index = ['nace_r2', 'geo', 'time', 'prof_pos'], columns = ['unit'], values = 'value').reset_index()
data_pers2_wide = data_pers2_wide.pivot(index = ['nace_r2', 'geo', 'time'], columns = ['prof_pos'], values = ['FTE','HC']).reset_index()
data_pers2_wide.columns = ["_".join([str(c) for c in col if c != ""])
                            for col in data_pers2_wide.columns.to_flat_index()]
data_pers2_wide = data_pers2_wide.rename(columns=lambda x: f"pers2_{x}" if x not in ['nace_r2', 'geo', 'time'] else x)
print('> Dataset pers2 was transformed into a wide format:')
print(data_pers2_wide.sample(5))
print('\n')

# A3. Merging datasets and saving files
print('--- O3 Merging datasets and saving files ...\n')

data = pd.merge(data_pers2_wide, data_exp2_wide, on = ['nace_r2', 'geo', 'time'], how = 'left') 
data = pd.merge(data, data_fem2, on = ['nace_r2', 'geo', 'time'], how = 'left') 
print('Datasets were merged:')
print(data.sample(5))
print('\n')

print('> Dataset \'nace_r2\' levels  : ', data['nace_r2'].unique().tolist())
print('> Dataset \'geo\' levels  : ', data['geo'].unique().tolist())
print('> Dataset \'time\' levels  : ', data['time'].unique().tolist())

data.to_csv('../data/scraper_data.csv', encoding='utf-8', index = False)
print('> Merged dataset was saved into \'../data/scraper_data.csv\'.')

