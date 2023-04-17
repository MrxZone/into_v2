#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.faucet_bind import FaucetBind
from app.schemas.faucet_bind import FaucetBindCreate, FaucetBindBase


class CRUDFaucetBind(CRUDBase[FaucetBind, FaucetBindCreate, FaucetBindBase]):
    async def get(self, db: Session, *, user_name: str) -> Optional[FaucetBind]:
        stmt = select(FaucetBind).where(FaucetBind.user_name == user_name)

        async with db() as _session:
            re = await _session.execute(stmt)
            res = re.scalars().first()
        return res

    async def get_by_child_address(
        self, db: Session, *, child_address: str
    ) -> Optional[FaucetBind]:
        stmt = select(FaucetBind).where(
            FaucetBind.child_address == child_address,
        )
        async with db() as _session:
            re = await _session.execute(stmt)
            res = re.scalars().first()
        return res

    async def get_by_device_id(
        self, db: Session, *, device_id: str
    ) -> Optional[FaucetBind]:
        stmt = select(FaucetBind).where(
            FaucetBind.device_id == device_id,
        )
        async with db() as _session:
            re = await _session.execute(stmt)
            res = re.scalars().first()
        return res


faucet_bind = CRUDFaucetBind(FaucetBind)
