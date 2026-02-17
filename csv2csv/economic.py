import pandas as pd

# load the csv
df = pd.read_csv(r"DATA3463\DATA3463-MiniProject1\data\Population_Economic_Indicators.csv")
# print(df) # check to make sure the csv was read correctly

# population is already clean, just convert to numeric to make sure its fine
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')

# median income has a missing value and a '81,000' value, so clean is more complex
def clean_median_income(value):
    if pd.isna(value):
        return None
    value = str(value).replace(',', '')  # remove commas
    try:
        return float(value)
    except ValueError:
        return None
df['Median_Income'] = df['Median_Income'].apply(clean_median_income)
# print(df) # check to make sure the columns were cleaned correctly

# Employment_Rate has a missing value, some values as '73%' and some as '0.78', we want everything to be like '73' or '78' (without the % or the decimal)
def clean_employment_rate(value):
    if pd.isna(value) or value == '':
        return None
    val_str = str(value).strip()
    if '%' in val_str:
        return float(val_str.replace('%', ''))
    try:
        num_val = float(val_str)
        if 0 < num_val <= 1:
            return num_val * 100
        return num_val
    except ValueError:
        return None
df['Employment_Rate'] = df['Employment_Rate'].apply(clean_employment_rate)
# print(df) # check to make sure the columns were cleaned correctly

# create the Data_Error column
def get_errors(row):
    errors = []
    if pd.isna(row['Population']):
        errors.append('missing_value(Population)')
    if pd.isna(row['Median_Income']):
        errors.append('missing_value(Median_Income)')
    if pd.isna(row['Employment_Rate']):
        errors.append('missing_value(Employment_Rate)')
    return '; '.join(errors)
df['Data_Error'] = df.apply(get_errors, axis=1)
# print(df) # check to make sure the new column was created correctly

# remove the duplicate D01 row, use last one since it seems to be newer (bigger numbers), add Data_Error stating the duplicate
duplicate_mask = df.duplicated(subset='District_ID', keep=False)
df.loc[duplicate_mask & ~df.duplicated(subset='District_ID', keep='last'), 'Data_Error'] = 'duplicate_row(Older value removed)'
df = df.drop_duplicates(subset='District_ID', keep='last')
# print(df) # check to make sure the duplicates were removed

# Make a new df with only the columns we want
new_df = df[['District_ID', 'Population', 'Median_Income', 'Employment_Rate', 'Data_Error']]
# print(new_df) # check to make sure the new df looks correct

# Export the new dataframe to a csv file, without the index
new_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\economic.csv", index=False)