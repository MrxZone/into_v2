#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.service.coingecko_api import CoinGeckoAPI, Broker

router = BaseRouter(tags=["proxy_coin_gecko"])

# use free plan
broker = Broker(api_key="", host="")

cg = CoinGeckoAPI(broker=broker)


@router.get('/simple/token_price/{chain_slug}', summary="")
def get_token_price(
    chain_slug: str,
    contract_addresses: str,
    vs_currencies: str,
    include_24hr_change: bool,
):
    res = cg.get_token_price(
        chain_slug,
        contract_addresses,
        vs_currencies,
        include_24hr_change=include_24hr_change,
    )
    return ErrorCode.SUCCESS, res


@router.get('/simple/price/', summary="")
def get_token_price(
    ids: str,
    vs_currencies: str,
    include_24hr_change: bool,
):
    res = cg.get_price(
        ids,
        vs_currencies,
        include_24hr_change=include_24hr_change,
    )
    return ErrorCode.SUCCESS, res


@router.get('/asset_platforms', summary="")
def get_asset_platforms():
    json_data = dict()
    try:
        with open("app/src/static/asset_platforms.json") as f:
            json_data = json.load(f)
    except Exception as e:
        print(e)
        json_data = cg.get_asset_platforms()

    return ErrorCode.SUCCESS, json_data


@router.get('/simple/supported_vs_currencies', summary="")
def get_supported_vs_currencies():
    json_data = ""
    try:
        with open("app/src/static/supported_vs_currencies.json") as f:
            json_data = json.load(f)
    except Exception as e:
        print(e)
        json_data = cg.get_supported_vs_currencies()

    return ErrorCode.SUCCESS, json_data
