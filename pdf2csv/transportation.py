import pandas as pd
import numpy as np
import pdfplumber

# read the pdf file and extract the table, basically just the same as in lecture 8
with pdfplumber.open(r"DATA3463\DATA3463-MiniProject1\data\Infrastructure_Transportation_Summary_2024.pdf") as pdf:
    # interested in the second page
    page = pdf.pages[1]
    table = page.extract_table()

# convert the table to a pandas dataframe so its easier to work with, the first row of the table is the header, so we use that as the column names
df = pd.DataFrame(table[1:], columns=table[0])
# print(df) # quick check to see if everything worked, also needed to see what parts of the table we need to clean up

# Create the YoY%_Road and YoY%_Bike columns
# While the 'YoY_%' columns exist with the same information, it is easier to calculate in a new column that it is to clean up the 'YoY_%' columns
# This is just the same process as in zoning.py, but we have to do it for both the 'Road' and 'Bike' columns
df['Road_2024_km'] = pd.to_numeric(df['Road_2024_km'], errors='coerce')
df['Road_2023_km'] = pd.to_numeric(df['Road_2023_km'], errors='coerce')
df['Bike_2024_km'] = pd.to_numeric(df['Bike_2024_km'], errors='coerce')
df['Bike_2023_km'] = pd.to_numeric(df['Bike_2023_km'], errors='coerce')

df["Data_Error"] = df.apply(
    lambda row: "; ".join(
        [f"missing_value({col})" for col in row.index[row.isna()]]
    ),
    axis=1
)
# print(df) # Check to make sure the new column was created correctly, and that the values are correct

df['YoY%_Bike'] = round((df['Bike_2024_km'] - df['Bike_2023_km']) / df['Bike_2023_km'] * 100, 1)
df['YoY%_Road'] = round((df['Road_2024_km'] - df['Road_2023_km']) / df['Road_2023_km'] * 100, 1)
# print(df) # Check to make sure the new columns were created correctly, and that the values are correct

# Make a new dataframe with only the columns we want to export to csv, which are the 'District_ID', 'YoY%_Road', 'YoY%_Bike', and 'Data_Error' columns
new_df = df[['District_ID', 'YoY%_Road', 'YoY%_Bike', 'Data_Error']]
# print(new_df) # make sure the new dataframe looks correct

# Export the new dataframe to a csv file, without the index
new_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\transportation.csv", index=False)