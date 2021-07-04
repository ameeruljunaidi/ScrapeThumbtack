import pandas as pd

servicesCSV = pd.read_csv("src/all_services.csv")
servicesCSV = servicesCSV[["Services", "ID"]]
servicesCSV["ID"] = servicesCSV["ID"].astype(int)

servicesNameCSV = servicesCSV["Services"].tolist()
servicesNameDf = servicesCSV.drop_duplicates(subset=["Services"])
serviceID = servicesNameDf.set_index("Services").T.to_dict("records")[0]
