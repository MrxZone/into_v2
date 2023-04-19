from typing import Any, Dict, Optional, Union

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from app.crud.base import CRUDBase
from app.models.relations import Relation
from app.schemas.relations import RelationBase, RelationUpdate


class CRUDRelations(CRUDBase[Relation, RelationBase,RelationUpdate]):
    async def create(self, db: Session, *, obj_in: RelationBase):
        return await super(CRUDRelations, self).create(db=db, obj_in=obj_in)

    async def get(self, db: Session, *, owner_id: int):
        q = (
            select(Relation)
            .where(Relation.owner_id == owner_id)
            .where(Relation.deleted == false())
        )
        async with db() as _session:
            r = await _session.execute(q)
            relations = r.scalars().all()
        return relations

    async def search(self, db: Session, *, owner_id: int, another_id):
        q = (
            select(Relation)
            .where(Relation.owner_id == owner_id)
            .where(Relation.another_id == another_id)
            .where(Relation.deleted == false())
        )
        async with db() as _session:
            r = await _session.execute(q)
            relation = r.scalars().first()
        return relation

    async def update(
            self, db: Session, *, db_obj: Relation, obj_in: Union[RelationUpdate, Dict[str, Any]]
    ) -> Relation:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super(CRUDRelations, self).update(db, db_obj=db_obj, obj_in=update_data)


relation = CRUDRelations(Relation)
