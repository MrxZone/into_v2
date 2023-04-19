import json
from typing import List

import app.crud as crud
from app.core.ecode import ErrorCode
from app.db.session import async_session
from app.schemas.relations import RelationBase, RelationJSONBase
from app.src.common import EMPTYDATA
from app.src.common.singleton import Singleton


class RelationJSONService(Singleton):
    def __init__(self) -> None:
        self.db = async_session.init()
        self.crud = crud.relation_json

    def __decode(self, user_id: int, data: str) -> List[RelationBase]:
        out = []
        ret = json.loads(data)
        for i in ret:
            out.append(RelationBase(owner_id=user_id, another_id=i.get('a_id'), note=i.get('note'),
                                    describe=i.get('describe')))
        return out

    def __find(self, user_id: int, data: str, another_id) -> RelationBase:
        ret = json.loads(data)
        for i in ret:
            if i.get('a_id') == another_id:
                return RelationBase(owner_id=user_id, another_id=i.get('a_id'), note=i.get('note'),
                                    describe=i.get('describe'))
        return None

    def __to_json_str(self, req: RelationBase) -> str:
        return json.dumps([{
            "a_id": req.another_id,
            "note": req.note,
            "describe": req.describe
        }])

    def __delete_json(self, data: str, another_id: int) -> str:
        ret = json.loads(data)
        out = []
        for i, r in enumerate(ret):
            if r.get('a_id') != another_id:
                out.append(r)
        return json.dumps(out)

    def __update_json(self, data: str, req: RelationBase) -> str:
        ret = json.loads(data)
        count = 0
        for r in ret:
            if r.get('a_id') == req.another_id:
                r['note'] = req.note
                r['describe'] = req.describe
                break
            count += 1
        if count == len(ret):
            ret.append({
                "a_id": req.another_id,
                "note": req.note,
                "describe": req.describe
            })
        return json.dumps(ret)

    async def create(self, req: RelationBase):
        relation = await self.crud.get(self.db, user_id=req.owner_id)
        if not relation:
            obj_in = self.__to_json_str(req)
            data = await self.crud.create(self.db, obj_in=RelationJSONBase(user_id=req.owner_id, data=obj_in))
            if data:
                return ErrorCode.SUCCESS, data
            else:
                return ErrorCode.NOT_EXIST, EMPTYDATA
        else:
            return await self.update(req)

    async def update(self, req: RelationBase):
        relation = await self.crud.get(self.db, user_id=req.owner_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        obj_in = RelationJSONBase(user_id=req.owner_id, data=self.__update_json(data=relation.data,req=req))
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=relation, obj_in=obj_in)

    async def delete(self, user_id: int, another_id: int):
        relation = await self.crud.get(self.db, user_id=user_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        obj_in = RelationJSONBase(user_id=user_id, data=self.__delete_json(data=relation.data, another_id=another_id))
        return ErrorCode.SUCCESS, await self.crud.update(self.db, db_obj=relation, obj_in=obj_in)

    async def get_relations(self, user_id):
        relation = await self.crud.get(self.db, user_id=user_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        return ErrorCode.SUCCESS, self.__delete_json(another_id=user_id, data=relation.data)

    async def get_relation(self, user_id: int, another_id: int):
        relation = await self.crud.get(self.db, user_id=user_id)
        if not relation:
            return ErrorCode.NOT_EXIST, EMPTYDATA
        ret = self.__find(user_id, relation.data, another_id=another_id)
        if ret:
            return ErrorCode.SUCCESS, ret
        return ErrorCode.NOT_EXIST, EMPTYDATA
