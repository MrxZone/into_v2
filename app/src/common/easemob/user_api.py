#!/usr/bin/env python
# -*- coding: utf-8 -*-


from aiohttp.hdrs import METH_PUT, METH_GET, METH_DELETE

from app.src.common.easemob.api_client import EasemobAPI


class UserApi(EasemobAPI):
    def __int__(self):
        super().__init__()

    async def __user(self, username, method, **kwargs):
        __url = super()._gen_url_base() + "users/" + username
        return await self._request(__url, method, **kwargs)

    async def get_user_info(self, username: str, app_token: str):
        header = {
            "Accept": "application/json",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        return await self.__user(username, METH_GET, headers=header)

    async def set_user_attr(self, username: str, app_token: str, **kwargs):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        return await self.__user(username, METH_PUT, data=kwargs, headers=header)

    async def delete_user_attr(self, username: str, app_token: str):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {YourAppToken}".format(YourAppToken=app_token),
        }
        return await self.__user(username, METH_DELETE, headers=header)
