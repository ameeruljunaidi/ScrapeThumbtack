import pandas as pd

zipCodeCSV = pd.read_csv("src/us_states.csv")
zipCodeCSV = zipCodeCSV["Representative ZIP Code"].tolist()
