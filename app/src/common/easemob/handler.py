#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import json
from typing import Callable

from app.core.config import settings
from app.db.redis_db import redis_cache
from app.src.common.easemob.api_client import UserMessage, GroupMessage
from app.src.service.define import KEY_FORWARD_MESSAGE
from app.tools.utils import get_app_name


class BaseHandler:
    def __init__(self, content_type: str, func: Callable = None, duplicates: bool = True) -> None:
        self.content_type = content_type
        self.func = func
        self.redis_client = redis_cache.client
        self.event = None
        self.duplicates = duplicates

    def set_event(self, event):
        self.event = event
        return self

    async def call_func(self, event):
        if self.duplicates and not await self.except_duplicates():
            return
        return await self.func(self, event)

    async def except_duplicates(self):
        if self.event.DUPLICATES_TIME == 0:
            return True
        # verify duplicates for payload
        _json_str = json.dumps(self.event.payload)
        pd = hashlib.md5(_json_str.encode("utf-8")).hexdigest()
        _key = f"easemob:{self.event.__class__.__name__}:{self.content_type}:duplicates:{pd}"

        if await self.redis_client.exists(_key):
            return False
        await self.redis_client.set(_key, 1, ex=self.event.DUPLICATES_TIME)
        return True


class Handler(BaseHandler):
    # class container
    pass


def handler(content_type: str, duplicates: bool = True):
    def decorator(func):
        return Handler(content_type=content_type, func=func, duplicates=duplicates)

    return decorator


# TODO(LiuTingwei): test code.
def app_flag():
    if settings.ENVIRONMENT == "PRODUCTION":
        return ""
    return get_app_name()


@handler(content_type="roster:accept")
async def roster_accept(__handler: BaseHandler, __event):
    message = UserMessage()
    await message.send_txt(
        from_user=__event.to_user,
        to_user=__event.from_user,
        msg=f"Hi Hello.{app_flag()}",
    )


@handler(content_type="muc:create")
async def muc_create(__handler, __event):
    if __event.is_group:
        group_message = GroupMessage()
        await group_message.send_txt(
            from_user=__event.from_user,
            group_id=__event.group_id,
            msg=f"Hello everyone.{app_flag()}",
        )


@handler(content_type="muc:presence")
async def muc_presence(__handler, __event):
    if __event.is_group:
        group_message = GroupMessage()
        await group_message.send_txt(
            from_user=None,
            group_id=__event.group_id,
            msg=f"您好，欢迎入群。",
        )


async def forward_group_msg(__handler, __event):
    _key = KEY_FORWARD_MESSAGE.format(group_id=__event.to_user)
    set_values = await __handler.redis_client.smembers(_key)
    if not set_values:
        return

    to_user_lst = list(set_values)
    _start = 0
    while True:
        _to = to_user_lst[_start: _start + 3]
        if not _to:
            break
        if await __handler.redis_client.exists(_key):
            if __event.is_group:
                group_message = GroupMessage()
                # TODO(LiuTingwei): 请求频率是否有限制？
                for _body in __event.payload["bodies"]:
                    await group_message.send_message(
                        from_user=settings.EASEMOB_ROBOT_1,
                        to_user=_to,
                        msg_type=_body["type"],
                        body=_body,
                    )
        await __handler.redis_client.expire(_key, 60 * 30)
        _start += 3


@handler(content_type="chat:group:text", duplicates=False)
async def chat_group_text(__handler, __event):
    await forward_group_msg(__handler, __event)


@handler(content_type="chat:group:image", duplicates=False)
async def chat_group_image(__handler, __event):
    await forward_group_msg(__handler, __event)


@handler(content_type="chat:group:voice", duplicates=False)
async def chat_group_voice(__handler, __event):
    await forward_group_msg(__handler, __event)


@handler(content_type="chat:group:video", duplicates=False)
async def chat_group_video(__handler, __event):
    await forward_group_msg(__handler, __event)


@handler(content_type="chat:group:file", duplicates=False)
async def chat_group_file(__handler, __event):
    await forward_group_msg(__handler, __event)

# {
#     "chat_type":"groupchat",
#     "callId":"1119230224168508#demo_1133442029800400488",
#     "security":"41284e482b9a4f435bb489341707f7ca",
#     "payload":{
#         "ext":{

#         },
#         "bodies":[
#             {
#                 "filename":"image702626411337670265.jpg",
#                 "size":{
#                     "width":614,
#                     "height":819
#                 },
#                 "file_length":13418,
#                 "secret":"DL6MOtqVEe2pp3uuYgYWtz7KYkrrQJRAtvJ_ZGmdRkpxA_4x",
#                 "thumbFilename":"86187100327761681456910319.jpg",
#                 "type":"img",
#                 "url":"https://a1.easemob.com/1119230224168508/demo/chatfiles/0cbe8c30-da95-11ed-88e0-3b28b5c70fce"
#             }
#         ],
#         "type":"groupchat"
#     },
#     "group_id":"211879431569422",
#     "host":"msync@ebs-ali-beijing-msync100",
#     "appkey":"1119230224168508#demo",
#     "from":"into.demo_robot",
#     "to":"8618710032776",
#     "eventType":"chat_offline",
#     "msg_id":"1133442029800400488",
#     "timestamp":1681464837445
# }
