from sqlalchemy import true

import app.crud as crud
from app.tools.nike_name import get_random_nickname
from app.tools.snow_id import get_snow_id
from app.db.session import async_session
from app.schemas.users_extra import UsersCreate, UsersUpdate
from app.src.common import EMPTYDATA
from app.src.common.singleton import Singleton
from app.core.ecode import ErrorCode


class UsersService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.users

    async def get_user(self, user_id=None, user_uid=None, user_phone=None, user_name=None):
        user_data = None
        if user_id:
            user_data = await self.crud.get(self.db, id=user_id)
        if user_data is None and user_uid:
            user_data = await self.crud.get_by_uid(self.db, uid=user_uid)
        if user_data is None and user_phone:
            user_data = await self.crud.get_by_phone(self.db, phone=user_phone)
        if user_data is None and user_name:
            user_data = await self.crud.get_by_username(self.db, username=user_name)
        if user_data is None and user_uid and user_phone and user_name:
            user_data = await self.crud.get_user(self.db, username=user_name, uid=user_uid, phone=user_phone)
        if not user_data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, user_data

    async def get_users(self):
        user_data = await self.crud.get_users(self.db)
        if not user_data:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, user_data

    async def create(self, req: UsersCreate):
        user = await self.crud.get_by_username(self.db, username=req.username)
        if not user:
            req.nickname = get_random_nickname()
            req.uid = str(get_snow_id())
            user = await self.crud.create(self.db, obj_in=req)  # noqa: F841
            if user:
                return ErrorCode.SUCCESS, user.dict()
        return ErrorCode.NOT_EXIST, EMPTYDATA

    async def update(self, req: UsersUpdate):
        code, user = await self.get_user(user_uid=req.uid, user_phone=req.phone, user_name=req.username)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=user, obj_in=req)

    async def delete(self, id: int, uid: str, phone: str, username: str):
        code, user = await self.get_user(user_id=id, user_uid=uid, user_phone=phone, user_name=username)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=user, obj_in={"deleted": true()})
