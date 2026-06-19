import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import statsmodels.formula.api as smf

# page setup
st.set_page_config(page_title="COVID Social Distancing Dashboard", layout="wide")

st.title("COVID-19 Social Distancing and Self-Reporting Bias Dashboard")
st.write("Demographic comparative analysis using cleaned COVID social distancing data.")

# load data
df = pd.read_csv("cleanedCDF.csv")

# theme colors
navy = "#012169"
gold = "#C99700"

# sidebar
st.sidebar.header("Dashboard Controls")

section = st.sidebar.radio(
    "Choose section",
    [
        "Dataset Overview",
        "Table 1",
        "Crosstabs + Charts",
        "Linear Regression",
        "Logistic Regression"
    ]
)

# variables
group_vars = [
    "gender_group",
    "education_group",
    "employment_group",
    "income_group",
    "ideo_group",
    "party_group",
    "marital_group"
]

outcome_score_options = {
    "Self-Isolation Score": "soc_dist6",
    "Mask Score": "soc_dist7"
}

binary_outcome_options = {
    "Self-Isolation Willing": "iso_binary",
    "Mask Willing": "mask_binary"
}

# dataset overview
if section == "Dataset Overview":
    st.header("Dataset Overview")

    st.write("Dataset shape:", df.shape)

    st.subheader("First Rows")
    st.dataframe(df.head())

    st.subheader("Columns")
    st.write(df.columns.tolist())

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum().reset_index().rename(columns={"index": "Variable", 0: "Missing Count"}))

# table 1
elif section == "Table 1":
    st.header("Table 1 Summary Statistics")

    table_var = st.selectbox("Choose a variable", group_vars)

    counts = df[table_var].value_counts(dropna=False)
    percents = df[table_var].value_counts(normalize=True, dropna=False) * 100

    table1 = pd.DataFrame({
        "Count": counts,
        "Percent": percents.round(1)
    })

    st.dataframe(table1)

    st.subheader("Bar Chart")

    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", color=navy, ax=ax)
    ax.set_title(f"Distribution of {table_var}")
    ax.set_xlabel(table_var)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

# crosstabs and charts
elif section == "Crosstabs + Charts":
    st.header("Crosstabs and Charts")

    outcome_label = st.selectbox("Choose binary outcome", list(binary_outcome_options.keys()))
    outcome = binary_outcome_options[outcome_label]

    group_var = st.selectbox("Choose grouping variable", group_vars)

    chart_df = df[[group_var, outcome]].dropna().copy()

    st.subheader("Crosstab")
    tab = pd.crosstab(chart_df[group_var], chart_df[outcome], margins=True)
    st.dataframe(tab)

    st.subheader("Percent Table")
    percent_tab = pd.crosstab(
        chart_df[group_var],
        chart_df[outcome],
        normalize="index"
    ) * 100

    st.dataframe(percent_tab.round(1))

    st.subheader("Stacked Bar Chart")

    fig, ax = plt.subplots(figsize=(9, 5))
    percent_tab.plot(
        kind="bar",
        stacked=True,
        color=[gold, navy],
        ax=ax
    )
    ax.set_title(f"{outcome_label} by {group_var}")
    ax.set_xlabel(group_var)
    ax.set_ylabel("Percent")
    ax.legend(title=outcome_label)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

# linear regression
elif section == "Linear Regression":
    st.header("Linear Regression")

    score_label = st.selectbox("Choose score outcome", list(outcome_score_options.keys()))
    score_outcome = outcome_score_options[score_label]

    formula = (
        f"{score_outcome} ~ age + C(gender_group) + C(education_group) + "
        "C(employment_group) + C(income_group) + C(ideo_group) + "
        "C(party_group) + C(marital_group)"
    )

    st.subheader("Model Formula")
    st.code(formula)

    linear_model = smf.ols(formula, data=df).fit()

    st.subheader("Model Fit")
    st.write("R-squared:", round(linear_model.rsquared, 3))
    st.write("Adjusted R-squared:", round(linear_model.rsquared_adj, 3))

    results_df = pd.DataFrame({
        "Coefficient": linear_model.params,
        "P-value": linear_model.pvalues
    })

    st.subheader("Regression Coefficients")
    st.dataframe(results_df)

    st.subheader("Significant Coefficient Plot")

    plot_df = results_df.copy()
    conf = linear_model.conf_int()
    plot_df["Lower"] = conf[0]
    plot_df["Upper"] = conf[1]
    plot_df = plot_df[plot_df.index != "Intercept"]
    plot_df = plot_df[plot_df["P-value"] < 0.05]

    if plot_df.empty:
        st.write("No statistically significant predictors at p < 0.05.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.errorbar(
            plot_df["Coefficient"],
            plot_df.index,
            xerr=[
                plot_df["Coefficient"] - plot_df["Lower"],
                plot_df["Upper"] - plot_df["Coefficient"]
            ],
            fmt="o",
            color=navy
        )
        ax.axvline(x=0, color=gold)
        ax.set_title(f"Linear Regression Predictors of {score_label}")
        ax.set_xlabel("Coefficient")
        ax.set_ylabel("Predictor")
        plt.tight_layout()
        st.pyplot(fig)

# logistic regression
elif section == "Logistic Regression":
    st.header("Logistic Regression")

    st.write("Small subgroup counts can cause convergence issues, so the app removes the very small 'Other' gender group if present.")

    logit_df = df[df["gender_group"] != "Other"].copy()

    binary_label = st.selectbox("Choose binary outcome", list(binary_outcome_options.keys()))
    binary_outcome = binary_outcome_options[binary_label]

    formula = (
        f"{binary_outcome} ~ age + C(gender_group) + C(education_group) + "
        "C(ideo_group) + C(party_group)"
    )

    st.subheader("Model Formula")
    st.code(formula)

    try:
        logit_model = smf.logit(formula, data=logit_df).fit(disp=False)

        logit_results = pd.DataFrame({
            "Coefficient": logit_model.params,
            "P-value": logit_model.pvalues,
            "Odds Ratio": np.exp(logit_model.params)
        })

        st.subheader("Logistic Regression Results")
        st.dataframe(logit_results)

        st.subheader("Significant Odds Ratio Plot")

        plot_df = logit_results.copy()
        conf = logit_model.conf_int()
        plot_df["Lower"] = np.exp(conf[0])
        plot_df["Upper"] = np.exp(conf[1])
        plot_df = plot_df[plot_df.index != "Intercept"]
        plot_df = plot_df[plot_df["P-value"] < 0.05]

        if plot_df.empty:
            st.write("No statistically significant predictors at p < 0.05.")
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.errorbar(
                plot_df["Odds Ratio"],
                plot_df.index,
                xerr=[
                    plot_df["Odds Ratio"] - plot_df["Lower"],
                    plot_df["Upper"] - plot_df["Odds Ratio"]
                ],
                fmt="o",
                color=navy
            )
            ax.axvline(x=1, color=gold)
            ax.set_title(f"Logistic Regression Predictors of {binary_label}")
            ax.set_xlabel("Odds Ratio")
            ax.set_ylabel("Predictor")
            plt.tight_layout()
            st.pyplot(fig)

    except Exception as e:
        st.error("The logistic regression model did not run.")
        st.write(e)


'''
https://docs.streamlit.io/
https://cheat-sheet.streamlit.app/
https://1337skills.com/cheatsheets/statsmodels/
python -m streamlit run CDFstreamlit.py
'''