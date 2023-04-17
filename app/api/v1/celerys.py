#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.src.common.auth_jwt import WriteRequired
from app.src.service.celery_service import celery_result, test

router = BaseRouter(tags=["celery"])


@router.get("/celery_result_by_id", summary="查单个task_id")
async def get(task_id: str, token: int = Depends(WriteRequired())):
    return ErrorCode.SUCCESS, jsonable_encoder(celery_result(task_id))


@router.post("/celery_result_by_ids", summary="查多个task_id")
async def get(task_id: list, token: int = Depends(WriteRequired())):
    res = [celery_result(i) for i in task_id]
    return ErrorCode.SUCCESS, jsonable_encoder(res)


@router.post("/celery_result", summary="did task result")
async def get(task_id: list, token: int = Depends(WriteRequired())):
    res = []
    for i in task_id:
        re_dic = dict(chain_id=i.get("chain_id"))
        re_dic.update(celery_result(i.get("task_id")))
        res.append(re_dic)
    return ErrorCode.SUCCESS, jsonable_encoder(res)


@router.get("/test", summary="celery_test")
async def get(token: int = Depends(WriteRequired())):
    return ErrorCode.SUCCESS, jsonable_encoder(test())
