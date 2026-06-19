COVID-19 Behavior and Political/Social Predictors Analysis

This project analyzes COVID-19 behavioral outcomes using survey data from the Journal of Behavioral Public Administration Dataverse dataset. The analysis focuses on self-isolation behavior, mask-wearing behavior, and the relationship between political party affiliation and masking behavior.

Project Overview

The goal of this project was to clean, analyze, and visualize COVID-19 survey data using Python. The project includes descriptive statistics, exploratory data analysis, regression modeling, chi-square testing, and publication-style tables and figures.

The analysis addresses three main research questions:

1. RQ1: Is age associated with self-isolation behavior?
2. RQ2: Which demographic or social factors are associated with mask-wearing behavior?
3. RQ3: Is political party affiliation associated with mask-wearing behavior?

Repository Structure

.
├── data/
│   ├── raw/              # Original dataset files
│   └── processed/        # Cleaned datasets used for analysis
│
├── scripts/              # Python scripts for cleaning, analysis, tables, and visualization
│
├── results/
│   ├── tables/           # Final tables and CSV outputs
│   └── model_outputs/    # Regression and statistical test outputs
│
├── figures/              # Charts and visualizations
│
├── docs/                 # Supporting documentation and original do-file
│
└── README.md

Methods

The analysis was conducted in Python and included the following steps:

1. Data cleaning
    * Imported the original dataset.
    * Cleaned and recoded variables.
    * Created analysis-ready datasets.
2. Exploratory data analysis
    * Generated descriptive statistics.
    * Created demographic summary tables.
    * Produced visualizations for age, gender, education, and mean behavioral scores.
3. Regression analysis
    * Used linear regression to examine the relationship between age and self-isolation behavior.
    * Used logistic regression to examine predictors of mask-wearing behavior.
4. Chi-square analysis
    * Tested the relationship between political party affiliation and mask-wearing behavior.
    * Produced crosstab tables and stacked bar charts.

Key Outputs

The repository includes:

* Cleaned analysis datasets
* Final regression tables
* Chi-square test results
* Descriptive tables
* Publication-style charts and figures
* A final Word document containing formatted results tables

Main Files

Data

* Dataset_JBPA_DOI_10.30636jbpa.32.182.dta — Original Dataverse dataset
* cleanedCDF.csv — Cleaned dataset used for analysis
* uncleaned_data.csv — Intermediate uncleaned CSV export

Scripts

* 0_cleanedCDF_cleaning.py — Data cleaning script
* 1_cleanedCDF_EDA.py — Exploratory data analysis script
* 2_cleanedCDF_DataAnalysis.py — Main data analysis script
* RegressionCDF.py — Regression analysis script
* TablesCDF.py — Table generation script
* Milestone4_Results_Outputs.py — Final results output script
* CDFstreamlit.py — Streamlit app script

Results and Figures

* FINAL_RESULTS_TABLES.docx — Final formatted results tables
* NEW_FINAL_RQ1_TABLE_READY.csv — Final RQ1 table
* NEW_FINAL_RQ2_TABLE_READY.csv — Final RQ2 table
* NEW_FINAL_RQ3_TABLE_READY.csv — Final RQ3 table
* NEW_RQ1_plot.png — RQ1 visualization
* NEW_RQ2_plot.png — RQ2 visualization
* NEW_RQ3_plot.png — RQ3 visualization

Tools Used

* Python
* pandas
* NumPy
* matplotlib
* seaborn
* statsmodels
* scipy
* Streamlit

Notes

This project was completed as part of a data analysis workflow using publicly available survey data. The repository is organized to show the progression from raw data to cleaned data, statistical analysis, tables, and visual results.

Data Source

The dataset used in this project comes from the Journal of Behavioral Public Administration Dataverse:

Dataset: Dataset_JBPA_DOI_10.30636jbpa.32.182.dta

The original dataset and associated do-file are included for reproducibility and reference.
