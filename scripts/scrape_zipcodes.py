import pandas as pd

dfZipCodes = pd.read_csv("src/us_states.csv")
dfZipCodesDict = dfZipCodes.set_index("Representative ZIP Code").T.to_dict("list")

# Source: https://vanwilson.info/2014/11/sample-zip-codes-50-states/
