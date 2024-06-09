# get_membership.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
import json
import time
import uuid
import os
from utils.a_login import login
from utils.c_create_student_list import create_student_list
from utils.c_filter_student import filter_students


def get_student():
    # Setup Chrome options
    options = Options()
    options.add_experimental_option("detach", True)

    # Start a new instance of Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    wait = WebDriverWait(driver, 10)
    print("WebDriver has been started.")

    # Extract groups data
    html_file_path = "utils/b_list_groups.html"
    output_json_path = "utils/b_groups_data.json"

    # Login to the website
    login(driver)

    # Load group page
    with open(output_json_path, "r", encoding="utf-8") as file:
        urls_data = json.load(file)["groups"]

    print(len(urls_data), " groups have been founded.\n")

    # Get student data from the URL
    students = create_student_list(urls_data, driver, wait)

    print(f"Total {len(students)} students have been founded.\n")

    print("-----------------------------------------------------------")
    print("Data comparison...\n")

    if os.path.getsize("utils/c_students_data.json") > 0:
        with open("utils/c_students_data.json", "r", encoding="utf-8") as file:
            old_students = json.load(file)["users"]
    else:
        old_students = []

    print("All students have been loaded.\n")
    time.sleep(0.5)
    print("Removing unnecessary data...\n")

    # Save the extracted data to a JSON file
    filtered_list = filter_students(students, old_students, driver, wait)

    students_list = {"users": filtered_list}
    time.sleep(0.5)

    print("Saving data to data.json file...\n")

    with open("utils/c_students_data.json", "w", encoding="utf-8") as outfile:
        json.dump(students_list, outfile, ensure_ascii=False, indent=4)

    time.sleep(0.5)

    print("Data has been saved to data.json file.\n")

    driver.quit()
    print("WebDriver has been closed.")
