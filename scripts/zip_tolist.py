import pandas as pd

zipCodeCSV = pd.read_csv("data/us_states.csv")
zipCodeCSV = zipCodeCSV["Representative ZIP Code"].tolist()

print(zipCodeCSV)
