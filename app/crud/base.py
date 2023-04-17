#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# TODO(LiuTingwei): future select
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        _q = (
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.deleted == false())
        )
        async with db() as _session:
            _r = await _session.execute(_q)
            _d = _r.scalars().first()
        return _d

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        # TODO(LiuTingwei): how to use core2.0
        # TODO(LiuTingwei): deleted field
        return await db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        _i = insert(self.model).values(**obj_in_data).returning(self.model)
        async with db() as _session:
            db_obj = await _session.execute(_i)
            _r = db_obj.scalars().first()
            await _session.flush(db_obj)
            await _session.commit()
        return _r

    # NOTE(LiuTingwei): test method
    async def create_many(
        self, db: Session, *, obj_in_lst: list[CreateSchemaType]
    ) -> ModelType:
        # TODO(LiuTingwei): obj_in_data, and how to insert many data for sqlalchemy
        obj_in_data = jsonable_encoder(obj_in_lst)
        _i = insert(self.model).values(obj_in_data)
        async with db() as _session:
            _r = await _session.execute(_i)
            await _session.flush()
            await _session.commit()
        # TODO(LiuTingwei): what's _r data?
        return _r

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        # TODO(LiuTingwei): new sqlalchemy core sql
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        async with db() as _session:
            _session.add(db_obj)
            await _session.commit()
            await _session.flush(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        # TODO(LiuTingwei): 灵活的查询结构方便remove
        obj = await db.query(self.model).get(id)
        obj_in = UpdateSchemaType(**{"deleted": True})
        return await self.update(db=db, db_obj=obj, obj_in=obj_in)
        # db.delete(obj)
        # db.commit()
        # return obj
