from typing import Any, Dict, Union

from sqlalchemy import select, false
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.groups import Group
from app.schemas.groups import GroupBase, GroupUpdate


class CRUDGroup(CRUDBase[Group, GroupBase, GroupUpdate]):

    async def get_by_id(self, db: Session, *, id: int):
        return await super(CRUDGroup, self).get(db=db, id=id)

    async def get_by_name(self, db: Session, *, name: str):
        q = select(Group).where(Group.name == name).where(Group.deleted == false())
        async with db() as _session:
            r = await _session.execute(q)
            group = r.scalars().first()
        return group

    async def create(self, db: Session, *, obj_in: GroupBase) -> Group:
        return await super(CRUDGroup, self).create(db=db, obj_in=obj_in)

    async def update(
            self, db: Session, *, db_obj: Group, obj_in: Union[GroupUpdate, Dict[str, Any]]
    ) -> Group:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super(CRUDGroup, self).update(db, db_obj=db_obj, obj_in=update_data)


groups = CRUDGroup(Group)
