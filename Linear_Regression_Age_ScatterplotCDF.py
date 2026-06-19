# -----------------------------------------
# SCATTERPLOT + LINE OF BEST FIT
# Poster-ready Figure 3
# Age vs Self-Isolation Score
# -----------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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