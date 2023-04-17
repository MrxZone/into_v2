#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class FaucetBind(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, index=True)
    parent_address = Column(String, index=True, nullable=False)
    child_address = Column(String, index=True, nullable=False)
    device_id = Column(String, nullable=False)
