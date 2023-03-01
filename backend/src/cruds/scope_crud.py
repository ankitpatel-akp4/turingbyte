from src.cruds.database import get_db
from backend.src.models import models
from src.schemas import user_schemas
from sqlalchemy import asc, delete, desc, select, update, insert
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from src.commons import util
from src.commons import parameters



def update_scope(scope: user_schemas.ScopeCreate):
    print(scope, scope.dict())
    query = (update(models.Scope)
             .where(models.Scope.id == scope.id)
             .values(**scope.dict())
             .returning(models.Scope)
             )
    print(query)
    with get_db() as db:
        result = db.scalars(query)
        db.commit()
        result = result.one()
    return result


def delete_scope(id: int):
    query = (delete(models.Scope)
             .where(models.Scope.id == id)
             .returning(models.Scope)
             )
    print(query)
    with get_db() as db:
        result = db.scalars(query)
        db.commit()
        result = result.one()
    return result


def get_scope(filter: dict = parameters.filter(), sort: str = parameters.sort(), page: dict = parameters.page()):
    sort = util.map_sort(model=models.Scope, sort=sort)
    filter = util.map_attr(model=models.Scope, filter=filter)
    with get_db() as db:
        query = select(models.Scope).where(
            *filter).order_by(*sort).offset(page["offset"]).limit(page["limit"])
        result = db.scalars(query).all()
    return result