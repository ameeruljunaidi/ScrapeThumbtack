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
