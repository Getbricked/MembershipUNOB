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


class GroupModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "groups"

    id = UUIDColumn()
    name = Column(String, comment="name of the group")
    # name_en = Column(String, comment="english name of the group")
    # abbreviation = Column(String, comment="name abbreviation of the group")
    # email = Column(String, comment="can be an email for whole group")

    # startdate = Column(DateTime, comment="born date of the group")
    # enddate = Column(DateTime, comment="date when group `died`")
    # valid = Column(Boolean, default=True, comment="if the group still exists")

    # grouptype_id = Column(ForeignKey("grouptypes.id"), index=True, comment="link to the group type (aka faculty)")
    # grouptype = relationship("GroupTypeModel", back_populates="groups")
    # mastergroup_id = Column(ForeignKey("groups.id"), index=True, comment="link to the commanding group")
    memberships = relationship("MembershipModel", back_populates="group")
    # roles = relationship("RoleModel", back_populates="group")

    # created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    # lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    # createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    # changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)

    # rbacobject = UUIDFKey(nullable=True, comment="holds object for role resolution")#Column(ForeignKey("users.id"), index=True, nullable=True)    