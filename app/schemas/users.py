#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from pydantic import BaseModel


class OrmModeBase(BaseModel):
    class Config:
        orm_mode = True


# Shared properties
class UserBase(OrmModeBase):
    username: Optional[str] = None
    phone: Optional[str] = None


# Properties to receive via API on creation
class UsersCreate(OrmModeBase):
    username: str
    phone: str


# Properties to receive via API on update
class UsersUpdate(OrmModeBase):
    password: Optional[str] = None
