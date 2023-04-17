#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.verifications import Verifications
from app.schemas.verifications import VerificationsCreate, VerificationsUpdate


class CRUDVerifications(
    CRUDBase[Verifications, VerificationsCreate, VerificationsUpdate]
):
    async def get_by_chainid(
        self, db: AsyncSession, *, user_id: int, account_address: str, chain_id: int
    ) -> Optional[Verifications]:
        q = select(Verifications).where(
            Verifications.user_id == user_id,
            Verifications.account_address == account_address,
            Verifications.chain_id == chain_id,
        )
        async with db() as _session:
            _r = await _session.execute(q)
            re = _r.scalars().first()
        return re

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Verifications,
        obj_in: Union[VerificationsUpdate, Dict[str, Any]]
    ) -> Verifications:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super(CRUDVerifications, self).update(db, db_obj=db_obj, obj_in=update_data)


verifications = CRUDVerifications(Verifications)
