from typing import Union

from app.core.ecode import ErrorCode
from app.routes.route import BaseRouter
from app.schemas.users_extra import UsersCreate, UsersUpdate
from app.src.service.users_extra import UsersService

# Service
router = BaseRouter(tags=["users"])
user_srv = UsersService()


@router.post("/", summary="创建用户")
async def create_user(req: UsersCreate):
    code, res = await user_srv.create(req)
    if code != ErrorCode.SUCCESS:
        return code, None
    return res


@router.get("/search", summary="查找用户")
async def get_user(
        user_name: Union[str, None] = None,
        uid: Union[str, None] = None,
        phone: Union[str, None] = None,
):
    return await user_srv.get_user(user_name=user_name, user_uid=uid, user_phone=phone)

@router.get("/", summary="查找全部用户")
async def get_users():
    return await user_srv.get_users()

@router.put("/", summary="更新用户信息")
async def update_user(req: UsersUpdate):
    return await user_srv.update(req)


@router.delete("/", summary="删除用户")
async def delete_user(
        id: Union[int, None] = None,
        user_name: Union[str, None] = None,
        uid: Union[str, None] = None,
        phone: Union[str, None] = None,
):
    return await user_srv.delete(id=id, uid=uid, phone=phone, username=user_name)
