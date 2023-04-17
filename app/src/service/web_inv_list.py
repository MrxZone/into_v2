#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

from app.core.into_web3 import IntoWeb3
from app.crud import we3_pay_order
from app.db.redis_db import redis_cache
from app.db.session import async_session
from app.settings.web3 import WebSettings

# from app.src.common.loggers import logger

_db = async_session.init()


# 根据级数获取用户子级
async def get_inv_list(contract_name, contract_address, items, level, count):
    # contract_name = "BSCRelation"
    config = WebSettings.get_contract_address(contract_name)
    contract = IntoWeb3.init_contract(contract_name, config[1], config[0])
    data = contract.functions.getInvListWithLevel(
        contract_address, IntoWeb3.to_checksum_address(items), level, count
    ).call()

    return data


# 批量获取用户的Uids
async def get_uids_with_address(items=None):
    contract_name = "IntoBind"
    if not items:
        return []

    if not items:
        return []

    config = WebSettings.get_contract_address(contract_name)
    contract = IntoWeb3.init_contract(contract_name, config[1], config[0])
    data = contract.functions.getUidsWithAddress(
        IntoWeb3.to_checksum_address(items)
    ).call()
    return data


# 批量获取用户的支付订单
async def get_order_with_uid(uid, group_id):
    contract_name = "IntoPay"
    config = WebSettings.get_contract_address(contract_name)
    contract = IntoWeb3.init_contract(contract_name, config[1], config[0])
    data = contract.functions.getGroupOrder(uid, group_id).call()
    return data


# 根据级别获取需要的数据,最多1000条
async def get_inv_address_with_level(
    contract_name: str, contract_address: str, address: str, level: int
):
    start = time.time()
    count = 200
    if level == 5:
        count = 500
    if level == 10:
        count = 1000
    childs = await get_inv_list(
        contract_name, contract_address, [address], level, count
    )
    # logger.debug(f"childs is {len(childs)}")
    # logger.debug(f"时间1 是{time.time()-start}")
    childs = [o for o in childs if o != "0x0000000000000000000000000000000000000000"]
    # start_1 = time.time()
    uids = await get_uids_with_address(childs)
    # logger.debug(f"uids len is {len(uids)}")
    # logger.debug(f"时间2 是{time.time()-start}")
    uids = [id for id in uids if id]
    return len(childs), len(uids), list(set(uids))


async def get_inv_address(contract_name: str, contract_address: str, address: str):
    redis_client = redis_cache.client
    key = f"inv_{contract_name}_{contract_address}_{address}"
    res = await redis_client.get(key)
    # print("res is",res)
    if res:
        return eval(res)

    items = []
    for index in [1, 5, 10]:
        # logger.debug(f"index is {index}")
        addr_count, uids_count, uids = await get_inv_address_with_level(
            contract_name, contract_address, address, index
        )

        items.append(
            dict(
                level=index,
                addr_count=addr_count,
                uids_count=uids_count,
                uids=uids,
                usdt=0,
            )
        )

    await redis_client.set(key, str(items), ex=600)
    return items


# 获取层级需要的USDT
async def get_level_usdt_with_contract():
    contract_name = "IntoPay"
    config = WebSettings.get_contract_address(contract_name)
    contract = IntoWeb3.init_contract(contract_name, config[1], config[0])
    data = contract.functions.getPayLevelFee().call()

    return data


# 用户最后支付的订单id是否相等
async def get_usdt(group_id: int, uid: str):
    orders = await get_pay_orders(uid, group_id)
    usdts = await get_level_usdt_with_contract()
    level5 = 10 * 10 ** 18
    level10 = 20 * 10 ** 18
    if usdts:
        level5 = usdts[0]
        level10 = usdts[1]
    item = {
        "5": {"usdt": level5, "pay_type": "unpaid"},
        "10": {"usdt": level10, "pay_type": "unpaid"},
        "1": {"usdt": 0, "pay_type": "unpaid"}
    }
    if not orders:
        return item
    payOrders = await we3_pay_order.get_items_by_params(
        _db, dict(group_id=group_id, uid=uid)
    )

    for o in payOrders:
        next_order_id = await get_next_pay_order_id(o.level, o.order_id, orders)
        if o.order_id != next_order_id:
            item[str(o.level)] = {"usdt": 0, "pay_type": "paid"}
    return item


# 获取用户的支付订单列表
async def get_pay_orders(uid: str, group_id: int):
    orders = await get_order_with_uid(uid, group_id)
    # logger.debug("*"*100)
    # logger.debug(orders)
    return orders


async def get_next_pay_order_id(level: int, used_order_id: str, orders=None):
    if not orders:
        return ""

    keys = [f"{o[0]}_{o[2]}_{o[3]}_{o[5]}" for o in orders if o[3] == level]

    if not keys:
        return ""

    if not used_order_id:
        return keys[0]

    if used_order_id == keys[-1]:
        return used_order_id

    count = keys.index(used_order_id)
    return keys[count + 1]


# 通过已经使用过的order获取下一个order_id
async def get_pay_order_id(uid, group_id, level, used_order_id):
    orders = await get_pay_orders(uid, group_id)
    next_order_id = await get_next_pay_order_id(level, used_order_id, orders)
    return next_order_id
