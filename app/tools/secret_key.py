#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random


def generate_secret_key(length: int):
    """
    生成固定长度的密钥
    :param length:
    :return:
    """
    seed = r"""1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()_+}{|:;'",<.>/?=[]-\\"""
    secret_key = ""
    for i in range(length):
        secret_key += random.choice(seed)
    return secret_key


if __name__ == '__main__':
    a = generate_secret_key(16)
    print(a)
