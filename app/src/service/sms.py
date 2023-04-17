#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import random
import string
from typing import Union
from uuid import uuid4

from fastapi import Query
from pydantic import BaseModel, Field

from app.core.ecode import ErrorCode
from app.db.redis_db import redis_cache
from app.src.common.loggers import logger
from app.src.common.singleton import Singleton
from app.src.common.sms import sms_manager
from app.src.jwt_token import generate_jwt
from app.src.service.define import (
    KEY_SMS_CODE,
    KEY_SMS_SENDED,
    KEY_SMS_TOTAL,
    KEY_SMS_VERIFY_ID,
    KEY_SMS_VERIFY_LIMIT,
)
from app.src.service.users import UsersService


class SendCodeItem(BaseModel):
    phone: str = Field(description="手机号")
    country_code: str = Field(description="国家区号")


class VerifyCodeItem(SendCodeItem):
    # code: str = Field(description="短信验证码")
    code: str = Query(min_length=6, max_length=6, description="短信验证码")


class VerifyCodeResponse(BaseModel):
    verify_id: Union[str, None] = Field(description="注册用户验证ID")
    token: Union[str, None] = Field(description="环信用户token")
    user_name: Union[str, None] = Field(description="环信用户名")
    is_new_user: Union[bool, None] = Field(description="是否新用户")
    into_token: Union[str, None] = Field(description="into_token")


class SendCodeResponse(BaseModel):
    result: bool = Field(description="result")


class SmsService(Singleton):
    CODE_MAP = string.digits

    def __init__(self) -> None:
        self.redis_client = redis_cache.client
        self.expire = 60 * 5
        self.code_length = 6
        self.user_svc = UsersService()

    async def gen_code(self):
        _code = "".join(random.sample(self.CODE_MAP, self.code_length))
        return _code

    async def verify_send(self, phone: str):
        send_lock = await self.redis_client.get(KEY_SMS_SENDED.format(phone=phone))
        if send_lock:
            return ErrorCode.TOO_FREQUENT

        _count = await self.redis_client.get(KEY_SMS_VERIFY_LIMIT.format(phone=phone))
        if _count and int(_count) >= 5:
            return ErrorCode.SMS_VERIFY_LIMIT

        return ErrorCode.SUCCESS

    async def send_code(self, req: SendCodeItem):
        """
        发送短信验证码
        """
        res = SendCodeResponse(result=False)
        phone = req.country_code + req.phone

        code = await self.verify_send(phone)
        if code != ErrorCode.SUCCESS:
            return code, res

        sms_code = await self.gen_code()
        sms_rsp = await sms_manager.send_sms(req.country_code, req.phone, sms_code)
        if int(sms_rsp) > 0:
            # 短信验证码有效期5分钟
            # total count
            if req.country_code == "86":
                await self.redis_client.incr(KEY_SMS_TOTAL.format(region="mainland"))
            else:
                await self.redis_client.incr(KEY_SMS_TOTAL.format(region="global"))
            # TODO: lock key and redis locker
            await self.redis_client.set(
                KEY_SMS_CODE.format(phone=phone), sms_code, ex=self.expire
            )
            # 60s发送一次短信
            await self.redis_client.set(KEY_SMS_SENDED.format(phone=phone), 1, ex=60)
            res.result = True
        return ErrorCode.SUCCESS, res

    async def verify_code(self, req: VerifyCodeItem):
        phone = req.country_code + req.phone
        res_data = VerifyCodeResponse()
        verify_code = await self.redis_client.get(KEY_SMS_CODE.format(phone=phone))
        if not verify_code:
            return ErrorCode.SMS_TIMEOUT_ERR, res_data
        if verify_code != req.code:
            _key = KEY_SMS_VERIFY_LIMIT.format(phone=phone)
            _count = await self.redis_client.incr(_key)
            if _count >= 5:
                return ErrorCode.SMS_VERIFY_LIMIT, res_data
            else:
                await self.redis_client.expire(_key, self.expire)
            return ErrorCode.SMS_CODE_ERR, res_data

        user_data = await self.user_svc.get_by_phone(phone)
        if user_data:
            starttime = datetime.datetime.now()
            code, access_token = await self.user_svc.auto_create_user(
                user_data.username
            )
            endtime = datetime.datetime.now()
            logger.info(f"@@@@:auto_create_user time: {(endtime - starttime).seconds}")
            if code != ErrorCode.SUCCESS:
                return code, res_data

            into_token = await generate_jwt(
                {"user_id": user_data.id, "user_name": user_data.username}
            )
            _rsp_data = {
                "verify_id": "",
                "token": access_token["access_token"],
                "is_new_user": False,
                "into_token": into_token,
                "user_name": user_data.username,
            }
        else:
            verify_id = str(uuid4())
            await self.redis_client.set(
                KEY_SMS_VERIFY_ID.format(uuid=verify_id), phone, ex=self.expire
            )
            _rsp_data = {
                "verify_id": verify_id,
                "token": "",
                "is_new_user": True,
                "into_token": "",
                "user_name": "",
            }
        await self.redis_client.delete(KEY_SMS_CODE.format(phone=phone))
        return ErrorCode.SUCCESS, res_data.parse_obj(_rsp_data)

    async def get_verify_code(self, req: SendCodeItem):
        phone = req.country_code + req.phone
        verify_code = await self.redis_client.get(KEY_SMS_CODE.format(phone=phone))
        res = {"code": verify_code or ""}
        return res
