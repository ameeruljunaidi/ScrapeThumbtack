import os
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
    providerRatings = []
    for ratings in tempList:
        if len(ratings) == 0:
            x = NaN
        else:
            x = ratings[0]
        providerRatings.append(x)

except Exception as e:
    print(e)
    driver.quit()

driver.quit()
