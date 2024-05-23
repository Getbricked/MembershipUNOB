# group_extractor.py
from bs4 import BeautifulSoup
import json
import uuid


def get_group(html_file_path, output_json_path):
    # Open the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <a> tags
    links = soup.find_all("a")

    # Initialize a list to store data
    data = []

    # Extract URL, group name, and group id from each <a> tag and store in data list
    for link in links:
        url = link["href"]
        group_id = str(uuid.uuid4())
        group_name = link.text.strip(";")
        data.append(
            {
                "group_id": group_id,
                "group_name": group_name,
                "url": "https://apl.unob.cz" + url,
            }
        )

    # Save data to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {output_json_path} file.")
