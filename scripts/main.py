import os
import pandas as pd
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

servicePlaceHolder = "DJ"
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
    serviceProvider = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]//div[2]//div//div[1]//div//div[1]//span[@class='b']",
            )
        )
    )

    listServiceProvider = []
    for service in serviceProvider:
        listServiceProvider.append(service.text)

    blocks = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@class='flex-1 m_flex relative z-0']",
            )
        )
    )

    # Returns a nested list for all the service blocks
    listBlockNodes = []
    for block in blocks:
        listBlockNodes.append(block.find_elements_by_xpath(".//*"))

    # Get all the ratings in nested form
    nestedRatings = []
    for i, listNodes in zip(range(len(listBlockNodes)), listBlockNodes):
        nestedRatings.append([])
        for nodes in listNodes:
            nestedRatings[i].append(nodes.get_attribute("data-star"))

    # Get a temporary list of all the ratings
    tempList = []
    for ratingsList in nestedRatings:
        tempList.append([ratings for ratings in ratingsList if ratings is not None])

    # Get the provider ratings
    listServiceRating = []
    for ratings in tempList:
        if len(ratings) == 0:
            x = NaN
        else:
            x = ratings[0]
        listServiceRating.append(x)

    dictServicesProvided = {
        "Service": listServiceProvider,
        "Rating": listServiceRating,
        "Type": servicePlaceHolder,
        "Zip Code": zipCodePlaceHolder,
    }

    dfServicesProvided = pd.DataFrame(dictServicesProvided)
    dfServicesProvided.to_csv("data/services_database.csv", index=False)

except:
    pass

driver.quit()

# TODO: Get more zipcodes
