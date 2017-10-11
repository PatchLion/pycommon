#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

TableBase = declarative_base()

def init_db(engine):
    print("init db!")
    TableBase.metadata.create_all(engine)

def drop_db(engine):
    print("drop db!")
    TableBase.metadata.drop_all(engine)

#返回session, engine
def createEngine(dbstring, reset = False):
    engine = create_engine(dbstring, echo=True)
    #engine = create_engine(dbstring, echo=True)
    DBSession = sessionmaker(bind=engine)
    if reset:
        init_db(engine)
    return DBSession()
