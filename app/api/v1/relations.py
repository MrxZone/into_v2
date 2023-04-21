from typing import Union

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.relations import RelationBase
from app.src.service.relations import RelationService

# Service
router = BaseRouter(tags=["relation"])
relation_srv = RelationService()


@router.post("/", summary="创建关系")
async def create_relation(req: RelationBase):
    code, res = await relation_srv.create(req)
    if code != ErrorCode.SUCCESS:
        return code, None
    return res


@router.get("/search", summary="查找关系")
async def get_relation(
        owner_id: int
):
    return await relation_srv.get_relations(owner_id = owner_id)


@router.put("/", summary="更新关系信息")
async def update_relation(req: RelationBase):
    return await relation_srv.update(req)


@router.delete("/", summary="删除关系")
async def delete_relation(
        owner_id: int,
        another_id: int
):
    return await relation_srv.delete(owner_id=owner_id, another_id=another_id)
