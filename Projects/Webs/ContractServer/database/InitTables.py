from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5, createUuid
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加权限表
addOrRecord(ContractDB.session(), Authority(authority_id = 0, authority_name = "根管理员"))
addOrRecord(ContractDB.session(), Authority(authority_id = 1, authority_name = "管理员"))

#增加用户
addOrRecord(ContractDB.session(), User(user_id="root", password=stringMD5("root"), name="root", authority_id=0))
addOrRecord(ContractDB.session(), User(user_id="admin", password=stringMD5("admin"), name="Adminstrator", authority_id=1))

#增加项目
addOrRecord(ContractDB.session(), Projects(project_name="成都市政项目"))

#增加公司
addOrRecord(ContractDB.session(), Companies(company_name="设计一公司"))

#增加合同
addOrRecord(ContractDB.session(), Contracts(contract_id=createUuid(),contract_name="设计合同", project_id=1, company_id=1))