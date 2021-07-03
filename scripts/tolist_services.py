import pandas as pd

servicesCSV = pd.read_csv("src/all_services.csv")
servicesCSV = servicesCSV[["Services", "ID"]]
servicesCSV["ID"] = servicesCSV["ID"].astype(int)

servicesNameCSV = servicesCSV["Services"].tolist()
serviceID = pd.Series(servicesCSV["Services"], index=servicesCSV["ID"]).to_dict()
serviceID = {v: k for k, v in serviceID.items()}
