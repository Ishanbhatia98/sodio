import os
from typing import Callable
import urllib.parse

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, Session, sessionmaker


class DatabaseInstance:
    _base: DeclarativeMeta = None

    def __init__(self):
        self._base = declarative_base()
        self._engine = create_engine(
            self.get_database_url(),
        )
        self._session_maker = sessionmaker(autocommit=False, bind=self._engine)

    @property
    def base(self) -> DeclarativeMeta:
        return self._base

    @staticmethod
    def get_database_url() -> str:
        DATABASE_URL = "sqlite:///shortener.db"
        return DATABASE_URL 
    
    def initialize_session(self) -> Session:
        return self._session_maker()

    def delete_all_tables_and_metadata(self):
        # Get a session from the session maker
        session = self.initialize_session()

        # Reflect all tables and drop the entire schema
        self.base.metadata.drop_all(self._engine)

        # Commit the changes and close the session
        session.commit()
        session.close()


db_instance = DatabaseInstance()



def get_db_session():
    if hasattr(get_db_session, "_session") and not get_db_session._session.is_active:
        return get_db_session._session
    session = db_instance.initialize_session()
    get_db_session._session = session
    return session

def db_session_wrapper(func: Callable):
    async def wrapped_func(*args, **kwargs):
        async with get_db_session() as session:
            return await func(*args, **kwargs)

    return wrapped_func