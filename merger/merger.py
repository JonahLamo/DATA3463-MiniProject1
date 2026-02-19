import pandas as pd

# Get the csvs we need to merge
pdfs = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/pdf_output.csv")
jsons = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/json_output.csv")
csvs = pd.read_csv(r"DATA3463/DATA3463-MiniProject1/data/phase2Outputs/csv_output.csv")

# merge the csvs on District_ID, using an outer join to keep all records
merged = pd.merge(pdfs, jsons, on="District_ID", how="outer")
merged = pd.merge(merged, csvs, on="District_ID", how="outer")
# print(merged) # check to make sure the merge worked correctly

# Merge the Data_Errors columns into one Data_Error column, combining the error messages if both columns have errors
error_columns = [col for col in merged.columns if 'Data_Errors' in col]
merged['Data_Error'] = merged.apply(lambda row: '; '.join([str(row[col]) for col in error_columns if pd.notnull(row[col])]), axis=1)
merged = merged.drop(columns=error_columns)
# print(merged) # check to make sure the new column was created correctly, that the values are correct, and the old error columns were dropped

# let user decide if N/As stay as N/As or are replaced with the average value of the column
pref = input("Do you want to replace N/As with the average value of the column? (y/n): ")
num_cols = merged.select_dtypes(include=['int64', 'float64']).columns
# print(num_cols) # check to make sure the columns were selected correctly
if pref == "y":
    # They all seem to have 0 ro 1 decimal places so round 2 guarantees no loss of data while still being readable
    merged[num_cols] = merged[num_cols].fillna(merged[num_cols].mean()).round(2)
    print("N/As have been replaced with the average value of the column.")
    # print(merged) # check to make sure the N/As were replaced correctly
else:
    print("N/As have not been replaced with the average value of the column.")
    # print(merged) # check to make sure the N/As were not replaced

# Export the merged dataframe to a csv file
merged.to_csv(r"DATA3463/DATA3463-MiniProject1/data/phase3Outputs/merged_output.csv", index=False)