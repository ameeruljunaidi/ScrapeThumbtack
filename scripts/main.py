import os
import pandas as pd
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = f"{os.getcwd()}/selenium/chromedriver"

zipCodeCSV = pd.read_csv("data/us_states.csv")
zipCodeCSV = zipCodeCSV["Representative ZIP Code"].tolist()

servicePlaceHolder = "DJ"

finalDf = pd.DataFrame()

for zipCode in zipCodeCSV:
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.thumbtack.com/more-services")

    link = driver.find_element_by_link_text(servicePlaceHolder)
    link.click()

    enterZipCode = driver.find_element_by_name("zip_code")
    enterZipCode.send_keys(zipCode)
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
                    "//*[@data-test]//div[2]//div//div[1]//div//div[1]//span[@class='b']",
                )
            )
        )

        listServiceProvider = []
        for service in serviceProvider:
            listServiceProvider.append(service.text)

        # List of ratings
        blocks = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[@class='flex-1 m_flex relative z-0']",
                )
            )
        )

        listBlockNodes = []
        for block in blocks:
            listBlockNodes.append(block.find_elements_by_xpath(".//*"))

        nestedRatings = []
        for i, listNodes in zip(range(len(listBlockNodes)), listBlockNodes):
            nestedRatings.append([])
            for nodes in listNodes:
                nestedRatings[i].append(nodes.get_attribute("data-star"))

        tempRatingsList = []
        for ratingsList in nestedRatings:
            tempRatingsList.append(
                [ratings for ratings in ratingsList if ratings is not None]
            )

        listServiceRating = []
        for ratings in tempRatingsList:
            if len(ratings) == 0:
                x = NaN
            else:
                x = ratings[0]
            listServiceRating.append(x)

        # Number of hires
        serviceHires = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[@data-test]/div/div[2]/div/div[1]/div/div[4]/ul/li[1]/span[2]",
                )
            )
        )

        tempListServiceHires = []
        for service in serviceHires:
            tempListServiceHires.append(service.text)

        listServiceHires = []
        for service in tempListServiceHires:
            if service.find("hires") != -1:
                x = service.split()[0]
            else:
                x = NaN
            listServiceHires.append(x)

        dictServicesProvided = {
            "Service": listServiceProvider,
            "Type": servicePlaceHolder,
            "Rating": listServiceRating,
            "Hires": listServiceHires,
            "Zip Code": zipCode,
        }

        dfServicesProvided = pd.DataFrame(dictServicesProvided)

    except Exception as e:
        print(e)
        driver.quit()

    finalDf = finalDf.append(dfServicesProvided, ignore_index=True)
    driver.quit()

driver.quit()
finalDf.to_csv("data/services_database.csv")
