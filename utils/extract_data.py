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
from utils.b_get_group import get_group
from utils.a_login import login
from utils.c_create_student_list import create_student_list
from utils.c_filter_student import filter_students


def extract_data():
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
    get_group(html_file_path, output_json_path)

    # Login to the website
    login(driver)

    # Load group page
    with open(output_json_path, "r", encoding="utf-8") as file:
        urls_data = json.load(file)

    print(len(urls_data), " groups have been founded.\n")

    # Get student data from the URL
    students = create_student_list(urls_data, driver, wait)

    print(f"Total {len(students)} students have been founded.\n")

    print("-----------------------------------------------------------")
    print("Data comparison...\n")

    if os.path.getsize("systemdata.json") > 0:
        with open("systemdata.json", "r", encoding="utf-8") as file:
            old_students = json.load(file)["memberships"]
    else:
        old_students = []

    # Student's index
    index = 1

    # Extract additional data for each student
    students = filter_students(students, old_students, driver, wait, index)

    print("All students have been loaded.\n")
    time.sleep(0.5)
    print("Removing unnecessary data...\n")

    # Remove the link attribute
    for student in students:
        if "link" in student:
            del student["link"]

    # Merge old and new students to filter out duplicates and update additional data
    student_dict = {}

    for student in old_students:
        student_dict[student["id"]] = student

    for student in students:
        student_dict[student["id"]] = student

    filtered_list = list(student_dict.values())

    # Save the extracted data to a JSON file
    groups = {"memberships": filtered_list}
    time.sleep(0.5)

    print("Saving data to data.json file...\n")

    with open("systemdata.json", "w", encoding="utf-8") as outfile:
        json.dump(groups, outfile, ensure_ascii=False, indent=4)

    time.sleep(0.5)

    print("Data has been saved to data.json file.\n")

    driver.quit()
    print("WebDriver has been closed.")
