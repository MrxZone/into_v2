#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models.versions import Versions
from app.schemas.versions import VersionsCreate, VersionsUpdate


class CRUDVersions(CRUDBase[Versions, VersionsCreate, VersionsUpdate]):
    async def get_version(
        self,
        db: AsyncSession,
        *,
        version_code: int,  # app端正在使用的版本号
        release_channel: str,  # 发布渠道
        ecosystem: str  # 生态 Android or iPhone
    ) -> Optional[Versions]:
        q = (
            select(Versions)
            .where(Versions.new_version_code > version_code)
            .where(Versions.release_channel == release_channel)
            .where(Versions.ecosystem == ecosystem)
            .where(Versions.deleted == false())
            .order_by(desc(Versions.id))
        )
        async with db() as _session:
            _r = await _session.execute(q)
            re = _r.scalars().first()
        return re

    # async def update(
    #         self,
    #         db: AsyncSession,
    #         *,
    #         db_obj: Versions,
    #         obj_in: Union[VersionsUpdate, Dict[str, Any]]
    # ) -> Versions:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     return await super(CRUDVersions, self).update(db, db_obj=db_obj, obj_in=update_data)


versions = CRUDVersions(Versions)
