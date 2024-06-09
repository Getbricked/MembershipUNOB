from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4

def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, index=True, comment="primary key", default=uuid)