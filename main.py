from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
from bs4 import BeautifulSoup

# Setup Chrome options
options = Options()
options.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://apl.unob.cz/rozvrh/api/read/rozvrh?id=7"
driver.get(url)
driver.refresh()

# Read username and password from JSON file
with open('credentials.json', 'r') as file:
    credentials = json.load(file)
    username = credentials["username"]
    password = credentials["password"]

# Fill in the login form and submit
driver.find_element(By.NAME, "Username").send_keys(username)
driver.find_element(By.NAME, "Password").send_keys(password)
driver.find_element(By.NAME, "button").click()
time.sleep(5)

# Extract the JSON data from the <pre> tag
data = driver.find_element(By.TAG_NAME, "pre").text
json_data = json.loads(data)
print(json_data)

# Write the JSON data to a file
with open('data.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

# Quit the driver
driver.quit()


# Function to extract specific attributes from JSON data

def extract_attributes(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract the specific attributes from each event
    extracted_data = []
    for event in data['events']:
        extracted_event = {
            'id': event.get('id'),
            'groupsIds': event.get('groupsIds', []),
            'groupsNames': event.get('groupsNames', []),
            'topic': event.get('topic'),
            'topicId': event.get('topicId')
        }
        extracted_data.append(extracted_event)

    # Save the extracted data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted data has been saved to {output_file}")

# Define the input and output file names for attribute extraction
input_file = 'data.json'  # This is the file created by the web scraping part
output_file = 'extracted_data.json'  # This is the file to save the extracted attributes

# Call the function to extract attributes
extract_attributes(input_file, output_file)
