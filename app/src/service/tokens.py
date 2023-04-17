#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.core.config import settings
from app.src.common.httper import AsyncHttper
from app.src.common.singleton import Singleton


class TokensService(Singleton):
    async def get_transfer_history(
        self,
        chain_id: str,
        action: str,
        contract_address: str,
        address: str,
        page: int,
        offset: int,
        sort: str,
    ):
        if action == "tokentx":
            url = (
                f"{settings.API[chain_id]['url']}?module=account&action={action}"
                f"&contractaddress={contract_address}&address={address}&page={page}&offset={offset}"
                f"&startblock=0&endblock=latest&sort={sort}&apikey={settings.API[chain_id]['key']}"
            )
        elif action == "txlist":
            url = (
                f"{settings.API[chain_id]['url']}?module=account&action={action}"
                f"&address={address}&page={page}&offset={offset}"
                f"&startblock=0&endblock=latest&sort={sort}&apikey={settings.API[chain_id]['key']}"
            )
        else:
            raise Exception({"msg": "don't have this action"})
        res = await AsyncHttper.get_json(url)
        return res
