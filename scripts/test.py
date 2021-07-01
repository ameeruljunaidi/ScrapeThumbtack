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

listServiceProvider = []
listServiceRating = []

try:
    serviceProvider = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]//div[2]//div//div[1]//div//div[1]//span[@class='b']",
            )
        )
    )

    serviceRating = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//*[@data-test]/div//div[1]//div[2]/div[1]/div/div/div/div[1]",
            )
        )
    )

except:
    pass

for service in serviceProvider:
    listServiceProvider.append(service.text)

for service in serviceRating:
    listServiceRating.append(service.text)

# dictServicesProvided = {
#     "Service": listServiceProvider,
#     "Rating": listServiceRating,
#     "Type": servicePlaceHolder,
#     "Zip Code": zipCodePlaceHolder,
# }

# dfServicesProvided = pd.DataFrame(dictServicesProvided)
# dfServicesProvided.to_csv("data/services_database.csv", index=False)


# driver.quit()

print(len(listServiceProvider))
print(listServiceProvider)
print(len(listServiceRating))
print(listServiceRating)
