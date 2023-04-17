#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from settings.web3 import WebSettings
from web3 import Web3
from web3.middleware import geth_poa_middleware

from app.src.common.loggers import logger

# keyDict = {"BSCRelation": "BSCRelation", "IntoBind": "IntoBind","IntoMessage":"IntoMessage"}


class Web3Config:
    http = {}

    # @classmethod
    def __init__(self, rpc):
       
        w3 = self.http.get(rpc)

        if isinstance(w3, Web3):
            if not w3.is_connected():
                w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 60}))
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        else:
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 60}))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.http[rpc] = w3
        self.w3=w3
        # return w3

    # def __init__(self, rpc) -> None:
    #     self.w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 60}))
    #     self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def initContract(self, abiName, address):
        CAKE_BSC_ABI = self.getABI(abiName)

        CAKE_BSC_ADDRESS = Web3.to_checksum_address(address)

        contract = self.w3.eth.contract(address=CAKE_BSC_ADDRESS, abi=CAKE_BSC_ABI)

        return contract

    def getABI(self, abiName):
        path = os.getcwd()
        path = "{}/app/core/abis/{}.json".format(path, abiName)

        with open(path, 'r', encoding='UTF-8') as file:
            items = json.load(file)

        return items


class IntoWeb3:
    # 链名称

    @classmethod
    def get_rpc(cls, chain_name):
        return WebSettings.get_rpc(chain_name)

    @classmethod
    def init_contract(cls, abi_name, address, rpc):
        w3 = Web3Config(cls.get_rpc(rpc))
        # logger.debug(f"abi_name is {abi_name}")
        contract = w3.initContract(abi_name, address)
        return contract

    @classmethod
    def to_checksum_address(cls, items):
        return [Web3.to_checksum_address(o) for o in items]
