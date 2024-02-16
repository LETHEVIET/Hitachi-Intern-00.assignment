import pandas as pd
from datetime import datetime


df = pd.read_csv("./dummy_data/driver_data.csv")

def apply_func(row):
    # print(row)
    row["birth_date"] = datetime.strptime(row["birth_date"], '%m/%d/%Y').date().strftime("%Y-%m-%d")
    row["expiry_date"] = datetime.strptime(row["expiry_date"], '%m/%d/%Y').date().strftime("%Y-%m-%d")
    row["driver_licence_number"] = str(row["driver_licence_number"])
    return row

df = df.apply(apply_func, axis=1)

df.to_json("./dummy_data/driver_data.json", orient='records')