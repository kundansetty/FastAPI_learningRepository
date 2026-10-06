from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Literal


#User related Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str


#Token Related Schema
class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


#Post related Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # user: UserResponse

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

class PostOut(BaseModel):
    title: str
    content: str
    created_at: datetime
    id: int
    published: bool
    user_id: int

class PostVoteResponse(BaseModel):
    Posts: PostOut
    votes: int

#Vote related Schema
class Vote(BaseModel):
    post_id : int
    dir: Literal[0, 1]