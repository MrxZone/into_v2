#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
from collections import defaultdict

from app.db.redis_db import redis_cache
from app.src.common.easemob.handler import Handler
from app.src.common.loggers import logger


class BaseEvent:
    DUPLICATES_TIME = 3

    def __parse_data(self):
        self.chat_type = self.data.get("chat_type")
        self.event_type = self.data.get("eventType")
        self.content_type = self.data.get("content_type")
        if not self.content_type and isinstance(self, ChatEvent):
            raise ValueError("no content_type")

        if self.data.get("group_id", None):
            self.is_group = True
            self.group_id = self.data.get("group_id")

    def __init__(self, data):
        self.data = data
        self.event_type = None
        self.chat_type = None
        self.secret = None
        self.is_group = False
        self.group_id = None
        self.content_type = None
        self.redis_client = redis_cache.client
        self._chat_handler = defaultdict(dict)
        self.__parse_data()

    def set_secret(self, secret):
        self.secret = secret
        return self

    def register(self, handler: Handler):  # maybe should be a function
        if self._chat_handler[self.event_type].get(handler.content_type, None):
            raise Exception("handler already exist")
        self._chat_handler[self.event_type][handler.content_type] = handler.set_event(
            self
        )

    def get_chat_handle(self) -> Handler:
        return self._chat_handler.get(self.event_type, {}).get(self.content_type, None)

    async def call_func(self):
        if not self.verify_security():
            # todo: log
            return
        if not await self.duplicates_callback():
            # todo: log
            return
        handler = self.get_chat_handle()
        if handler:
            return await handler.call_func(self)
        else:
            logger.error("No Handler........")

    @property
    def from_user(self):
        _from: str = self.data.get("from", "")
        try:
            _from_user = _from.split("#")[1].split("@")[0].split("_")[1]
        except IndexError:
            _from_user = _from
        return _from_user

    @property
    def to_user(self):
        return self.data.get("to")

    @property
    def payload(self):
        return self.data.get("payload", {})

    @property
    def security(self):
        return self.data.get("security")

    @property
    def call_id(self):
        return self.data.get("callId")

    @property
    def timestamp(self):
        return self.data.get("timestamp")

    def verify_security(self):
        f = f"{self.call_id}{self.secret}{self.timestamp}"
        pwd_dig = hashlib.md5(f.encode()).hexdigest()
        return pwd_dig == self.security

    async def duplicates_callback(self):
        if self.DUPLICATES_TIME == 0:
            return True
        _key = "easemob:%s:call_id:%s" % (self.__class__.__name__, self.call_id)
        if await self.redis_client.exists(_key):
            return False
        await self.redis_client.set(_key, 1, ex=self.DUPLICATES_TIME)
        return True


class ChatEvent(BaseEvent):
    # class container
    pass


class ChatOfflineEvent(BaseEvent):
    # class container
    async def call_func(self):
        return


def factory(body):
    event_type = body.get("eventType")
    if event_type == "chat":
        return ChatEvent(body)
    elif event_type == "chat_offline":
        return ChatOfflineEvent(body)
    else:
        raise ValueError("Invalid event type: {}".format(event_type))
