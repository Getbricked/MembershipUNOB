# group_extractor.py
from bs4 import BeautifulSoup
import json
import uuid
import os


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

    if os.path.getsize(output_json_path) > 0:
        with open(output_json_path, "r", encoding="utf-8") as old_data_file:
            old_groups = json.load(old_data_file)["groups"]
    else:
        old_groups = []

    old_groups_lookup = {
        (group["name"], group["url"]): group["id"] for group in old_groups
    }

    # Extract URL, group name, and group id from each <a> tag and store in data list
    for link in links:
        url = "https://apl.unob.cz" + link["href"]
        group_name = link.text.strip(";")
        group_id = old_groups_lookup.get((group_name, url), str(uuid.uuid4()))
        data.append(
            {
                "id": group_id,
                "name": group_name,
                "url": url,
                "valid": True,
            }
        )

    data = {"groups": data}

    # Save data to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    print(f"Data has been saved to {output_json_path} file.")
