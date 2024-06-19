import json
import time
import uuid
import os


def create_externalids(students, memberships, externalidtypes):
    externalids = []
    from .extract_data import open_file

    externalids_data = open_file("systemdata.json", "externalids")

    externalids_dict = {
        (item["inner_id"], item["outer_id"]): item["id"] for item in externalids_data
    }

    memberships_dict = {
        (item["user_id"], item["group_id"]): item["id"] for item in memberships
    }

    for student in students:
        link = student.get("link")
        outer_id = str(link).split("/")[-1]
        inner_id = memberships_dict.get(
            (student["id"], student["group_id"]), str(uuid.uuid4())
        )
        id = externalids_dict.get((inner_id, outer_id), str(uuid.uuid4()))

        externalids.append(
            {
                "id": id,
                "inner_id": inner_id,
                "outer_id": outer_id,
                "type_id": externalidtypes[0]["id"],
            }
        )

    return externalids
