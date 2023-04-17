#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import random

from app.core.config import settings
from app.src.common.enum import Enum, EnumMem
from app.src.common.httper import AsyncHttper
from app.src.common.loggers import logger


class SmsChannelType(Enum):
    MAINLAND = EnumMem("m", "mainland")
    GLOBAL = EnumMem("g", "global")


class TemplateLanguage(Enum):
    CHINESE = EnumMem(1, "Chinese")
    ENGLISH = EnumMem(2, "English")
    KOREA = EnumMem(3, "Korea")
    JAPANESE = EnumMem(4, "Japanese")
    PORTUGUESE = EnumMem(5, "Portuguese")
    FRENCH = EnumMem(6, "French")
    RUSSIAN = EnumMem(7, "Russian")
    CHINESE_SIM = EnumMem(8, "Simplified Chinese")


CHINESE_CODE = "86"
CHINESE_TEMP = ("852", "853", "886")
ENGLISH_TEMP = ("65", "60", "66", "63", "234", "34", "84", "91", "44")
KOREA_TEMP = ("82",)
JAPANESE_TEMP = ("81",)
PORTUGUESE_TEMP = ("351",)
FRENCH_TEMP = ("33",)
RUSSIAN_TEMP = ("7",)


class SmsTemplate:
    TEMPLATE_MAP = {
        TemplateLanguage.CHINESE_SIM: "",
        TemplateLanguage.CHINESE: "",
        TemplateLanguage.ENGLISH: "",
        TemplateLanguage.KOREA: "",
        TemplateLanguage.JAPANESE: "",
        TemplateLanguage.PORTUGUESE: "",
        TemplateLanguage.FRENCH: "",
        TemplateLanguage.RUSSIAN: "",
    }

    @classmethod
    def parse_language(cls, country_code):
        if country_code == CHINESE_CODE:
            return TemplateLanguage.CHINESE_SIM

        if country_code in ENGLISH_TEMP:
            return TemplateLanguage.ENGLISH

        if country_code in CHINESE_TEMP:
            return TemplateLanguage.CHINESE

        if country_code in KOREA_TEMP:
            return TemplateLanguage.KOREA

        if country_code in JAPANESE_TEMP:
            return TemplateLanguage.JAPANESE

        if country_code in PORTUGUESE_TEMP:
            return TemplateLanguage.PORTUGUESE

        if country_code in FRENCH_TEMP:
            return TemplateLanguage.FRENCH

        if country_code in RUSSIAN_TEMP:
            return TemplateLanguage.RUSSIAN

        return TemplateLanguage.ENGLISH

    @classmethod
    def generator(cls, country_code, sms_code):
        _language = cls.parse_language(country_code)
        return cls.TEMPLATE_MAP[_language].format(sms_code=sms_code)


class SmsProxy:
    class SMSECode(Enum):
        FAILD = EnumMem(0, "失败")
        AUTH = EnumMem(-1, "用户名或者密码不正确")
        MUSTEMP = EnumMem(-2, "必填选项为空")
        EMPTY = EnumMem(-3, "短信内容0个字节")
        PARAM = EnumMem(-4, "提交地址或参数有误")
        BALANCE = EnumMem(-5, "余额不够")
        DISABLE = EnumMem(-10, "用户被禁用")
        MAXCHARS = EnumMem(-11, "短信内容超过500字")
        NOEXT = EnumMem(-12, "无扩展权限(ext字段需填空)")
        IP = EnumMem(-13, "IP校验错误")
        CONTEXT = EnumMem(-14, "内容解析异常")
        UNKNOW = EnumMem(-990, "未知错误")

    def __init__(
        self, name, username, password, channel_type=SmsChannelType.MAINLAND
    ) -> None:
        self.username = username
        self.password = password
        self.name = name
        self.channel_type = channel_type
        self._host = "https://api.smsxy.com/smsSend.do"

    def gen_pwd(self, username, password):
        pwd_dig = hashlib.md5(password.encode()).hexdigest()
        password = hashlib.md5((username + pwd_dig).encode())
        return password.hexdigest()

    def get_params(self, phone, content):
        params = {
            "username": self.username,
            "password": self.gen_pwd(self.username, self.password),
            "mobile": phone,
            "content": content,
        }
        r = {"url": self._host, "method": "GET", "params": params}
        return r

    def raise_error(self, response):
        try:
            sms_resp_id = int(response)
        except ValueError as e:
            logger.error(f"SmsAPI Error, HTTP body is: {sms_resp_id}")
            return -1

        if sms_resp_id <= 0:
            logger.error(
                f"SmsAPI Error, Code: {sms_resp_id}, Description: {self.SMSECode.desc(sms_resp_id, 'UNKNOW')}"
            )
        return sms_resp_id

    def __str__(self) -> str:
        s = super().__str__()
        return s + f"proxy name is: {self.name}"

    def __repr__(self) -> str:
        return self.__str__


class SmsServer:
    Gmap = {SmsChannelType.GLOBAL: dict(), SmsChannelType.MAINLAND: dict()}

    @classmethod
    def register(cls, proxy: SmsProxy):
        cls.Gmap[proxy.channel_type] = {proxy.name: proxy}

    @classmethod
    def choice_proxy(cls, country_code) -> SmsProxy:
        _channel_type = SmsChannelType.MAINLAND
        if country_code != CHINESE_CODE:
            _channel_type = SmsChannelType.GLOBAL
        proxy_list = list(cls.Gmap[_channel_type].values())
        return random.choice(proxy_list)

    @classmethod
    def parse_phone(cls, phone: str):
        _phone = phone
        while True:
            if _phone[0] == "0":
                _phone = _phone[1:]
            else:
                break
        return _phone

    @classmethod
    async def send_sms(cls, country_code: str, phone: str, sms_code: str):
        _template = SmsTemplate.generator(country_code, sms_code)
        _proxy = cls.choice_proxy(country_code)
        _sms_phone = phone
        if _proxy.channel_type == SmsChannelType.GLOBAL:
            phone = cls.parse_phone(phone)
            _sms_phone = country_code + phone
        resp = await AsyncHttper._request(**_proxy.get_params(_sms_phone, _template))
        return _proxy.raise_error(resp)


class SmsManager:
    def __init__(self) -> None:
        self._server = SmsServer
        self._server.register(
            SmsProxy(
                "mainland_xy",
                username=settings.MAINLAND_XY_SMS_USERNAME,
                password=settings.MAINLAND_XY_SMS_PASSWORD,
                channel_type=SmsChannelType.MAINLAND,
            ),
        )
        self._server.register(
            SmsProxy(
                "global_xy",
                username=settings.GLOBAL_XY_SMS_USERNAME,
                password=settings.GLOBAL_XY_SMS_PASSWORD,
                channel_type=SmsChannelType.GLOBAL,
            )
        )

    async def send_sms(self, country_code: str, phone: str, sms_code: str):
        return await self._server.send_sms(country_code, phone, sms_code)


sms_manager = SmsManager()
