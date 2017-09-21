from flask import request

from Projects.Webs.ContractServer.app import app
from Projects.Webs.ContractServer.app.Businesses import *

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to ContractServer!"

# 注册用户
@app.route('/api/user/register', methods=["POST"])
def regist():
    return doRegister(request, None)

# 登录
@app.route('/api/user/login', methods=["POST"])
def login():
    return doUserLogin(request, None)

# 修改用户权限
@app.route('/api/user/modify/other', methods=["POST"])
def user_modify():
    return doUserModify(request, None)

# 获取权限列表
@app.route('/api/authority/list', methods=["GET"])
def authority_list():
    return getAuthorityList(request, None)

# 获取项目列表
@app.route('/api/project/list', methods=["GET"])
def project_list():
    return getProjectList(request, None)

# 创建项目
@app.route('/api/project/create', methods=["POST"])
def project_create():
    return doProjectCreate(request, None)

# 创建合同
@app.route('/api/contract/create', methods=["POST"])
def contract_create():
    return doContractCreate(request, None)

# 获取合同
@app.route('/api/contract/list', methods=["GET"])
def contract_list():
    return getContractList(request, None)

# 增加合同执行记录
@app.route('/api/contract/history/create', methods=["POST"])
def create_contracts_history():
    return doContractHistory(request, None)