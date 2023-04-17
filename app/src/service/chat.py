#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.core.config import settings
from app.src.common.agoraio.rtc_token import Role_Subscriber, RtcTokenBuilder
from app.src.common.singleton import Singleton


class ChatService(Singleton):
    TOKEN_EXPIRATION_IN_SECONDS = 3600
    PRIVILEGE_EXPIRATION_IN_SECONDS = 3600

    @classmethod
    async def get_rtc_token(cls, channel_name, user_id):
        rtc_token = RtcTokenBuilder.build_token_with_uid(
            settings.AgoraIO_APPID,
            settings.AgoraIO_CERTIFICATE,
            channel_name,
            user_id,
            Role_Subscriber,
            cls.TOKEN_EXPIRATION_IN_SECONDS,
            cls.PRIVILEGE_EXPIRATION_IN_SECONDS,
        )
        return rtc_token
