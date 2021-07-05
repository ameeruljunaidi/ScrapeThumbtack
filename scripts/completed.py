import glob
import pandas as pd
import numpy as np

from tolist_services import servicesNameCSV, serviceID
from tolist_zipcodes import zipCodeCSV

from functions import find_between

path = r"data/"
all_csv = glob.glob(path + "/*.csv")

dfAllServicesCSV = pd.read_csv("src/all_services.csv")

completed = []
for file in all_csv:
    completed.append(find_between(file, "/", "."))

tempServices = []
tempZipCode = []
for service in servicesNameCSV:
    for zip in zipCodeCSV:
        tempZipCode.append(zip)
        tempServices.append(serviceID[service])

dictAllServices = {"Service": tempServices, "Zip Code": tempZipCode}
dfAllServices = pd.DataFrame(dictAllServices)

dfAllServices["File Name"] = (
    dfAllServices["Service"].astype(str) + "_" + dfAllServices["Zip Code"].astype(str)
)

dfAllServices["Status"] = dfAllServices["File Name"].isin(completed)

nullDataFrames = open("src/null_dataframes.txt").read().splitlines()
dfAllServices["Null"] = dfAllServices["File Name"].isin(nullDataFrames)

dfAllServices = pd.merge(
    dfAllServices,
    dfAllServicesCSV[["Services", "ID"]],
    left_on="Service",
    right_on="ID",
    how="left",
).drop("ID", axis=1)

dfAllServices["To Do"] = np.where(
    (dfAllServices["Status"] == False) & (dfAllServices["Null"] == False), True, False
)

serviceTodo = dfAllServices[dfAllServices["Status"] == False]["Services"].tolist()
serviceTodo = list(dict.fromkeys(serviceTodo))
zipCodeTodo = dfAllServices[dfAllServices["Status"] == False]["Zip Code"].tolist()
zipCodeTodo = list(dict.fromkeys(zipCodeTodo))

dfAllServices.to_csv("src/tracker.csv")

percentageDone = "{:.2%}".format(
    dfAllServices[dfAllServices["To Do"] == False]["To Do"].count()
    / dfAllServices[dfAllServices["To Do"] == True]["To Do"].count()
)

print(f"Percent Done: {percentageDone}")