import strawberry

@strawberry.type(description="""Type for query root""")
class Query:

    from .userGQLModel import (
        user_by_id, 
        user_page,)
    user_by_id = user_by_id
    user_page = user_page


    from .groupGQLModel import group_by_id
    group_by_id = group_by_id

    from .groupGQLModel import group_page
    group_page = group_page

    

    from .membershipGQLModel import (
        membership_page,
        membership_by_id
    )
    membership_page = membership_page
    membership_by_id = membership_by_id

   