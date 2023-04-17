#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.routes.route import BaseRouter
from app.src.service.versions import VersionsService


router = BaseRouter(tags=["web"])

# Service
version_srv = VersionsService()


@router.get("/app_url", summary="")
async def register(ecosystem: str):
    version_info = await version_srv.get_version(
        version_code=0, release_channel="website", ecosystem=ecosystem
    )
    res = {}
    if version_info:
        res.update({version_info.ecosystem: version_info.new_app_download_url})
    return res
