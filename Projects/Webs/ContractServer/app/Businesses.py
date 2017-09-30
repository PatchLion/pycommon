#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
#from flask import request
from json.decoder import *
from Projects.Webs.ContractServer.settings import *
from Projects.Webs.ContractServer.app.Functions import *
from Projects.Webs.ContractServer.app.StateCodes import *
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
        user = args.get("username", "")
        pwd = args.get("pwd", "")
        name = args.get("nickname", "未命名")
        company_id = args.get("company_id", -1)
        role_id = args.get("role_id", -1)
        if checkDataVaild(user) and checkDataVaild(pwd):
            exist_objs = records(ContractDB.session(), User, User.user_name == user)
            if len(exist_objs) > 0:
                return buildStandResponse(StateCode_UserExist)
            else:
                pwdmd5 = stringMD5(pwd)  # 加密后的密码
                new_user = User(user_name=user, password=pwdmd5, nick_name=name, company_id=company_id, role_id=role_id)
                addOrRecord(ContractDB.session(), new_user)
                exist_objs = records(ContractDB.session(), User, User.user_name == user)
                if len(exist_objs) > 0:
                    returndata = userFromRecord(exist_objs[0])
                    return buildStandResponse(StateCode_Success, returndata)
                else:
                    return buildStandResponse(StateCode_FailedCreateUser)
        else:
            return buildStandResponse(StateCode_InvaildParam)

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
def userNickNameByID(id):
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
    returndata["username"] = record.user_name
    returndata["nickname"] = record.nick_name
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
        user = args.get("username", "")
        pwd = args.get("pwd", "")
        if checkDataVaild(user) and checkDataVaild(pwd):
            pwdmd5 = stringMD5(pwd)  # 加密后的密码)
            exist_users = records(ContractDB.session(), User, and_(User.user_name == user, User.password == pwdmd5))
            if len(exist_users) > 0:
                returndata = userFromRecord(exist_users[0])
                return buildStandResponse(StateCode_Success, returndata)
            else:
                return buildStandResponse(StateCode_FailedToLogin)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doUserModify(request, args=None):
    if args is not None:
        username= args.get("username", "")
        nickname= args.get("nickname", None)
        role_id= args.get("role_id", None)
        company_id= args.get("company_id", None)
        password_pair= args.get("password", None)
        auths= args.get("auths", None)
        if checkDataVaild(username):
            objs = records(ContractDB.session(), User, User.user_name == username)
            if len(objs) > 0:
                res = {}
                existuser = objs[0]
                if nickname is not None:
                    existuser.nick_name = nickname
                    res["nickname"] = True
                if role_id is not None:
                    existuser.role_id = role_id
                    res["role_id"] = True
                if company_id is not None:
                    existuser.company_id = company_id
                    res["company_id"] = True
                if auths is not None:
                    removeRecords(ContractDB.session(), UserAuth, UserAuth.user_id==existuser.id)
                    auth_records = [UserAuth(user_id=existuser.id, auth=auth) for auth in auths if isinstance(auth, int) and auth > -1]
                    if len(auth_records) > 0:
                        size = addOrRecord(ContractDB.session(), auth_records)
                    res["auths"] = True
                if password_pair is not None:
                    oldpwd = password_pair.get("old", "")
                    newpwd = password_pair.get("new", "")
                    if checkDataVaild(oldpwd) and checkDataVaild(newpwd):
                        temps = records(ContractDB.session(), User, and_(User.user_name == username, User.password==stringMD5(oldpwd)))
                        if len(temps) > 0:
                            existuser.password = stringMD5(newpwd)
                            res["password"] = True
                        else:
                            res["password"] = False

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
        name = args.get("name", "")
        money = args.get("money", -1)
        start_date = args.get("start_date", -1)
        last_date = args.get("last_date", -1)
        rate_of_profit = args.get("rate_of_profit", 0.1)
        if checkDataVaild(name) and money > 0 and last_date > start_date and last_date > -1 and start_date > -1:
            record = records(ContractDB.session(), Project, Project.name == name)
            if len(record) == 0:
                project = Project(name=name, money=money, start_date=start_date, last_date=last_date, rate_of_profit=rate_of_profit)
                addOrRecord(ContractDB.session(), project)
                record = records(ContractDB.session(), Project, Project.name == name)
                if len(record) > 0:
                    res = projectFromRecord(record[0])
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateProject)
            else:
                return buildStandResponse(StateCode_ProjectExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

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


@doResponse
def doContractCreate(request, args=None):
    if args is not None:
        project_id= args.get("project_id", -1)
        contract_name= args.get("name", "")
        company_id= args.get("company_id", -1)
        retention_money= args.get("retention_money", 0)
        retention_money_date= args.get("retention_money_date", 0)
        parent_contract_id= args.get("parent_contract_id", -1)
        money= args.get("money", 0)
        pay_money= args.get("pay_money", 0)
        progress= args.get("progress", 0)
        second_party_name= args.get("second_party_name", "")
        place_of_performance= args.get("place_of_performance", "")
        date_of_performance= args.get("date_of_performance", "")
        type_of_performance= args.get("type_of_performance", "")
        note= args.get("note", "")

        if checkDataVaild(contract_name) and project_id > -1 and company_id > -1 and checkDataVaild(second_party_name):
            record = records(ContractDB.session(), Contract, Contract.name == contract_name)
            if len(record) == 0:
                contract = Contract(project_id=project_id,
                                    name=contract_name,
                                    company_id=company_id,
                                    retention_money= retention_money,
                                    retention_money_date=retention_money_date,
                                    parent_contract_id=parent_contract_id,
                                    money=money,
                                    pay_money = pay_money,
                                    progress = progress,
                                    second_party_name= second_party_name,
                                    place_of_performance= place_of_performance,
                                    date_of_performance= date_of_performance,
                                    type_of_performance= type_of_performance,
                                    note= note)

                addOrRecord(ContractDB.session(), contract)
                record = records(ContractDB.session(), Contract, Contract.name == contract_name)
                if len(record) > 0:
                    res = {}
                    res["contract_id"] = record[0].id
                    res["project_id"] = record[0].project_id
                    res["contract_name"] = record[0].name
                    res["company_id"] = record[0].company_id
                    res["retention_money"] = record[0].retention_money
                    res["retention_money_date"] = record[0].retention_money_date
                    res["parent_contract_id"] = record[0].parent_contract_id
                    res["money"] = record[0].money
                    res["pay_money"] = record[0].pay_money
                    res["progress"] = record[0].progress
                    res["second_party_name"] = record[0].second_party_name
                    res["place_of_performance"] = record[0].place_of_performance
                    res["date_of_performance"] = record[0].date_of_performance
                    res["type_of_performance"] = record[0].type_of_performance
                    res["note"] = record[0].note
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateContract)
            else:
                return buildStandResponse(StateCode_ContractExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)

#获取项目审批信息
def approveInfoByProjectID(id):
    objs = records(ContractDB.session(), AskApprove, AskApprove.project_id==id)
    return objs

def projectFromRecord(record):
    returndata = {}
    returndata["id"] = record.id
    returndata["name"] = record.name
    returndata["money"] = record.money
    returndata["start_date"] = record.start_date
    returndata["last_date"] = record.last_date
    returndata["rate_of_profit"] = record.rate_of_profit
    apprs = approveInfoByProjectID(record.id)
    if len(apprs) >  0:
        returndata["first_approve_user_id"] = apprs[0].first_user_id
        returndata["first_approve_user_nickname"] = userNickNameByID(apprs[0].first_user_id)
        returndata["is_first_approve_user_passed"] = apprs[0].is_first_passed
        returndata["second_approve_user_id"] = apprs[0].second_user_id
        returndata["second_approve_user_nickname"] = userNickNameByID(apprs[0].second_user_id)
        returndata["is_second_approve_user_passed"] = apprs[0].is_second_passed
    else:
        returndata["first_approve_user_id"] = -1
        returndata["first_approve_user_nickname"] = ""
        returndata["is_first_approve_user_passed"] = False
        returndata["second_approve_user_id"] = -1
        returndata["second_approve_user_nickname"] = ""
        returndata["is_second_approve_user_passed"] = False
    return returndata

@doResponse
def getProjectList(request, args=None):
    if args is not None:
        id = args.get("id", -1)
        name = args.get("name", "")
        cond = None
        if id > -1 and checkDataVaild(name):
            cond = and_(Project.id == id, Project.name == name)
        elif id > -1:
            cond = (Project.id == id)
        elif checkDataVaild(name):
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

@doResponse
def doCreateRole(request, args=None):
    if args is not None:
        role_name = args.get("name", "")
        if checkDataVaild(role_name):
            objs = records(ContractDB.session(), Role, Role.name == role_name)
            if len(objs) == 0:
                id = createUuid()
                size = addOrRecord(ContractDB.session(), Role(name=role_name))
                if size > 0:
                    res_json = {}
                    res_json["id"] = id
                    res_json["name"] = role_name
                    return buildStandResponse(StateCode_Success, res_json)
                else:
                    return buildStandResponse(StateCode_FailedToCreateRole)
            else:
                return buildStandResponse(StateCode_RoleExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)\


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

def projectNameByID(id):
    objs = records(ContractDB.session(), Project, Project.id == id)
    if len(objs) > 0:
        return objs[0].name
    else:
        return ""

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

@doResponse
def getCompanies(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Company)
        res_json = {}
        res_json["companies"] = []
        for obj in objects:
            temp = {}
            temp["id"] = obj.id
            temp["name"] = obj.name
            res_json["companies"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

@doResponse
def getRoleList(request, args=None):
    if args is not None:
        objects = records(ContractDB.session(), Role)
        res_json = {}
        res_json["roles"] = []
        for obj in objects:
            temp = {}
            temp["id"] = obj.id
            temp["name"] = obj.name
            res_json["roles"].append(temp)
        return buildStandResponse(StateCode_Success, res_json)

@doResponse
def getContractList(request, args=None):
    if args is not None:
        project_id = args.get("project_id", -1)
        company_id = args.get("company_id", -1)
        contract_id = args.get("contract_id", -1)
        parent_contract_id = args.get("parent_contract_id", -1)
        if project_id > -1 or company_id > -1 or contract_id > -1 or parent_contract_id > -1:
            conds = []
            if project_id > -1:
                conds.append(Contract.project_id == project_id)

            if company_id > -1:
                conds.append(Contract.company_id == company_id)

            if contract_id > -1:
                conds.append(Contract.id == contract_id)

            if parent_contract_id > -1:
                conds.append(Contract.parent_contract_id == parent_contract_id)

            objs = records(ContractDB.session(), Contract, and_(*conds))

            res_json = {}
            res_json["contracts"] = []
            for cont in objs:
                res = {}
                res["id"] = cont.id
                res["project_id"] = cont.project_id
                res["name"] = cont.name
                res["company_id"] = cont.company_id
                res["retention_money"] = cont.retention_money
                res["retention_money_date"] = cont.retention_money_date
                res["parent_contract_id"] = cont.parent_contract_id
                res["money"] = cont.money
                res["pay_money"] = cont.pay_money
                res["progress"] = cont.progress
                res["second_party_name"] = cont.second_party_name
                res["place_of_performance"] = cont.place_of_performance
                res["date_of_performance"] = cont.date_of_performance
                res["type_of_performance"] = cont.type_of_performance
                res["note"] = cont.note
                files = []
                file_records = records(ContractDB.session(), File, File.contract_id==cont.id)
                for f in file_records:
                    temp = {}
                    temp["filename"] = f.name
                    temp["classify"] = f.classify
                    temp["contract_id"] = f.contract_id
                    temp["note"] = f.note
                    files.append(temp)
                res["files"] = files
                res_json["contracts"].append(res)
            return buildStandResponse(StateCode_Success, res_json)
        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doUpload(request, args=None):
    if args is not None:
        filename = args.get("filename", "")
        filedata = args.get("filedata", "")
        classify = args.get("classify", "")
        contract_id = args.get("contract_id", -1)
        note = args.get("note", "")
        if checkDataVaild(filename) and checkDataVaild(filedata) and contract_id > -1 and checkDataVaild(classify):
            dir = os.path.join(FILE_RESTORE_ROOT_DIR,str(contract_id), classify)
            if not os.path.exists(dir):
                os.makedirs(dir)
            fullpath = os.path.join(dir, filename)

            if os.path.exists(fullpath):
                return buildStandResponse(StateCode_FileExist)

            try:
                with open(fullpath, "wb", ) as f:
                    print("Write file to:", fullpath)
                    filesize = f.write(base64.b64decode(filedata))
                    if filesize > 0:
                        size = addOrRecord(ContractDB.session(), File(contract_id=contract_id, classify=classify, name = filename, note=note))
                        if size > 0:
                            return buildStandResponse(StateCode_Success, {})
                        else:
                            os.remove(fullpath)
                            return buildStandResponse(StateCode_FailedToCreateFileRecord)
                    else:
                        return buildStandResponse(StateCode_FailedToCreateFile)
            except Exception as e:
                return buildStandResponse(StateCode_FailedToCreateFile)

        else:
            return buildStandResponse(StateCode_InvaildParam)

@doResponse
def doCompanyCreate(request, args=None):
    if args is not None:
        name = args.get("name", "")
        if checkDataVaild(name):
            record = records(ContractDB.session(), Company, Company.name == name)
            if len(record) == 0:
                obj = Company(name=name)
                addOrRecord(ContractDB.session(), obj)
                record = records(ContractDB.session(), Company, Company.name == name)
                if len(record) > 0:
                    res = {}
                    res["id"] = record[0].id
                    res["name"] = record[0].name
                    return buildStandResponse(StateCode_Success, res)
                else:
                    return buildStandResponse(StateCode_FailedToCreateCompany)
            else:
                return buildStandResponse(StateCode_CompanyExist)
        else:
            return buildStandResponse(StateCode_InvaildParam)