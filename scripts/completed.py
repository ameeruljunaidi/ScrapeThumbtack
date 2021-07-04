import glob
import pandas as pd
from tolist_services import servicesNameCSV, serviceID
from tolist_zipcodes import zipCodeCSV

path = r"data/"
all_csv = glob.glob(path + "/*.csv")

dfAllServicesCSV = pd.read_csv("src/all_services.csv")


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


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
dfAllServices = pd.merge(
    dfAllServices,
    dfAllServicesCSV[["Services", "ID"]],
    left_on="Service",
    right_on="ID",
    how="left",
).drop("ID", axis=1)

serviceTodo = dfAllServices[dfAllServices["Status"] == False]["Services"].tolist()
serviceTodo = list(dict.fromkeys(serviceTodo))
zipCodeTodo = dfAllServices[dfAllServices["Status"] == False]["Zip Code"].tolist()
zipCodeTodo = list(dict.fromkeys(zipCodeTodo))
