#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime, text
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# from db.session import AsyncBase


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return "t_" + cls.__name__.lower()

    deleted = Column(Boolean, default=False, server_default=text("false"), index=True)
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(),
        server_default=text("NOW()"),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(),
        server_default=text("NOW()"),
        onupdate=lambda: datetime.now(),
    )
