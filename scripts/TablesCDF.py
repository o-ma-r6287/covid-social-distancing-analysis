import pandas as pd
import matplotlib.pyplot as plt

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