import pandas as pd

# load the csv
df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\City_Development_Projects.csv")
# print(df) # check to make sure the csv was read correctly

# function to create the Data_Error column, which checks for missing values in the Estimated_Units column and duplicate Project_IDs, and creates error messages accordingly
def get_errors(row):
    errors = []
    for col in df.columns:
        if pd.isna(row[col]):
            errors.append(f'missing_value({col} in Project_ID: {row["Project_ID"]})')
    if row['Project_ID'] in duplicates['Project_ID'].values:
        errors.append(f'duplicate_row(Project_ID: {row["Project_ID"]})')
    return '; '.join(errors)

# Ensure estimated units is treated as a numeric value, and that missing values are represented as NaN
df['Estimated_Units'] = pd.to_numeric(df['Estimated_Units'], errors='coerce')

# identify duplicates
duplicates = df[df.duplicated(subset=['Project_ID'], keep=False)]

# create the Data_Error column
df['Data_Error'] = df.apply(get_errors, axis=1)
df = df.drop_duplicates(subset=['Project_ID'], keep='first') # remove duplicate rows, keeping the first occurrence
# print(df) # check to make sure the new column was created correctly, and that the duplicates were removed

# create the grouped total estimated units per district and the grouped Data_Error columns
grouped = df.groupby('District_ID').agg({
    'Estimated_Units': 'sum',
    'Data_Error': lambda x: '; '.join([msg for msg in x if msg.strip() != ""])
}).reset_index()
# print(grouped) # check to make sure the new columns were created correctly

# rename Estimated_Units to Total_Units
grouped = grouped.rename(columns={'Estimated_Units': 'Total_Units'})
# print(grouped) # check to make sure the column was renamed correctly

# export the new dataframe to a csv file, without the index
grouped.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\development.csv", index=False)