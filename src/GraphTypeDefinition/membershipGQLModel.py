import datetime
import strawberry
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

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class MembershipGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).MembershipModel

    id = resolve_id
    user = strawberry.field(
        description="""user""",
        resolver=DBResolvers.MembershipModel.user(UserGQLModel)
    )

    group = strawberry.field(
        description="""group""",

        resolver=DBResolvers.MembershipModel.group(GroupGQLModel)
    )

    valid = strawberry.field(
        description="""is the membership is still valid""",
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
        resolver=DBResolvers.MembershipModel.valid
    )
    
    # startdate = strawberry.field(
    #     description="""date when the membership begins""",
    #     # permission_classes=[
    #     #     OnlyForAuthentized
    #     # ],
    #     resolver=DBResolvers.MembershipModel.startdate
    # )
    
    # enddate = strawberry.field(
    #     description="""date when the membership ends""",
    #     # permission_classes=[
    #     #     OnlyForAuthentized
    #     # ],
    #     resolver=DBResolvers.MembershipModel.enddate
    # )

    # RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    # @strawberry.field(
    #     description="""""",
    #     permission_classes=[OnlyForAuthentized])
    # async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
    #     from .RBACObjectGQLModel import RBACObjectGQLModel
    #     result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.group_id)
    #     return result    

#####################################################################
#
# Special fields for query
#
#####################################################################
# from .utils import createInputs
from dataclasses import dataclass
GroupInputWhereFilter = Annotated["GroupInputWhereFilter", strawberry.lazy(".groupGQLModel")]
UserInputWhereFilter = Annotated["UserInputWhereFilter", strawberry.lazy(".userGQLModel")]
@createInputs
@dataclass
class MembershipInputWhereFilter:
    valid: bool
    # from .userGQLModel import UserInputWhereFilter
    # from .groupGQLModel import GroupInputWhereFilter
    group: GroupInputWhereFilter
    user: UserInputWhereFilter

# from ._GraphResolvers import asPage

membership_page = strawberry.field(
    description="Retrieves memberships",
    # permission_classes=[
    #     OnlyForAuthentized
    # ],
    resolver=DBResolvers.MembershipModel.resolve_page(MembershipGQLModel, WhereFilterModel=MembershipInputWhereFilter)
)

membership_by_id = strawberry.field(
    description="Retrieves the membership",
    # permission_classes=[
    #     OnlyForAuthentized
    # ],
    resolver=DBResolvers.MembershipModel.resolve_by_id(MembershipGQLModel)
)
#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class MembershipUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    changedby: strawberry.Private[IDType] = None
    group_id: strawberry.Private[IDType] = None

@strawberry.input(description="")
class MembershipInsertGQLModel:
    user_id: IDType
    group_id: IDType
    id: Optional[IDType] = strawberry.field(description="Primary key of entity", default_factory=uuid.uuid1)
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[IDType] = None
    

@strawberry.type(description="")
class MembershipResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of membership operation""")
    async def membership(self, info: strawberry.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
class UpdateMembershipPermission():
    message = "User is not allowed to change membership"
    async def has_permission(self, source, info: strawberry.types.Info, membership: "MembershipUpdateGQLModel") -> bool:
        loader = MembershipGQLModel.getLoader(info)
        row = await loader.load(membership.id)
        membership.group_id = row.group_id

        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        role = await self.resolveUserRole(info, 
            rbacobject=membership.group_id,
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not role: return False
        # roleTypeName = role["type"]["name"]
        # if roleTypeName in allowedRoleNames:
        #     if group.mastergroup_id:
        #         raise self.error_class(f"{roleTypeName} cannot change mastergroup_id")
        #     if group.grouptype_id:
        #         raise self.error_class(f"{roleTypeName} cannot change grouptype_id")
        return True


@strawberry.mutation(
    description="""Update the membership, cannot update group / user""",)
async def membership_update(self, 
    info: strawberry.types.Info, 
    membership: "MembershipUpdateGQLModel"
) -> "MembershipResultGQLModel":
    return await encapsulateUpdate(info, MembershipGQLModel.getLoader(info), membership, MembershipResultGQLModel(id=membership.id, msg="ok"))

# class InsertMembershipPermission():
#     message = "User is not allowed create new membership"
#     async def has_permission(self, source, info: strawberry.types.Info, membership: "MembershipInsertGQLModel") -> bool:
#         adminRoleNames = ["administrátor"]
#         allowedRoleNames = ["garant"]
#         role = await self.resolveUserRole(info, 
#             rbacobject=membership.group_id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.mutation(
    description="""Inserts new membership""",
    # permission_classes=[
    #     OnlyForAuthentized,
    #     InsertMembershipPermission
    # ]
    )
async def membership_insert(self, 
    info: strawberry.types.Info, 
    membership: "MembershipInsertGQLModel"
) -> "MembershipResultGQLModel":
    return await encapsulateInsert(info, MembershipGQLModel.getLoader(info), membership, MembershipResultGQLModel(id=membership.id, msg="ok"))

@strawberry.mutation(
    description="Deletes the membership",
    # permission_classes=[
    #     OnlyForAuthentized,
    #     OnlyForAdmins
    # ]
    )
async def membership_delete(self, info: strawberry.types.Info, id: IDType) -> MembershipResultGQLModel:
    return await encapsulateDelete(info, MembershipGQLModel.getLoader(info), id, MembershipResultGQLModel(msg="ok", id=None))