from sqlalchemy import *

from DBOperator.EngineCreator import *


class User(TableBase):
    __tablename__ = "user"

    id = Column(String(20), primary_key=True)
    name = Column(String(20))