import pandas as pd

dfZipCodes = pd.read_csv("data/us_states.csv")
dfZipCodesDict = dfZipCodes.set_index("Representative ZIP Code").T.to_dict("list")
