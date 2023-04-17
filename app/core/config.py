#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib

from pydantic import BaseSettings

WORK_PATH = pathlib.Path(__name__).resolve().parent
AVATAR_PATH = WORK_PATH / "FileResource"
setting_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings")


class Settings(BaseSettings):
    APP_NAME: str
    SQLALCHEMY_DATABASE_URI: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    SECRET_KEY: str
    AES_KEY: str
    ENVIRONMENT: str = "DEV"

    # Redis
    REDIS_URL: str

    # EASEMOB
    EASEMOB_ORGNAME: str
    EASEMOB_APPNAME: str
    EASEMOB_CLIENTID: str
    EASEMOB_CLIENTSECRET: str
    EASEMOB_HOST: str
    EASEMOB_CALLBACK_1: str
    EASEMOB_ROBOT_1: str

    # 歆阳通讯短信
    MAINLAND_XY_SMS_USERNAME: str
    MAINLAND_XY_SMS_PASSWORD: str
    GLOBAL_XY_SMS_USERNAME: str
    GLOBAL_XY_SMS_PASSWORD: str

    # ALI FACE VERIFY
    SCENE_ID: str
    OUTER_ORDER_NO: str
    ACCESS_KEY_ID: str
    ACCESS_KEY_SECRET: str

    # WEB3
    CHAIN: dict

    PRIVATE_KEY: str
    FAUCET_PRIVATE_KEY: str
    INTO_FAUCET_ADDRESS: str
    API: dict

    # AgoraIO
    AgoraIO_APPID: str
    AgoraIO_CERTIFICATE: str

    # QCloudCOS
    COS_BUCKET: str
    COS_BUCKET_REGION: str
    COS_BUCKET_GLOBAL_CDN: str
    COS_SECRETID: str
    COS_SECRETKEY: str

    # twitter
    CONSUMER_KEY: str
    CONSUMER_SECRET: str


class Production(Settings):
    class Config:
        # 生产环境配置单独上传,不提交至git
        env_file = os.path.join(setting_file_path, ".env")
        env_file_encoding = 'utf-8'


class Testing(Settings):
    class Config:
        env_file = os.path.join(setting_file_path, ".testing.env")
        env_file_encoding = 'utf-8'


class Dev(Settings):
    class Config:
        env_file = os.path.join(setting_file_path, ".dev.env")
        env_file_encoding = 'utf-8'


def get_settings():
    env = os.getenv("INTOENV", "DEV")
    _inst = Dev()
    if env == "TESTING":
        _inst = Testing()
    if env == "PRODUCTION":
        _inst = Production()
    _inst.ENVIRONMENT = env
    return _inst


settings = get_settings()
settings.CHAIN = {}
settings.API = {}
