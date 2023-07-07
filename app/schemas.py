from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class LimitedResponse(BaseModel):
    title: str
    content: str
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserCreate):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    bearer: str

class TokenData(BaseModel):
    email: EmailStr
        
            