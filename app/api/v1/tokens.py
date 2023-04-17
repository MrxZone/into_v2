#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Depends

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.service.tokens import TokensService

router = BaseRouter(tags=["tokens"])

# Service
token_srv = TokensService()


@router.get("/token_transfer_history", summary="获取token交易历史 默认一页近最近一万条历史记录")
async def get(
    chain_id: str,
    contract_address: str,
    account_address: str,
    action: str,
    page: int = 1,
    offset: int = 10000,
    sort: str = "desc",
    token: str = Depends(WriteRequired()),
):
    text = await token_srv.get_transfer_history(
        chain_id,
        action=action,
        contract_address=contract_address,
        address=account_address,
        page=page,
        offset=offset,
        sort=sort,
    )

    if text['status'] != "1":
        return ErrorCode.INTER, None
    token_history = text['result']
    return ErrorCode.SUCCESS, token_history
