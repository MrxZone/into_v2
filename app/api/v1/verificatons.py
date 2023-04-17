#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.routes.route import BaseRouter
from app.schemas.verifications import VerificationsSchema
from app.src.common.auth_jwt import WriteRequired
from app.src.jwt_token import decode_jwt
from app.src.service.verificatons import VerificationsService

router = BaseRouter(tags=["verifications"])

# Service
srv = VerificationsService()


@router.post('/face_certify_id', summary="获取刷脸接口")
async def face_auth(face: VerificationsSchema, token=(Depends(WriteRequired()))):
    user = await decode_jwt(token)
    setattr(face, "user_id", user.get("user_id"))
    code, res = await srv.face_auth(**jsonable_encoder(face))
    return code, res


@router.get('/face_verify_result', summary="通过certify_id获取刷脸结果")
async def face_auth_result(
    certify_id: str,
    chain_id: int,
    account_address: str,
    paid_chain: str,
    token=(Depends(WriteRequired())),
):
    user = await decode_jwt(token)
    code, res = await srv.face_auth_result(
        user.get("user_id"), certify_id, chain_id, account_address, paid_chain
    )
    return code, res


@router.get('/twitter_verify', summary="twitter DID")
async def face_auth_result(
    oauth_token: str,
    oauth_token_secret: str,
    twitter_id: str,
    chain_id: int,
    account_address: str,
    paid_chain: str,
    token=(Depends(WriteRequired())),
):
    code, res = await srv.verified_by_twitter(
        oauth_token, oauth_token_secret, twitter_id, chain_id, account_address, paid_chain
    )
    return code, res


@router.get('/auth_result', summary="查询每条链是否认证 根据验证信息")
async def auth_result(chain_id: str, cert_name: str, cert_no: str):
    code, res = await srv.auth_result(chain_id, cert_name, cert_no)
    return code, res


@router.get('/auth_result_address', summary="查询每条链是否认证 根据账户地址")
async def auth_result_address(chain_id: str, account_address: str):
    code, res = await srv.auth_result_address(chain_id, account_address)
    return code, res


@router.get('/auth_result_twitter', summary="查询每条链是否认证 根据twitter_id")
async def auth_result_address(chain_id: str, twitter_id: str):
    code, res = await srv.auth_result_by_twitter(chain_id, twitter_id)
    return code, res


@router.get('/payment_message', summary="查询链对应地址的支付记录")
async def get_payment_message_api(chain_id: int, account_address: str):
    code, res = await srv.get_payment_message_api(chain_id, account_address)
    return code, res


@router.get('/set_face_auth_message_admin', summary="查询链对应地址的支付记录", dependencies=[Depends(WriteRequired())])
async def get_payment_message_api(chain_id: int, account_address: str, message: str):
    from app.src.service.contract import set_face_auth_message
    from app.core.ecode import ErrorCode
    res = set_face_auth_message.apply_async(
        args=[chain_id, account_address, message],
        queue='into_did',
        routing_key='app.verifications.did'
    )
    return ErrorCode.SUCCESS, res.id
