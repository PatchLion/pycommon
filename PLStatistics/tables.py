#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycommon.PLDatabase import TableBase
from sqlalchemy import *
from pycommon.PLCommons.functions import uuid64


#统计权限Keys
class StatisticsKeys(TableBase):
    __tablename__ = "StatisticsKeys"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    keyvalue = Column(String(64), unique=True, default=uuid64())


#页面统计表
class ViewStatistics(TableBase):
    __tablename__ = "ViewStatistics"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    page = Column(String(2048), nullable=False) #页面路径
    title = Column(String(256), nullable=False) #页面标题
    appversion = Column(String(24), nullable=False) #app版本
    clientid = Column(String(24), nullable=False) #客户端id
    datetime = Column(INTEGER(), nullable=False) #日期


#事件统计表
class EventStatistics(TableBase):
    __tablename__ = "EventStatistics"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    category = Column(String(256), nullable=False) #事件类型
    action = Column(String(256), nullable=False) #事件活动
    label = Column(String(256), nullable=True, default="") #标签备注
    appversion = Column(String(24), nullable=False) #app版本
    clientid = Column(String(24), nullable=False) #客户端id
    datetime = Column(INTEGER(), nullable=False) #日期