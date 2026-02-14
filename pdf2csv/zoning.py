import pandas as pd
import pdfplumber

# read the pdf file and extract the table, basically just the same as in lecture 8
with pdfplumber.open(r"DATA3463\DATA3463-MiniProject1\data\Housing_Zoning_Update_Q1_2024.pdf") as pdf:
    # interested in the second page
    page = pdf.pages[1]
    table = page.extract_table()

# convert the table to a pandas dataframe so its easier to work with, the first row of the table is the header, so we use that as the column names
df = pd.DataFrame(table[1:], columns=table[0])

# print(df) # quick check to see if everything worked, also needed to see what parts of the table we need to clean up

# Replace the 'fi' that used to be an arrow with ' to ' in Zoning_Type
df['Zoning_Type'] = df['Zoning_Type'].str.replace('fi', ' to ')
# print(df) # check to see if the replacement worked

# Create the YoY%_Zoning column
# While the 'YoY_Change_%' column exists with the same information, it is easier to calculate in a new column that it is to clean up the 'YoY_Change_%' column
# Thus, step one is to convert the 'Units_Q1_2024' and 'Units_Q1_2023' columns to numeric values from the string values
# We use the 'errors=coerce' argument to convert any non-numeric values to NaN, which will allow us to perform the calculation without errors
q1_2024 = pd.to_numeric(df['Units_Q1_2024'], errors='coerce')
q1_2023 = pd.to_numeric(df['Units_Q1_2023'], errors='coerce')

# Calculate the YoY%_Zoning column using the formula (Q1_2024 - Q1_2023) / Q1_2023 * 100, and round the result to 1 decimal place
df['YoY%_Zoning'] = round((q1_2024 - q1_2023) / q1_2023 * 100, 1)
# print(df) # Check to make sure the new column was created correctly, and that the values are correct

# add new column 'data_error' the dataframe, which explains what error is in the data, if there is an error, otherwise it will be blank
# Normal error types: missing_value, duplicate_row, whatever else we run into
# In this case, the only error was the NULL in 'Units_Q1_2024' and consequently, the NaN in 'YoY%_Zoning' (which we care about unlike the 'Units_Q1_2024' column)
df['Data_Error'] = df.apply(lambda row: 'missing_value' if pd.isna(row['YoY%_Zoning']) else '', axis=1)

# print(df) # Check to make sure the new column was created correctly, and that the values are correct

# Make a new dataframe with only the columns we want to export to csv, which are the 'District_ID', 'Zoning_Type' and 'YoY%_Zoning' columns
new_df = df[['District_ID', 'Zoning_Type', 'YoY%_Zoning', 'Data_Error']]
print(new_df) # make sure the new dataframe looks correct

# Export the new dataframe to a csv file, without the index
new_df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase1Outputs\zoning.csv", index=False)