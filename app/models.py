from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, create_engine, Boolean
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


def create_table(eg: Engine) -> None:
    SQLModel.metadata.create_all(eg)