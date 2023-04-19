from sqlalchemy import BigInteger, Column, String, text, DateTime, func, Integer
from app.db.base_class import Base


class Users(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    uid: str = Column(String, unique=True, index=True, nullable=False)
    username: str = Column(String)
    password: str = Column(String)
    avatar: str = Column(String)
    nickname: str = Column(String(20))
    bio: str = Column(String(200))
    phone: str = Column(String, unique=True, index=True, nullable=False)
    country: str = Column(String)
    union_id: str = Column(String)
    open_id: str = Column(String)
    regist_time: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    regist_ip: str = Column(String)
    login_time: DateTime = Column(DateTime(timezone=True), onupdate=func.now())
    login_ip: str = Column(String)

    def __repr__(self):
        return "{}".format(self.__tablename__)

    def dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "username": self.username,
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "phone": self.phone,
            "country": self.country
        }


