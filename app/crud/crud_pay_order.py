#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.web_project import Web3PayOrder
from app.schemas.web_project import WebPayOrderCreate, WebPayOrderUpdate


class CRUDWeb3PayOrder(CRUDBase[Web3PayOrder, WebPayOrderCreate, WebPayOrderUpdate]):
    async def get_item_by_params(self, db: Session, params: dict):
        q = select(Web3PayOrder).filter_by(deleted=False).filter_by(**params)
        async with db() as _session:
            r = await _session.execute(q)
            obj = r.scalars().first()
        return obj

    async def get_items_by_params(self, db: Session, params: dict):
        q = select(Web3PayOrder).filter_by(deleted=False).filter_by(**params)
        async with db() as _session:
            r = await _session.execute(q)
            items = r.scalars().all()
        return items

    async def get_or_create(self, db: Session, params: WebPayOrderCreate):
        obj = await self.get_item_by_params(db, dict(params))
        if not obj:
            obj = await self.create(db, params)
        return obj

    async def create(self, db: Session, params: WebPayOrderCreate) -> Web3PayOrder:
        db_obj = Web3PayOrder(**dict(params))
        async with db() as _session:
            _session.add(db_obj)
            await _session.commit()
            await _session.flush(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Web3PayOrder,
        obj_in: Union[WebPayOrderUpdate, Dict[str, Any]]
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super(CRUDWeb3PayOrder, self).update(db, db_obj=db_obj, obj_in=update_data)


we3_pay_order = CRUDWeb3PayOrder(Web3PayOrder)
