import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta


sqlite_file_name: str = "../database.sqlite"
base_dir: str = os.path.dirname(os.path.realpath(__file__))

database_url: str = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

engine: Engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
