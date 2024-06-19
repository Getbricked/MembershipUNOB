import json
import time
import uuid
import os

from .d_create_externalids import create_externalids
from ._config import config_check_web, config_web


def open_file(path, data_name):
    if os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
            if data_name in data:
                out_data = data[data_name]
            else:
                out_data = []
    else:
        out_data = []

    return out_data


@config_check_web(config_web["extract_data"])
def extract_data():

    module_dir = os.path.dirname(__file__)
    student_path = os.path.join(module_dir, "c_students_data.json")
    group_path = os.path.join(module_dir, "b_groups_data.json")
    # Load the data from the JSON files
    students = open_file(student_path, "users")
    groups = open_file(group_path, "groups")

    # Crewate a JSON file if it doesn't exist
    json_file = "systemdata.json"
    if os.path.exists(json_file):
        # If the file exists, load data from it
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        # If the file doesn't exist, initialize an empty data structure
        data = {}

        # Optionally, you can write the empty data to the file
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # Create a dictionary of old memberships base on group_id and user_id
    old_memberships = open_file("systemdata.json", "memberships")
    old_memberships_dict = {
        (m["user_id"], m["group_id"]): m["id"] for m in old_memberships
    }

    # Define the new data structures for memberships and users
    memberships = []
    users = []

    # Reformat the student data and create new memberships
    for student in students:
        # Split the name into parts
        name_parts = student["name"].split()

        # Assume the first part is the surname and the rest is the first name
        surname = name_parts[0]
        name = " ".join(name_parts[1:])

        membership_id = old_memberships_dict.get(
            (student["id"], student["group_id"]), str(uuid.uuid4())
        )

        memberships.append(
            {
                "id": membership_id,
                "user_id": student["id"],
                "group_id": student["group_id"],
                "valid": True,
            }
        )

        users.append(
            {
                "id": student["id"],
                "name": name,
                "surname": surname,
                "email": student["email"],
                # "group_id": student["group_id"],
                # "rocnik": student["rocnik"],
                # "fakulta": student["fakulta"],
                # "datova_schranka": student["datova_schranka"],
                # "valid": True,
            }
        )
    list_length = len(memberships)
    print(f"Number of memberships: {list_length}")

    # Create externalidtypes
    externalidtypes = []

    # Default externalidtype for MojeAP-Student from gqlUG
    externalidtypes.append(
        {
            "id": "d5bfe043-f82e-4d24-baa2-524a4f443ed0",
            "name": "MojeAP-Student",
            "name_en": "UCO",
            "urlformat": "https://apl.unob.cz/MojeAP/Student/%s",
            "category_id": "0ee3a92d-971f-499a-956f-ca6edb8d6094",
        }
    )

    # Create externalids
    externalids = create_externalids(students, memberships, externalidtypes)

    # Merge the old memberships with the new ones
    membership_dict = {}

    for m in old_memberships:
        membership_dict[m["id"]] = m

    for m in memberships:
        membership_dict[m["id"]] = {**membership_dict.get(m["id"], {}), **m}

    filtered_memberships = list(membership_dict.values())

    # Remove the URL parameter from the groups
    for group in groups:
        if "url" in group:
            del group["url"]

    # Save the extracted data to a JSON file
    extracted_data = {
        "externalidtypes": externalidtypes,
        "externalids": externalids,
        "groups": groups,
        "users": users,
        "memberships": filtered_memberships,
    }
    with open("systemdata.json", "w", encoding="utf-8") as outfile:
        json.dump(extracted_data, outfile, ensure_ascii=False, indent=4)
