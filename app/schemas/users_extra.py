from typing import Optional, Any, List

from pydantic import BaseModel, Field


class UsersBase(BaseModel):
    uid: Optional[str]
    username: str
    nickname: Optional[str] = Field(max_length=20)
    country: Optional[str]
    phone: str
    # union_id: Optional[str]
    # open_id: Optional[str]


class UsersCreate(UsersBase):
    password: Optional[str]
    regist_ip: Optional[str]


class UsersUpdate(UsersBase):
    id: Optional[int]
    avatar: Optional[str]
    bio: Optional[str] = Field(max_length=200)
    login_ip: Optional[str]

