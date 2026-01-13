from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    username: str
    age: int
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 64:
            raise ValueError("Password too long")
        return v
    
    @validator("username")
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

class UserResponse(BaseModel):
    username: str
    age: int
    email: str

class UserUpdate(BaseModel):
    age: int
    email: str

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[UserResponse] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
