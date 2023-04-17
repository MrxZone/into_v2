#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Union

from pydantic import BaseModel


class FaucetBindBase(BaseModel):
    user_name: str


class FaucetBindCreate(FaucetBindBase):
    parent_address: str
    child_address: str
    device_id: Union[str, None]

    class Config:
        schema_extra = {
            "example": {
                "user_name": "8618611112222",
                "parent_address": "0xa87317766b6C2F8A1f18FfB428886936C3F442A6",
                "child_address": "0x86a8478F78219421B0e4EC80F14a278ffdc0dA27",
                "device_id": "9/fall90",
            }
        }
