#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, text
from app.db.base_class import Base


class Users(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)


class UserBind(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    userid = Column(BigInteger, index=True)
    nickname = Column(String, server_default=text("''"), nullable=False)
    avatarurl = Column(String, server_default=text("''"), nullable=False)
    access_token = Column(String, server_default=text("''"), nullable=False)
