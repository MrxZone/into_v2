from sqlalchemy import select, false, insert, update, true
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.groups import GroupMembers
from app.schemas.groups import GroupMembersBase, GroupMembersUpdate


class CRUDGroupMembers(CRUDBase[GroupMembers, GroupMembersBase, GroupMembersUpdate]):

    async def get_members(self, db: Session, *, group_id: int):
        q = select(GroupMembers).where(GroupMembers.group_id == group_id).where(GroupMembers.deleted == false())
        async with db() as _session:
            r = await _session.execute(q)
            members = r.scalars().all()
        return members

    async def get_member(self, db: Session, *, obj_in: GroupMembersBase):
        q = select(GroupMembers).where(GroupMembers.group_id == obj_in.group_id).where(
            GroupMembers.deleted == false()).where(
            GroupMembers.user_id in [i.id for i in obj_in.users])
        async with db() as _session:
            r = await _session.execute(q)
            member = r.scalars().all()
        return member

    async def get(self, db: Session, *, group_id: int, user_id=int):
        q = select(GroupMembers).where(GroupMembers.group_id == group_id).where(
            GroupMembers.deleted == false()).where(
            GroupMembers.user_id == user_id)
        async with db() as _session:
            r = await _session.execute(q)
            member = r.scalars().first()
        return member

    async def create(self, db: Session, *, obj_in: GroupMembersBase) -> GroupMembers:
        q = insert(GroupMembers).values([{"group_id": obj_in.group_id,
                                          "user_id": members.id,
                                          "note": members.note
                                          } for members in obj_in.users])
        async with db() as _session:
            r = await _session.execute(q)
            await _session.flush()
            await _session.commit()
        return obj_in

    async def update_note(self, db: Session, *, obj_in: GroupMembersUpdate) -> GroupMembers:
        q = (
            update(GroupMembers).
            where(GroupMembers.group_id == obj_in.group_id).
            where(GroupMembers.user_id == obj_in.user_id).
            values(note=obj_in.note)
        )

        async with db() as _session:
            r = await _session.execute(q)
            await _session.commit()
            await _session.flush()
        return obj_in

    async def update_admin(self, db: Session, *, obj_in: GroupMembersUpdate) -> GroupMembers:
        q = update(GroupMembers).where(GroupMembers.group_id == obj_in.group_id).where(
            GroupMembers.user_id == obj_in.user_id).values(is_admin=obj_in.is_admin)

        async with db() as _session:
            r = await _session.execute(q)
            await _session.commit()
            await _session.flush()

        return obj_in

    async def delete(self, db: Session, *, group_id: int, user_id: int) -> GroupMembers:
        q = (
            update(GroupMembers).
            where(GroupMembers.group_id == group_id).
            where(GroupMembers.user_id == user_id).
            values(deleted=true())
        )

        async with db() as _session:
            r = await _session.execute(q)
            member = r.scalars().first()
        return member


group_members = CRUDGroupMembers(GroupMembers)
