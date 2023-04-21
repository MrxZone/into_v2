from typing import Any, Dict, Optional, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models.relations import RelationJson
from app.schemas.relations import RelationJSONBase


class CRUDRelationsJSON(CRUDBase[RelationJson, RelationJSONBase, RelationJSONBase]):
    async def get(self, db: Session, *, user_id: int) -> RelationJson:
        q = (
            select(RelationJson).where(RelationJson.user_id == user_id).where(RelationJson.deleted == false())
        )
        async with db() as _session:
            r = await _session.execute(q)
            relation = r.scalars().first()
        return relation

    async def create(self, db: Session, *, obj_in: RelationJSONBase) -> RelationJson:
        return await super(CRUDRelationsJSON, self).create(db=db, obj_in=obj_in)


relation_json = CRUDRelationsJSON(RelationJson)
