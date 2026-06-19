import pandas as pd
import matplotlib.pyplot as plt

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
