#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.core.ecode import ErrorCode
from app.db.redis_db import redis_cache
from app.src.common.enum import Enum, EnumMem
from app.src.common.singleton import Singleton
from app.src.service.define import KEY_FORWARD_MESSAGE


class Switch(Enum):
    """
    开关
    """

    ON = EnumMem("1", "ON")
    OFF = EnumMem("0", "OFF")


class UserGroup(Singleton):
    def __init__(self) -> None:
        self.redis_client = redis_cache.client

    async def get_admin_list(self):
        pass

    async def get_group_list(self, user_name: str):
        pass

    async def get_group_members(self, group_id: str):
        pass

    async def _limit_forward(self, groups):
        for i in groups:
            _key = KEY_FORWARD_MESSAGE.format(group_id=i)
            if await self.redis_client.exists(_key):
                return False
        return True

    async def get_forward_info(self, group_id: str):
        _key = KEY_FORWARD_MESSAGE.format(group_id=group_id)
        if not await self.redis_client.exists(_key):
            return {
                "groups": [],
                "count": 0,
                "status": Switch.desc(Switch.OFF)
            }

        _lst = await self.redis_client.smembers(_key)
        return {
            "groups": _lst,
            "count": len(_lst),
            "status": Switch.desc(Switch.ON)
        }

    async def forward_message(self, status, group_id, *groups):
        if not await self._limit_forward(groups):
            return ErrorCode.GROUP_FORWARD_ON, None

        if group_id in groups:
            return ErrorCode.GROUP_FORWARD_FAILED, None

        _key = KEY_FORWARD_MESSAGE.format(group_id=group_id)
        if status == Switch.ON:
            if await self.redis_client.exists(_key):
                return ErrorCode.GROUP_FORWARD_FAILED, None
            await self.redis_client.sadd(_key, *groups)
        elif status == Switch.OFF:
            await self.redis_client.delete(_key)
        return ErrorCode.SUCCESS, Switch.desc(status)
