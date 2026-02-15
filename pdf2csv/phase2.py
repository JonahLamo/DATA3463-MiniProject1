import pandas as pd
import re

# Phase 2 is just to combine the three csv files we created in phase 1 into one csv file (merging on District_ID)

# read the three csv files into pandas dataframes
housing_df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\housing.csv")
transportation_df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\transportation.csv")
zoning_df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\zoning.csv")

# merge on District ID
merged_df = pd.merge(housing_df, transportation_df, on='District_ID', how='outer')
merged_df = pd.merge(merged_df, zoning_df, on='District_ID', how='outer')
# print(merged_df) # check to make sure the merge worked correctly

# merge the Data_Error columns into one column called Data_Errors
error_columns = [col for col in merged_df.columns if 'Data_Error' in col]
merged_df['Data_Errors'] = merged_df.apply(lambda row: '; '.join([str(row[col]) for col in error_columns if pd.notnull(row[col])]), axis=1)
# print(merged_df) # check to make sure the new column was created correctly, and that the values are correct

# remove the Data_Error columns
merged_df = merged_df.drop(columns=error_columns)
# print(merged_df) # check to make sure the columns were removed correctly

# Export the merged dataframe to a csv file, without the index
merged_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase2Outputs\pdf_output.csv", index=False)