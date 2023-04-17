#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import Request, APIRouter

from app.core.config import settings
from app.routes.route import log_stuff
from app.src.common.easemob.event import factory
from app.src.common.easemob.handler import (
    roster_accept,
    muc_create,
    chat_group_text,
    chat_group_image,
    chat_group_voice,
    chat_group_video,
    chat_group_file,
)
from app.src.common.loggers import logger

router = APIRouter(tags=["open"], route_class=log_stuff)


@router.post("/callback/forward", summary="")
async def callback_forward(request: Request):
    # todo: finish this in the future
    body = await request.json()
    return {
        "valid": True,
    }


@router.post("/callback/behind")
async def callback_behind(request: Request):
    body = await request.json()
    if body.get("eventType") is None:
        return {
            "valid": False,
        }

    # event
    # filter secret key
    event = factory(body).set_secret(settings.EASEMOB_CALLBACK_1)
    event.register(roster_accept)
    event.register(muc_create)

    event.register(chat_group_text)
    event.register(chat_group_image)
    event.register(chat_group_voice)
    event.register(chat_group_video)
    event.register(chat_group_file)
    # event.register(muc_presence)
    try:
        await event.call_func()
    except Exception as e:
        logger.info(e)

    return {
        "valid": True,
    }
