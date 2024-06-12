# main.py
from utils.b_get_group import get_group
from utils.c_get_student import get_student
from utils.extract_data import extract_data
from utils.f_data_import import data_import


def webscraping():
    html_file_path = "utils/b_list_groups.html"
    output_json_path = "utils/b_groups_data.json"

    get_group(html_file_path, output_json_path)

    get_student()

    extract_data()


def main():
    webscraping()
    data_import()


if __name__ == "__main__":
    main()
