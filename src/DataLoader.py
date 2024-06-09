import logging
from uoishelpers.dataloaders import createIdLoader
import uuid

from src.DBDefinitions import (
    BaseModel,
    # UserModel,
    # MembershipModel,
    # GroupModel,
    # GroupTypeModel,
    # RoleModel,
    # RoleTypeModel,
    # RoleCategoryModel,
    # RoleTypeListModel
)

# from uoishelpers.resolvers import select, update, delete

from uoishelpers.dataloaders import createIdLoader
from functools import cache

def createLoaders(asyncSessionMaker):

    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)

    attrs = {}

    for DBModel in BaseModel.registry.mappers:
        cls = DBModel.class_
        attrs[cls.__tablename__] = property(cache(createLambda(asyncSessionMaker, cls)))
        attrs[cls.__name__] = attrs[cls.__tablename__]
    
    # attrs["authorizations"] = property(cache(lambda self: AuthorizationLoader()))
    Loaders = type('Loaders', (), attrs)   
    return Loaders()


def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        request = context.get("request", None)
        assert request is not None, context
        result = request.scope["user"]

    if result is None:
        result = {"id": None}
    else:
        result = {**result, "id": uuid.UUID(result["id"])}
    # logging.debug("getUserFromInfo", result)
    return result

def getLoadersFromInfo(info):
    # print("info", info)
    context = info.context
    # print("context", context)
    loaders = context.get("loaders", None)
    assert loaders is not None, f"'loaders' key missing in context"
    return loaders

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }