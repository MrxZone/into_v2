#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Optional

from fastapi import Header, HTTPException, status

from app.src.jwt_token import verify


class WriteRequired:
    async def __call__(self, x_into_token: str = Header(...)) -> Optional[str]:
        if not x_into_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        if await verify(x_into_token):
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_411_LENGTH_REQUIRED, detail="Authenticate fail！"
            )

        return x_into_token
