from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None

class UserOut(UserBase):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
