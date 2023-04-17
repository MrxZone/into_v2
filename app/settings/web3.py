#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class WebSettings:
    MUMBAI = "mumbai"
    MATCH = "match"
    POLYGON = "polygon"
    BSC = "bscscan"
    MATCHTEST = "match_test"
    GANACHE = "ganache"

    @classmethod
    def get_rpc(cls, chain_name):
        item = dict(
            match_test="",
            bscscan="",
            mumbai="",
            match="",
            polygon="",
            ganache="",
        )
        return item[chain_name]

    @classmethod
    def get_test_contract_address(cls, contract_name):
        item = dict(
            BSCRelation=[cls.GANACHE, ""],
            IntoBind=[cls.GANACHE, ""],
            # CTRelation=[cls.GANACHE, ""],
            IntoPay=[cls.GANACHE, ""],
        )
        return item[contract_name]

    @classmethod
    def get_dev_contract_address(cls, contract_name):
        item = dict(
            BSCRelation=[cls.BSC, ""],
            MATCHRelation=[cls.MATCHTEST, ""],
            IntoBind=[cls.MATCHTEST, ""],
            IntoPay=[cls.MATCHTEST, ""],
        )
        return item[contract_name]

    @classmethod
    def get_production_contract_address(cls, contract_name):
        item = dict(
            BSCRelation=[cls.BSC, ""],
            MATCHRelation=[cls.MATCHTEST, ""],
            IntoBind=[cls.MATCHTEST, ""],
            IntoPay=[cls.MATCHTEST, ""],
        )
        return item[contract_name]

    @classmethod
    def get_contract_address(cls, contract_name):
        env = os.getenv("INTOENV", "DEV")
        if env == "PRODUCTION":
            return cls.get_production_contract_address(contract_name)
        elif env == "TESTING":
            return cls.get_test_contract_address(contract_name)
        return cls.get_dev_contract_address(contract_name)
