from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.groups import GroupMembersBase, GroupMembersUpdate
from app.src.service.group_memebers import GroupMembersService

# Service
router = BaseRouter(tags=["groups_members"])
groups_memebers_srv = GroupMembersService()


@router.post("/", summary="创建群成员")
async def create_members(req: GroupMembersBase):
    code, res = await groups_memebers_srv.create(req)
    if code != ErrorCode.SUCCESS:
        return code, None
    return res


@router.get("/search", summary="查找群成员")
async def get_members(group_id: int):
    return await groups_memebers_srv.get(group_id)


@router.put("/", summary="更新群成员信息")
async def update_user(req: GroupMembersUpdate):
    return await groups_memebers_srv.update_note(req)


@router.put("/admin", summary="更新管理员")
async def update_user(req: GroupMembersUpdate):
    return await groups_memebers_srv.update_admin(req)


@router.delete("/", summary="删除群成员")
async def delete_user(group_id: int, user_id: int):
    return await groups_memebers_srv.delete(group_id=group_id, user_id=user_id)
