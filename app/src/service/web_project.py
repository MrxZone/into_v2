#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO(Req): using class object
from fastapi.encoders import jsonable_encoder

from app.crud import we3_pay_order, web3_project
from app.db.session import async_session
from app.schemas.web_project import WebPayOrderCreate, WebPayOrderUpdate
from app.src.service.web_inv_list import (get_inv_address, get_pay_order_id,
                                          get_usdt)

_db = async_session.init()


async def get_projects():
    projects = await web3_project.get_web_projects(_db)
    return [jsonable_encoder(o) for o in projects]


async def get_inv_list(web_project_id, address, uid):
    project = await web3_project.get_web_project(_db, web_project_id)
    # start = time.time()
    items = await get_inv_address(project.web_name, project.address, address)
    # logger.debug(f"items is {time.time() - start}")
    # start = time.time()
    usdts = await get_usdt(web_project_id, uid)
    # logger.debug(f"usdts is {time.time() - start}")
    for item in items:
        item.update(usdts[str(item.get("level"))])
        # item["usdt"] = usdts.get(str(item.get("level")))

    return items


async def pay_order(req: WebPayOrderCreate):
    order = await we3_pay_order.get_or_create(_db, req)
    new_order_id = await get_pay_order_id(
        req.uid, req.group_id, req.level, order.order_id
    )
    if new_order_id != order.order_id:
        item = WebPayOrderUpdate(order_id=new_order_id)
        await we3_pay_order.update(_db, db_obj=order, obj_in=item)
