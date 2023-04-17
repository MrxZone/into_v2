#!/usr/bin/env python
# -*- coding: utf-8 -*-


from qcloud_cos import CosConfig, CosS3Client

from app.core.config import settings

COS_RESOURCE_DOMAIN = (
    f"https://{settings.COS_BUCKET}.cos.{settings.COS_BUCKET_GLOBAL_CDN}.myqcloud.com/"
)
config = CosConfig(
    Region=settings.COS_BUCKET_REGION,
    SecretId=settings.COS_SECRETID,
    SecretKey=settings.COS_SECRETKEY,
)
client = CosS3Client(config)


def upload_file(file_path: str, file_name: str):
    response = client.upload_file(
        Bucket=settings.COS_BUCKET,
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False,
    )
    if response.get("ETag"):
        return COS_RESOURCE_DOMAIN + file_name
    return
