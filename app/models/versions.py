#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.db.base_class import Base


class Versions(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    version_name = Column(String, nullable=False)
    version_code = Column(Integer, index=True, nullable=False)
    new_version_name = Column(String, nullable=False)
    new_version_code = Column(Integer, nullable=False)
    release_channel = Column(String, index=True, nullable=False)
    ecosystem = Column(String, index=True, nullable=False)
    is_forced_updating = Column(Boolean, nullable=False)
    new_app_download_url = Column(String, nullable=False)
    md5 = Column(String, nullable=False)
    change_log = Column(String)

    __table_args__ = (
        UniqueConstraint('version_code', 'release_channel', 'ecosystem', name='version_unique'),
    )
