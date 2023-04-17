#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import List

from fastapi import BackgroundTasks, Depends
from fastapi.param_functions import Query

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.service.user_group import UserGroup, Switch

router = BaseRouter(tags=["根据项目建群"])




@router.get("/forward", summary="消息转发开关")
async def get_forward_info(
    group_id: str = Query(..., title="群组ID"),
    token: str = Depends(WriteRequired()),
):
    srv = UserGroup()
    res = await srv.get_forward_info(group_id)
    return res


@router.post("/forward", summary="消息转发开关")
async def group_forward(
    group_id: str = Query(..., title="群组ID"),
    groups: List[str] = Query(..., title="群组列表"),
    token: str = Depends(WriteRequired()),
):
    srv = UserGroup()
    code, res = await srv.forward_message(Switch.ON, group_id, *groups)
    return code, res


@router.delete("/forward", summary="消息转发开关")
async def group_forward(
    group_id: str = Query(..., title="群组ID"),
    token: str = Depends(WriteRequired()),
):
    srv = UserGroup()
    code, res = await srv.forward_message(Switch.OFF, group_id)
    return code, res
