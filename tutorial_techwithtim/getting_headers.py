import os  # import os to get path to directory
from selenium import webdriver  # import the webdriver module from selenium
from selenium.webdriver.common.keys import Keys  # import to use the keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = f"{os.getcwd()}/selenium/chromedriver"  # find path for chromedriver

# Set path to open a specific website
driver = webdriver.Chrome(PATH)
driver.get("https://techwithtim.net")

search = driver.find_element_by_name("s")  # search for the search bar
search.send_keys("test")  # type in test into the search bar
search.send_keys(Keys.RETURN)  # hit enter

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )

    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)

finally:
    driver.quit()
