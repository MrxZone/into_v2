#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alibabacloud_cloudauth20190307 import models as cloudauth_models
from alibabacloud_cloudauth20190307.client import Client as CloudauthClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

from app.core.config import settings

SCENE_ID = settings.SCENE_ID
OUTER_ORDER_NO = settings.OUTER_ORDER_NO
ACCESS_KEY_ID = settings.ACCESS_KEY_ID
ACCESS_KEY_SECRET = settings.ACCESS_KEY_SECRET


class InitFaceVerify:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        endpoint: str,
    ) -> CloudauthClient:
        config = open_api_models.Config(
            # 您的AccessKey ID。
            access_key_id=ACCESS_KEY_ID,
            # 您的AccessKey Secret。
            access_key_secret=ACCESS_KEY_SECRET,
            # 设置HTTP代理。
            # http_proxy='http://xx.xx.xx.xx:xxxx',
            # 设置HTTPS代理。
            # https_proxy='https://username:password@xxx.xxx.xxx.xxx:9999',
            endpoint=endpoint,
        )
        return CloudauthClient(config)

    @staticmethod
    def main(cert_name: str, cert_no: str, meta_info: str, return_url: str) -> dict:
        request = cloudauth_models.InitFaceVerifyRequest(
            # 请输入场景ID。
            scene_id=SCENE_ID,
            outer_order_no=OUTER_ORDER_NO,
            # 要接入的认证方案。
            product_code='ID_PRO',
            model='LIVENESS',
            # 固定值IDENTITY_CARD。
            cert_type='IDENTITY_CARD',
            cert_name=cert_name,
            cert_no=cert_no,
            return_url=return_url,
            # MetaInfo环境参数，需要通过客户端SDK获取。
            meta_info=meta_info,
        )
        response = InitFaceVerify.init_face_verify_auto_route(request)
        # 不支持服务自动路由。
        # response = InitFaceVerify.init_face_verify('cloudauth.cn-shanghai.aliyuncs.com', request)
        return {
            'code': response.code,
            'message': response.message,
            'request_id': response.request_id,
            'certify_id': response.result_object.certify_id,
            'certify_url': response.result_object.certify_url,
        }

    @staticmethod
    def init_face_verify_auto_route(
        request: cloudauth_models.InitFaceVerifyRequest,
    ) -> cloudauth_models.InitFaceVerifyResponse:
        endpoints = [
            'cloudauth.cn-shanghai.aliyuncs.com',
            'cloudauth.cn-beijing.aliyuncs.com',
        ]
        for endpoint in endpoints:
            try:
                response = InitFaceVerify.init_face_verify(endpoint, request)
                if UtilClient.equal_string('500', response.body.code):
                    continue
                return response.body
            except Exception as err:
                # 网络异常，切换到下个区域调用。
                print(err)
                continue
        return None

    @staticmethod
    def init_face_verify(
        endpoint: str,
        request: cloudauth_models.InitFaceVerifyRequest,
    ) -> cloudauth_models.InitFaceVerifyResponse:
        client = InitFaceVerify.create_client(endpoint)
        return client.init_face_verify(request)


class DescribeFaceVerify:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        endpoint: str,
    ) -> CloudauthClient:
        config = open_api_models.Config(
            # 您的AccessKey ID。
            access_key_id=ACCESS_KEY_ID,
            # 您的AccessKey Secret。
            access_key_secret=ACCESS_KEY_SECRET,
            # 设置HTTP代理。
            # http_proxy='http://xx.xx.xx.xx:xxxx',
            # 设置HTTPS代理。
            # https_proxy='https://xx.xx.xx.xx:xxxx',
            endpoint=endpoint,
        )
        return CloudauthClient(config)

    @staticmethod
    def main(certify_id: str) -> dict:
        request = cloudauth_models.DescribeFaceVerifyRequest(
            # 请输入场景ID。
            scene_id=SCENE_ID,
            certify_id=certify_id,
        )
        response = DescribeFaceVerify.describe_face_verify_auto_route(request)
        if response is not None:
            re = {
                'code': response.code,
                'message': response.message,
                'request_id': response.request_id,
            }
        else:
            re = {'code': 0, 'message': '阿里云人脸认证接口未返回数据', 'request_id': None}
        re.update(response.result_object.__dict__)
        return re

    @staticmethod
    def describe_face_verify_auto_route(
        request: cloudauth_models.DescribeFaceVerifyRequest,
    ) -> cloudauth_models.DescribeFaceVerifyResponse:
        endpoints = [
            'cloudauth.cn-shanghai.aliyuncs.com',
            'cloudauth.cn-beijing.aliyuncs.com',
        ]
        for endpoint in endpoints:
            try:
                response = DescribeFaceVerify.describe_face_verify(endpoint, request)
                if UtilClient.equal_string('500', response.body.code):
                    continue
                return response.body
            except Exception:
                continue
        return None

    @staticmethod
    def describe_face_verify(
        endpoint: str,
        request: cloudauth_models.DescribeFaceVerifyRequest,
    ) -> cloudauth_models.DescribeFaceVerifyResponse:
        client = DescribeFaceVerify.create_client(endpoint)
        return client.describe_face_verify(request)


if __name__ == '__main__':
    init_result = InitFaceVerify.main(
        cert_name="杨森",
        cert_no="",
        meta_info=str(
            {
                "zimVer": "3.0.0",
                "appVersion": "1",
                "bioMetaInfo": "4.1.0:11501568,0",
                "appName": "com.aliyun.antcloudauth",
                "deviceType": "ios",
                "osVersion": "iOS 10.3.2",
                "apdidToken": "",
                "deviceModel": "iPhone9,1",
            }
        ),
        return_url='',
    )
    print(init_result)
    # print(DescribeFaceVerify.main(init_result.get("certify_id")))
