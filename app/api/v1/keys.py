#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core.config import settings
from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.keys import KeysCreate, KeysDelete, KeysUpdate
from app.src.common.auth_jwt import WriteRequired
from app.src.jwt_token import decode_jwt
from app.src.service.keys import KeysService
from app.tools.AESText import aes

router = BaseRouter(tags=["私钥云备份"])

# Service
keys_srv = KeysService()


@router.get("/private_key", summary="获取加密后的私钥")
async def get(token: int = Depends(WriteRequired())):
    user = await decode_jwt(token)
    keys = await keys_srv.get(user_id=user.get("user_id"))

    for key in keys:
        private_key = key.private_key
        setattr(key, "private_key", aes.decrypt(settings.AES_KEY, private_key))
    return ErrorCode.SUCCESS, jsonable_encoder(keys)


@router.post("/private_key", summary="新增云备份私钥")
async def create(
    req: KeysCreate,
    token=Depends(WriteRequired()),
):
    user = await decode_jwt(token)
    req.user_id = user.get("user_id")
    # 重复判断
    key = await keys_srv.get_by_account_address(user_id=req.user_id, account_address=req.account_address)
    if key:
        return ErrorCode.DUPLICATE_BACKUP_ERR, None

    req.private_key = aes.encrypt(key=settings.AES_KEY, content=req.private_key)
    keys_res = await keys_srv.create(req)
    return ErrorCode.SUCCESS, jsonable_encoder(keys_res)


@router.put("/private_key", summary="修改钱包名称")
async def update(req: KeysUpdate, token=Depends(WriteRequired())):
    user = await decode_jwt(token)
    setattr(req, "user_id", user.get("user_id"))
    await keys_srv.update(req)
    return ErrorCode.SUCCESS, None


@router.delete("/private_key", summary="删除私钥")
async def remove(req: KeysDelete, token=Depends(WriteRequired())):
    user = await decode_jwt(token)
    setattr(req, "user_id", user.get("user_id"))
    await keys_srv.remove(req)
    return ErrorCode.SUCCESS, None
