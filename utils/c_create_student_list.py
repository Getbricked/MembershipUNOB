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
)


# Getting student data from the URL
def create_student_list(urls_data, driver, wait):
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

    return students
