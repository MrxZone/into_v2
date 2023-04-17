#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import traceback
import uuid

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import init_routers
from app.api.deps import RequestDataBase
from app.core.config import settings
from app.core.ecode import ErrorCode
from app.src.common.context import g
from app.src.common.loggers import logger
from app.src.common.resp_base import JSONBaseResponse

ROUTE_ROOT = '/api/v1'


def init_app(app):
    @app.exception_handler(Exception)
    async def exception_handler(req: Request, error: Exception):
        logger.error("%s Request Id: %s", traceback.format_exc(), g.request_id)
        # TODO(LiuTingwei): checkout this code
        return JSONBaseResponse((ErrorCode.INTER, g.request_id))

    @app.on_event("startup")
    async def startup():
        from app.db.redis_db import redis_cache

        redis_cache.init_cache()
        logger.info('startup')

    @app.on_event("shutdown")
    async def shutdown():
        from app.db.redis_db import redis_cache

        await redis_cache.close()
        logger.info('shutdown')


def setup_app(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        添加进程耗时
        """

        def format_request_logger_header(request):
            scope = request.scope
            server = f"{request.client.host}:{request.client.port}"
            method = scope.get("method")
            path = scope.get("path")
            #  http_type = f'{scope.get("type").upper()}/{scope.get("http_version")}'
            http_type = f'{scope.get("type").upper()}'
            #  logger_header = f'{server} - "{method} {path} {http_type}"'
            logger_header = f'"{method} {path}"'
            return logger_header

        start_time = time.time()
        logger_header = format_request_logger_header(request)
        g.request_id = str(uuid.uuid4())
        logger.info(f"{logger_header} Request Begin {g.request_id}")
        logger.info(f"{logger_header} query_params {request.query_params}")
        response = await call_next(request)
        # 计算运行时间
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-Id"] = g.request_id

        logger.info(
            f"{logger_header} Request {g.request_id} End time_used {process_time}"
        )
        return response


def create_app():
    app_config = {
        "title": "into",
        "docs_url": ROUTE_ROOT + '/docs',
        "redoc_url": ROUTE_ROOT + '/redoc',
        "openapi_url": ROUTE_ROOT + "/openapi.json",
        "dependencies": [Depends(RequestDataBase)],
    }
    if settings.ENVIRONMENT == "PRODUCTION":
        app_config.update(
            {
                "docs_url": None,
                "redoc_url": None,
                "openapi_url": None,
            }
        )
    app = FastAPI(**app_config)
    init_app(app)
    setup_app(app)
    init_routers(app)

    return app
