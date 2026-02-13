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
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import scipy as sp
from scipy.stats import shapiro
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, '..', 'assets', 'fonts', 'Ubuntu-Regular.ttf')
STYLE_PATH = os.path.join(BASE_DIR, 'custom.mplstyle')
FIGURES_PATH = os.path.join(BASE_DIR, '..', 'figures')
DATA_PATH = os.path.join(BASE_DIR, '..', 'data')

pd.options.display.precision = 3
plt.style.use(STYLE_PATH)
full_palette = plt.rcParams["axes.prop_cycle"].by_key()["color"]

if os.path.exists(FONT_PATH):
    fe = fm.FontEntry(
        fname = FONT_PATH,
        name = 'ProjectUbuntu'
    )
    fm.fontManager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = fe.name
else:
    print("Warning: Font file not found. Falling back to sans-serif.")
    plt.rcParams['font.family'] = 'sans-serif'

# Functions
def filter_countries(row):
    """Filter countries based on predefined set"""
    global set_of_countries
    if row['geo'] in set_of_countries:
        return 'in'
    else: 
        return 'out'

def load_datasets():
    print("---- O1.1 Loading datasets...")
    
    df_path = os.path.join(DATA_PATH, 'scraper_data.csv')
    df = pd.read_csv(df_path)
    print(f"✓ Main dataset loaded: {len(df):,} records")

    mdf_path = os.path.join(DATA_PATH, 'scraper_metadata.csv')
    mdf = pd.read_csv(mdf_path)
    print(f"✓ Metadata loaded: {len(mdf):,} records")

    co_path = os.path.join(DATA_PATH, 'eu_efta_countries.csv')
    euefta = pd.read_csv(co_path)
    print(f"✓ EU + EFTA countries loaded: {len(euefta):,} countries\n")
    
    return df, mdf, euefta


def filter_and_rename_variables(df, euefta):
    print("---- O1.2 Filtering and renaming variables:")
    
    print("• Converting time to datetime format")
    df['time'] = df['time'].astype('int32')
    df['Year'] = pd.to_datetime(df['time'], format = '%Y', errors = 'coerce')
    nan_pct = df.time.isnull().sum()*100/len(df.time)
    print(f"• Year conversion: {nan_pct:.0f}% values converted to NaT")

    print("• Filtering by NACE classification")
    df = df[df['nace_r2'] == "G-N"]
    print(f"• NACE type included: {df.nace_r2.unique()}")

    print("• Filtering by EU + EFTA countries")
    global set_of_countries
    set_of_countries = euefta['geo'].values
    df['geo_euefta'] = df.apply(filter_countries, axis = 1)
    df = df[df['geo_euefta'] == 'in']
    print(f"• Countries included: {len(df.geo.unique())} EU + EFTA countries")
    df = pd.merge(df, euefta, on = ['geo'], how = 'left') 

    print("• Renaming columns for clarity")
    df = df.rename(columns = {"pers2_FTE_RSE": "FTE Researcher",
                              "pers2_FTE_TOTAL": "FTE All",
                              "fem2_FTE_RSE" : "FTE Researcher Fem",
                              "exp2_MIO_EUR": "GDE Euro"})

    print("• Removing unused columns")
    df = df.drop(['pers2_HC_RSE', 'pers2_HC_TOTAL', 'exp2_PC_TOT', 'nace_r2', 'geo_euefta', 'time'], axis = 1)
    df = df[['Country', 'geo', 'Year', 'GDE Euro', 'FTE All', 'FTE Researcher', 'FTE Researcher Fem']]

    print(f"Pre-processed Dataset Preview:")
    print(f"• Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print("• Sample data:")
    print(df.sample(3))
    print()
    
    return df

def review_missing_data(df):
    print("---- O1.3 Missing data analysis:")

    nan_count = df.isna().sum()
    all_count = df.iloc[:,0].count()
    prc = (nan_count * 100)/all_count
    print("Missing Data by Column:")
    for col, pct in prc.items():
        if pct > 0:
            print(f"• {col}: {pct:.0f}% missing")
    print()

    # The percentage of data entry gaps per country:
    df_nans = df.groupby('Country')[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Country')
    df_nans = df_nans.stack().reset_index().rename(columns={'level_1': 'metrics', 0: 'value'})

    plt.close('all') 
    plt.style.use(STYLE_PATH)

    metrics = df_nans['metrics'].unique()
    num_rows = len(metrics)

    fig, axes = plt.subplots(num_rows, 1, figsize = (9, 3 * num_rows), sharey = True)
    if num_rows == 1: axes = [axes]
    for i, metric in enumerate(metrics):
        data_subset = df_nans[df_nans['metrics'] == metric]

        sns.barplot(data = data_subset, x = 'Country', y = 'value', ax = axes[i])

        axes[i].set_title(f"Metric: {metric}")
        axes[i].set_ylabel("NaN entries [%]")
        axes[i].set_xlabel("Country")

        axes[i].set_ylim(0, 100)
        axes[i].set_yticks([0, 20, 40, 60, 80, 100])

        axes[i].tick_params(axis = 'x', rotation = 90)

    plt.suptitle('The percentage of NaN values per country', y = 1.005)
    plt.tight_layout()

    file_name = 'Fig1.3.1 The percentage of NaN values per country.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig1.3.1 The percentage of NaN values per country")

    # The percentage of data entry gaps across years:
    df_nans = df.groupby(
    'Year')[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
    lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Year')
    df_nans = df_nans.stack().reset_index().rename(columns={'level_1': 'metrics', 0: 'value'})

    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (7,4)})

    ax = sns.lineplot(data = df_nans, x = 'Year', y = 'value', hue = 'metrics', linewidth = 2)

    plt.title('The percentage of NaN values per year', loc = 'center')
    plt.xlabel("Year")
    plt.ylabel("Percentage of NaN entries [%]")

    plt.legend(title = "Metrics", loc = 'upper left', bbox_to_anchor=(1.01, 0.98))

    plt.yticks([0,10,20,30,40,50,60,70,80,90,100], ['0','10','20','30','40','50','60','70','80','90','100'])
    
    plt.tight_layout()
    
    file_name = 'Fig1.3.2 The percentage of data entry gaps across years.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig1.3.2 The percentage of data entry gaps across years")

    # Choosing countries with the least data entry gaps.
    print("Filtering Countries by Data Quality:")
    df_nans = df.groupby(['Country','geo'])[['GDE Euro','FTE All', 'FTE Researcher', 'FTE Researcher Fem']].apply(
        lambda x: (x.isna().sum() * 100 / len(x) )).sort_values(by = 'Country')
    df_nans = df_nans[(df_nans['FTE Researcher'] <= 20) & (df_nans['FTE Researcher Fem'] <= 20) & (df_nans['FTE All'] <= 20) & (df_nans['GDE Euro'] <= 20)]
    df_nans.reset_index(inplace = True)

    global set_of_countries
    set_of_countries = df_nans.geo.unique()
    df['geo_nan'] = df.apply(filter_countries, axis = 1)
    df = df[df['geo_nan'] == "in"]
    print(f"• Countries selected for analysis: {len(df.Country.unique())} countries")
    print(f"• Selected countries: {df.Country.unique()}")
    print()
    
    return df

def calculate_efficiency_metrics(df):
    print("---- O2 Efficiency and Labor Intensity analysis:")

    print("• O2.1 Calculating Annual Spending Efficiency")
    efficiency_calc = df.groupby(['Country', 'Year'])[['GDE Euro','FTE Researcher']].apply(
        lambda x: pd.Series({
            'SpendEff': x['GDE Euro'].sum() / x['FTE Researcher'].sum() 
                if not (x['GDE Euro'].isna().any() or x['FTE Researcher'].isna().any()) 
                else float('nan')})).reset_index()
    df = df.merge(efficiency_calc, on=['Country', 'Year'], how = 'left')
    nan_pct = df['SpendEff'].isnull().sum()*100/len(df['SpendEff'])
    print(f"• SpendEff: {nan_pct:.0f}% values converted to NaN")

    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (7,4)})

    ax = sns.lineplot(data = df, x = 'Year', y = 'SpendEff', hue = 'Country', linewidth = 2)

    plt.legend(title = "Country", loc = 'upper left', bbox_to_anchor=(1.01, 0.98))

    plt.xlabel("Calendar year")
    plt.ylabel("Spending Efficiency [MIO € / 1 Reearcher FTE]")
    plt.title(f"Annual Spending Efficiency per a Researcher (FTE)", loc = 'center')

    plt.tight_layout()

    file_name = 'Fig2.1 Annual Spending Efficiency per a Researcher FTE.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig2.1 Annual Spending Efficiency per a Researcher FTE")

    print("\n• O2.2 Calculating Annual Labor Intensity")
    labour_calc = df.groupby(['Country', 'Year'])[['GDE Euro','FTE Researcher']].apply(
        lambda x: pd.Series({
            'LaborInt': x['FTE Researcher'].sum() / (x['GDE Euro'].sum())
                if not (x['GDE Euro'].isna().any() or x['FTE Researcher'].isna().any()) 
                else float('nan')})).reset_index()
    nan_pct = labour_calc['LaborInt'].isnull().sum()*100/len(labour_calc['LaborInt'])
    print(f"• LaborInt: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(labour_calc, on=['Country', 'Year'], how = 'left')

    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (7,4)})

    ax = sns.lineplot(x = 'Year', y = 'LaborInt', data = df, hue = 'Country', errorbar = None)

    plt.title('Annual Labor Intensity per 1 MIO €', loc = 'center')
    plt.xlabel("Calendar year")
    plt.ylabel("Labor Intensity [Researcher FTE / 1 MIO €]")

    plt.legend(title = "Country", loc = 'upper left', bbox_to_anchor = (1.01, 0.98))

    plt.tight_layout()

    file_name = 'Fig2.2 Annual Labor Intensity per million euro.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig2.2 Annual Labor Intensity per million euro")
    print()
    
    return df

def calculate_female_share(df):
    print("---- O3.1 Female researcher share analysis:")

    print("• Calculating Female Share of Researcher FTEs")
    femshare_calc = df.groupby(
        ['Country', 'Year'])[['FTE Researcher', 'FTE Researcher Fem']].apply(
        lambda x: pd.Series({
            'FemShare': x['FTE Researcher Fem'].sum() / (x['FTE Researcher'].sum())
                if not (x['FTE Researcher Fem'].isna().any() or x['FTE Researcher'].isna().any()) 
               else float('nan')})).reset_index()
    nan_pct = femshare_calc['FemShare'].isnull().sum()*100/len(femshare_calc['FemShare'])
    print(f"• FemShare: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(femshare_calc, on=['Country', 'Year'], how = 'left')

    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (7,4)})

    ax = sns.lineplot(data = df, x = 'Year', y = 'FemShare', hue = 'Country', linewidth = 2)

    plt.legend(title = "Country", loc = 'upper left', bbox_to_anchor=(1.01, 0.95))

    plt.xlabel("Calendar year")
    plt.ylabel("Female Share of Researchers")
    plt.title(f"Annual Female Share of Researchers (FTEs)", loc = 'center')

    plt.tight_layout()

    file_name = 'Fig3.1 Annual Female Share of Researchers.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig3.1 Annual Female Share of Researchers")
    print()
    
    return df

def calculate_correlations(df):
    print("---- O3.2 Relationship between Spending Efficiency and Female Share")

    print("• Preparing data for correlation analysis")
    new_df = df[df['FemShare'].notna() & df['SpendEff'].notna()]
    print(f"• Valid data points: {len(new_df):,} observations")
    
    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (7,4)})

    fig, ax = plt.subplots()

    sns.scatterplot(data = new_df, x = 'FemShare', y = 'SpendEff', hue = 'Country', ax = ax, s = 20)

    print('Correlation test (CT): coefficients and statistical significance\n')

    countries = new_df['Country'].unique()
    for c in countries:
        mask = new_df['Country'] == c
        x = new_df[mask]['FemShare']
        y = new_df[mask]['SpendEff']

        sh_x = shapiro(x)
        sh_y = shapiro(y)
        
        m, b = np.polyfit(x, y, 1)
        x_lims = ax.get_xlim()
        X_plot = np.linspace(x_lims[0] + 0.05, x_lims[1] - 0.05, 100)
        
        if (sh_x[1] <= 0.05) or (sh_y[1] <= 0.05):
            stat, p = sp.stats.spearmanr(a = x, b = y)
            dist_type = "Normality violation"
        else:  
            stat, p = sp.stats.pearsonr(x = x, y = y)
            dist_type = "Normal distribution"
            
        print(f"  - {c}: {dist_type} - Stat = {stat:.2f}, p = {p:.2E}")

        line_style = '-' if p <= 0.05 else ':'
        ax.plot(X_plot, m * X_plot + b, linestyle = line_style)

    ax.set_title('Female Share vs. Spending Efficiency')
    ax.set_xlabel('Female Share of Researchers')
    ax.set_ylabel('Spending Efficiency [MIO € / 1 Researcher FTE]')

    ax.legend(title = 'Country', bbox_to_anchor = (1.001, 1), loc = 'upper left')

    plt.tight_layout()

    file_name = 'Fig3.2 Female Share vs Spending Efficiency.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig3.2 Female Share vs Spending Efficiency")
    print()
    
    return df

def calculate_growth_rates(df):
    print("---- O3.3 Growth Rate analysis (2009-2021):")

    print("• Calculating Researcher FTE CAGR")
    res_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
        ['Country', 'Year']).groupby(
        ['Country'])[['FTE Researcher']].apply(
        lambda x: pd.Series({
            'Res CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
                  if not (x.iloc[0,].isna().any())
                  else float('nan')})).reset_index()
    nan_pct = res_cagr_calc['Res CAGR 2009_2021'].isnull().sum()*100/len(res_cagr_calc['Res CAGR 2009_2021'])
    print(f"  - Res CAGR: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(res_cagr_calc, on=['Country'], how = 'left')

    print("• Calculating Female Researcher FTE CAGR")
    fem_res_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
        ['Country', 'Year']).groupby(
        ['Country'])[['FTE Researcher Fem']].apply(
        lambda x: pd.Series({
            'Fem Res CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
                  if not (x.iloc[0,].isna().any())
                  else float('nan')})).reset_index()
    nan_pct = fem_res_cagr_calc['Fem Res CAGR 2009_2021'].isnull().sum()*100/len(fem_res_cagr_calc['Fem Res CAGR 2009_2021'])
    print(f"  - Fem Res CAGR: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(fem_res_cagr_calc, on=['Country'], how = 'left')

    print("• Calculating Spending Efficiency CAGR")
    cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
        ['Country', 'Year']).groupby(
        ['Country'])[['SpendEff']].apply(
        lambda x: pd.Series({
            'SpendEff CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
                  if not (x.iloc[0,].isna().any())
                  else float('nan')})).reset_index()
    nan_pct = cagr_calc['SpendEff CAGR 2009_2021'].isnull().sum()*100/len(cagr_calc['SpendEff CAGR 2009_2021'])
    print(f"  - SpendEff CAGR: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(cagr_calc, on=['Country'], how = 'left')

    print("• Calculating Female Share CAGR")
    femshare_cagr_calc = df.query("(Year >= '2009') and (Year <= '2021')").sort_values(
        ['Country', 'Year']).groupby(
        ['Country'])[['FemShare']].apply(
        lambda x: pd.Series({
            'FemShare CAGR 2009_2021': ((x.iloc[-1,].item() / x.iloc[0,].item())**(1/13) - 1)
                  if not (x.iloc[0,].isna().any())
                  else float('nan')})).reset_index()
    nan_pct = femshare_cagr_calc['FemShare CAGR 2009_2021'].isnull().sum()*100/len(femshare_cagr_calc['FemShare CAGR 2009_2021'])
    print(f"  - FemShare CAGR: {nan_pct:.0f}% values converted to NaN")
    df = df.merge(femshare_cagr_calc, on=['Country'], how = 'left')

    print("• Preparing CAGR data for visualization")
    df_cagr = df.melt(id_vars = ['Country','geo', 'Year'],
                      value_vars = df.columns[11:15], 
                      var_name = 'CAGR types', 
                      value_name = 'CAGR value').drop_duplicates()
    df_cagr = df_cagr[['Country', 'geo', 'Year', 'CAGR types', 'CAGR value']]

    plt.close('all') 
    plt.style.use(STYLE_PATH)
    plt.rcParams.update({
        'figure.figsize': (10,4)})

    ax = sns.barplot(data = df_cagr, x = 'Country', y = 'CAGR value', hue = 'CAGR types')

    plt.title('Compound Annual Growth Rates between 2009 and 2021')
    plt.xlabel("Country")
    plt.ylabel("CAGRs")

    plt.legend(title = 'CAGR types', loc = 'upper left', bbox_to_anchor = (0.95, 0.99), ncol = 1)

    plt.tight_layout()

    file_name = 'Fig3.3 CAGRs between 2009 and 2021.png'
    save_path = os.path.join(FIGURES_PATH, file_name)
    plt.savefig(save_path)
    plt.show()
    print("✓ Saved: Fig3.3 CAGRs between 2009 and 2021")
    print()
    
    return df, df_cagr

def display_metadata(mdf):
    print("Source metadata:")
    print("• Current analysis was prepared based on the following information sources:")
    
    for i, row in mdf.iterrows():
        print(f"  {i+1}. {mdf.dataset_id[i]} dataset provided by: {mdf.dataset_source[i]}")
        print(f"     Last updated: {mdf.dataset_last_updated[i]}")
    print()

def save_preprocessed_datasets(df, df_cagr):
    print("Saving analysis results:")
    
    file_name = 'analysis_data.csv'
    save_path = os.path.join(DATA_PATH, file_name)
    df.to_csv(save_path, encoding='utf-8', index=False)
    print(f"✓ Main analysis dataset saved: ../data/analysis_data.csv ({df.shape[0]:,} rows)")
    
    file_name = 'cagr_analysis_data.csv'
    save_path = os.path.join(DATA_PATH, file_name)
    df_cagr.to_csv(save_path, encoding='utf-8', index=False)
    print(f"✓ CAGR analysis dataset saved: ../data/cagr_analysis_data.csv ({df_cagr.shape[0]:,} rows)")

def main():
    print("=" * 60)
    print("Efficiency and Diversity of R&D in Knowledge‑Intensive Services (2005‑2023)")
    print("Data Analysis Pipeline")
    print("=" * 60)
    print()
    
    # Phase 1: Loading datasets
    df, mdf, euefta = load_datasets()
    
    # Phase 2: Filtering and renaming variables
    df = filter_and_rename_variables(df, euefta)
    
    # Phase 3: Analyzing missing data
    df = review_missing_data(df)
    
    # Phase 4: Calculating efficiency metrics
    df = calculate_efficiency_metrics(df)
    
    # Phase 5: Analyzing female researchers
    df = calculate_female_share(df)
    
    # Phase 6: Correlation analysis
    df = calculate_correlations(df)
    
    # Phase 7: Growth rate analysis
    df, df_cagr = calculate_growth_rates(df)
    
    # Phase 8: Display data sources
    display_metadata(mdf)
    
    # Phase 9: Save results
    save_preprocessed_datasets(df, df_cagr)

if __name__ == "__main__":
    main()