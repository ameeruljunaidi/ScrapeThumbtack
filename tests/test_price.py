import os
from numpy.core.arrayprint import set_printoptions
from numpy.lib.function_base import append
import pandas as pd
import time
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from zipcodes import dfZipCodesDict

PATH = f"{os.getcwd()}/selenium/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://www.thumbtack.com/more-services")

servicePlaceHolder = "House Cleaning"
zipCodePlaceHolder = "95814"

link = driver.find_element_by_link_text(servicePlaceHolder)
link.click()

enterZipCode = driver.find_element_by_name("zip_code")
enterZipCode.send_keys(zipCodePlaceHolder)
enterZipCode.send_keys(Keys.RETURN)

try:
    while True:
        seeMoreButton = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button//span[contains(text(), 'See More')]",
                )
            )
        )
        seeMoreButton.click()
except:
    pass

try:
    # Name of service
    serviceProvider = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]/div/div[2]/div/div[1]/div/div[1]/span",
            )
        )
    )

    listServiceProvider = []
    for service in serviceProvider:
        listServiceProvider.append(service.text)

    pricesList = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]/div/div[2]/div/div[2]",
            )
        )
    )

    tempListServiceHires = []
    for service in pricesList:
        tempListServiceHires.append(service.text)

    # listServiceHires = []
    # for service in tempListServiceHires:
    #     if service.find("hires") != -1:
    #         x = service.split()[0]
    #     else:
    #         x = NaN
    #     listServiceHires.append(x)

    listServicePrice = []
    for i in tempListServiceHires:
        if i.find("$") != -1:
            x = i.split()[0]
            x = x[1:]
        else:
            x = NaN
        listServicePrice.append(x)

    print(len(listServiceProvider))
    print(len(tempListServiceHires))

    dictDf = {"Name": listServiceProvider, "Price": listServicePrice}
    dfFinal = pd.DataFrame(dictDf)
    dfFinal.to_csv("data/test.csv")

except Exception as e:
    print(e)
    driver.quit()

driver.quit()
