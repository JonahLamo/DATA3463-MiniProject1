import pandas as pd
import numpy as np
import json

file = r'DATA3463\DATA3463-MiniProject1\data\Weather_AQI_feed.json'

#open the file
with open(file, "r") as f:
    data = json.load(f)

# Normalize districts into a flat dataframe
df = pd.json_normalize(data["districts"])

#drop unnecessary columns
df = df.drop(columns = ['monitoring_station','last_updated','weather.temp_f','aqi.pm25','aqi.pm10','aqi.aqi'])
#rename columns
df = df.rename(columns = {'weather.temp_c':'temp', 'weather.precip_mm':'percip_mm', 'weather.humidity_percent':'humid_percent', 'weather.wind_speed_kmh':'wind_kmh','aqi.category':'aqi_catagory'})

#search for missing values and add it to a new column called DataErrprs
df["Data_Errors"] = df.apply(
    lambda row: ", ".join(
        [f"missing_value({col})" for col in row.index[row.isna()]]
    ),
    axis=1
)

#print(df)
#output to csv

df.to_csv(r"DATA3463\DATA3463-MiniProject1\data\phase2Outputs\json_output.csv", index=False)
