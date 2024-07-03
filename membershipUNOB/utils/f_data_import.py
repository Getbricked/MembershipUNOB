import json
import asyncio
import aiohttp
from ._config import config_check_import, config_data
import os
from functools import cache
from async_lru import alru_cache

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

    async def queryGQL3(self, query, variables):
        times = 3
        result = None
        for i in range(times):
            try:
                result = await self.queryGQL(query=query, variables=variables)
                if result.get("errors", None) is None:
                    return result
                print(result)
            except Exception:
                pass

            await asyncio.sleep(10)

        raise Exception(
            f"unable to run query={query} with variables {variables} for {times} times\n{result}".replace(
                "'", '"'
            )
        )

    # def GetQuerySet(self, tableName):
    #     path = f"./gqls/{tableName}"
    #     querySet = gqlQueries.get(tableName, None)
    #     assert querySet is not None, f"missing query set for table {tableName}"
    #     return querySet

    @cache
    def GetQuery(self, tableName, queryType):
        assert queryType in [
            "read",
            "readp",
            "membership_add",
        ], f"unknown queryType {queryType}"
        queryfile = f"./gql/{queryType}.gql"
        # querySet = self.GetQuerySet(tableName=tableName)
        # query = querySet.get(queryType, None)
        with open(queryfile, "r", encoding="utf-8") as fi:
            lines = fi.readlines()
        query = "".join(lines)
        assert query is not None, f"missing {queryType} query for table {tableName}"
        return query

    @alru_cache(maxsize=1024)
    async def asyncTranslateID(self, outer_id, type_id):
        """prevede vnejsi id na vnitrni id pro dany typ,
        napr id (UCO) na id odpovidajici entity v nasem systemu
        """

        query = "query($type_id: UUID!, $outer_id: String!){ result: internalId(typeidId: $type_id, outerId: $outer_id) }"
        jsonData = await self.queryGQL3(
            query=query, variables={"outer_id": outer_id, "type_id": type_id}
        )
        data = jsonData.get("data", {"result": None})
        result = data.get("result", None)
        return result

    @alru_cache()
    async def getAllTypes(self):
        query = self.GetQuery(tableName="externalidtypes", queryType="readp")
        jsonData = await self.queryGQL3(query=query, variables={})
        data = jsonData.get("data", {"result": None})
        result = data.get("result", None)
        assert result is not None, f"unable to get externalidtypes"
        asdict = {item["name"]: item["id"] for item in result}
        return asdict

    @alru_cache(maxsize=1024)
    async def getTypeId(self, typeName):
        """podle typeName zjisti typeID
        cte pomoci query na gql endpointu
        """
        alltypes = await self.getAllTypes()
        result = alltypes.get(typeName, None)
        assert result is not None, f"unable to get id of type {typeName}"
        return result

    async def registerID(self, inner_id, outer_id, type_id):
        # assert inner_id is not None, f"missing {inner_id} in registerID"
        # assert outer_id is not None, f"missing {outer_id} in registerID"
        # assert type_id is not None, f"missing {type_id} in registerID"

        "zaregistruje vnitrni hodnotu primarniho klice (inner_id) a zpristupni jej pres puvodni id (outer_id a type_id)"
        mutation = """
            mutation ($type_id: UUID!, $inner_id: UUID!, $outer_id: String!) {
                result: externalidInsert(
                    externalid: {innerId: $inner_id, typeidId: $type_id, outerId: $outer_id}
                ) {
                    msg
                    result: externalid {
                        id    
                        }
                    }
                }
        """
        jsonData = await self.queryGQL3(
            query=mutation,
            variables={
                "inner_id": str(inner_id),
                "outer_id": outer_id,
                "type_id": str(type_id),
            },
        )
        data = jsonData.get("data", {"result": {"msg": "fail"}})
        msg = data["result"]["msg"]
        if msg != "ok":
            print(
                f'register ID failed ({ {"inner_id": inner_id, "outer_id": outer_id, "type_id": type_id} })\n\tprobably already registered'
            )
        else:
            print(f"registered {outer_id} for {inner_id} ({type_id})")
        return "ok"

    async def Read(self, tableName, variables, outer_id=None, outer_id_type_id=None):
        if outer_id:
            # read external id
            assert (
                outer_id_type_id is not None
            ), f"if outer_id ({outer_id}) defined, outer_id_type_id must be defined also "
            inner_id = await self.asyncTranslateID(
                outer_id=outer_id, type_id=outer_id_type_id
            )
            assert (
                inner_id is not None
            ), f"outer_id {outer_id} od type_id {outer_id_type_id} mapping failed on table {tableName}"
            variables = {**variables, "id": inner_id}

        queryRead = self.GetQuery(tableName, "read")
        response = await self.queryGQL3(query=queryRead, variables=variables)
        error = response.get("errors", None)
        assert (
            error is None
        ), f"error {error} during query \n{queryRead}\n with variables {variables}".replace(
            "'", '"'
        )
        data = response.get("data", None)
        assert (
            data is not None
        ), f"got no data during query \n{queryRead}\n with variables {variables}".replace(
            "'", '"'
        )
        result = data.get("result", None)
        # assert result is not None, f"missint result in response \n{response}\nto query \n{queryRead}\n with variables {variables}".replace("'", '"')
        return result

    async def Create(self, tableName, variables, outer_id=None, outer_id_type_id=None):
        queryType = "membership_add"
        if outer_id:
            # read external id
            assert (
                outer_id_type_id is not None
            ), f"if outer_id ({outer_id}) defined, outer_id_type_id must be defined also "
            inner_id = await self.asyncTranslateID(
                outer_id=outer_id, type_id=outer_id_type_id
            )

            if inner_id:
                print(
                    f"outer_id ({outer_id}) defined ({outer_id_type_id}) \t on table {tableName},\t going update"
                )
                old_data = await self.Read(
                    tableName=tableName, variables={"id": inner_id}
                )
                if old_data is None:
                    print(
                        f"found corrupted data, entity with id {inner_id} in table {tableName} is missing, going to create it"
                    )
                    variables = {**variables, "id": inner_id}
                else:
                    variables = {**old_data, **variables, "id": inner_id}
                    queryType = "update"
            else:
                print(
                    f"outer_id ({outer_id}) undefined ({outer_id_type_id}) \t on table {tableName},\t going insert"
                )
                registrationResult = await self.registerID(
                    inner_id=variables["id"],
                    outer_id=outer_id,
                    type_id=outer_id_type_id,
                )
                assert (
                    registrationResult == "ok"
                ), f"Something is really bad, ID reagistration failed"

        query = self.GetQuery(tableName, queryType)
        assert query is not None, f"missing {queryType} query for table {tableName}"
        response = await self.queryGQL3(query=query, variables=variables)
        data = response["data"]
        result = data["result"]  # operation result
        result = result["result"]  # entity result
        return result


async def db_writer_async():
    with open("systemdata.json", "r", encoding="utf-8") as f:
        systemdata = json.load(f)

    users = systemdata["users"]
    externalids = systemdata["externalids"]

    db_writer = DBWriter()

    for user in users:
        user["id"] = user["id"]
        await db_writer.Create(tableName="users", variables=user)

    for externalid in externalids:
        externalid["id"] = externalid["id"]
        externalid["inner_id"] = externalid["inner_id"]
        externalid["typeid_id"] = externalid["typeid_id"]
        await db_writer.registerID(
            inner_id=externalid["inner_id"],
            outer_id=externalid["outer_id"],
            type_id=externalid["typeid_id"],
        )


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
