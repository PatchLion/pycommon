#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pycommon.PLLogger import createLogger

TableBase = declarative_base()

# 数据库连接字符串示例
# oracle: oracle://apps:apps@10.0.0.100:1522/VID
# mysql: mysql://root:root@localhost:3306/new_db?charset=utf8
# sqlite: sqlite:///test.db
# mssql: mssql+pymssql://sa:Root123456@127.0.0.1:2796/BZQLYKT?charset=utf8

class DBInstance(object):
    LOGLEVEL = logging.DEBUG #日志级别
    ECHO = True #是否打印数据详情
    _contract_session = None
    _contract_engine = None
    _logger = None
    _connection_string = ""

    @classmethod
    def logger(cls):
        if cls._logger is None:
            cls._logger = createLogger("datebase", level=cls.LOGLEVEL)
        return cls._logger

    @classmethod
    def resetConnection(cls, connection):
        DBInstance.logger().debug("设置连接字符串:"+connection)
        cls._connection_string = connection
        cls._resetSession()

    @classmethod
    def _resetSession(cls):
        cls._contract_session = None
        cls._contract_engine = None

    @classmethod
    def engine(cls):
        if cls._contract_engine is None:
            DBInstance.logger().debug("Database engine init: " + cls._connection_string)
            cls._contract_engine = create_engine(cls._connection_string, echo=False)
        return cls._contract_engine

    @classmethod
    def session(cls):
        if cls._contract_session is None:
            DBInstance.logger().debug("Database session init......")
            DBSession = sessionmaker(bind=cls.engine())
            cls._contract_session = DBSession()
        return cls._contract_session

    @classmethod
    def initTables(cls):
        DBInstance.logger().debug("Init tables......")
        TableBase.metadata.create_all(bind=cls.engine())
        DBInstance.logger().debug("Init tables finished!")

    @classmethod
    def dropTables(cls):
        DBInstance.logger().debug("Drop tables......")
        TableBase.metadata.drop_all(bind=cls.engine())
        DBInstance.logger().debug("Drop tables finished!")

    @classmethod
    def init_db(cls, engine):
        DBInstance.logger().debug("init db!")
        TableBase.metadata.create_all(engine)

    @classmethod
    def drop_db(cls, engine):
        DBInstance.logger().debug("drop db!")
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
    def records(cls, type, cond=None, orderby=None):
        try:
            # DBLogger.logger().warn("Call records!")
            query = DBInstance.session().query(type)

            if cond is not None:
                # print("cond-->", cond)
                query = query.filter(cond)

            if orderby is not None:
                # print("orderby-->", orderby)
                query = query.order_by(orderby)

            # print("all")
            rs = query.all()

            # print("all finish")
            return rs
        except Exception as e:
            DBInstance.logger().warn("DBInstance.records: %s" % e)
            return []

    '''更新记录'''
    @classmethod
    def updateRecords(cls, type, cond, value):
        try:
            size = cls.session().query(type).filter(cond).update(value)
            DBInstance.logger().warn("update size---> %d" % size)
            cls.session().commit()
            return size
        except Exception as e:
            DBInstance.logger().warn("DBInstance.updateRecords: %s " % e)
            return 0


    '''联合查询'''
    @classmethod
    def unionRecords(cls, src_type, dest_type, cond):
        try:
            return cls.session().query(src_type, dest_type).filter(cond).all()
        except Exception as e:
            DBInstance.logger().warn("DBInstance.unionRecords: %s " % e)
            return []

    '''记录数量'''
    @classmethod
    def recordsCount(cls, type, cond=None):
        return len(cls.records(type, cond))

    '''记录是否存在'''
    @classmethod
    def isRecordExist(cls, type, cond=None):
        return (0 != cls.recordsCount(type, cond))

    '''添加或更新记录'''
    @classmethod
    def addOrRecord(cls, records):
        return cls.addRecord(records)

    '''添加或更新记录'''
    @classmethod
    def addRecord(cls, records):
        try:
            if isinstance(records, list):
                for record in records:
                    cls.session().merge(record)
                cls.session().commit()
                return len(records)
            else:
                cls.session().merge(records)
                cls.session().commit()
                return 1
        except Exception as e:
            DBInstance.logger().warn("DBInstance.addRecord: %s" % e)
            cls.session().rollback()
            return 0

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
            DBInstance.logger().warn("DBInstance.removeRecords: %s" % e)
            size = 0
            cls.session().rollback()
        DBInstance.logger().debug("Total {0} record removed! [{1}]".format(size, type(t)))
        return size