from sqlalchemy import BigInteger, Column, String, text, DateTime, func, Integer, Boolean, JSON
from app.db.base_class import Base


class Relation(Base):
    __tablename__ = "relation"
    id: int = Column(Integer, primary_key=True, index=True)
    owner_id: int = Column(Integer)
    another_id: int = Column(Integer)
    note: str = Column(String(20))
    describe: str = Column(String(200))
    # 因为他允许给陌生人加备注 所有1是陌生人，0是好友 莫名其妙的给陌生人加备注
    type: int = Column(Integer, default=0)
    # todo 预留字段是否让他看
    is_exposed: bool = Column(Boolean, default=True, server_default=text("true"))
    # todo 预留字段是否看他
    is_view: bool = Column(Boolean, default=True, server_default=text("true"))


class RelationJson(Base):
    __tablename__ = "relation_json"
    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer)
    data = Column(JSON)
