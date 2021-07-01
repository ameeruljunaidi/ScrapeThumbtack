import os
import pandas as pd
from selenium import webdriver

PATH = f"{os.getcwd()}/selenium/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://www.thumbtack.com/more-services")

listMainServices = []
listPeriServices = []

mainServices = driver.find_elements_by_class_name("categories__label")
for service in mainServices:
    listMainServices.append(service.text)

periServices = driver.find_elements_by_class_name("more-services-page__category__link")
for service in periServices:
    listPeriServices.append(service.text)

listAllServices = listMainServices + listPeriServices

dictMainServices = {"Services": listMainServices, "Type": "Main"}
dictPeriServices = {"Services": listPeriServices, "Type": "Peripheral"}

dfMainServices = pd.DataFrame(dictMainServices)
dfPeriServices = pd.DataFrame(dictPeriServices)

dfAllServices = pd.concat(
    [dfMainServices, dfPeriServices],
    ignore_index=True,
)

dfAllServices.to_csv("data/all_services.csv", index=False)

driver.quit()

# TODO: Categorize the data for all services
