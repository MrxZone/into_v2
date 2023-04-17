#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib

from pydantic import BaseModel, Field

import app.crud as crud
from app.core.config import AVATAR_PATH
from app.db.session import async_session
from app.schemas.versions import VersionsCreate
from app.src.common.qcloud.cos import upload_file
from app.src.common.singleton import Singleton
from app.tools.utils import del_file, save_file


class VersionInfoItem(BaseModel):
    version_name: str = Field(description="")
    version_code: int = Field(description="")
    new_version_name: str = Field(description="")
    new_version_code: int = Field(description="")
    release_channel: str = Field(description="")
    ecosystem: str = Field(description="")
    is_forced_updating: bool = Field(description="")
    change_log: str = Field(description="")


class VersionsService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.versions

    async def get_version(
        self, version_code: int, release_channel: str, ecosystem: str
    ):
        return await self.crud.get_version(
            self.db,
            version_code=version_code,
            release_channel=release_channel.lower(),
            ecosystem=ecosystem.lower(),
        )

    async def create_version(self, version_info: VersionInfoItem, file):
        file_type = ""
        if ".apk" not in version_info.new_version_name:
            file_type = ".apk"
        local_file_path, file_name = await save_file(
            file=file,
            facker_filename=version_info.new_version_name,
            file_type=file_type,
            path=AVATAR_PATH,
        )
        with open(local_file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        cos_resource_url = upload_file(local_file_path, file_name)
        obj_in = VersionsCreate(
            **version_info.dict(),
            new_app_download_url=cos_resource_url,
            md5=file_hash.hexdigest(),
        )
        return await self.crud.create(self.db, obj_in=obj_in)

    async def upload_file(self, file):
        file_type = ""
        if ".apk" not in file.filename:
            file_type = ".apk"
        local_file_path, file_name = await save_file(
            file=file,
            facker_filename=file.filename,
            file_type=file_type,
            path=AVATAR_PATH,
        )
        with open(local_file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        cos_resource_url = upload_file(local_file_path, file_name)
        return {
            "url": cos_resource_url,
            "hash": file_hash.hexdigest(),
        }

    async def del_version_file(self, file_name):
        # TODO(LiuTingwei): auto parse file type
        file_type = ""
        if ".apk" not in file_name:
            file_type = ".apk"
        await del_file(file_name, file_type, AVATAR_PATH)

    # async def update_version(self, obj_in: VersionsUpdate):
    #     pass
    #
    # async def delete_version(self, id: int):
    #     pass
