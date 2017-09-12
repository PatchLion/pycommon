from SqlAlchemy.EngineCreator import *
from sqlalchemy import *

class User(TableBase):
    __tablename__ = "user"

    id = Column(String(20), primary_key=True)
    name = Column(String(20))