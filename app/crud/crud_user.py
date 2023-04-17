#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, Optional, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UsersCreate, UsersUpdate


class CRUDUser(CRUDBase[Users, UsersCreate, UsersUpdate]):
    async def get_by_phone(self, db: Session, *, phone: str) -> Optional[Users]:
        q = select(Users).where(Users.phone == phone).where(Users.deleted == false())
        async with db() as _session:
            r = await _session.execute(q)
            user = r.scalars().first()
        return user

    async def get_by_username(self, db: Session, *, username: str) -> Optional[Users]:
        q = (
            select(Users)
            .where(Users.username == username)
            .where(Users.deleted == false())
        )
        async with db() as _session:
            r = await _session.execute(q)
            user = r.scalars().first()
        return user

    async def create(self, db: Session, *, obj_in: UsersCreate) -> Users:
        db_obj = Users(username=obj_in.username, phone=obj_in.phone)
        return await super(CRUDUser, self).create(db=db, obj_in=db_obj)

    async def update(
        self, db: Session, *, db_obj: Users, obj_in: Union[UsersUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super(CRUDUser, self).update(db, db_obj=db_obj, obj_in=update_data)


users = CRUDUser(Users)
