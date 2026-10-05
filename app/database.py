from sqlmodel import create_engine, Session, select
import models
from config import settings
from typing import Annotated
from fastapi import Depends

# 'postgresql://<username>:<password>@<ip-address/hostname>:<database_portnumber>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

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