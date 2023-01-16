import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Session

Base = declarative_base()
SQLModel.metadata = Base.metadata


def engine():
    if os.getenv('DATABASE_URL') is None:
        raise EnvironmentError("Don't find DATABASE_URL env value")
    return create_engine(os.getenv('DATABASE_URL'))


def init_db():
    SQLModel.metadata.create_all(engine())


def get_session():
    with Session(engine()) as session:
        yield session
