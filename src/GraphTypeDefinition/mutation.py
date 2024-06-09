import strawberry
import typing

@strawberry.type
class Mutation:
    from .groupGQLModel import (
        group_insert,
        group_update,
        group_delete
    )
    group_insert = group_insert
    group_update = group_update
    group_delete = group_delete

    from .userGQLModel import (
        user_insert,
        user_update,
        user_delete
    )
    user_insert = user_insert
    user_update = user_update
    user_delete = user_delete

    from .membershipGQLModel import (
        membership_insert,
        membership_update,
        membership_delete
    )
    membership_insert = membership_insert
    membership_update = membership_update
    membership_delete = membership_delete
    
    # from .roleGQLModel import (
    #     role_insert,
    #     role_update,
    #     role_delete
    # )
    # role_insert = role_insert
    # role_update = role_update
    # role_delete = role_delete

    # from .roleTypeGQLModel import (
    #     role_type_insert,
    #     role_type_update,
    #     role_type_delete
    # )

    # role_type_insert = role_type_insert   
    # role_type_update = role_type_update
    # role_type_delete = role_type_delete

    # from .roleCategoryGQLModel import (
    #     role_category_insert,
    #     role_category_update,
    #     role_category_delete
    # )
    # role_category_insert = role_category_insert
    # role_category_update = role_category_update
    # role_category_delete = role_category_delete

    # from .groupTypeGQLModel import (
    #     group_type_insert,
    #     group_type_update,
    #     group_type_delete
    # )
    # group_type_insert = group_type_insert
    # group_type_update = group_type_update
    # group_type_delete = group_type_delete

    # from .groupCategoryGQLModel import (
    #     group_category_insert,
    #     group_category_update,
    #     group_category_delete
    # )
    # group_category_insert = group_category_insert
    # group_category_update = group_category_update
    # group_category_delete = group_category_delete

    # from .roleListGQLModel import (
    #     role_type_list_add,
    #     role_type_list_remove
    # )
    # role_type_list_add_role = role_type_list_add
    # role_type_list_remove_role = role_type_list_remove

    # @strawberry.mutation()
    # async def createUniversity(self, info: strawberry.types.Info, name: typing.Optional[str] = "Uni") -> str:
    #     asyncMaker = info.context["asyncSessionMaker"]
    #     from src.DBFeeder import randomDataStructure
    #     async with asyncMaker() as session:
    #         await randomDataStructure(session, name=name)
    #     return "ok"
    #     pass