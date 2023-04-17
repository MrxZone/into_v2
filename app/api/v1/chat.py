#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Depends

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.jwt_token import decode_jwt
from app.src.service.chat import ChatService

router = BaseRouter(tags=["chat"])

# Service
user_srv = ChatService()


@router.get("/rtc_token", summary="音视频聊天token")
async def register(channel_name: str, token: int = Depends(WriteRequired())):
    user = await decode_jwt(token)
    user_id = user.get("user_id")
    if not user_id:
        return ErrorCode.TOKEN, None

    rtc_token = await user_srv.get_rtc_token(channel_name, user_id)
    res = {"accessToken": rtc_token, "agoraUserId": int(user_id)}
    return res
