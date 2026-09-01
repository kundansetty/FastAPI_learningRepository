from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}/{os.environ["DB_NAME"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]