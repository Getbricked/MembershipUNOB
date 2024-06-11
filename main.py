# main.py
from utils.b_get_group import get_group
from utils.c_get_student import get_student
from utils.extract_data import extract_data
from utils.f_data_import import data_import
from utils._config import config_web, config_data


def webscraping():
    html_file_path = "utils/b_list_groups.html"
    output_json_path = "utils/b_groups_data.json"

    if config_web["get_data"]:
        get_group(html_file_path, output_json_path)

        get_student()

    else:
        print("Skipping webscraping...")

    if config_web["extract_data"]:
        extract_data()

    else:
        print("Skipping data extraction...")


if __name__ == "__main__":
    webscraping()
    data_import(config_data)
