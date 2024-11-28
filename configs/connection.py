import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class  DBConnectionHandler():

    def __init__(self) -> None:
        self.__connection_string = f"sqlite:///{self.get_database_path()}"
        self.__engine = self.__create_database_engine()
        self.session = None

    def get_database_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            db_path = os.path.join(base_path, "_internal", "rpg_db")
        else:
            base_path = os.path.abspath(".")
            db_path = os.path.join(base_path, "rpg_db")
        return db_path


    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()



