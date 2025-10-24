# Efficiency and Diversity of R&D <br> in Knowledge-Intensive Services (2005–2023)

## :black_circle: About Me

I am a Doctor of Neuroscience with strong experience in data analysis, statistical modelling and research design. I focus on translating complex data into actionable insights for business and policy.

**Skills & tools**: advanced R, intermediate Python (*pandas*, *NumPy*, *matplotlib*, *seaborn*, *scipy*), developing my skills in Power BI & PowerApps. I enjoy data wrangling, visualization, and project management. My experience was gained through academic research and industry projects.

&emsp; **Location**: Poland, Krakow <br> 
&emsp; **Contact**: dominika.a.drazyk@gmail.com <br> 
&emsp; **LinkedIn**: [in/dominika-drazyk-otw95](https://www.linkedin.com/in/dominika-drazyk-otw95/)


## :grey_question: Are you:

[ :gear: ] &emsp; &emsp; &emsp; into the the code without much of a storytelling ? &emsp; open `./py_codes/` 

[ :gear: + :page_facing_up: ] &emsp; into the code and storytelling ? &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; open `./py_notebooks/`

[ :page_facing_up: ] &emsp; &emsp; &emsp; only into the storytelling ? &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; open `./reports/` 

Reports `./reports/*` were created using Jupyter Notebooks `./py_notebooks/*.ipynb` and Microsoft Power Point. Python codes `./py_codes/*.py` are concise versions of those notebooks. Both output the same figures `./figures/*.png` and data files `./data/*.csv`.

## :black_circle: Overview

This project examines how efficiently selected European countries convert R&D spending into researcher human capital within the knowledge-intensive services sector (NACE G–N). I inspect the available data to assess whether increasing female participation in researcher roles correlates with improved spending efficiency and labour dynamics.

:part_alternation_mark: *Practical business question*: Does investing in a more gender-diverse R&D workforce help or hinder the efficient use of R&D budgets in knowledge-intensive services?

### Data & Source Metadata

External data sources (Eurostat / DBnomics):

- [htec_sti_exp2](https://ec.europa.eu/eurostat/databrowser/view/htec_sti_exp2/default/table) dataset — R&D expenditure in high-tech sectors (Eurostat) 
- [htec_sti_pers2](https://ec.europa.eu/eurostat/databrowser/view/htec_sti_pers2/default/table) dataset — R&D personnel in high-tech sectors (Eurostat) 
- [rd_p_bempoccr2](https://db.nomics.world/Eurostat/rd_p_bempoccr2?dimensions=%7B%22freq%22%3A%5B%22A%22%5D%2C%22nace_r2%22%3A%5B%22G-N%22%5D%7D&tab=table) dataset — R&D personnel and researchers by activity and sex (DBnomics / Eurostat) 

### Key variables

- `Year`: 2005–2023
- `GDE Euro`: R&D expenditure (millions €) in NACE G–N sector
- `FTE All`: number of full-time positions in NACE G–N sector
- `FTE Researcher`: number of full-time researcher positions in NACE G–N sector
- `FTE Researcher Fem`: number of full-time researcher positions held by women in NACE G–N sector
- `Countries` analysed (final selection): Bulgaria, Czechia, Estonia, Croatia, Hungary, Italy, Poland, Portugal, Slovakia <br> 
  :grey_exclamation:	This set was selected because each country shows >80% data entry completeness for the chosen metrics.

### Tools & Methods

Programming & Analysis: Python {`pandas`, `NumPy`, `matplotlib`, `seaborn`, `scipy`}

Web scraping & metadata extraction: Python {`BeautifulSoup`, `selenium`}

Environment: Jupyter Notebook

Version control & sharing: Git & GitHub

Analytics performed: time-series plots, scatterplots, barplots, CAGR calculations, correlation analysis.

## :black_circle: Objectives

- Prepare a clean, merged panel dataset from Eurostat/DBnomics sources (2005–2023) for NACE G–N.
<br> Code: `scraper_code.ipynb` / `scraper_code.py`

- Load prepared datasets, filter and rename variables, review NaNs and missing data. 
<br> Code: `analysis_code.ipynb` / `analysis_code.py`

- Analyse sector's spending efficiency and labour intensity across selected countries.
<br> Code: `analysis_code.ipynb` / `analysis_code.py`

- Analyse participation of female researchers and its relationship to the sector's growth rates.
<br> Code: `analysis_code.ipynb` / `analysis_code.py`

- Compare trends, CAGRs and correlations across countries to understand how female inclusion relates to spending efficiency and labour intensity.
<br> Code: `analysis_code.ipynb` / `analysis_code.py`

### What this project delivers:

- A reproducible, well-documented merged datasets ready for dashboards or further analyses.

- Re-usable scraper and analysis code that can refresh results when source datasets are updated.

- Clear visualizations of time trends, CAGRs, and female-share vs efficiency correlations.

- :part_alternation_mark: Business-relevant insights for stakeholders interested in R&D investment, workforce planning, and diversity strategies.

## :black_circle: Examples of programming solutions

**Data cleaning**: clarify variable names and units.
```
df['time'] = df['time'].astype('int32')
df['Year'] = pd.to_datetime(df['time'], format = '%Y', errors = 'coerce')
print(f"Year: {df.time.isnull().sum()*100/len(df.time):.0f}% of entries were coerced to NaT.")
```
**Diagnosing missing data**: compute descriptive statistics, visualize coverage and gaps.
```
nan_count = df.isna().sum()
all_count = df.iloc[:,0].count()
prc = (nan_count * 100)/all_count
print('The percentage of NaN values per column:')
print(prc.apply(lambda x: x).apply("{:,.0f} %".format))
```
**Computing additional metrics**: calculate spending efficiency.
```
efficiency_calc = df.groupby(['Country', 'Year'])[['GDE Euro','FTE Researcher']].apply(
    lambda x: pd.Series({
        'SpendEff': x['GDE Euro'].sum() / x['FTE Researcher'].sum() 
            if not (x['GDE Euro'].isna().any() or x['FTE Researcher'].isna().any()) 
            else float('nan')})).reset_index()
df = df.merge(efficiency_calc, on=['Country', 'Year'], how = 'left')
print(f"SpendEff: {df['SpendEff'].isnull().sum()*100/len(df['SpendEff']):.0f}% of entries were coerced to NaN.")
```
**Visualising results**: ploting spending efficiency per country and across years.
```
g = sns.relplot(kind = 'line', x = 'Year', y = 'SpendEff', data = df, hue = 'Country', errorbar = None)
sns.move_legend(g, "upper right", bbox_to_anchor = (0.975, 0.95), ncol = 1)
g.set(title = 'Annual Spending Efficiency per a Researcher (FTE)', 
      xlabel = "Calendar year", ylabel = "Spending Efficiency [MIO € / 1 Reearcher FTE]")
g.fig.set_size_inches(10,4)
plt.savefig('../figures/Fig2.1 Annual Spending Efficiency per a Researcher FTE.png')
```
**Documenting**: providing merged dataset for future updates.
```
data = pd.merge(data_pers2_wide, data_exp2_wide, on = ['nace_r2', 'geo', 'time'], how = 'left') 
data = pd.merge(data, data_fem2, on = ['nace_r2', 'geo', 'time'], how = 'left')
data.to_csv('../data/scraper_data.csv', encoding='utf-8', index = False)
print('Merged dataset was saved into \'../data/scraper_data.csv\'.')
```

### Limitations & Challenges

- **Data limits**: substantial missing data before 2008 and after 2022; metric comparability is best between 2009 and 2021.

- **Country selection**: only 9 countries (with >80% completeness) were analysed — results are not a full EU/EFTA comparison.

- **Sector heterogeneity**: NACE G–N covers multiple service subsectors that can influence spending and hiring patterns.

- **Correlation**: correlations do not imply causation. Observed links between female share and efficiency may reflect confounders (economic structure, policy, funding cycles). <br>

:grey_exclamation: Offered insights are not based on a structured academic knowledge about EU policy or geo-political structure of discussed countries. My aim was to simply demonstrate my ability to understand complex datasets, data characteristics and measures that are outside my primary academic expertise.

## :black_circle: Key findings

**General trends**: Most countries showed increasing R&D spending efficiency and growing researcher workforces (2005–2023). Full-time research positions held by women increased faster than overall researcher growth in all analysed countries. <br> 
:part_alternation_mark: *Business Insight*: countries can be categorised as balanced, inclusion-phase, or efficiency-first.

  - **Balanced growth**: Poland and Slovakia increased spending efficiency, female share, and workforce size concurrently. <br> :part_alternation_mark: *Business Insight*: diversity initiatives combined with targeted funding and organizational change could result in a stable growth.

  - **Initial investment**: Italy, Portugal, and Croatia show rising female participation together with stagnant or declining spending efficiency — consistent with potential initial integration costs (recruitment, training). <br> :part_alternation_mark: *Business Insight*: gender-diversity investments may increase short-term costs but can bring long-term efficiency benefits.
      
  - **Efficiency prioritization**: Bulgaria, Czechia, and Estonia improved spending efficiency but presented declines in female share. <br> :part_alternation_mark:
  *Business Insight*: without corresponding diversity policies, improved spending efficiency may have favored male-dominated recruitment or sub-sectors.

## :black_circle: References

Carucci, R. (2024) One More Time: Why Diversity Leads to Better Team Performance. *Forbes*.

Hoogendoorn, S., Oosterbeek, H., & van Praag, M. (2019) When Gender Diversity Makes Firms More Productive. *Harvard Business Review*.

Niederle, M., Segal, C., & Vesterlund, L. (2008) How Costly is Diversity? Affirmative Action in Light of Gender Differences in Competitiveness. *NBER Working Paper*.

Phillips, K. (2014) How Diversity Makes Us Smarter. *Scientific American*.

Wearden, G. (2011) EU debt crisis: Italy hit with rating downgrade. *The Guardian*. 