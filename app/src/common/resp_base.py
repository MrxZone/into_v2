#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import typing

from fastapi.responses import Response
from starlette.background import BackgroundTask

from app.core.ecode import ErrorCode


class JSONBaseResponse(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        super(JSONBaseResponse, self).__init__(
            content, status_code, headers, media_type, background
        )

    def render(self, content: typing.Any) -> bytes:
        # TODO(LiuTingwei):
        # 传递code
        # 不传递code
        # 传递了但是不是int
        # 支持msg自定义
        if not isinstance(content, (list, tuple)) or len(content) < 2:
            code = ErrorCode.SUCCESS
            _data = content
        else:
            (code, *_data) = content
            if len(_data) == 1:
                _data = _data[0]

        if not isinstance(code, int):
            code = ErrorCode.SUCCESS
            _data = None

        _content = {
            "code": code,
            "msg": ErrorCode.dict().get(code, None),
            "data": _data,
        }
        return json.dumps(
            _content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
