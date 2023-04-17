#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Union

from pydantic import BaseModel


class KeysBase(BaseModel):
    user_id: Union[int, None]
    account_address: str


class KeysCreate(KeysBase):
    account_name: str
    private_key: str

    class Config:
        schema_extra = {
            "example": {
                "account_address": "0x86a8478F78219421B0e4EC80F14a278ffdc0dA27",
                "account_name": "jacob",
                "private_key": "9/fall90",
            }
        }


class KeysUpdate(KeysBase):
    id: int
    account_name: str


class KeysDelete(BaseModel):
    id: int
    user_id: Optional[int]


class KeysDeleteWithUser(KeysDelete):
    user_id: int
