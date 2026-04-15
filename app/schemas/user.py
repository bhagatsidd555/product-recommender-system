from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: Optional[int]
    gender: Optional[str]
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True