#!/usr/bin/env python
# -*- coding:utf-8 -*-


from functools import partial
from typing import Callable

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute
from multipart.multipart import parse_options_header

from app.src.common.loggers import logger
from app.src.common.resp_base import JSONBaseResponse


class log_stuff(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req = await request.body()
            content_type_header = request.headers.get("Content-Type")
            content_type, _ = parse_options_header(content_type_header)
            if request.method == "POST":
                if content_type == b"multipart/form-data":
                    pass
                else:
                    logger.info(f"post_data: {req.decode()}")
            response: Response = await original_route_handler(request)
            logger.info(f"response_data: {response.body.decode()}")
            return response

        return custom_route_handler


BaseRouter = partial(
    APIRouter, default_response_class=JSONBaseResponse, route_class=log_stuff
)
