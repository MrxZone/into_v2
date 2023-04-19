from typing import Optional, Any, List

from pydantic import BaseModel, Field


class RelationBase(BaseModel):
    owner_id: int
    another_id: int
    note: Optional[str] = Field(max_length=20)
    describe: Optional[str] = Field(max_length=200)


class RelationUpdate(RelationBase):
    id: int


class RelationJSONBase(BaseModel):
    user_id: int
    data: str

# class RelationJSONUpdate(RelationJSONBase):
#     id: int
