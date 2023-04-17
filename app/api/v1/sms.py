#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Tuple

from fastapi import BackgroundTasks

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.settings.sms_country_code import AlphaCountryCode
from app.src.service.sms import (
    SendCodeItem,
    SendCodeResponse,
    SmsService,
    VerifyCodeItem,
    VerifyCodeResponse,
)
from app.tools.utils import testing_api

router = BaseRouter(tags=["sms"])
# Service
sms_srv = SmsService()


# TODO: https://fastapi.tiangolo.com/zh/tutorial/background-tasks/
# 也许可以使用celery进行短信的发送
@router.post(
    "/send_code", summary="发送短信验证码", response_model=Tuple[int, SendCodeResponse]
)
async def send_code(req: SendCodeItem, background_task: BackgroundTasks):
    """
    发送短信验证码
    验证码有效时间5分钟
    发送频率1次/分钟
    """
    phone = req.country_code + req.phone
    code = await sms_srv.verify_send(phone)
    if code == ErrorCode.SUCCESS:
        background_task.add_task(sms_srv.send_code, req)
        return ErrorCode.SUCCESS, SendCodeResponse(result=True)
    return code, SendCodeResponse(result=False)


@router.post(
    "/verify_code", summary="验证短信验证码", response_model=Tuple[int, VerifyCodeResponse]
)
async def verify_code(req: VerifyCodeItem):
    code, res = await sms_srv.verify_code(req)
    return code, res


@router.get("/country_code", summary="获取国家区号")
async def country_code():
    return ErrorCode.SUCCESS, AlphaCountryCode


@router.get("/get_verify_code", summary="测试阶段获取短信验证码")
@testing_api
async def get_verify_code(phone: str, country_code: str):
    req = SendCodeItem(phone=phone, country_code=country_code)
    res = await sms_srv.get_verify_code(req)
    return res
