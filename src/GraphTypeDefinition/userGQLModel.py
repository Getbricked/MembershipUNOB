import datetime
import strawberry
import asyncio
import uuid
from typing import List, Optional, Union, Annotated
from uoishelpers.resolvers import createInputs

from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete
)

from src.DataLoader import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)
from src.DBResolvers import DBResolvers


MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
# RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]

# RoleInputWhereFilter = Annotated["RoleInputWhereFilter", strawberry.lazy(".roleGQLModel")]
MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).UserModel

    id = resolve_id
    name = resolve_name
    
    surname = strawberry.field(
        description="""User's family name (like Obama)""",
        resolver=DBResolvers.UserModel.name
    )  

    email = strawberry.field(
        description="""User's email""",
        resolver=DBResolvers.UserModel.email
    )

    valid = strawberry.field(
        description="""If the user is still valid""",
        resolver=DBResolvers.UserModel.valid
    )

    memberships = strawberry.field(
        description="""List of mmeberships associated with the user""",
        resolver=DBResolvers.UserModel.memberships(MembershipGQLModel, WhereFilterModel=MembershipInputWhereFilter)
    )

    membership = strawberry.field(
        description="""List of mmeberships associated with the user""",
        deprecation_reason="use memberships",
        resolver=DBResolvers.UserModel.memberships(MembershipGQLModel, WhereFilterModel=MembershipInputWhereFilter)
    )

    
    @strawberry.field(
        description="""User's family name (like Obama)""")
    def fullname(self) -> Optional[str]:
        return self.fullname


    # @strawberry.field(
    #     description="""GDPRInfo for permision test""", 
    #     permission_classes=[OnlyForAuthentized, UserGDPRPermission])
    # def GDPRInfo(self, info: strawberry.types.Info) -> Union[str, None]:
    #     actinguser = getUser(info)
    #     print(actinguser)
    #     return "GDPRInfo"


    @strawberry.field(
        description="""List of groups given type, where the user is member""")
    async def member_of(
        self, info: strawberry.types.Info, grouptype_id: Optional[IDType] = None, 
    ) -> List["GroupGQLModel"]:
        from .groupGQLModel import GroupGQLModel
        from .membershipGQLModel import MembershipGQLModel
        loader = MembershipGQLModel.getLoader(info)
        rows = await loader.filter_by(user_id=self.id)# , grouptype_id=grouptype_id)
        results = (GroupGQLModel.resolve_reference(info, row.group_id) for row in rows)
        results = await asyncio.gather(*results)
        if grouptype_id:
            results = filter(lambda item: item.grouptype_id == grouptype_id, results)
        return results
    
    # RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    # @strawberry.field(
    #     description="""Who made last change""")
    # async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
    #     from .RBACObjectGQLModel import RBACObjectGQLModel
    #     result = None if self.id is None else await RBACObjectGQLModel.resolve_reference(info, self.id)
    #     return result    

#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
#MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]

user_by_id = strawberry.field(
    description="",
    resolver=DBResolvers.UserModel.resolve_by_id(UserGQLModel)
)

@createInputs
@dataclass
class UserInputWhereFilter:
    id: IDType
    name: str
    surname: str
    email: str
    fullname: str
    valid: bool
    from .membershipGQLModel import MembershipInputWhereFilter
    memberships: MembershipInputWhereFilter
# from ._GraphResolvers import createRootResolver_by_page, asPage

user_page = strawberry.field(
    description="returns list of users",
    resolver=DBResolvers.UserModel.resolve_page(UserGQLModel, WhereFilterModel=UserInputWhereFilter)
    )




@strawberry.field(
    description="""This is logged user""",)
async def me(self,
    info: strawberry.types.Info) -> Optional[UserGQLModel]:
    result = None
    user = getUserFromInfo(info)
    if user is None: return None
    user_id = user.get("id", None)
    if user_id is None: return None
    # user_id = IDType(user_id)
    result = await UserGQLModel.resolve_reference(info, user_id)
    return result


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="Describes values for U operation on UserGQLModel")
class UserUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime  # razitko
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="Describes initial values for C operation on UserGQLModel")
class UserInsertGQLModel:
    id: Optional[IDType] = strawberry.field(description="primary key", default_factory=uuid.uuid1)
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None
    createdby: strawberry.Private[IDType] = None

@strawberry.type
class UserResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def user(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result

# class UpdateUserPermission():
#     message = "User is not allowed to update the user"
#     async def has_permission(self, source, info: strawberry.types.Info, user: UserUpdateGQLModel) -> bool:
#         adminRoleNames = ["administrátor", "personalista"]
#         allowedRoleNames = []
#         role = await self.resolveUserRole(info, 
#             rbacobject=user.id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.mutation(
    description="")
async def user_update(self, info: strawberry.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
    return await encapsulateUpdate(info, UserGQLModel.getLoader(info), user, UserResultGQLModel(msg="ok", id=user.id))

# class InsertUserPermission():
#     message = "User is not allowed to create an user"
#     async def has_permission(self, source, info: strawberry.types.Info, user: UserInsertGQLModel) -> bool:
#         adminRoleNames = ["administrátor", "personalista"]
#         allowedRoleNames = []
#         role = await self.resolveUserRole(info, 
#             rbacobject=user.id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.mutation(description="")
async def user_insert(self, info: strawberry.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
    return await encapsulateInsert(info, UserGQLModel.getLoader(info), user, UserResultGQLModel(msg="ok", id=None))

@strawberry.mutation(description="")
async def user_delete(self, info: strawberry.types.Info, id: IDType) -> UserResultGQLModel:
    return await encapsulateDelete(info, UserGQLModel.getLoader(info), id, UserResultGQLModel(msg="ok", id=None))
