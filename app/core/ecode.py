#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.src.common.enum import Enum, EnumMem

__all__ = ['ErrorCode']


class ErrorCode(Enum):
    """
    全局错误码
    """

    # 系统码
    NOT_EXISTS = EnumMem(-1, "不存在")
    SUCCESS = EnumMem(0, "成功")
    PARAM = EnumMem(1, "参数错误")
    INTER = EnumMem(2, "内部错误")
    TIMEOUT = EnumMem(3, "外部接口超时")
    EXTERNAL = EnumMem(4, "外部接口错误")
    RESRC = EnumMem(5, "接口不存在")
    AUTH = EnumMem(6, "鉴权失败")
    FORBID = EnumMem(7, "访问禁止")
    EXIST = EnumMem(8, "实体已存在")
    NOT_EXIST = EnumMem(9, "实体不存在")
    TOO_FREQUENT = EnumMem(10, "请求过于频繁")
    VERSION = EnumMem(11, "版本错误")

    # 用户相关
    TOKEN = EnumMem(11000, "Token无效")
    ACCOUNT = EnumMem(11001, "账号无效")

    # 短信相关
    SMS_CODE_ERR = EnumMem(12100, "验证码错误")
    SMS_TIMEOUT_ERR = EnumMem(12101, "验证码过期")
    SMS_TOO_FREQUENT = EnumMem(12102, "验证码请求频繁")
    SMS_VERIFY_LIMIT = EnumMem(12103, "错误次数过多")

    # 群消息相关
    GROUP_FORWARD_ON = EnumMem(12200, "群已开启消息转发")
    GROUP_FORWARD_FAILED = EnumMem(12201, "群转发开启失败")


    # 私钥云备份
    DUPLICATE_BACKUP_ERR = EnumMem(13001, "当前地址私钥已备份，请移除备份后重试")

    # 人脸识别相关
    NON_PAYMENT_ERR = EnumMem(14000, "未检测到支付信息，请稍等或者重新支付")
    IDENTIFY_ERR = EnumMem(14001, "身份证号码验证失败，请重新输入")
    VERIFY_ACCOUNT_ADDRESS_ERR = EnumMem(14002, "Web3账户地址校验失败")
    VERIFICATION_MESSAGE_ERR = EnumMem(14003, "身份信息不存在")
    UNPAID_CHAIN_ERR = EnumMem(14004, "当前所选链，拥有未支付的链")

    # Twitter相关
    TWITTER_OAUTH_AUTHORIZATION_ERR = EnumMem(15000, "Twitter授权验证失败")

    # FaucetBind相关
    HAVE_ALREADY_FAUCET_BIND_ERR = EnumMem(16000, "当前用户已经领取")

    #
    # CREATE_DATA_ERR = EnumMem(11001, "创建失败")
    # SELECT_DATA_ERR = EnumMem(11002, "查询失败")
    # UPDATE_DATA_ERR = EnumMem(11003, "修改失败")
    # DELETE_DATA_ERR = EnumMem(11004, "删除失败")

    # 针对业务错误码，一定要留有冗余位给未来新增的错误码
    # 业务大类需要留有足够的冗余错误码，比如数据类错误可以是20001，20002……
    # PULL_DATA_ERR = EnumMem(20000, "数据拉取失败")

    # CAL_DATA_ERR = EnumMem(30000, '计算失败')
