#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import string

from pydantic import BaseModel, Field

import app.crud as crud
import app.schemas as schemas
from app.core.config import AVATAR_PATH
from app.core.ecode import ErrorCode
from app.db.redis_db import redis_cache
from app.db.session import async_session
from app.src.common import EMPTYDATA
from app.src.common.easemob.api_client import EasemobAPI
from app.src.common.easemob.api_client import EasemobTokenManager
from app.src.common.qcloud.cos import upload_file
from app.src.common.singleton import Singleton
from app.src.jwt_token import generate_jwt
from app.src.service.define import KEY_SMS_VERIFY_ID
from app.tools.utils import del_file, save_file
from app.src.common.easemob.api_client import UserMessage


class RegisterItem(BaseModel):
    username: str = Field(description="用户名(环信使用)", default=None, deprecated=True)
    verify_id: str = Field(description="验证短信验证码返回的验证ID")
    phone: str = Field(description="手机号")
    country_code: str = Field(description="国家区号")


class UsersService(Singleton):
    def __init__(self) -> None:
        self._api = EasemobAPI()
        self.db = async_session.init()
        self.token = EasemobTokenManager()
        self.redis_client = redis_cache.client
        self.crud = crud.users
        self.user_msg = UserMessage()

    async def auto_create_user(self, user_name):
        app_token = await self.token.get_admin_token()
        if not app_token:
            return ErrorCode.TOKEN, EMPTYDATA

        # TODO(LiuTingwei): 并发问题。有可能多个请求同时去申请新的token，会浪费出口
        retry_times = 5
        while retry_times > 0:
            rsp_user_data = await self._api.auto_create_user(user_name, app_token)
            # TODO(LiuTingwei): 验证逻辑待完善
            if "error" in rsp_user_data:
                await self.token.refresh_admin_token()
                retry_times -= 1
            else:
                break
        return ErrorCode.SUCCESS, rsp_user_data or EMPTYDATA

    def get_random_nickname(self):
        __name = "".join(random.sample(string.ascii_letters, 6))
        return __name + "@Into"

    async def set_user_nickname(self, user_name: str, nickname: str):
        app_token = await self.token.get_admin_token()
        if not app_token:
            return ErrorCode.TOKEN, EMPTYDATA

        rsp_user_data = await self._api.set_user_attr(
            user_name, app_token, nickname=nickname
        )
        if "error" in rsp_user_data:
            return ErrorCode.TOKEN, EMPTYDATA
        return ErrorCode.SUCCESS, rsp_user_data

    async def register(self, req: RegisterItem):
        # TODO:
        verify_phone = await self.redis_client.get(
            KEY_SMS_VERIFY_ID.format(uuid=req.verify_id)
        )
        if not verify_phone:
            return ErrorCode.ACCOUNT, EMPTYDATA

        phone = req.country_code + req.phone
        if verify_phone != phone:
            return ErrorCode.ACCOUNT, EMPTYDATA

        # NOTE(LiuTingwei): 环信用户名暂定与手机号一致(产品短期需求)
        req.username = phone

        code, rsp_user_data = await self.auto_create_user(req.username)
        if code != ErrorCode.SUCCESS:
            return code, EMPTYDATA
        nickname = self.get_random_nickname()
        await self.set_user_nickname(req.username, nickname)
        user = await self.crud.get_by_username(self.db, username=req.username)
        if not user:
            user_in = schemas.UsersCreate(username=req.username, phone=verify_phone)
            user = await self.crud.create(self.db, obj_in=user_in)  # noqa: F841
            if user:
                await self.send_user_register_msg(user.username)
        await self.redis_client.delete(KEY_SMS_VERIFY_ID.format(uuid=req.verify_id))
        into_token = await generate_jwt(
            {"user_id": user.id, "user_name": user.username}
        )

        return ErrorCode.SUCCESS, {
            "token": rsp_user_data["access_token"],
            "into_token": into_token,
            "user_name": user.username,
        }

    async def set_user_avatar(self, user_name, avatar):
        file_type = "." + avatar.filename.split(".")[-1]
        local_file_path, file_name = await save_file(
            file=avatar,
            facker_filename=user_name,
            file_type=file_type,
            path=AVATAR_PATH,
        )
        cos_resource_url = upload_file(local_file_path, file_name)
        return cos_resource_url, file_name

    async def del_user_avatar(self, file_name):
        await del_file(file_name, "", AVATAR_PATH)

    async def get_by_phone(self, phone):
        user_data = await self.crud.get_by_phone(self.db, phone=phone)
        return user_data

    async def get_by_username(self, user_name):
        user_data = await self.crud.get_by_username(self.db, username=user_name)
        return user_data

    async def get_user(self, user_id):
        user_data = await self.crud.get(self.db, id=user_id)
        return user_data

    async def send_user_register_msg(self, to_user):
        r = await self.user_msg.send_custom(
            from_user="em_system",
            to_user=to_user,
            event="user_register",
            content="歡迎您來到全新的社交世界，與INTO一起遨游web3領域的每一個角落。https://www.baidu.com/",
        )
        return r
