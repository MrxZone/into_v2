#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import BackgroundTasks, Depends, File, UploadFile

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.jwt_token import decode_jwt
from app.src.service.users import RegisterItem, UsersService
from app.tools.utils import testing_api

router = BaseRouter(tags=["users"])

# Service
user_srv = UsersService()


# 配置工作目录及文件存储目录


@router.post("/register", summary="注册用户")
async def register(req: RegisterItem):
    code, res = await user_srv.register(req)
    if code != ErrorCode.SUCCESS:
        return code, None
    return res


@router.post("/upload_avatar", summary="上传头像")
async def upload_avatar(
    background_save_tasks: BackgroundTasks,
    files: UploadFile = File(...),
    token: str = Depends(WriteRequired()),
):
    user = await decode_jwt(token)
    user_name = user.get("user_name")
    cos_resource_url, file_name = await user_srv.set_user_avatar(user_name, files)
    background_save_tasks.add_task(user_srv.del_user_avatar, file_name)
    return cos_resource_url


@router.get("/username", summary="")
async def get_user_by_username(
    user_name: str,
    token: str = Depends(WriteRequired()),
):
    user_data = await user_srv.get_by_username(user_name)
    res = {"user_name": "", "user_id": 0}
    if user_data:
        res["user_name"] = user_data.username
        res["user_id"] = user_data.id
    return res


@router.get("/user", summary="")
async def get_user_by_username(
    uid: int,
    token: str = Depends(WriteRequired()),
):
    user_data = await user_srv.get_user(uid)
    res = {"user_name": ""}
    if user_data:
        res["user_name"] = user_data.username
    return res


@router.get("/user_info", summary="")
@testing_api
async def get_user_info(token: str = Depends(WriteRequired())):
    user = await decode_jwt(token)
    user_name = user.get("user_name")
    user_data = await user_srv.get_user_info(user_name)
    return user_data
