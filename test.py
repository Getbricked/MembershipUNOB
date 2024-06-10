import json
import asyncio
import aiohttp

class DBWriter:
    def __init__(self, username="john.newbie@world.com", password="john.newbie@world.com"):
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

            payload = {"key": keyJson["key"], "username": self.username, "password": self.password}
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
        cookies = {'authorization': token}
        async with aiohttp.ClientSession() as session:
            async with session.post(gqlurl, json=payload, cookies=cookies) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    print(f"failed query \n{query}\n with variables {variables}".replace("'", '"'))
                    print(f"failed resp.status={resp.status}, text={text}")
                    raise Exception(f"Unexpected GQL response", text)
                else:
                    response = await resp.json()
                    return response
                
async def add_users_from_json(json_file, db_writer):
    with open(json_file, 'r', encoding="utf-8")as file:
        data = json.load(file)

    users = data.get('users',[])
    if not isinstance(users, list):
        raise ValueError("Dữ liệu JSON phải là một danh sách các đối tượng trong mục 'users'")
    mutation ="""
    mutation($id: UUID!, $name: String!, $surname: String!, $email: String!) {
        result: userInsert(user: {id: $id, name: $name, surname: $surname, email: $email}) {
            id
            msg
            result: user {
                id
                lastchange
            }
        }
    }
    """
    tasks =[]

    semaphore = asyncio.Semaphore(5)  # Giới hạn số lượng kết nối đồng thời
    async def limited_query(mutation, variables):
        async with semaphore:
            return await db_writer.queryGQL(mutation, variables)
        
    for item in users:
        if not isinstance(item, dict):
            raise ValueError("Mỗi mục trong danh sách dữ liệu JSON phải là một đối tượng (dictionary)")
        
        variables ={
            "id": item["id"],
            "name":item["name"],
            "surname":item["surname"],
            "email":item["email"]
        }
        tasks.append(limited_query(mutation, variables))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    with open('results.txt', 'w', encoding='utf-8') as result_file:
        for result in results:
            if isinstance(result, Exception):
                result_file.write(f"Error: {result}\n")
                print(f"Error: {result}")
            else:
                result_file.write(f"Success: {result}\n")
                print(f"Success: {result}")



async def add_groups_from_json(json_file, db_writer):
    with open(json_file, 'r', encoding="utf-8")as file:
        data = json.load(file)

    groups = data.get('groups',[])
    if not isinstance(groups, list):
        raise ValueError("Dữ liệu JSON phải là một danh sách các đối tượng trong mục 'groups'")
    mutation ="""
    mutation($id: UUID!, $name: String!, $grouptype_id: UUID!) {
    result: groupInsert(group: {id: $id, name: $name, grouptypeId: $grouptype_id}) {
            id
            msg
            result: group {
                id
                lastchange
            }
        }
    }
    """
    tasks =[]

    semaphore = asyncio.Semaphore(5)  # Giới hạn số lượng kết nối đồng thời
    async def limited_query(mutation, variables):
        async with semaphore:
            return await db_writer.queryGQL(mutation, variables)
        
    for item in groups:
        if not isinstance(item, dict):
            raise ValueError("Mỗi mục trong danh sách dữ liệu JSON phải là một đối tượng (dictionary)")
        
        variables ={
            "id": item["id"],
            "name":item["name"],
            "grouptype_id":item["grouptype_id"],
        }
        tasks.append(limited_query(mutation, variables))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    with open('results2.txt', 'w', encoding='utf-8') as result_file:
        for result in results:
            if isinstance(result, Exception):
                result_file.write(f"Error: {result}\n")
                print(f"Error: {result}")
            else:
                result_file.write(f"Success: {result}\n")
                print(f"Success: {result}")



async def add_memberships_from_json(json_file, db_writer):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    memberships = data.get('memberships', [])
    if not isinstance(memberships, list):
        raise ValueError("Dữ liệu JSON phải là một danh sách các đối tượng trong mục 'memberships'")

    mutation = """
    mutation($id: UUID!, $user_id: UUID!, $group_id: UUID!, $valid: Boolean ) {
      result: membershipInsert(membership: {id: $id, userId: $user_id, groupId: $group_id, valid: $valid}) {
        id
        msg
        result: membership {
          id
          lastchange
        }
      }
    }
    """

    tasks = []
    semaphore = asyncio.Semaphore(5)  # Giới hạn số lượng kết nối đồng thời

    async def limited_query(mutation, variables):
        async with semaphore:
            return await db_writer.queryGQL(mutation, variables)

    for item in memberships:
        if not isinstance(item, dict):
            raise ValueError("Mỗi mục trong danh sách dữ liệu JSON phải là một đối tượng (dictionary)")

        variables = {
            "id": item["id"],
            "user_id": item["user_id"],
            "group_id": item["group_id"],
            "valid": item.get("valid")
            # "startdate": None,
            # "enddate": None
        }
        tasks.append(limited_query(mutation, variables))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    with open('results3.txt', 'w', encoding='utf-8') as result_file:
        for result in results:
            if isinstance(result, Exception):
                result_file.write(f"Error: {result}\n")
                print(f"Error: {result}")
            else:
                result_file.write(f"Success: {result}\n")
                print(f"Success: {result}")

def main():
    json_file = 'systemdata.json'  # Thay thế bằng đường dẫn tới tệp JSON của bạn
    db_writer = DBWriter()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_users_from_json(json_file, db_writer))
    loop.run_until_complete(add_groups_from_json(json_file, db_writer))
    loop.run_until_complete(add_memberships_from_json(json_file, db_writer))

if __name__ == "__main__":
    main()
