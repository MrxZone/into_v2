#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class PrivateKeys(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    account_address = Column(String, index=True, nullable=False)
    account_name = Column(String, nullable=False)
    private_key = Column(String, nullable=False)
