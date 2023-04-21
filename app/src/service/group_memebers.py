from sqlalchemy import true

import app.crud as crud
from app.core.ecode import ErrorCode
from app.db.session import async_session
from app.schemas.groups import GroupMembersBase, GroupMembersUpdate
from app.src.common import EMPTYDATA
from app.src.common.singleton import Singleton


class GroupMembersService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.group_members

    async def get(self, group_id: int):

        data = await self.crud.get_members(self.db, group_id=group_id)
        if not data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, data

    async def search(self, group_id: int, user_id=int):

        data = await self.crud.get_members(self.db, group_id=group_id)
        if not data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, data

    async def create(self, req: GroupMembersBase):
        members = await self.crud.get_member(self.db, obj_in=req)
        if not members:
            data = await self.crud.create(self.db, obj_in=req)  # noqa: F841
            if data:
                return ErrorCode.SUCCESS, data
        return ErrorCode.NOT_EXIST, EMPTYDATA

    async def update_note(self, req: GroupMembersUpdate):
        code, members = await self.get(group_id=req.group_id)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update_note(self.db, obj_in=req)

    async def update_admin(self, req: GroupMembersUpdate):
        code, members = await self.get(group_id=req.group_id)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update_admin(self.db, obj_in=req)

    async def delete(self, group_id: int, user_id: int):
        members = await self.crud.get(self.db, group_id=group_id, user_id=user_id)
        if not members:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=members, obj_in={"deleted": true()})
