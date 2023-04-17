#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .crud_key import keys
from .crud_pay_order import we3_pay_order
from .crud_user import users
from .crud_verifications import verifications
from .crud_web_project import web3_project
from .crud_versions import versions
from .crud_faucet_bind import faucet_bind

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
