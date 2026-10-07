from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Boolean, Relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import Engine

class Posts(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: Optional[bool] = Field(sa_column=Column(Boolean,server_default='TRUE', 
                                             nullable=False))
    created_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), 
                                            server_default=text("CURRENT_TIMESTAMP"),
                                            nullable=False))
    user_id: int =  Field(nullable=False,foreign_key="users.id",ondelete="CASCADE")

    user: "Users" = Relationship(back_populates="posts")

class Users(SQLModel, table=True):
    id: int | None = Field(default = None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    phone_number: str
    created_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True),
                                                             server_default=text("CURRENT_TIMESTAMP"),
                                                             nullable=False))

    posts: list["Posts"] = Relationship(back_populates="user")

class Votes(SQLModel, table=True):
    user_id: int = Field(nullable=False, primary_key=True, foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(nullable=False, primary_key=True, foreign_key="posts.id", ondelete="CASCADE")

def create_table(eg: Engine) -> None:
    SQLModel.metadata.create_all(eg)