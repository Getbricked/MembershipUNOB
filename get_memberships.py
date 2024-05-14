# get_membership.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import json
import time
from get_group import get_group

def get_membership():
    # Setup Chrome options
    options = Options()
    options.add_experimental_option("detach", True)

    # Start a new instance of Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    print("WebDriver has been started.")

    # Extract group data
    html_file_path = "list_groups.html"
    output_json_path = "groups_data.json"
    get_group(html_file_path, output_json_path)

    # Open the URL and Login
    with open("url.json", "r") as file:
        url = json.load(file)["url"]

    driver.get(url)
    driver.refresh()
    print("Logging in...\n")

    # Read username and password from JSON file
    with open("credentials.json", "r") as file:
        credentials = json.load(file)
        username = credentials["username"]
        password = credentials["password"]

    # Fill in the login form and submit
    driver.find_element(By.NAME, "Username").send_keys(username)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.NAME, "button").click()
    time.sleep(0.2)

    # Load group page
    with open("groups_data.json", "r", encoding="utf-8") as file:
        urls_data = json.load(file)

    students = []

    for item in urls_data:
        group_name = item["group_name"]
        group_id = item["group_id"]
        url = item["url"]
        print(f"Opening URL for group {group_name}: {url}\n")
        driver.get(url)
        time.sleep(0.3)

        # Find all student links
        try:
            links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#StudijniSkupinaStudents a")))
        except TimeoutException:
            print(f"Timeout while waiting for student links in group {group_name}.")
            continue

        # Extract usernames and IDs
        for link in links:
            try:
                student_link = link.get_attribute("href")
                student_id = student_link.split("/")[-1]
                student_name = link.text.strip()
                students.append({
                    "id": student_id,
                    "name": student_name,
                    "group": group_name,
                    "group_id": group_id,
                    "link": student_link
                })
            except StaleElementReferenceException as e:
                print(f"StaleElementReferenceException occurred for student {link.text.strip() if link else 'unknown'}: {e}")

    for student in students:
        try:
            driver.get(student["link"])
            time.sleep(0.3)

            email_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[strong[text()='E-mail:']]/following-sibling::div")))
            student["email"] = email_element.text if email_element else "N/A"

            rocnik_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[strong[text()='Ročník:']]/following-sibling::div")))
            student["rocnik"] = rocnik_element.text if rocnik_element else "N/A"

            fakulta_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[strong[text()='Fakulta:']]/following-sibling::div/a")))
            student["fakulta"] = fakulta_element.text if fakulta_element else "N/A"

            datova_schranka_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[strong[text()='Datová schránka:']]/following-sibling::div")))
            student["datova_schranka"] = datova_schranka_element.text if datova_schranka_element else "N/A"
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error occurred for student {student['name']}: {e}")

    for student in students:
        if "link" in student:
            del student["link"]

    # Save the extracted data to a JSON file
    groups = {"memberships": students}
    with open("data.json", "w", encoding="utf-8") as outfile:
        json.dump(groups, outfile, ensure_ascii=False, indent=4)

    driver.quit()
    print("WebDriver has been closed.")


