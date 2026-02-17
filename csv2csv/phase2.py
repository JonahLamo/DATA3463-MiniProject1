import pandas as pd

# Phase 2 is just to combine the two csv files we created in phase 1 into one csv file (merging on District_ID)

economic_df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\economic.csv")
development_df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\development.csv")

# merge on District ID
merged_df = pd.merge(economic_df, development_df, on='District_ID', how='outer')
# print(merged_df)

# merge the Data_Error columns into one column called Data_Errors
error_columns = [col for col in merged_df.columns if 'Data_Error' in col]
merged_df['Data_Errors'] = merged_df.apply(lambda row: '; '.join([str(row[col]) for col in error_columns if pd.notnull(row[col])]), axis=1)
# print(merged_df) # check to make sure the new column was created correctly, and that the values are correct

# remove the Data_Error columns
merged_df = merged_df.drop(columns=error_columns)
# print(merged_df) # check to make sure the columns were removed correctly

# Export the merged dataframe to a csv file, without the index
merged_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase2Outputs\csv_output.csv", index=False)