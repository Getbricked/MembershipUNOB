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

    # Remove the link attribute
    for student in students:
        if "link" in student:
            del student["link"]

    # Merge old and new students to filter out duplicates and update additional data
    student_dict = {}

    for student in old_students:
        student_dict[student["id"]] = student

    for student in students:
        # student_dict[student["id"]] = student
        student_dict[student["id"]] = {**student_dict.get(student["id"], {}), **student}

    filtered_list = list(student_dict.values())

    return filtered_list
