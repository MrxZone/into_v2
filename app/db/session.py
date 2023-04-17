#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


class AsyncDatabaseSession:
    @classmethod
    def init(cls):
        engine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI, echo=True, pool_size=10, max_overflow=30
        )
        session = async_scoped_session(
            async_sessionmaker(engine, future=True, expire_on_commit=False),
            scopefunc=asyncio.current_task,
        )
        return session


async_session = AsyncDatabaseSession
