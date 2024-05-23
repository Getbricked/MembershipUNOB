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
from get_group import get_group
import uuid


def get_membership():
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
    html_file_path = "list_groups.html"
    output_json_path = "groups_data.json"
    get_group(html_file_path, output_json_path)

    # Open the URL and Login
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

    # Load group page
    with open("groups_data.json", "r", encoding="utf-8") as file:
        urls_data = json.load(file)

    print(len(urls_data), " groups has been founded.\n")

    students = []

    for item in urls_data:
        group_name = item["group_name"]
        group_id = item["group_id"]
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
                        "link": student_link,
                    }
                )
            except StaleElementReferenceException as e:
                print(
                    f"StaleElementReferenceException occurred for student {link.text.strip() if link else 'unknown'}: {e}"
                )

    print(f"Total {len(students)} students has been founded.\n")

    # Student's index
    index = 1

    with open("systemdata.json", "r", encoding="utf-8") as file:
        old_students = json.load(file)["memberships"]

    # Extract additional data for each student
    for student in students:
        check = False
        for old_student in old_students:

            if (
                student["name"] == old_student["name"]
                and student["group"] == old_student["group"]
            ):

                student["email"] = old_student["email"]
                student["rocnik"] = old_student["rocnik"]
                student["fakulta"] = old_student["fakulta"]
                student["datova_schranka"] = old_student["datova_schranka"]
                student["id"] = old_student["id"]

                check = True
                index += 1

                print(
                    f"######{index}. {student['name']} - {student['group']} already exists, skipping."
                )

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

    print("All students have been loaded.\n")
    time.sleep(0.5)
    print("Removing unnecessary data...\n")

    # Remove the link attribute
    for student in students:
        if "link" in student:
            del student["link"]

    # Merge the old and new students data
    merged_students = students + old_students

    # Remove duplicates
    filtered_list = {item["id"]: item for item in merged_students}.values()
    filtered_list = list(filtered_list)

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
