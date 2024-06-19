from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import json
import time


def login(driver):
    url = "https://apl.unob.cz/MojeAP"

    driver.get(url)
    driver.refresh()
    print("Logging in...\n")

    # Read username and password from JSON file
    with open("credentials.json", "r") as file:
        credentials = json.load(file)
        username = credentials["username"]
        password = credentials["password"]

    # Login
    driver.find_element(By.NAME, "Username").send_keys(username)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.NAME, "button").click()
    time.sleep(0.05)
