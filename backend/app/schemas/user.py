import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: uuid.UUID
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[uuid.UUID] = None
    email: Optional[str] = None


class ChildBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    preferred_language: str = "en"


class ChildCreate(ChildBase):
    birth_date: Optional[str] = None


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    preferred_language: Optional[str] = None
    avatar_url: Optional[str] = None


class ChildResponse(ChildBase):
    id: uuid.UUID
    user_id: uuid.UUID
    birth_date: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
