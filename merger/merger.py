import pandas as pd

# Get the csvs we need to merge
pdfs = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/pdf_output.csv")
jsons = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/json_output.csv")
csvs = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/csv_output.csv")

# merge the csvs on District_ID, using an outer join to keep all records
merged = pd.merge(pdfs, jsons, on="District_ID", how="outer")
merged = pd.merge(merged, csvs, on="District_ID", how="outer")
# print(merged.head()) # check to make sure the merge worked correctly

# Merge the Data_Errors columns into one Data_Error column, combining the error messages if both columns have errors
error_columns = [col for col in merged.columns if 'Data_Errors' in col]
merged['Data_Error'] = merged.apply(lambda row: '; '.join([str(row[col]) for col in error_columns if pd.notnull(row[col])]), axis=1)
merged = merged.drop(columns=error_columns)
# print(merged.head()) # check to make sure the new column was created correctly, that the values are correct, and the old error columns were dropped

merged.to_csv(r"DATA3463/DATA3463-MiniProject1/data/phase3Outputs/merged_output.csv", index=False)