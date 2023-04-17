#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import re

from Crypto.Cipher import AES

from app.core.config import settings


class AESText:
    # key 长度8-16位 数字 字母(大小写) 特殊字符
    regular_expression = (
        r"""(?=^.{8,16}$)(?!.*\s)[0-9a-zA-Z`~!@#$%^&*()_+}{|:;'",<.>/?\=\[\]\-\\]*$"""
    )

    def pkcs7_padding(self, text: str):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用''
        padding_text = chr(padding) * padding
        return text + padding_text

    def pkcs7_unpadding(self, text: str):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0 : length - unpadding]

    def encrypt(self, key: str, content: str):
        """
        AES加密
        key,iv使用同一个
        模式cbc
        填充pkcs7
        :param key: 密钥
        :param content: 加密内容
        :return:
        """
        key_bytes = bytes(self.regenerate(key), encoding='utf-8')
        iv = key_bytes
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # 处理明文
        content_padding = self.pkcs7_padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def decrypt(self, key: str, content: str):
        """
        AES解密
         key,iv使用同一个
        模式cbc
        去填充pkcs7
        :param key:
        :param content:
        :return:
        """
        key_bytes = bytes(self.regenerate(key), encoding='utf-8')
        iv = key_bytes
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # base64解码
        encrypt_bytes = base64.b64decode(content)
        # 解密
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        # 重新编码
        result = str(decrypt_bytes, encoding='utf-8')
        # 去除填充内容
        result = self.pkcs7_unpadding(result)
        return result

    def verify(self, key: str):
        """
        采取传统密码校验的形式对密钥进行校验
        :param key:
        :return:
        """
        res = re.search(self.regular_expression, key)
        return True if res else False

    def regenerate(self, key: str):
        """
        将密钥补充到16位
        :param key:
        :return:
        """

        key_length = len(key)
        if not self.verify(key):
            raise Exception("Key format error")

        key += settings.SECRET_KEY[0 : (16 - key_length)]
        return key


aes = AESText()

if __name__ == '__main__':
    from app.tools.secret_key import generate_secret_key

    for i in range(1000):
        my_key = generate_secret_key(16)
        secret_text = aes.encrypt(key=my_key, content="baby love")
        origin_text = aes.decrypt(key=my_key, content=secret_text)
