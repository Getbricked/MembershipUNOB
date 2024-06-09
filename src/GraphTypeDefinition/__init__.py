import typing
from typing import List, Union, Optional
import strawberry
import uuid
import datetime

from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def getLoader(info):
    return info.context["all"]


import datetime
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

from .query import Query
from .mutation import Mutation

from .userGQLModel import UserGQLModel # jen jako demo
from .groupGQLModel import GroupGQLModel
# from .groupTypeGQLModel import GroupTypeGQLModel
from .membershipGQLModel import MembershipGQLModel
# from .roleGQLModel import RoleGQLModel
# from .roleCategoryGQLModel import RoleCategoryGQLModel
# from .roleTypeGQLModel import RoleTypeGQLModel

# from .RBACObjectGQLModel import RBACObjectGQLModel
from .BaseGQLModel import IDType

schema = strawberry.federation.Schema(query=Query, types=(IDType), mutation=Mutation)