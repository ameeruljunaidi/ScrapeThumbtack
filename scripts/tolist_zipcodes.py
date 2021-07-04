import csv
import pandas as pd

zipCodeCSV = pd.read_csv(
    "src/us_states.csv", converters={"Representative ZIP Code": lambda x: str(x)}
)
zipCodeCSV = zipCodeCSV["Representative ZIP Code"].tolist()
