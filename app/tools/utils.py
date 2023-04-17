#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from pathlib import Path

from fastapi import UploadFile
from fastapi import HTTPException, status
from app.core.config import settings


def _mkdir(path):
    try:
        p = Path(path)
        p.mkdir(parents=True)
    except FileExistsError:
        pass


async def save_file(file: UploadFile, facker_filename: str, file_type: str, path: Path):
    _mkdir(path)
    _file_name = facker_filename + file_type
    all_path = "{}/{}".format(str(path), _file_name)
    with open(all_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return all_path, _file_name


async def del_file(file_name: str, file_type: str, path: Path):
    _file_name = file_name + file_type
    all_path = "{}/{}".format(str(path), _file_name)
    if os.path.exists(all_path):
        os.remove(all_path)


def testing_api(func):
    async def wrapper():
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if settings.ENVIRONMENT == "PRODUCTION":
        func = wrapper
    return func


def get_app_name() -> str:
    return settings.APP_NAME.lower()
