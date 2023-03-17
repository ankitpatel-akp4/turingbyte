from __future__ import annotations
from fastapi import Depends
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime
from sqlalchemy import (
create_engine, func, select, text,TIMESTAMP
)
from sqlalchemy.orm import (
    relationship, mapped_column, selectinload,
    Mapped, DeclarativeBase, declared_attr, has_inherited_table, Session
)
from src.commons import parameters, util
from src.commons.context import current_context
from src.commons.config import settings


ASYNC_SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL
                                #    ,echo=True
                                #    ,future=True
                                   )
engine = create_engine(SQLALCHEMY_DATABASE_URL
                                #    ,echo=True
                                #    ,future=True
                                   )
AsyncLocalSession = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine,class_=AsyncSession)
LocalSession = async_sessionmaker(engine, expire_on_commit=False, class_=Session)


async def _get_db()->AsyncSession:
    db = AsyncLocalSession()
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        await db.commit()
        await db.close()

async def set_db(db_session:AsyncSession=Depends(_get_db))->None:
    current_context.get().db_session = db_session

def get_db()->AsyncSession:
    db_session = current_context.get().db_session
    return db_session



class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"),)

    # __mapper_args__ = {'eager_defaults':True}
    async def save(self):
        db = get_db()
        db.add(self)
        await db.commit()
        await db.refresh(self)

    async def update(self,data:dict={}):
        for attr, value in data.items():
            setattr(self,attr,value)
        db = get_db()
        await db.commit()
        await db.refresh(self)
    
    async def delete(self):
        db = get_db()
        await db.delete(self) 
        await db.commit()

    def _get_eager_load_items(cls,eager_load:dict={}):
        return [selectinload(getattr(cls,x)) for x in eager_load]


    @classmethod
    async def get(cls, id:int,eager_load:list[str]=[]):
        """It takes the id and a Optional list of relation that needs to be loaded eargely"""
        db = get_db()
        result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls,eager_load)).where(getattr(cls,"id")==id))
        return result.first()
    @classmethod
    async def get_all(cls, eager_load:list[str]=[]):
        """It takes an Optional list of relation that needs to be loaded eargely"""
        db = get_db()
        result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)))
        return result.all()
    @classmethod
    async def get_by_attr(cls, attr:str,value,eager_load:list[str]=[]):
        """It takes the attr and an Optional list of relations that needs to be loaded eargely"""
        db = get_db()
        result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)).where(getattr(cls,attr)==value))
        return result.all()
    
    @classmethod
    async def search(cls,filter: dict = {}, sort: str = parameters.sort(), page: dict = parameters.page(),eager_load:list[str]=[]):
        """this is a search function"""
        sort = util.map_sort(model=cls, sort=sort)
        filter = util.map_attr(model=cls, filter=filter)
        db = get_db()
        print(filter)
        query = select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)).where(
            *filter).order_by(*sort).offset(page["offset"]).limit(page["limit"])
        result = await db.scalars(query)
        return result.all()


