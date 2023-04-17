#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field


# Shared properties
class WebPayOrderCreate(BaseModel):
    uid: str = Field(..., title="用户ID(环信的username)")
    group_id: int = Field(..., title="项目ID")
    level: int = Field(..., title="付费等级")


class WebPayOrderUpdate(BaseModel):
    order_id: str = Field(..., title="订单ID")
