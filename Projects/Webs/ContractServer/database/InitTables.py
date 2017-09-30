from Projects.Webs.ContractServer.database.ContractDatabase import *
from Projects.Webs.ContractServer.app.Functions import stringMD5, createUuid
from MySqlAlchemy.DBOperator import *


ContractDB.initTables()

#增加角色表
removeRecords(ContractDB.session(), Role)
admin_role_id = createUuid()
test_role1_id = createUuid()
test_role2_id = createUuid()
addOrRecord(ContractDB.session(), Role(name ="管理员")) #管理员权限
addOrRecord(ContractDB.session(), Role(name ="测试角色1")) #
addOrRecord(ContractDB.session(), Role(name ="测试角色2")) #

#增加用户
removeRecords(ContractDB.session(), User)
#addOrRecord(ContractDB.session(), User(user_name="root", password=stringMD5("root"), nick_name="root"))
addOrRecord(ContractDB.session(), User(user_name="admin", password=stringMD5("admin"), nick_name="Adminstrator"))
addOrRecord(ContractDB.session(), User(user_name="simpleLove", password=stringMD5("simpleLove"), nick_name="SimpleLove"))
addOrRecord(ContractDB.session(), User(user_name="patchlion", password=stringMD5("patchlion"), nick_name="打补丁的狮子"))

#增加项目
removeRecords(ContractDB.session(), Project)
addOrRecord(ContractDB.session(), Project(name="成都市政项目", money = 1000000))
addOrRecord(ContractDB.session(), Project(name="三峡大坝项目", money = 100000000))

#增加公司
removeRecords(ContractDB.session(), Company)
addOrRecord(ContractDB.session(), Company(name="设计一公司"))
addOrRecord(ContractDB.session(), Company(name="建设一公司"))

#增加合同
removeRecords(ContractDB.session(), Contract)
addOrRecord(ContractDB.session(), Contract(name="合同1", project_id=1, company_id=1, money=100000, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同2", project_id=1, company_id=1, money=100000, parent_contract_id=1, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同3", project_id=1, company_id=1, money=100000, parent_contract_id=2, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同4", project_id=1, company_id=1, money=100000, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同5", project_id=1, company_id=1, money=100000, parent_contract_id=4, second_party_name="啦啦啦啦啊"))
addOrRecord(ContractDB.session(), Contract(name="合同6", project_id=1, company_id=1, money=100000, parent_contract_id=5, second_party_name="啦啦啦啦啊"))
