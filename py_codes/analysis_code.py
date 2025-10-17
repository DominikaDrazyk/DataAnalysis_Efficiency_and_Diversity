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

# Required libraries and custom styles:
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scipy as sp
from scipy.stats import shapiro
import os

custom_params = {"font.size": 16, "axes.titlesize": 14, "axes.labelsize": 10, "legend.fontsize": 10, 
                 'axes.facecolor':'white', 'figure.facecolor':'white', "grid.color": 'lightgray', 
                 "axes.edgecolor": '#3D3D3D', 'xtick.color': '#3D3D3D', 'ytick.color': '#3D3D3D',
                 "grid.linewidth": 1, "axes.linewidth": 1.25, 'xtick.bottom': True, 
                 'ytick.left': True, "xtick.major.size": 5, "ytick.major.size": 5, 
                 "xtick.minor.size": 2, "ytick.minor.size": 2}
sns.set_theme(context = 'paper', palette = 'muted', font = "Rubik", rc = custom_params)
pd.options.display.precision = 3
plt.style.use('custom.mplstyle')

# Paths
path = os.path.dirname(os.path.dirname( __file__ ))

# Functions:
def filter_countries(row):
    global set_of_countries
    if row['geo'] in set_of_countries:
        return 'in'
    else: return 'out'

# Loading prepared datasets
print('\n')
print('----- Efficiency and Diversity of R&D in Knowledge‑Intensive Services 2005‑2023 -----\n')

print('--- O1 Data preparation ...\n')

print('--- O1.1 Loading prepared datasets ...\n')
df_path = os.path.join(path, 'data/scraper_data.csv')
df = pd.read_csv(df_path)
print('> dataset')

mdf_path = os.path.join(path, 'data/scraper_metadata.csv')
mdf = pd.read_csv(mdf_path)
print('> metadata')

co_path = os.path.join(path, 'data/eu_efta_countries.csv')
euefta = pd.read_csv(co_path)
print('> EU + EFTA countries list\n')


# Filtering and renaming variables
print('--- O1.2 Filtering and renaming variables ...\n')

df['time'] = df['time'].astype('int32')
df['Year'] = pd.to_datetime(df['time'], format = '%Y', errors = 'coerce')
print(f"> Year: {df.time.isnull().sum()*100/len(df.time):.0f}% of entries were coerced to NaT.")

df = df[df['nace_r2'] == "G-N"]
print(f'> Only the following NACE type was included: {df.nace_r2.unique()}')

set_of_countries = euefta['geo'].values
df['geo_euefta'] = df.apply(filter_countries, axis = 1)
df = df[df['geo_euefta'] == 'in']
print(f'> Only EU + EFTA countries were included: {df.geo.unique()}')
df = pd.merge(df, euefta, on = ['geo'], how = 'left') 

df = df.rename(columns = {"pers2_FTE_RSE": "FTE Researcher",
                          "pers2_FTE_TOTAL": "FTE All",
                          "fem2_FTE_RSE" : "FTE Researcher Fem",
                          "exp2_MIO_EUR": "GDE Euro"})

df = df.drop(['pers2_HC_RSE', 'pers2_HC_TOTAL', 'exp2_PC_TOT', 'nace_r2', 'geo_euefta', 'time'], axis = 1)
df = df[['Country', 'geo', 'Year', 'GDE Euro', 'FTE All', 'FTE Researcher', 'FTE Researcher Fem']]

print('\n')
print('--- Pre-processed dataset preview:')
print(df.sample(10))
print('\n')

# Reviewing NaNs and missing data
print('--- O1.3 Reviewing NaNs and missing data...\n')

# The percentage of data entry gaps per column:
nan_count = df.isna().sum()
all_count = df.iloc[:,0].count()
prc = (nan_count * 100)/all_count
print('> The percentage of NaN values per column:')
print(prc.apply(lambda x: x).apply("{:,.0f} %".format))
print('\n')

# The percentage of data entry gaps per country:
df_nans = df.groupby('Country')[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Country')
df_nans = df_nans.stack().reset_index().rename(columns={'level_1': 'metrics', 0: 'value'})

g = sns.catplot(kind = 'bar', x = 'Country', y = 'value', row = 'metrics', height = 3, aspect = 3, 
                sharey = True, sharex = False, margin_titles = True,  data = df_nans)
g.set(title = 'The percentage of NaN values per country', 
      xlabel = "Country", ylabel = "Percentage of NaN entries [%]")
plt.yticks([0,10,20,30,40,50,60,70,80,90,100], ['0','10','20','30','40','50','60','70','80','90','100'])
g.tick_params(axis = 'x', rotation = 90)
g.figure.subplots_adjust(hspace = 0.8)
g.set(ylim = (0, 100))
plt.savefig('../figures/Fig1.3.1 The percentage of NaN values per country.png')
print('> saving Fig1.3.1 The percentage of NaN values per country')

# The percentage of data entry gaps across years:
df_nans = df.groupby(
    'Year')[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Year')
df_nans = df_nans.stack().reset_index().rename(columns={'level_1': 'metrics', 0: 'value'})

g = sns.relplot(kind = 'line', x = 'Year', y = 'value', data = df_nans, hue = 'metrics')
g.set(title = 'The percentage of NaN values per year', 
      xlabel = "Countries", ylabel = "Percentage of NaN entries [%]")
sns.move_legend(g, "upper right", title = 'Metrics', bbox_to_anchor = (0.68, 0.97))
g.set(ylim = (0, 100))
plt.yticks([0,10,20,30,40,50,60,70,80,90,100], ['0','10','20','30','40','50','60','70','80','90','100'])
g.figure.set_size_inches(10,4)
plt.savefig('../figures/Fig1.3.2 The percentage of data entry gaps across years.png')
print('> saving Fig1.3.2 The percentage of data entry gaps across years')

# Choosing countries with the least data entry gaps.
df_nans = df.groupby(['Country','geo'])[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Country')
df_nans = df_nans[(df_nans['FTE Researcher'] <= 20) & (df_nans['FTE Researcher Fem'] <= 20) & (df_nans['FTE All'] <= 20) & (df_nans['GDE Euro'] <= 20)]
df_nans.reset_index(inplace = True)

set_of_countries = df_nans.geo.unique()
df['geo_nan'] = df.apply(filter_countries, axis = 1)
df = df[df['geo_nan'] == "in"]
print(f'> Only following EU + EFTA countries were further analysed: {df.Country.unique()}')
print('\n')

print('--- O2 Sectors spending efficiency and labor intensity ...\n')

# A1.1 Annual Spending Efficiency
print('--- O2.1 Annual Spending Efficiency calculations ...\n')

efficiency_calc = df.groupby(['Country', 'Year'])[['GDE Euro','FTE Researcher']].apply(
    lambda x: pd.Series({
        'SpendEff': x['GDE Euro'].sum() / x['FTE Researcher'].sum() 
            if not (x['GDE Euro'].isna().any() or x['FTE Researcher'].isna().any()) 
            else float('nan')})).reset_index()
df = df.merge(efficiency_calc, on=['Country', 'Year'], how = 'left')
print(f"> SpendEff: {df['SpendEff'].isnull().sum()*100/len(df['SpendEff']):.0f}% of entries were coerced to NaN.")

g = sns.relplot(kind = 'line', x = 'Year', y = 'SpendEff', data = df, hue = 'Country', errorbar = None)
sns.move_legend(g, "upper right", bbox_to_anchor = (0.975, 0.95), ncol = 1)
g.set(title = 'Annual Spending Efficiency per a Researcher (FTE)', 
      xlabel = "Calendar year", ylabel = "Spending Efficiency [MIO € / 1 Reearcher FTE]")
g.figure.set_size_inches(10,4)
plt.savefig('../figures/Fig2.1 Annual Spending Efficiency per a Researcher FTE.png')
print('> Saving Fig2.1 Annual Spending Efficiency per a Researcher FTE')
print('\n')

# A1.2 Annual Labor Intensity
print('--- O2.2 Annual Labor Intensity calculations ...\n')

labour_calc = df.groupby(['Country', 'Year'])[['GDE Euro','FTE Researcher']].apply(
    lambda x: pd.Series({
        'LaborInt': x['FTE Researcher'].sum() / (x['GDE Euro'].sum())
            if not (x['GDE Euro'].isna().any() or x['FTE Researcher'].isna().any()) 
            else float('nan')})).reset_index()
print(f"> LaborInt: {labour_calc['LaborInt'].isnull().sum()*100/len(labour_calc['LaborInt']):.0f}% of entries were coerced to NaN.")
df = df.merge(labour_calc, on=['Country', 'Year'], how = 'left')

g = sns.relplot(kind = 'line', x = 'Year', y = 'LaborInt', data = df, hue = 'Country', errorbar = None)
sns.move_legend(g, "upper right", bbox_to_anchor = (0.975, 0.95), ncol = 1)
g.set(title = 'Annual Labor Intensity per 1 MIO €', 
      xlabel = "Calendar year", ylabel = "Labor Intensity [Reearcher FTE / 1 MIO €]")
g.figure.set_size_inches(10,4)
plt.savefig('../figures/Fig2.2 Annual Labor Intensity per million euro.png')
print('> Saving Fig2.2 Annual Labor Intensity per million euro')
print('\n')

print('--- O3 Participation of female researchers ...\n')

# A2.1 Female Share of Researcher FTEs
print('--- O3.1 Female Share of Researcher FTEs calculations ...\n')

femshare_calc = df.groupby(
    ['Country', 'Year'])[['FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: pd.Series({
        'FemShare': x['FTE Researcher Fem'].sum() / (x['FTE Researcher'].sum())
            if not (x['FTE Researcher Fem'].isna().any() or x['FTE Researcher'].isna().any()) 
           else float('nan')})).reset_index()
print(f"> FemShare: {femshare_calc['FemShare'].isnull().sum()*100/len(femshare_calc['FemShare']):.0f}% of entries were coerced to NaN.")
df = df.merge(femshare_calc, on=['Country', 'Year'], how = 'left')

g = sns.relplot(kind = 'line', x = 'Year', y = 'FemShare', data = df,
                hue = 'Country', errorbar = None)
sns.move_legend(g, "upper right", bbox_to_anchor = (0.975, 0.95), ncol = 1)
g.set(title = 'Annual Female Share of Researchers (FTEs)', 
      xlabel = "Calendar year", ylabel = "Female Share of Researchers")
g.figure.set_size_inches(10,4)
plt.savefig('../figures/Fig3.1 Annual Female Share of Researchers.png')
print('> Saving Fig3.1 Annual Female Share of Researchers')
print('\n')

# A2.2 Relationship between Spending Efficiency and Female Share of Researcher FTEs
print('--- O3.2 Relationship between Spending Efficiency and Female Share of Researcher FTEs calculations ...\n')

new_df = df[df['FemShare'].notna() & df['SpendEff'].notna()]
fig = plt.figure()
fig.set_size_inches(5.35, 5)
sns.scatterplot(data = new_df, x = 'FemShare', y = 'SpendEff', hue = 'Country')
plt.title('Female Share vs. Spending Efficiency')
plt.xlabel('Female Share of Researchers')
plt.ylabel('Spending Efficiency [MIO € / 1 Researcher FTE]')

print('> Correlation test (CT): coefficients and statistical significance\n')

for c in new_df['Country'].unique():
    x = new_df[new_df['Country'] == c]['FemShare']
    y = new_df[new_df['Country'] == c]['SpendEff']

    sh_x = shapiro(x)
    sh_y = shapiro(y)

    ax = plt.gca()
    ax.legend(title = 'Country', bbox_to_anchor = (1.35, 0.99))
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(ax.get_xlim()[0]+0.05, ax.get_xlim()[1]-0.05, 100)

    if (sh_x[1] <= 0.05) or (sh_y[1]  <= 0.05):
        stat, p = sp.stats.spearmanr(a = x, b = y)
        print(f"{c}: norm. violation - Spearman's CT: stat = {stat:.2f}, p = {p:.2E}")
        if p <= 0.05: plt.plot(X_plot, m*X_plot + b, '-')
        else: plt.plot(X_plot, m*X_plot + b, ':')

    else:  
        stat, p = sp.stats.pearsonr(x = x, y = y)
        print(f"{c}: norm. - Pearson's CT: stat = {stat:.2f}, p = {p:.2E}")
        if p <= 0.05: plt.plot(X_plot, m*X_plot + b, '-')
        else: plt.plot(X_plot, m*X_plot + b, ':')    

print('\n')
plt.savefig('../figures/Fig3.2 Female Share vs Spending Efficiency.png')
print('> Saving Fig3.2 Female Share vs Spending Efficiency')
print('\n')

# A2.3 Growth rates
print('--- O3.3 Growth rates calculations ...\n')

res_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
    ['Country', 'Year']).groupby(
    ['Country'])[['FTE Researcher']].apply(
    lambda x: pd.Series({
        'Res CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
              if not (x.iloc[0,].isna().any())
              else float('nan')})).reset_index()
print(f"> Res CAGR 2009_2021: {res_cagr_calc['Res CAGR 2009_2021'].isnull().sum()*100/len(res_cagr_calc['Res CAGR 2009_2021']):.0f}% of entries were coerced to NaN.")
df = df.merge(res_cagr_calc, on=['Country'], how = 'left')

fem_res_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
    ['Country', 'Year']).groupby(
    ['Country'])[['FTE Researcher Fem']].apply(
    lambda x: pd.Series({
        'Fem Res CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
              if not (x.iloc[0,].isna().any())
              else float('nan')})).reset_index()
print(f"> Fem Res CAGR 2009_2021: {fem_res_cagr_calc['Fem Res CAGR 2009_2021'].isnull().sum()*100/len(fem_res_cagr_calc['Fem Res CAGR 2009_2021']):.0f}% of entries were coerced to NaN.")
df = df.merge(fem_res_cagr_calc, on=['Country'], how = 'left')

cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
    ['Country', 'Year']).groupby(
    ['Country'])[['SpendEff']].apply(
    lambda x: pd.Series({
        'SpendEff CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
              if not (x.iloc[0,].isna().any())
              else float('nan')})).reset_index()
print(f"> SpendEff CAGR 2009_2021: {cagr_calc['SpendEff CAGR 2009_2021'].isnull().sum()*100/len(cagr_calc['SpendEff CAGR 2009_2021']):.0f}% of entries were coerced to NaN.")
df = df.merge(cagr_calc, on=['Country'], how = 'left')

femshare_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
    ['Country', 'Year']).groupby(
    ['Country'])[['FemShare']].apply(
    lambda x: pd.Series({
        'FemShare CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
              if not (x.iloc[0,].isna().any())
              else float('nan')})).reset_index()
print(f"> FemShare CAGR 2009_2021: {femshare_cagr_calc['FemShare CAGR 2009_2021'].isnull().sum()*100/len(femshare_cagr_calc['FemShare CAGR 2009_2021']):.0f}% of entries were coerced to NaN.")
df = df.merge(femshare_cagr_calc, on=['Country'], how = 'left')

df_cagr = df.melt(id_vars = ['Country','geo', 'Year'],
                  value_vars = df.columns[11:15], 
                  var_name = 'CAGR types', 
                  value_name = 'CAGR value').drop_duplicates()
df_cagr = df_cagr[['Country', 'geo', 'Year', 'CAGR types', 'CAGR value']]

g = sns.catplot(kind = 'bar', x = 'Country', y = 'CAGR value', hue = 'CAGR types', data = df_cagr)
g.set(title = 'Compound Annual Growth Rates between 2009 and 2021', xlabel = "Country", ylabel = "CAGRs")
sns.move_legend(g, "upper right", bbox_to_anchor = (0.95, 0.95), ncol = 1)
g.figure.set_size_inches(10,4)
plt.savefig('../figures/Fig3.3 CAGRs between 2009 and 2021.png')
print('> Saving Fig3.3 CAGRs between 2009 and 2021')
print('\n')

print('--- Current analysis was prepared based on the following information sources:')

for i, row in mdf.iterrows():
    print(f"{i+1}: {mdf.dataset_id[i]} dataset provided by: {mdf.dataset_source[i]}, last updated: {mdf.dataset_last_updated[i]}")

print('\n')
df.to_csv('../data/analysis_data.csv', encoding='utf-8', index = False)
print('Final dataset was saved into \'../data/analysis_data.csv\'.')
print('\n')
df_cagr.to_csv('../data/cagr_analysis_data.csv', encoding='utf-8', index = False)
print('Final cagr dataset was saved into \'../data/cagr_analysis_data.csv\'.')