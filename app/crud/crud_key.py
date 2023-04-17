#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, Optional, Union

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.keys import PrivateKeys
from app.schemas.keys import KeysCreate, KeysUpdate


class CRUDKeys(CRUDBase[PrivateKeys, KeysCreate, KeysUpdate]):
    async def get(
        self, db: Session, *, user_id: int
    ) -> Optional[PrivateKeys]:
        stmt = select(PrivateKeys).where(
            PrivateKeys.user_id == user_id
        )

        async with db() as _session:
            re = await _session.execute(stmt)
            key = re.scalars().all()
        return key

    async def get_with_account_address(
        self, db: Session, *, user_id: int, account_address: str
    ) -> Optional[PrivateKeys]:
        stmt = select(PrivateKeys).where(
            PrivateKeys.user_id == user_id,
            PrivateKeys.account_address == account_address,
        )
        async with db() as _session:
            re = await _session.execute(stmt)
            key = re.scalars().first()
        return key

    async def update(
        self,
        db: Session,
        *,
        db_obj: PrivateKeys,
        obj_in: Union[KeysUpdate, Dict[str, Any]]
    ) -> None:
        # db.query(PrivateKeys).filter(
        #     PrivateKeys.id == obj_in.id, PrivateKeys.user_id == obj_in.user_id
        # ).update({"account_name": obj_in.account_name})
        stmt = (
            update(PrivateKeys)
            .where(PrivateKeys.id == obj_in.id, PrivateKeys.user_id == obj_in.user_id)
            .values(account_name=obj_in.account_name)
        )
        async with db() as _session:
            await _session.execute(stmt)
            await _session.commit()

    async def remove(self, db: Session, *, id: int, user_id: int) -> None:
        stmt = delete(PrivateKeys).where(
            PrivateKeys.id == id,
            PrivateKeys.user_id == user_id,
        )
        async with db() as _session:
            await _session.execute(stmt)
            await _session.commit()
        return


keys = CRUDKeys(PrivateKeys)
