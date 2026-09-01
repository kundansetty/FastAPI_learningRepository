from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text
from datetime import datetime
from typing import Optional
from database import engine

class Posts(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True, nullable=False)
    created_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), 
                                            server_default=text("CURRENT_TIMESTAMP"),
                                            nullable=False))


def create_table():
    SQLModel.metadata.create_all(engine)