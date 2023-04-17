#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Request as __Request

from app.src.common.context import g

__all__ = ['RequestDataBase']


async def RequestDataBase(request: __Request):
    # Accept-Language: zh or en_us
    lang = request.headers.get("Accept-Language")
    if lang:
        g.locale = lang.split(",")[0]
    else:
        g.locale = "zh"

    # DeviceId: xxxxx-xxxx-xxx-xxxxxxx
    device_id = request.headers.get("X-DeviceId")
    if device_id:
        g.device_id = device_id
    else:
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     detail="Could not validate device id",
        # )
        g.device_id = ""

    # Token: JWT Token
    token = request.headers.get("X-Into-Token")
    if token:
        g.token = token
    else:
        g.token = ""

    # Platform: iSO or Android
    platform = request.headers.get("X-Platform")
    if platform:
        g.platform = platform
    else:
        g.platform = ""

    # Platform: 1.2.0
    app_version = request.headers.get("X-App-Versions")
    if app_version:
        g.app_version = app_version
    else:
        g.app_version = ""

    # Channel: google play or app store...
    app_channel = request.headers.get("X-App-Channel")
    if app_channel:
        g.app_channel = app_channel
    else:
        g.app_channel = ""
