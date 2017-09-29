#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Webs.ContractServer.settings import *
from Projects.Webs.ContractServer.database import TableBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, String, INTEGER, ForeignKey, Float, BOOLEAN


class ContractDB(object):
    contract_session = None
    contract_engine = None

    @classmethod
    def engine(cls):
        if cls.contract_engine is None:
            print("Database engine init......")
            cls.contract_engine = create_engine(DB_STRING, echo=True)
        return cls.contract_engine

    @classmethod
    def session(cls):
        if cls.contract_session is None:
            print("Database session init......")
            DBSession = sessionmaker(bind=cls.engine())
            cls.contract_session = DBSession()
        return cls.contract_session

    @classmethod
    def initTables(cls):
        print("Init tables......")
        TableBase.metadata.create_all(bind=cls.engine())
        print("Init tables finished!")

    @classmethod
    def dropTables(cls):
        print("Drop tables......")
        TableBase.metadata.drop_all(bind=cls.engine())
        print("Drop tables finished!")

#用户表
class User(TableBase):
    __tablename__ = "User"

    id = Column(INTEGER(), primary_key=True, autoincrement=True) #id
    user_name = Column(String(256), unique=True, nullable=False) #用户名
    password = Column(String(256), nullable=False) #密码
    nick_name = Column(String(256), nullable=True) #昵称
    company_id = Column(INTEGER(), nullable=True, default=-1) #公司id
    role_id = Column(INTEGER(), nullable=True, default=-1) #角色id

#角色表
class Role(TableBase):
    __tablename__ = "Role"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False) #角色名称

#角色权限表
class RoleAuth(TableBase):
    __tablename__ = "RoleAuth"

    id = Column(INTEGER(), primary_key=True, autoincrement=True) #id
    role_id = Column(INTEGER(), nullable=False) #角色id
    auth = Column(INTEGER(), nullable=False) #权限


#用户权限表
class UserAuth(TableBase):
    __tablename__ = "UserAuth"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    user_id = Column(INTEGER(), nullable=False) #用户id
    auth = Column(INTEGER(), nullable=False) #权限


#公司表
class Company(TableBase):
    __tablename__ = "Company"

    id = Column(INTEGER(), primary_key=True, autoincrement=True) #id
    name = Column(String(256), unique=True, nullable=False) #公司名称

#项目表
class Project(TableBase):
    __tablename__ = "Project"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False)  #工程名称
    money = Column(INTEGER(), nullable=True, default=-1) #项目总投资金额
    rate_of_profit = Column(Float(), nullable=True, default=0.1) #项目利润率
    start_date = Column(INTEGER(), nullable=True, default=-1) #项目开始日期，时间戳
    last_date = Column(INTEGER(), nullable=True, default=-1) #项目到期日期，时间戳
    #first_approve_user_id = Column(INTEGER(), nullable=True, default=-1) #首次审批用户
    #second_approve_user_id = Column(INTEGER(), nullable=True, default=-1) #第二次审批用户

#审批申请表
class AskApprove(TableBase):
    __tablename__ = "AskApprove"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    project_id = Column(INTEGER(), nullable=False)  #项目id
    user_id = Column(INTEGER(), nullable=False)  #用户id
    is_first = Column(BOOLEAN(), nullable=False)  #是否是首次审批
    is_pass = Column(BOOLEAN(), nullable=True, default=False)  #是否通过审批

#文件上传记录
class File(TableBase):
    __tablename__ = "File"

    id = Column(INTEGER(),primary_key=True, autoincrement=True)  #id
    contract_id = Column(INTEGER(),nullable=False)  #合同id
    classify = Column(String(256),nullable=False) #分类
    name = Column(String(256),nullable=False) #名称
    note = Column(String(256), nullable=True) #备注

#合同表
class Contract(TableBase):
    __tablename__ = "Contract"

    id = Column(INTEGER(),primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False) #合同名称
    project_id = Column(INTEGER(), nullable=False) #项目id
    company_id = Column(INTEGER(), nullable=False) #公司id
    retention_money = Column(INTEGER(), nullable=True, default=-1) #质保金额
    retention_money_date = Column(INTEGER(), nullable=True, default=-1) #质保金期限, 时间戳
    parent_contract_id = Column(INTEGER(),nullable=True, default=-1) #父合同ID -1为没有父合同
    money = Column(INTEGER(), nullable=False, default=0) #资金
    progress = Column(INTEGER(), default=0)  # 进度 0 - 100
    pay_money = Column(INTEGER(), nullable=False,default=0) #已支付款项
    second_party_name = Column(String(256), nullable=False) #乙方名称
    place_of_performance = Column(String(256), nullable=True) #履行地点
    date_of_performance = Column(String(256), nullable=True) #履行期限
    type_of_performance = Column(String(256), nullable=True) #履行方式
    note = Column(String(256), nullable=True, ) #备注

#合同进度记录表
class ContractHistory(TableBase):
    __tablename__ = "ContractsHistory"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    contract_id = Column(INTEGER(), nullable=False) #合同ID
    progress = Column(INTEGER(), default=0) #进度 0 - 100
    pay_money = Column(INTEGER(), default=0) #已支付款项
    datetime = Column(INTEGER(), nullable=False) #创建时间
    note = Column(String(256), nullable=True, ) #备注

