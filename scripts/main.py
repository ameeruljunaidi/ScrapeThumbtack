import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zipcodes import dfZipCodesDict

PATH = f"{os.getcwd()}/selenium/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://www.thumbtack.com/more-services")

link = driver.find_element_by_link_text("Personal Training")
link.click()

enterZipCode = driver.find_element_by_name("zip_code")
enterZipCode.send_keys("95814")
enterZipCode.send_keys(Keys.RETURN)

listServiceProvider = []

# try:
#     serviceProvider = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "mr1"))
#     )

#     for service in serviceProvider:
#         listServiceProvider.append(service.text)
# except:
#     pass

serviceProvider = driver.find_elements_by_class_name("hover-blue")
for service in serviceProvider:
    listServiceProvider.append(service.text)

print(listServiceProvider)

time.sleep(3)
driver.quit()
