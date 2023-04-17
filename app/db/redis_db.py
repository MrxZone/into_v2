#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

import aioredis

from app.core.config import settings


class RedisCache:
    MAX_CONNECTIONS = 10

    def __init__(self) -> None:
        self.redis_cache: Optional[aioredis.Redis] = None

    def init_cache(self):
        __pool = aioredis.ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf-8",
            max_connections=self.MAX_CONNECTIONS,
        )
        self.redis_cache = aioredis.Redis(connection_pool=__pool)

    @property
    def client(self):
        if not self.redis_cache:
            self.init_cache()
        return self.redis_cache

    async def close(self):
        await self.redis_cache.close()

    # TODO(LiuTingwei): locker


redis_cache = RedisCache()
