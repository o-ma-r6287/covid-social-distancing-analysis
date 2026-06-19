import pandas as pd

df = pd.read_csv("cleanedCDF.csv")

print(df.columns.tolist())
print(df.shape)