#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.core.config import settings
from app.db.redis_db import redis_cache
from app.src.common.easemob.define import KEY_APP_TOKEN
from app.src.common.enum import Enum, EnumMem
from app.src.common.httper import AsyncHttper
from app.src.common.loggers import logger


class EasemobTokenManager(object):
    TRY_TIMES = 5

    def __init__(self) -> None:
        self.redis_client = redis_cache.client

    async def get_admin_token(self):
        for _ in range(self.TRY_TIMES):
            admin_token = await self.redis_client.get(KEY_APP_TOKEN)
            if not admin_token:
                try:
                    admin_token = await self.refresh_admin_token()
                    if admin_token:
                        return admin_token
                except Exception as e:
                    return ""
            else:
                return admin_token

    async def refresh_admin_token(self):
        admin_token = await EasemobAPI().get_admin_token()
        _token = admin_token.get("access_token", None)
        if not _token:
            return ""
        await self.redis_client.set(KEY_APP_TOKEN, _token)
        return _token


class EasemobAPI(AsyncHttper):
    raise_error = False

    def __init__(self):
        self.token = EasemobTokenManager()

    @staticmethod
    def _gen_url_base():
        return f"https://{settings.EASEMOB_HOST}/{settings.EASEMOB_ORGNAME}/{settings.EASEMOB_APPNAME}/"

    @classmethod
    async def _request(cls, url, method="get", **kwargs):
        logger.info(f"EasemobAPI Request: {url}, method: {method}, kwargs: {kwargs}")
        return await super()._request(url, method, **kwargs)

    async def get_admin_token(self):
        api_url = '{0}token'.format(self._gen_url_base())
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        __json = {
            "grant_type": "client_credentials",
            "client_id": settings.EASEMOB_CLIENTID,
            "client_secret": settings.EASEMOB_CLIENTSECRET,
        }
        return await self._request(api_url, "post", json=__json, headers=header)

    # todo: add token cache
    async def auto_create_user(self, username: str, app_token: str):
        api_url = '{0}token'.format(self._gen_url_base())
        __json = {"grant_type": "inherit", "username": username, "autoCreateUser": True}
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        # {
        #     'access_token': '*****',
        #     'expires_in': 933120000,
        #     'user': {
        #         'uuid': '******-****-****-****-***********',
        #         'type': 'user',
        #         'created': 1676268310262,
        #         'modified': 1676268310262,
        #         'username': 'abcd',
        #         'activated': True
        #     }
        # }

        return await self._request(api_url, "post", json=__json, headers=header)

    async def set_user_attr(self, username: str, app_token: str, **kwargs):
        api_url = '{0}metadata/user/{1}'.format(self._gen_url_base(), username)
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        return await self._request(api_url, "put", data=kwargs, headers=header)


class EasemobMessageType(Enum):
    TXT = EnumMem("txt", "文本消息")
    IMG = EnumMem("img", "图片消息")
    VOICE = EnumMem("voice", "语音消息")
    VIDEO = EnumMem("video", "视频消息")
    FILE = EnumMem("file", "文件消息")
    LOC = EnumMem("loc", "位置消息")
    CMD = EnumMem("cmd", "透传消息")
    CUSTOM = EnumMem("custom", "自定义消息")


class EasemobMessage(EasemobAPI):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.method = "get"

    async def get_header(self):
        app_token = await self.token.get_admin_token()
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        return header

    def get_params(self, from_user: str, to_user: list, msg_type: str, body: dict):
        _data = {
            "to": to_user,
            "type": msg_type,
            "body": body,
            "sync_device": True,
            # "routetype": "ROUTE_ONLINE",
            # "ext": "",  # json string,
            # "msg_timestamp": 0,
        }
        if from_user:
            _data["from"] = from_user
        return _data

    async def send_message(
        self, from_user: str, to_user: list, msg_type: str, body: dict
    ):
        header = await self.get_header()
        data = self.get_params(from_user, to_user, msg_type, body)
        return await self._request(self.url, self.method, json=data, headers=header)


class UserMessage(EasemobMessage):
    # todo: support multi sub class of message type
    def __init__(self):
        super().__init__()
        self.url = "{0}messages/users".format(self._gen_url_base())
        self.method = "post"

    async def send_txt(self, from_user, to_user, msg):
        return await self.send_message(
            from_user=from_user,
            to_user=[to_user],
            msg_type=EasemobMessageType.TXT,
            body={"msg": msg},
        )

    async def send_custom(self, from_user, to_user, event, **exts):
        return await self.send_message(
            from_user=from_user,
            to_user=[to_user],
            msg_type=EasemobMessageType.CUSTOM,
            body={"customEvent": event, "customExts": exts},
        )


class GroupMessage(EasemobMessage):
    def __init__(self):
        super().__init__()
        self.url = "{0}messages/chatgroups".format(self._gen_url_base())
        self.method = "post"

    async def send_txt(self, from_user, group_id, **body):
        return await self.send_message(
            from_user=from_user,
            to_user=group_id,
            msg_type=EasemobMessageType.TXT,
            body=body,
        )
