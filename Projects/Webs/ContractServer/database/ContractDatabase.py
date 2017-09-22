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
    __tablename__ = "users"
    user_id = Column(String(256), primary_key=True) #用户ID
    password = Column(String(256), nullable=False) #密码
    name = Column(String(256), nullable=False) #名称

#角色表
class Roles(TableBase):
    __tablename__ = "roles"
    role_id = Column(String(256), primary_key=True) #角色ID
    role_name = Column(String(256), unique=True, nullable=False) #角色名称

#角色权限表
class RoleAuth(TableBase):
    __tablename__ = "roleauths"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #
    role_id = Column(String(256), ForeignKey("roles.role_id")) #角色ID
    role_value = Column(INTEGER(), nullable=True) #角色权限

#角色用户关联表
class UserRole(TableBase):
    __tablename__ = "userroles"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #
    user_id = Column(String(256), ForeignKey("users.user_id"), unique=True)  # 用户ID
    role_id = Column(String(256), ForeignKey("roles.role_id"))  # 角色ID


#公司表
class Companies(TableBase):
    __tablename__ = "companies"

    company_id = Column(INTEGER(),  primary_key=True, autoincrement=True) #公司ID
    company_name = Column(String(256), unique=True, nullable=False) #公司名称

#项目表
class Projects(TableBase):
    __tablename__ = "projects"

    project_id = Column(INTEGER(),primary_key=True, autoincrement=True)  # 工程ID
    project_name = Column(String(256), unique=True, nullable=False)  # 工程名称

#文件上传记录
class Uploads(TableBase):
    __tablename__ = "uploads"

    id = Column(INTEGER(),primary_key=True, autoincrement=True)  # ID
    contract_id = Column(String(256),nullable=False)  # 合同id
    path = Column(String(256),nullable=False)  # 工程名称

#合同表
class Contracts(TableBase):
    __tablename__ = "contracts"

    contract_id = Column(String(256), primary_key=True)  # 合同ID
    contract_name = Column(String(256), nullable=False) #合同名称
    project_id = Column(INTEGER(), ForeignKey('projects.project_id'), nullable=False) #项目id
    company_id = Column(String(256), ForeignKey('companies.company_id'), nullable=False) #公司id
    retention_money = Column(INTEGER(), default=0) #质保金额
    retention_money_date = Column(INTEGER()) #质保金期限
    parent_contract_id = Column(String(256), ForeignKey('contracts.contract_id')) #父合同ID -1为没有父合同
    money = Column(INTEGER(), default=0.0) #资金

#合同历史记录表
class ContractsHistory(TableBase):
    __tablename__ = "contracts_history"

    id = Column(String(256), primary_key=True)  # id
    contract_id = Column(String(256), ForeignKey("contracts.contract_id"), nullable=False) #合同ID
    progress = Column(Float(), default=0.0) #进度
    pay_money = Column(Float(), default=0.0) #已支付款项
    datetime = Column(INTEGER(), nullable=False) #创建时间

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

