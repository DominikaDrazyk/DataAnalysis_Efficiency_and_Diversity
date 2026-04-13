# Efficiency and Diversity of R&D <br> in Knowledge-Intensive Services (2005–2023)

## :large_orange_diamond: About Me

I am a Doctor of Neuroscience with strong experience in data analysis, statistical modelling and research design. I focus on translating complex data into actionable insights for business and policy. I enjoy data wrangling, visualization, and project management.

**Skills & tools:** 
- advanced **R**, advanced **Python** (*pandas*, *NumPy*, *matplotlib*, *seaborn*, *scipy*), 
- developing my skills in **Power BI** and **Power Apps** - see my [PowerBI portfolio project](https://github.com/DominikaDrazyk/DataAnalysis_Consultant_Dashboard),
- developing my skills in **SQL** (**ETL**, **PostgreSQL**, **pgAdmin4**, **DBeaver**) - see my [SQL portfolio project](https://github.com/DominikaDrazyk/DataAnalysis_eCommerce_Audit),
- comfortable managing **AI-augmented workflow**, leveraging *Cursor IDE* and *Claude* while ensuring code integrity through manual review - see my [Python/CSS portfolio project](https://github.com/DominikaDrazyk/DataAnalysis_euPOWERED_Navigator),
- technical documentation in **Jupyter Notebook** (*Markdown* syntax), version control in **Git**.

&emsp; **Contact**: dominika.a.drazyk@gmail.com <br> 
&emsp; **LinkedIn**: [in/dominika-drazyk-otw95](https://www.linkedin.com/in/dominika-drazyk-otw95/)

## :large_orange_diamond: Project Navigation
Select the path that best matches your interest:

**1. Executive & Business Insight** <br>
*For reviewers focused on storytelling, strategy, and end-results.*

- [PDF Presentation](./reports/Efficiency_and_Diversity_presentation.pdf): a step-by-step walkthrough of the project’s assumptions, technical execution highlights, and business insights;

- [Figures](./figures/): a repository of all programmatically generated visualizations used to drive the data narrative.

**2. Technical Deep-Dive & Audit** <br>
*For reviewers interested in the full analytical process and data interpretation.*

- [Full HTML Reports](./reports/): a comprehensive, rendered versions of the analysis, including all code, statistical interpretations, and granular findings;

- [Interactive Notebooks](./py_notebooks/): the original Jupyter environment used for iterative development and data exploration;

- [Clean Code](./py_codes/): production-ready, concise .py versions of the analytical logic, stripped of notebook metadata for better readability.

:eight_spoked_asterisk: **Dependency Management** <br>
This project uses Poetry to ensure a deterministic environment (locked versions) and 100% reproducibility. For basic users, a standard `requirements.txt` is also maintained.

- **Option 1: Modern Workflow (Recommended)**
Use this if you have Poetry installed. This will automatically create a virtual environment and install the exact versions from poetry.lock.

Bash
```
# Install dependencies and create virtual environment
poetry install
# Activate the environment
poetry shell
```

- **Option 2: Standard Workflow (Pip)**
Use this for a traditional setup using the provided `requirements.txt`.

1. Initialize the Virtual Environment

Linux / macOS: 
```
python3 -m venv .venv && source .venv/bin/activate
```

Windows: 
```
python -m venv .venv && .venv\Scripts\activate
```

2. Install Dependencies

Bash
```
pip install --upgrade pip
pip install -r requirements.txt
```

## :large_orange_diamond: Overview

Strategic evaluation of how efficiently selected European countries convert R&D spending into researcher human capital within the knowledge-intensive services sector (NACE G–N). I inspect the available data to assess whether increasing female participation in researcher roles correlates with improved spending efficiency and labour dynamics.

:part_alternation_mark: *Practical business question*: Does investing in a more gender-diverse R&D workforce help or hinder the efficient use of R&D budgets in knowledge-intensive services?

### What this project delivers:

- A reproducible, well-documented merged datasets ready for dashboards or further analyses.

- Re-usable scraper and analysis code that can refresh results when source datasets are updated.

- Clear visualizations of time trends, CAGRs, and female-share vs efficiency correlations.

- :part_alternation_mark: Business-relevant insights for stakeholders interested in R&D investment, workforce planning, and diversity strategies.

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
- `Countries` (final selection): Bulgaria, Czechia, Estonia, Croatia, Hungary, Italy, Poland, Portugal, Slovakia <br> 
  :grey_exclamation:	Each of those countries shows >80% data entry completeness for the chosen metrics.

### Tools & Methods

**Programming & Analysis**: Python {`pandas`, `NumPy`, `matplotlib`, `seaborn`, `scipy`}

**Web scraping & metadata extraction**: Python {`BeautifulSoup`, `selenium`}

**Documentation & Reporting**: Markdown, HTML syntax, Jupyter Notebooks.

**Version control & sharing**: Git & GitHub

**Analytics performed**: time-series plots, scatterplots, barplots, CAGR calculations, correlation analysis.

## :large_orange_diamond: Objectives

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

## :large_orange_diamond: Examples of programming solutions

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

## :large_orange_diamond: Key findings

**General trends**: Most countries showed increasing R&D spending efficiency and growing researcher workforces (2005–2023). Full-time research positions held by women increased faster than overall researcher growth in all analysed countries. <br> 
:part_alternation_mark: *Business Insight*: countries can be categorised as balanced, inclusion-phase, or efficiency-first.

  - **Balanced growth**: Poland and Slovakia increased spending efficiency, female share, and workforce size concurrently. <br> :part_alternation_mark: *Business Insight*: diversity initiatives combined with targeted funding and organizational change could result in a stable growth.

  - **Initial investment**: Italy, Portugal, and Croatia show rising female participation together with stagnant or declining spending efficiency — consistent with potential initial integration costs (recruitment, training). <br> :part_alternation_mark: *Business Insight*: gender-diversity investments may increase short-term costs but can bring long-term efficiency benefits.
      
  - **Efficiency prioritization**: Bulgaria, Czechia, and Estonia improved spending efficiency but presented declines in female share. <br> :part_alternation_mark:
  *Business Insight*: without corresponding diversity policies, improved spending efficiency may have favored male-dominated recruitment or sub-sectors.

## :large_orange_diamond: Presented skills

**Data Wrangling & Engineering**
- Developing *custom web scrapers* (`BeautifulSoup`, `selenium`) to automate the extraction of public datasets and metadata.
- Preparing and *cleaning panel datasets* using `pandas` and `NumPy` (handling missing values, datetime coercion, standardizing units).
- Executing complex data merging and restructuring across multiple external sources (Eurostat, DBnomics) to create a unified analytical foundation.

**Statistical Analysis & Modelling**
- Performing *time-series analysis* to track macro-level sector growth and workforce dynamics from 2005 to 2023.
- Calculating *advanced performance metrics*, including CAGR (Compound Annual Growth Rate) and custom spending efficiency indices.
- Conducting *correlation analysis* to evaluate the statistical relationship between demographic changes (female workforce participation) and financial efficiency.

**Data Visualization & Storytelling**
- Designing programmatic *visualizations* (`matplotlib`, `seaborn`) such as multi-variable time-series plots, scatterplots, and barplots.
- Translating abstract statistical findings into *actionable business insights* (e.g., categorizing country-level behaviors into "Balanced growth" or "Initial investment" phases).
- Documenting strict methodological limitations (e.g., distinguishing correlation from causation, addressing missing data gaps) to ensure *data integrity and transparent reporting*.