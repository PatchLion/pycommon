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
    __tablename__ = "user"

    user_id = Column(String(256), primary_key=True) #用户ID
    password = Column(String(256), nullable=False) #密码
    name = Column(String(256), nullable=False) #名称
    authority_id = Column(INTEGER(), nullable=True, default=-1) #权限 -1为没有任何权限
    company_id = Column(INTEGER(), nullable=True, default=-1) #所属公司 -1为不属于任何公司

#Token表
class Tokens(TableBase):
    __tablename__ = "usertokens"

    user_id = Column(String(256), primary_key=True)  #用户ID
    token = Column(String(256), nullable=False, unique=True)  #token
    timestamp = Column(String(256), nullable=False)  #过期时间戳

#权限表
class Authority(TableBase):
    __tablename__ = "authority"

    authority_id = Column(INTEGER(), primary_key=True, autoincrement=True)  #权限ID
    authority_name = Column(String(256), nullable=False)  #权限名称

#公司表
class Companies(TableBase):
    __tablename__ = "companies"

    company_id = Column(INTEGER(), primary_key=True, autoincrement=True) #公司ID
    company_name = Column(String(256), nullable=False) #公司名称

#项目表
class Projects(TableBase):
    __tablename__ = "projects"

    project_id = Column(INTEGER(), primary_key=True, autoincrement=True)  # 工程ID
    project_name = Column(INTEGER(), nullable=False, unique=True)  # 工程名称


#合同表
class Contracts(TableBase):
    __tablename__ = "contracts"

    contract_id = Column(String(256), primary_key=True)  # 合同ID
    contract_name = Column(String(256), nullable=False) #合同名称
    project_id = Column(INTEGER(), ForeignKey('projects.project_id'), nullable=False) #项目id
    company_id = Column(String(256), ForeignKey('companies.company_id'), nullable=False) #公司id
    retention_money = Column(INTEGER(), default=0) #质保金额
    retention_money_date = Column(String(256)) #质保金期限
    parent_contract_id = Column(String(256), ForeignKey('contracts.contract_id')) #父合同ID -1为没有父合同
    money = Column(INTEGER(), default=0.0) #资金

#合同历史记录表
class ContractsHistory(TableBase):
    __tablename__ = "contracts_history"

    id = Column(INTEGER(), primary_key=True)  # id
    contract_id = Column(String(256), ForeignKey("contracts.contract_id"), nullable=False) #合同ID
    progress = Column(Float(), default=0.0) #进度
    pay_money = Column(Float(), default=0.0) #已支付款项
    datetime = Column(String(256), nullable=False) #创建时间

#资金来源表
class MoneyFrom(TableBase):
    __tablename__ = "money_from"

    from_id = Column(INTEGER(), primary_key=True, autoincrement=True)  #来源ID
    from_name = Column(String(256), nullable=False)  #来源名称

#项目总资金及来源表
class ProjectMoney(TableBase):
    __tablename__ = "project_money"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #资金ID
    project_id = Column(INTEGER(), ForeignKey('projects.project_id'), nullable=False) #项目ID
    from_id = Column(INTEGER(), ForeignKey('money_from.from_id'), nullable=False)  # 来源ID
    money = Column(Float(), nullable=False, default=0.0) #金额
    is_in_accout = Column(BOOLEAN(), nullable=False, default=False) #是否已到账

