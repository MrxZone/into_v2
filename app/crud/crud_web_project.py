#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.web_project import Web3Project

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDWeb3Project(CRUDBase[Web3Project, CreateSchemaType, UpdateSchemaType]):
    async def get_web_projects(self, db: Session):
        q = select(Web3Project).filter_by(deleted=False)
        async with db() as _session:
            r = await _session.execute(q)
            items = r.scalars().all()
        return items

    async def get_web_project(self, db: Session, id):
        q = select(Web3Project).filter_by(deleted=False, id=id)
        async with db() as _session:
            r = await _session.execute(q)
            obj = r.scalars().first()
        return obj


web3_project = CRUDWeb3Project(Web3Project)
