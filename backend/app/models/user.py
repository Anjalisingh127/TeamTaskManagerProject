from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum


class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    #role = Column(Enum(Role), default=Role.MEMBER)
    role = Column(String, default="MEMBER")