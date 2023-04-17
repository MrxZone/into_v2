#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

import app.crud as crud
import app.schemas as schemas
from app.db.session import async_session
from app.models.keys import PrivateKeys
from app.src.common.singleton import Singleton


class KeysService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()

    async def get(self, user_id: int) -> Optional[PrivateKeys]:
        keys = await crud.keys.get(self.db, user_id=user_id)
        return keys

    async def get_by_account_address(self, user_id: int, account_address: str) -> Optional[PrivateKeys]:
        keys = await crud.keys.get_with_account_address(self.db, user_id=user_id, account_address=account_address)
        return keys


    async def create(self, req: schemas.KeysCreate):
        _schemas = schemas.KeysCreate(
            user_id=req.user_id,
            account_address=req.account_address,
            private_key=req.private_key,
            account_name=req.account_name,
        )
        user = await crud.keys.create(self.db, obj_in=_schemas)  # noqa: F841
        return user

    async def update(self, req: schemas.KeysUpdate):
        user = await crud.keys.update(
            self.db, db_obj=PrivateKeys, obj_in=req
        )  # noqa: F841
        return user

    async def remove(self, req: schemas.KeysDeleteWithUser):
        key = await crud.keys.remove(
            self.db, id=req.id, user_id=req.user_id
        )  # noqa: F841
        return key
