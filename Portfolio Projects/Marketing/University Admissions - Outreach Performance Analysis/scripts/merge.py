# LEFT MERGED
import pandas as pd

# Applicant Dataset - Adding a column at the start named Sl_ID and filling it with unique values starting from 1 uptil the number of rows in the dataset
df1 = pd.read_excel("ApplicantData.xlsx")
df1.insert(0,"SL_ID", range(1, len(df1) + 1))


# Outreach Dataset - Adding a column at the start named SL_ID and filling it with unique values starting from 1 uptil the number of rows in the dataset
df2 = pd.read_excel("OutreachData.xlsx")
df2.insert(0,"SL_ID", range(1, len(df2) + 1))

merge_df = pd.merge(df1, df2, on="SL_ID", how = "left")


print(f"Applicant rows: {len(df1)}")
print(f"Outreach rows: {len(df2)}")
print(f"Merged rows: {len(merge_df)}")

# Saving the merged dataset to a new Excel file
merge_df.to_excel("Merged_LEFT.xlsx", index = False)


# Mergin the Merged_Left Datset with the Campaign Dataset 
import pandas as pd
xlsx_file = "AOC.xlsx"

df1 = pd.read_excel("Merged_LEFT.xlsx")
df2 = pd.read_excel("CampaignData.xlsx", sheet_name = "Campaign_Data_Fixed")

merge_df = pd.merge(df1,df2, left_on = "Campaign_ID", right_on = "ID",how = "left")


print(f"AO_merged rows:" , len(df1))
print(f"Campaign_Data_rows, sheet = 2 :" , len(df2))
print(f"Merged_All_rows:", len(merge_df))

merge_df.to_excel(xlsx_file, index = False)