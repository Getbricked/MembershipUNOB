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
from .a_login import login
from ._config import config_check_web, config_web


# Getting student data from the URL
def create_student_list(urls_data, driver, wait):
    students = []

    for item in urls_data:
        group_name = item["name"]
        group_id = item["id"]
        url = item["url"]
        driver.get(url)
        # time.sleep(0.05)

        # Find all student links
        try:
            links = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "#StudijniSkupinaStudents a")
                )
            )
        except TimeoutException:
            print(f"Timeout while waiting for student links in group {group_name}.")
            continue

        print(f" - Opening URL for group {group_name}: {url}\n")

        # Extract usernames and IDs
        for link in links:
            try:
                student_link = link.get_attribute("href")
                student_name = link.text.strip()

                students.append(
                    {
                        "name": student_name,
                        "group": group_name,
                        "group_id": group_id,
                        "valid": True,
                        "link": student_link,
                    }
                )
            except StaleElementReferenceException as e:
                print(
                    f"StaleElementReferenceException occurred for student {link.text.strip() if link else 'unknown'}: {e}"
                )

    return students


# Filter students
def filter_students(students, old_students, driver, wait):
    index = 1
    for student in students:
        check = False
        for old_student in old_students:

            if (
                student["name"] == old_student["name"]
                and student["group"] == old_student["group"]
            ):
                student["id"] = old_student["id"]
                student["email"] = old_student["email"]
                student["rocnik"] = old_student["rocnik"]
                student["fakulta"] = old_student["fakulta"]
                student["datova_schranka"] = old_student["datova_schranka"]

                print(
                    f"######{index}. {student['name']} - {student['group']} already exists, skipping."
                )

                check = True
                index += 1
                break

        if check:
            continue

        try:
            driver.get(student["link"])
            # time.sleep(0.05)

            student["id"] = str(uuid.uuid4())

            # Email
            email_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[strong[text()='E-mail:']]/following-sibling::div")
                )
            )
            student["email"] = email_element.text if email_element else "N/A"

            # Year of study
            rocnik_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[strong[text()='Ročník:']]/following-sibling::div")
                )
            )
            student["rocnik"] = rocnik_element.text if rocnik_element else "N/A"

            # Falcuty
            fakulta_element = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[strong[text()='Fakulta:']]/following-sibling::div/a",
                    )
                )
            )
            student["fakulta"] = fakulta_element.text if fakulta_element else "N/A"

            # Datova schranka?
            datova_schranka_element = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[strong[text()='Datová schránka:']]/following-sibling::div",
                    )
                )
            )
            student["datova_schranka"] = (
                datova_schranka_element.text if datova_schranka_element else "N/A"
            )

            # Display on terminal
            print(f"{index}. {student['name']} - {student['group']} has been loaded.")
            index += 1

        # Handle errors
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException,
        ) as e:
            print(f"Error occurred for student {student['name']}: {e}")

    # Merge old and new students to filter out duplicates and update additional data
    student_dict = {}

    for student in old_students:
        student_dict[student["id"]] = student

    for student in students:
        # student_dict[student["id"]] = student
        student_dict[student["id"]] = {**student_dict.get(student["id"], {}), **student}

    filtered_list = list(student_dict.values())

    return filtered_list


@config_check_web(config_web["get_data"])
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

    # Login to the website
    login(driver)

    # Load group page
    from .extract_data import open_file
    script_dir = os.path.dirname(__file__)
    output_json_path = os.path.join(script_dir, 'b_groups_data.json')
    urls_data = open_file(output_json_path, "groups")

    print(len(urls_data), " groups have been founded.\n")

    # Get student data from the URL
    students = create_student_list(urls_data, driver, wait)

    print(f"Total {len(students)} students have been founded.\n")

    print("-----------------------------------------------------------")
    print("Data comparison...\n")

    module_dir = os.path.dirname(__file__)
    student_path = os.path.join(module_dir, "c_students_data.json")
    
    old_students=open_file(student_path, "users")
    print("All students have been loaded.\n")
    time.sleep(0.5)
    print("Removing unnecessary data...\n")

    # Save the extracted data to a JSON file
    filtered_list = filter_students(students, old_students, driver, wait)

    students_list = {"users": filtered_list}
    time.sleep(0.5)

    print("Saving data to data.json file...\n")

    with open(student_path, "w", encoding="utf-8") as outfile:
        json.dump(students_list, outfile, ensure_ascii=False, indent=4)

    time.sleep(0.5)

    driver.quit()
    print("WebDriver has been closed.")
