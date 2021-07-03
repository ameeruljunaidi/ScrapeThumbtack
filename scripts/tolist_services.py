import pandas as pd

servicesCSV = pd.read_csv("src/all_services.csv")
servicesCSV = servicesCSV["Services"].tolist()
