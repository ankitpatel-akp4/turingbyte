# from __future__ import annotations
# from datetime import datetime
# from time import timezone
# from sqlalchemy import (
# func, select, text,TIMESTAMP
# )
# from sqlalchemy.orm import (
#     relationship, mapped_column, selectinload,
#     Mapped, DeclarativeBase, declared_attr, has_inherited_table
# )
# from src.cruds.database import get_db
# from src.commons import parameters, util


# class Base(DeclarativeBase):
#     @declared_attr.directive
#     def __tablename__(cls):
#         if has_inherited_table(cls):
#             return None
#         return cls.__name__.lower()+"s"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"),)

#     __mapper_args__ = {'eager_defaults':True}
#     async def save(self):
#         db = get_db()
#         db.add(self)
#         await db.commit()
#         await db.refresh(self)

#     async def update(self,data:dict={}):
#         for attr, value in data.items():
#             setattr(self,attr,value)
#         db = get_db()
#         await db.commit()
    
#     async def delete(self):
#         db = get_db()
#         await db.delete(self) 
#         await db.commit()

#     def _get_eager_load_items(cls,eager_load:dict={}):
#         return [selectinload(getattr(cls,x)) for x in eager_load]

#     @classmethod
#     async def get(cls, id:int,eager_load:list[str]=[])->Base:
#         """It takes the id and a Optional list of relation that needs to be loaded eargely"""
#         db = get_db()
#         result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls,eager_load)).where(getattr(cls,"id")==id))
#         return result.first()
#     @classmethod
#     async def get_all(cls, id:int,eager_load:list[str]=[])->Base:
#         """It takes an Optional list of relation that needs to be loaded eargely"""
#         db = get_db()
#         result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)))
#         return result.all()
#     @classmethod
#     async def get_by_attr(cls, attr:str,value,eager_load:list[str]=[])->Base:
#         """It takes the attr and an Optional list of relations that needs to be loaded eargely"""
#         db = get_db()
#         result = await db.scalars(select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)).where(getattr(cls,attr)==value))
#         return result.all()
    
#     @classmethod
#     async def search(cls,filter: dict = parameters.filter(), sort: str = parameters.sort(), page: dict = parameters.page(),eager_load:list[str]=[]):
#         """this is a search function"""
#         sort = util.map_sort(model=cls, sort=sort)
#         filter = util.map_attr(model=cls, filter=filter)
#         db = get_db()
#         query = select(cls).options(*cls._get_eager_load_items(cls=cls,eager_load=eager_load)).where(
#             *filter).order_by(*sort).offset(page["offset"]).limit(page["limit"])
#         result = await db.scalars(query)
        
#         return result.all()
