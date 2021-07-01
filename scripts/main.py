import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from zipcodes import dfZipCodesDict

PATH = f"{os.getcwd()}/selenium/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://www.thumbtack.com/more-services")

servicePlaceHolder = "Lawn Mowing and Trimming"
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

listServiceProvider = []

try:
    serviceProvider = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]//div[2]//div//div[1]//div//div[1]//span[@class='b']",
            )
        )
    )

    for service in serviceProvider:
        listServiceProvider.append(service.text)

    dictServicesProvided = {
        "Service": listServiceProvider,
        "Type": servicePlaceHolder,
        "Zip Code": zipCodePlaceHolder,
    }

    dfServicesProvided = pd.DataFrame(dictServicesProvided)
    dfServicesProvided.to_csv("data/services_database.csv", index=False)
except:
    pass

# TODO: Get more zipcodes
