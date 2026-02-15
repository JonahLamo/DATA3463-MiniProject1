import pandas as pd
import numpy as np
import pdfplumber

# read the pdf file and extract the table, basically just the same as in lecture 8
with pdfplumber.open(r"DATA3463\DATA3463-MiniProject1\data\Urban_Growth_Report_2023.pdf") as pdf:
    # interested in the second page
    page = pdf.pages[1]
    table = page.extract_table()

# convert the table to a pandas dataframe so its easier to work with, the first row of the table is the header, so we use that as the column names
df = pd.DataFrame(table[1:], columns=table[0])
# print(df) # quick check to see if everything worked, also needed to see what parts of the table we need to clean up

# Create the YoY%_Housing column, same stuff as before, but we have to do it for the 'Housing' column
housing_2022 = pd.to_numeric(df['Units_2022'], errors='coerce')
housing_2023 = pd.to_numeric(df['Units_2023'], errors='coerce')
df['YoY%_Housing'] = round((housing_2023 - housing_2022) / housing_2022 * 100, 1)
# print(df) # Check to make sure the new column was created correctly, and that the values are correct

# We are interested in the 'Green_Space_2023_sq_m' column too this time so we have to fix the "NULL" string there too
df['Green_Space_2023_sq_m'] = pd.to_numeric(df['Green_Space_2023_sq_m'], errors='coerce')

# add Data_Error column, same as last time, but also for the 'Green_Space_2023_sq_m' column this time
conditions = [
    df['YoY%_Housing'].isna() & df['Green_Space_2023_sq_m'].isna(),
    df['YoY%_Housing'].isna(),
    df['Green_Space_2023_sq_m'].isna()
]
choices = [
    'missing_value(YoY%_Housing); missing_value(Green_Space_2023_sq_m)',
    'missing_value(YoY%_Housing)',
    'missing_value(Green_Space_2023_sq_m)'
]
df['Data_Error'] = np.select(conditions, choices, default='')
# print(df) # Check to make sure the new column was created correctly, and that the values are correct

# Make a new dataframe with only the columns we want to export to csv, which are the 'District_ID', 'YoY%_Housing', and 'Data_Error' columns
new_df = df[['District_ID', 'YoY%_Housing', 'Green_Space_2023_sq_m', 'Data_Error']]
# print(new_df) # make sure the new dataframe looks correct

# Export the new dataframe to a csv file, without the index
new_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\housing.csv", index=False)