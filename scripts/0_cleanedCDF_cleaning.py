#Project: Effects of demographic variables on self-isolation and mask wearing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

#Load dataset
df = pd.read_stata("/Users/omara-rahman/Desktop/Semester 2 MPH/Computer based class/Python BIOS 584/Final_project/dataverse_files 2/Dataset_JBPA_DOI_10.30636jbpa.32.182.dta")

#Check variables causing issues
print(df["soc_dist6"].dtype)
print(df["soc_dist6"].unique())

print(df["soc_dist7"].dtype)
print(df["soc_dist7"].unique())

print(df["byear"].dtype)
print(df["byear"].head())

#Keep only variables needed
df = df[[
    "education",
    "gender",
    "byear",
    "employment",
    "hhinc",
    "pol_ideo",
    "pol_pident",
    "marr_status",
    "soc_dist6",
    "soc_dist7"
]]

#Fix soc_dist6 scale
df["soc_dist6"] = df["soc_dist6"].astype(str)
df["soc_dist6"] = df["soc_dist6"].replace({
    "Not at all willing": 1,
    "2.0": 2,
    "3.0": 3,
    "4.0": 4,
    "5.0": 5,
    "6.0": 6,
    "7.0": 7,
    "8.0": 8,
    "9.0": 9,
    "10": 10,
    "Entirely willing": 11,
    "nan": None
})
df["soc_dist6"] = df["soc_dist6"].astype(float)

#Fix soc_dist7 scale
df["soc_dist7"] = df["soc_dist7"].astype(str)
df["soc_dist7"] = df["soc_dist7"].replace({
    "Not at all willing": 1,
    "2.0": 2,
    "3.0": 3,
    "4.0": 4,
    "5.0": 5,
    "6.0": 6,
    "7.0": 7,
    "8.0": 8,
    "9.0": 9,
    "10": 10,
    "Entirely willing": 11,
    "nan": None
})
df["soc_dist7"] = df["soc_dist7"].astype(float)

#Fix birth year and create age
df["byear"] = df["byear"].astype(str)
df["byear"] = df["byear"].replace("nan", None)
df["byear"] = df["byear"].astype(float)

#Survey was taken in 2020
df["age"] = 2020 - df["byear"]

#Create binary outcomes
#1 = willing (6 or higher)
#0 = not willing (1-5)
df["mask_binary"] = (df["soc_dist7"] >= 6).astype(int)
df["iso_binary"] = (df["soc_dist6"] >= 6).astype(int)

#Remove ideology response not useful for analysis
df["pol_ideo"] = df["pol_ideo"].replace(
    "I haven't thought much about this",
    np.nan
)

#Gender -> Male / Female / Other
df["gender_group"] = df["gender"].astype(str).replace({
    "Male": "Male",
    "Female": "Female",
    "Nonbinary/third gender": "Other",
    "Prefer not to say": "Other",
    "Prefer to self-describe": "Other"
})

#Education -> Some college or less / College degree / Advanced degree
df["education_group"] = df["education"].astype(str).replace({
    "Less than high school": "Some college or less",
    "High school graduate": "Some college or less",
    "Some college": "Some college or less",
    "2-year degree": "College degree",
    "4-year degree": "College degree",
    "Professional degree": "Advanced degree",
    "Doctorate": "Advanced degree"
})

#Income -> Less than 50k / 50k to 99k / 100k+
df["income_group"] = df["hhinc"].astype(str).replace({
    "Less than $10,000": "Less than 50k",
    "$10,000 - $19,999": "Less than 50k",
    "$20,000 - $29,999": "Less than 50k",
    "$30,000 - $39,999": "Less than 50k",
    "$40,000 - $49,999": "Less than 50k",
    "$50,000 - $59,999": "50k to 99k",
    "$60,000 - $69,999": "50k to 99k",
    "$70,000 - $79,999": "50k to 99k",
    "$80,000 - $89,999": "50k to 99k",
    "$90,000 - $99,999": "50k to 99k",
    "$100,000 - $109,999": "100k+",
    "$110,000 - $124,999": "100k+",
    "$125,000 or more": "100k+"
})

#Political ideology -> Liberal / Moderate / Conservative
df["ideo_group"] = df["pol_ideo"].astype(str).replace({
    "Extremely liberal": "Liberal",
    "Slightly liberal": "Liberal",
    "Liberal": "Liberal",
    "Moderate; middle of the road": "Moderate",
    "Slightly conservative": "Conservative",
    "Conservative": "Conservative",
    "Extremely conservative": "Conservative"
})

#Party ID -> Democrat / Republican / Other or independent
df["party_group"] = df["pol_pident"].astype(str).replace({
    "Democrat": "Democrat",
    "Republican": "Republican",
    "Independent with no party preference": "Other or independent",
    "Independent, but lean Democrat": "Other or independent",
    "Independent, but lean Republican": "Other or independent",
    "Other": "Other or independent"
})

#Employment -> Working / Not working
df["employment_group"] = df["employment"].astype(str).replace({
    "Employed full-time in an organization": "Working",
    "Employed part-time in an organization": "Working",
    "Self-employed": "Working",
    "Student": "Not working",
    "Retired": "Not working",
    "Currently unable to work": "Not working",
    "Unemployed, looking for work": "Not working",
    "Unemployed, not looking for work": "Not working"
})

#Marital status -> Married / Not married
df["marital_group"] = df["marr_status"].astype(str).replace({
    "Married or in a domestic partnership": "Married",
    "Single, never married": "Not married",
    "Divorced": "Not married",
    "Widowed": "Not married",
    "Separated": "Not married"
})

#Check grouped variables
print(df[[
    "mask_binary",
    "iso_binary",
    "gender_group",
    "education_group",
    "income_group",
    "ideo_group",
    "party_group",
    "employment_group",
    "marital_group"
]].head())

#Remove missing rows
df = df.dropna()

#Check cleaned data
print(df.shape)
print(df.head())
print(df.describe())

#Check coding for variables
for col in df.columns:
    print("\n", col)
    print(df[col].value_counts())

#---------------------------------------------------
#OLS = Ordinary Least Squares linear regression
#---------------------------------------------------

#Model 1 self-isolation
model1 = smf.ols(
    "soc_dist6 ~ age + C(gender) + C(education) + C(employment) + C(hhinc) + C(pol_ideo) + C(pol_pident) + C(marr_status)",
    data=df
).fit()
print("\nMODEL 1")
print(model1.summary())

#Model 2 face mask
model2 = smf.ols(
    "soc_dist7 ~ age + C(gender) + C(education) + C(employment) + C(hhinc) + C(pol_ideo) + C(pol_pident) + C(marr_status)",
    data=df
).fit()

print("\nMODEL 2")
print(model2.summary())

#Important results
print(model1.params)
print(model1.pvalues)
print(model1.rsquared)
print(model1.rsquared_adj)

print(model2.params)
print(model2.pvalues)
print(model2.rsquared)
print(model2.rsquared_adj)

#Figures

#Age histogram
plt.figure()
plt.hist(df["age"], bins=15)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.savefig("age_distribution_pythonf.png", dpi=300, bbox_inches="tight")
plt.show()

#Gender bar chart
plt.figure()
df["gender"].value_counts().plot(kind="bar")
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.savefig("gender_pythonf.png", dpi=300, bbox_inches="tight")
plt.show()

#Education bar chart
plt.figure()
df["education"].value_counts().plot(kind="bar")
plt.title("Education Level")
plt.xlabel("Education")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.savefig("education_pythonf.png", dpi=300, bbox_inches="tight")
plt.show()

#Average outcome scores
plt.figure()
means = [df["soc_dist6"].mean(), df["soc_dist7"].mean()]
plt.bar(["Self-Isolation", "Mask Wearing"], means)
plt.title("Average Outcome Scores")
plt.ylabel("Mean Score")
plt.savefig("mean_score_pythonf.png", dpi=300, bbox_inches="tight")
plt.show()

df.to_csv("cleanedCDF.csv", index=False)
