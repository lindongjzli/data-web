from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="User's username")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User's password")

class UserInDB(UserBase):
    hashed_password: str = Field(..., description="Hashed password for storage")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
