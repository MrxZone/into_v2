#!/usr/bin/env python
# -*- coding: utf-8 -*-


import aiohttp
from aiohttp.client_exceptions import ContentTypeError
from requests.packages.urllib3.util import Retry
from app.src.common.loggers import logger


class AsyncHttper(object):
    raise_error = True

    @classmethod
    # TODO: retry request
    async def _request(cls, url, method="get", **kwargs):
        # connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession() as session:
            # TODO(LiuTingwei): log request
            # logger.info(f"request url: {url}, method: {method}, kwargs: {kwargs}")
            try:
                async with session.request(method, url, **kwargs) as response:
                    if cls.raise_error:
                        response.raise_for_status()
                    try:
                        content = await response.json()
                    except ContentTypeError as e:
                        content = await response.text()
                    return content
            except Exception as e:
                raise

    @classmethod
    async def get_json(cls, url, method="get", **kwargs):
        return await cls._request(url, method, **kwargs)
