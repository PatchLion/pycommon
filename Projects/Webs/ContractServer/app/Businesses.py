#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
#from flask import request
from json.decoder import *
from Projects.Webs.ContractServer.app.ArgsChecker import *
from Projects.Webs.ContractServer.settings import *
from Projects.Webs.ContractServer.app.Functions import *
from Projects.Webs.ContractServer.app.StateCodes import *
from Projects.Webs.ContractServer.app.RoleCode import *
from Projects.Webs.ContractServer.database.ContractDatabase import *
from MySqlAlchemy.DBOperator import *
import base64

#args不为None时，证明已经通过参数验证, 外部调用请勿传args
def doResponse(func):
    def wrapper(request,args):
        supports_methods = ["POST", "GET"]
        print(request.method)
        if request.method in supports_methods:
            args = {}
            if "POST" == request.method:
                json_data = request.get_data()
                print("POST json data:", json_data)
                if checkDataVaild(json_data):
                    try:
                        if isinstance(json_data, bytes):
                            args = json.loads(str(json_data, encoding='utf-8'))
                        else:
                            args = json.loads(json_data)
                    except JSONDecodeError as e:
                        return buildStandResponse(StateCode_InvaildDataFormat)
            elif "GET" == request.method:
                args = request.args
                print("GET args:", args)
            return func(None, args)
        else:
            return buildStandResponse(StateCode_UnsupportMethod)
    return wrapper


@doResponse
def doRegister(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        user_name = args_checker.addStringChecker(name="user_name", is_req=True)
        password = args_checker.addStringChecker(name="password", is_req=True)
        nick_name = args_checker.addStringChecker(name="nick_name", is_req=False)
        company_id = args_checker.addNumerChecker(name="company_id", is_req=False, range=(-1, None))
        role_id = args_checker.addNumerChecker(name="role_id", is_req=False, range=(-1, None))
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        exist_objs = records(ContractDB.session(), User, User.user_name == user_name)
        if len(exist_objs) > 0:
            return buildStandResponse(StateCode_UserExist)
        else:
            pwdmd5 = stringMD5(password)  # 加密后的密码

            params = args_checker.outputParams()
            params["password"]=pwdmd5
            new_user = User(**args_checker.outputParams())
            addOrRecord(ContractDB.session(), new_user)
            exist_objs = records(ContractDB.session(), User, User.user_name == user_name)
            if len(exist_objs) > 0:
                returndata = userFromRecord(exist_objs[0])
                return buildStandResponse(StateCode_Success, returndata)
            else:
                return buildStandResponse(StateCode_FailedCreateUser)

#获取角色的授权
def authByRoleID(id):
    auths = []
    if id is not None and id != -1:
        exist_auths = records(ContractDB.session(), RoleAuth, RoleAuth.role_id == id)
        auths = [auth.auth for auth in exist_auths]
    return auths

#获取用户的授权
def authByUserID(id):
    auths = []
    if id is not None and id != -1:
        exist_auths = records(ContractDB.session(), UserAuth, UserAuth.user_id == id)
        auths = [auth.auth for auth in exist_auths]
    return auths

#获取公司名称
def companyByID(id):
    rs = records(ContractDB.session(), Company, Company.id == id)
    if len(rs) > 0:
        return rs[0].name
    else:
        return ""

#获取用户昵称
def usernick_nameByID(id):
    rs = records(ContractDB.session(), User, User.id == id)
    if len(rs) > 0:
        return rs[0].nick_name
    else:
        return ""

#获取角色名称
def roleNameByID(id):
    if id > -1:
        roles = records(ContractDB.session(), Role, Role.id)
        if len(roles) > 0:
            return roles[0].name

    return ""


def userFromRecord(record):
    returndata = {}
    returndata["id"] = record.id
    returndata["user_name"] = record.user_name
    returndata["nick_name"] = record.nick_name
    returndata["role_id"] = record.role_id
    returndata["role_name"] = roleNameByID(record.role_id)
    returndata["auths"] = authByUserID(record.id) + authByRoleID(record.role_id)
    returndata["company_id"] = record.company_id
    returndata["company_name"] = companyByID(record.company_id)
    return returndata

@doResponse
def getUserList(request, args=None):
    if args is not None:
        returndata = []
        exist_users = records(ContractDB.session(), User)
        for user in exist_users:
            returndata.append(userFromRecord(user))
        return buildStandResponse(StateCode_Success, {"users": returndata})

@doResponse
def doUserLogin(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        user_name = args_checker.addStringChecker(name="user_name", is_req=True)
        password = args_checker.addStringChecker(name="password", is_req=True)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        pwdmd5 = stringMD5(password)  # 加密后的密码)
        exist_users = records(ContractDB.session(), User, and_(User.user_name == user_name, User.password == pwdmd5))
        if len(exist_users) > 0:
            returndata = userFromRecord(exist_users[0])
            return buildStandResponse(StateCode_Success, returndata)
        else:
            return buildStandResponse(StateCode_FailedToLogin)

@doResponse
def doUserModify(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        user_name = args_checker.addStringChecker(name="user_name", is_req=True)
        nick_name = args_checker.addStringChecker(name="nick_name", is_req=False)
        role_id = args_checker.addNumerChecker(name="role_id", is_req=False, range=(-1, None))
        company_id = args_checker.addNumerChecker(name="company_id", is_req=False, range=(-1, None))
        password = args_checker.addStringChecker(name="password", is_req=False)
        auths = args_checker.addArrayChecker(name="auths", is_req=False, value_range=AuthNames.keys())
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        if checkDataVaild(user_name):
            objs = records(ContractDB.session(), User, User.user_name == user_name)
            if len(objs) > 0:
                res = {}
                existuser = objs[0]
                if nick_name is not None:
                    existuser.nick_name = nick_name
                    res["nick_name"] = True
                if role_id is not None:
                    existuser.role_id = args["role_id"]
                    res["role_id"] = True
                if company_id is not None:
                    existuser.company_id = company_id
                    res["company_id"] = True
                if auths is not None:
                    removeRecords(ContractDB.session(), UserAuth, UserAuth.user_id==existuser.id)
                    auth_records = [UserAuth(user_id=existuser.id, auth=auth) for auth in auths]
                    size = addOrRecord(ContractDB.session(), auth_records)
                    res["auths"] = (size > 0)
                if password is not None:
                    existuser.password = stringMD5(password)

                size =addOrRecord(ContractDB.session(), existuser)
                if size > 0:
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToModifyUserInfo)
            else:
                return buildStandResponse(StateCode_UserNotExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doProjectCreate(request, args=None):
    if args is not None:

        args_checker = ArgsChecker(args)
        name = args_checker.addStringChecker(name="name", is_req=True)
        moneytypes = args_checker.addArrayChecker(name="moneytypes", is_req=True, value_range=None)
        addr = args_checker.addStringChecker(name="addr", is_req=True)
        content = args_checker.addStringChecker(name="content", is_req=True)
        buildtype_id = args_checker.addNumerChecker(name="buildtype_id", is_req=True, range=(0, None))
        trade_id = args_checker.addNumerChecker(name="trade_id", is_req=True, range=(0, None))
        start_date = args_checker.addNumerChecker(name="start_date", is_req=True, range=(0, None))
        last_date = args_checker.addNumerChecker(name="last_date", is_req=True, range=(0, None))
        rate_of_profit = args_checker.addNumerChecker(name="rate_of_profit", is_req=False, range=(0.0, 1.0))
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        for type in moneytypes:
            type_checker = ArgsChecker(type)
            type_checker.addNumerChecker(name="type", is_req=True, range = (0, None))
            type_checker.addNumerChecker(name="money", is_req=True, range = (0, None))
            temp1, temp2 = type_checker.checkResult()
            if not temp1:
                return buildStandResponse(StateCode_InvaildParam, "moneytypes参数校验失败:" + str(temp2))


        objs = records(ContractDB.session(), Project, Project.name == name)
        if len(objs) == 0:
            project = Project(**args_checker.outputParams())
            addOrRecord(ContractDB.session(), project)
            objs = records(ContractDB.session(), Project, Project.name == name)
            if len(objs) > 0:
                #添加资金类型
                #清除旧有项目资金记录
                removeRecords(ContractDB.session(), ProjectMoney, ProjectMoney.project_id == objs[0].id)
                money_records = [ProjectMoney(moneytype_id=type["type"], money=type["money"], project_id=objs[0].id) for type in moneytypes]
                if len(money_records) > 0:
                    size = addOrRecord(ContractDB.session(), money_records)

                    if size != len(money_records):
                        #添加的资金数量不对，处理异常
                        #移除已添加的项目信息
                        removeRecords(ContractDB.session(), Project, Project.id == objs[0].id)

                        # 清除旧有项目资金记录
                        removeRecords(ContractDB.session(), ProjectMoney, ProjectMoney.project_id == objs[0].id)
                        return buildStandResponse(StateCode_FailedToCreateProject, "创建项目资金记录失败")

                res = projectFromRecord(objs[0])
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_FailedToCreateProject)
        else:
            return buildStandResponse(StateCode_ProjectExist)

'''
@doResponse
def doContractHistory(request, args=None):
    if args is not None:
        contract_id = args.get("contract_id", -1)
        progress = args.get("progress", -1)
        pay_money = args.get("pay_money", -1)
        if contract_id > -1 and progress > -1 and pay_money > -1:
            size = addOrRecord(ContractDB.session(), ContractHistory(contract_id=contract_id, progress=progress, pay_money=pay_money, datetime = currentTimeStamp()))
            if size > 0:
                return buildStandResponse(StateCode_Success, {})
            else:
                return buildStandResponse(StateCode_FailedToCreateContractHistory)
        else:
            return buildStandResponse(StateCode_InvaildParam)
'''
def contractNameByID(id):
    contracts = records(ContractDB.session(), Contract, Contract.id == id)
    if len(contracts) > 0:
        return contracts[0].name
    else:
        return ""

def contractFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    res["project_id"] = record.project_id
    res["project_name"] = projectNameByID(record.project_id)
    companies = records(ContractDB.session(), Company, Company.id == record.company_id)
    res["company_id"] = record.company_id
    if len(companies) > 0:
        res["company_name"] = companies[0].name
        res["company_is_outsourced"] = companies[0].is_outsourced

    res["retention_money"] =record.retention_money
    res["retention_money_date"] =record.retention_money_date
    res["parent_contract_id"] =record.parent_contract_id
    res["parent_contract_name"] = contractNameByID(record.parent_contract_id)
    res["money"] =record.money
    res["place_of_performance"] =record.place_of_performance
    res["date_of_performance"] =record.date_of_performance
    res["type_of_performance"] =record.type_of_performance
    res["note"] =record.note
    res["code"] =record.code
    res["tag_object_name"] =record.tag_object_name
    res["content"] =record.content
    res["scope"] =record.scope
    res["retention_money_percent"] =record.retention_money_percent
    res["responsible_person"] =record.responsible_person
    res["responsible_person_contact"] =record.responsible_person_contact
    res["pay_condtion"] =record.pay_condtion
    res["sign_date"] =record.sign_date
    res["start_date"] =record.start_date
    res["progress"] =record.progress
    return res

@doResponse
def doContractCreate(request, args=None):
    if args is not None:


        args_checker = ArgsChecker(args)
        name = args_checker.addStringChecker(name="name", is_req=True)
        project_id = args_checker.addNumerChecker(name="project_id", is_req=True, range=(0, None))
        company_id = args_checker.addNumerChecker(name="company_id", is_req=True, range=(0, None))
        retention_money = args_checker.addNumerChecker(name="retention_money", is_req=True, range=(0, None))
        retention_money_date = args_checker.addNumerChecker(name="retention_money_date", is_req=True, range=(0, None))
        parent_contract_id = args_checker.addNumerChecker(name="parent_contract_id", is_req=True, range=(-1, None))
        money = args_checker.addNumerChecker(name="money", is_req=True, range=(0, None))
        progress = args_checker.addNumerChecker(name="progress", is_req=False, range=(0, 100))
        place_of_performance = args_checker.addStringChecker(name="place_of_performance", is_req=True)
        date_of_performance = args_checker.addStringChecker(name="date_of_performance", is_req=True)
        type_of_performance = args_checker.addStringChecker(name="type_of_performance", is_req=True)
        note = args_checker.addStringChecker(name="note", is_req=False)
        code = args_checker.addStringChecker(name="code", is_req=True)
        tag_object_name = args_checker.addStringChecker(name="tag_object_name", is_req=True)
        content = args_checker.addStringChecker(name="content", is_req=True)
        scope = args_checker.addStringChecker(name="scope", is_req=True)
        retention_money_percent = args_checker.addNumerChecker(name="retention_money_percent", is_req=False, range=(0.0, 1.0))
        responsible_person = args_checker.addStringChecker(name="responsible_person", is_req=False)
        responsible_person_contact = args_checker.addStringChecker(name="responsible_person_contact", is_req=False)
        pay_condtion = args_checker.addStringChecker(name="pay_condtion", is_req=False)
        sign_date = args_checker.addNumerChecker(name="sign_date", is_req=True, range=(0, None))
        start_date = args_checker.addNumerChecker(name="start_date", is_req=True, range=(0, None))
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        record = records(ContractDB.session(), Contract, Contract.name == name)
        if len(record) == 0:

            contract = Contract(**args_checker.outputParams())

            addOrRecord(ContractDB.session(), contract)
            objs = records(ContractDB.session(), Contract, Contract.name == name)
            if len(objs) > 0:
                res = contractFromRecord(objs[0])
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_FailedToCreateContract)
        else:
            return buildStandResponse(StateCode_ContractExist)

'''
#获取项目审批信息
def approveInfoByProjectID(id):
    objs = records(ContractDB.session(), AskApprove, AskApprove.project_id==id)
    return objs
'''

#行业名称
def tradeNameByID(id):
    objs = records(ContractDB.session(), Trade, Trade.id==id)
    if len(objs) > 0:
        return objs[0].name
    else:
        return ""

#建设性质名称
def buildTypeNameByID(id):
    objs = records(ContractDB.session(), BuildType, BuildType.id == id)
    if len(objs) > 0:
        return objs[0].name
    else:
        return ""

def moneyTypesFromRecord(record):
    res = {}
    res["type"] = record.moneytype_id
    res["money"] = record.money
    return res

def projectFromRecord(record):
    returndata = {}
    returndata["id"] = record.id
    returndata["name"] = record.name
    returndata["addr"] = record.addr
    returndata["trade_id"] = record.trade_id
    returndata["trade_name"] = tradeNameByID(record.trade_id)
    returndata["buildtype_id"] = record.buildtype_id
    returndata["buildtype_name"] = buildTypeNameByID(record.buildtype_id)
    returndata["content"] = record.content
    returndata["start_date"] = record.start_date
    returndata["last_date"] = record.last_date
    returndata["rate_of_profit"] = record.rate_of_profit
    moneytypes = []
    mondeys = records(ContractDB.session(), ProjectMoney, ProjectMoney.project_id == record.id)
    totol_money = 0
    for money in mondeys:
        print(type(money), money)
        temp = moneyTypesFromRecord(money)
        totol_money = totol_money + temp["money"]
        moneytypes.append(temp)
    returndata["money"] = totol_money
    returndata["moneytypes"] = moneytypes

    '''
    apprs = approveInfoByProjectID(record.id)
    if len(apprs) >  0:
        returndata["first_approve_user_id"] = apprs[0].first_user_id
        returndata["first_approve_user_nick_name"] = usernick_nameByID(apprs[0].first_user_id)
        returndata["is_first_approve_user_passed"] = apprs[0].is_first_passed
        returndata["second_approve_user_id"] = apprs[0].second_user_id
        returndata["second_approve_user_nick_name"] = usernick_nameByID(apprs[0].second_user_id)
        returndata["is_second_approve_user_passed"] = apprs[0].is_second_passed
    else:
        returndata["first_approve_user_id"] = -1
        returndata["first_approve_user_nick_name"] = ""
        returndata["is_first_approve_user_passed"] = False
        returndata["second_approve_user_id"] = -1
        returndata["second_approve_user_nick_name"] = ""
        returndata["is_second_approve_user_passed"] = False
    '''
    return returndata

@doResponse
def getProjectList(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        id = args_checker.addNumerChecker(name="id", is_req=False, range=(0, None))
        name = args_checker.addStringChecker(name="name", is_req=False)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        cond = None
        if id is not None and name is not None:
            cond = and_(Project.id == id, Project.name == name)
        elif id is not None:
            cond = (Project.id == id)
        elif name is not None:
            cond = (Project.name == name)
        if cond is None:
            projects = records(ContractDB.session(), Project)
        else:
            projects = records(ContractDB.session(), Project, cond)

        project_json = {}
        project_json["projects"] = []
        for pro in projects:
            temp = projectFromRecord(pro)
            project_json["projects"].append(temp)
        return buildStandResponse(StateCode_Success, project_json)

def roleFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    return res

@doResponse
def doCreateRole(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        name = args_checker.addStringChecker(name="name", is_req=True)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        objs = records(ContractDB.session(), Role, Role.name == name)
        if len(objs) == 0:
            addOrRecord(ContractDB.session(), Role(name=name))
            objs = records(ContractDB.session(), Role, Role.name==name)
            if len(objs) > 0:
                res_json = roleFromRecord(objs[0])
                return buildStandResponse(StateCode_Success, res_json)
            else:
                return buildStandResponse(StateCode_FailedToCreateRole)
        else:
            return buildStandResponse(StateCode_RoleExist)

'''
@doResponse
def doAskApproveCreate(request, args=None):
    if args is not None:
        project_id = args.get("project_id", -1)
        first_approve_user_id = args.get("first_approve_user_id", -1)
        second_approve_user_id = args.get("second_approve_user_id", -1)

        if project_id > -1 and first_approve_user_id > -1 and second_approve_user_id > -1:
            new_objs = [AskApprove(project_id=project_id,first_user_id=first_approve_user_id, is_first_passed=Approve_Waiting, second_user_id=second_approve_user_id, is_second_passed=Approve_Waiting)]
            size = addOrRecord(ContractDB.session(), new_objs)
            if size > 0:
                return buildStandResponse(StateCode_Success, {})
            else:
                return buildStandResponse(StateCode_FailedToCreateProjectAskApprove)
        else:
            return buildStandResponse(StateCode_InvaildParam)
'''

def projectNameByID(id):
    objs = records(ContractDB.session(), Project, Project.id == id)
    if len(objs) > 0:
        return objs[0].name
    else:
        return ""

'''
@doResponse
def getAskApprove(request, args=None):
    if args is not None:
        user_id = args.get("user_id", -1)
        if user_id > -1:
            objs = records(ContractDB.session(), AskApprove, or_(AskApprove.first_user_id==user_id, AskApprove.second_user_id==user_id))

            need_noitfy = []
            #查找包含user，并且user需要通知的项目
            for obj in objs:
                if (user_id == obj.first_user_id and obj.is_first_passed == Approve_Waiting) \
                        or (user_id == obj.second_user_id and obj.is_first_passed == Approve_Passed and obj.is_second_passed ==Approve_Waiting):
                    if obj.project_id not in need_noitfy:
                        pro={}
                        pro["id"] =obj.project_id
                        pro["name"] = projectNameByID(obj.project_id)
                        need_noitfy.append(pro)
            return buildStandResponse(StateCode_Success, {"project_ids":need_noitfy})
        else:
            return buildStandResponse(StateCode_InvaildParam)
'''

'''
@doResponse
def setApproveState(request, args=None):
    if args is not None:
        project_id= args.get("project_id", -1)
        user_id= args.get("user_id", -1)
        state= args.get("state", -1)

        if user_id > -1 and project_id > -1 and (state ==Approve_Passed or state == Approve_Waiting or state == Approve_Rejected) :
            objs = records(ContractDB.session(), AskApprove, AskApprove.project_id == project_id)

            if len(objs) >= 0:
                approve = objs[0]
                is_changed = False
                if user_id == approve.first_user_id:
                    approve.is_first_passed = state
                    if approve.second_user_id == approve.first_user_id:
                        approve.is_second_passed = state
                    is_changed = True
                elif user_id == approve.second_user_id and approve.is_first_passed == Approve_Passed:
                    approve.is_second_passed = state
                    is_changed = True
                else:
                    return buildStandResponse(StateCode_FailedToSetProjectApprove)

                if is_changed:
                    size = addOrRecord(ContractDB.session(), approve)
                    if size > 0:
                        return buildStandResponse(StateCode_Success, {})
                    else:
                        return buildStandResponse(StateCode_FailedToSetProjectApprove)
            else:
                return buildStandResponse(StateCode_ProjectAskApproveNotExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)
'''

@doResponse
def getCompanies(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Company)
        res_json = {}
        res_json["companies"] = []
        for obj in objects:
            temp = companyFromRecord(obj)
            res_json["companies"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

@doResponse
def getRoleList(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Role)
        res_json = {}
        res_json["roles"] = []
        for obj in objects:
            temp = roleFromRecord(obj)
            res_json["roles"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

def tradeFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    return res

@doResponse
def getTradeList(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Trade)
        res_json = {}
        res_json["trades"] = []
        for obj in objects:
            temp = tradeFromRecord(obj)
            res_json["trades"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

def buildTypeFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    return res

@doResponse
def getBuildTypeList(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), BuildType)
        res_json = {}
        res_json["buildtypes"] = []
        for obj in objects:
            temp = buildTypeFromRecord(obj)
            res_json["buildtypes"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

def moneyTypeFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    return res

@doResponse
def getMoneyTypeList(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), MoneyType)
        res_json = {}
        res_json["moneytypes"] = []
        for obj in objects:
            temp = moneyTypeFromRecord(obj)
            res_json["moneytypes"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)
@doResponse
def getContractList(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        project_id = args_checker.addNumerChecker(name="project_id", is_req=False, range=(0, None))
        company_id = args_checker.addNumerChecker(name="company_id", is_req=False, range=(0, None))
        contract_id = args_checker.addNumerChecker(name="contract_id", is_req=False, range=(0, None))
        parent_contract_id = args_checker.addNumerChecker(name="parent_contract_id", is_req=False, range=(0, None))
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        conds = []
        if project_id is not None:
            conds.append(Contract.project_id == project_id)

        if company_id is not None:
            conds.append(Contract.company_id == company_id)

        if contract_id is not None:
            conds.append(Contract.id == contract_id)

        if parent_contract_id is not None:
            conds.append(Contract.parent_contract_id == parent_contract_id)

        if len(conds) == 0:
            objs = records(ContractDB.session(), Contract)
        else:
            objs = records(ContractDB.session(), Contract, and_(*conds))

        res_json = {}
        res_json["contracts"] = []
        for cont in objs:
            res = contractFromRecord(cont)
            res_json["contracts"].append(res)
        return buildStandResponse(StateCode_Success, res_json)

@doResponse
def uploadBill(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)

        filename = args_checker.addStringChecker(name="filename", is_req=True)
        filedata = args_checker.addStringChecker(name="filedata", is_req=True)
        contract_id = args_checker.addNumerChecker(name="contract_id", is_req=True, range=(0, None))
        bill_number = args_checker.addStringChecker(name="bill_number", is_req=True)  # 凭证号
        datetime = args_checker.addNumerChecker(name="datetime", is_req=True, range=(0, None))
        abstract = args_checker.addStringChecker(name="abstract", is_req=False)  # 摘要
        payment_amount = args_checker.addNumerChecker(name="payment_amount", is_req=True, range=(0, None))  # 付款金额（元）
        not_settlement_amount = args_checker.addNumerChecker(name="not_settlement_amount", is_req=False, range=(0, None)) # 未结算金额（元）
        bill_amount = args_checker.addNumerChecker(name="bill_amount", is_req=False, range=(0, None))   # 提供票据金额（元）
        receipt_amount = args_checker.addNumerChecker(name="receipt_amount", is_req=False, range=(0, None))  # 提供发票金额（元）
        payment_bank_and_type = args_checker.addStringChecker(name="payment_bank_and_type", is_req=True)  # 付款银行及方式
        note = args_checker.addStringChecker(name="note", is_req=False)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        child_path = os.path.join(contractNameByID(contract_id), str(bill_number))
        dir = os.path.join(FILE_RESTORE_ROOT_DIR, child_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        child_path = os.path.join(child_path, filename)
        fullpath = os.path.join(FILE_RESTORE_ROOT_DIR, child_path)
        print("full path:", fullpath)
        if os.path.exists(fullpath):
            return buildStandResponse(StateCode_FileExist)

        try:
            with open(fullpath, "wb", ) as f:
                print("Write file to:", fullpath)
                filesize = f.write(base64.b64decode(filedata))
                if filesize > 0:
                    params = {}
                    params["contract_id"] = contract_id
                    params["bill_number"] = bill_number
                    params["datetime"] = datetime
                    if abstract is not None:
                        params["abstract"] = abstract
                    params["payment_amount"] = payment_amount

                    if not_settlement_amount is not None:
                        params["not_settlement_amount"] = not_settlement_amount

                    if bill_amount is not None:
                        params["bill_amount"] = bill_amount

                    if receipt_amount is not None:
                        params["receipt_amount"] = receipt_amount

                    params["payment_bank_and_type"] = payment_bank_and_type
                    params["bill_file_path"] = child_path
                    if note is not None:
                        params["note"] = note

                    size = addOrRecord(ContractDB.session(), ContractBill(**params))
                    if size > 0:
                        return buildStandResponse(StateCode_Success, {})
                    else:
                        os.remove(fullpath)
                        return buildStandResponse(StateCode_FailedToCreateFileRecord)
                else:
                    return buildStandResponse(StateCode_FailedToCreateFile)
        except Exception as e:
            print(e)
            return buildStandResponse(StateCode_FailedToCreateFile)


def companyFromRecord(record):
    res = {}
    res["id"] = record.id
    res["name"] = record.name
    res["is_outsourced"] = record.is_outsourced
    return res

@doResponse
def doCompanyCreate(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        name = args_checker.addStringChecker(name="name", is_req=True)
        is_outsourced = args_checker.addBooleanChecker(name="is_outsourced", is_req=False)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        record = records(ContractDB.session(), Company, Company.name == name)
        if len(record) == 0:
            com = Company(**args_checker.outputParams())
            addOrRecord(ContractDB.session(), com)
            objs = records(ContractDB.session(), Company, Company.name == name)
            if len(objs) > 0:
                res = companyFromRecord(objs[0])
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_FailedToCreateCompany)
        else:
            return buildStandResponse(StateCode_CompanyExist)

def billFromRecord(record):
    res = {}
    res["id"] = record.id
    res["contract_id"] = record.contract_id
    res["bill_number"] = record.bill_number
    res["datetime"] = record.datetime
    res["abstract"] = record.abstract
    res["payment_amount"] = record.payment_amount
    res["not_settlement_amount"] = record.not_settlement_amount
    res["bill_amount"] = record.bill_amount
    res["receipt_amount"] = record.receipt_amount
    res["payment_bank_and_type"] = record.payment_bank_and_type
    res["bill_file_path"] = record.bill_file_path
    res["note"] = record.note
    return res
'''
@doResponse
def doBillCreate(request, args=None):
    if args is not None:
        args_checker = ArgsChecker(args)
        contract_id = args_checker.addNumerChecker("contract_id", is_req=True, range=(0, None))
        bill_number = args_checker.addStringChecker("bill_number", is_req=True)
        datetime = args_checker.addNumerChecker("datetime", is_req=True, range=(0, None))
        abstract = args_checker.addStringChecker("abstract", is_req=True)
        payment_amount = args_checker.addNumerChecker("payment_amount", is_req=False, range=(0, None))
        not_settlement_amount = args_checker.addNumerChecker("not_settlement_amount", is_req=False, range=(0, None))
        bill_amount = args_checker.addNumerChecker("bill_amount", is_req=False, range=(0, None))
        receipt_amount = args_checker.addNumerChecker("receipt_amount", is_req=False, range=(0, None))
        payment_bank_and_type = args_checker.addStringChecker("payment_bank_and_type", is_req=True)
        note = args_checker.addStringChecker("note", is_req=False)
        successed, message = args_checker.checkResult()

        if not successed:
            return buildStandResponse(StateCode_InvaildParam, message)

        record = records(ContractDB.session(), ContractBill, ContractBill.bill_number == bill_number)
        if len(record) == 0:
            bill = ContractBill(**args_checker.outputParams())
            addOrRecord(ContractDB.session(), bill)
            objs = records(ContractDB.session(), ContractBill, ContractBill.bill_number == bill_number)
            if len(objs) > 0:
                res = billFromRecord(objs[0])
                return buildStandResponse(StateCode_Success, res)
            else:
                return buildStandResponse(StateCode_FailedToCreateContractBill)
        else:
            return buildStandResponse(StateCode_CompanyExist)
'''