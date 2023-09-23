import os

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.future import Engine


sqlite_file_name: str = "../database.sqlite"
base_dir: str = os.path.dirname(os.path.realpath(__file__))

database_url: str = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

engine: Engine = create_engine(database_url, echo=True)
Connection = Session(bind=engine)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
