from typing import Union

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.groups import GroupUpdate, GroupBase, GroupCreate
from app.src.service.groups import GroupService

# Service
router = BaseRouter(tags=["groups"])
groups_srv = GroupService()


@router.post("/", summary="创建群")
async def create_group(req: GroupCreate):
    code, res = await groups_srv.create(req)
    if code != ErrorCode.SUCCESS:
        return code, None
    return res


@router.get("/search", summary="查找群")
async def get_group(id: int):
    return await groups_srv.get_group(id)


@router.put("/", summary="更新群信息")
async def update_user(req: GroupUpdate):
    return await groups_srv.update(req)


@router.delete("/", summary="删除群")
async def delete_user(id: int):
    return await groups_srv.delete(id=id)
