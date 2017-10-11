#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Projects.Webs.MyContractServer.app.Functions import currentTimeStamp
from Projects.Webs.MyContractServer.app.StateCodes import *
from Projects.Webs.MyContractServer.database import TableBase
from sqlalchemy import Column, String, INTEGER, Float, BOOLEAN
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Practices.MyContractServer.settings import *


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
    nick_name = Column(String(256), nullable=True, default="未命名") #昵称
    company_id = Column(INTEGER(), nullable=True, default=-1) #公司id
    role_id = Column(INTEGER(), nullable=True, default=-1) #角色id

#角色表
class Role(TableBase):
    __tablename__ = "Role"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False) #角色名称
    note = Column(String(256), nullable=True, default="") #角色描述

#角色权限表
class RoleAuth(TableBase):
    __tablename__ = "RoleAuth"

    id = Column(INTEGER(), primary_key=True, autoincrement=True) #id
    role_id = Column(INTEGER(), nullable=False) #角色id
    auth = Column(INTEGER(), nullable=False) #权限

'''
#用户权限表
class UserAuth(TableBase):
    __tablename__ = "UserAuth"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    user_id = Column(INTEGER(), nullable=False) #用户id
    auth = Column(INTEGER(), nullable=False) #权限
'''

#公司表
class Company(TableBase):
    __tablename__ = "Company"

    id = Column(INTEGER(), primary_key=True, autoincrement=True) #id
    name = Column(String(256), unique=True, nullable=False) #公司名称
    is_outsourced = Column(BOOLEAN(), nullable=True, default=False) #是否是外包公司

#行业表
class Trade(TableBase):
    __tablename__ = "Trade"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    name = Column(String(256), unique=True, nullable=False)  # 行业名称

#建设性质表
class BuildType(TableBase):
    __tablename__ = "BuildType"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    name = Column(String(256), unique=True, nullable=False)  # 建设性质名称

#资金来源种类
class MoneyType(TableBase):
    __tablename__ = "MoneyType"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    name = Column(String(256), unique=True, nullable=False)  # 资金来源种类名称

#项目资金及来源表
class ProjectMoney(TableBase):
    __tablename__ = "ProjectMoney"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    project_id = Column(INTEGER(), nullable=False)  #项目ID
    moneytype_id = Column(INTEGER(), nullable=False)  #资金来源
    money = Column(INTEGER(), nullable=False)  #资金（元）

#项目表
class Project(TableBase):
    __tablename__ = "Project"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False)  #项目名称
    addr = Column(String(512), nullable=False)#建设地点
    trade_id = Column(INTEGER(), nullable=False)  #所属行业
    buildtype_id = Column(String(256), nullable=False)#建设性质
    content = Column(String(1024), nullable=False)#项目描述
    rate_of_profit = Column(Float(), nullable=True, default=0.1) #项目利润率
    start_date = Column(INTEGER(), nullable=False, default=currentTimeStamp()) #项目开始日期，时间戳
    last_date = Column(INTEGER(), nullable=False, default=currentTimeStamp() + 10000) #项目到期日期，时间戳


'''
#审批申请表
class AskApprove(TableBase):
    __tablename__ = "AskApprove"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  #id
    project_id = Column(INTEGER(), nullable=False)  #项目id
    first_user_id = Column(INTEGER(), nullable=False)  #第一审批用户ID
    second_user_id = Column(INTEGER(), nullable=False)  #第二审批用户ID
    is_first_passed = Column(INTEGER(), nullable=True, default=Approve_Waiting)  #是否第一审批用户通过
    is_second_passed = Column(INTEGER(), nullable=True, default=Approve_Waiting)  #是否第二审批用户通过
'''


#合同表
class Contract(TableBase):
    __tablename__ = "Contract"

    id = Column(INTEGER(),primary_key=True, autoincrement=True)  #id
    name = Column(String(256), unique=True, nullable=False) #合同名称
    project_id = Column(INTEGER(), nullable=False) #项目id
    company_id = Column(INTEGER(), nullable=False) #公司id(施工单位)
    retention_money = Column(INTEGER(), nullable=True, default=-1) #质保金额（元）
    retention_money_date = Column(INTEGER(), nullable=True, default=-1) #质保金期限, 时间戳
    parent_contract_id = Column(INTEGER(),nullable=True, default=-1) #父合同ID -1为没有父合同
    money = Column(INTEGER(), nullable=False, default=0) #资金（元）
    place_of_performance = Column(String(256), nullable=True) #履行地点
    date_of_performance = Column(String(256), nullable=True) #履行期限
    type_of_performance = Column(String(256), nullable=True) #履行方式
    note = Column(String(256), nullable=True) #备注
    code = Column(String(256), unique=True, nullable=False) #合同编码
    tag_object_name = Column(String(256), nullable=True) #标的物名称
    content = Column(String(256), nullable=False) #合同内容
    scope = Column(String(256), nullable=False) #合同范围
    retention_money_percent = Column(INTEGER(), nullable=True, default=0.1) #质保金比例
    responsible_person = Column(String(256), nullable=True) #经办人名称
    responsible_person_contact = Column(String(256), nullable=True) #经办人联系方式
    pay_condtion = Column(String(1000), nullable=True) #合同付款条件 多条记录用分割符分割
    sign_date = Column(INTEGER(), nullable=False) #签订时间, 时间戳
    start_date = Column(INTEGER(), nullable=False) #生效时间, 时间戳
    progress = Column(INTEGER(), nullable=True,default=0) #进度 0 - 100
'''
#合同进度记录表

class ContractHistory(TableBase):
    __tablename__ = "ContractsHistory"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    contract_id = Column(INTEGER(), nullable=False) #合同ID
    progress = Column(INTEGER(), default=0) #进度 0 - 100
    pay_money = Column(INTEGER(), default=0) #已支付款项
    datetime = Column(INTEGER(), nullable=False) #创建时间
    note = Column(String(256), nullable=True, ) #备注



#文件上传记录
class File(TableBase):
    __tablename__ = "File"

    id = Column(INTEGER(),primary_key=True, autoincrement=True)  #id
    contract_id = Column(INTEGER(),nullable=False)  #合同id
    classify = Column(String(256),nullable=False) #分类
    name = Column(String(256),nullable=False) #名称
    note = Column(String(256), nullable=True) #备注
'''

#合同票据信息
class ContractBill(TableBase):
    __tablename__ = "ContractBil"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)  # id
    contract_id = Column(INTEGER(), nullable=False) # 合同编号
    bill_number = Column(String(256), nullable=False, unique=True)  # 凭证号
    datetime = Column(INTEGER(), nullable=False) # 时间
    abstract = Column(String(256), nullable=True) # 摘要
    payment_amount = Column(INTEGER(), nullable=False) # 付款金额（元）
    not_settlement_amount = Column(INTEGER(), nullable=True) # 未结算金额（元）
    bill_amount = Column(INTEGER(), nullable=True, default=0) # 提供票据金额（元）
    receipt_amount = Column(INTEGER(), nullable=True, default=0) # 提供发票金额（元）
    payment_bank_and_type = Column(String(256), nullable=False) # 付款银行及方式
    bill_file_path = Column(String(512), nullable=True) # 票据文件路径
    note = Column(String(256), nullable=True) # 备注