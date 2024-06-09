import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel

class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem"""

    __tablename__ = "users"

    id = UUIDColumn()
    name = Column(String)
    # surname = Column(String)

    @hybrid_property
    def fullname(self):
        return self.name

    email = Column(String)
    # startdate = Column(DateTime, comment="first date of user in the system")
    # enddate = Column(DateTime, comment="last date of user in the system")
    valid = Column(Boolean, default=True, comment="if the user is still active")
    memberships = relationship("MembershipModel", back_populates="user", foreign_keys="MembershipModel.user_id")
    # roles = relationship("RoleModel", back_populates="user", foreign_keys="RoleModel.user_id")
    # groups = relationship("GroupModel", 
    #     secondary="join(MembershipModel, GroupModel, GroupModel.id==MembershipModel.group_id)",
    #     primaryjoin="UserModel.id==MembershipModel.user_id",
    #     secondaryjoin="GroupModel.id==MembershipModel.group_id",
    #     uselist=True,
    #     viewonly=True
    # )

    # created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    # lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    # createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    # changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # rbacobject = UUIDFKey(nullable=True, comment="holds object for role resolution")#Column(ForeignKey("users.id"), index=True, nullable=True)        