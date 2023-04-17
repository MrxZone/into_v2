#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, text

from app.db.base_class import Base


class Web3Project(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    address = Column(String, default="", server_default=text("''"), doc="合约地址")
    name = Column(String, default="", server_default=text("''"), doc="项目名称")
    img = Column(String, default="", server_default=text("''"), doc="项目图片")
    web_name = Column(String, default="", server_default=text("''"), doc="")


class Web3PayOrder(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uid = Column(String, default="", server_default=text("''"), doc="")
    group_id = Column(Integer, default=0, server_default=text("'0'"), doc="项目ID")
    level = Column(
        Integer,
        default=0,
        server_default=text("'0'"),
    )
    order_id = Column(String, default="", server_default=text("''"), doc="")
