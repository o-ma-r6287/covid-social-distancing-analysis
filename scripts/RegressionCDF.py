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


