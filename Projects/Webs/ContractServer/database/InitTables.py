from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加权限表
addOrRecord(ContractDB.session(), Authority(authority_id = 0, authority_name = "根管理员"))

#增加用户
addOrRecord(ContractDB.session(), User(user_id="admin", password=stringMD5("admin"), name="根管理员", authority_id=0))
