import os
from sys import platform
import pandas as pd
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tolist_services import servicesNameCSV, serviceID
from tolist_zipcodes import zipCodeCSV
from completed import (
    serviceTodo,
    zipCodeTodo,
    completed,
    nullDataFrames,
)

from functions import append_new_line

if platform == "linux":
    PATH = f"{os.getcwd()}/selenium/linux/chromedriver"
elif platform == "darwin":
    PATH = f"{os.getcwd()}/selenium/macos/chromedriver"
else:
    pass

serviceList = serviceTodo
zipCodeList = zipCodeTodo

for serviceName in serviceList:
    for zipCode in zipCodeList:

        if (f"{serviceID[serviceName]}_{zipCode}" in completed) | (
            f"{serviceID[serviceName]}_{zipCode}" in nullDataFrames
        ):
            pass
        else:

            # Clear the list for service name and zip codes
            listServices = []
            listZipCodes = []

            # Open a chrome page with url specified
            driver = webdriver.Chrome(PATH)
            driver.get("https://www.thumbtack.com/more-services")

            # Click the name of the service
            link = driver.find_element_by_link_text(serviceName)
            link.click()

            # Enter zipcode and press enter
            enterZipCode = driver.find_element_by_name("zip_code")
            driver.implicitly_wait(10)
            enterZipCode.send_keys(zipCode)
            enterZipCode.send_keys(Keys.RETURN)

            try:
                while True:
                    # Make sure the "see more" button is pressed if it's there
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
                # Get elements for names of services
                serviceProvider = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//*[@data-test]/div/div[2]/div/div[1]/div/div[1]/span",
                        )
                    )
                )
            except:
                driver.quit()
                append_new_line(
                    "src/null_dataframes.txt", f"{serviceID[serviceName]}_{zipCode}"
                )

            try:
                # Get a list of the names of services
                listServiceProvider = []
                for service in serviceProvider:
                    listServiceProvider.append(service.text)

                # Get elements for ratings (need to get blocks first)
                blocks = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//*[@class='flex-1 m_flex relative z-0']",
                        )
                    )
                )

                # Get children nodes for the blocks for ratings
                listBlockNodes = []
                for block in blocks:
                    listBlockNodes.append(block.find_elements_by_xpath(".//*"))

                # Put all the nodes in a nested list (to make sure NA values are counted)
                nestedRatings = []
                for i, listNodes in zip(range(len(listBlockNodes)), listBlockNodes):
                    nestedRatings.append([])
                    for nodes in listNodes:
                        nestedRatings[i].append(nodes.get_attribute("data-star"))

                # Remove all the none values from the children nodes
                tempRatingsList = []
                for ratingsList in nestedRatings:
                    tempRatingsList.append(
                        [ratings for ratings in ratingsList if ratings is not None]
                    )

                # Put all ratings into a list
                listServiceRating = []
                for ratings in tempRatingsList:
                    if len(ratings) == 0:
                        x = NaN
                    else:
                        x = ratings[0]
                    listServiceRating.append(x)

                # Get elements for number of hires
                serviceHires = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//*[@data-test]/div/div[2]/div/div[1]/div/div[4]/ul/li[1]/span[2]",
                        )
                    )
                )

                # Put in a temporary list (for # of hires)
                tempListServiceHires = []
                for service in serviceHires:
                    tempListServiceHires.append(service.text)

                # Check for the word "hire" and put in a list
                listServiceHires = []
                for service in tempListServiceHires:
                    if service.find("hires") != -1:
                        x = service.split()[0]
                    else:
                        x = NaN
                    listServiceHires.append(x)

                # Get elements for prices
                elementServicePrices = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//*[@data-test]/div/div[2]/div/div[2]",
                        )
                    )
                )

                # Put prices into temporary list
                tempListServicePrice = []
                for service in elementServicePrices:
                    tempListServicePrice.append(service.text)

                # Check for dollar signs and put into list
                listServicePrice = []
                for i in tempListServicePrice:
                    if i.find("$") != -1:
                        x = i.split()[0]
                        x = x[1:]
                    else:
                        x = NaN
                    listServicePrice.append(x)

                # Add the name of service and zipcode into a list
                for i in range(len(listServiceProvider)):
                    listServices.append(serviceID[serviceName])
                    listZipCodes.append(zipCode)

                # Create a dictionary for all lists
                dictServicesProvided = {
                    "Service": listServiceProvider,
                    "Type": listServices,
                    "Rating": listServiceRating,
                    "Hires": listServiceHires,
                    "Price": listServicePrice,
                    "Zip Code": listZipCodes,
                }

                # Convert to csv for all names and zipcodes
                dfServicesProvided = pd.DataFrame(dictServicesProvided).to_csv(
                    f"data/{serviceID[serviceName]}_{zipCode}.csv"
                )
                driver.quit()

                # os.system("python3 scripts/completed.py")

            except:
                driver.quit()
                pass
