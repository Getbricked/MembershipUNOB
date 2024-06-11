import json
import time
import uuid
import os

from utils.d_create_externalids import create_externalids


def extract_data():

    # Get student data
    if os.path.getsize("utils/c_students_data.json") > 0:
        with open("utils/c_students_data.json", "r", encoding="utf-8") as data_file:
            students = json.load(data_file)["users"]
    else:
        students = []

    # Get group data
    if os.path.getsize("utils/b_groups_data.json") > 0:
        with open("utils/b_groups_data.json", "r", encoding="utf-8") as data_file:
            groups = json.load(data_file)["groups"]
    else:
        groups = []

    memberships = []
    users = []

    # create_externalids(students)

    # Get old memberships data
    if os.path.getsize("systemdata.json") > 0:
        with open("systemdata.json", "r", encoding="utf-8") as data_file:
            data = json.load(data_file)
            if "memberships" in data:
                old_memberships = data["memberships"]
            else:
                old_memberships = []
    else:
        old_memberships = []

    # Create a dictionary of old memberships base on group_id and user_id
    old_memberships_dict = {
        (m["user_id"], m["group_id"]): m["id"] for m in old_memberships
    }

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
                # "group_id": student["group_id"],
                "email": student["email"],
                # "rocnik": student["rocnik"],
                # "fakulta": student["fakulta"],
                # "datova_schranka": student["datova_schranka"],
                "valid": True,
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
