#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional
import app.crud as crud
import app.schemas as schemas
from app.db.session import async_session
from app.models.faucet_bind import FaucetBind
from app.src.common.singleton import Singleton


class FaucetBindService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()

    async def get(self, user_name: str) -> Optional[FaucetBind]:
        faucet_bind = await crud.faucet_bind.get(self.db, user_name=user_name)
        return faucet_bind

    async def get_by_child_address(self, child_address: str) -> Optional[FaucetBind]:
        faucet_bind = await crud.faucet_bind.get_by_child_address(
            self.db, child_address=child_address
        )
        return faucet_bind

    async def get_by_device_id(self, device_id: str) -> Optional[FaucetBind]:
        faucet_bind = await crud.faucet_bind.get_by_device_id(
            self.db, device_id=device_id
        )
        return faucet_bind

    async def create(self, req: schemas.FaucetBindCreate):
        faucet_bind = await crud.faucet_bind.create(self.db, obj_in=req)
        return faucet_bind
