import pandas as pd
import random 
from datetime import datetime


df_d = pd.read_csv("./dummy_data/driver_data.csv")
df = pd.DataFrame()
df["license_plate"] = df_d["license_plate_number"]

def random_year(row):
    year = random.randint(1999, 2024)
    # print(year)
    return year

df["manufacture_year"] = df.apply(random_year, axis=1)

df.to_json("./dummy_data/vehicle_data.json", orient='records')