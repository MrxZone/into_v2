#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib

import web3

import app.crud as crud
from app.core.config import settings
from app.core.ecode import ErrorCode
from app.db.session import async_session
from app.models.verifications import Verifications
from app.schemas.verifications import VerificationsCreate, VerificationsUpdate
from app.src.common.ali_face_verify import DescribeFaceVerify, InitFaceVerify
from app.src.common.singleton import Singleton
from app.tools.identity.identity import IdNumber
from app.src.service.twitter import auth_twitter_token

from .contract import (face_auth_address, get_face_auth_message,
                       get_payment_message, set_face_auth_message)


class VerificationsService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.verifications

    def _gen_message(self, *, cert_name: str, cert_no: str):
        _message = cert_name + " " + cert_no
        message = str(hashlib.sha256(_message.encode('utf-8')).hexdigest())
        return message

    def enciphered_data_twitter(self, twitter_id):
        data = "into" + str(twitter_id)
        return str(hashlib.sha256(data.encode('utf-8')).hexdigest())

    async def face_auth(
        self,
        user_id: int,
        chain_id: int,
        account_address: str,
        cert_name: str,
        cert_no: str,
        meta_info: str,
        return_url: str,
    ):
        if not IdNumber.verify_id(cert_no):
            return ErrorCode.IDENTIFY_ERR, None
        if not web3.Web3.is_address(account_address):
            return ErrorCode.VERIFY_ACCOUNT_ADDRESS_ERR, None

        re = await self.crud.get_by_chainid(
            self.db, user_id=user_id, account_address=account_address, chain_id=chain_id
        )

        message = self._gen_message(cert_name=cert_name, cert_no=cert_no)
        if not re:
            face_message = VerificationsCreate(
                user_id=user_id,
                account_address=account_address,
                chain_id=chain_id,
                message=message,
            )
            await self.crud.create(self.db, obj_in=face_message)
        else:
            stmt = VerificationsUpdate(
                user_id=user_id,
                chain_id=chain_id,
                account_address=account_address,
                message=message,
            )
            await self.crud.update(self.db, db_obj=re, obj_in=stmt)

        if await get_payment_message(chain_id, account_address):
            certify_id = InitFaceVerify.main(
                cert_name=cert_name,
                cert_no=cert_no,
                meta_info=meta_info,
                return_url=return_url,
            )
        else:
            return ErrorCode.NON_PAYMENT_ERR, None
        return ErrorCode.SUCCESS, certify_id

    async def face_auth_result(
        self, user_id, certify_id, chain_id, account_address, paid_chain
    ):
        ali_face_auth_result = DescribeFaceVerify.main(certify_id)

        verification = await self.crud.get_by_chainid(
            self.db, user_id=user_id, account_address=account_address, chain_id=chain_id
        )

        if not verification:
            return ErrorCode.VERIFICATION_MESSAGE_ERR, None
        message = verification.message

        # 刷脸是否通过
        if ali_face_auth_result['passed'] == 'T':
            payment_message = await get_payment_message(chain_id, account_address)
            payment_id = [int(payment.get("chainId")) for payment in payment_message]

            for i in paid_chain.split(','):
                if int(i) not in payment_id:
                    return ErrorCode.UNPAID_CHAIN_ERR, None
            ali_face_auth_result["celery_task"] = []
            for chain_id in paid_chain.split(','):
                chain_id = int(chain_id)
                if chain_id in payment_id:
                    # res = set_face_auth_message.delay(
                    #     chain_id, account_address, message
                    # )
                    res = set_face_auth_message.apply_async(
                        args=[chain_id, account_address, message],
                        queue='into_did',
                        routing_key='app.verifications.did'
                    )

                    ali_face_auth_result["celery_task"].append({"chain_id": chain_id, "task_id": res.id})
        return ErrorCode.SUCCESS, ali_face_auth_result

    async def verified_by_twitter(
        self,
        oauth_token: str,
        oauth_token_secret: str,
        twitter_id: str,
        chain_id: int,
        account_address: str,
        paid_chain: str
    ):
        re = {}
        # 验证twitter
        twitter_result, twitter_id = auth_twitter_token(twitter_id, oauth_token, oauth_token_secret)
        msg = self.enciphered_data_twitter(twitter_id)
        if twitter_result:
            payment_message = await get_payment_message(
                chain_id, account_address
            )
            payment_id = [int(payment.get("chainId")) for payment in payment_message]

            for i in paid_chain.split(','):
                if int(i) not in payment_id:
                    return ErrorCode.UNPAID_CHAIN_ERR, None
            re["celery_task"] = []
            for chain_id in paid_chain.split(','):
                chain_id = int(chain_id)
                if chain_id in payment_id:
                    # res = set_face_auth_message.delay(
                    #     chain_id, account_address, msg
                    # )
                    res = set_face_auth_message.apply_async(
                        args=[chain_id, account_address, msg],
                        queue='into_did',
                        routing_key='app.verifications.did'
                    )
                    re["celery_task"].append({"chain_id": chain_id, "task_id": res.id})
            return ErrorCode.SUCCESS, re
        return ErrorCode.TWITTER_OAUTH_AUTHORIZATION_ERR, None

    async def auth_result(self, chain_id, cert_name, cert_no):
        """
        查询每条链是否认证 根据验证信息
        """
        message = self._gen_message(cert_name=cert_name, cert_no=cert_no)
        chain_auth_result = []
        for i in chain_id.split(','):
            i = int(i)
            auth_message = await face_auth_address(i, message)
            if auth_message != "0x0000000000000000000000000000000000000000":
                chain_auth_result.append({"chainId": i, "status": True})
            else:
                chain_auth_result.append({"chainId": i, "status": False})
        return ErrorCode.SUCCESS, chain_auth_result

    async def auth_result_by_twitter(self, chain_id, twitter_id):
        msg = self.enciphered_data_twitter(twitter_id)
        chain_auth_result = []
        for i in chain_id.split(','):
            i = int(i)
            auth_message = await face_auth_address(i, msg)
            if auth_message != "0x0000000000000000000000000000000000000000":
                chain_auth_result.append({"chainId": i, "status": True})
            else:
                chain_auth_result.append({"chainId": i, "status": False})
        return ErrorCode.SUCCESS, chain_auth_result

    async def auth_result_address(self, chain_id, account_address):
        """
        查询每条链是否认证 根据账户地址
        """

        chain_auth_result = []
        for i in chain_id.split(','):
            i = int(i)
            auth_message = await get_face_auth_message(
                i, account_address
            )
            if auth_message:
                chain_auth_result.append({"chainId": i, "status": True})
            else:
                chain_auth_result.append({"chainId": i, "status": False})
        return ErrorCode.SUCCESS, chain_auth_result

    async def get_payment_message_api(self, chain_id, account_address):
        """
        查询链对应地址的支付记录
        """

        payment_message = await get_payment_message(
            chain_id, account_address
        )
        return ErrorCode.SUCCESS, payment_message
