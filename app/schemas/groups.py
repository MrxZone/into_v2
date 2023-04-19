from typing import Optional, Any, List

from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str
    note: Optional[str] = Field(max_length=20)


class GroupCreate(GroupBase):
    user_id: Optional[int]


class GroupUpdate(GroupBase):
    id: int


class Users(BaseModel):
    id: int
    note: Optional[str] = Field(max_length=20)


class GroupMembersBase(BaseModel):
    group_id: int
    users: List[Users]


class GroupMembersUpdate(BaseModel):
    group_id: int
    user_id: int
    note: Optional[str] = Field(max_length=20)
    is_admin:  Optional[bool]
