from abc import ABC
from sqlalchemy.orm import sessionmaker, Session

class AbstractRepository(ABC):

    def __init__(self, session_factory: sessionmaker):
        self.__session_factory = session_factory

    def get_session(self)-> Session:
        return self.__session_factory() 