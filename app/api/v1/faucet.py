#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Depends, Header
from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.jwt_token import decode_jwt
from app.schemas import FaucetBindCreate
from app.src.service.users import UsersService
from app.src.service.into_faucet_contract import into_faucet_bind
from app.src.service.into_faucet import FaucetBindService

router = BaseRouter(tags=["faucet"])
user_srv = UsersService()
faucet_bind_srv = FaucetBindService()


@router.get("/faucet_bind", summary="水龙头绑定")
async def faucet_bind(
    parent_address: str,
    child_address: str,
    x_device_id: str = Header(...),
    token=(Depends(WriteRequired())),
):
    user = await decode_jwt(token)
    uid = user.get('user_id')
    user = await user_srv.get_user(uid)
    if not user:
        return ErrorCode.ACCOUNT, None
    # 校验
    # bind_by_name = await faucet_bind_srv.get(user_name=user.username)
    # bind_by_child = await faucet_bind_srv.get_by_child_address(child_address=child_address)
    # # bind_by_device = await faucet_bind_srv.get_by_device_id(device_id=x_device_id)
    # if bind_by_name or bind_by_child:
    #     return ErrorCode.HAVE_ALREADY_FAUCET_BIND_ERR, None
    res = into_faucet_bind.apply_async(
        args=[parent_address, child_address, user.username, x_device_id],
        queue='into_faucet',
        routing_key='app.faucet.bind',
    )

    req = FaucetBindCreate(
        user_name=user.username,
        parent_address=parent_address,
        child_address=child_address,
        device_id=x_device_id,
    )
    await faucet_bind_srv.create(req=req)

    return ErrorCode.SUCCESS, res.id
