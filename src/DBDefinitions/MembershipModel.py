import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class MembershipModel(BaseModel):
    """Spojuje User s Group jestlize User je clen Group
    Umoznuje udrzovat historii spojeni
    """

    __tablename__ = "memberships"

    id = UUIDColumn()
    # name = Column(String)
    # group = Column(String)
    user_id = Column(ForeignKey("users.id"), index=True)
    group_id = Column(ForeignKey("groups.id"), index=True)
    valid = Column(Boolean, default=True, comment="if the membership is still active")
    # email = Column(String)
    # rocnik = Column(String)
    # fakulta = Column(String)
    # datova_schranka= Column(String)



    