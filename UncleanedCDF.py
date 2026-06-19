import pandas as pd

df = pd.read_stata("/Users/omara-rahman/Desktop/Semester 2 MPH/Computer based class/Python BIOS 584/Final_project/dataverse_files 2/Dataset_JBPA_DOI_10.30636jbpa.32.182.dta")

df.to_csv("uncleaned_data.csv", index=False)