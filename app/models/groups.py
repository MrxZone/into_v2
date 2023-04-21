from sqlalchemy import BigInteger, Column, String, text, DateTime, func, Integer, Boolean
from app.db.base_class import Base


class Group(Base):
    __tablename__ = "groups"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String)
    note: str = Column(String(20))


class GroupMembers(Base):
    __tablename__ = "group_members"
    id: int = Column(Integer, primary_key=True, index=True)
    group_id: int = Column(Integer)
    user_id: int = Column(Integer)
    note: str = Column(String(20))
    is_admin: bool = Column(Boolean, default=False, server_default=text("false"))
