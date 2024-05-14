from bs4 import BeautifulSoup
import json

# Open the HTML file
with open("list_groups.html", "r", encoding="utf-8") as file:
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
    group_id = url.split("/")[-1]
    group_name = link.text.strip(";")
    data.append(
        {
            "group_id": group_id,
            "group_name": group_name,
            "url": "https://apl.unob.cz" + url,
        }
    )

# Save data to a JSON file
with open("urls.json", "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Data has been saved to urls.json file.")
