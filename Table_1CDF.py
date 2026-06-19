import pandas as pd
import matplotlib.pyplot as plt

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