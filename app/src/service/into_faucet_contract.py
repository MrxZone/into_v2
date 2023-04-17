#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import logging
from app.src.service.contract import ContractHandler, set_gas
from app.core.celery_app import celery_app
from app.core.config import settings

chain = settings.CHAIN
private_key = settings.FAUCET_PRIVATE_KEY
into_faucet_address = settings.INTO_FAUCET_ADDRESS
into_faucet_abi = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'abi/IntoFaucet.json'
)


@celery_app.task(bind=True)
def into_faucet_bind(self, parent, child, uid, device_id):
    try:
        w3 = ContractHandler.create("9001")
        admin_address = w3.eth.account.from_key(private_key).address
        nonce = w3.eth.get_transaction_count(admin_address)
        contract = ContractHandler.get_contract_with_address(
            w3, into_faucet_abi, into_faucet_address
        )
        transaction = {'from': admin_address, 'nonce': nonce}
        contract_method = contract.functions.bind(parent, child, uid, device_id)
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
                "func": "into_faucet_contract.into_faucet_bind",
                "param": [parent, child, uid, device_id],
                "code": 40010,
                "msg": "transaction failure",
                "receipt": str(receipt)
            })

    except Exception as e:
        raise self.retry(exc=e, countdown=10, max_retries=3)
