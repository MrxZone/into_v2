#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional, Union

from pydantic import BaseModel


class VerificationsUpdate(BaseModel):
    user_id: int
    account_address: str
    message: str
    chain_id: int
    message: Union[str, None]
    status: Union[int, None]


class VerificationsCreate(BaseModel):
    user_id: int
    account_address: str
    chain_id: int
    message: Union[str, None]
    status: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "account_address": "0x86a8478F78219421B0e4EC80F14a278ffdc0dA27",
                "chain_id": 137,
            }
        }


class VerificationsSchema(BaseModel):
    user_id: Optional[int]
    chain_id: int
    account_address: str
    cert_name: str
    cert_no: str
    meta_info: str
    return_url: str

    class Config:
        schema_extra = {
            "example": {
                "chain_id": 137,
                "account_address": "0x86a8478F78219421B0e4EC80F14a278ffdc0dA27",
                "cert_name": "杨森",
                "cert_no": "341282199401115518",
                "meta_info": str(
                    {
                        "zimVer": "3.0.0",
                        "appVersion": "1",
                        "bioMetaInfo": "4.1.0:11501568,0",
                        "appName": "com.aliyun.antcloudauth",
                        "deviceType": "ios",
                        "osVersion": "iOS 10.3.2",
                        "apdidToken": "",
                        "deviceModel": "iPhone9,1",
                    }
                ),
                "return_url": "www.baidu.com",
            }
        }
