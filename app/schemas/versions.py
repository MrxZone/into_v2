#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

from pydantic import BaseModel


class OrmModeBase(BaseModel):
    class Config:
        orm_mode = True


class VersionsBase(OrmModeBase):
    id: int
    app_version: str
    release_channel: str
    ecosystem: str
    is_forced_updating: bool
    new_app_version: str
    new_app_download_url: str
    change_log: Optional[str]


class VersionsCreate(OrmModeBase):
    version_name: str
    version_code: int
    new_version_name: str
    new_version_code: int
    release_channel: str
    ecosystem: str
    is_forced_updating: bool
    md5: str
    new_app_download_url: str
    change_log: Optional[str]


class VersionsUpdate(OrmModeBase):
    is_forced_updating: bool
    new_app_version: str
    new_app_download_url: str
    change_log: Optional[str]
