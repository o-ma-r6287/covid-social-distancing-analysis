import pandas as pd

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