import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Note:
This document includes a compiled version of all code used in this project. 
The code is also organized into separate scripts for data cleaning, exploratory data analysis, 
and final data analysis.

Because this is a compiled version, some imports, dataset loading steps,
and variable creation steps may appear more than once.
'''

#Cleaned Data
df = pd.read_csv("cleanedCDF.csv")

#Table 1
table1_rows = []

#Sample size
table1_rows.append(["Total Sample Size", f"{len(df)}"])

#Age mean and SD
age_mean = df["age"].mean()
age_sd = df["age"].std()
table1_rows.append(["Age (Mean ± SD)", f"{age_mean:.1f} ± {age_sd:.1f}"])


#Counts/Percentages
def add_categorical(var_name, header_name):
    table1_rows.append([header_name, ""])

    counts = df[var_name].value_counts(dropna=False)

    for category, count in counts.items():
        percent = (count / len(df)) * 100
        table1_rows.append(
            [f"   {category}", f"{count} ({percent:.1f}%)"]
        )


#Grouped Vars
add_categorical("gender_group", "Gender")
add_categorical("education_group", "Education")
add_categorical("employment_group", "Employment")
add_categorical("income_group", "Income")
add_categorical("ideo_group", "Political Ideology")
add_categorical("party_group", "Party Identification")
add_categorical("marital_group", "Marital Status")

#Outcomes
table1_rows.append([
    "Self-Isolation Score (Mean ± SD)",
    f'{df["soc_dist6"].mean():.2f} ± {df["soc_dist6"].std():.2f}'
])
table1_rows.append([
    "Mask Score (Mean ± SD)",
    f'{df["soc_dist7"].mean():.2f} ± {df["soc_dist7"].std():.2f}'
])

# Binary willingness
df["iso_binary"] = (df["soc_dist6"] >= 6).astype(int)
df["mask_binary"] = (df["soc_dist7"] >= 6).astype(int)
iso_yes = df["iso_binary"].sum()
mask_yes = df["mask_binary"].sum()
table1_rows.append([
    "Willing to Self-Isolate (6+)",
    f"{iso_yes} ({iso_yes / len(df) * 100:.1f}%)"
])
table1_rows.append([
    "Willing to Wear Mask (6+)",
    f"{mask_yes} ({mask_yes / len(df) * 100:.1f}%)"
])

table1 = pd.DataFrame(table1_rows, columns=["Characteristic", "Value"])
print(table1)
table1.to_csv("Table1_BIOS584.csv", index=False)

table1 = pd.read_csv("Table1_BIOS584.csv")

#====================
#Png of table
#====================
#moduel 9
fig, ax = plt.subplots(figsize=(10, 14))

# Remove axes
ax.axis("off")

# Build table
tbl = ax.table(
    cellText=table1.values,
    colLabels=table1.columns,
    cellLoc="left",
    colLoc="left",
    loc="center"
)

# Styling
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.5)

# Bold header row
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold")
        cell.set_facecolor("#D9E6F2")

#Title
plt.title(
    "Table 1. Characteristics of Participants Included in Analysis",
    fontsize=14,
    weight="bold",
    pad=20
)

#Save as PNG
plt.savefig("Table1_BIOS584.png", dpi=300, bbox_inches="tight")
plt.show()
print("Table 1 PNG has been saved.")

#Load cleaned dataset
df = pd.read_csv("cleanedCDF.csv")

#6 or higher = willing
df["mask_binary"] = (df["soc_dist7"] >= 6).astype(int)
df["iso_binary"] = (df["soc_dist6"] >= 6).astype(int)

#N and (%) table
def make_percent_table(data, group_var, binary_var):
    willing_n = data.groupby(group_var)[binary_var].sum()
    total_n = data[group_var].value_counts().sort_index()
    percent = (willing_n / total_n * 100).round(1)

    table = pd.DataFrame({
        "Category": total_n.index,
        "n (%)": willing_n.astype(int).astype(str) + " (" + percent.astype(str) + "%)"
    })

    table = table.reset_index(drop=True)
    return table

#Save table as styled PNG
def save_table_png(table_df, title, filename):
    fig, ax = plt.subplots(figsize=(8, 0.6 * len(table_df) + 1.5))
    ax.axis("off")

    tbl = ax.table(
        cellText=table_df.values,
        colLabels=table_df.columns,
        cellLoc="center",
        loc="center"
    )

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.5)

    #Theme colors (NAVY/WHITE/GOLD/BLACK)
    header_color = "#0A2342"   #navy
    header_text = "white"
    body_text = "black"
    alt_row = "#FFF4CC"        #light gold
    white_row = "white"
    border_color = "#0A2342"   #navy
    title_color = "#0A2342"    #navy

    #Style cells
    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor(border_color)
        cell.set_linewidth(1)

        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color=header_text, weight="bold")
        else:
            if row % 2 == 1:
                cell.set_facecolor(alt_row)
            else:
                cell.set_facecolor(white_row)
            cell.set_text_props(color=body_text)

#Bolded and no vertical
    plt.title(title, fontsize=12, weight="bold", color=title_color, pad=12)
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

#Tables

#Gender
mask_gender = make_percent_table(df, "gender", "mask_binary")
iso_gender = make_percent_table(df, "gender", "iso_binary")

#Education
mask_education = make_percent_table(df, "education", "mask_binary")
iso_education = make_percent_table(df, "education", "iso_binary")

#Political ideology
mask_ideo = make_percent_table(df, "pol_ideo", "mask_binary")
iso_ideo = make_percent_table(df, "pol_ideo", "iso_binary")

#Party ID
mask_party = make_percent_table(df, "pol_pident", "mask_binary")
iso_party = make_percent_table(df, "pol_pident", "iso_binary")

#Employment
mask_employment = make_percent_table(df, "employment", "mask_binary")
iso_employment = make_percent_table(df, "employment", "iso_binary")

#Marital status
mask_marital = make_percent_table(df, "marr_status", "mask_binary")
iso_marital = make_percent_table(df, "marr_status", "iso_binary")

#Save tables as PNG files

save_table_png(mask_gender, "Mask Wearing by Gender", "mask_gender_table.png")
save_table_png(iso_gender, "Self-Isolation by Gender", "iso_gender_table.png")

save_table_png(mask_education, "Mask Wearing by Education", "mask_education_table.png")
save_table_png(iso_education, "Self-Isolation by Education", "iso_education_table.png")

save_table_png(mask_ideo, "Mask Wearing by Political Ideology", "mask_ideo_table.png")
save_table_png(iso_ideo, "Self-Isolation by Political Ideology", "iso_ideo_table.png")

save_table_png(mask_party, "Mask Wearing by Party ID", "mask_party_table.png")
save_table_png(iso_party, "Self-Isolation by Party ID", "iso_party_table.png")

save_table_png(mask_employment, "Mask Wearing by Employment", "mask_employment_table.png")
save_table_png(iso_employment, "Self-Isolation by Employment", "iso_employment_table.png")

save_table_png(mask_marital, "Mask Wearing by Marital Status", "mask_marital_table.png")
save_table_png(iso_marital, "Self-Isolation by Marital Status", "iso_marital_table.png")

print("All navy/gold themed table PNGs have been saved.")

#Save percent bar charts
def save_percent_bar(data, group_var, binary_var, title, filename):

    percent = data.groupby(group_var)[binary_var].mean() * 100
    percent = percent.sort_index()

    plt.figure(figsize=(8,5))
    plt.bar(percent.index.astype(str), percent.values,
            color="#0A2342", edgecolor="black")

    plt.title(title, fontsize=12, weight="bold")
    plt.xlabel(group_var)
    plt.ylabel("Percent (%) willing")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0,100)

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

#Best charts
save_percent_bar(df, "gender", "mask_binary", "Percent Willing to Wear Mask by Gender", "mask_gender_chart.png")
save_percent_bar(df, "pol_ideo", "mask_binary", "Percent Willing to Wear Mask by Political Ideology", "mask_ideo_chart.png")
save_percent_bar(df, "pol_pident", "iso_binary", "Percent Willing to Self-Isolate by Party ID", "iso_party_chart.png")
save_percent_bar(df, "education", "mask_binary", "Percent Willing to Wear Mask by Education", "mask_education_chart.png")

#No more errors :))

'''
https://www.w3schools.com/datascience/ds_stat_intro.asp

'''

table1 = pd.read_csv("Table1_BIOS584.csv")

#Remove "nan"
table1["Value"] = table1["Value"].replace("nan", "")
table1["Value"] = table1["Value"].fillna("")

#Headers
header_rows = [
    "Gender",
    "Education",
    "Employment",
    "Income",
    "Political Ideology",
    "Party Identification",
    "Marital Status"
]

#PNG of table
fig, ax = plt.subplots(figsize=(12, 12)) #(11, 14) too long (16, 8)/(18, 7) words go into the chart
ax.axis("off")
tbl = ax.table(
    cellText=table1.values,
    colLabels=table1.columns,
    cellLoc="left",
    colLoc="left",
    loc="center"
)

#Font
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 1.55) #The table was too smushed together x = fatter y = taller

#Theme colors
navy = "#0A2342"
gold_light = "#FFF4CC"
header_fill = "#D9E6F2"
white = "white"
black = "black"

#Styling the table to fit theme and bold title amd headers
for (row, col), cell in tbl.get_celld().items():

    # Top header row
    if row == 0:
        cell.set_text_props(weight="bold", color=black)
        cell.set_facecolor(header_fill)

    # Data rows
    else:
        row_label = table1.iloc[row - 1, 0]

        # Section headers like Gender, Education.........
        if row_label in header_rows:
            cell.set_text_props(weight="bold", color=black)
            cell.set_facecolor(gold_light)
        else:
            cell.set_facecolor(white)

#Title
plt.title(
    "Table 1. Characteristics of Participants Included in Analysis",
    fontsize=15,
    weight="bold",
    pad=20
)

#PNG
plt.savefig("Table1_BIOS584_clean.png", dpi=300, bbox_inches="tight")
plt.show()


df = pd.read_csv("cleanedCDF.csv")
print(df.head())
print(df.shape)

#6 or higher = willing
df["mask_binary"] = (df["soc_dist7"] >= 6).astype(int)
df["iso_binary"] = (df["soc_dist6"] >= 6).astype(int)

print(df[["soc_dist7", "mask_binary", "soc_dist6", "iso_binary"]].head())

#Percent willing by gender
print("\nMask Wearing by Gender")
print(df.groupby("gender")["mask_binary"].mean() * 100)

print("\nSelf-Isolation by Gender")
print(df.groupby("gender")["iso_binary"].mean() * 100)

#Percent willing by education
print("\nMask Wearing by Education")
print(df.groupby("education")["mask_binary"].mean() * 100)

print("\nSelf-Isolation by Education")
print(df.groupby("education")["iso_binary"].mean() * 100)

#Percent willing by political ideology
print("\nMask Wearing by Political Ideology")
print(df.groupby("pol_ideo")["mask_binary"].mean() * 100)

print("\nSelf-Isolation by Political Ideology")
print(df.groupby("pol_ideo")["iso_binary"].mean() * 100)

#Percent willing by party identification
print("\nMask Wearing by Party ID")
print(df.groupby("pol_pident")["mask_binary"].mean() * 100)

print("\nSelf-Isolation by Party ID")
print(df.groupby("pol_pident")["iso_binary"].mean() * 100)


df = pd.read_csv("cleanedCDF.csv")

# Create figure
plt.figure(figsize=(9,6))

# Scatterplot
plt.scatter(
    df["age"],
    df["soc_dist6"],
    color="#0A2342",      # navy blue
    alpha=0.15,
    s=15,
    label="Participants"
)

# Line of best fit
x = df["age"]
y = df["soc_dist6"]

m, b = np.polyfit(x, y, 1)

plt.plot(
    x,
    m*x + b,
    color="#D4AF37",      # gold
    linewidth=3,
    label="Best Fit Line"
)

# Titles and labels
plt.title(
    "Association Between Age and Self-Isolation Score",
    fontsize=16,
    weight="bold",
    color="#0A2342"
)

plt.xlabel("Age (Years)", fontsize=12)
plt.ylabel("Self-Isolation Score (Low to High Willingness)", fontsize=12)

# Grid
plt.grid(alpha=0.20)

# Legend
plt.legend(frameon=False)

# Clean layout
plt.tight_layout()

# Save image
plt.savefig(
    "age_selfisolation_regression_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

'''
beginners_python_cheat_sheet_pcc_matplotlib.pdf
beginners_python_cheat_sheet_pcc_plotly.pdf
'''

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

#Linear and logistic regression for the final project

#Load cleaned dataset
df = pd.read_csv("cleanedCDF.csv")

#Check data
print(df.head())
print(df.shape)

#---------------------------------------------------
#LINEAR REGRESSION
#OLS = Ordinary Least Squares
#Uses original 1-11 willingness scores
#---------------------------------------------------

#Model 1: self-isolation score
linear_iso = smf.ols(
    "soc_dist6 ~ age + C(gender_group) + C(education_group) + C(employment_group) + C(income_group) + C(ideo_group) + C(party_group) + C(marital_group)",
    data=df
).fit()

print("\nLINEAR REGRESSION MODEL 1: SELF-ISOLATION SCORE")
print(linear_iso.summary())

print("\nModel 1 coefficients")
print(linear_iso.params)

print("\nModel 1 p-values")
print(linear_iso.pvalues)

print("\nModel 1 R-squared")
print(linear_iso.rsquared)

print("\nModel 1 Adjusted R-squared")
print(linear_iso.rsquared_adj)

#Model 2: mask score
linear_mask = smf.ols(
    "soc_dist7 ~ age + C(gender_group) + C(education_group) + C(employment_group) + C(income_group) + C(ideo_group) + C(party_group) + C(marital_group)",
    data=df
).fit()

print("\nLINEAR REGRESSION MODEL 2: MASK SCORE")
print(linear_mask.summary())

print("\nModel 2 coefficients")
print(linear_mask.params)

print("\nModel 2 p-values")
print(linear_mask.pvalues)

print("\nModel 2 R-squared")
print(linear_mask.rsquared)

print("\nModel 2 Adjusted R-squared")
print(linear_mask.rsquared_adj)

#For logistic regression, tiny subgroup counts can cause convergence issues. (ERROR MESSAGE)
#Remove the very small "Other" gender group for more stable estimation.
logit_df = df[df["gender_group"] != "Other"].copy()

#---------------------------------------------------
#LOGISTIC REGRESSION
#Uses binary willing variables
#1 = willing (6 or higher)        >5
#0 = not willing (1-5)           =<5
#---------------------------------------------------

#Model 3: self-isolation willing yes/no
logit_iso = smf.logit(
    "iso_binary ~ age + C(gender_group) + C(education_group) + C(ideo_group) + C(party_group)",
    data=logit_df
).fit()

print("\nLOGISTIC REGRESSION MODEL 3: SELF-ISOLATION WILLING")
print(logit_iso.summary())

print("\nModel 3 coefficients")
print(logit_iso.params)

print("\nModel 3 p-values")
print(logit_iso.pvalues)

#Odds ratios for Model 3
iso_odds_ratios = np.exp(logit_iso.params)
print("\nModel 3 odds ratios")
print(iso_odds_ratios)

#Model 4: mask willing yes/no
logit_mask = smf.logit(
    "mask_binary ~ age + C(gender_group) + C(education_group) + C(ideo_group) + C(party_group)",
    data=logit_df
).fit()

print("\nLOGISTIC REGRESSION MODEL 4: MASK WILLING")
print(logit_mask.summary())

print("\nModel 4 coefficients")
print(logit_mask.params)

print("\nModel 4 p-values")
print(logit_mask.pvalues)

#Odds ratios for Model 4
mask_odds_ratios = np.exp(logit_mask.params)
print("\nModel 4 odds ratios")
print(mask_odds_ratios)

#Regression Outputs

#Linear regression summary table
linear_results = pd.DataFrame({
    "Linear Isolation Coef": linear_iso.params,
    "Linear Isolation p": linear_iso.pvalues,
    "Linear Mask Coef": linear_mask.params,
    "Linear Mask p": linear_mask.pvalues
})
linear_results.to_csv("linear_regression_results.csv", index=False)

#Logistic regression summary table
logit_results = pd.DataFrame({
    "Logit Isolation Coef": logit_iso.params,
    "Logit Isolation p": logit_iso.pvalues,
    "Logit Isolation OR": np.exp(logit_iso.params),
    "Logit Mask Coef": logit_mask.params,
    "Logit Mask p": logit_mask.pvalues,
    "Logit Mask OR": np.exp(logit_mask.params)
})
logit_results.to_csv("logistic_regression_results.csv", index=False)

#Made it to the end:)
print("\nRegression results (files) have been saved.")

# -----------------------------------
# REGRESSION CHARTS FOR POSTER
# -----------------------------------

navy = "#0A2342"
gold = "#D4AF37"

#Linear coefficient plot + logistic odds ratio plot
#Function to pull regression results into a dataframe
def make_regression_df(model, model_type):
    results_df = pd.DataFrame({
        "term": model.params.index,
        "coef": model.params.values,
        "pvalue": model.pvalues.values
    })

    conf = model.conf_int()
    results_df["lower"] = conf[0].values
    results_df["upper"] = conf[1].values

    #Remove intercept
    results_df = results_df[results_df["term"] != "Intercept"]

    #Keep only significant predictors
    results_df = results_df[results_df["pvalue"] < 0.05]

    #For logistic regression, convert to odds ratios
    if model_type == "logit":
        results_df["coef"] = np.exp(results_df["coef"])
        results_df["lower"] = np.exp(results_df["lower"])
        results_df["upper"] = np.exp(results_df["upper"])

    return results_df

#---------------------------------------------------
#LINEAR REGRESSION COEFFICIENT PLOT
#Use self-isolation linear model
#---------------------------------------------------

linear_plot_df = make_regression_df(linear_iso, "linear")

plt.figure(figsize=(10, 6))
plt.errorbar(
    linear_plot_df["coef"],
    linear_plot_df["term"],
    xerr=[
        linear_plot_df["coef"] - linear_plot_df["lower"],
        linear_plot_df["upper"] - linear_plot_df["coef"]
    ],
    fmt="o",
    color=navy
)

plt.axvline(x=0, color=gold)
plt.title("Linear Regression Predictors of Self-Isolation")
plt.xlabel("Coefficient")
plt.ylabel("Predictor")
plt.tight_layout()
plt.savefig("linear_regression_coefficient_plot.png", dpi=300)
plt.close()

#---------------------------------------------------
#LOGISTIC REGRESSION FOREST PLOT
#Use mask logistic model
#---------------------------------------------------

logit_plot_df = make_regression_df(logit_mask, "logit")

plt.figure(figsize=(10, 6))

#Coefficient plot with confidence interval bars
#Dot = estimated regression effect
#Horizontal lines = 95% confidence intervals
plt.errorbar(
    logit_plot_df["coef"],
    logit_plot_df["term"],
    xerr=[
        logit_plot_df["coef"] - logit_plot_df["lower"],
        logit_plot_df["upper"] - logit_plot_df["coef"]
    ],
    fmt="o",
    color=navy
)

plt.axvline(x=1, color=gold)
plt.title("Logistic Regression Predictors of Mask Willingness")
plt.xlabel("Odds Ratio")
plt.ylabel("Predictor")
plt.tight_layout()
plt.savefig("logistic_regression_forest_plot.png", dpi=300)
plt.close()

'''
beginners_python_cheat_sheet_pcc_matplotlib.pdf
beginners_python_cheat_sheet_pcc_plotly.pdf
https://pandas.pydata.org/docs/
https://www.statsmodels.org/stable/index.html
https://www.statsmodels.org/stable/generated/statsmodels.formula.api.ols.html
https://www.statsmodels.org/stable/generated/statsmodels.formula.api.logit.html
https://www.statsmodels.org/stable/example_formulas.html
https://numpy.org/doc/stable/
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html
'''
