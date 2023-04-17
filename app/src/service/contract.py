#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os
import logging
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware

from app.core.celery_app import celery_app
from app.core.config import settings

chain = settings.CHAIN
private_key = settings.PRIVATE_KEY


class ContractHandler:
    http = {}

    @classmethod
    def create(cls, chain_id):
        chain_id = str(chain_id)
        w3 = cls.http.get(chain_id)

        if isinstance(w3, Web3):
            if not w3.is_connected():
                w3 = Web3(HTTPProvider(chain[chain_id]["rpc_url"]))
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        else:
            w3 = Web3(HTTPProvider(chain[chain_id]["rpc_url"]))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        cls.http[chain_id] = w3
        return w3

    @classmethod
    def get_contract(cls, w3, chain_id, abi_path_param):
        with open(abi_path_param, 'r') as abi_definition:
            abi = json.load(abi_definition)
        return w3.eth.contract(
            address=chain[chain_id]["contract_address"], abi=abi["abi"]
        )

    @classmethod
    def get_contract_with_address(cls, w3, abi_path_param, contract_address):
        with open(abi_path_param, 'r') as abi_definition:
            abi = json.load(abi_definition)
        return w3.eth.contract(address=contract_address, abi=abi["abi"])


"""
实名认证合约接口
"""
abi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abi/Auth.json')


def set_gas(estimate_gas, gas_price):
    return {
        'gas': max(int(estimate_gas * 1.2), 21000),  # gas 数量限制
        'gasPrice': gas_price,  # gasPrice
    }


async def get_payment_message(chain_id, account_address):
    chain_id = str(chain_id)
    w3 = ContractHandler.create(chain_id)
    auth_contract = ContractHandler.get_contract(w3, chain_id, abi_path)
    admin_address = w3.eth.account.from_key(private_key).address
    payment_message = auth_contract.functions.getPaymentMessage(account_address).call(
        {"from": admin_address}
    )
    return [{"chainId": _id, "status": status} for _id, status in payment_message]


async def face_auth_address(chain_id, message):
    chain_id = str(chain_id)
    w3 = ContractHandler.create(chain_id)
    auth_contract = ContractHandler.get_contract(w3, chain_id, abi_path)
    admin_address = w3.eth.account.from_key(private_key).address
    auth_message = auth_contract.functions.faceAuthAddress(message).call(
        {"from": admin_address}
    )
    return auth_message


async def get_face_auth_message(chain_id, account_address):
    chain_id = str(chain_id)
    w3 = ContractHandler.create(chain_id)
    auth_contract = ContractHandler.get_contract(w3, chain_id, abi_path)
    admin_address = w3.eth.account.from_key(private_key).address
    auth_message = auth_contract.functions.getFaceAuthMessage(account_address).call(
        {"from": admin_address}
    )
    return auth_message


@celery_app.task(bind=True)
def set_face_auth_message(self, chain_id, account_address, message):
    # TODO(Jacob) 添加任务重拾失败后的邮件提醒
    try:
        chain_id = str(chain_id)
        w3 = ContractHandler.create(chain_id)
        auth_contract = ContractHandler.get_contract(w3, chain_id, abi_path)
        admin_address = w3.eth.account.from_key(private_key).address
        nonce = w3.eth.get_transaction_count(admin_address)
        transaction = {
            'from': admin_address,
            'nonce': nonce,
        }
        contract_method = auth_contract.functions.setFaceAuthMessage(
            account_address, message
        )
        gas_estimate = contract_method.estimate_gas(transaction=transaction)
        transaction.update(set_gas(gas_estimate, w3.eth.gas_price))
        txn = contract_method.build_transaction(transaction)
        signed_txn = w3.eth.account.sign_transaction(
            transaction_dict=txn, private_key=private_key
        )
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        if receipt.status != 1:
            logging.error({
                "func": "contract.set_face_auth_message",
                "param": [chain_id, account_address, message],
                "code": 40010,
                "msg": "transaction failure",
                "receipt": str(receipt)
            })
            raise Exception({"code": 40010, "msg": "transaction failure"})
    except Exception as e:
        raise self.retry(exc=e, countdown=10, max_retries=3)
