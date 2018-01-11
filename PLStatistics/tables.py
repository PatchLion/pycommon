#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PLDatabase import TableBase
from sqlalchemy import *

#统计权限Keys
class StatisticsKeys(TableBase):

    __tablename__ = "StatisticsKeys"
    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    key = Column(String(32), nullable=False) #key


#页面统计表
class ViewStatistics(TableBase):
    __tablename__ = "ViewStatistics"

    id = Column(String(32), primary_key=True)  # id
    page = Column(String(2048), nullable=False) # 页面路径
    title = Column(String(256), nullable=False) # 页面标题
    appversion = Column(String(32), nullable=False) # app版本
    clientid = Column(String(32), nullable=False) #客户端id
    datetime = Column(INTEGER(), nullable=False) #日期


#事件统计表
class EventStatistics(TableBase):
    __tablename__ = "EventStatistics"

    id = Column(String(32), primary_key=True)  # id
    category = Column(String(32), nullable=False) #事件类型
    action = Column(String(32), nullable=False) #事件活动
    label = Column(String(1024), nullable=True, default="") #标签备注
    appversion = Column(String(32), nullable=False) # app版本
    clientid = Column(String(32), nullable=False) #客户端id
    datetime = Column(INTEGER(), nullable=False) #日期