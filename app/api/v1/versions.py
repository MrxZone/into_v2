#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import BackgroundTasks, Depends, File, Form, Header, UploadFile
from fastapi.encoders import jsonable_encoder

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.service.versions import VersionInfoItem, VersionsService
from app.tools.utils import testing_api

version_srv = VersionsService()
router = BaseRouter(tags=["versions"])


@router.get('/versions', summary="获取client端最新版本信息")
async def get_versions(
    version_code: int,
    release_channel: str,
    x_platform=Header(...),
    token=(Depends(WriteRequired())),
):
    version = await version_srv.get_version(version_code, release_channel, x_platform)
    return ErrorCode.SUCCESS, jsonable_encoder(version)


@router.post('/versions', summary="新增client端版本信息")
async def add_version(
    background_tasks: BackgroundTasks,
    version_name: str = Form(),
    version_code: int = Form(),
    new_version_name: str = Form(),
    new_version_code: int = Form(),
    release_channel: str = Form(),
    ecosystem: str = Form(),
    is_forced_updating: bool = Form(),
    change_log: str = Form(),
    file: UploadFile = File(...),
    token=(Depends(WriteRequired())),
):
    version_info = VersionInfoItem(
        version_name=version_name,
        version_code=version_code,
        new_version_name=new_version_name,
        new_version_code=new_version_code,
        release_channel=release_channel.lower(),
        ecosystem=ecosystem.lower(),
        is_forced_updating=is_forced_updating,
        change_log=change_log,
    )
    new_version = await version_srv.create_version(version_info, file)
    background_tasks.add_task(version_srv.del_version_file, new_version_name)
    return ErrorCode.SUCCESS, new_version


@router.put('/versions', summary="")
@testing_api
async def put_versions_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    token=(Depends(WriteRequired())),
):
    res = await version_srv.upload_file(file)
    background_tasks.add_task(version_srv.del_version_file, file.filename)
    return ErrorCode.SUCCESS, res


# @router.put('/versions', summary="修改client端版本信息")
# async def face_auth(token=(Depends(WriteRequired()))):
#     version = await srv.update_version()
#     return ErrorCode.SUCCESS, None
#
#
# @router.delete('/versions', summary="删除client端版本信息")
# async def face_auth(token=(Depends(WriteRequired()))):
#     version = await srv.delete_version()
#     return ErrorCode.SUCCESS, None


@router.get('/app_method', summary="")
async def app_switch(
    token=(Depends(WriteRequired())),
):
    res = {"group_message": True}
    return res
