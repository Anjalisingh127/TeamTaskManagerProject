from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.MEMBER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str