from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
import get_group

# get_group()

# Setup Chrome options
options = Options()
options.add_experimental_option("detach", True)

# Start a new instance of Chrome WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

print("WebDriver has been started.")

## Open the URL and Login
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

## Load group page
with open("groups_data.json", "r", encoding="utf-8") as file:
    urls_data = json.load(file)

groups = []

for item in urls_data:
    group_name = item["group_name"]
    url = item["url"]
    print(f"Opening URL for group {group_name}: {url}\n")
    driver.get(url)
    time.sleep(0.3)
    # Find all student links
    links = driver.find_elements(By.CSS_SELECTOR, "#StudijniSkupinaStudents a")

    # Extract usernames and IDs
    students = []
    student_links = []

    for link in links:
        student_link = link.get_attribute("href")
        student_id = link.get_attribute("href").split("/")[-1]
        student_name = link.text.strip()
        student_links.append(student_link)
        students.append({"id": student_id, "username": student_name})

    for i, link in enumerate(student_links):
        driver.get(link)

        email_element = driver.find_element(
            By.XPATH, "//div[strong[text()='E-mail:']]/following-sibling::div"
        )
        email = email_element.text

        students[i][
            "email"
        ] = email  # Add email to the corresponding student dictionary
        time.sleep(0.3)

    groups.append({"group_name": group_name, "students": students})

    # Print the extracted usernames and IDs
    # for group in groups:
    #     print(f"Group: {group['group_name']}")
    #     for student in group["students"]:
    #         print(
    #             f"ID: {student['id']}, Username: {student['username']}, Email: {student['email']}"
    #         )
    print(groups)

with open("data.json", "w", encoding="utf-8") as outfile:
    json.dump(groups, outfile, ensure_ascii=False, indent=4)

driver.quit()
