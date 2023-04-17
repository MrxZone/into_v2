#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text

from app.db.base_class import Base


class Verifications(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False)
    account_address = Column(String(50), index=True)
    chain_id = Column(Integer, index=True)
    message = Column(String(500))
    status = Column(Integer, default=0, server_default=text("'0'"))
