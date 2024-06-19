import json
import asyncio
import aiohttp
from ._config import config_check_import, config_data
import os

config = config_data


class DBWriter:
    def __init__(
        self, username="john.newbie@world.com", password="john.newbie@world.com"
    ):
        self.username = username
        self.password = password
        self.token = None

    async def getToken(self):
        if self.token:
            return self.token

        keyurl = "http://localhost:33001/oauth/login3"
        async with aiohttp.ClientSession() as session:
            async with session.get(keyurl) as resp:
                keyJson = await resp.json()

            payload = {
                "key": keyJson["key"],
                "username": self.username,
                "password": self.password,
            }
            async with session.post(keyurl, json=payload) as resp:
                tokenJson = await resp.json()
        self.token = tokenJson.get("token", None)
        return self.token

    async def queryGQL(self, query, variables):
        gqlurl = "http://localhost:33001/api/gql"
        token = self.token
        if token is None:
            token = await self.getToken()
        payload = {"query": query, "variables": variables}
        cookies = {"authorization": token}
        async with aiohttp.ClientSession() as session:
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    print(
                        f"failed query \n{query}\n with variables {variables}".replace(
                            "'", '"'
                        )
                    )
                    print(f"failed resp.status={resp.status}, text={text}")
                    raise Exception(f"Unexpected GQL response", text)
                else:
                    response = await resp.json()
                    return response


async def execute_mutation(data, db_writer, graphql_dir):
    # Get the mutation graphql from the file
    with open(graphql_dir, "r", encoding="utf-8") as file:
        mutation = file.read()

    # Check if the data is a list
    if not isinstance(data, list):
        raise ValueError("JSON data must be a list!")

    # Limited to 5 concurrent connections at the same time
    semaphore = asyncio.Semaphore(5)

    async def limited_query(mutation, variables):
        async with semaphore:
            return await db_writer.queryGQL(mutation, variables)

    tasks = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item must be a dictionary in the JSON data list!")

        variables = item
        tasks.append(limited_query(mutation, variables))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    with open("results.txt", "a", encoding="utf-8") as result_file:
        for result in results:
            if isinstance(result, Exception):
                result_file.write(f"Error: {result}\n")
                print(f"Error: {result}")
            else:
                result_file.write(f"Success: {result}\n")
                print(f"Success: {result}")


@config_check_import("users")
async def import_user(data, db_writer, gql_func):
    await execute_mutation(data, db_writer, gql_func)


@config_check_import("groups")
async def import_group(data, db_writer, gql_func):
    await execute_mutation(data, db_writer, gql_func)


@config_check_import("memberships")
async def import_membership(data, db_writer, gql_func):
    await execute_mutation(data, db_writer, gql_func)


def data_import():
    json_file = "systemdata.json"

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    script_dir = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    user_gql = os.path.join(base_dir, "membershipUNOB", "gql", "user_add.gql")
    group_gql = os.path.join(base_dir, "membershipUNOB", "gql", "group_add.gql")
    membership_gql = os.path.join(
        base_dir, "membershipUNOB", "gql", "membership_add.gql"
    )

    loop = asyncio.get_event_loop()
    db_writer = DBWriter()

    async def import_data():
        await import_user(config, data, db_writer, user_gql)
        await import_group(config, data, db_writer, group_gql)
        await import_membership(config, data, db_writer, membership_gql)

    loop.run_until_complete(import_data())
