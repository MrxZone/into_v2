from sqlalchemy import true

import app.crud as crud
from app.core.ecode import ErrorCode
from app.db.session import async_session
from app.schemas.groups import GroupBase, GroupUpdate, GroupMembersBase, Users, GroupMembersUpdate, GroupCreate
from app.src.common import EMPTYDATA
from app.src.common.singleton import Singleton


class GroupService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.groups
        self.group_members = crud.group_members

    async def get_group(self, id: int):

        data = await self.crud.get(self.db, id=id)
        if not data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, data

    async def create(self, req: GroupCreate):
        group = await self.crud.get_by_name(self.db, name=req.name)
        if not group:
            obj_in = GroupBase(name=req.name, note=req.note)
            data = await self.crud.create(self.db, obj_in=obj_in)
            member = GroupMembersBase(group_id=data.id, users=[Users(id=req.user_id)])
            await self.group_members.create(self.db, obj_in=member)
            obj_in = GroupMembersUpdate(group_id=data.id, user_id=req.user_id, is_admin=true())
            self.group_members.update_admin(self.db, obj_in=obj_in)  # noqa: F841
            if data:
                return ErrorCode.SUCCESS, data
        return ErrorCode.NOT_EXIST, EMPTYDATA

    async def update(self, req: GroupUpdate):
        code, group = await self.get_group(id=req.id)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=group, obj_in=req)

    async def delete(self, id: int):
        group = await self.crud.get(id=id)
        if not group:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=group, obj_in={"deleted": true()})
