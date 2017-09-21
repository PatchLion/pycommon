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

# 获取权限列表
@app.route('/api/authority/list', methods=["GET"])
def authority_list():
    return getAuthorityList(request, None)
