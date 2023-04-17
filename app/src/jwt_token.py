#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
from typing import Dict, Optional

import jwt
from jwt.exceptions import DecodeError

from app.core.config import settings


async def generate_jwt(user: Dict) -> str:
    """
    生成JWT Token
    :param user:
    :return:
    """

    return jwt.encode(user, settings.SECRET_KEY, 'HS256')


async def decode_jwt(jwt_token: str) -> Optional[dict]:
    """
    解析JWT Token
    :param jwt_token:
    :return:
    """
    return jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])


async def verify(jwt_token) -> bool:
    """
    验证JWT Token
    :param jwt_token:
    :return: bool
    """
    try:
        jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return True
    except DecodeError:
        return False


if __name__ == '__main__':

    class User:
        def __init__(self, pk):
            self.user_id = pk
            self.user_name = "test"

    async def main():
        user1 = User(123)
        token = await generate_jwt(user1.__dict__)
        print(token)
        # tips: 目前token没有过期时间
        # time.sleep(60 * 60 * 2)

        # tips: test async 异步
        re = asyncio.sleep(2)
        info = await decode_jwt(token)
        print(info)
        await re
        print("end")

    asyncio.run(main())
