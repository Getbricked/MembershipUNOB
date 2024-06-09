import sqlalchemy

from .Base import BaseModel
from .UUID import UUIDColumn
from .MembershipModel import MembershipModel
from .UserModel import UserModel
from .GroupModel import GroupModel
Model =[
    UserModel,
    GroupModel,
    MembershipModel
]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

dbInitIsDone = False

def startSyncEngine(connectionstring=None) -> Session:
    if connectionstring is None:
        connectionstring = ComposeConnectionString()
    syncEngine = create_engine(connectionstring)
    sessionMaker = sessionmaker(syncEngine, expire_on_commit=False)
    assert dbInitIsDone == True, "Seems DB has not been initialized"
    return sessionMaker

async def startEngine(connectionstring=None, makeDrop=False, makeUp=True) -> AsyncSession:
    if connectionstring is None:
        connectionstring = ComposeConnectionString()
    global dbInitIsDone
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring, pool_pre_ping=True)
    # pool_size=20, max_overflow=10, pool_recycle=60) #pool_pre_ping=True, pool_recycle=3600

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None
    dbInitIsDone = True
    
    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring