from sqlmodel import create_engine, Session, select
import models
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}/{os.environ["DB_NAME"]}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine, autocommit=False, autoflush=False) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]

def main():
    with Session(engine, autocommit=False, autoflush=False) as session1, Session(engine, autocommit=False, autoflush=False) as session2:
        print(session1.exec(select(models.Posts)).all())
        new_post = models.Posts(title="FifthPost", content="Fifthcontent")
        session2.add(new_post)
        print(session2.exec(select(models.Posts)).all())
        # session2.commit()
        statement = select(models.Posts)
        posts = session1.exec(statement=statement).all()
        print(posts)

if __name__ == '__main__':
    main()