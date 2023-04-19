from sqlalchemy import true

import app.crud as crud
from app.core.ecode import ErrorCode
from app.db.session import async_session
from app.schemas.relations import RelationBase
from app.src.common import EMPTYDATA
from app.src.common.singleton import Singleton


class RelationService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.relation

    async def get_relations(self, owner_id: int):

        data = await self.crud.get(self.db, owner_id=owner_id)
        if not data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, data

    async def create(self, req: RelationBase):
        relation = await self.crud.search(self.db, owner_id=req.owner_id, another_id=req.another_id)
        if not relation:
            data = await self.crud.create(self.db, obj_in=req)  # noqa: F841
            if data:
                return ErrorCode.SUCCESS, data
        return ErrorCode.NOT_EXIST, EMPTYDATA

    async def update(self, req: RelationBase):
        relation = await self.crud.search(self.db, owner_id=req.owner_id, another_id=req.another_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=relation, obj_in=req)

    async def delete(self, owner_id: int, another_id: int):
        relation = await self.crud.search(self.db,owner_id=owner_id, another_id=another_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=relation, obj_in={"deleted": true()})
