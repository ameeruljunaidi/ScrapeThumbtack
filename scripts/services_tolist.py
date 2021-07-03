import pandas as pd

servicesCSV = pd.read_csv("data/all_services.csv")
servicesCSV = servicesCSV["Services"].tolist()

print(servicesCSV)
