#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pycommon.PLLogger import createLogger

TableBase = declarative_base()

# 数据库连接字符串示例
# oracle: oracle://apps:apps@10.0.0.100:1522/VID
# mysql: mysql://root:root@localhost:3306/new_db?charset=utf8
# sqlite: sqlite:///test.db
# mssql: mssql+pymssql://sa:123456@localhost:1433/test

class DBInstance(object):
    contract_session = None
    contract_engine = None
    logger = createLogger("datebase")

    @classmethod
    def connectionString(cls):
        connection = json.loads("configs.json", encoding="utf-8").get("Connection", "")
        DBInstance.logger.warn("Connection String:"+connection)
        return connection

    @classmethod
    def engine(cls):
        if cls.contract_engine is None:
            DBInstance.logger.debug("Database engine init......")
            cls.contract_engine = create_engine(DBInstance.connectionString(), echo=True)
        return cls.contract_engine

    @classmethod
    def session(cls):
        if cls.contract_session is None:
            DBInstance.logger.debug("Database session init......")
            DBSession = sessionmaker(bind=cls.engine())
            cls.contract_session = DBSession()
        return cls.contract_session

    @classmethod
    def initTables(cls):
        DBInstance.logger.debug("Init tables......")
        TableBase.metadata.create_all(bind=cls.engine())
        DBInstance.logger.debug("Init tables finished!")

    @classmethod
    def dropTables(cls):
        DBInstance.logger.debug("Drop tables......")
        TableBase.metadata.drop_all(bind=cls.engine())
        DBInstance.logger.debug("Drop tables finished!")

    @classmethod
    def init_db(cls, engine):
        DBInstance.logger.debug("init db!")
        TableBase.metadata.create_all(engine)

    @classmethod
    def drop_db(cls, engine):
        DBInstance.logger.debug("drop db!")
        TableBase.metadata.drop_all(engine)

    # 返回session, engine
    @classmethod
    def createEngine(cls, dbstring, reset=False):
        engine = create_engine(dbstring, echo=True)
        DBSession = sessionmaker(bind=engine)
        if reset:
            cls.init_db(engine)
        return DBSession()

    '''查询记录'''
    @classmethod
    def records(cls, type, cond=None):
        try:
            if cond is None or cond is "":
                rs = cls.session().query(type).all()
            else:
                rs = cls.session().query(type).filter(cond).all()
            return rs
        except Exception as e:
            DBInstance.logger.warn("DBInstance.records:"+str(e))
            return []

    '''联合查询'''
    @classmethod
    def unionRecords(cls, src_type, dest_type, cond):
        try:
            return cls.session().query(src_type, dest_type).filter(cond).all()
        except Exception as e:
            DBInstance.logger.warn("DBInstance.unionRecords:"+str(e))
            return []

    '''记录数量'''
    @classmethod
    def recordsCount(cls, type, cond=None):
        return len(cls.records(type, cond))

    '''记录是否存在'''
    @classmethod
    def isRecordExist(cls, type, cond):
        return (0 != cls.recordsCount(type, cond))

    '''添加或更新记录'''
    @classmethod
    def addOrRecord(cls, records):
        size = 0

        try:
            if isinstance(records, list):
                for record in records:
                    cls.session().merge(record)
                size = len(records)
            else:
                cls.session().merge(records)
                size = 1
            cls.session().commit()
        except Exception as e:
            DBInstance.logger.warn("DBInstance.addOrRecord:"+e)
            size = 0
            cls.session().rollback()

        DBInstance.logger.debug("Total {0} record added or updated!".format(size))
        return size

    '''删除纪录'''
    @classmethod
    def removeRecords(cls, t, conds=None):
        size = 0
        try:
            if conds is None:
                size = cls.session().query(t).delete(synchronize_session=False)
            else:
                size = cls.session().query(t).filter(conds).delete(synchronize_session=False)
            cls.session().commit()
        except Exception as e:
            DBInstance.logger.warn("DBInstance.removeRecords:" + str(e))
            size = 0
            cls.session().rollback()
        DBInstance.logger.debug("Total {0} record removed! [{1}]".format(size, type(t)))
        return size